/*
  Entra ID role assignments for the backend managed identity, scoped to the
  pre-existing ai-tutor data resources. Keyless data-plane access:
  - Cognitive Services OpenAI User  -> Foundry (chat + embeddings)
  - Cosmos DB Built-in Data Contributor -> Cosmos NoSQL (vectors + chat history)
  - Storage Blob Data Contributor   -> Blob storage (files)
  - Key Vault Secrets User          -> Key Vault (secrets)
  - AcrPull                         -> ACR (pull backend image)
*/

param principalId string
param foundryName string
param cosmosName string
param storageName string
param keyVaultName string
param acrName string

// Built-in role definition GUIDs
var roles = {
  openaiUser: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd'
  blobDataContributor: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
  keyVaultSecretsUser: '4633458b-17de-408a-b874-0445c86b69e6'
  acrPull: '7f951dda-4ed3-4680-a7ca-43fe172d538d'
}
var cosmosDataContributorId = '00000000-0000-0000-0000-000000000002'

resource foundry 'Microsoft.CognitiveServices/accounts@2024-10-01' existing = { name: foundryName }
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-08-15' existing = { name: cosmosName }
resource storage 'Microsoft.Storage/storageAccounts@2024-01-01' existing = { name: storageName }
resource keyvault 'Microsoft.KeyVault/vaults@2023-07-01' existing = { name: keyVaultName }
resource acr 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' existing = { name: acrName }

resource openaiUserRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundry.id, principalId, roles.openaiUser)
  scope: foundry
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.openaiUser)
    principalType: 'ServicePrincipal'
  }
}

resource blobRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(storage.id, principalId, roles.blobDataContributor)
  scope: storage
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.blobDataContributor)
    principalType: 'ServicePrincipal'
  }
}

resource kvRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyvault.id, principalId, roles.keyVaultSecretsUser)
  scope: keyvault
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.keyVaultSecretsUser)
    principalType: 'ServicePrincipal'
  }
}

resource acrRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, principalId, roles.acrPull)
  scope: acr
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.acrPull)
    principalType: 'ServicePrincipal'
  }
}

// Cosmos data-plane RBAC uses a dedicated sub-resource (not Microsoft.Authorization).
resource cosmosDataRA 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-08-15' = {
  parent: cosmos
  name: guid(cosmos.id, principalId, cosmosDataContributorId)
  properties: {
    roleDefinitionId: '${cosmos.id}/sqlRoleDefinitions/${cosmosDataContributorId}'
    principalId: principalId
    scope: cosmos.id
  }
}
