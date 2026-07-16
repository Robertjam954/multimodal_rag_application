/*
  Main Bicep entry — Stage 1 deploy against the EXISTING `ai-tutor` resources.
  Provisions only the missing compute/observability and wires the backend
  (keyless / Entra ID) to the pre-existing Foundry, Cosmos (vector + history),
  Blob storage, and Key Vault.

  New: Log Analytics, Application Insights, ACR, Container Apps Environment,
       backend Container App, RBAC role assignments.
  Existing (referenced): ai-tutor-foundry, cosmosdbaitutor7a79c7,
       azureblobstorageai, Key Vault `ai-tutor`.
*/

targetScope = 'resourceGroup'

param environmentName string
param location string = resourceGroup().location
@description('Deploying user objectId (optional; reserved for dev grants).')
param principalId string = ''

@description('Existing ai-tutor resources')
param foundryName string = 'ai-tutor-foundry'
param foundryProjectName string = 'ai-tutor-ms-azure-proj'
param cosmosAccountName string = 'cosmosdbaitutor7a79c7'
param storageAccountName string = 'azureblobstorageai'
param keyVaultName string = 'ai-tutor'

@description('Model deployments already present on the Foundry account')
param chatGptDeploymentName string = 'gpt-4o-mini'
param embeddingDeploymentName string = 'text-embedding-3-large'

@description('Azure AI Search: optional runtime retrieval backend. Off by default (local Obsidian RAG is the active direction); flip on to provision the service.')
param useAzureSearch bool = false
param searchServiceName string = ''
param searchIndexName string = 'rag-index'
@allowed(['free', 'basic', 'standard'])
param searchSkuName string = 'basic'
@allowed(['disabled', 'free', 'standard'])
param searchSemanticSearch string = 'free'
@description('Primary retrieval backend for the container: azure_search or cosmos.')
@allowed(['azure_search', 'cosmos'])
param documentRetriever string = 'cosmos'

param useVerifier bool = true
param useFeedback bool = true
param rateLimitPerMin int = 30
param maxTokensPerSession int = 200000
param langsmithProject string = 'multimodal-rag'

var tags = { 'azd-env-name': environmentName }
var abbrs = loadJsonContent('abbreviations.json')
var resourceToken = toLower(uniqueString(resourceGroup().id, environmentName))
var foundryServicesEndpoint = 'https://${foundryName}.services.ai.azure.com'
var foundryProjectEndpoint = '${foundryServicesEndpoint}/api/projects/${foundryProjectName}'

// ---- Existing data resources (referenced, not created) ----
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-08-15' existing = {
  name: cosmosAccountName
}

// ---- New compute / observability ----
module logAnalytics 'core/monitor/log-analytics.bicep' = {
  name: 'log'
  params: {
    name: '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    location: location
    tags: tags
  }
}

module appInsights 'core/monitor/applicationinsights.bicep' = {
  name: 'appi'
  params: {
    name: '${abbrs.insightsComponents}${resourceToken}'
    location: location
    tags: tags
    workspaceResourceId: logAnalytics.outputs.id
  }
}

module acr 'core/host/container-registry.bicep' = {
  name: 'acr'
  params: {
    name: 'acr${resourceToken}'
    location: location
    tags: tags
  }
}

module containerEnv 'core/host/container-apps-environment.bicep' = {
  name: 'caenv'
  params: {
    name: '${abbrs.appManagedEnvironments}${resourceToken}'
    location: location
    tags: tags
    logAnalyticsWorkspaceName: logAnalytics.outputs.name
  }
}

module search 'core/search/search-services.bicep' = if (useAzureSearch) {
  name: 'search'
  params: {
    name: !empty(searchServiceName) ? searchServiceName : '${abbrs.searchSearchServices}${resourceToken}'
    location: location
    tags: tags
    skuName: searchSkuName
    semanticSearch: searchSemanticSearch
  }
}

