/*
  Main Bicep entry. Provisions a complete multimodal RAG environment:
  - Azure OpenAI (chat + embeddings)
  - Azure AI Search
  - Azure Document Intelligence
  - Azure Speech
  - Azure AI Vision (multimodal)
  - Azure AI Content Safety
  - Azure AI Foundry Hub + Project
  - Storage (Blob + ADLS Gen2 for user uploads)
  - Cosmos DB (SQL for chat history + Gremlin for knowledge graph)
  - Log Analytics + Application Insights
  - Key Vault
  - Container Apps environment + backend
  - Functions app (for cloud ingestion skills)
*/

targetScope = 'subscription'

param environmentName string
param location string = deployment().location
param principalId string = ''

@description('Azure OpenAI deployments')
param chatGptDeploymentName string = 'gpt-4.1-mini'
param chatGptModelName string = 'gpt-4.1-mini'
param chatGptModelVersion string = '2025-04-14'
param embeddingDeploymentName string = 'text-embedding-3-large'
param embeddingModelName string = 'text-embedding-3-large'

param searchIndexName string = 'rag-index'
param useMultimodal bool = false
param useGraphRag bool = true
param useVerifier bool = true
param useHierarchicalAgents bool = false
param useVoiceDemo bool = true
param useSqlDemo bool = true
param useContentSafety bool = false
param useFeedback bool = true
param rateLimitPerMin int = 30
param maxTokensPerSession int = 200000
param openaiFileSearchVectorStoreId string = ''
param langsmithProject string = 'multimodal-rag'

var tags = { 'azd-env-name': environmentName }
var abbrs = loadJsonContent('abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-${environmentName}'
  location: location
  tags: tags
}

module logAnalytics 'core/monitor/log-analytics.bicep' = {
  name: 'log'
  scope: rg
  params: {
    name: '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    location: location
    tags: tags
  }
}

module appInsights 'core/monitor/applicationinsights.bicep' = {
  name: 'ai'
  scope: rg
  params: {
    name: '${abbrs.insightsComponents}${resourceToken}'
    location: location
    tags: tags
    workspaceResourceId: logAnalytics.outputs.id
  }
}

module keyvault 'core/security/keyvault.bicep' = {
  name: 'kv'
  scope: rg
  params: {
    name: '${abbrs.keyVaultVaults}${resourceToken}'
    location: location
    tags: tags
    principalId: principalId
  }
}

module openai 'core/ai/openai.bicep' = {
  name: 'openai'
  scope: rg
  params: {
    name: '${abbrs.cognitiveServicesAccounts}oai-${resourceToken}'
    location: location
    tags: tags
    chatDeployment: { name: chatGptDeploymentName, model: chatGptModelName, version: chatGptModelVersion, capacity: 30 }
    embedDeployment: { name: embeddingDeploymentName, model: embeddingModelName, version: '1', capacity: 100 }
  }
}

module search 'core/search/search-services.bicep' = {
  name: 'search'
  scope: rg
  params: {
    name: '${abbrs.searchSearchServices}${resourceToken}'
    location: location
    tags: tags
  }
}

module docintel 'core/ai/documentintelligence.bicep' = {
  name: 'docintel'
  scope: rg
  params: {
    name: '${abbrs.cognitiveServicesAccounts}di-${resourceToken}'
    location: location
    tags: tags
  }
}

module speech 'core/ai/speech.bicep' = if (useVoiceDemo) {
  name: 'speech'
  scope: rg
  params: {
    name: '${abbrs.cognitiveServicesAccounts}sp-${resourceToken}'
    location: location
    tags: tags
  }
}

module vision 'core/ai/vision.bicep' = if (useMultimodal) {
  name: 'vision'
  scope: rg
  params: {
    name: '${abbrs.cognitiveServicesAccounts}vis-${resourceToken}'
    location: location
    tags: tags
  }
}

module contentSafety 'core/ai/contentsafety.bicep' = if (useContentSafety) {
  name: 'safety'
  scope: rg
  params: {
    name: '${abbrs.cognitiveServicesAccounts}cs-${resourceToken}'
    location: location
    tags: tags
  }
}

module storage 'core/storage/storage-account.bicep' = {
  name: 'storage'
  scope: rg
  params: {
    name: '${abbrs.storageStorageAccounts}${resourceToken}'
    location: location
    tags: tags
    containers: ['content', 'user-content', 'figures', 'recordings']
    enableHnsForUserContent: true
  }
}

