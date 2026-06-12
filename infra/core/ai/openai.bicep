param name string
param location string
param tags object = {}
param chatDeployment object
param embedDeployment object

resource aoai 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  tags: tags
  kind: 'OpenAI'
  sku: { name: 'S0' }
  properties: {
    customSubDomainName: name
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
  }
}

resource chat 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: aoai
  name: chatDeployment.name
  sku: { name: 'GlobalStandard', capacity: chatDeployment.capacity }
  properties: { model: { format: 'OpenAI', name: chatDeployment.model, version: chatDeployment.version } }
}

resource embed 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: aoai
  name: embedDeployment.name
  sku: { name: 'Standard', capacity: embedDeployment.capacity }
  properties: { model: { format: 'OpenAI', name: embedDeployment.model, version: embedDeployment.version } }
  dependsOn: [ chat ]
}

output id string = aoai.id
output name string = aoai.name
output endpoint string = aoai.properties.endpoint
