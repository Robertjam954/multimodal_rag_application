<!-- source: https://learn.microsoft.com/en-us/cli/azure/functionapp?view=azure-cli-latest -->

# az functionapp

Table of contents
Exit editor mode
Note
Access to this page requires authorization. You can try
signing in
or
changing directories
.
Access to this page requires authorization. You can try
changing directories
.
az functionapp
Note
This command group has commands that are defined in both Azure CLI and at least one extension. Install each extension to benefit from its extended capabilities.
Learn more
about extensions.
Manage function apps. To install the Azure Functions Core tools see
https://github.com/Azure/azure-functions-core-tools
.
Commands
Name
Description
Type
Status
az functionapp app
Commands to manage Azure Functions app.
Extension
Preview
az functionapp app up
Deploy to Azure Functions via GitHub actions.
Extension
Preview
az functionapp config
Configure a function app.
Core and Extension
GA
az functionapp config access-restriction
Methods that show, set, add, and remove access restrictions on a functionapp.
Core
GA
az functionapp config access-restriction add
Adds an Access Restriction to the function app.
Core
GA
az functionapp config access-restriction remove
Removes an Access Restriction from the functionapp.
Core
GA
az functionapp config access-restriction set
Sets if SCM site is using the same restrictions as the main site.
Core
GA
az functionapp config access-restriction show
Show Access Restriction settings for functionapp.
Core
GA
az functionapp config appsettings
Configure function app settings.
Core
GA
az functionapp config appsettings delete
Delete a function app's settings.
Core
GA
az functionapp config appsettings list
Show settings for a function app.
Core
GA
az functionapp config appsettings set
Update a function app's settings.
Core
GA
az functionapp config container
Manage an existing function app's container settings.
Core and Extension
GA
az functionapp config container delete
Delete an existing function app's container settings.
Core
GA
az functionapp config container set
Set an existing function app's container settings.
Core
GA
az functionapp config container set (appservice-kube extension)
Set an existing function app's container settings.
Extension
GA
az functionapp config container show
Get details of a function app's container settings.
Core
GA
az functionapp config hostname
Configure hostnames for a function app.
Core
GA
az functionapp config hostname add
Bind a hostname to a function app.
Core
GA
az functionapp config hostname delete
Unbind a hostname from a function app.
Core
GA
az functionapp config hostname get-external-ip
Get the external-facing IP address for a function app.
Core
GA
az functionapp config hostname list
List all hostname bindings for a function app.
Core
GA
az functionapp config set
Set an existing function app's configuration.
Core
GA
az functionapp config show
Get the details of an existing function app's configuration.
Core
GA
az functionapp config ssl
Configure SSL certificates.
Core
GA
az functionapp config ssl bind
Bind an SSL certificate to a function app.
Core
GA
az functionapp config ssl create
Create a Managed Certificate for a hostname in a function app.
Core
Preview
az functionapp config ssl delete
Delete an SSL certificate from a function app.
Core
GA
az functionapp config ssl import
Import an SSL certificate to a function app from Key Vault.
Core
GA
az functionapp config ssl list
List SSL certificates for a function app.
Core
GA
az functionapp config ssl show
Show the details of an SSL certificate for a function app.
Core
GA
az functionapp config ssl unbind
Unbind an SSL certificate from a function app.
Core
GA
az functionapp config ssl upload
Upload an SSL certificate to a function app.
Core
GA
az functionapp connection
Commands to manage functionapp connections.
Core and Extension
GA
az functionapp connection create
Create a connection between a functionapp and a target resource.
Core and Extension
GA
az functionapp connection create app-insights
Create a functionapp connection to app-insights.
Core
GA
az functionapp connection create appconfig
Create a functionapp connection to appconfig.
Core
GA
az functionapp connection create cognitiveservices
Create a functionapp connection to cognitiveservices.
Core
GA
az functionapp connection create confluent-cloud
Create a functionapp connection to confluent-cloud.
Core
GA
az functionapp connection create cosmos-cassandra
Create a functionapp connection to cosmos-cassandra.
Core
GA
az functionapp connection create cosmos-gremlin
Create a functionapp connection to cosmos-gremlin.
Core
GA
az functionapp connection create cosmos-mongo
Create a functionapp connection to cosmos-mongo.
Core
GA
az functionapp connection create cosmos-sql
Create a functionapp connection to cosmos-sql.
Core
GA
az functionapp connection create cosmos-table
Create a functionapp connection to cosmos-table.
Core
GA
az functionapp connection create eventhub
Create a functionapp connection to eventhub.
Core
GA
az functionapp connection create fabric-sql
Create a functionapp connection to fabric-sql.
Core
GA
az functionapp connection create fabric-sql (serviceconnector-passwordless extension)
Create a functionapp connection to fabric-sql.
Extension
GA
az functionapp connection create keyvault
Create a functionapp connection to keyvault.
Core
GA
az functionapp connection create mongodb-atlas
Create a functionapp connection to mongodb-atlas.
Core
GA
az functionapp connection create mysql
Create a functionapp connection to mysql.
Core
Deprecated
az functionapp connection create mysql-flexible
Create a functionapp connection to mysql-flexible.
Core
GA
az functionapp connection create mysql-flexible (serviceconnector-passwordless extension)
Create a functionapp connection to mysql-flexible.
Extension
GA
az functionapp connection create neon-postgres
Create a functionapp connection to neon-postgres.
Core
GA
az functionapp connection create postgres
Create a functionapp connection to postgres.
Core
Deprecated
az functionapp connection create postgres-flexible
Create a functionapp connection to postgres-flexible.
Core
GA
az functionapp connection create postgres-flexible (serviceconnector-passwordless extension)
Create a functionapp connection to postgres-flexible.
Extension
GA
az functionapp connection create redis
Create a functionapp connection to redis.
Core
GA
az functionapp connection create redis-enterprise
Create a functionapp connection to redis-enterprise.
Core
GA
az functionapp connection create servicebus
Create a functionapp connection to servicebus.
Core
GA
az functionapp connection create signalr
Create a functionapp connection to signalr.
Core
GA
az functionapp connection create sql
Create a functionapp connection to sql.
Core
GA
az functionapp connection create sql (serviceconnector-passwordless extension)
Create a functionapp connection to sql.
Extension
GA
az functionapp connection create storage-blob
Create a functionapp connection to storage-blob.
Core
GA
az functionapp connection create storage-file
Create a functionapp connection to storage-file.
Core
GA
az functionapp connection create storage-queue
Create a functionapp connection to storage-queue.
Core
GA
az functionapp connection create storage-table
Create a functionapp connection to storage-table.
Core
GA
az functionapp connection create webpubsub
Create a functionapp connection to webpubsub.
Core
GA
az functionapp connection delete
Delete a functionapp connection.
Core
GA
az functionapp connection list
List connections of a functionapp.
Core
GA
az functionapp connection list-configuration
List source configurations of a functionapp connection.
Core
GA
az functionapp connection list-support-types
List client types and auth types supported by functionapp connections.
Core
GA
az functionapp connection show
Get the details of a functionapp connection.
Core
GA
az functionapp connection update
Update a functionapp connection.
Core
GA
az functionapp connection update app-insights
Update a functionapp to app-insights connection.
Core
GA
az functionapp connection update appconfig
Update a functionapp to appconfig connection.
Core
GA
az functionapp connection update cognitiveservices
Update a functionapp to cognitiveservices connection.
Core
GA
az functionapp connection update confluent-cloud
Update a functionapp to confluent-cloud connection.
Core
GA
az functionapp connection update cosmos-cassandra
Update a functionapp to cosmos-cassandra connection.
Core
GA
az functionapp connection update cosmos-gremlin
Update a functionapp to cosmos-gremlin connection.
Core
GA
az functionapp connection update cosmos-mongo
Update a functionapp to cosmos-mongo connection.
Core
GA
az functionapp connection update cosmos-sql
Update a functionapp to cosmos-sql connection.
Core
GA
az functionapp connection update cosmos-table
Update a functionapp to cosmos-table connection.
Core
GA
az functionapp connection update eventhub
Update a functionapp to eventhub connection.
Core
GA
az functionapp connection update fabric-sql
Update a functionapp to fabric-sql connection.
Core
GA
az functionapp connection update keyvault
Update a functionapp to keyvault connection.
Core
GA
az functionapp connection update mongodb-atlas
Update a functionapp to mongodb-atlas connection.
Core
GA
az functionapp connection update mysql
Update a functionapp to mysql connection.
Core
Deprecated
az functionapp connection update mysql-flexible
Update a functionapp to mysql-flexible connection.
Core
GA
az functionapp connection update neon-postgres
Update a functionapp to neon-postgres connection.
Core
GA
az functionapp connection update postgres
Update a functionapp to postgres connection.
Core
Deprecated
az functionapp connection update postgres-flexible
Update a functionapp to postgres-flexible connection.
Core
GA
az functionapp connection update redis
Update a functionapp to redis connection.
Core
GA
az functionapp connection update redis-enterprise
Update a functionapp to redis-enterprise connection.
Core
GA
az functionapp connection update servicebus
Update a functionapp to servicebus connection.
Core
GA
az functionapp connection update signalr
Update a functionapp to signalr connection.
Core
GA
az functionapp connection update sql
Update a functionapp to sql connection.
Core
GA
az functionapp connection update storage-blob
Update a functionapp to storage-blob connection.
Core
GA
az functionapp connection update storage-file
Update a functionapp to storage-file connection.
Core
GA
az functionapp connection update storage-queue
Update a functionapp to storage-queue connection.
Core
GA
az functionapp connection update storage-table
Update a functionapp to storage-table connection.
Core
GA
az functionapp connection update webpubsub
Update a functionapp to webpubsub connection.
Core
GA
az functionapp connection validate
Validate a functionapp connection.
Core
GA
az functionapp connection wait
Place the CLI in a waiting state until a condition of the connection is met.
Core
GA
az functionapp cors
Manage Cross-Origin Resource Sharing (CORS).
Core
GA
az functionapp cors add
Add allowed origins.
Core
GA
az functionapp cors credentials
Enable or disable access-control-allow-credentials.
Core
GA
az functionapp cors remove
Remove allowed origins.
Core
GA
az functionapp cors show
Show allowed origins.
Core
GA
az functionapp create
Create a function app.
Core
GA
az functionapp create (appservice-kube extension)
Create a function app.
Extension
GA
az functionapp delete
Delete a function app.
Core
GA
az functionapp deploy
Deploys a provided artifact to Azure functionapp.
Core
Preview
az functionapp deployment
Manage function app deployments.
Core and Extension
GA
az functionapp deployment config
Manage a function app's deployment configuration.
Core
GA
az functionapp deployment config set
Update an existing function app's deployment configuration.
Core
GA
az functionapp deployment config show
Get the details of a function app's deployment configuration.
Core
GA
az functionapp deployment container
Manage container-based continuous deployment.
Core
GA
az functionapp deployment container config
Configure continuous deployment via containers.
Core
GA
az functionapp deployment container show-cd-url
Get the URL which can be used to configure webhooks for continuous deployment.
Core
GA
az functionapp deployment github-actions
Configure GitHub Actions for a functionapp.
Core
GA
az functionapp deployment github-actions add
Add a GitHub Actions workflow file to the specified repository. The workflow will build and deploy your app to the specified functionapp.
Core
GA
az functionapp deployment github-actions remove
Remove and disconnect the GitHub Actions workflow file from the specified repository.
Core
GA
az functionapp deployment list-publishing-credentials
Get the details for available function app publishing credentials.
Core
GA
az functionapp deployment list-publishing-profiles
Get the details for available function app deployment profiles.
Core
GA
az functionapp deployment slot
Manage function app deployment slots.
Core
GA
az functionapp deployment slot auto-swap
Configure deployment slot auto swap.
Core
GA
az functionapp deployment slot create
Create a deployment slot.
Core
GA
az functionapp deployment slot delete
Delete a deployment slot.
Core
GA
az functionapp deployment slot list
List all deployment slots.
Core
GA
az functionapp deployment slot swap
Swap deployment slots for a function app.
Core
GA
az functionapp deployment source
Manage function app deployment via source control.
Core and Extension
GA
az functionapp deployment source config
Manage deployment from git or Mercurial repositories.
Core
GA
az functionapp deployment source config-local-git
Get a URL for a git repository endpoint to clone and push to for function app deployment.
Core
GA
az functionapp deployment source config-zip
Perform deployment using the kudu zip push deployment for a function app.
Core
GA
az functionapp deployment source config-zip (appservice-kube extension)
Perform deployment using the kudu zip push deployment for a function app.
Extension
GA
az functionapp deployment source delete
Delete a source control deployment configuration.
Core
GA
az functionapp deployment source show
Get the details of a source control deployment configuration.
Core
GA
az functionapp deployment source sync
Synchronize from the repository. Only needed under manual integration mode.
Core
GA
az functionapp deployment source update-token
Update source control token cached in Azure app service.
Core
GA
az functionapp deployment user
Manage user credentials for deployment.
Core
GA
az functionapp deployment user set
Update deployment credentials.
Core
GA
az functionapp deployment user show
Gets publishing user.
Core
GA
az functionapp devops-pipeline
Azure Function specific integration with Azure DevOps. Please visit
https://aka.ms/functions-azure-devops
for more information.
Extension
GA
az functionapp devops-pipeline create
Create an Azure DevOps pipeline for a function app.
Extension
GA
az functionapp flex-migration
Manage migration of Linux Consumption function apps to the Flex Consumption plan.
Core
GA
az functionapp flex-migration list
List all Linux Consumption function apps that are eligible for migration to the Flex Consumption plan.
Core
GA
az functionapp flex-migration start
Create a Flex Consumption app with the same settings as the provided Linux Consumption function app.
Core
GA
az functionapp function
Manage function app functions.
Core
GA
az functionapp function delete
Delete a function.
Core
GA
az functionapp function keys
Manage function keys.
Core
GA
az functionapp function keys delete
Delete a function key.
Core
GA
az functionapp function keys list
List all function keys.
Core
GA
az functionapp function keys set
Create or update a function key.
Core
GA
az functionapp function list
List functions in a function app.
Core
GA
az functionapp function show
Get the details of a function.
Core
GA
az functionapp hybrid-connection
Methods that list, add and remove hybrid-connections from functionapp.
Core
GA
az functionapp hybrid-connection add
Add an existing hybrid-connection to a functionapp.
Core
GA
az functionapp hybrid-connection list
List the hybrid-connections on a functionapp.
Core
GA
az functionapp hybrid-connection remove
Remove a hybrid-connection from a functionapp.
Core
GA
az functionapp identity
Manage web app's managed identity.
Core
GA
az functionapp identity assign
Assign managed identity to the web app.
Core
GA
az functionapp identity remove
Disable web app's managed identity.
Core
GA
az functionapp identity show
Display web app's managed identity.
Core
GA
az functionapp keys
Manage function app keys.
Core
GA
az functionapp keys delete
Delete a function app key.
Core
GA
az functionapp keys list
List all function app keys.
Core
GA
az functionapp keys set
Create or update a function app key.
Core
GA
az functionapp list
List function apps.
Core
GA
az functionapp list-consumption-locations
List available locations for running function apps.
Core
GA
az functionapp list-flexconsumption-locations
List available locations for running function apps on the Flex Consumption plan.
Core
GA
az functionapp list-flexconsumption-runtimes
List available built-in stacks which can be used for function apps on the Flex Consumption plan.
Core
GA
az functionapp list-runtimes
List available built-in stacks which can be used for function apps.
Core
GA
az functionapp log
Manage function app logs.
Core
GA
az functionapp log deployment
Manage function app deployment logs.
Core
GA
az functionapp log deployment list
List deployment logs of the deployments associated with function app.
Core
GA
az functionapp log deployment show
Show deployment logs of the latest deployment, or a specific deployment if deployment-id is specified.
Core
GA
az functionapp plan
Manage App Service Plans for an Azure Function.
Core
GA
az functionapp plan create
Create an App Service Plan for an Azure Function.
Core
GA
az functionapp plan delete
Delete an App Service Plan.
Core
GA
az functionapp plan list
List App Service Plans.
Core
GA
az functionapp plan show
Get the App Service Plans for a resource group or a set of resource groups.
Core
GA
az functionapp plan update
Update an App Service plan for an Azure Function.
Core
GA
az functionapp restart
Restart a function app.
Core
GA
az functionapp restart (appservice-kube extension)
Restart a function app.
Extension
GA
az functionapp runtime
Manage a function app's runtime.
Core
GA
az functionapp runtime config
Manage a function app's runtime configuration.
Core
GA
az functionapp runtime config set
Update an existing function app's runtime configuration.
Core
GA
az functionapp runtime config show
Get the details of a function app's runtime configuration.
Core
GA
az functionapp scale
Manage a function app's scale.
Core
GA
az functionapp scale config
Manage a function app's scale configuration.
Core
GA
az functionapp scale config always-ready
Manage the always-ready settings in the scale configuration.
Core
GA
az functionapp scale config always-ready delete
Delete always-ready settings in the scale configuration.
Core
GA
az functionapp scale config always-ready set
Add or update existing always-ready settings in the scale configuration.
Core
GA
az functionapp scale config set
Update an existing function app's scale configuration.
Core
GA
az functionapp scale config show
Get the details of a function app's scale configuration.
Core
GA
az functionapp show
Get the details of a function app.
Core
GA
az functionapp show (appservice-kube extension)
Get the details of a function app.
Extension
GA
az functionapp start
Start a function app.
Core
GA
az functionapp stop
Stop a function app.
Core
GA
az functionapp update
Update a function app.
Core
GA
az functionapp update-strategy
Manage a function app's update strategy.
Core
GA
az functionapp update-strategy config
Manage a function app's update strategy configuration.
Core
GA
az functionapp update-strategy config set
Set or update a function app's update strategy configuration.
Core
GA
az functionapp update-strategy config show
Get the details of a function app's update strategy configuration.
Core
GA
az functionapp vnet-integration
Methods that list, add, and remove virtual networks integrations from a functionapp.
Core
GA
az functionapp vnet-integration add
Add a regional virtual network integration to a functionapp.
Core
GA
az functionapp vnet-integration list
List the virtual network integrations on a functionapp.
Core
GA
az functionapp vnet-integration remove
Remove a regional virtual network integration from functionapp.
Core
GA
az functionapp create
Edit
Create a function app.
The function app's name must be able to produce a unique FQDN as AppName.azurewebsites.net.
```
az functionapp create --name
                      --resource-group
                      --storage-account
                      [--acquire-policy-token]
                      [--always-ready-instances]
                      [--app-insights]
                      [--app-insights-key]
                      [--assign-identity]
                      [--change-reference]
                      [--cnl --configure-networking-later {false, true}]
                      [--consumption-plan-location]
                      [--cpu]
                      [--dal --dapr-enable-api-logging {false, true}]
                      [--dapr-app-id]
                      [--dapr-app-port]
                      [--dapr-http-max-request-size --dhmrs]
                      [--dapr-http-read-buffer-size --dhrbs]
                      [--dapr-log-level {debug, error, info, warn}]
                      [--deployment-container-image-name]
                      [--deployment-local-git]
                      [--deployment-source-branch]
                      [--deployment-source-url]
                      [--deployment-storage-auth-type --dsat {StorageAccountConnectionString, SystemAssignedIdentity, UserAssignedIdentity}]
                      [--deployment-storage-auth-value --dsav]
                      [--deployment-storage-container-name --dscn]
                      [--deployment-storage-name --dsn]
                      [--disable-app-insights {false, true}]
                      [--docker-registry-server-password]
                      [--docker-registry-server-user]
                      [--domain-name-scope {NoReuse, ResourceGroupReuse, SubscriptionReuse, TenantReuse}]
                      [--enable-dapr {false, true}]
                      [--environment]
                      [--flexconsumption-location]
                      [--functions-version {4}]
                      [--https-only {false, true}]
                      [--image]
                      [--instance-memory]
                      [--max-replicas]
                      [--maximum-instance-count]
                      [--memory]
                      [--min-replicas]
                      [--os-type {Linux, Windows}]
                      [--plan]
                      [--registry-password]
                      [--registry-server]
                      [--registry-username]
                      [--role]
                      [--runtime]
                      [--runtime-version]
                      [--scope]
                      [--subnet]
                      [--tags]
                      [--vnet]
                      [--workload-profile-name]
                      [--workspace]
                      [--zone-redundant {false, true}]
```
Examples
Create a basic function app.
```
az functionapp create -g MyResourceGroup  -p MyPlan -n MyUniqueAppName -s MyStorageAccount
```
Create a function app. (autogenerated)
```
az functionapp create --consumption-plan-location westus --name MyUniqueAppName --os-type Windows --resource-group MyResourceGroup --runtime dotnet-isolated --storage-account MyStorageAccount
```
Create a function app using a private ACR image.
```
az functionapp create -g MyResourceGroup -p MyPlan -n MyUniqueAppName --runtime node --storage-account MyStorageAccount --deployment-container-image-name myacr.azurecr.io/myimage:tag --docker-registry-server-password passw0rd --docker-registry-server-user MyUser
```
Create a flex consumption function app. See https://aka.ms/flex-http-concurrency for more information on default http concurrency values.
```
az functionapp create -g MyResourceGroup --name MyUniqueAppName -s MyStorageAccount --flexconsumption-location northeurope --runtime java --instance-memory 2048
```
Required Parameters
--name -n
Name of the new function app.
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
--storage-account -s
Provide a string value of a Storage Account in the provided Resource Group. Or Resource ID of a Storage Account in a different Resource Group.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--always-ready-instances
Space-separated configuration for the number of pre-allocated instances in the format
<name>=<value>
.
--app-insights
Name of the existing App Insights project to be added to the function app. Must be in the same resource group.
--app-insights-key
Instrumentation key of App Insights to be added.
--assign-identity
Accept system or user assigned identities separated by spaces. Use '[system]' to refer system assigned identity, or a resource id to refer user assigned identity. Check out help for more examples.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--cnl --configure-networking-later
Use this option if you want to configure networking later for an app using network-restricted storage.
Property
Value
Accepted values:
false, true
--consumption-plan-location -c
Geographic location where function app will be hosted. Use
az functionapp list-consumption-locations
to view available locations.
--cpu
Preview
The CPU in cores of the container app. e.g 0.75.
--dal --dapr-enable-api-logging
Enable/Disable API logging for the Dapr sidecar.
Property
Value
Default value:
False
Accepted values:
false, true
--dapr-app-id
The Dapr application identifier.
--dapr-app-port
The port Dapr uses to communicate to the application.
--dapr-http-max-request-size --dhmrs
Max size of request body http and grpc servers in MB to handle uploading of large files.
--dapr-http-read-buffer-size --dhrbs
Max size of http header read buffer in KB to handle when sending multi-KB headers.
--dapr-log-level
The log level for the Dapr sidecar.
Property
Value
Accepted values:
debug, error, info, warn
--deployment-container-image-name
Deprecated
Container image, e.g. publisher/image-name:tag.
--deployment-local-git -l
Enable local git.
--deployment-source-branch -b
The branch to deploy.
--deployment-source-url -u
Git repository URL to link with manual integration.
--deployment-storage-auth-type --dsat
The deployment storage account authentication type.
Property
Value
Accepted values:
StorageAccountConnectionString, SystemAssignedIdentity, UserAssignedIdentity
--deployment-storage-auth-value --dsav
The deployment storage account authentication value. For the user-assigned managed identity authentication type, this should be the user assigned identity resource id. For the storage account connection string authentication type, this should be the name of the app setting that will contain the storage account connection string. For the system assigned managed-identity authentication type, this parameter is not applicable and should be left empty.
--deployment-storage-container-name --dscn
The deployment storage account container name.
--deployment-storage-name --dsn
The deployment storage account name.
--disable-app-insights
Disable creating application insights resource during functionapp create. No logs will be available.
Property
Value
Accepted values:
false, true
--docker-registry-server-password
Deprecated
The container registry server password. Required for private registries.
--docker-registry-server-user
Deprecated
The container registry server username.
--domain-name-scope
Specify the scope of uniqueness for the default hostname during resource creation.
Property
Value
Accepted values:
NoReuse, ResourceGroupReuse, SubscriptionReuse, TenantReuse
--enable-dapr
Enable/Disable Dapr for a function app on an Azure Container App environment.
Property
Value
Default value:
False
Accepted values:
false, true
--environment
Preview
Name of the container app environment.
--flexconsumption-location -f
Geographic location where function app will be hosted. Use
az functionapp list-flexconsumption-locations
to view available locations.
--functions-version
The functions app version. NOTE: This will be required starting the next release cycle.
Property
Value
Accepted values:
4
--https-only
Redirect all traffic made to an app using HTTP to HTTPS.
Property
Value
Default value:
False
Accepted values:
false, true
--image -i
Container image, e.g. publisher/image-name:tag.
--instance-memory
The instance memory size in MB. See
https://aka.ms/flex-instance-sizes
for more information on the supported values.
--max-replicas
Preview
The maximum number of replicas when create function app on container app.
--maximum-instance-count
The maximum number of instances.
--memory
Preview
The memory size of the container app. e.g. 1.0Gi,.
--min-replicas
Preview
The minimum number of replicas when create function app on container app.
--os-type
Set the OS type for the app to be created.
Property
Value
Accepted values:
Linux, Windows
--plan -p
Name or resource id of the functionapp app service plan. Use 'appservice plan create' to get one. If using an App Service plan from a different resource group, the full resource id must be used and not the plan name.
--registry-password -w
The container registry server password. Required for private registries.
--registry-server
Preview
The container registry server hostname, e.g. myregistry.azurecr.io.
--registry-username -d
The container registry server username.
--role
Role name or id the system assigned identity will have.
Property
Value
Default value:
Contributor
--runtime
The functions runtime stack. Use "az functionapp list-runtimes" to check supported runtimes and versions.
--runtime-version
The version of the functions runtime stack. The functions runtime stack. Use "az functionapp list-runtimes" to check supported runtimes and versions.
--scope
Scope that the system assigned identity can access.
--subnet
Name or resource ID of the pre-existing subnet to have the webapp join. The --vnet is argument also needed if specifying subnet by name.
--tags
Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags.
--vnet
Name or resource ID of the regional virtual network. If there are multiple vnets of the same name across different resource groups, use vnet resource id to specify which vnet to use. If vnet name is used, by default, the vnet in the same resource group as the webapp will be used. Must be used with --subnet argument.
--workload-profile-name
Preview
The workload profile name to run the container app on.
--workspace
Name of an existing log analytics workspace to be used for the application insights component.
--zone-redundant
Enable zone redundancy for high availability. Applies to Flex Consumption SKU only.
Property
Value
Default value:
False
Accepted values:
false, true
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp create (appservice-kube extension)
Create a function app.
The function app's name must be able to produce a unique FQDN as AppName.azurewebsites.net.
```
az functionapp create --name
                      --resource-group
                      [--acquire-policy-token]
                      [--app-insights]
                      [--app-insights-key]
                      [--assign-identity]
                      [--change-reference]
                      [--consumption-plan-location]
                      [--custom-location]
                      [--deployment-container-image-name]
                      [--deployment-local-git]
                      [--deployment-source-branch]
                      [--deployment-source-url]
                      [--disable-app-insights {false, true}]
                      [--docker-registry-server-password]
                      [--docker-registry-server-user]
                      [--functions-version {4}]
                      [--max-worker-count]
                      [--min-worker-count]
                      [--os-type {Linux, Windows}]
                      [--plan]
                      [--role]
                      [--runtime]
                      [--runtime-version]
                      [--scope]
                      [--storage-account]
                      [--tags]
```
Examples
Create a basic function app.
```
az functionapp create -g MyResourceGroup  -p MyPlan -n MyUniqueAppName -s MyStorageAccount
```
Create a function app. (autogenerated)
```
az functionapp create --consumption-plan-location westus --name MyUniqueAppName --os-type Windows --resource-group MyResourceGroup --runtime dotnet --storage-account MyStorageAccount
```
Create a function app using a private ACR image.
```
az functionapp create -g MyResourceGroup -p MyPlan -n MyUniqueAppName --runtime node --storage-account MyStorageAccount --deployment-container-image-name myacr.azurecr.io/myimage:tag --docker-registry-server-password passw0rd --docker-registry-server-user MyUser
```
Create a function app in an app service kubernetes environment
```
az functionapp create -g MyResourceGroup  -p MyPlan -n MyUniqueAppName -s MyStorageAccount --custom-location /subscriptions/sub_id/resourcegroups/group_name/providers/microsoft.extendedlocation/customlocations/custom_location_name
```
Create a function app in an app service kubernetes environment and in the same resource group as the custom location
```
az functionapp create -g MyResourceGroup  -p MyPlan -n MyUniqueAppName -s MyStorageAccount --custom-location custom_location_name
```
Required Parameters
--name -n
Name of the function app.
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--app-insights
Name of the existing App Insights project to be added to the Function app. Must be in the same resource group.
--app-insights-key
Instrumentation key of App Insights to be added.
--assign-identity
Accept system or user assigned identities separated by spaces. Use '[system]' to refer system assigned identity, or a resource id to refer user assigned identity. Check out help for more examples.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--consumption-plan-location -c
Geographic location where Function App will be hosted. Use
az functionapp list-consumption-locations
to view available locations.
--custom-location
Name or ID of the custom location. Use an ID for a custom location in a different resource group from the app.
--deployment-container-image-name -i
Linux only. Container image name from Docker Hub, e.g. publisher/image-name:tag.
--deployment-local-git -l
Enable local git.
--deployment-source-branch -b
The branch to deploy.
Property
Value
Default value:
master
--deployment-source-url -u
Git repository URL to link with manual integration.
--disable-app-insights
Disable creating application insights resource during functionapp create. No logs will be available.
Property
Value
Accepted values:
false, true
--docker-registry-server-password
The container registry server password. Required for private registries.
--docker-registry-server-user
The container registry server username.
--functions-version
The functions app version.  Use "az functionapp list-runtimes" to check compatibility with runtimes and runtime versions.
Property
Value
Accepted values:
4
--max-worker-count
Preview
Maximum number of workers to be allocated.
--min-worker-count
Preview
Minimum number of workers to be allocated.
--os-type
Set the OS type for the app to be created.
Property
Value
Accepted values:
Linux, Windows
--plan -p
Name or resource id of the function app service plan. Use 'appservice plan create' to get one.
--role
Role name or id the system assigned identity will have.
Property
Value
Default value:
Contributor
--runtime
The functions runtime stack. Use "az functionapp list-runtimes" to check supported runtimes and versions.
--runtime-version
The version of the functions runtime stack. Use "az functionapp list-runtimes" to check supported runtimes and versions.
--scope
Scope that the system assigned identity can access.
--storage-account -s
Provide a string value of a Storage Account in the provided Resource Group. Or Resource ID of a Storage Account in a different Resource Group. Required for non-kubernetes function apps.
--tags
Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags.
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp delete
Edit
Delete a function app.
```
az functionapp delete [--acquire-policy-token]
                      [--change-reference]
                      [--ids]
                      [--keep-empty-plan]
                      [--name]
                      [--resource-group]
                      [--slot]
                      [--subscription]
```
Examples
Delete a function app. (autogenerated)
```
az functionapp delete --name MyFunctionApp --resource-group MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--keep-empty-plan
Keep empty app service plan.
--name -n
The name of the functionapp.
Property
Value
Parameter group:
Resource Id Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--slot -s
The name of the slot. Default to the productions slot if not specified.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp deploy
Edit
Preview
Deploys a provided artifact to Azure functionapp.
```
az functionapp deploy [--acquire-policy-token]
                      [--async {false, true}]
                      [--change-reference]
                      [--clean {false, true}]
                      [--ids]
                      [--ignore-stack {false, true}]
                      [--name]
                      [--resource-group]
                      [--restart {false, true}]
                      [--slot]
                      [--src-path]
                      [--src-url]
                      [--subscription]
                      [--target-path]
                      [--timeout]
                      [--type {ear, jar, lib, startup, static, war, zip}]
