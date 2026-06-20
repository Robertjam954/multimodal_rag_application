<!-- source: https://learn.microsoft.com/en-us/cli/azure/containerapp?view=azure-cli-latest -->

# az containerapp

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
az containerapp
Note
This command group has commands that are defined in both Azure CLI and at least one extension. Install each extension to benefit from its extended capabilities.
Learn more
about extensions.
Manage Azure Container Apps.
Commands
Name
Description
Type
Status
az containerapp add-on
Commands to manage add-ons available within the environment.
Extension
Preview
az containerapp add-on kafka
Commands to manage the kafka add-on for the Container Apps environment.
Extension
Preview
az containerapp add-on kafka create
Command to create the kafka add-on.
Extension
Preview
az containerapp add-on kafka delete
Command to delete the kafka add-on.
Extension
Preview
az containerapp add-on list
List all add-ons within the environment.
Extension
Preview
az containerapp add-on mariadb
Commands to manage the mariadb add-on for the Container Apps environment.
Extension
Preview
az containerapp add-on mariadb create
Command to create the mariadb add-on.
Extension
Preview
az containerapp add-on mariadb delete
Command to delete the mariadb add-on.
Extension
Preview
az containerapp add-on milvus
Commands to manage the milvus add-on for the Container Apps environment.
Extension
Preview
az containerapp add-on milvus create
Command to create the milvus add-on.
Extension
Preview
az containerapp add-on milvus delete
Command to delete the milvus service.
Extension
Preview
az containerapp add-on postgres
Commands to manage the postgres add-on for the Container Apps environment.
Extension
Preview
az containerapp add-on postgres create
Command to create the postgres add-on.
Extension
Preview
az containerapp add-on postgres delete
Command to delete the postgres add-on.
Extension
Preview
az containerapp add-on qdrant
Commands to manage the qdrant add-on for the Container Apps environment.
Extension
Preview
az containerapp add-on qdrant create
Command to create the qdrant add-on.
Extension
Preview
az containerapp add-on qdrant delete
Command to delete the qdrant add-on.
Extension
Preview
az containerapp add-on redis
Commands to manage the redis add-on for the Container Apps environment.
Extension
Preview
az containerapp add-on redis create
Command to create the redis add-on.
Extension
Preview
az containerapp add-on redis delete
Command to delete the redis add-on.
Extension
Preview
az containerapp add-on weaviate
Commands to manage the weaviate add-on for the Container Apps environment.
Extension
Preview
az containerapp add-on weaviate create
Command to create the weaviate add-on.
Extension
Preview
az containerapp add-on weaviate delete
Command to delete the weaviate service.
Extension
Preview
az containerapp arc
Install prerequisites for Kubernetes cluster on Arc.
Extension
Preview
az containerapp arc setup-core-dns
Setup CoreDNS for Kubernetes cluster on Arc.
Extension
Preview
az containerapp auth
Manage containerapp authentication and authorization.
Core and Extension
GA
az containerapp auth apple
Manage containerapp authentication and authorization of the Apple identity provider.
Core
GA
az containerapp auth apple show
Show the authentication settings for the Apple identity provider.
Core
GA
az containerapp auth apple update
Update the client id and client secret for the Apple identity provider.
Core
GA
az containerapp auth facebook
Manage containerapp authentication and authorization of the Facebook identity provider.
Core
GA
az containerapp auth facebook show
Show the authentication settings for the Facebook identity provider.
Core
GA
az containerapp auth facebook update
Update the app id and app secret for the Facebook identity provider.
Core
GA
az containerapp auth github
Manage containerapp authentication and authorization of the GitHub identity provider.
Core
GA
az containerapp auth github show
Show the authentication settings for the GitHub identity provider.
Core
GA
az containerapp auth github update
Update the client id and client secret for the GitHub identity provider.
Core
GA
az containerapp auth google
Manage containerapp authentication and authorization of the Google identity provider.
Core
GA
az containerapp auth google show
Show the authentication settings for the Google identity provider.
Core
GA
az containerapp auth google update
Update the client id and client secret for the Google identity provider.
Core
GA
az containerapp auth microsoft
Manage containerapp authentication and authorization of the Microsoft identity provider.
Core
GA
az containerapp auth microsoft show
Show the authentication settings for the Azure Active Directory identity provider.
Core
GA
az containerapp auth microsoft update
Update the client id and client secret for the Azure Active Directory identity provider.
Core
GA
az containerapp auth openid-connect
Manage containerapp authentication and authorization of the custom OpenID Connect identity providers.
Core
GA
az containerapp auth openid-connect add
Configure a new custom OpenID Connect identity provider.
Core
GA
az containerapp auth openid-connect remove
Removes an existing custom OpenID Connect identity provider.
Core
GA
az containerapp auth openid-connect show
Show the authentication settings for the custom OpenID Connect identity provider.
Core
GA
az containerapp auth openid-connect update
Update the client id and client secret setting name for an existing custom OpenID Connect identity provider.
Core
GA
az containerapp auth show
Show the authentication settings for the containerapp.
Core
GA
az containerapp auth show (containerapp extension)
Show the authentication settings for the containerapp.
Extension
GA
az containerapp auth twitter
Manage containerapp authentication and authorization of the Twitter identity provider.
Core
GA
az containerapp auth twitter show
Show the authentication settings for the Twitter identity provider.
Core
GA
az containerapp auth twitter update
Update the consumer key and consumer secret for the Twitter identity provider.
Core
GA
az containerapp auth update
Update the authentication settings for the containerapp.
Core
GA
az containerapp auth update (containerapp extension)
Update the authentication settings for the containerapp.
Extension
GA
az containerapp browse
Open a containerapp in the browser, if possible.
Core
GA
az containerapp compose
Commands to create Azure Container Apps from Compose specifications.
Core and Extension
GA
az containerapp compose create
Create one or more Container Apps in a new or existing Container App Environment from a Compose specification.
Core
GA
az containerapp compose create (containerapp extension)
Create one or more Container Apps in a new or existing Container App Environment from a Compose specification.
Extension
GA
az containerapp connected-env
Commands to manage Container Apps Connected environments for use with Arc enabled Container Apps.
Extension
Preview
az containerapp connected-env certificate
Commands to manage certificates for the Container Apps connected environment.
Extension
Preview
az containerapp connected-env certificate delete
Delete a certificate from the Container Apps connected environment.
Extension
Preview
az containerapp connected-env certificate list
List certificates for a connected environment.
Extension
Preview
az containerapp connected-env certificate upload
Add or update a certificate.
Extension
Preview
az containerapp connected-env create
Create a Container Apps connected environment.
Extension
Preview
az containerapp connected-env dapr-component
Commands to manage Dapr components for Container Apps connected environments.
Extension
Preview
az containerapp connected-env dapr-component list
List Dapr components for a connected environment.
Extension
Preview
az containerapp connected-env dapr-component remove
Remove a Dapr component from a connected environment.
Extension
Preview
az containerapp connected-env dapr-component set
Create or update a Dapr component.
Extension
Preview
az containerapp connected-env dapr-component show
Show the details of a Dapr component.
Extension
Preview
az containerapp connected-env delete
Delete a Container Apps connected environment.
Extension
Preview
az containerapp connected-env list
List Container Apps connected environments by subscription or resource group.
Extension
Preview
az containerapp connected-env show
Show details of a Container Apps connected environment.
Extension
Preview
az containerapp connected-env storage
Commands to manage storage for the Container Apps connected environment.
Extension
Preview
az containerapp connected-env storage list
List the storages for a connected environment.
Extension
Preview
az containerapp connected-env storage remove
Remove a storage from a connected environment.
Extension
Preview
az containerapp connected-env storage set
Create or update a storage.
Extension
Preview
az containerapp connected-env storage show
Show the details of a storage.
Extension
Preview
az containerapp connection
Commands to manage containerapp connections.
Core and Extension
GA
az containerapp connection create
Create a connection between a containerapp and a target resource.
Core and Extension
GA
az containerapp connection create app-insights
Create a containerapp connection to app-insights.
Core
GA
az containerapp connection create appconfig
Create a containerapp connection to appconfig.
Core
GA
az containerapp connection create cognitiveservices
Create a containerapp connection to cognitiveservices.
Core
GA
az containerapp connection create confluent-cloud
Create a containerapp connection to confluent-cloud.
Core
GA
az containerapp connection create containerapp
Create a containerapp-to-containerapp connection.
Core
GA
az containerapp connection create cosmos-cassandra
Create a containerapp connection to cosmos-cassandra.
Core
GA
az containerapp connection create cosmos-gremlin
Create a containerapp connection to cosmos-gremlin.
Core
GA
az containerapp connection create cosmos-mongo
Create a containerapp connection to cosmos-mongo.
Core
GA
az containerapp connection create cosmos-sql
Create a containerapp connection to cosmos-sql.
Core
GA
az containerapp connection create cosmos-table
Create a containerapp connection to cosmos-table.
Core
GA
az containerapp connection create eventhub
Create a containerapp connection to eventhub.
Core
GA
az containerapp connection create fabric-sql
Create a containerapp connection to fabric-sql.
Core
GA
az containerapp connection create fabric-sql (serviceconnector-passwordless extension)
Create a containerapp connection to fabric-sql.
Extension
GA
az containerapp connection create keyvault
Create a containerapp connection to keyvault.
Core
GA
az containerapp connection create mongodb-atlas
Create a containerapp connection to mongodb-atlas.
Core
GA
az containerapp connection create mysql
Create a containerapp connection to mysql.
Core
Deprecated
az containerapp connection create mysql-flexible
Create a containerapp connection to mysql-flexible.
Core
GA
az containerapp connection create mysql-flexible (serviceconnector-passwordless extension)
Create a containerapp connection to mysql-flexible.
Extension
GA
az containerapp connection create neon-postgres
Create a containerapp connection to neon-postgres.
Core
GA
az containerapp connection create postgres
Create a containerapp connection to postgres.
Core
Deprecated
az containerapp connection create postgres-flexible
Create a containerapp connection to postgres-flexible.
Core
GA
az containerapp connection create postgres-flexible (serviceconnector-passwordless extension)
Create a containerapp connection to postgres-flexible.
Extension
GA
az containerapp connection create redis
Create a containerapp connection to redis.
Core
GA
az containerapp connection create redis-enterprise
Create a containerapp connection to redis-enterprise.
Core
GA
az containerapp connection create servicebus
Create a containerapp connection to servicebus.
Core
GA
az containerapp connection create signalr
Create a containerapp connection to signalr.
Core
GA
az containerapp connection create sql
Create a containerapp connection to sql.
Core
GA
az containerapp connection create sql (serviceconnector-passwordless extension)
Create a containerapp connection to sql.
Extension
GA
az containerapp connection create storage-blob
Create a containerapp connection to storage-blob.
Core
GA
az containerapp connection create storage-file
Create a containerapp connection to storage-file.
Core
GA
az containerapp connection create storage-queue
Create a containerapp connection to storage-queue.
Core
GA
az containerapp connection create storage-table
Create a containerapp connection to storage-table.
Core
GA
az containerapp connection create webpubsub
Create a containerapp connection to webpubsub.
Core
GA
az containerapp connection delete
Delete a containerapp connection.
Core
GA
az containerapp connection list
List connections of a containerapp.
Core
GA
az containerapp connection list-configuration
List source configurations of a containerapp connection.
Core
GA
az containerapp connection list-support-types
List client types and auth types supported by containerapp connections.
Core
GA
az containerapp connection show
Get the details of a containerapp connection.
Core
GA
az containerapp connection update
Update a containerapp connection.
Core
GA
az containerapp connection update app-insights
Update a containerapp to app-insights connection.
Core
GA
az containerapp connection update appconfig
Update a containerapp to appconfig connection.
Core
GA
az containerapp connection update cognitiveservices
Update a containerapp to cognitiveservices connection.
Core
GA
az containerapp connection update confluent-cloud
Update a containerapp to confluent-cloud connection.
Core
GA
az containerapp connection update containerapp
Update a containerapp-to-containerapp connection.
Core
GA
az containerapp connection update cosmos-cassandra
Update a containerapp to cosmos-cassandra connection.
Core
GA
az containerapp connection update cosmos-gremlin
Update a containerapp to cosmos-gremlin connection.
Core
GA
az containerapp connection update cosmos-mongo
Update a containerapp to cosmos-mongo connection.
Core
GA
az containerapp connection update cosmos-sql
Update a containerapp to cosmos-sql connection.
Core
GA
az containerapp connection update cosmos-table
Update a containerapp to cosmos-table connection.
Core
GA
az containerapp connection update eventhub
Update a containerapp to eventhub connection.
Core
GA
az containerapp connection update fabric-sql
Update a containerapp to fabric-sql connection.
Core
GA
az containerapp connection update keyvault
Update a containerapp to keyvault connection.
Core
GA
az containerapp connection update mongodb-atlas
Update a containerapp to mongodb-atlas connection.
Core
GA
az containerapp connection update mysql
Update a containerapp to mysql connection.
Core
Deprecated
az containerapp connection update mysql-flexible
Update a containerapp to mysql-flexible connection.
Core
GA
az containerapp connection update neon-postgres
Update a containerapp to neon-postgres connection.
Core
GA
az containerapp connection update postgres
Update a containerapp to postgres connection.
Core
Deprecated
az containerapp connection update postgres-flexible
Update a containerapp to postgres-flexible connection.
Core
GA
az containerapp connection update redis
Update a containerapp to redis connection.
Core
GA
az containerapp connection update redis-enterprise
Update a containerapp to redis-enterprise connection.
Core
GA
az containerapp connection update servicebus
Update a containerapp to servicebus connection.
Core
GA
az containerapp connection update signalr
Update a containerapp to signalr connection.
Core
GA
az containerapp connection update sql
Update a containerapp to sql connection.
Core
GA
az containerapp connection update storage-blob
Update a containerapp to storage-blob connection.
Core
GA
az containerapp connection update storage-file
Update a containerapp to storage-file connection.
Core
GA
az containerapp connection update storage-queue
Update a containerapp to storage-queue connection.
Core
GA
az containerapp connection update storage-table
Update a containerapp to storage-table connection.
Core
GA
az containerapp connection update webpubsub
Update a containerapp to webpubsub connection.
Core
GA
az containerapp connection validate
Validate a containerapp connection.
Core
GA
az containerapp connection wait
Place the CLI in a waiting state until a condition of the connection is met.
Core
GA
az containerapp create
Create a container app.
Core
GA
az containerapp create (containerapp extension)
Create a container app.
Extension
GA
az containerapp dapr
Commands to manage Dapr. To manage Dapr components, see
az containerapp env dapr-component
.
Core
GA
az containerapp dapr disable
Disable Dapr for a container app. Removes existing values.
Core
GA
az containerapp dapr enable
Enable Dapr for a container app. Updates existing values.
Core
GA
az containerapp debug
Open an SSH-like interactive shell within a container app debug console or execute a command inside the container and exit.
Extension
Preview
az containerapp delete
Delete a container app.
Core
GA
az containerapp delete (containerapp extension)
Delete a container app.
Extension
GA
az containerapp env
Commands to manage Container Apps environments.
Core and Extension
GA
az containerapp env certificate
Commands to manage certificates for the Container Apps environment.
Core and Extension
GA
az containerapp env certificate create
Create a managed certificate.
Core
Preview
az containerapp env certificate delete
Delete a certificate from the Container Apps environment.
Core
GA
az containerapp env certificate delete (containerapp extension)
Delete a certificate from the Container Apps environment.
Extension
GA
az containerapp env certificate list
List certificates for an environment.
Core
GA
az containerapp env certificate list (containerapp extension)
List certificates for an environment.
Extension
GA
az containerapp env certificate upload
Add or update a certificate.
Core
GA
az containerapp env certificate upload (containerapp extension)
Add or update a certificate.
Extension
GA
az containerapp env create
Create a Container Apps environment.
Core
GA
az containerapp env create (containerapp extension)
Create a Container Apps environment.
Extension
GA
az containerapp env dapr-component
Commands to manage Dapr components for the Container Apps environment.
Core and Extension
GA
az containerapp env dapr-component init
Initializes Dapr components and dev services for an environment.
Extension
Preview
az containerapp env dapr-component list
List Dapr components for an environment.
Core
GA
az containerapp env dapr-component remove
Remove a Dapr component from an environment.
Core
GA
az containerapp env dapr-component resiliency
Commands to manage resiliency policies for a dapr component.
Extension
Preview
az containerapp env dapr-component resiliency create
Create resiliency policies for a dapr component.
Extension
Preview
az containerapp env dapr-component resiliency delete
Delete resiliency policies for a dapr component.
Extension
Preview
az containerapp env dapr-component resiliency list
List resiliency policies for a dapr component.
Extension
Preview
az containerapp env dapr-component resiliency show
Show resiliency policies for a dapr component.
Extension
Preview
az containerapp env dapr-component resiliency update
Update resiliency policies for a dapr component.
Extension
Preview
az containerapp env dapr-component set
Create or update a Dapr component.
Core
GA
az containerapp env dapr-component show
Show the details of a Dapr component.
Core
GA
az containerapp env delete
Delete a Container Apps environment.
Core
GA
az containerapp env delete (containerapp extension)
Delete a Container Apps environment.
Extension
GA
az containerapp env dotnet-component
Commands to manage DotNet components within the environment.
Extension
Preview
az containerapp env dotnet-component create
Command to create DotNet component to enable Aspire Dashboard. Supported DotNet component type is Aspire Dashboard.
Extension
Preview
az containerapp env dotnet-component delete
Command to delete DotNet component to disable Aspire Dashboard.
Extension
Preview
az containerapp env dotnet-component list
Command to list DotNet components within the environment.
Extension
Preview
az containerapp env dotnet-component show
Command to show DotNet component in environment.
Extension
Preview
az containerapp env http-route-config
Commands to manage environment level http routing.
Core
GA
az containerapp env http-route-config create
Create a new http route config.
Core
GA
az containerapp env http-route-config delete
Delete a http route config.
Core
GA
az containerapp env http-route-config list
List the http route configs in the environment.
Core
GA
az containerapp env http-route-config show
Show a http route config.
Core
GA
az containerapp env http-route-config update
Update a http route config.
Core
GA
az containerapp env identity
Commands to manage environment managed identities.
Extension
Preview
az containerapp env identity assign
Assign managed identity to a managed environment.
Extension
Preview
az containerapp env identity remove
Remove a managed identity from a managed environment.
Extension
Preview
az containerapp env identity show
Show managed identities of a managed environment.
Extension
Preview
az containerapp env java-component
Commands to manage Java components within the environment.
Extension
GA
az containerapp env java-component admin-for-spring
Commands to manage the Admin for Spring for the Container Apps environment.
Extension
GA
az containerapp env java-component admin-for-spring create
Command to create the Admin for Spring.
Extension
GA
az containerapp env java-component admin-for-spring delete
Command to delete the Admin for Spring.
Extension
GA
az containerapp env java-component admin-for-spring show
Command to show the Admin for Spring.
Extension
GA
az containerapp env java-component admin-for-spring update
Command to update the Admin for Spring.
Extension
GA
az containerapp env java-component config-server-for-spring
Commands to manage the Config Server for Spring for the Container Apps environment.
Extension
GA
az containerapp env java-component config-server-for-spring create
Command to create the Config Server for Spring.
Extension
GA
az containerapp env java-component config-server-for-spring delete
Command to delete the Config Server for Spring.
Extension
GA
az containerapp env java-component config-server-for-spring show
Command to show the Config Server for Spring.
Extension
GA
az containerapp env java-component config-server-for-spring update
Command to update the Config Server for Spring.
Extension
GA
az containerapp env java-component eureka-server-for-spring
Commands to manage the Eureka Server for Spring for the Container Apps environment.
Extension
GA
az containerapp env java-component eureka-server-for-spring create
Command to create the Eureka Server for Spring.
Extension
GA
az containerapp env java-component eureka-server-for-spring delete
Command to delete the Eureka Server for Spring.
Extension
GA
az containerapp env java-component eureka-server-for-spring show
Command to show the Eureka Server for Spring.
Extension
GA
az containerapp env java-component eureka-server-for-spring update
Command to update the Eureka Server for Spring.
Extension
GA
az containerapp env java-component gateway-for-spring
Commands to manage the Gateway for Spring for the Container Apps environment.
Extension
Preview
az containerapp env java-component gateway-for-spring create
Command to create the Gateway for Spring.
Extension
Preview
az containerapp env java-component gateway-for-spring delete
Command to delete the Gateway for Spring.
Extension
Preview
az containerapp env java-component gateway-for-spring show
Command to show the Gateway for Spring.
Extension
Preview
az containerapp env java-component gateway-for-spring update
Command to update the Gateway for Spring.
Extension
Preview
az containerapp env java-component list
List all Java components within the environment.
Extension
GA
az containerapp env java-component nacos
Commands to manage the Nacos for the Container Apps environment.
Extension
Preview
az containerapp env java-component nacos create
Command to create the Nacos.
Extension
Preview
az containerapp env java-component nacos delete
Command to delete the Nacos.
Extension
Preview
az containerapp env java-component nacos show
Command to show the Nacos.
Extension
Preview
az containerapp env java-component nacos update
Command to update the Nacos.
Extension
Preview
az containerapp env list
List Container Apps environments by subscription or resource group.
Core
GA
az containerapp env list (containerapp extension)
List Container Apps environments by subscription or resource group.
Extension
GA
az containerapp env list-usages
List usages of quotas for specific managed environment.
Core
GA
az containerapp env logs
Show container app environment logs.
Core
GA
az containerapp env logs show
Show past environment logs and/or print logs in real time (with the --follow parameter).
Core
GA
az containerapp env maintenance-config
Commands to manage Planned Maintenance for Container Apps.
Extension
Preview
az containerapp env maintenance-config add
Add Planned Maintenance to a Container App Environment.
Extension
Preview
az containerapp env maintenance-config list
List Planned Maintenance in a Container App Environment.
Extension
Preview
az containerapp env maintenance-config remove
Remove Planned Maintenance in a Container App Environment.
Extension
Preview
az containerapp env maintenance-config update
Update Planned Maintenance in a Container App Environment.
Extension
Preview
az containerapp env premium-ingress
Configure premium ingress settings for the environment.
Core
GA
az containerapp env premium-ingress add
Enable the premium ingress settings for the environment.
Core
GA
az containerapp env premium-ingress remove
Remove the ingress settings and restores the system to default values.
Core
GA
az containerapp env premium-ingress show
Show the premium ingress settings for the environment.
Core
GA
az containerapp env premium-ingress update
Update the premium ingress settings for the environment.
Core
GA
az containerapp env show
Show details of a Container Apps environment.
Core
GA
az containerapp env show (containerapp extension)
Show details of a Container Apps environment.
Extension
GA
az containerapp env storage
Commands to manage storage for the Container Apps environment.
Core and Extension
GA
az containerapp env storage list
List the storages for an environment.
Core
GA
az containerapp env storage list (containerapp extension)
List the storages for an environment.
Extension
GA
az containerapp env storage remove
Remove a storage from an environment.
Core
GA
az containerapp env storage remove (containerapp extension)
Remove a storage from an environment.
Extension
GA
az containerapp env storage set
Create or update a storage.
Core
GA
az containerapp env storage set (containerapp extension)
Create or update a storage.
Extension
GA
az containerapp env storage show
Show the details of a storage.
Core
GA
az containerapp env storage show (containerapp extension)
Show the details of a storage.
Extension
GA
az containerapp env telemetry
Commands to manage telemetry settings for the container apps environment.
Extension
Preview
az containerapp env telemetry app-insights
Commands to manage app insights settings for the container apps environment.
Extension
Preview
az containerapp env telemetry app-insights delete
Delete container apps environment telemetry app insights settings.
Extension
Preview
az containerapp env telemetry app-insights set
Create or update container apps environment telemetry app insights settings.
Extension
Preview
az containerapp env telemetry app-insights show
Show container apps environment telemetry app insights settings.
Extension
Preview
az containerapp env telemetry data-dog
Commands to manage data dog settings for the container apps environment.
Extension
Preview
az containerapp env telemetry data-dog delete
Delete container apps environment telemetry data dog settings.
Extension
Preview
az containerapp env telemetry data-dog set
Create or update container apps environment telemetry data dog settings.
Extension
Preview
az containerapp env telemetry data-dog show
Show container apps environment telemetry data dog settings.
Extension
Preview
az containerapp env telemetry otlp
Commands to manage otlp settings for the container apps environment.
Extension
Preview
az containerapp env telemetry otlp add
Add container apps environment telemetry otlp settings.
Extension
Preview
az containerapp env telemetry otlp list
List container apps environment telemetry otlp settings.
Extension
Preview
az containerapp env telemetry otlp remove
Remove container apps environment telemetry otlp settings.
Extension
Preview
az containerapp env telemetry otlp show
Show container apps environment telemetry otlp settings.
Extension
Preview
az containerapp env telemetry otlp update
Update container apps environment telemetry otlp settings.
Extension
Preview
az containerapp env update
Update a Container Apps environment.
Core
GA
az containerapp env update (containerapp extension)
Update a Container Apps environment.
Extension
GA
az containerapp env workload-profile
Manage the workload profiles of a Container Apps environment.
Core
GA
az containerapp env workload-profile add
Create a workload profile in a Container Apps environment.
Core
GA
az containerapp env workload-profile delete
Delete a workload profile from a Container Apps environment.
Core
GA
az containerapp env workload-profile list
List the workload profiles from a Container Apps environment.
Core
GA
az containerapp env workload-profile list-supported
List the supported workload profiles in a region.
Core
GA
az containerapp env workload-profile show
Show a workload profile from a Container Apps environment.
Core
GA
az containerapp env workload-profile update
Update an existing workload profile in a Container Apps environment.
Core
GA
az containerapp exec
Open an SSH-like interactive shell within a container app replica.
Core
GA
az containerapp function
Commands related to Azure Functions on Container Apps.
Extension
Preview
az containerapp function invocations
Commands to get function invocation data and traces from Application Insights.
Extension
Preview
az containerapp function invocations summary
Get function invocation summary from Application Insights.
Extension
Preview
az containerapp function invocations traces
Get function invocation traces from Application Insights.
Extension
Preview
az containerapp function keys
Commands for keys management in an Azure Functions on Container Apps.
Extension
Preview
az containerapp function keys list
List function keys in an Azure Functions on Container Apps.
Extension
Preview
az containerapp function keys set
Create or update specific function key in an Azure Functions on Container Apps.
Extension
Preview
az containerapp function keys show
Show specific function key in an Azure Functions on Container Apps.
Extension
Preview
az containerapp function list
List all functions in an Azure Functions on Container Apps.
Extension
Preview
az containerapp function show
Get details of a function in an Azure Functions on Container Apps.
Extension
Preview
az containerapp github-action
Commands to manage GitHub Actions.
Core and Extension
GA
az containerapp github-action add
Add a GitHub Actions workflow to a repository to deploy a container app.
Core
GA
az containerapp github-action add (containerapp extension)
Add a GitHub Actions workflow to a repository to deploy a container app.
Extension
GA
az containerapp github-action delete
Remove a previously configured Container Apps GitHub Actions workflow from a repository.
Core
GA
az containerapp github-action show
Show the GitHub Actions configuration on a container app.
Core
GA
az containerapp hostname
Commands to manage hostnames of a container app.
Core and Extension
GA
az containerapp hostname add
Add the hostname to a container app without binding.
Core
GA
az containerapp hostname bind
Add or update the hostname and binding with a certificate.
Core
GA
az containerapp hostname bind (containerapp extension)
Add or update the hostname and binding with a certificate.
Extension
GA
az containerapp hostname delete
Delete hostnames from a container app.
Core
GA
az containerapp hostname list
List the hostnames of a container app.
Core
GA
az containerapp identity
Commands to manage managed identities.
Core
GA
az containerapp identity assign
Assign managed identity to a container app.
Core
GA
az containerapp identity remove
Remove a managed identity from a container app.
Core
GA
az containerapp identity show
Show managed identities of a container app.
Core
GA
az containerapp ingress
Commands to manage ingress and traffic-splitting.
Core
GA
az containerapp ingress access-restriction
Commands to manage IP access restrictions.
Core
GA
az containerapp ingress access-restriction list
List IP access restrictions for a container app.
Core
GA
az containerapp ingress access-restriction remove
Remove IP access restrictions from a container app.
Core
GA
az containerapp ingress access-restriction set
Configure IP access restrictions for a container app.
Core
GA
az containerapp ingress cors
Commands to manage CORS policy for a container app.
Core
GA
az containerapp ingress cors disable
Disable CORS policy for a container app.
Core
GA
az containerapp ingress cors enable
Enable CORS policy for a container app.
Core
GA
az containerapp ingress cors show
Show CORS policy for a container app.
Core
GA
az containerapp ingress cors update
Update CORS policy for a container app.
Core
GA
az containerapp ingress disable
Disable ingress for a container app.
Core
GA
az containerapp ingress enable
Enable or update ingress for a container app.
Core
GA
az containerapp ingress show
Show details of a container app's ingress.
Core
GA
az containerapp ingress sticky-sessions
Commands to set Sticky session affinity for a container app.
Core
GA
az containerapp ingress sticky-sessions set
Configure Sticky session for a container app.
Core
GA
az containerapp ingress sticky-sessions show
Show the Affinity for a container app.
Core
GA
az containerapp ingress traffic
Commands to manage traffic-splitting.
Core
GA
az containerapp ingress traffic set
Configure traffic-splitting for a container app.
Core
GA
az containerapp ingress traffic show
Show traffic-splitting configuration for a container app.
Core
GA
az containerapp ingress update
Update ingress for a container app.
Core
GA
az containerapp java
Commands to manage Java workloads.
Extension
GA
az containerapp java logger
Dynamically change log level for Java workloads.
Extension
GA
az containerapp java logger delete
Delete logger for Java workloads.
Extension
GA
az containerapp java logger set
Create or update logger for Java workloads.
Extension
GA
az containerapp java logger show
Display logger setting for Java workloads.
Extension
GA
az containerapp job
Commands to manage Container Apps jobs.
Core and Extension
GA
az containerapp job create
Create a container apps job.
Core
GA
az containerapp job create (containerapp extension)
Create a container apps job.
Extension
GA
az containerapp job delete
Delete a Container Apps Job.
Core
GA
az containerapp job delete (containerapp extension)
Delete a Container Apps Job.
Extension
GA
az containerapp job execution
Commands to view executions of a Container App Job.
Core
GA
az containerapp job execution list
Get list of all executions of a Container App Job.
Core
GA
az containerapp job execution show
Get execution of a Container App Job.
Core
GA
az containerapp job identity
Commands to manage managed identities for container app job.
Core
GA
az containerapp job identity assign
Assign managed identity to a container app job.
Core
GA
az containerapp job identity remove
Remove a managed identity from a container app job.
Core
GA
az containerapp job identity show
Show managed identities of a container app job.
Core
GA
az containerapp job list
List Container Apps Job by subscription or resource group.
Core
GA
az containerapp job list (containerapp extension)
List Container Apps Job by subscription or resource group.
Extension
GA
az containerapp job logs
Show container app job logs.
Extension
Preview
az containerapp job logs show
Show past logs and/or print logs in real time (with the --follow parameter). Note that the logs are only taken from one execution, replica, and container.
Extension
Preview
az containerapp job registry
Commands to manage container registry information of a Container App Job.
Core and Extension
Preview
az containerapp job registry list
List container registries configured in a Container App Job.
Core
Preview
az containerapp job registry remove
Remove a container registry's details in a Container App Job.
Core
Preview
az containerapp job registry set
Add or update a container registry's details in a Container App Job.
Core
Preview
az containerapp job registry set (containerapp extension)
Add or update a container registry's details in a Container App Job.
Extension
Preview
az containerapp job registry show
Show details of a container registry from a Container App Job.
Core
Preview
az containerapp job replica
Manage container app replicas.
Extension
Preview
az containerapp job replica list
List a container app job execution's replica.
Extension
Preview
az containerapp job secret
Commands to manage secrets.
Core
GA
az containerapp job secret list
List the secrets of a container app job.
Core
GA
az containerapp job secret remove
Remove secrets from a container app job.
Core
GA
az containerapp job secret set
Create/update secrets.
Core
GA
az containerapp job secret show
Show details of a secret.
Core
GA
az containerapp job show
Show details of a Container Apps Job.
Core
GA
az containerapp job show (containerapp extension)
Show details of a Container Apps Job.
Extension
GA
az containerapp job start
Start a Container Apps Job execution.
Core
GA
az containerapp job stop
Stops a Container Apps Job execution.
Core
GA
az containerapp job update
Update a Container Apps Job.
Core
GA
az containerapp job update (containerapp extension)
Update a Container Apps Job.
Extension
GA
az containerapp label-history
Show the history for one or more labels on the Container App.
Extension
Preview
az containerapp label-history list
List the history for all labels on the Container App.
Extension
Preview
az containerapp label-history show
Show the history for a specific label on the Container App.
Extension
Preview
az containerapp list
List container apps.
Core
GA
az containerapp list (containerapp extension)
List container apps.
Extension
GA
az containerapp list-usages
List usages of subscription level quotas in specific region.
Core
GA
az containerapp logs
Show container app logs.
Core
GA
az containerapp logs show
Show past logs and/or print logs in real time (with the --follow parameter). Note that the logs are only taken from one revision, replica, and container (for non-system logs).
Core
GA
az containerapp patch
Patch Azure Container Apps. Patching is only available for the apps built using the source to cloud feature. See
https://aka.ms/aca-local-source-to-cloud
.
Extension
Preview
az containerapp patch apply
List and apply container apps to be patched. Patching is only available for the apps built using the source to cloud feature. See
https://aka.ms/aca-local-source-to-cloud
.
Extension
Preview
az containerapp patch interactive
List and select container apps to be patched in an interactive way. Patching is only available for the apps built using the source to cloud feature. See
https://aka.ms/aca-local-source-to-cloud
.
Extension
Preview
az containerapp patch list
List container apps that can be patched. Patching is only available for the apps built using the source to cloud feature. See
https://aka.ms/aca-local-source-to-cloud
.
Extension
Preview
az containerapp registry
Commands to manage container registry information.
Core and Extension
GA
az containerapp registry list
List container registries configured in a container app.
Core
GA
az containerapp registry remove
Remove a container registry's details.
Core
GA
az containerapp registry set
Add or update a container registry's details.
Core
GA
az containerapp registry set (containerapp extension)
Add or update a container registry's details.
Extension
Preview
az containerapp registry show
Show details of a container registry.
Core
GA
az containerapp replica
Manage container app replicas.
Core and Extension
GA
az containerapp replica count
Count of a container app's replica(s).
Extension
Preview
az containerapp replica list
List a container app revision's replica.
Core
GA
az containerapp replica list (containerapp extension)
List a container app revision's replica.
Extension
GA
az containerapp replica show
Show a container app replica.
Core
GA
az containerapp replica show (containerapp extension)
Show a container app replica.
Extension
GA
az containerapp resiliency
Commands to manage resiliency policies for a container app.
Extension
Preview
az containerapp resiliency create
Create resiliency policies for a container app.
Extension
Preview
az containerapp resiliency delete
Delete resiliency policies for a container app.
Extension
Preview
az containerapp resiliency list
List resiliency policies for a container app.
Extension
Preview
az containerapp resiliency show
Show resiliency policies for a container app.
Extension
Preview
az containerapp resiliency update
Update resiliency policies for a container app.
Extension
Preview
az containerapp revision
Commands to manage revisions.
Core and Extension
GA
az containerapp revision activate
Activate a revision.
Core
GA
az containerapp revision copy
Create a revision based on a previous revision.
Core
GA
az containerapp revision deactivate
Deactivate a revision.
Core
GA
az containerapp revision label
Manage revision labels assigned to traffic weights.
Core and Extension
GA
az containerapp revision label add
Set a revision label to a revision with an associated traffic weight.
Core
GA
az containerapp revision label add (containerapp extension)
Set a revision label to a revision with an associated traffic weight.
Extension
GA
az containerapp revision label remove
Remove a revision label from a revision with an associated traffic weight.
Core
GA
az containerapp revision label remove (containerapp extension)
Remove a revision label from a revision with an associated traffic weight.
Extension
GA
az containerapp revision label swap
Swap a revision label between two revisions with associated traffic weights.
Core
GA
az containerapp revision list
List a container app's revisions.
Core
GA
az containerapp revision restart
Restart a revision.
Core
GA
az containerapp revision set-mode
Set the revision mode of a container app.
Core
GA
az containerapp revision set-mode (containerapp extension)
Set the revision mode of a container app.
Extension
GA
az containerapp revision show
Show details of a revision.
Core
GA
az containerapp secret
Commands to manage secrets.
Core
GA
az containerapp secret list
List the secrets of a container app.
Core
GA
az containerapp secret remove
Remove secrets from a container app.
Core
GA
az containerapp secret set
Create/update secrets.
Core
GA
az containerapp secret show
Show details of a secret.
Core
GA
az containerapp session
Commands to manage sessions.To learn more about individual commands under each subgroup run containerapp session [subgroup name] --help.
Extension
GA
az containerapp session code-interpreter
Commands to interact with and manage code interpreter sessions.
Extension
GA
az containerapp session code-interpreter delete-file
Delete a file uploaded to a code interpreter session.
Extension
GA
az containerapp session code-interpreter execute
Execute code in a code interpreter session.
Extension
GA
az containerapp session code-interpreter list-files
List files uploaded to a code interpreter session.
Extension
GA
az containerapp session code-interpreter show-file-content
Show the content a file uploaded to a code interpreter session.
Extension
GA
az containerapp session code-interpreter show-file-metadata
Shows the meta-data content a file uploaded to a code interpreter session.
Extension
GA
az containerapp session code-interpreter upload-file
Upload a file to a code interpreter session .
Extension
GA
az containerapp session stop
Stop a custom container session.
Extension
Preview
az containerapp sessionpool
Commands to manage session pools.
Extension
GA
az containerapp sessionpool create
Create or update a Session pool.
Extension
GA
az containerapp sessionpool delete
Delete a session pool.
Extension
GA
az containerapp sessionpool list
List Session Pools by subscription or resource group.
Extension
GA
az containerapp sessionpool show
Show details of a Session Pool.
Extension
GA
az containerapp sessionpool update
Update a Session pool.
Extension
GA
az containerapp show
Show details of a container app.
Core
GA
az containerapp show (containerapp extension)
Show details of a container app.
Extension
GA
az containerapp show-custom-domain-verification-id
Show the verification id for binding app or environment custom domains.
Core
GA
az containerapp ssl
Upload certificate to a managed environment, add hostname to an app in that environment, and bind the certificate to the hostname.
Core
GA
az containerapp ssl upload
Upload certificate to a managed environment, add hostname to an app in that environment, and bind the certificate to the hostname.
Core
GA
az containerapp up
Create or update a container app as well as any associated resources (ACR, resource group, container apps environment, GitHub Actions, etc.).
Core
GA
az containerapp up (containerapp extension)
Create or update a container app as well as any associated resources (ACR, resource group, container apps environment, GitHub Actions, etc.).
Extension
GA
az containerapp update
Update a container app. In multiple revisions mode, create a new revision based on the latest revision.
Core
GA
az containerapp update (containerapp extension)
Update a container app. In multiple revisions mode, create a new revision based on the latest revision.
Extension
GA
az containerapp browse
Edit
Open a containerapp in the browser, if possible.
```
az containerapp browse [--acquire-policy-token]
                       [--change-reference]
                       [--ids]
                       [--name]
                       [--resource-group]
                       [--subscription]
```
Examples
open a containerapp in the browser
```
az containerapp browse -n my-containerapp -g MyResourceGroup
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
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
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
az containerapp create
Edit
Create a container app.
```
az containerapp create --name
                       --resource-group
                       [--acquire-policy-token]
                       [--allow-insecure {false, true}]
                       [--args]
                       [--change-reference]
                       [--command]
                       [--container-name]
                       [--cpu]
                       [--dal --dapr-enable-api-logging]
                       [--dapr-app-id]
                       [--dapr-app-port]
                       [--dapr-app-protocol {grpc, http}]
                       [--dapr-http-max-request-size --dhmrs]
                       [--dapr-http-read-buffer-size --dhrbs]
                       [--dapr-log-level {debug, error, info, warn}]
                       [--enable-dapr {false, true}]
                       [--env-vars]
                       [--environment]
                       [--exposed-port]
                       [--image]
                       [--ingress {external, internal}]
                       [--max-replicas]
                       [--memory]
                       [--min-replicas]
                       [--no-wait]
                       [--registry-identity]
                       [--registry-password]
                       [--registry-server]
                       [--registry-username]
                       [--revision-suffix]
                       [--revisions-mode {multiple, single}]
                       [--scale-rule-auth --sra]
                       [--scale-rule-http-concurrency --scale-rule-tcp-concurrency --srhc --srtc]
                       [--scale-rule-metadata --srm]
                       [--scale-rule-name --srn]
                       [--scale-rule-type --srt]
                       [--secret-volume-mount]
                       [--secrets]
                       [--system-assigned]
                       [--tags]
                       [--target-port]
                       [--termination-grace-period --tgp]
                       [--transport {auto, http, http2, tcp}]
                       [--user-assigned]
                       [--workload-profile-name]
                       [--yaml]