module backend 'app/backend.bicep' = {
  name: 'backend'
  params: {
    name: '${abbrs.appContainerApps}backend-${resourceToken}'
    location: location
    tags: union(tags, { 'azd-service-name': 'backend' })
    containerAppsEnvironmentId: containerEnv.outputs.id
    appInsightsConnectionString: appInsights.outputs.connectionString
    containerRegistryName: acr.outputs.name
    env: [
      // Chat / Responses -> Foundry PROJECT endpoint (ai.azure.com audience)
      { name: 'AZURE_OPENAI_ENDPOINT', value: foundryProjectEndpoint }
      { name: 'AZURE_OPENAI_AAD_SCOPE', value: 'https://ai.azure.com/.default' }
      { name: 'AZURE_AI_PROJECT_ENDPOINT', value: foundryProjectEndpoint }
      { name: 'FOUNDRY_PROJECT_ENDPOINT', value: foundryProjectEndpoint }
      // Embeddings -> Foundry ACCOUNT endpoint (cognitiveservices audience; project path 404s for embeddings)
      { name: 'AZURE_OPENAI_EMBEDDING_ENDPOINT', value: foundryServicesEndpoint }
      { name: 'AZURE_OPENAI_EMBEDDING_AAD_SCOPE', value: 'https://cognitiveservices.azure.com/.default' }
      { name: 'AZURE_OPENAI_USE_AAD', value: 'true' }
      { name: 'AZURE_OPENAI_CHATGPT_DEPLOYMENT', value: chatGptDeploymentName }
      { name: 'AZURE_AI_MODEL_DEPLOYMENT_NAME', value: chatGptDeploymentName }
      { name: 'AZURE_OPENAI_EMBEDDING_DEPLOYMENT', value: embeddingDeploymentName }
      { name: 'AZURE_OPENAI_EMB_DEPLOYMENT', value: embeddingDeploymentName }
      { name: 'DOCUMENT_RETRIEVER', value: documentRetriever }
      { name: 'AZURE_SEARCH_SERVICE', value: useAzureSearch ? search!.outputs.name : '' }
      { name: 'AZURE_SEARCH_INDEX', value: searchIndexName }
      { name: 'AZURE_SEARCH_SEMANTIC_RANKER', value: (useAzureSearch && searchSemanticSearch != 'disabled') ? 'true' : 'false' }
      { name: 'AZURE_COSMOSDB_ENDPOINT', value: cosmos.properties.documentEndpoint }
      { name: 'AZURE_COSMOSDB_VECTOR_DATABASE', value: 'rag' }
      { name: 'AZURE_COSMOSDB_VECTOR_CONTAINER', value: 'documents' }
      { name: 'AZURE_COSMOSDB_CHAT_DATABASE', value: 'chat' }
      { name: 'AZURE_COSMOSDB_CHAT_CONTAINER', value: 'history' }
      { name: 'USE_CHAT_HISTORY_COSMOS', value: 'true' }
      { name: 'AZURE_STORAGE_ACCOUNT', value: storageAccountName }
      { name: 'AZURE_STORAGE_CONTAINER', value: 'content' }
      { name: 'AZURE_USER_STORAGE_ACCOUNT', value: storageAccountName }
      { name: 'AZURE_USER_STORAGE_CONTAINER', value: 'user-content' }
      { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsights.outputs.connectionString }
      { name: 'USE_GRAPHRAG', value: 'false' }
      { name: 'USE_MULTIMODAL', value: 'false' }
      { name: 'USE_VOICE_DEMO', value: 'false' }
      { name: 'USE_SQL_DEMO', value: 'false' }
      { name: 'USE_CONTENT_SAFETY', value: 'false' }
      { name: 'USE_PII_REDACTION', value: 'false' }
      { name: 'USE_VECTOR_SEARCH', value: 'true' }
      { name: 'USE_VERIFIER', value: string(useVerifier) }
      { name: 'USE_FEEDBACK', value: string(useFeedback) }
      { name: 'RATE_LIMIT_PER_MIN', value: string(rateLimitPerMin) }
      { name: 'MAX_TOKENS_PER_SESSION', value: string(maxTokensPerSession) }
      { name: 'LANGSMITH_PROJECT', value: langsmithProject }
      { name: 'RUNNING_IN_PRODUCTION', value: 'true' }
    ]
  }
}

module rbac 'app/rbac.bicep' = {
  name: 'rbac'
  params: {
    principalId: backend.outputs.identityPrincipalId
    foundryName: foundryName
    cosmosName: cosmosAccountName
    storageName: storageAccountName
    keyVaultName: keyVaultName
    acrName: acr.outputs.name
    searchName: useAzureSearch ? search!.outputs.name : ''
    userPrincipalId: principalId
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = resourceGroup().name
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = acr.outputs.loginServer
output AZURE_CONTAINER_REGISTRY_NAME string = acr.outputs.name
output APPLICATIONINSIGHTS_CONNECTION_STRING string = appInsights.outputs.connectionString
output AZURE_OPENAI_ENDPOINT string = foundryServicesEndpoint
output AZURE_AI_PROJECT_ENDPOINT string = foundryProjectEndpoint
output AZURE_COSMOSDB_ENDPOINT string = cosmos.properties.documentEndpoint
output AZURE_SEARCH_SERVICE string = useAzureSearch ? search!.outputs.name : ''
output AZURE_SEARCH_ENDPOINT string = useAzureSearch ? search!.outputs.endpoint : ''
output AZURE_SEARCH_INDEX string = searchIndexName
output CLOUD_DOCUMENT_RETRIEVER string = documentRetriever
output BACKEND_URI string = backend.outputs.uri