```
Examples
Deploy a war file asynchronously.
```
az functionapp deploy --resource-group ResourceGroup --name AppName --src-path SourcePath --type war --async true
```
Deploy a static text file to wwwroot/staticfiles/test.txt
```
az functionapp deploy --resource-group ResourceGroup --name AppName --src-path SourcePath --type static --target-path staticfiles/test.txt
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--async
Asynchronous deployment.
Property
Value
Accepted values:
false, true
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--clean
If true, cleans the target directory prior to deploying the file(s). Default value is determined based on artifact type.
Property
Value
Accepted values:
false, true
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--ignore-stack
If true, any stack-specific defaults are ignored.
Property
Value
Accepted values:
false, true
--name -n
Name of the function app to deploy to.
Property
Value
Parameter group:
Resource Id Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--restart
If true, the web app will be restarted following the deployment, default value is true. Set this to false if you are deploying multiple artifacts and do not want to restart the site on the earlier deployments.
Property
Value
Accepted values:
false, true
--slot -s
The name of the slot. Default to the productions slot if not specified.
--src-path
Path of the artifact to be deployed. Ex: "myapp.zip" or "/myworkspace/apps/myapp.war".
--src-url
URL of the artifact. The webapp will pull the artifact from this URL. Ex: "http://mysite.com/files/myapp.war?key=123".
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
--target-path
Absolute path that the artifact should be deployed to. Defaults to "home/site/wwwroot/". Ex: "/home/site/deployments/tools/", "/home/site/scripts/startup-script.sh".
--timeout
Timeout for the deployment operation in milliseconds.
--type
Used to override the type of artifact being deployed.
Property
Value
Accepted values:
ear, jar, lib, startup, static, war, zip
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp list
Edit
List function apps.
```
az functionapp list [--resource-group]
```
Examples
List all function apps in MyResourceGroup.
```
az functionapp list --resource-group MyResourceGroup
```
List default host name and state for all function apps.
```
az functionapp list --query "[].{hostName: defaultHostName, state: state}"
```
List all running function apps.
```
az functionapp list --query "[?state=='Running']"
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp list-consumption-locations
Edit
List available locations for running function apps.
```
az functionapp list-consumption-locations [--acquire-policy-token]
                                          [--change-reference]
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp list-flexconsumption-locations
Edit
List available locations for running function apps on the Flex Consumption plan.
```
az functionapp list-flexconsumption-locations [--acquire-policy-token]
                                              [--change-reference]
                                              [--runtime]
                                              [--show-details {false, true}]
                                              [--zone-redundant {false, true}]
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--runtime
Limit the output to just the specified runtime.
--show-details
Include the runtime details of the regions.
Property
Value
Default value:
False
Accepted values:
false, true
--zone-redundant
Filter the list to return only locations which support zone redundancy.
Property
Value
Default value:
False
Accepted values:
false, true
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp list-flexconsumption-runtimes
Edit
List available built-in stacks which can be used for function apps on the Flex Consumption plan.
```
az functionapp list-flexconsumption-runtimes --location
                                             --runtime
                                             [--acquire-policy-token]
                                             [--change-reference]