```
Examples
Create a container app and retrieve its fully qualified domain name.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image myregistry.azurecr.io/my-app:v1.0 --environment MyContainerappEnv \
    --ingress external --target-port 80 \
    --registry-server myregistry.azurecr.io --registry-username myregistry --registry-password $REGISTRY_PASSWORD \
    --query properties.configuration.ingress.fqdn
```
Create a container app with resource requirements and replica count limits.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image nginx --environment MyContainerappEnv \
    --cpu 0.5 --memory 1.0Gi \
    --min-replicas 4 --max-replicas 8
```
Create a container app with secrets and environment variables.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-app:v1.0 --environment MyContainerappEnv \
    --secrets mysecret=secretvalue1 anothersecret="secret value 2" \
    --env-vars GREETING="Hello, world" SECRETENV=secretref:anothersecret
```
Create a container app using a YAML configuration. Example YAML configuration - https://aka.ms/azure-container-apps-yaml
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --environment MyContainerappEnv \
    --yaml "path/to/yaml/file.yml"
```
Create a container app with an http scale rule
```
az containerapp create -n myapp -g mygroup --environment myenv --image nginx \
    --scale-rule-name my-http-rule \
    --scale-rule-http-concurrency 50
```
Create a container app with a custom scale rule
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-queue-processor --environment MyContainerappEnv \
    --min-replicas 4 --max-replicas 8 \
    --scale-rule-name queue-based-autoscaling \
    --scale-rule-type azure-queue \
    --scale-rule-metadata "accountName=mystorageaccountname" \
                          "cloud=AzurePublicCloud" \
                          "queueLength=5" "queueName=foo" \
    --scale-rule-auth "connection=my-connection-string-secret-name"
```
Create a container app with secrets and mounts them in a volume.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-app:v1.0 --environment MyContainerappEnv \
    --secrets mysecret=secretvalue1 anothersecret="secret value 2" \
    --secret-volume-mount "mnt/secrets"
