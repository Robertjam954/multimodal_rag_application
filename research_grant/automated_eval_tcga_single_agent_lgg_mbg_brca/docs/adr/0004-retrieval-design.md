# ADR-0004: Retrieval over rendered TCGA cards, model outputs, and PubMed abstracts

Date: 2026-09-02
Status: accepted

## Context

The agents need one retrieval surface over three very different kinds of evidence:

1. **Structured TCGA cohort data** from cBioPortal (`brca_tcga_pan_can_atlas_2018`) -
   clinical attributes, mutations, copy-number alterations. Tabular, not prose.
2. **Model outputs** - the CBBio driver-gene ensemble rankings and SHAP attributions
   ported from `genie_impact_tcga_brain_mets/src/modeling/cbbio/`. Also tabular, and
   *derived*, so provenance must distinguish a computed result from an observed fact.
3. **PubMed abstracts** scoped to TCGA BRCA biology. Genuine prose.

Embedding raw table rows is a known failure: a CSV row of gene symbols and z-scores has
almost no semantic surface for a text embedder, so retrieval collapses to keyword luck.
Meanwhile the whole benchmark depends on retrieval being **identical across arms**
(ADR-0003), so this component is shared infrastructure and its configuration is pinned.

Two more constraints. Claims must be **verifiable to a specific row or span**, because
citation faithfulness is a reported metric and an unresolvable citation cannot be
scored. And the repo is local-first for phase 1, so the store must run with no
infrastructure while leaving a clean path to the portfolio's stated primary
(Postgres + pgvector).

## Decision

**Render structured data into text cards before embedding.** `src/rag/render_cards.py`
emits self-contained natural-language documents rather than serialized rows:

- *Gene cards* - one per gene: alteration frequency in the cohort, mutation types,
  CNA distribution, co-occurring alterations, and the gene's driver-ensemble rank and
  SHAP importance when present.
- *Cohort-slice cards* - one per clinically meaningful stratum (subtype, stage, receptor
  status): n, demographic and clinical distributions, top altered genes.
- *Result cards* - one per model output: the driver-gene ensemble ranking, SHAP global
  importance, and per-feature dependence findings, each stating the model, the features,
  and the cohort it was fit on.
- *Paper cards* - title, abstract, journal, year, PMID.

Every card carries structured provenance in its metadata - `source` (`cbioportal` /
`derived` / `pubmed`), `table`, `row_ids`, `pmid`, and the snapshot date - so
`cite_evidence` resolves a claim to `study/table/row` or `pmid/span`. The
`derived` marker is load-bearing: it is what stops the agent presenting a SHAP
attribution as an observed clinical fact.

**Cards are generated, not authored.** They are a deterministic function of the cohort
parquet and the model outputs, regenerable from a clean checkout, and hashed into the
experiment metadata so a corpus change is detectable.

**Store: SQLite + `sqlite-vec`** (`src/rag/vector_store.py`), behind a narrow
`VectorStore` interface (`upsert`, `search`, `get_by_id`). Zero infrastructure, sits in
the same file-based stack as the Chainlit SQLAlchemy run store, and the interface keeps
the pgvector swap a store-layer change rather than a retrieval-logic rewrite.

**Embedding and chunking.** OpenAI `text-embedding-3-large`. Cards are written to be
individually coherent and are embedded whole where they fit the context budget; only
long paper cards and long result cards are chunked, with the parent card id retained so
a chunk hit resolves to its source. Model, dimensions, chunk size, and overlap are
recorded in `docs/experiment_metadata.md` and pinned under ADR-0003.

**Retrieval.** Dense top-k by default, with metadata filtering by `source` and card
type so a tool can scope a search to structured evidence or to literature. Hybrid
(dense + BM25) is implemented behind the same interface but **off by default in phase
1**: enabling it is a configuration change that invalidates cross-arm comparison, so it
is a decision to make once, before the phase-1 freeze, not an experiment knob.

**Retrieval is not an arm property.** All agents call the same `search_corpus` against
the same index with the same parameters.

## Consequences

- Structured cohort data becomes genuinely retrievable, and a single query can return
  a gene card, a SHAP result card, and a supporting abstract - which is what makes
  cross-referencing tasks possible at all.
- Citations resolve to rows and spans, so citation faithfulness is measurable rather
  than aspirational, and derived results cannot masquerade as observations.
- Card rendering is a real component with real failure modes: a bug in the renderer
  silently degrades every arm equally, so it needs its own tests (row counts, spot
  checks against the parquet) rather than being treated as glue.
- Card granularity is a judgment call baked in early. Cards too coarse hide detail;
  too fine and retrieval fragments. Changing it after the phase-1 freeze costs a
  full re-run.
- `sqlite-vec` brute-forces search. Fine at this corpus size (thousands of cards),
  and it would not be at millions - the interface exists for that day.
- Keeping hybrid off by default means phase 1 may under-retrieve on rare gene symbols,
  where lexical matching would help. Accepted to keep one pinned configuration.
- **Rejected: embedding raw CSV rows** - no semantic surface, retrieval degenerates.
- **Rejected: a separate index per source type** - forces the agent to choose an index
  before it knows what it needs, and makes cross-source synthesis a multi-tool dance.
- **Rejected: GraphRAG** (as used in `agentic_research_team`) - its community summaries
  suit an unstructured paper corpus, but the cohort here is already relational, and
  indexing cost is one LLM call per chunk, which is hard to justify when the structure
  is not being discovered but is known in advance.

## References

- `src/rag/render_cards.py`, `src/rag/{chunk,embed,vector_store,retrievers}.py` (to be built)
- `src/ingest/build_cohort.py` - the parquet the cards are rendered from
- Ported from: `genie_impact_tcga_brain_mets/src/modeling/cbbio/`, `plot_shap.py`
- Pattern lineage: `llm_summarization_br_ca/src/rag/`
- [ADR-0003](0003-benchmark-protocol.md) - why this configuration is pinned
- [ADR-0002](0002-single-react-agent-research-baseline.md) - `search_corpus` and `cite_evidence`
