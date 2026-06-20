<!-- source: https://learn.microsoft.com/en-us/cli/azure/cosmosdb?view=azure-cli-latest -->

# az cosmosdb

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
az cosmosdb
Note
This command group has commands that are defined in both Azure CLI and at least one extension. Install each extension to benefit from its extended capabilities.
Learn more
about extensions.
Manage Azure Cosmos DB database accounts.
Commands
Name
Description
Type
Status
az cosmosdb cassandra
Manage Cassandra resources of Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb cassandra keyspace
Manage Azure Cosmos DB Cassandra keyspaces.
Core
GA
az cosmosdb cassandra keyspace create
Create an Cassandra keyspace under an Azure Cosmos DB account.
Core
GA
az cosmosdb cassandra keyspace delete
Delete the Cassandra keyspace under an Azure Cosmos DB account.
Core
GA
az cosmosdb cassandra keyspace exists
Checks if an Azure Cosmos DB Cassandra keyspace exists.
Core
GA
az cosmosdb cassandra keyspace list
List the Cassandra keyspaces under an Azure Cosmos DB account.
Core
GA
az cosmosdb cassandra keyspace show
Show the details of a Cassandra keyspace under an Azure Cosmos DB account.
Core
GA
az cosmosdb cassandra keyspace throughput
Manage throughput of Cassandra keyspace under an Azure Cosmos DB account.
Core
GA
az cosmosdb cassandra keyspace throughput migrate
Migrate the throughput of the Cassandra keyspace between autoscale and manually provisioned.
Core
GA
az cosmosdb cassandra keyspace throughput show
Get the throughput of the Cassandra keyspace under an Azure Cosmos DB account.
Core
GA
az cosmosdb cassandra keyspace throughput update
Update the throughput of the Cassandra keyspace under an Azure Cosmos DB account.
Core
GA
az cosmosdb cassandra role
Manage Azure Cosmos DB Cassandra role resources.
Extension
GA
az cosmosdb cassandra role assignment
Manage Azure Cosmos DB Cassandra role assignments.
Extension
GA
az cosmosdb cassandra role assignment create
Create a Cassandra role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role assignment delete
Delete a Cassandra role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role assignment exists
Check if an Azure Cosmos DB role assignment exists.
Extension
GA
az cosmosdb cassandra role assignment list
List all Cassandra role assignments under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role assignment show
Show the properties of a Cassandra role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role assignment update
Update a Cassandra role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role definition
Manage Azure Cosmos DB Cassandra role definitions.
Extension
GA
az cosmosdb cassandra role definition create
Create a Cassandra role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role definition delete
Delete a Cassandra role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role definition exists
Check if an Azure Cosmos DB role definition exists.
Extension
GA
az cosmosdb cassandra role definition list
List all Cassandra role definitions under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role definition show
Show the properties of a Cassandra role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra role definition update
Update a Cassandra role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb cassandra table
Manage Azure Cosmos DB Cassandra tables.
Core
GA
az cosmosdb cassandra table create
Create an Cassandra table under an Azure Cosmos DB Cassandra keyspace.
Core
GA
az cosmosdb cassandra table delete
Delete the Cassandra table under an Azure Cosmos DB Cassandra keyspace.
Core
GA
az cosmosdb cassandra table exists
Checks if an Azure Cosmos DB Cassandra table exists.
Core
GA
az cosmosdb cassandra table list
List the Cassandra tables under an Azure Cosmos DB Cassandra keyspace.
Core
GA
az cosmosdb cassandra table show
Show the details of a Cassandra table under an Azure Cosmos DB Cassandra keyspace.
Core
GA
az cosmosdb cassandra table throughput
Manage throughput of Cassandra table under an Azure Cosmos DB account.
Core
GA
az cosmosdb cassandra table throughput migrate
Migrate the throughput of the Cassandra table between autoscale and manually provisioned.
Core
GA
az cosmosdb cassandra table throughput show
Get the throughput of the Cassandra table under an Azure Cosmos DB Cassandra keyspace.
Core
GA
az cosmosdb cassandra table throughput update
Update the throughput of the Cassandra table under an Azure Cosmos DB Cassandra keyspace.
Core
GA
az cosmosdb cassandra table update
Update an Cassandra table under an Azure Cosmos DB Cassandra keyspace.
Core
GA
az cosmosdb check-name-exists
Checks if an Azure Cosmos DB account name exists.
Core
GA
az cosmosdb copy
Manage container copy job.
Extension
Preview
az cosmosdb copy cancel
Cancel a container copy job.
Extension
Preview
az cosmosdb copy complete
Completes an online container copy job.
Extension
Preview
az cosmosdb copy create
Creates a container copy job.
Extension
Preview
az cosmosdb copy list
Get a container copy job.
Extension
Preview
az cosmosdb copy pause
Pause a container copy job.
Extension
Preview
az cosmosdb copy resume
Resume a container copy job.
Extension
Preview
az cosmosdb copy show
Get a container copy job.
Extension
Preview
az cosmosdb create
Creates a new Azure Cosmos DB database account.
Core
GA
az cosmosdb create (cosmosdb-preview extension)
Creates a new Azure Cosmos DB database account.
Extension
Preview
az cosmosdb delete
Deletes an Azure Cosmos DB database account.
Core
GA
az cosmosdb failover-priority-change
Changes the failover priority for the Azure Cosmos DB database account.
Core
GA
az cosmosdb fleet
Manage Azure Cosmos DB Fleet resources.
Core and Extension
Preview
az cosmosdb fleet analytics
Manage Azure Cosmos DB Fleet Analytics resources.
Extension
Preview
az cosmosdb fleet analytics create
Create a new Fleet Analytics resource under a Cosmos DB Fleet.
Extension
Preview
az cosmosdb fleet analytics delete
Delete a Fleet Analytics resource from a Fleet.
Extension
Preview
az cosmosdb fleet analytics list
List all Fleet Analytics resources under a Fleet.
Extension
Preview
az cosmosdb fleet analytics show
Show details of a specific Fleet Analytics resource.
Extension
Preview
az cosmosdb fleet create
Create a new Cosmos DB Fleet.
Core
Preview
az cosmosdb fleet create (cosmosdb-preview extension)
Create a new Cosmos DB Fleet.
Extension
Preview
az cosmosdb fleet delete
Delete a specific Cosmos DB Fleet.
Core
Preview
az cosmosdb fleet delete (cosmosdb-preview extension)
Delete a specific Cosmos DB Fleet.
Extension
Preview
az cosmosdb fleet list
List Cosmos DB Fleets in a subscription or resource group.
Core
Preview
az cosmosdb fleet list (cosmosdb-preview extension)
List Cosmos DB Fleets in a subscription or resource group.
Extension
Preview
az cosmosdb fleet show
Show details of a specific Cosmos DB Fleet.
Core
Preview
az cosmosdb fleet show (cosmosdb-preview extension)
Show details of a specific Cosmos DB Fleet.
Extension
Preview
az cosmosdb fleetspace
Manage Cosmos DB Fleetspace resources.
Core and Extension
Preview
az cosmosdb fleetspace account
Manage database accounts within a Cosmos DB Fleetspace.
Core and Extension
Preview
az cosmosdb fleetspace account create
Register an existing Cosmos DB database account to a Fleetspace.
Core
Preview
az cosmosdb fleetspace account create (cosmosdb-preview extension)
Register an existing Cosmos DB database account to a Fleetspace.
Extension
Preview
az cosmosdb fleetspace account delete
Unregister a database account from a Fleetspace.
Core
Preview
az cosmosdb fleetspace account delete (cosmosdb-preview extension)
Unregister a database account from a Fleetspace.
Extension
Preview
az cosmosdb fleetspace account list
List all database accounts associated with a Fleetspace.
Core
Preview
az cosmosdb fleetspace account list (cosmosdb-preview extension)
List all database accounts associated with a Fleetspace.
Extension
Preview
az cosmosdb fleetspace account show
Show details of a registered database account in a Fleetspace.
Core
Preview
az cosmosdb fleetspace account show (cosmosdb-preview extension)
Show details of a registered database account in a Fleetspace.
Extension
Preview
az cosmosdb fleetspace create
Create a new Fleetspace under a Cosmos DB Fleet.
Core
Preview
az cosmosdb fleetspace create (cosmosdb-preview extension)
Create a new Fleetspace under a Cosmos DB Fleet.
Extension
Preview
az cosmosdb fleetspace delete
Delete a Fleetspace from a Fleet.
Core
Preview
az cosmosdb fleetspace delete (cosmosdb-preview extension)
Delete a Fleetspace from a Fleet.
Extension
Preview
az cosmosdb fleetspace list
List all Fleetspaces under a Fleet.
Core
Preview
az cosmosdb fleetspace list (cosmosdb-preview extension)
List all Fleetspaces under a Fleet.
Extension
Preview
az cosmosdb fleetspace show
Show details of a specific Fleetspace.
Core
Preview
az cosmosdb fleetspace show (cosmosdb-preview extension)
Show details of a specific Fleetspace.
Extension
Preview
az cosmosdb fleetspace update
Update an existing Cosmos DB Fleetspace.
Core
Preview
az cosmosdb fleetspace update (cosmosdb-preview extension)
Update an existing Cosmos DB Fleetspace.
Extension
Preview
az cosmosdb gremlin
Manage Gremlin resources of Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb gremlin database
Manage Azure Cosmos DB Gremlin databases.
Core and Extension
GA
az cosmosdb gremlin database create
Create an Gremlin database under an Azure Cosmos DB account.
Core
GA
az cosmosdb gremlin database delete
Delete the Gremlin database under an Azure Cosmos DB account.
Core
GA
az cosmosdb gremlin database exists
Checks if an Azure Cosmos DB Gremlin database exists.
Core
GA
az cosmosdb gremlin database list
List the Gremlin databases under an Azure Cosmos DB account.
Core
GA
az cosmosdb gremlin database restore
Restore a deleted gremlin database within the same account.
Core
GA
az cosmosdb gremlin database restore (cosmosdb-preview extension)
Restore a deleted gremlin database within the same account.
Extension
Preview
az cosmosdb gremlin database show
Show the details of a Gremlin database under an Azure Cosmos DB account.
Core
GA
az cosmosdb gremlin database throughput
Manage throughput of Gremlin database under an Azure Cosmos DB account.
Core
GA
az cosmosdb gremlin database throughput migrate
Migrate the throughput of the Gremlin database between autoscale and manually provisioned.
Core
GA
az cosmosdb gremlin database throughput show
Get the throughput of the Gremlin database under an Azure Cosmos DB account.
Core
GA
az cosmosdb gremlin database throughput update
Update the throughput of the Gremlin database under an Azure Cosmos DB account.
Core
GA
az cosmosdb gremlin graph
Manage Azure Cosmos DB Gremlin graphs.
Core and Extension
GA
az cosmosdb gremlin graph create
Create an Gremlin graph under an Azure Cosmos DB Gremlin database.
Core
GA
az cosmosdb gremlin graph delete
Delete the Gremlin graph under an Azure Cosmos DB Gremlin database.
Core
GA
az cosmosdb gremlin graph exists
Checks if an Azure Cosmos DB Gremlin graph exists.
Core
GA
az cosmosdb gremlin graph list
List the Gremlin graphs under an Azure Cosmos DB Gremlin database.
Core
GA
az cosmosdb gremlin graph restore
Restore a deleted gremlin graph within the same account.
Core
GA
az cosmosdb gremlin graph restore (cosmosdb-preview extension)
Restore a deleted gremlin graph within the same account.
Extension
Preview
az cosmosdb gremlin graph show
Show the details of a Gremlin graph under an Azure Cosmos DB Gremlin database.
Core
GA
az cosmosdb gremlin graph throughput
Manage throughput of Gremlin graph under an Azure Cosmos DB account.
Core
GA
az cosmosdb gremlin graph throughput migrate
Migrate the throughput of the Gremlin Graph between autoscale and manually provisioned.
Core
GA
az cosmosdb gremlin graph throughput show
Get the throughput of the Gremlin graph under an Azure Cosmos DB Gremlin database.
Core
GA
az cosmosdb gremlin graph throughput update
Update the throughput of the Gremlin graph under an Azure Cosmos DB Gremlin database.
Core
GA
az cosmosdb gremlin graph update
Update an Gremlin graph under an Azure Cosmos DB Gremlin database.
Core
GA
az cosmosdb gremlin restorable-database
Manage different versions of gremlin databases that are restorable in a Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb gremlin restorable-database list
List all the versions of all the gremlin databases that were created / modified / deleted in the given restorable account.
Core
GA
az cosmosdb gremlin restorable-database list (cosmosdb-preview extension)
List all the versions of all the gremlin databases that were created / modified / deleted in the given restorable account.
Extension
Preview
az cosmosdb gremlin restorable-graph
Manage different versions of gremlin graphs that are restorable in a database of a Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb gremlin restorable-graph list
List all the versions of all the gremlin graphs that were created / modified / deleted in the given database and restorable account.
Core
GA
az cosmosdb gremlin restorable-graph list (cosmosdb-preview extension)
List all the versions of all the gremlin graphs that were created / modified / deleted in the given database and restorable account.
Extension
Preview
az cosmosdb gremlin restorable-resource
Manage the databases and its graphs that can be restored in the given account at the given timestamp and region.
Core and Extension
GA
az cosmosdb gremlin restorable-resource list
List all the databases and its graphs that can be restored in the given account at the given timestamp and region.
Core
GA
az cosmosdb gremlin restorable-resource list (cosmosdb-preview extension)
List all the databases and its graphs that can be restored in the given account at the given timestamp and region.
Extension
Preview
az cosmosdb gremlin retrieve-latest-backup-time
Retrieves latest restorable timestamp for the given gremlin graph in given region.
Core
GA
az cosmosdb gremlin retrieve-latest-backup-time (cosmosdb-preview extension)
Retrieves latest restorable timestamp for the given gremlin graph in given region.
Extension
Preview
az cosmosdb gremlin role
Manage Azure Cosmos DB Gremlin role resources.
Extension
GA
az cosmosdb gremlin role assignment
Manage Azure Cosmos DB Gremlin role assignments.
Extension
GA
az cosmosdb gremlin role assignment create
Create a Gremlin role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role assignment delete
Delete a Gremlin role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role assignment exists
Check if an Azure Cosmos DB role assignment exists.
Extension
GA
az cosmosdb gremlin role assignment list
List all Gremlin role assignments under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role assignment show
Show the properties of a Gremlin role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role assignment update
Update a Gremlin role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role definition
Manage Azure Cosmos DB Gremlin role definitions.
Extension
GA
az cosmosdb gremlin role definition create
Create a Gremlin role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role definition delete
Delete a Gremlin role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role definition exists
Check if an Azure Cosmos DB role definition exists.
Extension
GA
az cosmosdb gremlin role definition list
List all Gremlin role definitions under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role definition show
Show the properties of a Gremlin role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb gremlin role definition update
Update a Gremlin role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb identity
Manage Azure Cosmos DB managed service identities.
Core
Preview
az cosmosdb identity assign
Assign SystemAssigned identity for a Azure Cosmos DB database account.
Core
Preview
az cosmosdb identity remove
Remove SystemAssigned identity for a Azure Cosmos DB database account.
Core
Preview
az cosmosdb identity show
Show the identities for a Azure Cosmos DB database account.
Core
Preview
az cosmosdb keys
Manage Azure Cosmos DB keys.
Core
GA
az cosmosdb keys list
List the access keys or connection strings for a Azure Cosmos DB database account.
Core
GA
az cosmosdb keys regenerate
Regenerate an access key for a Azure Cosmos DB database account.
Core
GA
az cosmosdb list
List Azure Cosmos DB database accounts.
Core
GA
az cosmosdb list (cosmosdb-preview extension)
List Azure Cosmos DB database accounts.
Extension
GA
az cosmosdb locations
Manage Azure Cosmos DB location properties.
Core
GA
az cosmosdb locations list
Retrieves the list of cosmosdb locations and their properties.
Core
GA
az cosmosdb locations show
Show the Azure Cosmos DB location properties in the given location.
Core
GA
az cosmosdb mongocluster
Mongo cluster.
Extension
Preview
az cosmosdb mongocluster create
Create a Mongo cluster.
Extension
Preview
az cosmosdb mongocluster delete
Delete a Mongo Cluster Resource.
Extension
Preview
az cosmosdb mongocluster firewall
Mongo cluster firewall.
Extension
Preview
az cosmosdb mongocluster firewall rule
Mongo cluster firewall rule.
Extension
Preview
az cosmosdb mongocluster firewall rule create
Create a Mongo cluster firewall rule.
Extension
Preview
az cosmosdb mongocluster firewall rule delete
Delete a Mongo cluster firewall rule.
Extension
Preview
az cosmosdb mongocluster firewall rule list
Lists firewall rule on a Mongo cluster.
Extension
Preview
az cosmosdb mongocluster firewall rule show
Get a Mongo cluster firewall rule.
Extension
Preview
az cosmosdb mongocluster firewall rule update
Create a Mongo cluster firewall rule.
Extension
Preview
az cosmosdb mongocluster list
List a Mongo Cluster Resource.
Extension
Preview
az cosmosdb mongocluster show
Get a Mongo Cluster Resource.
Extension
Preview
az cosmosdb mongocluster update
Update a Mongo cluster.
Extension
Preview
az cosmosdb mongodb
Manage MongoDB resources of Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb mongodb collection
Manage Azure Cosmos DB MongoDB collections.
Core and Extension
GA
az cosmosdb mongodb collection create
Create an MongoDB collection under an Azure Cosmos DB MongoDB database.
Core
GA
az cosmosdb mongodb collection delete
Delete the MongoDB collection under an Azure Cosmos DB MongoDB database.
Core
GA
az cosmosdb mongodb collection exists
Checks if an Azure Cosmos DB MongoDB collection exists.
Core
GA
az cosmosdb mongodb collection list
List the MongoDB collections under an Azure Cosmos DB MongoDB database.
Core
GA
az cosmosdb mongodb collection merge
Merges the partitions of a mongodb collection.
Extension
Preview
az cosmosdb mongodb collection redistribute-partition-throughput
Redistributes the partition throughput of a mongodb collection.
Extension
Preview
az cosmosdb mongodb collection restore
Restore a deleted mongodb collection within the same account.
Core
GA
az cosmosdb mongodb collection restore (cosmosdb-preview extension)
Restore a deleted mongodb collection within the same account.
Extension
Preview
az cosmosdb mongodb collection retrieve-partition-throughput
Retrieve the partition throughput of a mongodb collection.
Extension
Preview
az cosmosdb mongodb collection show
Show the details of a MongoDB collection under an Azure Cosmos DB MongoDB database.
Core
GA
az cosmosdb mongodb collection throughput
Manage throughput of MongoDB collection under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb collection throughput migrate
Migrate the throughput of the MongoDB collection between autoscale and manually provisioned.
Core
GA
az cosmosdb mongodb collection throughput show
Get the throughput of the MongoDB collection under an Azure Cosmos DB MongoDB database.
Core
GA
az cosmosdb mongodb collection throughput update
Update the throughput of the MongoDB collection under an Azure Cosmos DB MongoDB database.
Core
GA
az cosmosdb mongodb collection update
Update an MongoDB collection under an Azure Cosmos DB MongoDB database.
Core
GA
az cosmosdb mongodb database
Manage Azure Cosmos DB MongoDB databases.
Core and Extension
GA
az cosmosdb mongodb database create
Create an MongoDB database under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb database delete
Delete the MongoDB database under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb database exists
Checks if an Azure Cosmos DB MongoDB database exists.
Core
GA
az cosmosdb mongodb database list
List the MongoDB databases under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb database merge
Merges the partitions of a mongodb database.
Extension
Preview
az cosmosdb mongodb database restore
Restore a deleted mongodb database within the same account.
Core
GA
az cosmosdb mongodb database restore (cosmosdb-preview extension)
Restore a deleted mongodb database within the same account.
Extension
Preview
az cosmosdb mongodb database show
Show the details of a MongoDB database under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb database throughput
Manage throughput of MongoDB database under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb database throughput migrate
Migrate the throughput of the MongoDB database between autoscale and manually provisioned.
Core
GA
az cosmosdb mongodb database throughput show
Get the throughput of the MongoDB database under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb database throughput update
Update the throughput of the MongoDB database under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb restorable-collection
Manage different versions of mongodb collections that are restorable in a database of a Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb mongodb restorable-collection list
List all the versions of all the mongodb collections that were created / modified / deleted in the given database and restorable account.
Core
GA
az cosmosdb mongodb restorable-collection list (cosmosdb-preview extension)
List all the versions of all the mongodb collections that were created / modified / deleted in the given database and restorable account.
Extension
Preview
az cosmosdb mongodb restorable-database
Manage different versions of mongodb databases that are restorable in a Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb restorable-database list
List all the versions of all the mongodb databases that were created / modified / deleted in the given restorable account.
Core
GA
az cosmosdb mongodb restorable-resource
Manage the databases and its collections that can be restored in the given account at the given timesamp and region.
Core
GA
az cosmosdb mongodb restorable-resource list
List all the databases and its collections that can be restored in the given account at the given timesamp and region.
Core
GA
az cosmosdb mongodb retrieve-latest-backup-time
Retrieves latest restorable timestamp for the given mongodb collection in given region.
Core
GA
az cosmosdb mongodb role
Manage Azure Cosmos DB Mongo role resources.
Core and Extension
GA
az cosmosdb mongodb role definition
Manage Azure Cosmos DB Mongo role definitions.
Core and Extension
GA
az cosmosdb mongodb role definition create
Create a Mongo DB role definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb role definition create (cosmosdb-preview extension)
Create a Mongo DB role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb role definition delete
Delete a CosmosDb MongoDb role definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb role definition delete (cosmosdb-preview extension)
Delete a CosmosDb MongoDb role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb role definition exists
Check if an Azure Cosmos DB MongoDb role definition exists.
Core
GA
az cosmosdb mongodb role definition exists (cosmosdb-preview extension)
Check if an Azure Cosmos DB MongoDb role definition exists.
Extension
GA
az cosmosdb mongodb role definition list
List all MongoDb role definitions under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb role definition list (cosmosdb-preview extension)
List all MongoDb role definitions under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb role definition show
Show the properties of a MongoDb role definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb role definition show (cosmosdb-preview extension)
Show the properties of a MongoDb role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb role definition update
Update a MongoDb role definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb role definition update (cosmosdb-preview extension)
Update a MongoDb role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb user
Manage Azure Cosmos DB Mongo user resources.
Core and Extension
GA
az cosmosdb mongodb user definition
Manage Azure Cosmos DB Mongo user definitions.
Core and Extension
GA
az cosmosdb mongodb user definition create
Create a Mongo DB user definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb user definition create (cosmosdb-preview extension)
Create a Mongo DB user definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb user definition delete
Delete a CosmosDb MongoDb user definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb user definition delete (cosmosdb-preview extension)
Delete a CosmosDb MongoDb user definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb user definition exists
Check if an Azure Cosmos DB MongoDb user definition exists.
Core
GA
az cosmosdb mongodb user definition exists (cosmosdb-preview extension)
Check if an Azure Cosmos DB MongoDb user definition exists.
Extension
GA
az cosmosdb mongodb user definition list
List all MongoDb user definitions under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb user definition list (cosmosdb-preview extension)
List all MongoDb user definitions under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb user definition show
Show the properties of a MongoDb user definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb user definition show (cosmosdb-preview extension)
Show the properties of a MongoDb user definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongodb user definition update
Update a MongoDb user definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb mongodb user definition update (cosmosdb-preview extension)
Update a MongoDb user definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi
Manage Azure Cosmos DB MongoMI resources.
Extension
GA
az cosmosdb mongomi role
Manage Azure Cosmos DB MongoMI role resources.
Extension
GA
az cosmosdb mongomi role assignment
Manage Azure Cosmos DB MongoMI role assignments.
Extension
GA
az cosmosdb mongomi role assignment create
Create a MongoMI role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role assignment delete
Delete a MongoMI role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role assignment exists
Check if an Azure Cosmos DB role assignment exists.
Extension
GA
az cosmosdb mongomi role assignment list
List all MongoMI role assignments under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role assignment show
Show the properties of a MongoMI role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role assignment update
Update a MongoMI role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role definition
Manage Azure Cosmos DB MongoMI role definitions.
Extension
GA
az cosmosdb mongomi role definition create
Create a MongoMI role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role definition delete
Delete a MongoMI role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role definition exists
Check if an Azure Cosmos DB role definition exists.
Extension
GA
az cosmosdb mongomi role definition list
List all MongoMI role definitions under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role definition show
Show the properties of a MongoMI role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb mongomi role definition update
Update a MongoMI role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb network-rule
Manage Azure Cosmos DB network rules.
Core
GA
az cosmosdb network-rule add
Adds a virtual network rule to an existing Cosmos DB database account.
Core
GA
az cosmosdb network-rule list
Lists the virtual network accounts associated with a Cosmos DB account.
Core
GA
az cosmosdb network-rule remove
Remove a virtual network rule from an existing Cosmos DB database account.
Core
GA
az cosmosdb offline-region
Offline the specified region for the specified Azure Cosmos DB database account.
Core
GA
az cosmosdb postgres
Manage Azure Cosmos DB for PostgreSQL resources.
Core
GA
az cosmosdb postgres check-name-availability
Checks availability of a cluster name. Cluster names should be globally unique; at least 3 characters and at most 40 characters long; they must only contain lowercase letters, numbers, and hyphens; and must not start or end with a hyphen.
Core
GA
az cosmosdb postgres cluster
Manage Azure Cosmos DB for PostgreSQL clusters.
Core
GA
az cosmosdb postgres cluster create
Create a new cluster with nodes.
Core
GA
az cosmosdb postgres cluster delete
Delete a cluster together with nodes in it.
Core
GA
az cosmosdb postgres cluster list
List all clusters in a subscription or a resource group.
Core
GA
az cosmosdb postgres cluster promote
Promotes read replica cluster to an independent read-write cluster.
Core
GA
az cosmosdb postgres cluster restart
Restarts all nodes in the cluster.
Core
GA
az cosmosdb postgres cluster server
Manage Azure Cosmos DB for PostgreSQL cluster servers.
Core
GA
az cosmosdb postgres cluster server list
List nodes of a cluster.
Core
GA
az cosmosdb postgres cluster server show
Get information about a node in cluster.
Core
GA
az cosmosdb postgres cluster show
Get information about a cluster such as compute and storage configuration and cluster lifecycle metadata such as cluster creation date and time.
Core
GA
az cosmosdb postgres cluster start
Starts stopped compute on all cluster nodes.
Core
GA
az cosmosdb postgres cluster stop
Stops compute on all cluster nodes.
Core
GA
az cosmosdb postgres cluster update
Update an existing cluster. The request body can contain one or several properties from the cluster definition.
Core
GA
az cosmosdb postgres cluster wait
Place the CLI in a waiting state until a condition is met.
Core
GA
az cosmosdb postgres configuration
Manage Azure Cosmos DB for PostgreSQL configurations.
Core
GA
az cosmosdb postgres configuration coordinator
Manage Azure Cosmos DB for PostgreSQL coordinator configurations.
Core
GA
az cosmosdb postgres configuration coordinator show
Get information of a configuration for coordinator.
Core
GA
az cosmosdb postgres configuration coordinator update
Updates configuration of coordinator in a cluster.
Core
GA
az cosmosdb postgres configuration coordinator wait
Place the CLI in a waiting state until a condition is met.
Core
GA
az cosmosdb postgres configuration list
List all the configurations of a cluster.
Core
GA
az cosmosdb postgres configuration node
Manage Azure Cosmos DB for PostgreSQL node configurations.
Core
GA
az cosmosdb postgres configuration node show
Get information of a configuration for worker nodes.
Core
GA
az cosmosdb postgres configuration node update
Updates configuration of worker nodes in a cluster.
Core
GA
az cosmosdb postgres configuration node wait
Place the CLI in a waiting state until a condition is met.
Core
GA
az cosmosdb postgres configuration server
Manage Azure Cosmos DB for PostgreSQL server configurations.
Core
GA
az cosmosdb postgres configuration server list
List all the configurations of a server in cluster.
Core
GA
az cosmosdb postgres configuration show
Get information of a configuration for coordinator and nodes.
Core
GA
az cosmosdb postgres firewall-rule
Manage Azure Cosmos DB for PostgreSQL firewall rules.
Core
GA
az cosmosdb postgres firewall-rule create
Create a new cluster firewall rule or updates an existing cluster firewall rule.
Core
GA
az cosmosdb postgres firewall-rule delete
Delete a cluster firewall rule.
Core
GA
az cosmosdb postgres firewall-rule list
List all the firewall rules on cluster.
Core
GA
az cosmosdb postgres firewall-rule show
Get information about a cluster firewall rule.
Core
GA
az cosmosdb postgres firewall-rule update
Update an existing cluster firewall rule.
Core
GA
az cosmosdb postgres firewall-rule wait
Place the CLI in a waiting state until a condition is met.
Core
GA
az cosmosdb postgres role
Manage Azure Cosmos DB for PostgreSQL roles.
Core
GA
az cosmosdb postgres role create
Create a new role or updates an existing role.
Core
GA
az cosmosdb postgres role delete
Delete a cluster role.
Core
GA
az cosmosdb postgres role list
List all the roles in a given cluster.
Core
GA
az cosmosdb postgres role show
Get information about a cluster role.
Core
GA
az cosmosdb postgres role update
Update an existing role.
Core
GA
az cosmosdb postgres role wait
Place the CLI in a waiting state until a condition is met.
Core
GA
az cosmosdb private-endpoint-connection
Manage Azure Cosmos DB private endpoint connections.
Core
GA
az cosmosdb private-endpoint-connection approve
Approve the specified private endpoint connection associated with Azure Cosmos DB.
Core
GA
az cosmosdb private-endpoint-connection delete
Delete the specified private endpoint connection associated with Azure Cosmos DB.
Core
GA
az cosmosdb private-endpoint-connection reject
Reject the specified private endpoint connection associated with Azure Cosmos DB.
Core
GA
az cosmosdb private-endpoint-connection show
Show details of a private endpoint connection associated with Azure Cosmos DB.
Core
GA
az cosmosdb private-link-resource
Manage Azure Cosmos DB private link resources.
Core
GA
az cosmosdb private-link-resource list
List the private link resources supported for Azure Cosmos DB.
Core
GA
az cosmosdb restorable-database-account
Manage restorable Azure Cosmos DB accounts.
Core and Extension
GA
az cosmosdb restorable-database-account list
List all the database accounts that can be restored.
Core
GA
az cosmosdb restorable-database-account list (cosmosdb-preview extension)
List all the database accounts that can be restored.
Extension
GA
az cosmosdb restorable-database-account show
Show the details of a database account that can be restored.
Core
GA
az cosmosdb restorable-database-account show (cosmosdb-preview extension)
Show the details of a database account that can be restored.
Extension
GA
az cosmosdb restore
Create a new Azure Cosmos DB database account by restoring from an existing database account.
Core
GA
az cosmosdb restore (cosmosdb-preview extension)
Create a new Azure Cosmos DB database account by restoring from an existing database account.
Extension
Preview
az cosmosdb service
Commands to perform operations on Service.
Core and Extension
GA
az cosmosdb service create
Create a cosmosdb service resource.
Core
GA
az cosmosdb service create (cosmosdb-preview extension)
Create a cosmosdb service resource.
Extension
Preview
az cosmosdb service delete
Delete the given cosmosdb service resource.
Core
GA
az cosmosdb service delete (cosmosdb-preview extension)
Delete the given cosmosdb service resource.
Extension
Preview
az cosmosdb service list
List all cosmosdb service resource under an account.
Core
GA
az cosmosdb service list (cosmosdb-preview extension)
List all cosmosdb service resource under an account.
Extension
Preview
az cosmosdb service show
Get cosmosdb service resource under an account.
Core
GA
az cosmosdb service show (cosmosdb-preview extension)
Get cosmosdb service resource under an account.
Extension
Preview
az cosmosdb service update
Update a cosmosdb service resource.
Core
GA
az cosmosdb service update (cosmosdb-preview extension)
Update a cosmosdb service resource.
Extension
Preview
az cosmosdb show
Get the details of an Azure Cosmos DB database account.
Core
GA
az cosmosdb show (cosmosdb-preview extension)
Get the details of an Azure Cosmos DB database account.
Extension
GA
az cosmosdb sql
Manage SQL resources of Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb sql container
Manage Azure Cosmos DB SQL containers.
Core and Extension
GA
az cosmosdb sql container create
Create an SQL container under an Azure Cosmos DB SQL database.
Core
GA
az cosmosdb sql container create (cosmosdb-preview extension)
Create an SQL container under an Azure Cosmos DB SQL database.
Extension
GA
az cosmosdb sql container delete
Delete the SQL container under an Azure Cosmos DB SQL database.
Core
GA
az cosmosdb sql container exists
Checks if an Azure Cosmos DB SQL container exists.
Core
GA
az cosmosdb sql container list
List the SQL containers under an Azure Cosmos DB SQL database.
Core
GA
az cosmosdb sql container merge
Merges the partitions of a sql container.
Extension
Preview
az cosmosdb sql container redistribute-partition-throughput
Redistributes the partition throughput of a sql container.
Extension
Preview
az cosmosdb sql container restore
Restore a deleted sql container within the same account.
Core
GA
az cosmosdb sql container restore (cosmosdb-preview extension)
Restore a deleted sql container within the same account.
Extension
Preview
az cosmosdb sql container retrieve-partition-throughput
Retrieve  the partition throughput of a sql container.
Extension
Preview
az cosmosdb sql container show
Show the details of a SQL container under an Azure Cosmos DB SQL database.
Core
GA
az cosmosdb sql container throughput
Manage throughput of SQL container under an Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb sql container throughput migrate
Migrate the throughput of the SQL container between autoscale and manually provisioned.
Core
GA
az cosmosdb sql container throughput migrate (cosmosdb-preview extension)
Migrate the throughput of the SQL container between autoscale and manually provisioned.
Extension
GA
az cosmosdb sql container throughput show
Get the throughput of the SQL container under an Azure Cosmos DB SQL database.
Core
GA
az cosmosdb sql container throughput show (cosmosdb-preview extension)
Get the throughput of the SQL container under an Azure Cosmos DB SQL database.
Extension
GA
az cosmosdb sql container throughput update
Update the throughput of the SQL container under an Azure Cosmos DB SQL database.
Core
GA
az cosmosdb sql container throughput update (cosmosdb-preview extension)
Update the throughput of the SQL container under an Azure Cosmos DB SQL database.
Extension
GA
az cosmosdb sql container update
Update an SQL container under an Azure Cosmos DB SQL database.
Core
GA
az cosmosdb sql container update (cosmosdb-preview extension)
Update an SQL container under an Azure Cosmos DB SQL database.
Extension
GA
az cosmosdb sql database
Manage Azure Cosmos DB SQL databases.
Core and Extension
GA
az cosmosdb sql database create
Create an SQL database under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql database delete
Delete the SQL database under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql database exists
Checks if an Azure Cosmos DB SQL database exists.
Core
GA
az cosmosdb sql database list
List the SQL databases under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql database merge
Merge the partitions of a sql database.
Extension
Preview
az cosmosdb sql database restore
Restore a deleted sql database within the same account.
Core
GA
az cosmosdb sql database restore (cosmosdb-preview extension)
Restore a deleted sql database within the same account.
Extension
Preview
az cosmosdb sql database show
Show the details of a SQL database under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql database throughput
Manage throughput of SQL database under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql database throughput migrate
Migrate the throughput of the SQL database between autoscale and manually provisioned.
Core
GA
az cosmosdb sql database throughput show
Get the throughput of the SQL database under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql database throughput update
Update the throughput of the SQL database under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql restorable-container
Manage different versions of sql containers that are restorable in a database of a Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb sql restorable-container list
List all the versions of all the sql containers that were created / modified / deleted in the given database and restorable account.
Core
GA
az cosmosdb sql restorable-container list (cosmosdb-preview extension)
List all the versions of all the sql containers that were created / modified / deleted in the given database and restorable account.
Extension
Preview
az cosmosdb sql restorable-database
Manage different versions of sql databases that are restorable in a Azure Cosmos DB account.
Core
GA
az cosmosdb sql restorable-database list
List all the versions of all the sql databases that were created / modified / deleted in the given restorable account.
Core
GA
az cosmosdb sql restorable-resource
Manage the databases and its containers that can be restored in the given account at the given timesamp and region.
Core
GA
az cosmosdb sql restorable-resource list
List all the databases and its containers that can be restored in the given account at the given timesamp and region.
Core
GA
az cosmosdb sql retrieve-latest-backup-time
Retrieves latest restorable timestamp for the given sql container in given region.
Core
GA
az cosmosdb sql role
Manage Azure Cosmos DB SQL role resources.
Core
GA
az cosmosdb sql role assignment
Manage Azure Cosmos DB SQL role assignments.
Core
GA
az cosmosdb sql role assignment create
Create a SQL role assignment under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role assignment delete
Delete a SQL role assignment under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role assignment exists
Check if an Azure Cosmos DB role assignment exists.
Core
GA
az cosmosdb sql role assignment list
List all SQL role assignments under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role assignment show
Show the properties of a SQL role assignment under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role assignment update
Update a SQL role assignment under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role assignment wait
Poll on a SQL role assignment until a specific condition is met.
Core
GA
az cosmosdb sql role definition
Manage Azure Cosmos DB SQL role definitions.
Core
GA
az cosmosdb sql role definition create
Create a SQL role definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role definition delete
Delete a SQL role definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role definition exists
Check if an Azure Cosmos DB role definition exists.
Core
GA
az cosmosdb sql role definition list
List all SQL role definitions under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role definition show
Show the properties of a SQL role definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role definition update
Update a SQL role definition under an Azure Cosmos DB account.
Core
GA
az cosmosdb sql role definition wait
Poll on a SQL role definition until a specific condition is met.
Core
GA
az cosmosdb sql stored-procedure
Manage Azure Cosmos DB SQL stored procedures.
Core
GA
az cosmosdb sql stored-procedure create
Create an SQL stored procedure under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql stored-procedure delete
Delete the SQL stored procedure under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql stored-procedure list
List the SQL stored procedures under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql stored-procedure show
Show the details of a SQL stored procedure under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql stored-procedure update
Creates or Updates an Azure Cosmos DB SQL stored procedure.
Core
GA
az cosmosdb sql trigger
Manage Azure Cosmos DB SQL triggers.
Core
GA
az cosmosdb sql trigger create
Create an SQL trigger under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql trigger delete
Delete the SQL trigger under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql trigger list
List the SQL triggers under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql trigger show
Show the details of a SQL trigger under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql trigger update
Updates an Azure Cosmos DB SQL trigger.
Core
GA
az cosmosdb sql user-defined-function
Manage Azure Cosmos DB SQL user defined functions.
Core
GA
az cosmosdb sql user-defined-function create
Create an SQL user defined function under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql user-defined-function delete
Delete the SQL user defined function under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql user-defined-function list
List the SQL user defined functions under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql user-defined-function show
Show the details of a SQL user defined function under an Azure Cosmos DB SQL container.
Core
GA
az cosmosdb sql user-defined-function update
Creates or Updates an Azure Cosmos DB SQL user defined function.
Core
GA
az cosmosdb table
Manage Table resources of Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb table create
Create an Table under an Azure Cosmos DB account.
Core
GA
az cosmosdb table delete
Delete the Table under an Azure Cosmos DB account.
Core
GA
az cosmosdb table exists
Checks if an Azure Cosmos DB table exists.
Core
GA
az cosmosdb table list
List the Tables under an Azure Cosmos DB account.
Core
GA
az cosmosdb table restorable-resource
Manage the tables that can be restored in the given account at the given timestamp and region.
Core and Extension
GA
az cosmosdb table restorable-resource list
List all the tables that can be restored in the given account at the given timestamp and region.
Core
GA
az cosmosdb table restorable-resource list (cosmosdb-preview extension)
List all the tables that can be restored in the given account at the given timestamp and region.
Extension
Preview
az cosmosdb table restorable-table
Manage different versions of tables that are restorable in Azure Cosmos DB account.
Core and Extension
GA
az cosmosdb table restorable-table list
List all the versions of all the tables that were created / modified / deleted in the given restorable account.
Core
GA
az cosmosdb table restorable-table list (cosmosdb-preview extension)
List all the versions of all the tables that were created / modified / deleted in the given restorable account.
Extension
Preview
az cosmosdb table restore
Restore a deleted table within the same account.
Core
GA
az cosmosdb table restore (cosmosdb-preview extension)
Restore a deleted table within the same account.
Extension
Preview
az cosmosdb table retrieve-latest-backup-time
Retrieves latest restorable timestamp for the given table in given region.
Core
GA
az cosmosdb table retrieve-latest-backup-time (cosmosdb-preview extension)
Retrieves latest restorable timestamp for the given table in given region.
Extension
Preview
az cosmosdb table role
Manage Azure Cosmos DB Table role resources.
Extension
GA
az cosmosdb table role assignment
Manage Azure Cosmos DB Table role assignments.
Extension
GA
az cosmosdb table role assignment create
Create a Table role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role assignment delete
Delete a Table role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role assignment exists
Check if an Azure Cosmos DB role assignment exists.
Extension
GA
az cosmosdb table role assignment list
List all Table role assignments under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role assignment show
Show the properties of a Table role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role assignment update
Update a Table role assignment under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role definition
Manage Azure Cosmos DB Table role definitions.
Extension
GA
az cosmosdb table role definition create
Create a Table role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role definition delete
Delete a Table role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role definition exists
Check if an Azure Cosmos DB role definition exists.
Extension
GA
az cosmosdb table role definition list
List all Table role definitions under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role definition show
Show the properties of a Table role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table role definition update
Update a Table role definition under an Azure Cosmos DB account.
Extension
GA
az cosmosdb table show
Show the details of a Table under an Azure Cosmos DB account.
Core
GA
az cosmosdb table throughput
Manage throughput of Table under an Azure Cosmos DB account.
Core
GA
az cosmosdb table throughput migrate
Migrate the throughput of the Table between autoscale and manually provisioned.
Core
GA
az cosmosdb table throughput show
Get the throughput of the Table under an Azure Cosmos DB account.
Core
GA
az cosmosdb table throughput update
Update the throughput of the Table under an Azure Cosmos DB account.
Core
GA
az cosmosdb update
Update an Azure Cosmos DB database account.
Core
GA
az cosmosdb update (cosmosdb-preview extension)
Update an Azure Cosmos DB database account.
Extension
GA
az cosmosdb check-name-exists
Edit
Checks if an Azure Cosmos DB account name exists.
```
az cosmosdb check-name-exists [--acquire-policy-token]
                              [--change-reference]
                              [--ids]
                              [--name]
                              [--subscription]
```
Examples
Checks if an Azure Cosmos DB account name exists. (autogenerated)
```
az cosmosdb check-name-exists --name MyCosmosDBDatabaseAccount
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
Name of the Cosmos DB database account.
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
az cosmosdb create
Edit
Creates a new Azure Cosmos DB database account.
```
az cosmosdb create --name
                   --resource-group
                   [--acquire-policy-token]
                   [--analytical-storage-schema-type --as-schema {FullFidelity, WellDefined}]
                   [--assign-identity]
                   [--backup-interval]
                   [--backup-policy-type {Continuous, Periodic}]
                   [--backup-redundancy {Geo, Local, Zone}]
                   [--backup-retention]
                   [--capabilities]
                   [--change-reference]
                   [--continuous-tier {Continuous30Days, Continuous7Days}]
                   [--databases-to-restore]
                   [--default-consistency-level {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}]
                   [--default-identity]
                   [--default-priority-level {High, Low}]
                   [--disable-key-based-metadata-write-access {false, true}]
                   [--disable-local-auth {false, true}]
                   [--enable-analytical-storage {false, true}]
                   [--enable-automatic-failover {false, true}]
                   [--enable-burst-capacity {false, true}]
                   [--enable-free-tier {false, true}]
                   [--enable-multiple-write-locations {false, true}]
                   [--enable-partition-merge {false, true}]
                   [--enable-pbe {false, true}]
                   [--enable-prpp-autoscale {false, true}]
                   [--enable-virtual-network {false, true}]
                   [--gremlin-databases-to-restore]
                   [--ip-range-filter]
                   [--is-restore-request {false, true}]
                   [--key-uri]
                   [--kind {GlobalDocumentDB, MongoDB, Parse}]
                   [--locations]
                   [--max-interval]
                   [--max-staleness-prefix]
                   [--minimal-tls-version {Tls, Tls11, Tls12}]
                   [--network-acl-bypass {AzureServices, None}]
                   [--network-acl-bypass-resource-ids]
                   [--public-network-access {DISABLED, ENABLED, SECUREDBYPERIMETER}]
                   [--restore-source]
                   [--restore-timestamp]
                   [--server-version {3.2, 3.6, 4.0, 4.2, 5.0, 6.0, 7.0}]
                   [--tables-to-restore]
                   [--tags]
                   [--virtual-network-rules]