```
Required Parameters
--name -n
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
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
--allow-insecure
Allow insecure connections for ingress traffic.
Property
Value
Default value:
False
Accepted values:
false, true
--args
A list of container startup command argument(s). Space-separated values e.g. "-c" "mycommand". Empty string to clear existing values.
Property
Value
Parameter group:
Container Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--command
A list of supported commands on the container that will executed during startup. Space-separated values e.g. "/bin/queue" "mycommand". Empty string to clear existing values.
Property
Value
Parameter group:
Container Arguments
--container-name
Name of the container.
Property
Value
Parameter group:
Container Arguments
--cpu
Required CPU in cores from 0.25 - 2.0, e.g. 0.5.
Property
Value
Parameter group:
Container Arguments
--dal --dapr-enable-api-logging
Enable API logging for the Dapr sidecar.
Property
Value
Parameter group:
Dapr Arguments
Default value:
False
--dapr-app-id
The Dapr application identifier.
Property
Value
Parameter group:
Dapr Arguments
--dapr-app-port
The port Dapr uses to talk to the application.
Property
Value
Parameter group:
Dapr Arguments
--dapr-app-protocol
The protocol Dapr uses to talk to the application.
Property
Value
Parameter group:
Dapr Arguments
Accepted values:
grpc, http
--dapr-http-max-request-size --dhmrs
Increase max size of request body http and grpc servers parameter in MB to handle uploading of big files.
Property
Value
Parameter group:
Dapr Arguments
--dapr-http-read-buffer-size --dhrbs
Dapr max size of http header read buffer in KB to handle when sending multi-KB headers..
Property
Value
Parameter group:
Dapr Arguments
--dapr-log-level
Set the log level for the Dapr sidecar.
Property
Value
Parameter group:
Dapr Arguments
Accepted values:
debug, error, info, warn
--enable-dapr
Boolean indicating if the Dapr side car is enabled.
Property
Value
Parameter group:
Dapr Arguments
Default value:
False
Accepted values:
false, true
--env-vars
A list of environment variable(s) for the container. Space-separated values in 'key=value' format. Empty string to clear existing values. Prefix value with 'secretref:' to reference a secret.
Property
Value
Parameter group:
Container Arguments
--environment
Name or resource ID of the container app's environment.
--exposed-port
Additional exposed port. Only supported by tcp transport protocol. Must be unique per environment if the app ingress is external.
Property
Value
Parameter group:
Ingress Arguments
--image -i
Container image, e.g. publisher/image-name:tag.
Property
Value
Parameter group:
Container Arguments
--ingress
The ingress type.
Property
Value
Parameter group:
Ingress Arguments
Accepted values:
external, internal
--max-replicas
The maximum number of replicas.
Property
Value
Parameter group:
Scale Arguments
--memory
Required memory from 0.5 - 4.0 ending with "Gi", e.g. 1.0Gi.
Property
Value
Parameter group:
Container Arguments
--min-replicas
The minimum number of replicas.
Property
Value
Parameter group:
Scale Arguments
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--registry-identity
A Managed Identity to authenticate with the registry server instead of username/password. Use a resource ID or 'system' for user-defined and system-defined identities, respectively. The registry must be an ACR. If possible, an 'acrpull' role assignment will be created for the identity automatically.
Property
Value
Parameter group:
Configuration Arguments
--registry-password
The password to log in to container registry. If stored as a secret, value must start with 'secretref:' followed by the secret name.
Property
Value
Parameter group:
Configuration Arguments
--registry-server
The container registry server hostname, e.g. myregistry.azurecr.io.
Property
Value
Parameter group:
Configuration Arguments
--registry-username
The username to log in to container registry.
Property
Value
Parameter group:
Configuration Arguments
--revision-suffix
User friendly suffix that is appended to the revision name.
Property
Value
Parameter group:
Container Arguments
--revisions-mode
The active revisions mode for the container app.
Property
Value
Parameter group:
Configuration Arguments
Default value:
single
Accepted values:
multiple, single
--scale-rule-auth --sra
Scale rule auth parameters. Auth parameters must be in format "{triggerParameter}={secretRef} {triggerParameter}={secretRef} ...".
Property
Value
Parameter group:
Scale Arguments
--scale-rule-http-concurrency --scale-rule-tcp-concurrency --srhc --srtc
The maximum number of concurrent requests before scale out. Only supported for http and tcp scale rules.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-metadata --srm
Scale rule metadata. Metadata must be in format "{key}={value} {key}={value} ...".
Property
Value
Parameter group:
Scale Arguments
--scale-rule-name --srn
The name of the scale rule.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-type --srt
The type of the scale rule. Default: http. For more information please visit
https://learn.microsoft.com/azure/container-apps/scale-app#scale-triggers
.
Property
Value
Parameter group:
Scale Arguments
--secret-volume-mount
Path to mount all secrets e.g. mnt/secrets.
--secrets -s
A list of secret(s) for the container app. Space-separated values in 'key=value' format.
Property
Value
Parameter group:
Configuration Arguments
--system-assigned
Boolean indicating whether to assign system-assigned identity.
Property
Value
Parameter group:
Identity Arguments
Default value:
False
--tags
Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags.
--target-port
The application port used for ingress traffic.
Property
Value
Parameter group:
Ingress Arguments
--termination-grace-period --tgp
Duration in seconds a replica is given to gracefully shut down before it is forcefully terminated. (Default: 30).
--transport
The transport protocol used for ingress traffic.
Property
Value
Parameter group:
Ingress Arguments
Default value:
auto
Accepted values:
auto, http, http2, tcp
--user-assigned
Space-separated user identities to be assigned.
Property
Value
Parameter group:
Identity Arguments
--workload-profile-name -w
Name of the workload profile to run the app on.
--yaml
Path to a .yaml file with the configuration of a container app. All other parameters will be ignored. For an example, see
https://learn.microsoft.com/azure/container-apps/azure-resource-manager-api-spec#examples
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
az containerapp create (containerapp extension)
Create a container app.
```
az containerapp create --name
                       --resource-group
                       [--acquire-policy-token]
                       [--allow-insecure {false, true}]
                       [--args]
                       [--artifact]
                       [--bind]
                       [--branch]
                       [--build-env-vars]
                       [--change-reference]
                       [--command]
                       [--container-name]
                       [--context-path]
                       [--cpu]
                       [--customized-keys]
                       [--dal --dapr-enable-api-logging]
                       [--dapr-app-id]
                       [--dapr-app-port]
                       [--dapr-app-protocol {grpc, http}]
                       [--dapr-http-max-request-size --dhmrs]
                       [--dapr-http-read-buffer-size --dhrbs]
                       [--dapr-log-level {debug, error, info, warn}]
                       [--enable-dapr {false, true}]
                       [--enable-java-agent {false, true}]
                       [--enable-java-metrics {false, true}]
                       [--env-vars]
                       [--environment]
                       [--environment-type {connected, managed}]
                       [--exposed-port]
                       [--image]
                       [--ingress {external, internal}]
                       [--kind {functionapp}]
                       [--max-inactive-revisions]
                       [--max-replicas]
                       [--memory]
                       [--min-replicas]
                       [--no-wait]
                       [--registry-identity]
                       [--registry-password]
                       [--registry-server]
                       [--registry-username]
                       [--repo]
                       [--revision-suffix]
                       [--revisions-mode {labels, multiple, single}]
                       [--runtime {generic, java}]
                       [--scale-rule-auth --sra]
                       [--scale-rule-http-concurrency --scale-rule-tcp-concurrency --srhc --srtc]
                       [--scale-rule-identity --sri]
                       [--scale-rule-metadata --srm]
                       [--scale-rule-name --srn]
                       [--scale-rule-type --srt]
                       [--secret-volume-mount]
                       [--secrets]
                       [--service-principal-client-id --sp-cid]
                       [--service-principal-client-secret --sp-sec]
                       [--service-principal-tenant-id --sp-tid]
                       [--source]
                       [--system-assigned]
                       [--tags]
                       [--target-label]
                       [--target-port]
                       [--termination-grace-period --tgp]
                       [--token]
                       [--transport {auto, http, http2, tcp}]
                       [--user-assigned]
                       [--workload-profile-name]
                       [--yaml]