```
Required Parameters
--location -l
Limit the output to just the runtimes available in the specified location.
--runtime
Limit the output to just the specified runtime.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp list-runtimes
Edit
List available built-in stacks which can be used for function apps.
```
az functionapp list-runtimes [--acquire-policy-token]
                             [--change-reference]
                             [--os --os-type {linux, windows}]
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--os --os-type
Limit the output to just windows or linux runtimes.
Property
Value
Accepted values:
linux, windows
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp restart
Edit
Restart a function app.
```
az functionapp restart [--acquire-policy-token]
                       [--change-reference]
                       [--ids]
                       [--name]
                       [--resource-group]
                       [--slot]
                       [--subscription]
```
Examples
Restart a function app. (autogenerated)
```
az functionapp restart --name MyFunctionApp --resource-group MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--name -n
Name of the function app.
Property
Value
Parameter group:
Resource Id Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--slot -s
The name of the slot. Default to the productions slot if not specified.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp restart (appservice-kube extension)
Restart a function app.
```
az functionapp restart [--acquire-policy-token]
                       [--change-reference]
                       [--ids]
                       [--name]
                       [--resource-group]
                       [--slot]
                       [--subscription]
```
Examples
Restart a function app. (autogenerated)
```
az functionapp restart --name MyFunctionApp --resource-group MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--name -n
Name of the function app.
Property
Value
Parameter group:
Resource Id Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--slot -s
The name of the slot. Default to the productions slot if not specified.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp show
Edit
Get the details of a function app.
```
az functionapp show [--ids]
                    [--name]
                    [--resource-group]
                    [--slot]
                    [--subscription]
```
Examples
Get the details of a function app. (autogenerated)
```
az functionapp show --name MyFunctionApp --resource-group MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--name -n
Name of the function app.
Property
Value
Parameter group:
Resource Id Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--slot -s
The name of the slot. Default to the productions slot if not specified.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp show (appservice-kube extension)
Get the details of a function app.
```
az functionapp show [--ids]
                    [--name]
                    [--resource-group]
                    [--slot]
                    [--subscription]
