"""Gene-binary matrix and Sanchez-Vega pathway annotation.

Python implementation of harmonization_spec.md sections 13 and 14, which the GENIE
arm produced with `gnomeR::create_gene_binary()` + `gnomeR::add_pathways()`. gnomeR is
an R package with no Python equivalent and is not installable against the R build on
this machine, so the logic is reimplemented here against the same settings and the
same pathway table (vendored at references/gnomer_sanchez_vega_pathways.csv, taken
from the gnomeR source of truth) so the two cohorts remain comparable.

gnomeR settings reproduced (spec section 13):
    mut_type="somatic_only", include_silent=FALSE, snp_only=FALSE,
    high_level_cna_only=TRUE (+2 Amp / -2 Del only), specify_panel="no",
    recode_aliases="no". Samples absent from the mutation/CNA/SV tables are kept as
    all-zero rows rather than dropped.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

# Non-coding and synonymous consequences carry no oncogenic signal for a gene-binary
# matrix; gnomeR drops them via include_silent=FALSE (spec section 12).
DROPPED_VARIANT_CLASSIFICATIONS = frozenset({
    "Silent", "3'UTR", "5'UTR", "3'Flank", "5'Flank", "Intron", "RNA", "IGR",
})

# GISTIC discrete calls. Only the high-level events become gene-binary columns.
GISTIC_AMPLIFICATION = 2
GISTIC_DEEP_DELETION = -2

AMPLIFICATION_SUFFIX = ".Amp"
DELETION_SUFFIX = ".Del"
FUSION_SUFFIX = ".fus"
# Pathway rows may reference methylation events. No methylation profile is pulled, so
# these never fire - identical to gnomeR's behaviour when no methylation input is given.
METHYLATION_SUFFIX = ".meth"

PATHWAY_COLUMN_PREFIX = "pathway_"


def load_pathway_definitions(path: Path) -> dict[str, list[str]]:
    """Read the gnomeR pathway table into {pathway_name: [alteration, ...]}.

    The table is alteration-level (`TP53.mut`, `MYC.Amp`, ...), one column per pathway,
    padded with NAs to a rectangle.
    """
    table = pd.read_csv(path)
    return {
        pathway: sorted({str(v) for v in table[pathway].dropna()})
        for pathway in table.columns
    }


def _mutation_flags(sample_ids: pd.Index, mutations: pd.DataFrame) -> pd.DataFrame:
    """One 0/1 column per mutated gene, using the bare HUGO symbol as the column name."""
    coding = mutations[~mutations["mutationType"].isin(DROPPED_VARIANT_CLASSIFICATIONS)]
    coding = coding.dropna(subset=["hugoGeneSymbol", "sampleId"])
    print(f"      mutations: {len(mutations):,} -> {len(coding):,} after consequence filter")

    pairs = coding[["sampleId", "hugoGeneSymbol"]].drop_duplicates()
    flags = (
        pd.crosstab(pairs["sampleId"], pairs["hugoGeneSymbol"])
        .clip(upper=1)
        .reindex(sample_ids, fill_value=0)
    )
    return flags.astype("int8")


def _copy_number_flags(sample_ids: pd.Index, cna: pd.DataFrame) -> pd.DataFrame:
    """`<GENE>.Amp` / `<GENE>.Del` columns from high-level GISTIC calls."""
    frames: list[pd.DataFrame] = []
    for alteration, suffix in ((GISTIC_AMPLIFICATION, AMPLIFICATION_SUFFIX),
                               (GISTIC_DEEP_DELETION, DELETION_SUFFIX)):
        subset = cna[cna["alteration"] == alteration]
        pairs = subset[["sampleId", "hugoGeneSymbol"]].drop_duplicates()
        if pairs.empty:
            continue
        flags = (
            pd.crosstab(pairs["sampleId"], pairs["hugoGeneSymbol"])
            .clip(upper=1)
            .reindex(sample_ids, fill_value=0)
        )
        flags.columns = [f"{gene}{suffix}" for gene in flags.columns]
        print(f"      cna {suffix}: {len(subset):,} events, {flags.shape[1]:,} genes")
        frames.append(flags.astype("int8"))
    return pd.concat(frames, axis=1) if frames else pd.DataFrame(index=sample_ids)


def _fusion_flags(sample_ids: pd.Index, structural_variants: pd.DataFrame) -> pd.DataFrame:
    """`<GENE>.fus` columns; an SV flags the gene at either breakpoint."""
    breakpoints: list[pd.DataFrame] = []
    for site_column in ("site1HugoSymbol", "site2HugoSymbol"):
        if site_column not in structural_variants.columns:
            continue
        side = structural_variants[["sampleId", site_column]].rename(
            columns={site_column: "hugoGeneSymbol"}
        )
        breakpoints.append(side)
    if not breakpoints:
        return pd.DataFrame(index=sample_ids)

    pairs = pd.concat(breakpoints, ignore_index=True)
    pairs["hugoGeneSymbol"] = pairs["hugoGeneSymbol"].replace("", pd.NA)
    pairs = pairs.dropna(subset=["sampleId", "hugoGeneSymbol"]).drop_duplicates()
    if pairs.empty:
        return pd.DataFrame(index=sample_ids)

    flags = (
        pd.crosstab(pairs["sampleId"], pairs["hugoGeneSymbol"])
        .clip(upper=1)
        .reindex(sample_ids, fill_value=0)
    )
    flags.columns = [f"{gene}{FUSION_SUFFIX}" for gene in flags.columns]
    print(f"      fusions: {len(pairs):,} sample-gene pairs, {flags.shape[1]:,} genes")
    return flags.astype("int8")


def build_gene_binary(
    sample_ids: pd.Index,
    mutations: pd.DataFrame,
    cna: pd.DataFrame,
    structural_variants: pd.DataFrame,
) -> pd.DataFrame:
    """Assemble the per-sample x per-alteration binary matrix.

    Columns with a zero sum across all samples are dropped, matching gnomeR's default;
    they carry no information and would otherwise inflate the frame by tens of thousands
    of all-zero gene columns.
    """
    print("   building gene binary matrix")
    blocks = [
        _mutation_flags(sample_ids, mutations),
        _copy_number_flags(sample_ids, cna),
        _fusion_flags(sample_ids, structural_variants),
    ]
    matrix = pd.concat([b for b in blocks if not b.empty], axis=1)
    matrix = matrix.loc[:, ~matrix.columns.duplicated()]

    non_empty = matrix.columns[matrix.sum(axis=0) > 0]
    dropped = matrix.shape[1] - len(non_empty)
    matrix = matrix[non_empty]
    print(f"      matrix: {matrix.shape[0]:,} samples x {matrix.shape[1]:,} alterations "
          f"({dropped:,} all-zero columns dropped)")
    return matrix


def add_pathways(
    gene_binary: pd.DataFrame,
    pathway_definitions: dict[str, list[str]],
) -> pd.DataFrame:
    """Append one `pathway_<name>` 0/1 column per pathway.

    A pathway fires when ANY of its member alterations is present in the sample. A
    `<GENE>.mut` entry maps to the bare-symbol mutation column; Amp/Del/fus map to their
    suffixed columns; `.meth` entries are unmatched because no methylation is pulled.
    """
    print("   annotating pathways")
    pathways = pd.DataFrame(index=gene_binary.index)
    for name, alterations in pathway_definitions.items():
        columns: list[str] = []
        unmatched_methylation = 0
        for alteration in alterations:
            gene, _, suffix = alteration.rpartition(".")
            if f".{suffix}" == METHYLATION_SUFFIX:
                unmatched_methylation += 1
                continue
            column = gene if suffix == "mut" else alteration
            if column in gene_binary.columns:
                columns.append(column)
        flag = (
            gene_binary[columns].max(axis=1).astype("int8")
            if columns
            else pd.Series(0, index=gene_binary.index, dtype="int8")
        )
        pathways[f"{PATHWAY_COLUMN_PREFIX}{name}"] = flag
        print(f"      {name:<12s} {len(columns):3d}/{len(alterations):3d} alterations present, "
              f"{int(flag.sum()):4d} samples flagged"
              + (f" ({unmatched_methylation} .meth skipped)" if unmatched_methylation else ""))
    return pathways
