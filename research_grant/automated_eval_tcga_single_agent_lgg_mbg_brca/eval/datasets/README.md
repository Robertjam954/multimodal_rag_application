# Evaluation datasets

Store versioned, manually adjudicated JSON golden cases for the staged extraction
pipeline here. Use JSON Lines only when the dataset is batched. Each case records the
bounded input, expected schema-valid output, expected numeric features, and metadata.

Do not store source patient records or model output from real TCGA cases in this
directory.