```
Examples
Create a container app and retrieve its fully qualified domain name.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image myregistry.azurecr.io/my-app:v1.0 --environment MyContainerappEnv \
    --ingress external --target-port 80 \
    --registry-server myregistry.azurecr.io --registry-username myregistry --registry-password $REGISTRY_PASSWORD \
    --query properties.configuration.ingress.fqdn
```
Create a container app with resource requirements and replica count limits.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image nginx --environment MyContainerappEnv \
    --cpu 0.5 --memory 1.0Gi \
    --min-replicas 4 --max-replicas 8
```
Create a container app with secrets and environment variables.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-app:v1.0 --environment MyContainerappEnv \
    --secrets mysecret=secretvalue1 anothersecret="secret value 2" \
    --env-vars GREETING="Hello, world" SECRETENV=secretref:anothersecret
```
Create a container app using a YAML configuration. Example YAML configuration - https://aka.ms/azure-container-apps-yaml
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --environment MyContainerappEnv \
    --yaml "path/to/yaml/file.yml"
```
Create a container app with an http scale rule
```
az containerapp create -n myapp -g mygroup --environment myenv --image nginx \
    --scale-rule-name my-http-rule \
    --scale-rule-http-concurrency 50
```
Create a container app with a custom scale rule
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-queue-processor --environment MyContainerappEnv \
    --min-replicas 4 --max-replicas 8 \
    --scale-rule-name queue-based-autoscaling \
    --scale-rule-type azure-queue \
    --scale-rule-metadata "accountName=mystorageaccountname" \
                          "cloud=AzurePublicCloud" \
                          "queueLength=5" "queueName=foo" \
    --scale-rule-auth "connection=my-connection-string-secret-name"
```
Create a container app with a custom scale rule using identity to authenticate
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-queue-processor --environment MyContainerappEnv \
    --user-assigned myUserIdentityResourceId --min-replicas 4 --max-replicas 8 \
    --scale-rule-name queue-based-autoscaling \
    --scale-rule-type azure-queue \
    --scale-rule-metadata "accountName=mystorageaccountname" \
                          "cloud=AzurePublicCloud" \
                          "queueLength=5" "queueName=foo" \
    --scale-rule-identity myUserIdentityResourceId
