# Status

> Project: **TCGA glioma and BRCA analysis** - Stage: **analysis and extraction design**

## Governance and reproducibility
- [x] ADR convention and benchmark constraints documented
- [x] TCGA-only, public-data scope documented
- [x] `tests/unit/test_json_staging_and_evaluation.py` has 13 passing tests for JSON normalization, strict decoding including exponent overflow, clinical duplicate-pair rejection, retry auditing, manifest metadata, Aim 1 named-schema validation including intended-empty arrays, and three-model inference
- [ ] Freeze source snapshots, mutation definitions, pathway map, and analytic thresholds
- [ ] Run the required missingness and merge-diagnostics audits

## 1. LGG versus GBM EDA
- [x] GDC MAF pull and Fisher-test workflow implemented
- [ ] Execute and archive a snapshot-dated LGG/GBM run
- [ ] Add prevalence-ratio confidence intervals to the result workflow
- [ ] Add gene and pathway correlation analysis
- [ ] Add prespecified logistic-regression analysis
- [ ] Create final EDA notebook and publication figures

## Supplied Aim 1 aggregate-table staging
- [x] Static JSON Schema contract for the five supplied Aim 1 table layouts added
- [x] Atomic CSV-to-JSON staging utility with manifest, bounded previews, named table-schema and cross-field validation, UUID-prefixed attachment support, and intended-empty-array support implemented
- [x] Local `data/processed/aim1/` JSON staging output created from supplied aggregates
- [ ] Verify the supplied aggregate provenance and use only after the related analysis scope is documented

## 2. BRCA staged JSON extraction
- [x] Extraction stages, output contract, golden cases, and evaluation strategy documented
- [x] Public cBioPortal BRCA snapshot-pull script implemented
- [x] Stage 0 JSON normalizer and cBioPortal pull emit canonical pre-normalization source-checksum provenance and pass strict Draft 2020-12 report validation
- [x] Three-model JSON extraction-accuracy comparison utility with strict schema validation implemented
- [ ] Execute and archive a manifest-backed BRCA source snapshot
- [ ] Run Stage 0 on a BRCA source snapshot and archive its JSON report
- [ ] Define Pydantic models and semantic validators
- [ ] Implement JSON-first staged extraction with Instructor, including JSON or JSON Lines artifacts only
- [ ] Create manually adjudicated golden cases
- [ ] Implement code-based Pydantic Evals with typed cases, schema validation, exact-match checks, and accuracy reporting
- [ ] Create one immutable golden JSON dataset and three comparable prediction payloads, then run the comparison utility
- [ ] Run error analysis and freeze the extraction version

## 3. BRCA brain-metastasis analysis
- [ ] Pull and stage public TCGA-BRCA clinical and mutation data
- [ ] Finalize and audit the brain-metastasis-ever definition
- [ ] Estimate gene and pathway prevalence ratios and regression models
- [ ] Analyze time to brain metastasis, recurrence, and overall survival
- [ ] Compare top-five mutated-gene groups within brain-metastasis cases

## 4. Cross-cohort comparison
- [ ] Harmonize BRCA brain-metastasis and GBM mutation features
- [ ] Compare gene and pathway mutation prevalence and overlap

## 5. Deliverables
- [x] Create final-notebook directory and notebook project scaffold
- [ ] Execute `01_lgg_gbm_mutation_pathway_eda.ipynb`
- [ ] Execute `02_brca_staged_structured_extraction.ipynb`
- [ ] Execute `03_brca_brain_metastasis_and_survival.ipynb`
- [ ] Execute `04_brca_brain_met_vs_gbm.ipynb`
- [ ] Generate final tables and PDF plus 600 DPI PNG figures
