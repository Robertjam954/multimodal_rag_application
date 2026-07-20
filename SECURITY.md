# Security

## Reporting a vulnerability

Email security reports to robertjam954@gmail.com. Do not file public issues for security problems.

## Cloud identity and secrets

- The deployed backend authenticates to Azure services with **keyless Entra ID** only.
  The Container App runs under a system-assigned managed identity; data-plane access is
  granted via Azure RBAC role assignments in `infra/app/rbac.bicep` (Cognitive Services
  OpenAI User, Azure AI User, Cosmos DB Built-in Data Contributor, Storage Blob Data
  Contributor, Key Vault Secrets User, AcrPull). There are no API keys in the deployed
  configuration.
- In code, credentials come from `DefaultAzureCredential` / `ManagedIdentityCredential`
  (production) or `AzureDeveloperCliCredential` (local). No secrets are hardcoded in the
  Python source.
- `.env*` files are git-ignored and used for local development only. Any keys referenced
  by optional integrations (for example a local Redis URL) live there and must not be
  committed.

## In-product safeguards

- Azure AI Content Safety screens prompts and completions when `USE_CONTENT_SAFETY=true`
  (off in the current deployment).
- Azure AI Language / regex strips PII at ingestion when `USE_PII_REDACTION=true`
  (off in the current deployment).
- Per-IP rate limiting via `RATE_LIMIT_PER_MIN` (`decorators.py`).
- Per-session token cap via `MAX_TOKENS_PER_SESSION` (`core/costmeter.py`).
- An adversarial-simulation harness is available at `evals/safety_evaluation.py`.

## Application login

Optional Entra ID login via MSAL, enabled with `AZURE_USE_AUTHENTICATION=true`. Per-document
ACLs are managed via `scripts/manageacl.py`.