```
Examples
Creates a new Azure Cosmos DB database account. (autogenerated)
```
az cosmosdb create --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup --subscription MySubscription
```
Creates a new Azure Cosmos DB database account with two regions. UK South is zone redundant.
```
az cosmosdb create -n myaccount -g mygroup --locations regionName=eastus failoverPriority=0 isZoneRedundant=False --locations regionName=uksouth failoverPriority=1 isZoneRedundant=True --enable-multiple-write-locations --network-acl-bypass AzureServices --network-acl-bypass-resource-ids /subscriptions/subId/resourceGroups/rgName/providers/Microsoft.Synapse/workspaces/wsName
```
Create a new Azure Cosmos DB database account by restoring from an existing account in the given location
```
az cosmosdb create -n restoredaccount -g mygroup --is-restore-request true --restore-source /subscriptions/2296c272-5d55-40d9-bc05-4d56dc2d7588/providers/Microsoft.DocumentDB/locations/westus/restorableDatabaseAccounts/d056a4f8-044a-436f-80c8-cd3edbc94c68 --restore-timestamp 2020-07-13T16:03:41+0000 --locations regionName=westus failoverPriority=0 isZoneRedundant=False
```
Required Parameters
--name -n
Name of the Cosmos DB database account.
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
--analytical-storage-schema-type --as-schema
Schema type for analytical storage.
Property
Value
Parameter group:
Analytical Storage Configuration Arguments
Accepted values:
FullFidelity, WellDefined
--assign-identity
Assign system or user assigned identities separated by spaces. Use '[system]' to refer system assigned identity.
--backup-interval
The frequency(in minutes) with which backups are taken (only for accounts with periodic mode backups).
Property
Value
Parameter group:
Backup Policy Arguments
--backup-policy-type
The type of backup policy of the account to create.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Continuous, Periodic
--backup-redundancy
The redundancy type of the backup Storage account.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Geo, Local, Zone
--backup-retention
The time(in hours) for which each backup is retained (only for accounts with periodic mode backups).
Property
Value
Parameter group:
Backup Policy Arguments
--capabilities
Set custom capabilities on the Cosmos DB database account.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--continuous-tier
The tier of Continuous backup.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Continuous30Days, Continuous7Days
--databases-to-restore
Add a database and its collection names to restore.
Usage:          --databases-to-restore name=DatabaseName collections=collection1 [collection2 ...].
Property
Value
Parameter group:
Restore Arguments
--default-consistency-level
Default consistency level of the Cosmos DB database account.
Property
Value
Accepted values:
BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong
--default-identity
The primary identity to access key vault in CMK related features. e.g. 'FirstPartyIdentity', 'SystemAssignedIdentity' and more. User-assigned identities are specified in format
UserAssignedIdentity=<resource ID of the user-assigned identity>
.
--default-priority-level
Default Priority Level of Request if not specified.
Property
Value
Accepted values:
High, Low
--disable-key-based-metadata-write-access
Disable write operations on metadata resources (databases, containers, throughput) via account keys.
Property
Value
Accepted values:
false, true
--disable-local-auth
Disable key-based authentication on the Cosmos DB account.
Property
Value
Accepted values:
false, true
--enable-analytical-storage
Flag to enable log storage on the account.
Property
Value
Accepted values:
false, true
--enable-automatic-failover
Enables automatic failover of the write region in the rare event that the region is unavailable due to an outage. Automatic failover will result in a new write region for the account and is chosen based on the failover priorities configured for the account.
Property
Value
Accepted values:
false, true
--enable-burst-capacity
Flag to Enable/Disable burst capacity feature.
Usage:    --enable-burst-capacity true
Default:  false
The accepted values for the enable-burst-capacity are true and false.
Property
Value
Accepted values:
false, true
--enable-free-tier
Preview
If enabled the account is free-tier.
Property
Value
Accepted values:
false, true
--enable-multiple-write-locations
Enable Multiple Write Locations.
Property
Value
Accepted values:
false, true
--enable-partition-merge
Flag to enable partition merge on the account.
Property
Value
Accepted values:
false, true
--enable-pbe
Flag to enable priority based execution on the account.
Property
Value
Accepted values:
false, true
--enable-prpp-autoscale
Flag to Enable/Disable burst capacity feature.
Usage:    --enable-prpp-autoscale true
Default:  false
The accepted values for the --enable-prpp-autoscale are true and false.
Property
Value
Accepted values:
false, true
--enable-virtual-network
Enables virtual network on the Cosmos DB database account.
Property
Value
Accepted values:
false, true
--gremlin-databases-to-restore
Add a gremlin database and its graph names to restore.
Usage:          --gremlin-databases-to-restore name=DatabaseName graphs=graph1 [graph2 ...].
Property
Value
Parameter group:
Restore Arguments
--ip-range-filter
Firewall support. Specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma-separated and must not contain any spaces.
--is-restore-request -r
Restore from an existing/deleted account.
Property
Value
Parameter group:
Restore Arguments
Accepted values:
false, true
--key-uri
The URI of the key vault.
--kind
The type of Cosmos DB database account to create.
Property
Value
Default value:
GlobalDocumentDB
Accepted values:
GlobalDocumentDB, MongoDB, Parse
--locations
Add a location to the Cosmos DB database account.
Usage:          --locations KEY=VALUE [KEY=VALUE ...]
Required Keys:  regionName, failoverPriority
Optional Key:   isZoneRedundant
Default:        single region account in the location of the specified resource group.
Failover priority values are 0 for write regions and greater than 0 for read regions. A failover priority value must be unique and less than the total number of regions.
Multiple locations can be specified by using more than one
--locations
argument.
--max-interval
When used with Bounded Staleness consistency, this value represents the time amount of staleness (in seconds) tolerated. Accepted range for this value is 5 - 86400.
Property
Value
Default value:
5
--max-staleness-prefix
When used with Bounded Staleness consistency, this value represents the number of stale requests tolerated. Accepted range for this value is 10 - 2,147,483,647.
Property
Value
Default value:
100
--minimal-tls-version
Indicate the minimum allowed TLS version.
Usage:    --minimal-tls-version TLSVersion
Default:  Tls, except for Cassandra and Mongo APIs, which only work with Tls12
The accepted values for the minimal TLS version are 'Tls', 'Tls11', and 'Tls12', which correspond to the
TLS versions 1.0, 1.1, and 1.2.
Property
Value
Accepted values:
Tls, Tls11, Tls12
--network-acl-bypass
Flag to enable or disable Network Acl Bypass.
Property
Value
Accepted values:
AzureServices, None
--network-acl-bypass-resource-ids -i
List of Resource Ids to allow Network Acl Bypass.
--public-network-access -p
Sets public network access in server to either Enabled, Disabled, or SecuredByPerimeter.
Property
Value
Accepted values:
DISABLED, ENABLED, SECUREDBYPERIMETER
--restore-source
The restorable-database-account Id of the source account from which the account has to be restored. Required if --is-restore-request is set to true.
Property
Value
Parameter group:
Restore Arguments
--restore-timestamp
The timestamp to which the account has to be restored to. Required if --is-restore-request is set to true.
Property
Value
Parameter group:
Restore Arguments
--server-version
Valid only for MongoDB accounts.
Property
Value
Accepted values:
3.2, 3.6, 4.0, 4.2, 5.0, 6.0, 7.0
--tables-to-restore
Add table names to restore.
Usage:          --tables-to-restore tables=table1 [table2 ...].
Property
Value
Parameter group:
Restore Arguments
--tags
Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags.
--virtual-network-rules
ACL's for virtual network.
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
az cosmosdb create (cosmosdb-preview extension)
Preview
Creates a new Azure Cosmos DB database account.
```
az cosmosdb create --name
                   --resource-group
                   [--acquire-policy-token]
                   [--analytical-storage-schema-type --as-schema {FullFidelity, WellDefined}]
                   [--assign-identity]
                   [--backup-interval]
                   [--backup-policy-type {Continuous, Periodic}]
                   [--backup-redundancy {Geo, Local, Zone}]
                   [--backup-retention]
                   [--capabilities]
                   [--capacity-mode {None, Provisioned, Serverless}]
                   [--change-reference]
                   [--continuous-tier {Continuous30Days, Continuous7Days}]
                   [--databases-to-restore]
                   [--default-consistency-level {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}]
                   [--default-identity]
                   [--default-priority-level {High, Low}]
                   [--disable-key-based-metadata-write-access {false, true}]
                   [--enable-analytical-storage {false, true}]
                   [--enable-automatic-failover {false, true}]
                   [--enable-burst-capacity {false, true}]
                   [--enable-free-tier {false, true}]
                   [--enable-materialized-views --enable-mv {false, true}]
                   [--enable-multiple-write-locations {false, true}]
                   [--enable-partition-merge {false, true}]
                   [--enable-pbe --enable-priority-based-execution {false, true}]
                   [--enable-prpp-autoscale {false, true}]
                   [--enable-virtual-network {false, true}]
                   [--gremlin-databases-to-restore]
                   [--ip-range-filter]
                   [--is-restore-request {false, true}]
                   [--key-uri]
                   [--kind {GlobalDocumentDB, MongoDB, Parse}]
                   [--locations]
                   [--max-interval]
                   [--max-staleness-prefix]
                   [--network-acl-bypass {AzureServices, None}]
                   [--network-acl-bypass-resource-ids]
                   [--public-network-access {DISABLED, ENABLED, SECUREDBYPERIMETER}]
                   [--restore-source]
                   [--restore-timestamp]
                   [--server-version {3.2, 3.6, 4.0, 4.2, 5.0, 6.0, 7.0}]
                   [--tables-to-restore]
                   [--tags]
                   [--virtual-network-rules]
