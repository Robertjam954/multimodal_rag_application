param name string
param location string
param tags object = {}
param workspaceResourceId string

resource appi 'Microsoft.Insights/components@2020-02-02' = {
  name: name
  location: location
  tags: tags
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: workspaceResourceId
  }
}

output id string = appi.id
output name string = appi.name
output connectionString string = appi.properties.ConnectionString