module cosmosSql 'core/cosmos/cosmos-sql.bicep' = {
  name: 'cosmos-sql'
  scope: rg
  params: {
    name: '${abbrs.documentDBDatabaseAccounts}sql-${resourceToken}'
    location: location
    tags: tags
    databaseName: 'chat'
    containerName: 'history'
  }
}

module cosmosGremlin 'core/cosmos/cosmos-gremlin.bicep' = if (useGraphRag) {
  name: 'cosmos-gremlin'
  scope: rg
  params: {
    name: '${abbrs.documentDBDatabaseAccounts}kg-${resourceToken}'
    location: location
    tags: tags
    databaseName: 'kg'
    graphName: 'graph'
  }
}

module containerEnv 'core/host/container-apps-environment.bicep' = {
  name: 'caenv'
  scope: rg
  params: {
    name: '${abbrs.appManagedEnvironments}${resourceToken}'
    location: location
    tags: tags
    logAnalyticsWorkspaceName: logAnalytics.outputs.name
  }
}

module backend 'app/backend.bicep' = {
  name: 'backend'
  scope: rg
  params: {
    name: '${abbrs.appContainerApps}backend-${resourceToken}'
    location: location
    tags: union(tags, { 'azd-service-name': 'backend' })
    containerAppsEnvironmentId: containerEnv.outputs.id
    appInsightsConnectionString: appInsights.outputs.connectionString
    env: [
      { name: 'AZURE_OPENAI_SERVICE', value: openai.outputs.name }
      { name: 'AZURE_OPENAI_CHATGPT_DEPLOYMENT', value: chatGptDeploymentName }
      { name: 'AZURE_OPENAI_EMB_DEPLOYMENT', value: embeddingDeploymentName }
      { name: 'AZURE_SEARCH_SERVICE', value: search.outputs.name }
      { name: 'AZURE_SEARCH_INDEX', value: searchIndexName }
      { name: 'AZURE_DOCUMENTINTELLIGENCE_ENDPOINT', value: docintel.outputs.endpoint }
      { name: 'AZURE_STORAGE_ACCOUNT', value: storage.outputs.name }
      { name: 'AZURE_STORAGE_CONTAINER', value: 'content' }
      { name: 'AZURE_USER_STORAGE_ACCOUNT', value: storage.outputs.name }
      { name: 'AZURE_USER_STORAGE_CONTAINER', value: 'user-content' }
      { name: 'AZURE_COSMOSDB_ENDPOINT', value: cosmosSql.outputs.endpoint }
      { name: 'AZURE_COSMOSDB_CHAT_DATABASE', value: 'chat' }
      { name: 'AZURE_COSMOSDB_CHAT_CONTAINER', value: 'history' }
      { name: 'AZURE_COSMOSDB_ACCOUNT', value: useGraphRag ? cosmosGremlin.outputs.name : '' }
      { name: 'AZURE_COSMOSDB_GRAPH_DATABASE', value: 'kg' }
      { name: 'AZURE_COSMOSDB_GRAPH_CONTAINER', value: 'graph' }
      { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsights.outputs.connectionString }
      { name: 'USE_MULTIMODAL', value: string(useMultimodal) }
      { name: 'USE_GRAPHRAG', value: string(useGraphRag) }
      { name: 'USE_VERIFIER', value: string(useVerifier) }
      { name: 'USE_VOICE_DEMO', value: string(useVoiceDemo) }
      { name: 'USE_SQL_DEMO', value: string(useSqlDemo) }
      { name: 'USE_CONTENT_SAFETY', value: string(useContentSafety) }
      { name: 'USE_FEEDBACK', value: string(useFeedback) }
      { name: 'RATE_LIMIT_PER_MIN', value: string(rateLimitPerMin) }
      { name: 'MAX_TOKENS_PER_SESSION', value: string(maxTokensPerSession) }
      { name: 'OPENAI_FILE_SEARCH_VECTOR_STORE_ID', value: openaiFileSearchVectorStoreId }
      { name: 'LANGSMITH_PROJECT', value: langsmithProject }
      { name: 'RUNNING_IN_PRODUCTION', value: 'true' }
    ]
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = rg.name
output AZURE_OPENAI_SERVICE string = openai.outputs.name
output AZURE_SEARCH_SERVICE string = search.outputs.name
output AZURE_DOCUMENTINTELLIGENCE_ENDPOINT string = docintel.outputs.endpoint
output AZURE_STORAGE_ACCOUNT string = storage.outputs.name
output APPLICATIONINSIGHTS_CONNECTION_STRING string = appInsights.outputs.connectionString
output BACKEND_URI string = backend.outputs.uri
