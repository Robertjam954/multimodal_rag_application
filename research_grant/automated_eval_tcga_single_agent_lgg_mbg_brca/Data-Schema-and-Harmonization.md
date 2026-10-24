# Data schema and harmonization

## Active schema boundary

There is no implemented canonical BRCA analytic frame yet. The current BRCA pull writes
raw, public cBioPortal snapshot tables and a manifest under `data/raw/cbioportal/`.
Its wide clinical tables retain cBioPortal field names; they are not a validated
brain-metastasis or survival schema.

The target analytic record is staged and evidence-linked JSON, specified in
[`docs/brca_staged_extraction_and_evaluation.md`](docs/brca_staged_extraction_and_evaluation.md):

1. Source inventory.
2. Patient and primary-sample linkage.
3. Clinical timeline, including explicit observed, not-recorded, ambiguous, and
   conflicting statuses.
4. Non-silent molecular profile and pathway indicators.
5. Derived analytic record with cross-field validation and provenance.

No Pydantic models, Instructor calls, pathway mapper, or harmonizer implements this
contract today. In particular, an absent source field must not become a negative
brain-metastasis finding.

## LGG and GBM workflow schema

`compare_tcga_lgg_gbm.R` works directly from the GDC query inventory and masked MAF
data. Its analytical unit is one selected sample-type-01 primary tumor per patient.
The output tables contain patient denominators, mutation counts and prevalence, Fisher
test p-values, BH q-values, and continuity-corrected odds ratios. Prevalence ratios and
their confidence intervals are planned additions, not current columns.

## Historical schema specification

`data collection and processing/harmonization_spec.md` and its copy below `src/`
describe a prior GENIE-oriented sample-level CSV schema. They remain historical
reference material only. Their derived brain-metastasis flags and survival endpoints
must not be applied to TCGA-BRCA without a new, validated implementation and a source
field audit.
