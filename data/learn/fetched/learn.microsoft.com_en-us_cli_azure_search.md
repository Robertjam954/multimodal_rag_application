<!-- source: https://learn.microsoft.com/en-us/cli/azure/search?view=azure-cli-latest -->

# az search

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
az search
Manage Azure AI Search.
Commands
Name
Description
Type
Status
az search admin-key
Manage Azure AI Search admin keys.
Core
GA
az search admin-key renew
Regenerates either the primary or secondary admin API key.
Core
GA
az search admin-key show
Gets the primary and secondary admin API keys for the specified Azure AI Search service.
Core
GA
az search offering
Manage Azure AI Search offerings.
Core
GA
az search offering list
List all Azure AI Search offerings by region.
Core
GA
az search private-endpoint-connection
Manage Azure AI Search private endpoint connections.
Core
GA
az search private-endpoint-connection delete
Disconnects the private endpoint connection and deletes it from the search service.
Core
GA
az search private-endpoint-connection list
Gets a list of all private endpoint connections in the given service.
Core
GA
az search private-endpoint-connection show
Gets the details of the private endpoint connection to the search service in the given resource group.
Core
GA
az search private-endpoint-connection update
Update an existing private endpoint connection in a Search service in the given resource group.
Core
GA
az search private-link-resource
Manage Azure AI Search private link resources.
Core
GA
az search private-link-resource list
Gets a list of all supported private link resource types for the given service.
Core
GA
az search query-key
Manage Azure AI Search query keys.
Core
GA
az search query-key create
Generates a new query key for the specified search service.
Core
GA
az search query-key delete
Deletes the specified query key.
Core
GA
az search query-key list
Returns the list of query API keys for the given Azure AI Search service.
Core
GA
az search service
Manage Service.
Core
GA
az search service admin-key
Manage Admin Key.
Core
GA
az search service admin-key list
Gets the primary and secondary admin API keys for the specified Azure AI Search service.
Core
GA
az search service admin-key regenerate
Regenerates either the primary or secondary admin API key. You can only regenerate one key at a time.
Core
GA
az search service check-name-availability
Checks whether or not the given search service name is available for use. Search service names must be globally unique since they are part of the service URI (https://
<name>
.search.windows.net).
Core
GA
az search service create
Creates or updates a search service in the given resource group. If the search service already exists, all properties will be updated with the given values.
Core
GA
az search service delete
Delete a search service in the given resource group, along with its associated resources.
Core
GA
az search service list
Gets a list of all Search services in the given resource group.
Core
GA
az search service network-security-perimeter-configuration
Manage Network Security Perimeter Configuration.
Core
GA
az search service network-security-perimeter-configuration list
List a list of network security perimeter configurations for a search service.
Core
GA
az search service network-security-perimeter-configuration reconcile
Reconcile network security perimeter configuration for the Azure AI Search resource provider. This triggers a manual resync with network security perimeter configurations by ensuring the search service carries the latest configuration.
Core
GA
az search service network-security-perimeter-configuration show
Get a network security perimeter configuration.
Core
GA
az search service private-endpoint-connection
Manage Private Endpoint Connection.
Core
GA
az search service private-endpoint-connection delete
Delete the private endpoint connection and deletes it from the search service.
Core
GA
az search service private-endpoint-connection list
List a list of all private endpoint connections in the given service.
Core
GA
az search service private-endpoint-connection show
Get the details of the private endpoint connection to the search service in the given resource group.
Core
GA
az search service private-endpoint-connection update
Update a private endpoint connection to the search service in the given resource group.
Core
GA
az search service private-link-resource
Manage Private Link Resource.
Core
GA
az search service private-link-resource list
List a list of all supported private link resource types for the given service.
Core
GA
az search service query-key
Manage Create Query Key.
Core
GA
az search service query-key create
Create a new query key for the specified search service. You can create up to 50 query keys per service.
Core
GA
az search service query-key delete
Delete the specified query key. Unlike admin keys, query keys are not regenerated. The process for regenerating a query key is to delete and then recreate it.
Core
GA
az search service query-key list
Returns the list of query API keys for the given Azure AI Search service.
Core
GA
az search service shared-private-link-resource
Manage Shared Private Link Resource.
Core
GA
az search service shared-private-link-resource create
Create the creation or update of a shared private link resource managed by the search service in the given resource group.
Core
GA
az search service shared-private-link-resource delete
Delete the deletion of the shared private link resource from the search service.
Core
GA
az search service shared-private-link-resource list
List a list of all shared private link resources managed by the given service.
Core
GA
az search service shared-private-link-resource show
Get the details of the shared private link resource managed by the search service in the given resource group.
Core
GA
az search service shared-private-link-resource update
Update the creation or update of a shared private link resource managed by the search service in the given resource group.
Core
GA
az search service shared-private-link-resource wait
Place the CLI in a waiting state until a condition is met.
Core
GA
az search service show
Get the search service with the given name in the given resource group.
Core
GA
az search service update
Update an existing search service in the given resource group.
Core
GA
az search service upgrade
Upgrades the Azure AI Search service to the latest version available.
Core
GA
az search service wait
Place the CLI in a waiting state until a condition is met.
Core
GA
az search shared-private-link-resource
Manage Azure AI Search shared private link resources.
Core
GA
az search shared-private-link-resource create
Create shared privatelink resources in a Search service in the given resource group.
Core
GA
az search shared-private-link-resource delete
Initiates the deletion of the shared private link resource from the search service.
Core
GA
az search shared-private-link-resource list
Gets a list of all shared private link resources managed by the given service.
Core
GA
az search shared-private-link-resource show
Gets the details of the shared private link resource managed by the search service in the given resource group.
Core
GA
az search shared-private-link-resource update
Update shared privatelink resources in a Search service in the given resource group.
Core
GA
az search shared-private-link-resource wait
Wait for async shared private link resource operations.
Core
GA
az search usage
Manage Usage.
Core
GA
az search usage list
List a list of all Azure AI Search quota usages across the subscription.
Core
GA
az search usage show
Get the quota usage for a search SKU in the given subscription.
Core
GA
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