```
Create a container app with secrets and mounts them in a volume.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-app:v1.0 --environment MyContainerappEnv \
    --secrets mysecret=secretvalue1 anothersecret="secret value 2" \
    --secret-volume-mount "mnt/secrets"
```
Create a container app hosted on a Connected Environment.
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-app:v1.0 --environment MyContainerappConnectedEnv \
    --environment-type connected
```
Create a container app from a new GitHub Actions workflow in the provided GitHub repository
```
az containerapp create -n my-containerapp -g MyResourceGroup \
--environment MyContainerappEnv --registry-server MyRegistryServer \
--registry-user MyRegistryUser --registry-pass MyRegistryPass \
--repo https://github.com/myAccount/myRepo
```
Create a Container App from the provided application source
```
az containerapp create -n my-containerapp -g MyResourceGroup \
--environment MyContainerappEnv --registry-server MyRegistryServer \
--registry-user MyRegistryUser --registry-pass MyRegistryPass \
--source .
```
Create a container app with java metrics enabled
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-app:v1.0 --environment MyContainerappEnv \
    --enable-java-metrics
```
Create a container app with java agent enabled
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-app:v1.0 --environment MyContainerappEnv \
    --enable-java-agent
```
Create an Azure Functions on Container Apps (kind=functionapp)
```
az containerapp create -n my-containerapp -g MyResourceGroup \
    --image my-app:v1.0 --environment MyContainerappEnv \
    --kind functionapp
```
Required Parameters
--name -n
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
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
--allow-insecure
Allow insecure connections for ingress traffic.
Property
Value
Default value:
False
Accepted values:
false, true
--args
A list of container startup command argument(s). Space-separated values e.g. "-c" "mycommand". Empty string to clear existing values.
Property
Value
Parameter group:
Container Arguments
--artifact
Preview
Local path to the application artifact for building the container image. See the supported artifacts here:
https://aka.ms/SourceToCloudSupportedArtifacts
.
--bind
Preview
Space separated list of services, bindings or Java components to be connected to this app. e.g. SVC_NAME1[:BIND_NAME1] SVC_NAME2[:BIND_NAME2]...
Property
Value
Parameter group:
Service Binding Arguments
--branch -b
Preview
Branch in the provided GitHub repository. Assumed to be the GitHub repository's default branch if not specified.
Property
Value
Parameter group:
GitHub Repository Arguments
--build-env-vars
Preview
A list of environment variable(s) for the build. Space-separated values in 'key=value' format.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--command
A list of supported commands on the container that will executed during startup. Space-separated values e.g. "/bin/queue" "mycommand". Empty string to clear existing values.
Property
Value
Parameter group:
Container Arguments
--container-name
Name of the container.
Property
Value
Parameter group:
Container Arguments
--context-path
Preview
Path in the repository to run docker build. Defaults to "./". Dockerfile is assumed to be named "Dockerfile" and in this directory.
Property
Value
Parameter group:
GitHub Repository Arguments
--cpu
Required CPU in cores from 0.25 - 2.0, e.g. 0.5.
Property
Value
Parameter group:
Container Arguments
--customized-keys
Preview
The customized keys used to change default configuration names. Key is the original name, value is the customized name.
Property
Value
Parameter group:
Service Binding Arguments
--dal --dapr-enable-api-logging
Enable API logging for the Dapr sidecar.
Property
Value
Parameter group:
Dapr Arguments
Default value:
False
--dapr-app-id
The Dapr application identifier.
Property
Value
Parameter group:
Dapr Arguments
--dapr-app-port
The port Dapr uses to talk to the application.
Property
Value
Parameter group:
Dapr Arguments
--dapr-app-protocol
The protocol Dapr uses to talk to the application.
Property
Value
Parameter group:
Dapr Arguments
Accepted values:
grpc, http
--dapr-http-max-request-size --dhmrs
Increase max size of request body http and grpc servers parameter in MB to handle uploading of big files.
Property
Value
Parameter group:
Dapr Arguments
--dapr-http-read-buffer-size --dhrbs
Dapr max size of http header read buffer in KB to handle when sending multi-KB headers..
Property
Value
Parameter group:
Dapr Arguments
--dapr-log-level
Set the log level for the Dapr sidecar.
Property
Value
Parameter group:
Dapr Arguments
Accepted values:
debug, error, info, warn
--enable-dapr
Boolean indicating if the Dapr side car is enabled.
Property
Value
Parameter group:
Dapr Arguments
Default value:
False
Accepted values:
false, true
--enable-java-agent
Boolean indicating whether to enable Java agent for the app. Only applicable for Java runtime.
Property
Value
Parameter group:
Runtime Arguments
Accepted values:
false, true
--enable-java-metrics
Boolean indicating whether to enable Java metrics for the app. Only applicable for Java runtime.
Property
Value
Parameter group:
Runtime Arguments
Accepted values:
false, true
--env-vars
A list of environment variable(s) for the container. Space-separated values in 'key=value' format. Empty string to clear existing values. Prefix value with 'secretref:' to reference a secret.
Property
Value
Parameter group:
Container Arguments
--environment
Name or resource ID of the container app's environment.
--environment-type
Preview
Type of environment.
Property
Value
Default value:
managed
Accepted values:
connected, managed
--exposed-port
Additional exposed port. Only supported by tcp transport protocol. Must be unique per environment if the app ingress is external.
Property
Value
Parameter group:
Ingress Arguments
--image -i
Container image, e.g. publisher/image-name:tag.
Property
Value
Parameter group:
Container Arguments
--ingress
The ingress type.
Property
Value
Parameter group:
Ingress Arguments
Accepted values:
external, internal
--kind
Preview
Set to 'functionapp' to enable built-in support and autoscaling for Azure Functions on Container Apps.
Property
Value
Accepted values:
functionapp
--max-inactive-revisions
Preview
Max inactive revisions a Container App can have.
--max-replicas
The maximum number of replicas.
Property
Value
Parameter group:
Scale Arguments
--memory
Required memory from 0.5 - 4.0 ending with "Gi", e.g. 1.0Gi.
Property
Value
Parameter group:
Container Arguments
--min-replicas
The minimum number of replicas.
Property
Value
Parameter group:
Scale Arguments
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--registry-identity
The managed identity with which to authenticate to the Azure Container Registry (instead of username/password). Use 'system' for a system-defined identity, Use 'system-environment' for an environment level system-defined identity or a resource id for a user-defined environment/containerapp level identity. The managed identity should have been assigned acrpull permissions on the ACR before deployment (use 'az role assignment create --role acrpull ...').
Property
Value
Parameter group:
Configuration Arguments
--registry-password
The password to log in to container registry. If stored as a secret, value must start with 'secretref:' followed by the secret name.
Property
Value
Parameter group:
Configuration Arguments
--registry-server
The container registry server hostname, e.g. myregistry.azurecr.io.
Property
Value
Parameter group:
Configuration Arguments
--registry-username
The username to log in to container registry.
Property
Value
Parameter group:
Configuration Arguments
--repo
Preview
Create an app via GitHub Actions in the format:
https://github.com/owner/repository-name
or owner/repository-name.
Property
Value
Parameter group:
GitHub Repository Arguments
--revision-suffix
User friendly suffix that is appended to the revision name.
Property
Value
Parameter group:
Container Arguments
--revisions-mode
The active revisions mode for the container app.
Property
Value
Parameter group:
Configuration Arguments
Default value:
single
Accepted values:
labels, multiple, single
--runtime
The runtime of the container app.
Property
Value
Parameter group:
Runtime Arguments
Accepted values:
generic, java
--scale-rule-auth --sra
Scale rule auth parameters. Auth parameters must be in format "{triggerParameter}={secretRef} {triggerParameter}={secretRef} ...".
Property
Value
Parameter group:
Scale Arguments
--scale-rule-http-concurrency --scale-rule-tcp-concurrency --srhc --srtc
The maximum number of concurrent requests before scale out. Only supported for http and tcp scale rules.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-identity --sri
Preview
Resource ID of a managed identity to authenticate with Azure scaler resource(storage account/eventhub or else), or System to use a system-assigned identity.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-metadata --srm
Scale rule metadata. Metadata must be in format "{key}={value} {key}={value} ...".
Property
Value
Parameter group:
Scale Arguments
--scale-rule-name --srn
The name of the scale rule.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-type --srt
The type of the scale rule. Default: http. For more information please visit
https://learn.microsoft.com/azure/container-apps/scale-app#scale-triggers
.
Property
Value
Parameter group:
Scale Arguments
--secret-volume-mount
Path to mount all secrets e.g. mnt/secrets.
--secrets -s
A list of secret(s) for the container app. Space-separated values in 'key=value' format.
Property
Value
Parameter group:
Configuration Arguments
--service-principal-client-id --sp-cid
Preview
The service principal client ID. Used by GitHub Actions to authenticate with Azure.
Property
Value
Parameter group:
GitHub Repository Arguments
--service-principal-client-secret --sp-sec
Preview
The service principal client secret. Used by GitHub Actions to authenticate with Azure.
Property
Value
Parameter group:
GitHub Repository Arguments
--service-principal-tenant-id --sp-tid
Preview
The service principal tenant ID. Used by GitHub Actions to authenticate with Azure.
Property
Value
Parameter group:
GitHub Repository Arguments
--source
Preview
Local directory path containing the application source and Dockerfile for building the container image. Preview: If no Dockerfile is present, a container image is generated using buildpacks. If Docker is not running or buildpacks cannot be used, Oryx will be used to generate the image. See the supported Oryx runtimes here:
https://aka.ms/SourceToCloudSupportedVersions
.
--system-assigned
Boolean indicating whether to assign system-assigned identity.
Property
Value
Parameter group:
Identity Arguments
Default value:
False
--tags
Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags.
--target-label
Preview
The label to apply to new revisions. Required for revisions-mode 'labels'.
--target-port
The application port used for ingress traffic.
Property
Value
Parameter group:
Ingress Arguments
--termination-grace-period --tgp
Duration in seconds a replica is given to gracefully shut down before it is forcefully terminated. (Default: 30).
--token
Preview
A Personal Access Token with write access to the specified repository. For more information:
https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
. If not provided or not found in the cache (and using --repo), a browser page will be opened to authenticate with Github.
Property
Value
Parameter group:
GitHub Repository Arguments
--transport
The transport protocol used for ingress traffic.
Property
Value
Parameter group:
Ingress Arguments
Default value:
auto
Accepted values:
auto, http, http2, tcp
--user-assigned
Space-separated user identities to be assigned.
Property
Value
Parameter group:
Identity Arguments
--workload-profile-name -w
Name of the workload profile to run the app on.
--yaml
Path to a .yaml file with the configuration of a container app. All other parameters will be ignored. For an example, see
https://learn.microsoft.com/azure/container-apps/azure-resource-manager-api-spec#examples
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
az containerapp debug
Preview
Open an SSH-like interactive shell within a container app debug console or execute a command inside the container and exit.
```
az containerapp debug --name
                      --resource-group
                      [--acquire-policy-token]
                      [--change-reference]
                      [--command]
                      [--container]
                      [--replica]
                      [--revision]