```
Examples
DB database account. (autogenerated)
```
az cosmosdb create --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup --subscription MySubscription
```
Creates a new Azure Cosmos DB database account with two regions. UK South is zone redundant.
```
az cosmosdb create -n myaccount -g mygroup --locations regionName=eastus failoverPriority=0 isZoneRedundant=False --locations regionName=uksouth failoverPriority=1 isZoneRedundant=True --enable-multiple-write-locations --network-acl-bypass AzureServices --network-acl-bypass-resource-ids /subscriptions/subId/resourceGroups/rgName/providers/Microsoft.Synapse/workspaces/wsName
```
Create a new Azure Cosmos DB database account by restoring from an existing account in the given location
```
az cosmosdb create -n restoredaccount -g mygroup --is-restore-request true --restore-source /subscriptions/2296c272-5d55-40d9-bc05-4d56dc2d7588/providers/Microsoft.DocumentDB/locations/westus/restorableDatabaseAccounts/d056a4f8-044a-436f-80c8-cd3edbc94c68 --restore-timestamp 2020-07-13T16:03:41+0000 --locations regionName=westus failoverPriority=0 isZoneRedundant=False
```
Creates a new Azure Cosmos DB database account with materialized views and cassandra capability enabled.
```
az cosmosdb create --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup --enable-materialized-views true --capabilities EnableCassandra CassandraEnableMaterializedViews
```
Required Parameters
--name -n
Name of the Cosmos DB database account.
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
--analytical-storage-schema-type --as-schema
Schema type for analytical storage.
Property
Value
Parameter group:
Analytical Storage Configuration Arguments
Accepted values:
FullFidelity, WellDefined
--assign-identity
Assign system or user assigned identities separated by spaces. Use '[system]' to refer system assigned identity.
--backup-interval
The frequency(in minutes) with which backups are taken (only for accounts with periodic mode backups).
Property
Value
Parameter group:
Backup Policy Arguments
--backup-policy-type
The type of backup policy of the account to create.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Continuous, Periodic
--backup-redundancy
The redundancy type of the backup Storage account.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Geo, Local, Zone
--backup-retention
The time(in hours) for which each backup is retained (only for accounts with periodic mode backups).
Property
Value
Parameter group:
Backup Policy Arguments
--capabilities
Set custom capabilities on the Cosmos DB database account.
--capacity-mode
Preview
CapacityMode of the account.
Property
Value
Accepted values:
None, Provisioned, Serverless
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--continuous-tier
The tier of Continuous backup.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Continuous30Days, Continuous7Days
--databases-to-restore
Preview
Add a database and its collection names to restore.
Usage:          --databases-to-restore name=DatabaseName collections=collection1 [collection2 ...].
Property
Value
Parameter group:
Restore Arguments
--default-consistency-level
Default consistency level of the Cosmos DB database account.
Property
Value
Accepted values:
BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong
--default-identity
The primary identity to access key vault in CMK related features. e.g. 'FirstPartyIdentity', 'SystemAssignedIdentity' and more.
--default-priority-level
Preview
Default Priority Level of Request if not specified.
Property
Value
Accepted values:
High, Low
--disable-key-based-metadata-write-access
Disable write operations on metadata resources (databases, containers, throughput) via account keys.
Property
Value
Accepted values:
false, true
--enable-analytical-storage
Flag to enable log storage on the account.
Property
Value
Accepted values:
false, true
--enable-automatic-failover
Enables automatic failover of the write region in the rare event that the region is unavailable due to an outage. Automatic failover will result in a new write region for the account and is chosen based on the failover priorities configured for the account.
Property
Value
Accepted values:
false, true
--enable-burst-capacity
Preview
Flag to enable burst capacity on the account.
Property
Value
Accepted values:
false, true
--enable-free-tier
Preview
If enabled the account is free-tier.
Property
Value
Accepted values:
false, true
--enable-materialized-views --enable-mv
Preview
Flag to enable MaterializedViews on the account.
Property
Value
Accepted values:
false, true
--enable-multiple-write-locations
Enable Multiple Write Locations.
Property
Value
Accepted values:
false, true
--enable-partition-merge
Flag to enable partition merge on the account.
Property
Value
Accepted values:
false, true
--enable-pbe --enable-priority-based-execution
Preview
Flag to enable priority based execution on the account.
Property
Value
Accepted values:
false, true
--enable-prpp-autoscale
Preview
Enable or disable PerRegionPerPartitionAutoscale.
Property
Value
Accepted values:
false, true
--enable-virtual-network
Enables virtual network on the Cosmos DB database account.
Property
Value
Accepted values:
false, true
--gremlin-databases-to-restore
Preview
Add a gremlin database and its graph names to restore.
Usage:          --gremlin-databases-to-restore name=DatabaseName graphs=graph1 [graph2 ...].
Property
Value
Parameter group:
Restore Arguments
--ip-range-filter
Firewall support. Specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma-separated and must not contain any spaces.
--is-restore-request -r
Preview
Restore from an existing/deleted account.
Property
Value
Parameter group:
Restore Arguments
Accepted values:
false, true
--key-uri
The URI of the key vault.
--kind
The type of Cosmos DB database account to create.
Property
Value
Default value:
GlobalDocumentDB
Accepted values:
GlobalDocumentDB, MongoDB, Parse
--locations
Add a location to the Cosmos DB database account.
Usage:          --locations KEY=VALUE [KEY=VALUE ...]
Required Keys:  regionName, failoverPriority
Optional Key:   isZoneRedundant
Default:        single region account in the location of the specified resource group.
Failover priority values are 0 for write regions and greater than 0 for read regions. A failover priority value must be unique and less than the total number of regions.
Multiple locations can be specified by using more than one
--locations
argument.
--max-interval
When used with Bounded Staleness consistency, this value represents the time amount of staleness (in seconds) tolerated. Accepted range for this value is 1 - 100.
Property
Value
Default value:
5
--max-staleness-prefix
When used with Bounded Staleness consistency, this value represents the number of stale requests tolerated. Accepted range for this value is 1 - 2,147,483,647.
Property
Value
Default value:
100
--network-acl-bypass
Flag to enable or disable Network Acl Bypass.
Property
Value
Accepted values:
AzureServices, None
--network-acl-bypass-resource-ids -i
List of Resource Ids to allow Network Acl Bypass.
--public-network-access -p
Sets public network access in server to either Enabled, Disabled, or SecuredByPerimeter.
Property
Value
Accepted values:
DISABLED, ENABLED, SECUREDBYPERIMETER
--restore-source
Preview
The restorable-database-account Id of the source account from which the account has to be restored. Required if --is-restore-request is set to true.
Property
Value
Parameter group:
Restore Arguments
--restore-timestamp
Preview
The timestamp to which the account has to be restored to. Required if --is-restore-request is set to true.
Property
Value
Parameter group:
Restore Arguments
--server-version
Valid only for MongoDB accounts.
Property
Value
Accepted values:
3.2, 3.6, 4.0, 4.2, 5.0, 6.0, 7.0
--tables-to-restore
Preview
Add table names to restore.
Usage:          --tables-to-restore tables=table1 [table2 ...].
Property
Value
Parameter group:
Restore Arguments
--tags
Space-separated tags: key[=value] [key[=value] ...]. Use "" to clear existing tags.
--virtual-network-rules
ACL's for virtual network.
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
az cosmosdb delete
Edit
Deletes an Azure Cosmos DB database account.
```
az cosmosdb delete [--acquire-policy-token]
                   [--change-reference]
                   [--ids]
                   [--name]
                   [--no-wait]
                   [--resource-group]
                   [--subscription]
                   [--yes]
