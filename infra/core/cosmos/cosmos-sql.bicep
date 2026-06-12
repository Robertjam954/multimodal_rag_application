param name string
param location string
param tags object = {}
param databaseName string = 'chat'
param containerName string = 'history'

resource acct 'Microsoft.DocumentDB/databaseAccounts@2024-08-15' = {
  name: name
  location: location
  tags: tags
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [{ locationName: location, failoverPriority: 0, isZoneRedundant: false }]
    consistencyPolicy: { defaultConsistencyLevel: 'Session' }
  }
}

resource db 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-08-15' = {
  parent: acct
  name: databaseName
  properties: { resource: { id: databaseName } }
}

resource container 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-08-15' = {
  parent: db
  name: containerName
  properties: {
    resource: {
      id: containerName
      partitionKey: { paths: ['/oid'], kind: 'Hash' }
    }
  }
}

output endpoint string = acct.properties.documentEndpoint
output name string = acct.name
