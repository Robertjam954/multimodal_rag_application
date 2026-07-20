/*
  Entra ID role assignments for the backend managed identity, scoped to the
  pre-existing ai-tutor data resources. Keyless data-plane access:
  - Cognitive Services OpenAI User  -> Foundry (chat + embeddings)
  - Cosmos DB Built-in Data Contributor -> Cosmos NoSQL (vectors + chat history)
  - Storage Blob Data Contributor   -> Blob storage (files)
  - Key Vault Secrets User          -> Key Vault (secrets)
  - AcrPull                         -> ACR (pull backend image)
  - Search Service Contributor + Search Index Data Contributor -> AI Search
    (backend: runtime hybrid queries + in-process ingestion incl. index create;
     deploying user: local prepdocs.sh runs)
*/

param principalId string
param foundryName string
param cosmosName string
param storageName string
param keyVaultName string
param acrName string
param searchName string = ''
@description('Deploying user objectId; granted search data-plane roles for local prepdocs. Empty skips.')
param userPrincipalId string = ''

// Built-in role definition GUIDs
var roles = {
  openaiUser: '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd' // Cognitive Services OpenAI User (account endpoint: embeddings)
  azureAIUser: '53ca6127-db72-4b80-b1b0-d745d6d5456d' // Azure AI User (project endpoint: chat/Responses + agents)
  blobDataContributor: 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'
  keyVaultSecretsUser: '4633458b-17de-408a-b874-0445c86b69e6'
  acrPull: '7f951dda-4ed3-4680-a7ca-43fe172d538d'
  searchServiceContributor: '7ca78c08-252a-4471-8644-bb5ff32d4ba0' // index create/update (control plane of indexes)
  searchIndexDataContributor: '8ebe5a00-799e-43f5-93ac-243d3dce84a7' // document read/write (data plane)
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

resource azureAIUserRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(foundry.id, principalId, roles.azureAIUser)
  scope: foundry
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.azureAIUser)
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

resource search 'Microsoft.Search/searchServices@2024-06-01-preview' existing = if (!empty(searchName)) {
  name: searchName
}

resource searchSvcContribRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(searchName)) {
  name: guid(searchName, principalId, roles.searchServiceContributor)
  scope: search
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchServiceContributor)
    principalType: 'ServicePrincipal'
  }
}

resource searchDataContribRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(searchName)) {
  name: guid(searchName, principalId, roles.searchIndexDataContributor)
  scope: search
  properties: {
    principalId: principalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchIndexDataContributor)
    principalType: 'ServicePrincipal'
  }
}

resource userSearchSvcContribRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(searchName) && !empty(userPrincipalId)) {
  name: guid(searchName, userPrincipalId, roles.searchServiceContributor)
  scope: search
  properties: {
    principalId: userPrincipalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchServiceContributor)
    principalType: 'User'
  }
}

resource userSearchDataContribRA 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(searchName) && !empty(userPrincipalId)) {
  name: guid(searchName, userPrincipalId, roles.searchIndexDataContributor)
  scope: search
  properties: {
    principalId: userPrincipalId
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', roles.searchIndexDataContributor)
    principalType: 'User'
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
