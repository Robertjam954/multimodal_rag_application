param name string
param location string
param tags object = {}

resource cs 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'ContentSafety'
  sku: { name: 'S0' }
  properties: { customSubDomainName: name, publicNetworkAccess: 'Enabled' }
}

output id string = cs.id
output name string = cs.name
output endpoint string = cs.properties.endpoint
