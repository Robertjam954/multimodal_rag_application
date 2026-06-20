<!-- source: https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest -->

# az group

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
az group
Manage resource groups and template deployments.
Commands
Name
Description
Type
Status
az group create
Create a new resource group.
Core
GA
az group delete
Delete a resource group.
Core
GA
az group exists
Check if a resource group exists.
Core
GA
az group export
Captures a resource group as a template.
Core
GA
az group list
List resource groups.
Core
GA
az group lock
Manage Azure resource group locks.
Core
GA
az group lock create
Create a resource group lock.
Core
GA
az group lock delete
Delete a resource group lock.
Core
GA
az group lock list
List lock information in the resource-group.
Core
GA
az group lock show
Show the details of a resource group lock.
Core
GA
az group lock update
Update a resource group lock.
Core
GA
az group show
Gets a resource group.
Core
GA
az group update
Update a resource group.
Core
GA
az group wait
Place the CLI in a waiting state until a condition of the resource group is met.
Core
GA
az group create
Edit
Create a new resource group.
```
az group create --location
                --name --resource-group
                [--acquire-policy-token]
                [--change-reference]
                [--managed-by]
                [--tags]
```
Examples
Create a new resource group in the West US region.
```
az group create -l westus -n MyResourceGroup
```
Required Parameters
--location -l
Location. Values from:
az account list-locations
. You can configure the default location using
az configure --defaults location=<location>
.
--name --resource-group -g -n
Name of the new resource group.
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
--managed-by
The ID of the resource that manages this resource group.
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
az group delete
Edit
Delete a resource group.
```
az group delete --name --resource-group
                [--acquire-policy-token]
                [--change-reference]
                [--force-deletion-types {Microsoft.Compute/virtualMachineScaleSets, Microsoft.Compute/virtualMachines, Microsoft.Databricks/workspaces}]
                [--no-wait]
                [--yes]
```
Examples
Delete a resource group.
```
az group delete -n MyResourceGroup
```
Force delete all the Virtual Machines in a resource group.
```
az group delete -n MyResourceGroup --force-deletion-types Microsoft.Compute/virtualMachines
```
Required Parameters
--name --resource-group -g -n
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
--force-deletion-types -f
The resource types you want to force delete.
Property
Value
Accepted values:
Microsoft.Compute/virtualMachineScaleSets, Microsoft.Compute/virtualMachines, Microsoft.Databricks/workspaces
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
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
az group exists
Edit
Check if a resource group exists.
```
az group exists --name --resource-group
                [--acquire-policy-token]
                [--change-reference]
```
Examples
Check if 'MyResourceGroup' exists.
```
az group exists -n MyResourceGroup
```
Required Parameters
--name --resource-group -g -n
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
az group export
Edit
Captures a resource group as a template.
```
az group export --name --resource-group
                [--acquire-policy-token]
                [--change-reference]
                [--export-format {arm, bicep, json}]
                [--include-comments]
                [--include-parameter-default-value]
                [--resource-ids]
                [--skip-all-params]
                [--skip-resource-name-params]
```
Required Parameters
--name --resource-group -g -n
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
--export-format
The format of the exported template.
Property
Value
Default value:
json
Accepted values:
arm, bicep, json
--include-comments
Export template with comments.
Property
Value
Default value:
False
--include-parameter-default-value
Export template parameter with default value.
Property
Value
Default value:
False
--resource-ids
Space-separated resource ids to filter the export by. To export all resources, do not specify this argument or supply "*".
--skip-all-params
Export template parameter and skip all parameterization.
Property
Value
Default value:
False
--skip-resource-name-params
Export template and skip resource name parameterization.
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
az group list
Edit
List resource groups.
```
az group list [--tag]
```
Examples
List all resource groups located in the West US region.
```
az group list --query "[?location=='westus']"
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--tag
A single tag in 'key[=value]' format. Use "" to clear existing tags.
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
az group show
Edit
Gets a resource group.
```
az group show --name --resource-group
```
Required Parameters
--name --resource-group -g -n
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
az group update
Edit
Update a resource group.
```
az group update --name --resource-group
                [--acquire-policy-token]
                [--change-reference]
                [--force-string]
                [--set]
                [--tags]
```
Examples
Update a resource group. (autogenerated)
```
az group update --resource-group MyResourceGroup --set tags.CostCenter='{"Dept":"IT","Environment":"Test"}'
```
Required Parameters
--name --resource-group -g -n
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
--force-string
When using 'set' or 'add', preserve string literals instead of attempting to convert to JSON.
Property
Value
Parameter group:
Generic Update Arguments
Default value:
False
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
az group wait
Edit
Place the CLI in a waiting state until a condition of the resource group is met.
```
az group wait --name --resource-group
              [--acquire-policy-token]
              [--change-reference]
              [--created]
              [--custom]
              [--deleted]
              [--exists]
              [--interval]
              [--timeout]
              [--updated]
```
Examples
Place the CLI in a waiting state until a condition of the resource group is met. (autogenerated)
```
az group wait --created  --resource-group MyResourceGroup
```
Place the CLI in a waiting state until a condition of the resource group is met. (autogenerated)
```
az group wait --deleted --resource-group MyResourceGroup
```
Required Parameters
--name --resource-group -g -n
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
--created
Wait until created with 'provisioningState' at 'Succeeded'.
Property
Value
Parameter group:
Wait Condition Arguments
Default value:
False
--custom
Wait until the condition satisfies a custom JMESPath query. E.g. provisioningState!='InProgress', instanceView.statuses[?code=='PowerState/running'].
Property
Value
Parameter group:
Wait Condition Arguments
--deleted
Wait until deleted.
Property
Value
Parameter group:
Wait Condition Arguments
Default value:
False
--exists
Wait until the resource exists.
Property
Value
Parameter group:
Wait Condition Arguments
Default value:
False
--interval
Polling interval in seconds.
Property
Value
Parameter group:
Wait Condition Arguments
Default value:
30
--timeout
Maximum wait in seconds.
Property
Value
Parameter group:
Wait Condition Arguments
Default value:
3600
--updated
Wait until updated with provisioningState at 'Succeeded'.
Property
Value
Parameter group:
Wait Condition Arguments
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