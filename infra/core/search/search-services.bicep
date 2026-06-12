param name string
param location string
param tags object = {}

resource srch 'Microsoft.Search/searchServices@2024-06-01-preview' = {
  name: name
  location: location
  tags: tags
  sku: { name: 'standard' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    semanticSearch: 'standard'
  }
}

output id string = srch.id
output name string = srch.name
output endpoint string = 'https://${srch.name}.search.windows.net'