```
Examples
Get the details of a function app. (autogenerated)
```
az functionapp show --name MyFunctionApp --resource-group MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--name -n
Name of the function app.
Property
Value
Parameter group:
Resource Id Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--slot -s
The name of the slot. Default to the productions slot if not specified.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp start
Edit
Start a function app.
```
az functionapp start [--acquire-policy-token]
                     [--change-reference]
                     [--ids]
                     [--name]
                     [--resource-group]
                     [--slot]
                     [--subscription]
```
Examples
Start a function app. (autogenerated)
```
az functionapp start --name MyFunctionApp --resource-group MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--name -n
Name of the function app.
Property
Value
Parameter group:
Resource Id Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--slot -s
The name of the slot. Default to the productions slot if not specified.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp stop
Edit
Stop a function app.
```
az functionapp stop [--acquire-policy-token]
                    [--change-reference]
                    [--ids]
                    [--name]
                    [--resource-group]
                    [--slot]
                    [--subscription]
```
Examples
Stop a function app. (autogenerated)
```
az functionapp stop --name MyFunctionApp --resource-group MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--name -n
Name of the function app.
Property
Value
Parameter group:
Resource Id Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--slot -s
The name of the slot. Default to the productions slot if not specified.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az functionapp update
Edit
Update a function app.
```
az functionapp update [--acquire-policy-token]
                      [--add]
                      [--change-reference]
                      [--force]
                      [--force-string]
                      [--ids]
                      [--name]
                      [--plan]
                      [--remove]
                      [--resource-group]
                      [--set]
                      [--slot]
                      [--subscription]
```
Examples
Update a function app. (autogenerated)
```
az functionapp update --name MyFunctionApp --resource-group MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--add
Add an object to a list of objects by specifying a path and key value pairs.  Example:
--add property.listProperty <key=value, string or JSON string>
.
Property
Value
Parameter group:
Generic Update Arguments
Default value:
[]
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--force
Required if attempting to migrate functionapp from Premium to Consumption --plan.
Property
Value
Default value:
False
--force-string
When using 'set' or 'add', preserve string literals instead of attempting to convert to JSON.
Property
Value
Parameter group:
Generic Update Arguments
Default value:
False
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--name -n
Name of the function app.
Property
Value
Parameter group:
Resource Id Arguments
--plan
The name or resource id of the plan to update the functionapp with.
--remove
Remove a property or an element from a list.  Example:
--remove property.list <indexToRemove>
OR
--remove propertyToRemove
.
Property
Value
Parameter group:
Generic Update Arguments
Default value:
[]
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--set
Update an object by specifying a property path and value to set.  Example:
--set property1.property2=<value>
.
Property
Value
Parameter group:
Generic Update Arguments
Default value:
[]
--slot -s
The name of the slot. Default to the productions slot if not specified.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
Global Parameters
--debug
Increase logging verbosity to show all debug logs.
Property
Value
Default value:
False
--help -h
Show this help message and exit.
--only-show-errors
Only show errors, suppressing warnings.
Property
Value
Default value:
False
--output -o
Output format.
Property
Value
Default value:
json
Accepted values:
json, jsonc, none, table, tsv, yaml, yamlc
--query
JMESPath query string. See
http://jmespath.org/
for more information and examples.
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
Collaborate with us on GitHub
The source for this content can be found on GitHub, where you can also create and review issues and pull requests. For more information, see
our contributor guide
.
Azure CLI
Open a documentation issue
Provide product feedback
Feedback
Was this page helpful?
Yes
No
No
Need help with this topic?
Want to try using Ask Learn to clarify or guide you through this topic?
Ask Learn
Ask Learn
Suggest a fix?