```
Examples
Deletes an Azure Cosmos DB database account. (autogenerated)
```
az cosmosdb delete --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup
```
an Azure Cosmos DB database account without waiting for the long-running operation to finish.
```
az cosmosdb delete --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup --no-wait
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
Name of the Cosmos DB database account.
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
az cosmosdb failover-priority-change
Edit
Changes the failover priority for the Azure Cosmos DB database account.
```
az cosmosdb failover-priority-change --failover-policies
                                     [--acquire-policy-token]
                                     [--change-reference]
                                     [--ids]
                                     [--name]
                                     [--resource-group]
                                     [--subscription]
```
Examples
Changes the failover priority for the Azure Cosmos DB database account.
```
az cosmosdb failover-priority-change --failover-policies southafricanorth=0 westus=8 northeurope=3 --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup
```
Required Parameters
--failover-policies
Space-separated failover policies in 'regionName=failoverPriority' format. Number of policies must match the number of regions the account is currently replicated. All regionName values must match those of the regions the account is currently replicated. All failoverPriority values must be unique. There must be one failoverPriority value zero (0) specified. All remaining failoverPriority values can be any positive integer and they don't have to be contiguos, neither written in any specific order. E.g eastus=0 westus=1.
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
Name of the Cosmos DB database account.
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
az cosmosdb list
Edit
List Azure Cosmos DB database accounts.
```
az cosmosdb list [--resource-group]
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
az cosmosdb list (cosmosdb-preview extension)
List Azure Cosmos DB database accounts.
```
az cosmosdb list [--resource-group]
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
az cosmosdb offline-region
Edit
Offline the specified region for the specified Azure Cosmos DB database account.
```
az cosmosdb offline-region --region
                           [--acquire-policy-token]
                           [--change-reference]
                           [--ids]
                           [--name]
                           [--resource-group]
                           [--subscription]
```
Examples
Offlines North Europe regional account for the Azure Cosmos DB database account MyCosmosDBDatabaseAccount.
```
az cosmosdb offline-region --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup --region NorthEurope
```
Required Parameters
--region
The region to offline for the CosmosDB account.
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
Name of the Cosmos DB database account.
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
az cosmosdb restore
Edit
Create a new Azure Cosmos DB database account by restoring from an existing database account.
```
az cosmosdb restore --account-name
                    --location
                    --resource-group
                    --restore-timestamp
                    --target-database-account-name
                    [--acquire-policy-token]
                    [--assign-identity]
                    [--change-reference]
                    [--databases-to-restore]
                    [--default-identity]
                    [--disable-ttl {false, true}]
                    [--gremlin-databases-to-restore]
                    [--public-network-access {DISABLED, ENABLED}]
                    [--source-backup-location]
                    [--tables-to-restore]
```
Examples
Create a new Azure Cosmos DB database account by restoring from an existing database account.
```
az cosmosdb restore --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 -g MyResourceGroup --location westus
```
Create a new Azure Cosmos DB Sql or MongoDB database account by restoring only the selected databases and collections from an existing database account.
```
az cosmosdb restore -g MyResourceGroup --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 --location westus --databases-to-restore name=MyDB1 collections=collection1 collection2 --databases-to-restore name=MyDB2 collections=collection3 collection4
```
Create a new Azure Cosmos DB Gremlin database account by restoring only the selected databases or graphs from an existing database account.
```
az cosmosdb restore -g MyResourceGroup --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 --location westus --gremlin-databases-to-restore name=graphdb1 graphs=graph1 graph2
```
Create a new Azure Cosmos DB Table database account by restoring only the selected tables from an existing database account.
```
az cosmosdb restore -g MyResourceGroup --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 --location westus --tables-to-restore table1,table2
```
Create a new Azure Cosmos DB Table database account by restoring with Time-To-Live disabled.
```
az cosmosdb restore -g MyResourceGroup --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 --location westus --disable-ttl True
```
Required Parameters
--account-name -a
Name of the source Cosmos DB database account for the restore.
--location -l
This is the write region of the restored account. This is also the location of the source account where its backups are located if source_backup_location is not provided.
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
--restore-timestamp -t
The timestamp to which the account has to be restored to.
--target-database-account-name -n
Name of the new target Cosmos DB database account after the restore.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--assign-identity
Assign system or user assigned identities separated by spaces. Use '[system]' to refer system assigned identity.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--databases-to-restore
Add a database and its collection names to restore.
Usage:          --databases-to-restore name=DatabaseName collections=collection1 [collection2 ...]
Multiple databases can be specified by using more than one
--databases-to-restore
argument.
--default-identity
The primary identity to access key vault in CMK related features. e.g. 'FirstPartyIdentity', 'SystemAssignedIdentity' and more.
--disable-ttl -d
Enable or disable restoring with ttl disabled.
Property
Value
Accepted values:
false, true
--gremlin-databases-to-restore
Add a gremlin database and its graph names to restore.
Usage:          --gremlin-databases-to-restore name=DatabaseName graphs=graph1 [graph2 ...].
--public-network-access -p
Sets public network access in server to either Enabled or Disabled.
Property
Value
Accepted values:
DISABLED, ENABLED
--source-backup-location
This is the location of the source account where backups are located. Provide this value if the source and target are in different locations.
--tables-to-restore
Add table names to restore.
Usage:          --tables-to-restore table1 [table2 ...].
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
az cosmosdb restore (cosmosdb-preview extension)
Preview
Create a new Azure Cosmos DB database account by restoring from an existing database account.
```
az cosmosdb restore --account-name
                    --location
                    --resource-group
                    --restore-timestamp
                    --target-database-account-name
                    [--acquire-policy-token]
                    [--assign-identity]
                    [--change-reference]
                    [--databases-to-restore]
                    [--default-identity]
                    [--disable-ttl {false, true}]
                    [--gremlin-databases-to-restore]
                    [--public-network-access {DISABLED, ENABLED}]
                    [--source-backup-location]
                    [--tables-to-restore]
```
Examples
Create a new Azure Cosmos DB database account by restoring from an existing database account.
```
az cosmosdb restore --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 -g MyResourceGroup --location westus
```
Create a new Azure Cosmos DB Sql or MongoDB database account by restoring only the selected databases and collections from an existing database account.
```
az cosmosdb restore -g MyResourceGroup --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 --location westus --databases-to-restore name=MyDB1 collections=collection1 collection2 --databases-to-restore name=MyDB2 collections=collection3 collection4
```
Create a new Azure Cosmos DB Gremlin database account by restoring only the selected databases or graphs from an existing database account.
```
az cosmosdb restore -g MyResourceGroup --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 --location westus --gremlin-databases-to-restore name=graphdb1 graphs=graph1 graph2
```
Create a new Azure Cosmos DB Table database account by restoring only the selected tables from an existing database account.
```
az cosmosdb restore -g MyResourceGroup --target-database-account-name MyRestoredCosmosDBDatabaseAccount --account-name MySourceAccount --restore-timestamp 2020-07-13T16:03:41+0000 --location westus --tables-to-restore table1,table2
```
Required Parameters
--account-name -a
Name of the source Cosmos DB database account for the restore.
--location -l
This is the write region of the restored account. This is also the location of the source account where its backups are located if source_backup_location is not provided.
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
--restore-timestamp -t
The timestamp to which the account has to be restored to.
--target-database-account-name -n
Name of the new target Cosmos DB database account after the restore.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--assign-identity
Assign system or user assigned identities separated by spaces. Use '[system]' to refer system assigned identity.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--databases-to-restore
Add a database and its collection names to restore.
Usage:          --databases-to-restore name=DatabaseName collections=collection1 [collection2 ...]
Multiple databases can be specified by using more than one
--databases-to-restore
argument.
--default-identity
The primary identity to access key vault in CMK related features. e.g. 'FirstPartyIdentity', 'SystemAssignedIdentity' and more.
--disable-ttl
Preview
Enable or disable restoring with ttl disabled.
Property
Value
Accepted values:
false, true
--gremlin-databases-to-restore
Preview
Add a gremlin database and its graph names to restore.
Usage:          --gremlin-databases-to-restore name=DatabaseName graphs=graph1 [graph2 ...].
--public-network-access -p
Sets public network access in server to either Enabled or Disabled.
Property
Value
Accepted values:
DISABLED, ENABLED
--source-backup-location
Preview
This is the location of the source account where backups are located. Provide this value if the source and target are in different locations.
--tables-to-restore
Preview
Add table names to restore.
Usage:          --tables-to-restore table1 [table2 ...].
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
az cosmosdb show
Edit
Get the details of an Azure Cosmos DB database account.
```
az cosmosdb show [--ids]
                 [--name]
                 [--resource-group]
                 [--subscription]
```
Examples
Get the details of an Azure Cosmos DB database account. (autogenerated)
```
az cosmosdb show --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup
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
Name of the Cosmos DB database account.
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
az cosmosdb show (cosmosdb-preview extension)
Get the details of an Azure Cosmos DB database account.
```
az cosmosdb show [--ids]
                 [--name]
                 [--resource-group]
                 [--subscription]
