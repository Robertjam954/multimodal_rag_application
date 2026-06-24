/*
  Flex Consumption Function App for the cloud ingestion skills
  (document_extractor, figure_processor, text_processor, audio_transcriber,
  graph_indexer). Code (zip) deploy via azd — no container image.

  These functions import the full backend RAG dependency stack, so Flex
  Consumption is used (large package + better cold-start behaviour than the
  legacy Consumption SKU). The function app gets a dedicated runtime/deployment
  storage account (Functions best practice — not the HNS-enabled app-data
  account) and a SystemAssigned identity that must be granted the same
  data-plane roles as the backend (see role assignments in main.bicep).
*/

param name string
param planName string
param storageAccountName string
param location string
param tags object = {}
param appInsightsConnectionString string
param runtimeVersion string = '3.11'
param instanceMemoryMB int = 2048
param maximumInstanceCount int = 40
@description('Service env vars (same service wiring the backend receives).')
param appSettings array = []

var deploymentContainerName = 'deployment'

resource stg 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: storageAccountName
  location: location
  tags: tags
  kind: 'StorageV2'
  sku: { name: 'Standard_LRS' }
  properties: {
    accessTier: 'Hot'
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' = {
  parent: stg
  name: 'default'
  properties: {}
}

resource deploymentContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2024-01-01' = {
  parent: blobService
  name: deploymentContainerName
  properties: { publicAccess: 'None' }
}

var storageConnectionString = 'DefaultEndpointsProtocol=https;AccountName=${stg.name};AccountKey=${stg.listKeys().keys[0].value};EndpointSuffix=${environment().suffixes.storage}'

resource plan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: location
  tags: tags
  kind: 'functionapp'
  sku: { tier: 'FlexConsumption', name: 'FC1' }
  properties: { reserved: true }
}

resource functionApp 'Microsoft.Web/sites@2023-12-01' = {
  name: name
  location: location
  tags: union(tags, { 'azd-service-name': 'functions' })
  kind: 'functionapp,linux'
  identity: { type: 'SystemAssigned' }
  properties: {
    serverFarmId: plan.id
    httpsOnly: true
    functionAppConfig: {
      deployment: {
        storage: {
          type: 'blobContainer'
          value: '${stg.properties.primaryEndpoints.blob}${deploymentContainerName}'
          authentication: {
            type: 'StorageAccountConnectionStringSecret'
            storageAccountConnectionStringName: 'DEPLOYMENT_STORAGE_CONNECTION_STRING'
          }
        }
      }
      runtime: {
        name: 'python'
        version: runtimeVersion
      }
      scaleAndConcurrency: {
        instanceMemoryMB: instanceMemoryMB
        maximumInstanceCount: maximumInstanceCount
      }
    }
    siteConfig: {
      appSettings: union(
        [
          { name: 'AzureWebJobsStorage', value: storageConnectionString }
          { name: 'DEPLOYMENT_STORAGE_CONNECTION_STRING', value: storageConnectionString }
          { name: 'APPLICATIONINSIGHTS_CONNECTION_STRING', value: appInsightsConnectionString }
        ],
        appSettings
      )
    }
  }

  dependsOn: [deploymentContainer]
}

output name string = functionApp.name
output uri string = 'https://${functionApp.properties.defaultHostName}'
output identityPrincipalId string = functionApp.identity.principalId
