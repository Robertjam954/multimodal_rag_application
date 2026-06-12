param name string
param location string
param tags object = {}
param databaseName string = 'kg'
param graphName string = 'graph'

resource acct 'Microsoft.DocumentDB/databaseAccounts@2024-08-15' = {
  name: name
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    capabilities: [{ name: 'EnableGremlin' }]
    locations: [{ locationName: location, failoverPriority: 0, isZoneRedundant: false }]
    consistencyPolicy: { defaultConsistencyLevel: 'Session' }
  }
}

resource db 'Microsoft.DocumentDB/databaseAccounts/gremlinDatabases@2024-08-15' = {
  parent: acct
  name: databaseName
  properties: { resource: { id: databaseName } }
}

resource graph 'Microsoft.DocumentDB/databaseAccounts/gremlinDatabases/graphs@2024-08-15' = {
  parent: db
  name: graphName
  properties: {
    resource: {
      id: graphName
      partitionKey: { paths: ['/partitionKey'], kind: 'Hash' }
    }
    options: { throughput: 400 }
  }
}

output name string = acct.name
output endpoint string = acct.properties.documentEndpoint