```
Examples
Get the details of an Azure Cosmos DB database account. (autogenerated)
```
az cosmosdb show --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup
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
Name of the Cosmos DB database account.
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
az cosmosdb update
Edit
Update an Azure Cosmos DB database account.
```
az cosmosdb update [--acquire-policy-token]
                   [--analytical-storage-schema-type --as-schema {FullFidelity, WellDefined}]
                   [--backup-interval]
                   [--backup-policy-type {Continuous, Periodic}]
                   [--backup-redundancy {Geo, Local, Zone}]
                   [--backup-retention]
                   [--capabilities]
                   [--change-reference]
                   [--continuous-tier {Continuous30Days, Continuous7Days}]
                   [--default-consistency-level {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}]
                   [--default-identity]
                   [--default-priority-level {High, Low}]
                   [--disable-key-based-metadata-write-access {false, true}]
                   [--disable-local-auth {false, true}]
                   [--enable-analytical-storage {false, true}]
                   [--enable-automatic-failover {false, true}]
                   [--enable-burst-capacity {false, true}]
                   [--enable-multiple-write-locations {false, true}]
                   [--enable-partition-merge {false, true}]
                   [--enable-pbe {false, true}]
                   [--enable-prpp-autoscale {false, true}]
                   [--enable-virtual-network {false, true}]
                   [--ids]
                   [--ip-range-filter]
                   [--key-uri]
                   [--locations]
                   [--max-interval]
                   [--max-staleness-prefix]
                   [--minimal-tls-version {Tls, Tls11, Tls12}]
                   [--name]
                   [--network-acl-bypass {AzureServices, None}]
                   [--network-acl-bypass-resource-ids]
                   [--public-network-access {DISABLED, ENABLED, SECUREDBYPERIMETER}]
                   [--resource-group]
                   [--server-version {3.2, 3.6, 4.0, 4.2, 5.0, 6.0, 7.0}]
                   [--subscription]
                   [--tags]
                   [--virtual-network-rules]
```
Examples
Update an Azure Cosmos DB database account. (autogenerated)
```
az cosmosdb update --capabilities EnableGremlin --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup
```
Creates a new Azure Cosmos DB database account with two regions. UK South is zone redundant.
```
az cosmosdb update -n myaccount -g mygroup --locations regionName=eastus failoverPriority=0 isZoneRedundant=False --locations regionName=uksouth failoverPriority=1 isZoneRedundant=True --enable-multiple-write-locations --network-acl-bypass AzureServices --network-acl-bypass-resource-ids /subscriptions/subId/resourceGroups/rgName/providers/Microsoft.Synapse/workspaces/wsName
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--analytical-storage-schema-type --as-schema
Schema type for analytical storage.
Property
Value
Parameter group:
Analytical Storage Configuration Arguments
Accepted values:
FullFidelity, WellDefined
--backup-interval
The frequency(in minutes) with which backups are taken (only for accounts with periodic mode backups).
Property
Value
Parameter group:
Backup Policy Arguments
--backup-policy-type
The type of backup policy of the account to create.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Continuous, Periodic
--backup-redundancy
The redundancy type of the backup Storage account.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Geo, Local, Zone
--backup-retention
The time(in hours) for which each backup is retained (only for accounts with periodic mode backups).
Property
Value
Parameter group:
Backup Policy Arguments
--capabilities
Set custom capabilities on the Cosmos DB database account.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--continuous-tier
The tier of Continuous backup.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Continuous30Days, Continuous7Days
--default-consistency-level
Default consistency level of the Cosmos DB database account.
Property
Value
Accepted values:
BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong
--default-identity
The primary identity to access key vault in CMK related features. e.g. 'FirstPartyIdentity', 'SystemAssignedIdentity' and more. User-assigned identities are specified in format
UserAssignedIdentity=<resource ID of the user-assigned identity>
.
--default-priority-level
Default Priority Level of Request if not specified.
Property
Value
Accepted values:
High, Low
--disable-key-based-metadata-write-access
Disable write operations on metadata resources (databases, containers, throughput) via account keys.
Property
Value
Accepted values:
false, true
--disable-local-auth
Disable key-based authentication on the Cosmos DB account.
Property
Value
Accepted values:
false, true
--enable-analytical-storage
Flag to enable log storage on the account.
Property
Value
Accepted values:
false, true
--enable-automatic-failover
Enables automatic failover of the write region in the rare event that the region is unavailable due to an outage. Automatic failover will result in a new write region for the account and is chosen based on the failover priorities configured for the account.
Property
Value
Accepted values:
false, true
--enable-burst-capacity
Flag to Enable/Disable burst capacity feature.
Usage:    --enable-burst-capacity true
Default:  false
The accepted values for the enable-burst-capacity are true and false.
Property
Value
Accepted values:
false, true
--enable-multiple-write-locations
Enable Multiple Write Locations.
Property
Value
Accepted values:
false, true
--enable-partition-merge
Flag to enable partition merge on the account.
Property
Value
Accepted values:
false, true
--enable-pbe
Flag to enable priority based execution on the account.
Property
Value
Accepted values:
false, true
--enable-prpp-autoscale
Flag to Enable/Disable burst capacity feature.
Usage:    --enable-prpp-autoscale true
Default:  false
The accepted values for the --enable-prpp-autoscale are true and false.
Property
Value
Accepted values:
false, true
--enable-virtual-network
Enables virtual network on the Cosmos DB database account.
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
--ip-range-filter
Firewall support. Specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma-separated and must not contain any spaces.
--key-uri
Preview
The URI of the key vault.
--locations
Add a location to the Cosmos DB database account.
Usage:          --locations KEY=VALUE [KEY=VALUE ...]
Required Keys:  regionName, failoverPriority
Optional Key:   isZoneRedundant
Default:        single region account in the location of the specified resource group.
Failover priority values are 0 for write regions and greater than 0 for read regions. A failover priority value must be unique and less than the total number of regions.
Multiple locations can be specified by using more than one
--locations
argument.
--max-interval
When used with Bounded Staleness consistency, this value represents the time amount of staleness (in seconds) tolerated. Accepted range for this value is 5 - 86400.
--max-staleness-prefix
When used with Bounded Staleness consistency, this value represents the number of stale requests tolerated. Accepted range for this value is 10 - 2,147,483,647.
--minimal-tls-version
Indicate the minimum allowed TLS version.
Usage:    --minimal-tls-version TLSVersion
Default:  Tls, except for Cassandra and Mongo APIs, which only work with Tls12
The accepted values for the minimal TLS version are 'Tls', 'Tls11', and 'Tls12', which correspond to the
TLS versions 1.0, 1.1, and 1.2.
Property
Value
Accepted values:
Tls, Tls11, Tls12
--name -n
Name of the Cosmos DB database account.
Property
Value
Parameter group:
Resource Id Arguments
--network-acl-bypass
Flag to enable or disable Network Acl Bypass.
Property
Value
Accepted values:
AzureServices, None
--network-acl-bypass-resource-ids -i
List of Resource Ids to allow Network Acl Bypass.
--public-network-access -p
Sets public network access in server to either Enabled, Disabled, or SecuredByPerimeter.
Property
Value
Accepted values:
DISABLED, ENABLED, SECUREDBYPERIMETER
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--server-version
Valid only for MongoDB accounts.
Property
Value
Accepted values:
3.2, 3.6, 4.0, 4.2, 5.0, 6.0, 7.0
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
--virtual-network-rules
ACL's for virtual network.
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
az cosmosdb update (cosmosdb-preview extension)
Update an Azure Cosmos DB database account.
```
az cosmosdb update [--acquire-policy-token]
                   [--analytical-storage-schema-type --as-schema {FullFidelity, WellDefined}]
                   [--backup-interval]
                   [--backup-policy-type {Continuous, Periodic}]
                   [--backup-redundancy {Geo, Local, Zone}]
                   [--backup-retention]
                   [--capabilities]
                   [--capacity-mode {None, Provisioned, Serverless}]
                   [--change-reference]
                   [--continuous-tier {Continuous30Days, Continuous7Days}]
                   [--default-consistency-level {BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong}]
                   [--default-identity]
                   [--default-priority-level {High, Low}]
                   [--disable-key-based-metadata-write-access {false, true}]
                   [--enable-analytical-storage {false, true}]
                   [--enable-automatic-failover {false, true}]
                   [--enable-burst-capacity {false, true}]
                   [--enable-materialized-views --enable-mv {false, true}]
                   [--enable-multiple-write-locations {false, true}]
                   [--enable-partition-merge {false, true}]
                   [--enable-pbe --enable-priority-based-execution {false, true}]
                   [--enable-prpp-autoscale {false, true}]
                   [--enable-virtual-network {false, true}]
                   [--ids]
                   [--ip-range-filter]
                   [--locations]
                   [--max-interval]
                   [--max-staleness-prefix]
                   [--name]
                   [--network-acl-bypass {AzureServices, None}]
                   [--network-acl-bypass-resource-ids]
                   [--public-network-access {DISABLED, ENABLED, SECUREDBYPERIMETER}]
                   [--resource-group]
                   [--server-version {3.2, 3.6, 4.0, 4.2, 5.0, 6.0, 7.0}]
                   [--subscription]
                   [--tags]
                   [--virtual-network-rules]
