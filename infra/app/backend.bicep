param name string
param location string
param tags object = {}
param containerAppsEnvironmentId string
param appInsightsConnectionString string
param env array = []
param imageName string = 'mcr.microsoft.com/k8se/quickstart:latest'

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: location
  tags: tags
  identity: { type: 'SystemAssigned' }
  properties: {
    managedEnvironmentId: containerAppsEnvironmentId
    configuration: {
      ingress: { external: true, targetPort: 50505, transport: 'http' }
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: imageName
          env: env
          resources: { cpu: json('1.0'), memory: '2Gi' }
        }
      ]
      scale: { minReplicas: 1, maxReplicas: 5 }
    }
  }
}

output uri string = 'https://${app.properties.configuration.ingress.fqdn}'
output name string = app.name
