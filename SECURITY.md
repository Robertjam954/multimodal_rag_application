# Security

## Reporting a vulnerability

Email security reports to robertjam954@gmail.com. Do not file public issues for security problems.

## In-product safeguards

- Azure AI Content Safety screens prompts and completions when `USE_CONTENT_SAFETY=true`.
- Azure AI Language strips PII at ingestion when `USE_PII_REDACTION=true`.
- Per-IP rate limiting via `RATE_LIMIT_PER_MIN`.
- Per-session token cap via `MAX_TOKENS_PER_SESSION`.
- Adversarial simulation tests run nightly via `evals/safety_evaluation.py`.
- All secrets live in Azure Key Vault; `.env*` files are gitignored.

## Authentication

Optional Entra ID login via MSAL. Per-document ACLs enforced by `@authenticated_path` decorator; managed via `scripts/manageacl.py`.