```
Examples
Update an Azure Cosmos DB database account. (autogenerated)
```
az cosmosdb update --capabilities EnableGremlin --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup
```
Update an Azure Cosmos DB database account to enable materialized views.
```
az cosmosdb update --name MyCosmosDBDatabaseAccount --resource-group MyResourceGroup --enable-materialized-views true
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--analytical-storage-schema-type --as-schema
Schema type for analytical storage.
Property
Value
Parameter group:
Analytical Storage Configuration Arguments
Accepted values:
FullFidelity, WellDefined
--backup-interval
The frequency(in minutes) with which backups are taken (only for accounts with periodic mode backups).
Property
Value
Parameter group:
Backup Policy Arguments
--backup-policy-type
The type of backup policy of the account to create.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Continuous, Periodic
--backup-redundancy
The redundancy type of the backup Storage account.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Geo, Local, Zone
--backup-retention
The time(in hours) for which each backup is retained (only for accounts with periodic mode backups).
Property
Value
Parameter group:
Backup Policy Arguments
--capabilities
Set custom capabilities on the Cosmos DB database account.
--capacity-mode
Preview
CapacityMode of the account.
Property
Value
Accepted values:
None, Provisioned, Serverless
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--continuous-tier
The tier of Continuous backup.
Property
Value
Parameter group:
Backup Policy Arguments
Accepted values:
Continuous30Days, Continuous7Days
--default-consistency-level
Default consistency level of the Cosmos DB database account.
Property
Value
Accepted values:
BoundedStaleness, ConsistentPrefix, Eventual, Session, Strong
--default-identity
The primary identity to access key vault in CMK related features. e.g. 'FirstPartyIdentity', 'SystemAssignedIdentity' and more.
--default-priority-level
Preview
Default Priority Level of Request if not specified.
Property
Value
Accepted values:
High, Low
--disable-key-based-metadata-write-access
Disable write operations on metadata resources (databases, containers, throughput) via account keys.
Property
Value
Accepted values:
false, true
--enable-analytical-storage
Flag to enable log storage on the account.
Property
Value
Accepted values:
false, true
--enable-automatic-failover
Enables automatic failover of the write region in the rare event that the region is unavailable due to an outage. Automatic failover will result in a new write region for the account and is chosen based on the failover priorities configured for the account.
Property
Value
Accepted values:
false, true
--enable-burst-capacity
Preview
Flag to enable burst capacity on the account.
Property
Value
Accepted values:
false, true
--enable-materialized-views --enable-mv
Preview
Flag to enable MaterializedViews on the account.
Property
Value
Accepted values:
false, true
--enable-multiple-write-locations
Enable Multiple Write Locations.
Property
Value
Accepted values:
false, true
--enable-partition-merge
Flag to enable partition merge on the account.
Property
Value
Accepted values:
false, true
--enable-pbe --enable-priority-based-execution
Preview
Flag to enable priority based execution on the account.
Property
Value
Accepted values:
false, true
--enable-prpp-autoscale
Preview
Enable or disable PerRegionPerPartitionAutoscale.
Property
Value
Accepted values:
false, true
--enable-virtual-network
Enables virtual network on the Cosmos DB database account.
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
--ip-range-filter
Firewall support. Specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma-separated and must not contain any spaces.
--locations
Add a location to the Cosmos DB database account.
Usage:          --locations KEY=VALUE [KEY=VALUE ...]
Required Keys:  regionName, failoverPriority
Optional Key:   isZoneRedundant
Default:        single region account in the location of the specified resource group.
Failover priority values are 0 for write regions and greater than 0 for read regions. A failover priority value must be unique and less than the total number of regions.
Multiple locations can be specified by using more than one
--locations
argument.
--max-interval
When used with Bounded Staleness consistency, this value represents the time amount of staleness (in seconds) tolerated. Accepted range for this value is 1 - 100.
--max-staleness-prefix
When used with Bounded Staleness consistency, this value represents the number of stale requests tolerated. Accepted range for this value is 1 - 2,147,483,647.
--name -n
Name of the Cosmos DB database account.
Property
Value
Parameter group:
Resource Id Arguments
--network-acl-bypass
Flag to enable or disable Network Acl Bypass.
Property
Value
Accepted values:
AzureServices, None
--network-acl-bypass-resource-ids -i
List of Resource Ids to allow Network Acl Bypass.
--public-network-access -p
Sets public network access in server to either Enabled, Disabled, or SecuredByPerimeter.
Property
Value
Accepted values:
DISABLED, ENABLED, SECUREDBYPERIMETER
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
Property
Value
Parameter group:
Resource Id Arguments
--server-version
Valid only for MongoDB accounts.
Property
Value
Accepted values:
3.2, 3.6, 4.0, 4.2, 5.0, 6.0, 7.0
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
--virtual-network-rules
ACL's for virtual network.
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