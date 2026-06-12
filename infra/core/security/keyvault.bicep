param name string
param location string
param tags object = {}
param principalId string = ''

resource kv 'Microsoft.KeyVault/vaults@2024-04-01-preview' = {
  name: name
  location: location
  tags: tags
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    accessPolicies: []
    publicNetworkAccess: 'Enabled'
  }
}

output id string = kv.id
output name string = kv.name
output uri string = kv.properties.vaultUri
