<!-- source: https://learn.microsoft.com/en-us/cli/azure/keyvault?view=azure-cli-latest -->

# az keyvault

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
az keyvault
Note
This command group has commands that are defined in both Azure CLI and at least one extension. Install each extension to benefit from its extended capabilities.
Learn more
about extensions.
Manage KeyVault keys, secrets, and certificates.
Commands
Name
Description
Type
Status
az keyvault backup
Manage full HSM backup.
Core
GA
az keyvault backup start
Begin a full backup of the HSM.
Core
GA
az keyvault certificate
Manage certificates.
Core
GA
az keyvault certificate backup
Backs up the specified certificate.
Core
GA
az keyvault certificate contact
Manage contacts for certificate management.
Core
GA
az keyvault certificate contact add
Add a contact to the specified vault to receive notifications of certificate operations.
Core
GA
az keyvault certificate contact delete
Remove a certificate contact from the specified vault.
Core
GA
az keyvault certificate contact list
Lists the certificate contacts for a specified key vault.
Core
GA
az keyvault certificate create
Create a Key Vault certificate.
Core
GA
az keyvault certificate delete
Deletes a certificate from a specified key vault.
Core
Deprecated
az keyvault certificate download
Download the public portion of a Key Vault certificate.
Core
GA
az keyvault certificate get-default-policy
Get the default policy for self-signed certificates.
Core
GA
az keyvault certificate import
Import a certificate into KeyVault.
Core
GA
az keyvault certificate issuer
Manage certificate issuer information.
Core
GA
az keyvault certificate issuer admin
Manage admin information for certificate issuers.
Core
GA
az keyvault certificate issuer admin add
Add admin details for a specified certificate issuer.
Core
GA
az keyvault certificate issuer admin delete
Remove admin details for the specified certificate issuer.
Core
GA
az keyvault certificate issuer admin list
List admins for a specified certificate issuer.
Core
GA
az keyvault certificate issuer create
Create a certificate issuer record.
Core
GA
az keyvault certificate issuer delete
Deletes the specified certificate issuer.
Core
GA
az keyvault certificate issuer list
Lists properties of the certificate issuers for the key vault.
Core
GA
az keyvault certificate issuer show
Gets the specified certificate issuer.
Core
GA
az keyvault certificate issuer update
Update a certificate issuer record.
Core
GA
az keyvault certificate list
List certificates in a specified key vault.
Core
GA
az keyvault certificate list-deleted
Lists the currently-recoverable deleted certificates.
Core
GA
az keyvault certificate list-versions
List the versions of a certificate.
Core
GA
az keyvault certificate pending
Manage pending certificate creation operations.
Core
GA
az keyvault certificate pending delete
Deletes the creation operation for a specific certificate.
Core
GA
az keyvault certificate pending merge
Merges a certificate or a certificate chain with a key pair existing on the server.
Core
GA
az keyvault certificate pending show
Gets the creation operation of a certificate.
Core
GA
az keyvault certificate purge
Permanently deletes the specified deleted certificate.
Core
GA
az keyvault certificate recover
Recover a deleted certificate to its latest version.
Core
GA
az keyvault certificate restore
Restores a backed up certificate to a vault.
Core
GA
az keyvault certificate set-attributes
Updates the specified attributes associated with the given certificate.
Core
GA
az keyvault certificate show
Gets information about a certificate.
Core
GA
az keyvault certificate show-deleted
Get a deleted certificate.
Core
GA
az keyvault check-name
Check that the given name is valid and is not already in use.
Core
GA
az keyvault create
Create a Vault or HSM.
Core
GA
az keyvault delete
Delete a Vault or HSM.
Core
GA
az keyvault delete-policy
Delete security policy settings for a Key Vault.
Core
GA
az keyvault key
Manage keys.
Core
GA
az keyvault key backup
Request that a backup of the specified key be downloaded to the client.
Core
GA
az keyvault key create
Create a new key, stores it, then returns key parameters and attributes to the client.
Core
GA
az keyvault key decrypt
Decrypt a single block of encrypted data.
Core
Preview
az keyvault key delete
Delete a key of any type from storage in Vault or HSM.
Core
GA
az keyvault key download
Download the public part of a stored key.
Core
GA
az keyvault key encrypt
Encrypt an arbitrary sequence of bytes using an encryption key that is stored in a Vault or HSM.
Core
Preview
az keyvault key get-attestation
Get a key's attestation blob.
Core
GA
az keyvault key get-policy-template
Return policy template as JSON encoded policy definition.
Core
Preview
az keyvault key import
Import a private key.
Core
GA
az keyvault key list
List keys in the specified Vault or HSM.
Core
GA
az keyvault key list-deleted
List the deleted keys in the specified Vault or HSM.
Core
GA
az keyvault key list-versions
List the identifiers and properties of a key's versions.
Core
GA
az keyvault key purge
Permanently delete the specified key.
Core
GA
az keyvault key random
Get the requested number of random bytes from a managed HSM.
Core
GA
az keyvault key recover
Recover the deleted key to its latest version.
Core
GA
az keyvault key restore
Restore a backed up key to a Vault or HSM.
Core
GA
az keyvault key rotate
Rotate the key based on the key policy by generating a new version of the key.
Core
GA
az keyvault key rotation-policy
Manage key's rotation policy.
Core
GA
az keyvault key rotation-policy show
Get the rotation policy of a Key Vault key.
Core
GA
az keyvault key rotation-policy update
Update the rotation policy of a Key Vault key.
Core
GA
az keyvault key set-attributes
The update key operation changes specified attributes of a stored key and can be applied to any key type and key version stored in Vault or HSM.
Core
GA
az keyvault key show
Get a key's attributes and, if it's an asymmetric key, its public material.
Core
GA
az keyvault key show-deleted
Get the public part of a deleted key.
Core
GA
az keyvault key sign
Create a signature from a digest using a key that is stored in a Vault or HSM.
Core
GA
az keyvault key verify
Verify a signature using the key that is stored in a Vault or HSM.
Core
GA
az keyvault list
List Vaults and/or HSMs.
Core
GA
az keyvault list-deleted
Get information about the deleted Vaults or HSMs in a subscription.
Core
GA
az keyvault network-rule
Manage network ACLs for vault or managed hsm.
Core
GA
az keyvault network-rule add
Add a network rule to the network ACLs for a Key Vault or a Managed HSM.
Core
GA
az keyvault network-rule list
List the network rules from the network ACLs for a Key Vault or a Managed HSM.
Core
GA
az keyvault network-rule remove
Remove a network rule from the network ACLs for a Key Vault or a Managed HSM.
Core
GA
az keyvault network-rule wait
Place the CLI in a waiting state until a condition of the vault or managed hsm is met.
Core
GA
az keyvault private-endpoint-connection
Manage vault/HSM private endpoint connections.
Core
GA
az keyvault private-endpoint-connection approve
Approve a private endpoint connection request for a Key Vault/HSM.
Core
GA
az keyvault private-endpoint-connection delete
Delete the specified private endpoint connection associated with a Key Vault/HSM.
Core
GA
az keyvault private-endpoint-connection list
List all private endpoint connections associated with a HSM.
Core
GA
az keyvault private-endpoint-connection reject
Reject a private endpoint connection request for a Key Vault/HSM.
Core
GA
az keyvault private-endpoint-connection show
Show details of a private endpoint connection associated with a Key Vault/HSM.
Core
GA
az keyvault private-endpoint-connection wait
Place the CLI in a waiting state until a condition of the private endpoint connection is met.
Core
GA
az keyvault private-link-resource
Manage vault/HSM private link resources.
Core
GA
az keyvault private-link-resource list
List the private link resources supported for a Key Vault/HSM.
Core
GA
az keyvault purge
Permanently delete the specified Vault or HSM. Aka Purges the deleted Vault or HSM.
Core
GA
az keyvault recover
Recover a Vault or HSM.
Core
GA
az keyvault region
Manage MHSM multi-regions.
Core and Extension
GA
az keyvault region add
Add regions for the managed HSM Pool.
Core
GA
az keyvault region add (keyvault-preview extension)
Add regions for the managed HSM Pool.
Extension
Preview
az keyvault region list
Get regions information associated with the managed HSM Pool.
Core
GA
az keyvault region list (keyvault-preview extension)
Get regions information associated with the managed HSM Pool.
Extension
Preview
az keyvault region remove
Remove regions for the managed HSM Pool.
Core
GA
az keyvault region remove (keyvault-preview extension)
Remove regions for the managed HSM Pool.
Extension
Preview
az keyvault region wait
Place the CLI in a waiting state until a condition of the HSM is met.
Core
GA
az keyvault region wait (keyvault-preview extension)
Place the CLI in a waiting state until a condition of the HSM is met.
Extension
Preview
az keyvault restore
Manage full HSM restore.
Core
GA
az keyvault restore start
Restore a full backup of a HSM.
Core
GA
az keyvault role
Manage user roles for access control.
Core
GA
az keyvault role assignment
Manage role assignments.
Core
GA
az keyvault role assignment create
Create a new role assignment for a user, group, or service principal.
Core
GA
az keyvault role assignment delete
Delete a role assignment.
Core
GA
az keyvault role assignment list
List role assignments.
Core
GA
az keyvault role definition
Manage role definitions.
Core
GA
az keyvault role definition create
Create a custom role definition.
Core
GA
az keyvault role definition delete
Delete a role definition.
Core
GA
az keyvault role definition list
List role definitions.
Core
GA
az keyvault role definition show
Show the details of a role definition.
Core
GA
az keyvault role definition update
Update a role definition.
Core
GA
az keyvault secret
Manage secrets.
Core
GA
az keyvault secret backup
Backs up the specified secret.
Core
GA
az keyvault secret delete
Delete all versions of a secret.
Core
Deprecated
az keyvault secret download
Download a secret from a KeyVault.
Core
GA
az keyvault secret list
List secrets in a specified key vault.
Core
GA
az keyvault secret list-deleted
Lists deleted secrets for the specified vault.
Core
GA
az keyvault secret list-versions
List all versions of the specified secret.
Core
GA
az keyvault secret purge
Permanently deletes the specified secret.
Core
GA
az keyvault secret recover
Recovers the deleted secret to the latest version.
Core
GA
az keyvault secret restore
Restores a backed up secret to a vault.
Core
GA
az keyvault secret set
Create a secret (if one doesn't exist) or update a secret in a KeyVault.
Core
GA
az keyvault secret set-attributes
Updates the attributes associated with a specified secret in a given key vault.
Core
GA
az keyvault secret show
Get a specified secret from a given key vault.
Core
GA
az keyvault secret show-deleted
Gets the specified deleted secret.
Core
GA
az keyvault security-domain
Manage security domain operations.
Core
GA
az keyvault security-domain download
Download the security domain file from the HSM.
Core
GA
az keyvault security-domain init-recovery
Retrieve the exchange key of the HSM.
Core
GA
az keyvault security-domain restore-blob
Enable to decrypt and encrypt security domain file as blob. Can be run in offline environment, before file is uploaded to HSM using security-domain upload.
Core
GA
az keyvault security-domain upload
Start to restore the HSM.
Core
GA
az keyvault security-domain wait
Place the CLI in a waiting state until HSM security domain operation is finished.
Core
GA
az keyvault set-policy
Update security policy settings for a Key Vault.
Core
GA
az keyvault setting
Manage MHSM settings.
Core
GA
az keyvault setting list
Get all settings associated with the managed HSM.
Core
GA
az keyvault setting show
Get specific setting associated with the managed HSM.
Core
GA
az keyvault setting update
Update specific setting associated with the managed HSM.
Core
GA
az keyvault show
Show details of a Vault or HSM.
Core
GA
az keyvault show-deleted
Show details of a deleted Vault or HSM.
Core
GA
az keyvault update
Update the properties of a Vault.
Core
GA
az keyvault update-hsm
Update the properties of a HSM.
Core
GA
az keyvault update-hsm (keyvault-preview extension)
Update the properties of a HSM.
Extension
GA
az keyvault wait
Place the CLI in a waiting state until a condition of the Vault is met.
Core
GA
az keyvault wait-hsm
Place the CLI in a waiting state until a condition of the HSM is met.
Core
GA
az keyvault check-name
Edit
Check that the given name is valid and is not already in use.
```
az keyvault check-name --name
                       [--acquire-policy-token]
                       [--change-reference]
                       [--resource-type {hsm}]
```
Required Parameters
--name -n
The name of the HSM within the specified resource group.
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
--resource-type
Type of resource.
Property
Value
Default value:
hsm
Accepted values:
hsm
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
az keyvault create
Edit
Create a Vault or HSM.
RBAC authorization is enabled by default. If
--enable-rbac-authorization
is manually specified to
false
and
--no-self-perms
flag is not specified, default permissions are created for the current user or service principal.
If you want to assign the default permission, you have to change the default subscription with
az account set
first, instead of using
--subscription
.
```
az keyvault create --resource-group
                   [--acquire-policy-token]
                   [--administrators]
                   [--bypass {AzureServices, None}]
                   [--change-reference]
                   [--default-action {Allow, Deny}]
                   [--enable-purge-protection {false, true}]
                   [--enable-rbac-authorization {false, true}]
                   [--enabled-for-deployment {false, true}]
                   [--enabled-for-disk-encryption {false, true}]
                   [--enabled-for-template-deployment {false, true}]
                   [--hsm-name]
                   [--location]
                   [--mi-user-assigned]
                   [--name]
                   [--network-acls]
                   [--network-acls-ips]
                   [--network-acls-vnets]
                   [--no-self-perms {false, true}]
                   [--no-wait]
                   [--public-network-access {Disabled, Enabled}]
                   [--retention-days]
                   [--sku]
                   [--tags]
```
Examples
Create a key vault with network ACLs specified (use --network-acls to specify IP and VNet rules by using a JSON string).
```
az keyvault create --location westus2 --name MyKeyVault --resource-group MyResourceGroup --network-acls "{\"ip\": [\"1.2.3.4\", \"2.3.4.0/24\"], \"vnet\": [\"vnet_name_1/subnet_name1\", \"vnet_name_2/subnet_name2\", \"/subscriptions/000000-0000-0000/resourceGroups/MyResourceGroup/providers/Microsoft.Network/virtualNetworks/MyVNet/subnets/MySubnet\"]}"
```
Create a key vault with network ACLs specified (use --network-acls to specify IP and VNet rules by using a JSON file).
```
az keyvault create --location westus2 --name MyKeyVault --resource-group MyResourceGroup --network-acls network-acls-example.json
```
Create a key vault with network ACLs specified (use --network-acls-ips to specify IP rules).
```
az keyvault create --location westus2 --name MyKeyVault --resource-group MyResourceGroup --network-acls-ips 3.4.5.0/24 4.5.6.0/24
```
Create a key vault with network ACLs specified (use --network-acls-vnets to specify VNet rules).
```
az keyvault create --location westus2 --name MyKeyVault --resource-group MyResourceGroup --network-acls-vnets vnet_name_2/subnet_name_2 vnet_name_3/subnet_name_3 /subscriptions/000000-0000-0000/resourceGroups/MyResourceGroup/providers/Microsoft.Network/virtualNetworks/vnet_name_4/subnets/subnet_name_4
```
Create a key vault with network ACLs specified (use --network-acls, --network-acls-ips and --network-acls-vnets together, redundant rules will be removed, finally there will be 4 IP rules and 3 VNet rules).
```
az keyvault create --location westus2 --name MyKeyVault --resource-group MyResourceGroup --network-acls "{\"ip\": [\"1.2.3.4\", \"2.3.4.0/24\"], \"vnet\": [\"vnet_name_1/subnet_name1\", \"vnet_name_2/subnet_name2\"]}" --network-acls-ips 3.4.5.0/24 4.5.6.0/24 --network-acls-vnets vnet_name_2/subnet_name_2 vnet_name_3/subnet_name_3 /subscriptions/000000-0000-0000/resourceGroups/MyResourceGroup/providers/Microsoft.Network/virtualNetworks/vnet_name_4/subnets/subnet_name_4
```
Create a key vault. (autogenerated)
```
az keyvault create --location westus2 --name MyKeyVault --resource-group MyResourceGroup
```
Required Parameters
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
--administrators
[HSM Only] Administrator role for data plane operations for Managed HSM. It accepts a space separated list of OIDs that will be assigned.
--bypass
Bypass traffic for space-separated uses.
Property
Value
Parameter group:
Network Rule Arguments
Accepted values:
AzureServices, None
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--default-action
Default action to apply when no rule matches.
Property
Value
Parameter group:
Network Rule Arguments
Accepted values:
Allow, Deny
--enable-purge-protection
Property specifying whether protection against purge is enabled for this vault/managed HSM pool. Setting this property to true activates protection against purge for this vault/managed HSM pool and its content - only the Key Vault/Managed HSM service may initiate a hard, irrecoverable deletion. The setting is effective only if soft delete is also enabled. Enabling this functionality is irreversible.
Property
Value
Accepted values:
false, true
--enable-rbac-authorization
Property that controls how data actions are authorized. When true, the key vault will use Role Based Access Control (RBAC) for authorization of data actions, and the access policies specified in vault properties will be ignored. When false, the key vault will use the access policies specified in vault properties, and any policy stored on Azure Resource Manager will be ignored. If null or not specified, the vault is created with the default value of true. Note that management actions are always authorized with RBAC.
Property
Value
Default value:
True
Accepted values:
false, true
--enabled-for-deployment
[Vault Only] Property to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault.
Property
Value
Accepted values:
false, true
--enabled-for-disk-encryption
[Vault Only] Property to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys.
Property
Value
Accepted values:
false, true
--enabled-for-template-deployment
[Vault Only] Property to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault.
Property
Value
Accepted values:
false, true
--hsm-name
Name of the HSM. (--hsm-name and --name/-n are mutually exclusive, please specify just one of them).
--location -l
Location. Values from:
az account list-locations
. You can configure the default location using
az configure --defaults location=<location>
.
--mi-user-assigned
[HSM Only] Enable user-assigned managed identities for managed HSM. Accept space-separated list of identity resource IDs.
--name -n
Name of the Vault.
--network-acls
Network ACLs. It accepts a JSON filename or a JSON string. JSON format:
{\"ip\":[<ip1>, <ip2>...],\"vnet\":[<vnet_name_1>/<subnet_name_1>,<subnet_id2>...]}
.
Property
Value
Parameter group:
Network Rule Arguments
--network-acls-ips
Network ACLs IP rules. Space-separated list of IP addresses.
Property
Value
Parameter group:
Network Rule Arguments
--network-acls-vnets
Network ACLS VNet rules. Space-separated list of Vnet/subnet pairs or subnet resource ids.
Property
Value
Parameter group:
Network Rule Arguments
--no-self-perms
[Vault Only] Don't add permissions for the current user/service principal in the new vault.
Property
Value
Accepted values:
false, true
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--public-network-access
Control permission for data plane traffic coming from public networks while private endpoint is enabled.
Property
Value
Accepted values:
Disabled, Enabled
--retention-days
Soft delete data retention days. It accepts >=7 and <=90. Defaults to 90 for keyvault creation. Required for MHSM creation.
--sku
Required. SKU details. Allowed values for Vault: premium, standard. Default: standard. Allowed values for HSM: Standard_B1, Custom_B32, Custom_B6, Custom_C42, Custom_C10. Default: Standard_B1.
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
az keyvault delete
Edit
Delete a Vault or HSM.
```
az keyvault delete [--acquire-policy-token]
                   [--change-reference]
                   [--hsm-name]
                   [--name]
                   [--no-wait]
                   [--resource-group]
```
Examples
Delete a key vault. (autogenerated)
```
az keyvault delete --name MyKeyVault --resource-group MyResourceGroup
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
--hsm-name
Name of the HSM. (--hsm-name and --name/-n are mutually exclusive, please specify just one of them).
--name -n
Name of the Vault.
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--resource-group -g
Name of resource group.
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
az keyvault delete-policy
Edit
Delete security policy settings for a Key Vault.
```
az keyvault delete-policy --name
                          [--acquire-policy-token]
                          [--application-id]
                          [--change-reference]
                          [--no-wait]
                          [--object-id]
                          [--resource-group]
                          [--spn]
                          [--upn]
```
Required Parameters
--name -n
Name of the Vault.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--application-id
Application ID of the client making request on behalf of a principal. Exposed for compound identity using on-behalf-of authentication flow.
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--object-id
A GUID that identifies the principal that will receive permissions.
--resource-group -g
Name of resource group.
--spn
Name of a service principal that will receive permissions.
--upn
Name of a user principal that will receive permissions.
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
az keyvault list
Edit
List Vaults and/or HSMs.
```
az keyvault list [--resource-group]
                 [--resource-type]
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--resource-group -g
Name of resource group. You can configure the default group using
az configure --defaults group=<name>
.
--resource-type
When --resource-type is not present the command will list all Vaults and HSMs. Possible values for --resource-type are vault and hsm.
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
az keyvault list-deleted
Edit
Get information about the deleted Vaults or HSMs in a subscription.
```
az keyvault list-deleted [--acquire-policy-token]
                         [--change-reference]
                         [--resource-type]
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
--resource-type
When --resource-type is not present the command will list all deleted Vaults and HSMs. Possible values for --resource-type are vault and hsm.
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
az keyvault purge
Edit
Permanently delete the specified Vault or HSM. Aka Purges the deleted Vault or HSM.
```
az keyvault purge [--acquire-policy-token]
                  [--change-reference]
                  [--hsm-name]
                  [--location]
                  [--name]
                  [--no-wait]
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
--hsm-name
Name of the deleted HSM. (--hsm-name and --name/-n are mutually exclusive, please specify just one of them).
--location -l
Location of the deleted Vault or HSM.
--name -n
Name of the deleted Vault.
--no-wait
Do not wait for the long-running operation to finish.
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
az keyvault recover
Edit
Recover a Vault or HSM.
Recover a previously deleted Vault or HSM for which soft delete was enabled.
```
az keyvault recover [--acquire-policy-token]
                    [--change-reference]
                    [--hsm-name]
                    [--location]
                    [--name]
                    [--no-wait]
                    [--resource-group]
```
Examples
Recover a key vault. (autogenerated)
```
az keyvault recover --location westus2 --name MyKeyVault --resource-group MyResourceGroup
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
--hsm-name
Name of the deleted HSM. (--hsm-name and --name/-n are mutually exclusive, please specify just one of them).
--location -l
Location of the deleted Vault or HSM.
--name -n
Name of the deleted Vault.
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--resource-group -g
Resource group of the deleted Vault or HSM.
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
az keyvault set-policy
Edit
Update security policy settings for a Key Vault.
```
az keyvault set-policy --name
                       [--acquire-policy-token]
                       [--application-id]
                       [--certificate-permissions {all, backup, create, delete, deleteissuers, get, getissuers, import, list, listissuers, managecontacts, manageissuers, purge, recover, restore, setissuers, update}]
                       [--change-reference]
                       [--key-permissions {all, backup, create, decrypt, delete, encrypt, get, getrotationpolicy, import, list, purge, recover, release, restore, rotate, setrotationpolicy, sign, unwrapKey, update, verify, wrapKey}]
                       [--no-wait]
                       [--object-id]
                       [--resource-group]
                       [--secret-permissions {all, backup, delete, get, list, purge, recover, restore, set}]
                       [--spn]
                       [--storage-permissions {all, backup, delete, deletesas, get, getsas, list, listsas, purge, recover, regeneratekey, restore, set, setsas, update}]
                       [--upn]
```
Examples
Assign key permissions `get`, `list`, `import` and secret permissions `backup`, `restore` to an object id.
```
az keyvault set-policy -n MyVault --key-permissions get list import --secret-permissions backup restore --object-id {GUID}
```
Assign key permissions `get`, `list` to a UPN (User Principal Name).
```
az keyvault set-policy -n MyVault --key-permissions get list --upn {UPN}
```
Assign key permissions `get`, `list` to a SPN (Service Principal Name).
```
az keyvault set-policy -n MyVault --key-permissions get list --spn {SPN}
```
Required Parameters
--name -n
Name of the Vault.
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--application-id
Application ID of the client making request on behalf of a principal. Exposed for compound identity using on-behalf-of authentication flow.
--certificate-permissions
Space-separated list of certificate permissions to assign.
Property
Value
Parameter group:
Permission Arguments
Accepted values:
all, backup, create, delete, deleteissuers, get, getissuers, import, list, listissuers, managecontacts, manageissuers, purge, recover, restore, setissuers, update
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--key-permissions
Space-separated list of key permissions to assign.
Property
Value
Parameter group:
Permission Arguments
Accepted values:
all, backup, create, decrypt, delete, encrypt, get, getrotationpolicy, import, list, purge, recover, release, restore, rotate, setrotationpolicy, sign, unwrapKey, update, verify, wrapKey
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--object-id
A GUID that identifies the principal that will receive permissions.
--resource-group -g
Name of resource group.
--secret-permissions
Space-separated list of secret permissions to assign.
Property
Value
Parameter group:
Permission Arguments
Accepted values:
all, backup, delete, get, list, purge, recover, restore, set
--spn
Name of a service principal that will receive permissions.
--storage-permissions
Space-separated list of storage permissions to assign.
Property
Value
Parameter group:
Permission Arguments
Accepted values:
all, backup, delete, deletesas, get, getsas, list, listsas, purge, recover, regeneratekey, restore, set, setsas, update
--upn
Name of a user principal that will receive permissions.
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
az keyvault show
Edit
Show details of a Vault or HSM.
```
az keyvault show [--hsm-name]
                 [--name]
                 [--resource-group]
```
Examples
Show details of a key vault. (autogenerated)
```
az keyvault show --name MyKeyVault
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--hsm-name
Name of the HSM. (--hsm-name and --name/-n are mutually exclusive, please specify just one of them).
--name -n
Name of the Vault.
--resource-group -g
Name of resource group.
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
az keyvault show-deleted
Edit
Show details of a deleted Vault or HSM.
```
az keyvault show-deleted [--acquire-policy-token]
                         [--change-reference]
                         [--hsm-name]
                         [--location]
                         [--name]
```
Examples
Show details of a deleted key vault.
```
az keyvault show-deleted --name MyKeyVault
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
--hsm-name
Name of the deleted HSM. (--hsm-name and --name/-n are mutually exclusive, please specify just one of them).
--location -l
Location of the deleted Vault or HSM.
--name -n
Name of the deleted Vault.
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
az keyvault update
Edit
Update the properties of a Vault.
```
az keyvault update --name
                   [--acquire-policy-token]
                   [--add]
                   [--bypass {AzureServices, None}]
                   [--change-reference]
                   [--default-action {Allow, Deny}]
                   [--enable-purge-protection {false, true}]
                   [--enable-rbac-authorization {false, true}]
                   [--enabled-for-deployment {false, true}]
                   [--enabled-for-disk-encryption {false, true}]
                   [--enabled-for-template-deployment {false, true}]
                   [--force-string]
                   [--no-wait]
                   [--public-network-access {Disabled, Enabled}]
                   [--remove]
                   [--resource-group]
                   [--retention-days]
                   [--set]
```
Examples
Update the properties of a Vault. (autogenerated)
```
az keyvault update --enabled-for-disk-encryption true --name MyKeyVault --resource-group MyResourceGroup
```
Required Parameters
--name -n
Name of the Vault.
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
--bypass
Bypass traffic for space-separated uses.
Property
Value
Parameter group:
Network Rule Arguments
Accepted values:
AzureServices, None
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--default-action
Default action to apply when no rule matches.
Property
Value
Parameter group:
Network Rule Arguments
Accepted values:
Allow, Deny
--enable-purge-protection
Property specifying whether protection against purge is enabled for this vault/managed HSM pool. Setting this property to true activates protection against purge for this vault/managed HSM pool and its content - only the Key Vault/Managed HSM service may initiate a hard, irrecoverable deletion. The setting is effective only if soft delete is also enabled. Enabling this functionality is irreversible.
Property
Value
Accepted values:
false, true
--enable-rbac-authorization
Property that controls how data actions are authorized. When true, the key vault will use Role Based Access Control (RBAC) for authorization of data actions, and the access policies specified in vault properties will be ignored. When false, the key vault will use the access policies specified in vault properties, and any policy stored on Azure Resource Manager will be ignored. If null or not specified, the vault is created with the default value of true. Note that management actions are always authorized with RBAC.
Property
Value
Accepted values:
false, true
--enabled-for-deployment
[Vault Only] Property to specify whether Azure Virtual Machines are permitted to retrieve certificates stored as secrets from the key vault.
Property
Value
Accepted values:
false, true
--enabled-for-disk-encryption
[Vault Only] Property to specify whether Azure Disk Encryption is permitted to retrieve secrets from the vault and unwrap keys.
Property
Value
Accepted values:
false, true
--enabled-for-template-deployment
[Vault Only] Property to specify whether Azure Resource Manager is permitted to retrieve secrets from the key vault.
Property
Value
Accepted values:
false, true
--force-string
When using 'set' or 'add', preserve string literals instead of attempting to convert to JSON.
Property
Value
Parameter group:
Generic Update Arguments
Default value:
False
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--public-network-access
Control permission for data plane traffic coming from public networks while private endpoint is enabled.
Property
Value
Accepted values:
Disabled, Enabled
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
Name of resource group.
--retention-days
Soft delete data retention days. It accepts >=7 and <=90.
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
az keyvault update-hsm
Edit
Update the properties of a HSM.
```
az keyvault update-hsm --hsm-name
                       [--acquire-policy-token]
                       [--add]
                       [--bypass {AzureServices, None}]
                       [--change-reference]
                       [--default-action {Allow, Deny}]
                       [--enable-purge-protection {false, true}]
                       [--force-string]
                       [--mi-user-assigned]
                       [--no-wait]
                       [--public-network-access {Disabled, Enabled}]
                       [--remove]
                       [--resource-group]
                       [--secondary-locations]
                       [--set]
```
Examples
Update the properties of a HSM.
```
az keyvault update-hsm --enable-purge-protection true --hsm-name MyHSM --resource-group MyResourceGroup
```
Required Parameters
--hsm-name
Name of the HSM.
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
--bypass
Bypass traffic for space-separated uses.
Property
Value
Parameter group:
Network Rule Arguments
Accepted values:
AzureServices, None
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--default-action
Default action to apply when no rule matches.
Property
Value
Parameter group:
Network Rule Arguments
Accepted values:
Allow, Deny
--enable-purge-protection -e
Property specifying whether protection against purge is enabled for this vault/managed HSM pool. Setting this property to true activates protection against purge for this vault/managed HSM pool and its content - only the Key Vault/Managed HSM service may initiate a hard, irrecoverable deletion. The setting is effective only if soft delete is also enabled. Enabling this functionality is irreversible.
Property
Value
Accepted values:
false, true
--force-string
When using 'set' or 'add', preserve string literals instead of attempting to convert to JSON.
Property
Value
Parameter group:
Generic Update Arguments
Default value:
False
--mi-user-assigned
Enable user-assigned managed identities for managed HSM. Accept space-separated list of identity resource IDs.
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
--public-network-access
Control permission for data plane traffic coming from public networks while private endpoint is enabled.
Property
Value
Accepted values:
Disabled, Enabled
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
Name of resource group.
--secondary-locations
--secondary-locations extends/contracts an HSM pool to listed regions. The primary location where the resource was originally created CANNOT be removed.
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
az keyvault update-hsm (keyvault-preview extension)
Update the properties of a HSM.
```
az keyvault update-hsm --hsm-name
                       [--acquire-policy-token]
                       [--add]
                       [--bypass {AzureServices, None}]
                       [--change-reference]
                       [--default-action {Allow, Deny}]
                       [--enable-purge-protection {false, true}]
                       [--force-string]
                       [--no-wait]
                       [--remove]
                       [--resource-group]
                       [--set]
```
Examples
Update the properties of a HSM.
```
az keyvault update-hsm --enable-purge-protection true --hsm-name MyHSM --resource-group MyResourceGroup
```
Required Parameters
--hsm-name
Name of the HSM.
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
--bypass
Bypass traffic for space-separated uses.
Property
Value
Parameter group:
Network Rule Arguments
Accepted values:
AzureServices, None
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--default-action
Default action to apply when no rule matches.
Property
Value
Parameter group:
Network Rule Arguments
Accepted values:
Allow, Deny
--enable-purge-protection -e
Property specifying whether protection against purge is enabled for this managed HSM pool. Setting this property to true activates protection against purge for this managed HSM pool and its content - only the Managed HSM service may initiate a hard, irrecoverable deletion. The setting is effective only if soft delete is also enabled. Enabling this functionality is irreversible.
Property
Value
Accepted values:
false, true
--force-string
When using 'set' or 'add', preserve string literals instead of attempting to convert to JSON.
Property
Value
Parameter group:
Generic Update Arguments
Default value:
False
--no-wait
Do not wait for the long-running operation to finish.
Property
Value
Default value:
False
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
Proceed only if Key Vault belongs to the specified resource group.
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
az keyvault wait
Edit
Place the CLI in a waiting state until a condition of the Vault is met.
```
az keyvault wait --name
                 [--acquire-policy-token]
                 [--change-reference]
                 [--created]
                 [--custom]
                 [--deleted]
                 [--exists]
                 [--interval]
                 [--resource-group]
                 [--timeout]
                 [--updated]
```
Examples
Pause CLI until the vault is created.
```
az keyvault wait --name MyVault --created
```
Required Parameters
--name -n
Name of the Vault.
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
--resource-group -g
Name of resource group.
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
az keyvault wait-hsm
Edit
Place the CLI in a waiting state until a condition of the HSM is met.
```
az keyvault wait-hsm --hsm-name
                     [--acquire-policy-token]
                     [--change-reference]
                     [--created]
                     [--custom]
                     [--deleted]
                     [--exists]
                     [--interval]
                     [--resource-group]
                     [--timeout]
                     [--updated]
```
Examples
Pause CLI until the HSM is created.
```
az keyvault wait-hsm --hsm-name MyHSM --created
```
Required Parameters
--hsm-name
Name of the HSM.
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
--resource-group -g
Proceed only if HSM belongs to the specified resource group.
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