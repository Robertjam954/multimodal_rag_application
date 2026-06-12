#!/usr/bin/env bash
# Assigns role-based access for the deployer / managed identity. Run after `azd up`.
set -euo pipefail
echo "Stub: assign Search Index Data Contributor, Cognitive Services User, Storage Blob Data Contributor, Cosmos DB Built-in Data Contributor."
echo "Implementation deferred to infra/core/security/role.bicep modules invoked from main.bicep."
