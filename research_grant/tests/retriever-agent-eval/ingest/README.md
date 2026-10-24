# Ingestion

Place reusable, public-TCGA ingestion code here. Each loader must create a
snapshot-dated, checksum-manifested JSON payload below gitignored `data/raw/`.

The implemented BRCA cBioPortal pull remains at
`src/data collection and processing/pull_tcga_brca_cbioportal.py` until it is
refactored with tests into this package. Do not duplicate it here.

`stage_aim1_result_tables.py` is implemented here. It validates five supplied,
table-specific CSV layouts against the static JSON contract in
`schemas/aim1_result_tables.schema.json`, then atomically publishes JSON record arrays
and a manifest below gitignored `data/processed/aim1/`. This is staging of supplied
aggregates, not an analysis implementation. All five inputs must be distinct by
filesystem identity: device and inode identify files, with the resolved path used only
when an inode is unavailable. Hard-linked source CSVs are therefore rejected.
