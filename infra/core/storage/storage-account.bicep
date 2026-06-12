param name string
param location string
param tags object = {}
param containers array = []
param enableHnsForUserContent bool = false

resource sa 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: name
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    isHnsEnabled: enableHnsForUserContent
    minimumTlsVersion: 'TLS1_2'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' = {
  parent: sa
  name: 'default'
  properties: {}
}

resource containerResources 'Microsoft.Storage/storageAccounts/blobServices/containers@2024-01-01' = [for c in containers: {
  parent: blobService
  name: c
  properties: { publicAccess: 'None' }
}]

output id string = sa.id
output name string = sa.name