```
Examples
Debug by connecting to a container app's debug console by replica, revision and container
```
az containerapp debug -n MyContainerapp -g MyResourceGroup --revision MyRevision --replica MyReplica --container MyContainer
```
Debug by executing a command inside a container app and exit
```
az containerapp debug -n MyContainerapp -g MyResourceGroup --revision MyRevision --replica MyReplica --container MyContainer --command "echo Hello World"
```
Required Parameters
--name -n
The name of the Containerapp.
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
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--command
The command to run inside the debug container and exit. If specified, the command is run and the session ends. If not specified, an interactive bash shell is started.
--container
The container name that the debug console will connect to. Default to the first container of first replica.
--replica
The name of the replica. List replicas with 'az containerapp replica list'. A replica may be not found when it's scaled to zero if there is no traffic to your app. Default to the first replica of 'az containerapp replica list'.
--revision
The name of the container app revision. Default to the latest revision.
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
az containerapp delete
Edit
Delete a container app.
```
az containerapp delete [--acquire-policy-token]
                       [--change-reference]
                       [--ids]
                       [--name]
                       [--no-wait]
                       [--resource-group]
                       [--subscription]
                       [--yes]
```
Examples
Delete a container app.
```
az containerapp delete -g MyResourceGroup -n MyContainerapp
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
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
Property
Value
Parameter group:
Resource Id Arguments
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
--yes -y
Do not prompt for confirmation.
Property
Value
Default value:
False
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
az containerapp delete (containerapp extension)
Delete a container app.
```
az containerapp delete [--acquire-policy-token]
                       [--change-reference]
                       [--ids]
                       [--name]
                       [--no-wait]
                       [--resource-group]
                       [--subscription]
                       [--yes]
```
Examples
Delete a container app.
```
az containerapp delete -g MyResourceGroup -n MyContainerapp
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
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
Property
Value
Parameter group:
Resource Id Arguments
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
--yes -y
Do not prompt for confirmation.
Property
Value
Default value:
False
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
az containerapp exec
Edit
Open an SSH-like interactive shell within a container app replica.
```
az containerapp exec --name
                     --resource-group
                     [--acquire-policy-token]
                     [--change-reference]
                     [--command]
                     [--container]
                     [--replica]
                     [--revision]
```
Examples
exec into a container app
```
az containerapp exec -n my-containerapp -g MyResourceGroup
```
exec into a particular container app replica and revision
```
az containerapp exec -n my-containerapp -g MyResourceGroup --replica MyReplica --revision MyRevision
```
open a bash shell in a containerapp
```
az containerapp exec -n my-containerapp -g MyResourceGroup --command bash
```
Required Parameters
--name -n
The name of the Containerapp.
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
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--command
The startup command (bash, zsh, sh, etc.).
Property
Value
Parameter group:
Container Arguments
Default value:
sh
--container
The name of the container to ssh into.
--replica
The name of the replica to ssh into. List replicas with 'az containerapp replica list'. A replica may not exist if there is not traffic to your app.
--revision
The name of the container app revision to ssh into. Defaults to the latest revision.
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
az containerapp list
Edit
List container apps.
```
az containerapp list [--environment]
                     [--resource-group]
```
Examples
List container apps in the current subscription.
```
az containerapp list
```
List container apps by resource group.
```
az containerapp list -g MyResourceGroup
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--environment
Name or resource ID of the container app's environment.
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
az containerapp list (containerapp extension)
List container apps.
```
az containerapp list [--environment]
                     [--environment-type {connected, managed}]
                     [--kind {functionapp, logicapp}]
                     [--resource-group]
```
Examples
List container apps in the current subscription.
```
az containerapp list
```
List container apps by resource group.
```
az containerapp list -g MyResourceGroup
```
List container apps by environment type.
```
az containerapp list --environment-type connected
```
List Azure Functions on Container Apps only.
```
az containerapp list --kind functionapp
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--environment
Name or resource ID of the container app's environment.
--environment-type
Preview
Type of environment.
Property
Value
Default value:
all
Accepted values:
connected, managed
--kind
Preview
Filter by kind. Use 'functionapp' to list only Azure Functions on Container Apps.
Property
Value
Accepted values:
functionapp, logicapp
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
az containerapp list-usages
Edit
List usages of subscription level quotas in specific region.
```
az containerapp list-usages --location
                            [--acquire-policy-token]
                            [--change-reference]
```
Examples
List usages of  quotas in specific region.
```
az containerapp list-usages -l eastus
```
Required Parameters
--location -l
Location. Values from:
az account list-locations
. You can configure the default location using
az configure --defaults location=<location>
.
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
az containerapp show
Edit
Show details of a container app.
```
az containerapp show [--ids]
                     [--name]
                     [--resource-group]
                     [--show-secrets]
                     [--subscription]
```
Examples
Show the details of a container app.
```
az containerapp show -n my-containerapp -g MyResourceGroup
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
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
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
--show-secrets
Show Containerapp secrets.
Property
Value
Default value:
False
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
az containerapp show (containerapp extension)
Show details of a container app.
```
az containerapp show [--ids]
                     [--name]
                     [--resource-group]
                     [--show-secrets]
                     [--subscription]
```
Examples
Show the details of a container app.
```
az containerapp show -n my-containerapp -g MyResourceGroup
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
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
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
--show-secrets
Show Containerapp secrets.
Property
Value
Default value:
False
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
az containerapp show-custom-domain-verification-id
Edit
Show the verification id for binding app or environment custom domains.
```
az containerapp show-custom-domain-verification-id [--acquire-policy-token]
                                                   [--change-reference]
