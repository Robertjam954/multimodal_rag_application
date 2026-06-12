param name string
param location string
param tags object = {}

resource vis 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'ComputerVision'
  sku: { name: 'S1' }
  properties: { customSubDomainName: name, publicNetworkAccess: 'Enabled' }
}

output id string = vis.id
output name string = vis.name
output endpoint string = vis.properties.endpoint
