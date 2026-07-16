param name string
param location string
param tags object = {}

@description('Search SKU. basic is enough for a single-index portfolio app; standard adds replicas/partitions headroom.')
@allowed(['free', 'basic', 'standard'])
param skuName string = 'basic'

@description('Semantic ranker tier. free = 1000 requests/month; disabled turns it off.')
@allowed(['disabled', 'free', 'standard'])
param semanticSearch string = 'free'

@description('Keyless posture: disable admin/query keys so only Entra ID data-plane auth works.')
param disableLocalAuth bool = true

resource srch 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: name
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  sku: { name: skuName }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    semanticSearch: semanticSearch
    disableLocalAuth: disableLocalAuth
  }
}

output id string = srch.id
output name string = srch.name
output endpoint string = 'https://${srch.name}.search.windows.net'
output identityPrincipalId string = srch.identity.principalId