```
Examples
Get the verification id, which needs to be added as a TXT record for app custom domain to verify domain ownership
```
az containerapp show-custom-domain-verification-id
```
Get the verification id, which needs to be added as a TXT record for custom environment DNS suffix to verify domain ownership
```
az containerapp show-custom-domain-verification-id
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
az containerapp up
Edit
Create or update a container app as well as any associated resources (ACR, resource group, container apps environment, GitHub Actions, etc.).
```
az containerapp up --name
                   [--acquire-policy-token]
                   [--branch]
                   [--browse]
                   [--change-reference]
                   [--context-path]
                   [--env-vars]
                   [--environment]
                   [--image]
                   [--ingress {external, internal}]
                   [--location]
                   [--logs-workspace-id]
                   [--logs-workspace-key]
                   [--registry-password]
                   [--registry-server]
                   [--registry-username]
                   [--repo]
                   [--resource-group]
                   [--service-principal-client-id --sp-cid]
                   [--service-principal-client-secret --sp-sec]
                   [--service-principal-tenant-id --sp-tid]
                   [--source]
                   [--target-port]
                   [--token]
                   [--workload-profile-name]
```
Examples
Create a container app from a dockerfile in a GitHub repo (setting up github actions)
```
az containerapp up -n my-containerapp --repo https://github.com/myAccount/myRepo
```
Create a container app from a dockerfile in a local directory (or autogenerate a container if no dockerfile is found)
```
az containerapp up -n my-containerapp --source .
```
Create a container app from an image in a registry
```
az containerapp up -n my-containerapp --image myregistry.azurecr.io/myImage:myTag
```
Create a container app from an image in a registry with ingress enabled and a specified environment
```
az containerapp up -n my-containerapp --image myregistry.azurecr.io/myImage:myTag --ingress external --target-port 80 --environment MyEnv
```
Required Parameters
--name -n
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--branch -b
The branch of the Github repo. Assumed to be the Github repo's default branch if not specified.
Property
Value
Parameter group:
Github Repo Arguments
--browse
Open the app in a web browser after creation and deployment, if possible.
Property
Value
Default value:
False
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--context-path
Path in the repo from which to run the docker build. Defaults to "./". Dockerfile is assumed to be named "Dockerfile" and in this directory.
Property
Value
Parameter group:
Github Repo Arguments
--env-vars
A list of environment variable(s) for the container. Space-separated values in 'key=value' format. Empty string to clear existing values. Prefix value with 'secretref:' to reference a secret.
Property
Value
Parameter group:
Container Arguments
--environment
Name or resource ID of the container app's environment.
--image -i
Container image, e.g. publisher/image-name:tag.
--ingress
The ingress type.
Property
Value
Parameter group:
Ingress Arguments
Accepted values:
external, internal
--location -l
Location. Values from:
az account list-locations
. You can configure the default location using
az configure --defaults location=<location>
.
--logs-workspace-id
Workspace ID of the Log Analytics workspace to send diagnostics logs to. You can use "az monitor log-analytics workspace create" to create one. Extra billing may apply.
Property
Value
Parameter group:
Log Analytics (Environment) Arguments
--logs-workspace-key
Log Analytics workspace key to configure your Log Analytics workspace. You can use "az monitor log-analytics workspace get-shared-keys" to retrieve the key.
Property
Value
Parameter group:
Log Analytics (Environment) Arguments
--registry-password
The password to log in to container registry. If stored as a secret, value must start with 'secretref:' followed by the secret name.
Property
Value
Parameter group:
Configuration Arguments
--registry-server
The container registry server hostname, e.g. myregistry.azurecr.io.
Property
Value
Parameter group:
Configuration Arguments
--registry-username
The username to log in to container registry.
Property
Value
Parameter group:
Configuration Arguments
--repo
Create an app via Github Actions. In the format:
https://github.com/<owner>/<repository-name>
or
<owner>/<repository-name>
.
Property
Value
Parameter group:
Github Repo Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
--service-principal-client-id --sp-cid
The service principal client ID. Used by Github Actions to authenticate with Azure.
Property
Value
Parameter group:
Github Repo Arguments
--service-principal-client-secret --sp-sec
The service principal client secret. Used by Github Actions to authenticate with Azure.
Property
Value
Parameter group:
Github Repo Arguments
--service-principal-tenant-id --sp-tid
The service principal tenant ID. Used by Github Actions to authenticate with Azure.
Property
Value
Parameter group:
Github Repo Arguments
--source
Local directory path containing the application source and Dockerfile for building the container image. Preview: If no Dockerfile is present, a container image is generated using buildpacks. If Docker is not running or buildpacks cannot be used, Oryx will be used to generate the image. See the supported Oryx runtimes here:
https://github.com/microsoft/Oryx/blob/main/doc/supportedRuntimeVersions.md
.
--target-port
The application port used for ingress traffic.
Property
Value
Parameter group:
Ingress Arguments
--token
A Personal Access Token with write access to the specified repository. For more information:
https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
. If not provided or not found in the cache (and using --repo), a browser page will be opened to authenticate with Github.
Property
Value
Parameter group:
Github Repo Arguments
--workload-profile-name -w
The friendly name for the workload profile.
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
az containerapp up (containerapp extension)
Create or update a container app as well as any associated resources (ACR, resource group, container apps environment, GitHub Actions, etc.).
```
az containerapp up --name
                   [--acquire-policy-token]
                   [--artifact]
                   [--branch]
                   [--browse]
                   [--build-env-vars]
                   [--change-reference]
                   [--connected-cluster-id]
                   [--context-path]
                   [--custom-location]
                   [--env-vars]
                   [--environment]
                   [--image]
                   [--ingress {external, internal}]
                   [--kind {functionapp}]
                   [--location]
                   [--logs-workspace-id]
                   [--logs-workspace-key]
                   [--model-name]
                   [--model-registry]
                   [--model-version]
                   [--registry-identity]
                   [--registry-password]
                   [--registry-server]
                   [--registry-username]
                   [--repo]
                   [--resource-group]
                   [--revisions-mode {labels, multiple, single}]
                   [--service-principal-client-id --sp-cid]
                   [--service-principal-client-secret --sp-sec]
                   [--service-principal-tenant-id --sp-tid]
                   [--source]
                   [--system-assigned]
                   [--target-label]
                   [--target-port]
                   [--token]
                   [--user-assigned]
                   [--workload-profile-name]
```
Examples
Create a container app from a dockerfile in a GitHub repo (setting up github actions)
```
az containerapp up -n my-containerapp --repo https://github.com/myAccount/myRepo
```
Create a container app from a dockerfile in a local directory (or autogenerate a container if no dockerfile is found)
```
az containerapp up -n my-containerapp --source .
```
Create a container app from an image in a registry
```
az containerapp up -n my-containerapp --image myregistry.azurecr.io/myImage:myTag
```
Create a container app from an image in a registry with ingress enabled and a specified environment
```
az containerapp up -n my-containerapp --image myregistry.azurecr.io/myImage:myTag --ingress external --target-port 80 --environment MyEnv
```
Create a container app from an image in a registry on a Connected cluster
```
az containerapp up -n my-containerapp --image myregistry.azurecr.io/myImage:myTag --connected-cluster-id MyConnectedClusterResourceId
```
Create a container app from an image in a registry on a connected environment
```
az containerapp up -n my-containerapp --image myregistry.azurecr.io/myImage:myTag --environment MyConnectedEnvironmentId
```
Create a container app and deploy a model from Azure AI Foundry
```
az containerapp up -n my-containerapp -l westus3 --model-registry azureml --model-name Phi-4 --model-version 7
```
Create an Azure Functions on Container Apps (kind=functionapp)
```
az containerapp up -n my-containerapp --image my-app:v1.0 --kind functionapp
```
Required Parameters
--name -n
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--artifact
Preview
Local path to the application artifact for building the container image. See the supported artifacts here:
https://aka.ms/SourceToCloudSupportedArtifacts
.
--branch -b
The branch of the Github repo. Assumed to be the Github repo's default branch if not specified.
Property
Value
Parameter group:
Github Repo Arguments
--browse
Open the app in a web browser after creation and deployment, if possible.
Property
Value
Default value:
False
--build-env-vars
Preview
A list of environment variable(s) for the build. Space-separated values in 'key=value' format.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--connected-cluster-id
Preview
Resource ID of connected cluster. List using 'az connectedk8s list'.
--context-path
Path in the repo from which to run the docker build. Defaults to "./". Dockerfile is assumed to be named "Dockerfile" and in this directory.
Property
Value
Parameter group:
Github Repo Arguments
--custom-location
Preview
Resource ID of custom location. List using 'az customlocation list'.
--env-vars
A list of environment variable(s) for the container. Space-separated values in 'key=value' format. Empty string to clear existing values. Prefix value with 'secretref:' to reference a secret.
Property
Value
Parameter group:
Container Arguments
--environment
Name or resource ID of the container app's managed environment or connected environment.
--image -i
Container image, e.g. publisher/image-name:tag.
--ingress
The ingress type.
Property
Value
Parameter group:
Ingress Arguments
Accepted values:
external, internal
--kind
Preview
Set to 'functionapp' to enable built-in support and autoscaling for Azure Functions on Container Apps.
Property
Value
Accepted values:
functionapp
--location -l
Location. Values from:
az account list-locations
. You can configure the default location using
az configure --defaults location=<location>
.
--logs-workspace-id
Workspace ID of the Log Analytics workspace to send diagnostics logs to. You can use "az monitor log-analytics workspace create" to create one. Extra billing may apply.
Property
Value
Parameter group:
Log Analytics (Environment) Arguments
--logs-workspace-key
Log Analytics workspace key to configure your Log Analytics workspace. You can use "az monitor log-analytics workspace get-shared-keys" to retrieve the key.
Property
Value
Parameter group:
Log Analytics (Environment) Arguments
--model-name
Preview
The name of the Azure AI Foundry model.
Property
Value
Parameter group:
Deploy an Azure AI Foundry Model Arguments
--model-registry
Preview
The name of the Azure AI Foundry model registry.
Property
Value
Parameter group:
Deploy an Azure AI Foundry Model Arguments
--model-version
Preview
The version of the Azure AI Foundry model.
Property
Value
Parameter group:
Deploy an Azure AI Foundry Model Arguments
--registry-identity
A Managed Identity to authenticate with the registry server instead of username/password. Use a resource ID or 'system' for user-defined and system-defined identities, respectively. The registry must be an ACR. If possible, an 'acrpull' role assignment will be created for the identity automatically.
Property
Value
Parameter group:
Configuration Arguments
--registry-password
The password to log in to container registry. If stored as a secret, value must start with 'secretref:' followed by the secret name.
Property
Value
Parameter group:
Configuration Arguments
--registry-server
The container registry server hostname, e.g. myregistry.azurecr.io.
Property
Value
Parameter group:
Configuration Arguments
--registry-username
The username to log in to container registry.
Property
Value
Parameter group:
Configuration Arguments
--repo
Create an app via Github Actions. In the format:
https://github.com/owner/repository-name
or owner/repository-name.
Property
Value
Parameter group:
Github Repo Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
--revisions-mode
The active revisions mode for the container app.
Property
Value
Parameter group:
Configuration Arguments
Accepted values:
labels, multiple, single
--service-principal-client-id --sp-cid
The service principal client ID. Used by Github Actions to authenticate with Azure.
Property
Value
Parameter group:
Github Repo Arguments
--service-principal-client-secret --sp-sec
The service principal client secret. Used by Github Actions to authenticate with Azure.
Property
Value
Parameter group:
Github Repo Arguments
--service-principal-tenant-id --sp-tid
The service principal tenant ID. Used by Github Actions to authenticate with Azure.
Property
Value
Parameter group:
Github Repo Arguments
--source
Local directory path containing the application source and Dockerfile for building the container image. Preview: If no Dockerfile is present, a container image is generated using buildpacks. If Docker is not running or buildpacks cannot be used, Oryx will be used to generate the image. See the supported Oryx runtimes here:
https://github.com/microsoft/Oryx/blob/main/doc/supportedRuntimeVersions.md
.
--system-assigned
Boolean indicating whether to assign system-assigned identity.
Property
Value
Parameter group:
Identity Arguments
--target-label
Preview
The label to apply to new revisions. Required for revisions-mode 'labels'.
--target-port
The application port used for ingress traffic.
Property
Value
Parameter group:
Ingress Arguments
--token
A Personal Access Token with write access to the specified repository. For more information:
https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
. If not provided or not found in the cache (and using --repo), a browser page will be opened to authenticate with Github.
Property
Value
Parameter group:
Github Repo Arguments
--user-assigned
Space-separated user identities to be assigned.
Property
Value
Parameter group:
Identity Arguments
--workload-profile-name -w
The friendly name for the workload profile.
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
az containerapp update
Edit
Update a container app. In multiple revisions mode, create a new revision based on the latest revision.
```
az containerapp update [--acquire-policy-token]
                       [--args]
                       [--change-reference]
                       [--command]
                       [--container-name]
                       [--cpu]
                       [--ids]
                       [--image]
                       [--max-replicas]
                       [--memory]
                       [--min-replicas]
                       [--name]
                       [--no-wait]
                       [--remove-all-env-vars]
                       [--remove-env-vars]
                       [--replace-env-vars]
                       [--resource-group]
                       [--revision-suffix]
                       [--scale-rule-auth --sra]
                       [--scale-rule-http-concurrency --scale-rule-tcp-concurrency --srhc --srtc]
                       [--scale-rule-metadata --srm]
                       [--scale-rule-name --srn]
                       [--scale-rule-type --srt]
                       [--secret-volume-mount]
                       [--set-env-vars]
                       [--subscription]
                       [--tags]
                       [--termination-grace-period --tgp]
                       [--workload-profile-name]
                       [--yaml]
```
Examples
Update a container app's container image.
```
az containerapp update -n my-containerapp -g MyResourceGroup \
    --image myregistry.azurecr.io/my-app:v2.0
```
Update a container app's resource requirements and scale limits.
```
az containerapp update -n my-containerapp -g MyResourceGroup \
    --cpu 0.5 --memory 1.0Gi \
    --min-replicas 4 --max-replicas 8
```
Update a container app with an http scale rule
```
az containerapp update -n myapp -g mygroup \
    --scale-rule-name my-http-rule \
    --scale-rule-http-concurrency 50
```
Update a container app with a custom scale rule
```
az containerapp update -n myapp -g mygroup \
    --scale-rule-name my-custom-rule \
    --scale-rule-type my-custom-type \
    --scale-rule-metadata key=value key2=value2 \
    --scale-rule-auth triggerparam=secretref triggerparam=secretref
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--args
A list of container startup command argument(s). Space-separated values e.g. "-c" "mycommand". Empty string to clear existing values.
Property
Value
Parameter group:
Container Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--command
A list of supported commands on the container that will executed during startup. Space-separated values e.g. "/bin/queue" "mycommand". Empty string to clear existing values.
Property
Value
Parameter group:
Container Arguments
--container-name
Name of the container.
Property
Value
Parameter group:
Container Arguments
--cpu
Required CPU in cores from 0.25 - 2.0, e.g. 0.5.
Property
Value
Parameter group:
Container Arguments
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--image -i
Container image, e.g. publisher/image-name:tag.
Property
Value
Parameter group:
Container Arguments
--max-replicas
The maximum number of replicas.
Property
Value
Parameter group:
Scale Arguments
--memory
Required memory from 0.5 - 4.0 ending with "Gi", e.g. 1.0Gi.
Property
Value
Parameter group:
Container Arguments
--min-replicas
The minimum number of replicas.
Property
Value
Parameter group:
Scale Arguments
--name -n
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
Property
Value
Parameter group:
Resource Id Arguments
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--remove-all-env-vars
Remove all environment variable(s) from container..
Property
Value
Parameter group:
Environment variables Arguments
Default value:
False
--remove-env-vars
Remove environment variable(s) from container. Space-separated environment variable names.
Property
Value
Parameter group:
Environment variables Arguments
--replace-env-vars
Replace environment variable(s) in container. Other existing environment variables are removed. Space-separated values in 'key=value' format. If stored as a secret, value must start with 'secretref:' followed by the secret name.
Property
Value
Parameter group:
Environment variables Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--revision-suffix
User friendly suffix that is appended to the revision name.
Property
Value
Parameter group:
Container Arguments
--scale-rule-auth --sra
Scale rule auth parameters. Auth parameters must be in format "{triggerParameter}={secretRef} {triggerParameter}={secretRef} ...".
Property
Value
Parameter group:
Scale Arguments
--scale-rule-http-concurrency --scale-rule-tcp-concurrency --srhc --srtc
The maximum number of concurrent requests before scale out. Only supported for http and tcp scale rules.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-metadata --srm
Scale rule metadata. Metadata must be in format "{key}={value} {key}={value} ...".
Property
Value
Parameter group:
Scale Arguments
--scale-rule-name --srn
The name of the scale rule.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-type --srt
The type of the scale rule. Default: http. For more information please visit
https://learn.microsoft.com/azure/container-apps/scale-app#scale-triggers
.
Property
Value
Parameter group:
Scale Arguments
--secret-volume-mount
Path to mount all secrets e.g. mnt/secrets.
Property
Value
Parameter group:
Container Arguments
--set-env-vars
Add or update environment variable(s) in container. Existing environment variables are not modified. Space-separated values in 'key=value' format. If stored as a secret, value must start with 'secretref:' followed by the secret name.
Property
Value
Parameter group:
Environment variables Arguments
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
--tags
Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags.
--termination-grace-period --tgp
Duration in seconds a replica is given to gracefully shut down before it is forcefully terminated. (Default: 30).
Property
Value
Parameter group:
Container Arguments
--workload-profile-name -w
The friendly name for the workload profile.
Property
Value
Parameter group:
Container Arguments
--yaml
Path to a .yaml file with the configuration of a container app. All other parameters will be ignored. For an example, see
https://learn.microsoft.com/azure/container-apps/azure-resource-manager-api-spec#examples
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
--verbose
Increase logging verbosity. Use --debug for full debug logs.
Property
Value
Default value:
False
az containerapp update (containerapp extension)
Update a container app. In multiple revisions mode, create a new revision based on the latest revision.
```
az containerapp update [--acquire-policy-token]
                       [--args]
                       [--artifact]
                       [--bind]
                       [--build-env-vars]
                       [--change-reference]
                       [--command]
                       [--container-name]
                       [--cpu]
                       [--customized-keys]
                       [--enable-java-agent {false, true}]
                       [--enable-java-metrics {false, true}]
                       [--ids]
                       [--image]
                       [--max-inactive-revisions]
                       [--max-replicas]
                       [--memory]
                       [--min-replicas]
                       [--name]
                       [--no-wait]
                       [--remove-all-env-vars]
                       [--remove-env-vars]
                       [--replace-env-vars]
                       [--resource-group]
                       [--revision-suffix]
                       [--revisions-mode {labels, multiple, single}]
                       [--runtime {generic, java}]
                       [--scale-rule-auth --sra]
                       [--scale-rule-http-concurrency --scale-rule-tcp-concurrency --srhc --srtc]
                       [--scale-rule-identity --sri]
                       [--scale-rule-metadata --srm]
                       [--scale-rule-name --srn]
                       [--scale-rule-type --srt]
                       [--secret-volume-mount]
                       [--set-env-vars]
                       [--source]
                       [--subscription]
                       [--tags]
                       [--target-label]
                       [--termination-grace-period --tgp]
                       [--unbind]
                       [--workload-profile-name]
                       [--yaml]
