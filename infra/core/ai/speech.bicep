param name string
param location string
param tags object = {}

resource sp 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'SpeechServices'
  sku: { name: 'S0' }
  properties: { customSubDomainName: name, publicNetworkAccess: 'Enabled' }
}

output id string = sp.id
output name string = sp.name
output endpoint string = sp.properties.endpoint