```
Examples
Update a container app's container image.
```
az containerapp update -n my-containerapp -g MyResourceGroup \
    --image myregistry.azurecr.io/my-app:v2.0
```
Update a container app's resource requirements and scale limits.
```
az containerapp update -n my-containerapp -g MyResourceGroup \
    --cpu 0.5 --memory 1.0Gi \
    --min-replicas 4 --max-replicas 8
```
Update a container app with an http scale rule
```
az containerapp update -n myapp -g mygroup \
    --scale-rule-name my-http-rule \
    --scale-rule-http-concurrency 50
```
Update a container app with a custom scale rule
```
az containerapp update -n myapp -g mygroup \
    --scale-rule-name my-custom-rule \
    --scale-rule-type my-custom-type \
    --scale-rule-metadata key=value key2=value2 \
    --scale-rule-auth triggerparam=secretref triggerparam=secretref
```
Update a Container App from the provided application source
```
az containerapp update -n my-containerapp -g MyResourceGroup --source .
```
Update a container app with java metrics enabled
```
az containerapp update -n my-containerapp -g MyResourceGroup \
    --enable-java-metrics
```
Update a container app with java agent enabled
```
az containerapp update -n my-containerapp -g MyResourceGroup \
    --enable-java-agent
```
Update a container app to erase java enhancement capabilities, like java metrics, java agent, etc.
```
az containerapp update -n my-containerapp -g MyResourceGroup \
    --runtime generic
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--args
A list of container startup command argument(s). Space-separated values e.g. "-c" "mycommand". Empty string to clear existing values.
Property
Value
Parameter group:
Container Arguments
--artifact
Preview
Local path to the application artifact for building the container image. See the supported artifacts here:
https://aka.ms/SourceToCloudSupportedArtifacts
.
--bind
Preview
Space separated list of services, bindings or Java components to be connected to this app. e.g. SVC_NAME1[:BIND_NAME1] SVC_NAME2[:BIND_NAME2]...
Property
Value
Parameter group:
Service Binding Arguments
--build-env-vars
Preview
A list of environment variable(s) for the build. Space-separated values in 'key=value' format.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--command
A list of supported commands on the container that will executed during startup. Space-separated values e.g. "/bin/queue" "mycommand". Empty string to clear existing values.
Property
Value
Parameter group:
Container Arguments
--container-name
Name of the container.
Property
Value
Parameter group:
Container Arguments
--cpu
Required CPU in cores from 0.25 - 2.0, e.g. 0.5.
Property
Value
Parameter group:
Container Arguments
--customized-keys
Preview
The customized keys used to change default configuration names. Key is the original name, value is the customized name.
Property
Value
Parameter group:
Service Binding Arguments
--enable-java-agent
Boolean indicating whether to enable Java agent for the app. Only applicable for Java runtime.
Property
Value
Parameter group:
Runtime Arguments
Accepted values:
false, true
--enable-java-metrics
Boolean indicating whether to enable Java metrics for the app. Only applicable for Java runtime.
Property
Value
Parameter group:
Runtime Arguments
Accepted values:
false, true
--ids
One or more resource IDs (space-delimited). It should be a complete resource ID containing all information of 'Resource Id' arguments. You should provide either --ids or other 'Resource Id' arguments.
Property
Value
Parameter group:
Resource Id Arguments
--image -i
Container image, e.g. publisher/image-name:tag.
Property
Value
Parameter group:
Container Arguments
--max-inactive-revisions
Preview
Max inactive revisions a Container App can have.
--max-replicas
The maximum number of replicas.
Property
Value
Parameter group:
Scale Arguments
--memory
Required memory from 0.5 - 4.0 ending with "Gi", e.g. 1.0Gi.
Property
Value
Parameter group:
Container Arguments
--min-replicas
The minimum number of replicas.
Property
Value
Parameter group:
Scale Arguments
--name -n
The name of the Containerapp. A name must consist of lower case alphanumeric characters or '-', start with a letter, end with an alphanumeric character, cannot have '--', and must be less than 32 characters.
Property
Value
Parameter group:
Resource Id Arguments
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--remove-all-env-vars
Remove all environment variable(s) from container..
Property
Value
Parameter group:
Environment variables Arguments
Default value:
False
--remove-env-vars
Remove environment variable(s) from container. Space-separated environment variable names.
Property
Value
Parameter group:
Environment variables Arguments
--replace-env-vars
Replace environment variable(s) in container. Other existing environment variables are removed. Space-separated values in 'key=value' format. If stored as a secret, value must start with 'secretref:' followed by the secret name.
Property
Value
Parameter group:
Environment variables Arguments
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--revision-suffix
User friendly suffix that is appended to the revision name.
Property
Value
Parameter group:
Container Arguments
--revisions-mode
The active revisions mode for the container app.
Property
Value
Parameter group:
Configuration Arguments
Accepted values:
labels, multiple, single
--runtime
The runtime of the container app.
Property
Value
Parameter group:
Runtime Arguments
Accepted values:
generic, java
--scale-rule-auth --sra
Scale rule auth parameters. Auth parameters must be in format "{triggerParameter}={secretRef} {triggerParameter}={secretRef} ...".
Property
Value
Parameter group:
Scale Arguments
--scale-rule-http-concurrency --scale-rule-tcp-concurrency --srhc --srtc
The maximum number of concurrent requests before scale out. Only supported for http and tcp scale rules.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-identity --sri
Preview
Resource ID of a managed identity to authenticate with Azure scaler resource(storage account/eventhub or else), or System to use a system-assigned identity.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-metadata --srm
Scale rule metadata. Metadata must be in format "{key}={value} {key}={value} ...".
Property
Value
Parameter group:
Scale Arguments
--scale-rule-name --srn
The name of the scale rule.
Property
Value
Parameter group:
Scale Arguments
--scale-rule-type --srt
The type of the scale rule. Default: http. For more information please visit
https://learn.microsoft.com/azure/container-apps/scale-app#scale-triggers
.
Property
Value
Parameter group:
Scale Arguments
--secret-volume-mount
Path to mount all secrets e.g. mnt/secrets.
Property
Value
Parameter group:
Container Arguments
--set-env-vars
Add or update environment variable(s) in container. Existing environment variables are not modified. Space-separated values in 'key=value' format. If stored as a secret, value must start with 'secretref:' followed by the secret name.
Property
Value
Parameter group:
Environment variables Arguments
--source
Preview
Local directory path containing the application source and Dockerfile for building the container image. Preview: If no Dockerfile is present, a container image is generated using buildpacks. If Docker is not running or buildpacks cannot be used, Oryx will be used to generate the image. See the supported Oryx runtimes here:
https://aka.ms/SourceToCloudSupportedVersions
.
--subscription
Name or ID of subscription. You can configure the default subscription using
az account set -s NAME_OR_ID
.
Property
Value
Parameter group:
Resource Id Arguments
--tags
Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags.
--target-label
Preview
The label to apply to new revisions. Required for revisions-mode 'labels'.
--termination-grace-period --tgp
Duration in seconds a replica is given to gracefully shut down before it is forcefully terminated. (Default: 30).
Property
Value
Parameter group:
Container Arguments
--unbind
Preview
Space separated list of services, bindings or Java components to be removed from this app. e.g. BIND_NAME1...
Property
Value
Parameter group:
Service Binding Arguments
--workload-profile-name -w
The friendly name for the workload profile.
Property
Value
Parameter group:
Container Arguments
--yaml
Path to a .yaml file with the configuration of a container app. All other parameters will be ignored. For an example, see
https://learn.microsoft.com/azure/container-apps/azure-resource-manager-api-spec#examples
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