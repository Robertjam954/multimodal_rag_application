<!-- source: https://learn.microsoft.com/en-us/cli/azure/storage?view=azure-cli-latest -->

# az storage

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
az storage
Note
This command group has commands that are defined in both Azure CLI and at least one extension. Install each extension to benefit from its extended capabilities.
Learn more
about extensions.
Manage Azure Cloud Storage resources.
Commands
Name
Description
Type
Status
az storage account
Manage storage accounts.
Core and Extension
GA
az storage account blob-inventory-policy
Manage storage account Blob Inventory Policy.
Core
Preview
az storage account blob-inventory-policy create
Create Blob Inventory Policy for storage account.
Core
Preview
az storage account blob-inventory-policy delete
Delete Blob Inventory Policy associated with the specified storage account.
Core
Preview
az storage account blob-inventory-policy show
Show Blob Inventory Policy properties associated with the specified storage account.
Core
Preview
az storage account blob-inventory-policy update
Update Blob Inventory Policy associated with the specified storage account.
Core
Preview
az storage account blob-service-properties
Manage the properties of a storage account's blob service.
Core
GA
az storage account blob-service-properties cors-rule
Manage the Cross-Origin Resource Sharing (CORS) rules of a storage account's blob service properties.
Core
GA
az storage account blob-service-properties cors-rule add
Add a CORS rule for a storage account.
Core
GA
az storage account blob-service-properties cors-rule clear
Clear all CORS rules for a storage account.
Core
GA
az storage account blob-service-properties cors-rule list
List all CORS rules of a storage account's blob service properties.
Core
GA
az storage account blob-service-properties show
Show the properties of a storage account's blob service.
Core
GA
az storage account blob-service-properties update
Update the properties of a storage account's blob service.
Core
GA
az storage account check-name
Check that the storage account name is valid and is not already in use.
Core
GA
az storage account create
Create a storage account.
Core
GA
az storage account create (storage-preview extension)
Create a storage account.
Extension
GA
az storage account delete
Delete a storage account.
Core
GA
az storage account encryption-scope
Manage encryption scope for a storage account.
Core
GA
az storage account encryption-scope create
Create an encryption scope within storage account.
Core
GA
az storage account encryption-scope list
List encryption scopes within storage account.
Core
GA
az storage account encryption-scope show
Show properties for specified encryption scope within storage account.
Core
GA
az storage account encryption-scope update
Update properties for specified encryption scope within storage account.
Core
GA
az storage account failover
Failover request can be triggered for a storage account in case of availability issues.
Core
GA
az storage account file-service-properties
Manage the properties of file service in storage account.
Core
GA
az storage account file-service-properties show
Show the properties of file service in storage account.
Core
GA
az storage account file-service-properties update
Update the properties of file service in storage account.
Core
GA
az storage account file-service-usage
Get the usage of file service in storage account including account limits, file share limits and constants used in recommendations and bursting formula.
Core
GA
az storage account generate-sas
Generate a shared access signature for the storage account.
Core
GA
az storage account hns-migration
Manage storage account migration to enable hierarchical namespace.
Core
GA
az storage account hns-migration start
Validate/Begin migrating a storage account to enable hierarchical namespace.
Core
GA
az storage account hns-migration stop
Stop the enabling hierarchical namespace migration of a storage account.
Core
GA
az storage account keys
Manage storage account keys.
Core
GA
az storage account keys list
List the access keys or Kerberos keys (if active directory enabled) for a storage account.
Core
GA
az storage account keys renew
Regenerate one of the access keys or Kerberos keys (if active directory enabled) for a storage account.
Core
GA
az storage account list
List storage accounts.
Core
GA
az storage account local-user
Manage storage account local users.
Core and Extension
GA
az storage account local-user create
Create a local user for a given storage account.
Core
GA
az storage account local-user create (storage-preview extension)
Create a local user for a given storage account.
Extension
GA
az storage account local-user delete
Delete a local user.
Core
GA
az storage account local-user delete (storage-preview extension)
Delete a local user.
Extension
GA
az storage account local-user list
List local users for a storage account.
Core
GA
az storage account local-user list (storage-preview extension)
List local users for a storage account.
Extension
GA
az storage account local-user list-keys
List sharedkeys and sshAuthorizedKeys for a local user.
Core
GA
az storage account local-user list-keys (storage-preview extension)
List sharedkeys and sshAuthorizedKeys for a local user.
Extension
GA
az storage account local-user regenerate-password
Regenerate sshPassword for a local user.
Core
GA
az storage account local-user regenerate-password (storage-preview extension)
Regenerate sshPassword for a local user.
Extension
GA
az storage account local-user show
Show info for a local user.
Core
GA
az storage account local-user show (storage-preview extension)
Show info for a local user.
Extension
GA
az storage account local-user update
Update properties for a local user.
Core
GA
az storage account local-user update (storage-preview extension)
Update properties for a local user.
Extension
GA
az storage account management-policy
Manage storage account management policies.
Core
GA
az storage account management-policy create
Create the data policy rules associated with the specified storage account.
Core
GA
az storage account management-policy delete
Delete the data policy rules associated with the specified storage account.
Core
GA
az storage account management-policy show
Get the data policy rules associated with the specified storage account.
Core
GA
az storage account management-policy update
Update the data policy rules associated with the specified storage account.
Core
GA
az storage account migration
Manage Storage Account Migration.
Core
GA
az storage account migration show
Get the status of the ongoing migration for the specified storage account.
Core
GA
az storage account migration start
Account Migration request can be triggered for a storage account to change its redundancy level. The migration updates the non-zonal redundant storage account to a zonal redundant account or vice-versa in order to have better reliability and availability. Zone-redundant storage (ZRS) replicates your storage account synchronously across three Azure availability zones in the primary region.
Core
GA
az storage account network-rule
Manage network rules.
Core
GA
az storage account network-rule add
Add a network rule.
Core
GA
az storage account network-rule list
List network rules.
Core
GA
az storage account network-rule remove
Remove a network rule.
Core
GA
az storage account network-security-perimeter-configuration
Manage Network Security Perimeter Configuration.
Core
GA
az storage account network-security-perimeter-configuration list
List list of effective NetworkSecurityPerimeterConfiguration for storage account.
Core
GA
az storage account network-security-perimeter-configuration reconcile
Refreshes any information about the association.
Core
GA
az storage account network-security-perimeter-configuration show
Get effective NetworkSecurityPerimeterConfiguration for association.
Core
GA
az storage account or-policy
Manage storage account Object Replication Policy.
Core
GA
az storage account or-policy create
Create Object Replication Service Policy for storage account.
Core
GA
az storage account or-policy delete
Delete specified Object Replication Service Policy associated with the specified storage account.
Core
GA
az storage account or-policy list
List Object Replication Service Policies associated with the specified storage account.
Core
GA
az storage account or-policy rule
Manage Object Replication Service Policy Rules.
Core
GA
az storage account or-policy rule add
Add rule to the specified Object Replication Service Policy.
Core
GA
az storage account or-policy rule list
List all the rules in the specified Object Replication Service Policy.
Core
GA
az storage account or-policy rule remove
Remove the specified rule from the specified Object Replication Service Policy.
Core
GA
az storage account or-policy rule show
Show the properties of specified rule in Object Replication Service Policy.
Core
GA
az storage account or-policy rule update
Update rule properties to Object Replication Service Policy.
Core
GA
az storage account or-policy show
Show the properties of specified Object Replication Service Policy for storage account.
Core
GA
az storage account or-policy update
Update Object Replication Service Policy properties for storage account.
Core
GA
az storage account private-endpoint-connection
Manage storage account private endpoint connection.
Core
Preview
az storage account private-endpoint-connection approve
Approve a private endpoint connection request for storage account.
Core
Preview
az storage account private-endpoint-connection delete
Delete a private endpoint connection request for storage account.
Core
Preview
az storage account private-endpoint-connection reject
Reject a private endpoint connection request for storage account.
Core
Preview
az storage account private-endpoint-connection show
Show details of a private endpoint connection request for storage account.
Core
Preview
az storage account private-link-resource
Manage storage account private link resources.
Core
GA
az storage account private-link-resource list
Get the private link resources that need to be created for a storage account.
Core
Preview
az storage account revoke-delegation-keys
Revoke all user delegation keys for a storage account.
Core
GA
az storage account show
Show storage account properties.
Core
GA
az storage account show-connection-string
Get the connection string for a storage account.
Core
GA
az storage account show-usage
Show the current count and limit of the storage accounts under the subscription.
Core
GA
az storage account task-assignment
Manage storage account task assignment.
Extension
GA
az storage account task-assignment create
Create a new storage task assignment sub-resource with the specified parameters. If a storage task assignment is already created and a subsequent create request is issued with different properties, the storage task assignment properties will be updated. If a storage task assignment is already created and a subsequent create or update request is issued with the exact same set of properties, the request will succeed.
Extension
GA
az storage account task-assignment delete
Delete the storage task assignment sub-resource.
Extension
GA
az storage account task-assignment list
List all the storage task assignments in an account.
Extension
GA
az storage account task-assignment list-report
List the report summary of a single storage task assignment's instances.
Extension
GA
az storage account task-assignment show
Get the storage task assignment properties.
Extension
GA
az storage account task-assignment update
Update a new storage task assignment sub-resource with the specified parameters. If a storage task assignment is already created and a subsequent create request is issued with different properties, the storage task assignment properties will be updated. If a storage task assignment is already created and a subsequent create or update request is issued with the exact same set of properties, the request will succeed.
Extension
GA
az storage account task-assignment wait
Place the CLI in a waiting state until a condition is met.
Extension
GA
az storage account update
Update the properties of a storage account.
Core
GA
az storage account update (storage-preview extension)
Update the properties of a storage account.
Extension
GA
az storage advanced-platform-metric
Manage Advanced Platform Metric.
Core
GA
az storage advanced-platform-metric create
Create the advanced platform metrics rule for the storage account.
Core
Preview
az storage advanced-platform-metric delete
Delete the advanced platform metrics rule for the storage account by rule type.
Core
Preview
az storage advanced-platform-metric list
List the advanced platform metrics rules associated with the storage account.
Core
Preview
az storage advanced-platform-metric show
Get the advanced platform metrics rule for the storage account by rule type.
Core
Preview
az storage advanced-platform-metric update
Update the advanced platform metrics rule for the storage account.
Core
Preview
az storage azcopy
[EXPERIMENTAL] Manage storage operations utilizing AzCopy.
Extension
GA
az storage azcopy blob
Manage object storage for unstructured data (blobs) using AzCopy.
Extension
GA
az storage azcopy blob delete
Delete blobs from a storage blob container using AzCopy.
Extension
GA
az storage azcopy blob download
Download blobs from a storage blob container using AzCopy.
Extension
GA
az storage azcopy blob sync
Sync blobs recursively to a storage blob container using AzCopy.
Extension
GA
az storage azcopy blob upload
Upload blobs to a storage blob container using AzCopy.
Extension
GA
az storage azcopy run-command
Run a command directly using the AzCopy CLI. Please use SAS tokens for authentication.
Extension
GA
az storage blob
Manage object storage for unstructured data (blobs).
Core and Extension
GA
az storage blob copy
Manage blob copy operations. Use
az storage blob show
to check the status of the blobs.
Core and Extension
GA
az storage blob copy cancel
Abort an ongoing copy operation.
Core
GA
az storage blob copy start
Copy a blob asynchronously. Use
az storage blob show
to check the status of the blobs.
Core
GA
az storage blob copy start (storage-blob-preview extension)
Start a copy blob job.
Extension
GA
az storage blob copy start-batch
Copy multiple blobs to a blob container. Use
az storage blob show
to check the status of the blobs.
Core
GA
az storage blob delete
Mark a blob or snapshot for deletion.
Core
GA
az storage blob delete (storage-blob-preview extension)
Mark a blob or snapshot for deletion.
Extension
GA
az storage blob delete-batch
Delete blobs from a blob container recursively.
Core
GA
az storage blob download
Download a blob to a file path.
Core
GA
az storage blob download-batch
Download blobs from a blob container recursively.
Core
GA
az storage blob exists
Check for the existence of a blob in a container.
Core
GA
az storage blob filter
List blobs across all containers whose tags match a given search expression.
Extension
Preview
az storage blob generate-sas
Generate a shared access signature for the blob.
Core
GA
az storage blob generate-sas (storage-blob-preview extension)
Generate a shared access signature for the blob.
Extension
GA
az storage blob immutability-policy
Manage blob immutability policy.
Core
GA
az storage blob immutability-policy delete
Delete blob's immutability policy.
Core
GA
az storage blob immutability-policy set
Set blob's immutability policy.
Core
GA
az storage blob incremental-copy
Manage blob incremental copy operations.
Core
GA
az storage blob incremental-copy cancel
Aborts a pending copy_blob operation, and leaves a destination blob with zero length and full metadata.
Core
GA
az storage blob incremental-copy start
Copies an incremental copy of a blob asynchronously.
Core
GA
az storage blob lease
Manage storage blob leases.
Core
GA
az storage blob lease acquire
Request a new lease.
Core
GA
az storage blob lease break
Break the lease, if the container or blob has an active lease.
Core
GA
az storage blob lease change
Change the lease ID of an active lease.
Core
GA
az storage blob lease release
Release the lease.
Core
GA
az storage blob lease renew
Renew the lease.
Core
GA
az storage blob list
List blobs in a given container.
Core
GA
az storage blob metadata
Manage blob metadata.
Core
GA
az storage blob metadata show
Return all user-defined metadata for the specified blob or snapshot.
Core
GA
az storage blob metadata update
Sets user-defined metadata for the blob as one or more name-value pairs.
Core
GA
az storage blob query
Enable users to select/project on blob or blob snapshot data by providing simple query expressions.
Core
Preview
az storage blob restore
Restore blobs in the specified blob ranges.
Core
GA
az storage blob rewrite
Create a new Block Blob where the content of the blob is read from a given URL.
Core
Preview
az storage blob service-properties
Manage storage blob service properties.
Core and Extension
GA
az storage blob service-properties delete-policy
Manage storage blob delete-policy service properties.
Core
GA
az storage blob service-properties delete-policy show
Show the storage blob delete-policy.
Core
GA
az storage blob service-properties delete-policy update
Update the storage blob delete-policy.
Core
GA
az storage blob service-properties show
Gets the properties of a storage account's Blob service, including Azure Storage Analytics.
Core
GA
az storage blob service-properties update
Update storage blob service properties.
Core
GA
az storage blob service-properties update (storage-blob-preview extension)
Update storage blob service properties.
Extension
GA
az storage blob set-legal-hold
Set blob legal hold.
Core
GA
az storage blob set-tier
Set the block or page tiers on the blob.
Core
GA
az storage blob set-tier (storage-blob-preview extension)
Set the block or page tiers on the blob.
Extension
GA
az storage blob show
Get the details of a blob.
Core
GA
az storage blob show (storage-blob-preview extension)
Get the details of a blob.
Extension
GA
az storage blob snapshot
Creates a snapshot of the blob.
Core
GA
az storage blob sync
Sync blobs recursively to a storage blob container.
Core
Preview
az storage blob tag
Manage blob tags.
Extension
Preview
az storage blob tag list
Get tags on a blob or specific blob version, or snapshot.
Extension
Preview
az storage blob tag set
Set tags on a blob or specific blob version, but not snapshot.
Extension
Preview
az storage blob undelete
Restore soft deleted blob or snapshot.
Core
GA
az storage blob update
Sets system properties on the blob.
Core
GA
az storage blob upload
Upload a file to a storage blob.
Core
GA
az storage blob upload-batch
Upload files from a local directory to a blob container.
Core
GA
az storage blob url
Create the url to access a blob.
Core
GA
az storage container
Manage blob storage containers.
Core and Extension
GA
az storage container-rm
Manage Azure containers using the Microsoft.Storage resource provider.
Core
GA
az storage container-rm create
Create a new container under the specified storage account.
Core
GA
az storage container-rm delete
Delete the specified container under its account.
Core
GA
az storage container-rm exists
Check for the existence of a container.
Core
GA
az storage container-rm list
List all containers under the specified storage account.
Core
GA
az storage container-rm migrate-vlw
Migrate a blob container from container level WORM to object level immutability enabled container.
Core
Preview
az storage container-rm show
Show the properties for a specified container.
Core
GA
az storage container-rm update
Update the properties for a container.
Core
GA
az storage container create
Create a container in a storage account.
Core
GA
az storage container delete
Mark the specified container for deletion.
Core
GA
az storage container exists
Check for the existence of a storage container.
Core
GA
az storage container generate-sas
Generate a SAS token for a storage container.
Core
GA
az storage container generate-sas (storage-blob-preview extension)
Generate a SAS token for a storage container.
Extension
GA
az storage container immutability-policy
Manage container immutability policies.
Core
GA
az storage container immutability-policy create
Create or update an unlocked immutability policy.
Core
GA
az storage container immutability-policy delete
Aborts an unlocked immutability policy.
Core
GA
az storage container immutability-policy extend
Extend the immutabilityPeriodSinceCreationInDays of a locked immutabilityPolicy.
Core
GA
az storage container immutability-policy lock
Sets the ImmutabilityPolicy to Locked state.
Core
GA
az storage container immutability-policy show
Gets the existing immutability policy along with the corresponding ETag in response headers and body.
Core
GA
az storage container lease
Manage blob storage container leases.
Core
GA
az storage container lease acquire
Request a new lease.
Core
GA
az storage container lease break
Break the lease, if the container has an active lease.
Core
GA
az storage container lease change
Change the lease ID of an active lease.
Core
GA
az storage container lease release
Release the lease.
Core
GA
az storage container lease renew
Renew the lease.
Core
GA
az storage container legal-hold
Manage container legal holds.
Core
GA
az storage container legal-hold clear
Clear legal hold tags.
Core
GA
az storage container legal-hold set
Set legal hold tags.
Core
GA
az storage container legal-hold show
Get the legal hold properties of a container.
Core
GA
az storage container list
List containers in a storage account.
Core
GA
az storage container metadata
Manage container metadata.
Core
GA
az storage container metadata show
Return all user-defined metadata for the specified container.
Core
GA
az storage container metadata update
Set one or more user-defined name-value pairs for the specified container.
Core
GA
az storage container policy
Manage container stored access policies.
Core
GA
az storage container policy create
Create a stored access policy on the containing object.
Core
GA
az storage container policy delete
Delete a stored access policy on a containing object.
Core
GA
az storage container policy list
List stored access policies on a containing object.
Core
GA
az storage container policy show
Show a stored access policy on a containing object.
Core
GA
az storage container policy update
Set a stored access policy on a containing object.
Core
GA
az storage container restore
Restore soft-deleted container.
Core
GA
az storage container set-permission
Set the permissions for the specified container.
Core
GA
az storage container show
Return all user-defined metadata and system properties for the specified container.
Core
GA
az storage container show-permission
Get the permissions for the specified container.
Core
GA
az storage copy
Copy files or directories to or from Azure storage.
Core
GA
az storage cors
Manage storage service Cross-Origin Resource Sharing (CORS).
Core
GA
az storage cors add
Add a CORS rule to a storage account.
Core
GA
az storage cors clear
Remove all CORS rules from a storage account.
Core
GA
az storage cors list
List all CORS rules for a storage account.
Core
GA
az storage directory
Manage file storage directories.
Core and Extension
GA
az storage directory create
Create a new directory under the specified share or parent directory.
Core
GA
az storage directory create (storage-preview extension)
Create a new directory under the specified share or parent directory.
Extension
GA
az storage directory delete
Delete the specified empty directory.
Core
GA
az storage directory delete (storage-preview extension)
Delete the specified empty directory.
Extension
GA
az storage directory exists
Check for the existence of a storage directory.
Core
GA
az storage directory exists (storage-preview extension)
Check for the existence of a storage directory.
Extension
GA
az storage directory list
List directories in a share.
Core
GA
az storage directory list (storage-preview extension)
List directories in a share.
Extension
GA
az storage directory metadata
Manage file storage directory metadata.
Core and Extension
GA
az storage directory metadata show
Get all user-defined metadata for the specified directory.
Core
GA
az storage directory metadata show (storage-preview extension)
Get all user-defined metadata for the specified directory.
Extension
GA
az storage directory metadata update
Set one or more user-defined name-value pairs for the specified directory.
Core
GA
az storage directory metadata update (storage-preview extension)
Set one or more user-defined name-value pairs for the specified directory.
Extension
GA
az storage directory show
Get all user-defined metadata and system properties for the specified directory.
Core
GA
az storage directory show (storage-preview extension)
Get all user-defined metadata and system properties for the specified directory.
Extension
GA
az storage entity
Manage table storage entities.
Core
GA
az storage entity delete
Delete an existing entity in a table.
Core
GA
az storage entity insert
Insert an entity into a table.
Core
GA
az storage entity merge
Update an existing entity by merging the entity's properties.
Core
GA
az storage entity query
List entities which satisfy a query.
Core
GA
az storage entity replace
Update an existing entity in a table.
Core
GA
az storage entity show
Get a single entity in a table.
Core
GA
az storage file
Manage file shares.
Core and Extension
GA
az storage file copy
Manage file copy operations.
Core and Extension
GA
az storage file copy cancel
Abort an ongoing copy operation.
Core
GA
az storage file copy cancel (storage-preview extension)
Abort an ongoing copy operation.
Extension
GA
az storage file copy start
Copy a file asynchronously.
Core
GA
az storage file copy start (storage-preview extension)
Copy a file asynchronously.
Extension
GA
az storage file copy start-batch
Copy multiple files or blobs to a file share.
Core
GA
az storage file copy start-batch (storage-preview extension)
Copy multiple files or blobs to a file share.
Extension
GA
az storage file delete
Mark the specified file for deletion.
Core
GA
az storage file delete (storage-preview extension)
Mark the specified file for deletion.
Extension
GA
az storage file delete-batch
Delete files from an Azure Storage File Share.
Core
GA
az storage file delete-batch (storage-preview extension)
Delete files from an Azure Storage File Share.
Extension
GA
az storage file download
Download a file to a file path, with automatic chunking and progress notifications.
Core
GA
az storage file download (storage-preview extension)
Download a file to a file path, with automatic chunking and progress notifications.
Extension
GA
az storage file download-batch
Download files from an Azure Storage File Share to a local directory in a batch operation.
Core
GA
az storage file download-batch (storage-preview extension)
Download files from an Azure Storage File Share to a local directory in a batch operation.
Extension
GA
az storage file exists
Check for the existence of a file.
Core
GA
az storage file exists (storage-preview extension)
Check for the existence of a file.
Extension
GA
az storage file generate-sas
Generate a shared access signature for the file.
Core
GA
az storage file generate-sas (storage-preview extension)
Generate a shared access signature for the file.
Extension
GA
az storage file hard-link
Manage storage file hard-link.
Core
GA
az storage file hard-link create
NFS only. Create a hard link to the file specified by path.
Core
GA
az storage file list
List files and directories in a share.
Core
GA
az storage file list (storage-preview extension)
List files and directories in a share.
Extension
GA
az storage file metadata
Manage file metadata.
Core and Extension
GA
az storage file metadata show
Return all user-defined metadata for the file.
Core
GA
az storage file metadata show (storage-preview extension)
Return all user-defined metadata for the file.
Extension
GA
az storage file metadata update
Update file metadata.
Core
GA
az storage file metadata update (storage-preview extension)
Update file metadata.
Extension
GA
az storage file resize
Resize a file to the specified size.
Core
GA
az storage file resize (storage-preview extension)
Resize a file to the specified size.
Extension
GA
az storage file show
Return all user-defined metadata, standard HTTP properties, and system properties for the file.
Core
GA
az storage file show (storage-preview extension)
Return all user-defined metadata, standard HTTP properties, and system properties for the file.
Extension
GA
az storage file symbolic-link
Manage storage file symbolic-link.
Core
GA
az storage file symbolic-link create
NFS only. Creates a symbolic link to the specified file.
Core
GA
az storage file symbolic-link show
NFS only. Gets the symbolic link for the file client.
Core
GA
az storage file update
Set system properties on the file.
Core
GA
az storage file update (storage-preview extension)
Set system properties on the file.
Extension
GA
az storage file upload
Upload a file to a share.
Core
GA
az storage file upload (storage-preview extension)
Upload a file to a share that uses the SMB 3.0 protocol.
Extension
GA
az storage file upload-batch
Upload files from a local directory to an Azure Storage File Share in a batch operation.
Core
GA
az storage file upload-batch (storage-preview extension)
Upload files from a local directory to an Azure Storage File Share in a batch operation.
Extension
GA
az storage file url
Create the url to access a file.
Core
GA
az storage file url (storage-preview extension)
Create the url to access a file.
Extension
GA
az storage fs
Manage file systems in Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs access
Manage file system access and permissions for Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs access remove-recursive
Remove the Access Control on a path and sub-paths in Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs access set
Set the access control properties of a path(directory or file) in Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs access set-recursive
Set the Access Control on a path and sub-paths in Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs access show
Show the access control properties of a path (directory or file) in Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs access update-recursive
Modify the Access Control on a path and sub-paths in Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs create
Create file system for Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs delete
Delete a file system in ADLS Gen2 account.
Core
GA
az storage fs directory
Manage directories in Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs directory create
Create a directory in ADLS Gen2 file system.
Core
GA
az storage fs directory delete
Delete a directory in ADLS Gen2 file system.
Core
GA
az storage fs directory download
Download files from the directory in ADLS Gen2 file system to a local file path.
Core
Preview
az storage fs directory exists
Check for the existence of a directory in ADLS Gen2 file system.
Core
GA
az storage fs directory generate-sas
Generate a SAS token for directory in ADLS Gen2 account.
Core
GA
az storage fs directory list
List directories in ADLS Gen2 file system.
Core
GA
az storage fs directory metadata
Manage the metadata for directory in file system.
Core
GA
az storage fs directory metadata show
Return all user-defined metadata for the specified directory.
Core
GA
az storage fs directory metadata update
Sets one or more user-defined name-value pairs for the specified file system.
Core
GA
az storage fs directory move
Move a directory in ADLS Gen2 file system.
Core
GA
az storage fs directory show
Show properties of a directory in ADLS Gen2 file system.
Core
GA
az storage fs directory upload
Upload files or subdirectories to a directory in ADLS Gen2 file system.
Core
Preview
az storage fs exists
Check for the existence of a file system in ADLS Gen2 account.
Core
GA
az storage fs file
Manage files in Azure Data Lake Storage Gen2 account.
Core
GA
az storage fs file append
Append content to a file in ADLS Gen2 file system.
Core
GA
az storage fs file create
Create a new file in ADLS Gen2 file system.
Core
GA
az storage fs file delete
Delete a file in ADLS Gen2 file system.
Core
GA
az storage fs file download
Download a file from the specified path in ADLS Gen2 file system.
Core
GA
az storage fs file exists
Check for the existence of a file in ADLS Gen2 file system.
Core
GA
az storage fs file generate-sas
Generate a SAS token for file in ADLS Gen2 account.
Core
GA
az storage fs file list
List files and directories in ADLS Gen2 file system.
Core
GA
az storage fs file metadata
Manage the metadata for file in file system.
Core
GA
az storage fs file metadata show
Return all user-defined metadata for the specified file.
Core
GA
az storage fs file metadata update
Sets one or more user-defined name-value pairs for the specified file system.
Core
GA
az storage fs file move
Move a file in ADLS Gen2 Account.
Core
GA
az storage fs file set-expiry
Sets the time a file will expire and be deleted.
Core
GA
az storage fs file show
Show properties of file in ADLS Gen2 file system.
Core
GA
az storage fs file upload
Upload a file to a file path in ADLS Gen2 file system.
Core
GA
az storage fs generate-sas
Generate a SAS token for file system in ADLS Gen2 account.
Core
Preview
az storage fs list
List file systems in ADLS Gen2 account.
Core
GA
az storage fs list-deleted-path
List the deleted (file or directory) paths under the specified file system.
Core
GA
az storage fs metadata
Manage the metadata for file system.
Core
GA
az storage fs metadata show
Return all user-defined metadata for the specified file system.
Core
GA
az storage fs metadata update
Sets one or more user-defined name-value pairs for the specified file system.
Core
GA
az storage fs service-properties
Manage storage datalake service properties.
Core
GA
az storage fs service-properties show
Show the properties of a storage account's datalake service, including Azure Storage Analytics.
Core
GA
az storage fs service-properties update
Update the properties of a storage account's datalake service, including Azure Storage Analytics.
Core
GA
az storage fs show
Show properties of file system in ADLS Gen2 account.
Core
GA
az storage fs undelete-path
Restore soft-deleted path.
Core
GA
az storage logging
Manage storage service logging information.
Core
GA
az storage logging off
Turn off logging for a storage account.
Core
Preview
az storage logging show
Show logging settings for a storage account.
Core
GA
az storage logging update
Update logging settings for a storage account.
Core
GA
az storage message
Manage queue storage messages.
Core
Preview
az storage message clear
Delete all messages from the specified queue.
Core
Preview
az storage message delete
Delete the specified message.
Core
Preview
az storage message get
Retrieve one or more messages from the front of the queue.
Core
Preview
az storage message peek
Retrieve one or more messages from the front of the queue, but do not alter the visibility of the message.
Core
Preview
az storage message put
Add a new message to the back of the message queue.
Core
Preview
az storage message update
Update the visibility timeout of a message.
Core
Preview
az storage metrics
Manage storage service metrics.
Core
GA
az storage metrics show
Show metrics settings for a storage account.
Core
GA
az storage metrics update
Update metrics settings for a storage account.
Core
GA
az storage queue
Manage storage queues.
Core
Preview
az storage queue create
Create a queue under the given account.
Core
Preview
az storage queue delete
Delete the specified queue and any messages it contains.
Core
Preview
az storage queue exists
Return a boolean indicating whether the queue exists.
Core
Preview
az storage queue generate-sas
Generate a shared access signature for the queue.Use the returned signature with the sas_token parameter of QueueService.
Core
Preview
az storage queue list
List queues in a storage account.
Core
Preview
az storage queue metadata
Manage the metadata for a storage queue.
Core
Preview
az storage queue metadata show
Return all user-defined metadata for the specified queue.
Core
Preview
az storage queue metadata update
Set user-defined metadata on the specified queue.
Core
Preview
az storage queue policy
Manage shared access policies for a storage queue.
Core
Preview
az storage queue policy create
Create a stored access policy on the containing object.
Core
Preview
az storage queue policy delete
Delete a stored access policy on a containing object.
Core
Preview
az storage queue policy list
List stored access policies on a containing object.
Core
Preview
az storage queue policy show
Show a stored access policy on a containing object.
Core
Preview
az storage queue policy update
Set a stored access policy on a containing object.
Core
Preview
az storage queue stats
Retrieve statistics related to replication for the Queue service. It is only available when read-access geo-redundant replication is enabled for the storage account.
Core
Preview
az storage remove
Delete blobs or files from Azure Storage.
Core
GA
az storage share
Manage file shares.
Core and Extension
GA
az storage share-rm
Manage Azure file shares using the Microsoft.Storage resource provider.
Core
GA
az storage share-rm create
Create a new share under the specified account as described by request body. The share resource includes metadata and properties for that share. It does not include a list of the files contained by the share.
Core
GA
az storage share-rm delete
Delete the specified Azure file share or share snapshot.
Core
GA
az storage share-rm exists
Check for the existence of an Azure file share.
Core
GA
az storage share-rm list
List all shares.
Core
GA
az storage share-rm restore
Restore a file share within a valid retention days if share soft delete is enabled.
Core
GA
az storage share-rm show
Show the properties for a specified Azure file share or share snapshot.
Core
GA
az storage share-rm snapshot
Create a snapshot of an existing share under the specified account.
Core
Preview
az storage share-rm stats
Get the usage bytes of the data stored on the share.
Core
GA
az storage share-rm update
Update a new share under the specified account as described by request body. The share resource includes metadata and properties for that share. It does not include a list of the files contained by the share.
Core
GA
az storage share close-handle
Close file handles of a file share.
Core
GA
az storage share close-handle (storage-preview extension)
Close file handles of a file share.
Extension
GA
az storage share create
Creates a new share under the specified account.
Core
GA
az storage share delete
Mark the specified share for deletion.
Core
GA
az storage share exists
Check for the existence of a file share.
Core
GA
az storage share generate-sas
Generate a shared access signature for the share.
Core
GA
az storage share list
List the file shares in a storage account.
Core
GA
az storage share list-handle
List file handles of a file share.
Core
GA
az storage share list-handle (storage-preview extension)
List file handles of a file share.
Extension
GA
az storage share metadata
Manage the metadata of a file share.
Core
GA
az storage share metadata show
Return all user-defined metadata for the specified share.
Core
GA
az storage share metadata update
Set one or more user-defined name-value pairs for the specified share.
Core
GA
az storage share policy
Manage shared access policies of a storage file share.
Core
GA
az storage share policy create
Create a stored access policy on the containing object.
Core
GA
az storage share policy delete
Delete a stored access policy on a containing object.
Core
GA
az storage share policy list
List stored access policies on a containing object.
Core
GA
az storage share policy show
Show a stored access policy on a containing object.
Core
GA
az storage share policy update
Set a stored access policy on a containing object.
Core
GA
az storage share show
Return all user-defined metadata and system properties for the specified share.
Core
GA
az storage share snapshot
Create a snapshot of an existing share under the specified account.
Core
GA
az storage share stats
Get the approximate size of the data stored on the share, rounded up to the nearest gigabyte.
Core
GA
az storage share update
Set service-defined properties for the specified share.
Core
GA
az storage share url
Create a URI to access a file share.
Core
GA
az storage sku
Manage Sku.
Core
GA
az storage sku list
List the available SKUs supported by Microsoft.Storage for given subscription.
Core
GA
az storage table
Manage NoSQL key-value storage.
Core
GA
az storage table create
Create a new table in the storage account.
Core
GA
az storage table delete
Delete the specified table and any data it contains.
Core
GA
az storage table exists
Return a boolean indicating whether the table exists.
Core
GA
az storage table generate-sas
Generate a shared access signature for the table.
Core
GA
az storage table list
List tables in a storage account.
Core
GA
az storage table policy
Manage shared access policies of a storage table.
Core
GA
az storage table policy create
Create a stored access policy on the containing object.
Core
GA
az storage table policy delete
Delete a stored access policy on a containing object.
Core
GA
az storage table policy list
List stored access policies on a containing object.
Core
GA
az storage table policy show
Show a stored access policy on a containing object.
Core
GA
az storage table policy update
Set a stored access policy on a containing object.
Core
GA
az storage table stats
Retrieves statistics related to replication for the Table service.
Core
GA
az storage copy
Edit
Copy files or directories to or from Azure storage.
```
az storage copy [--account-key]
                [--account-name]
                [--acquire-policy-token]
                [--auth-mode {key, login}]
                [--blob-type {AppendBlob, BlockBlob, PageBlob}]
                [--cap-mbps]
                [--change-reference]
                [--connection-string]
                [--content-type]
                [--destination]
                [--destination-account-name]
                [--destination-blob]
                [--destination-container]
                [--destination-file-path]
                [--destination-local-path]
                [--destination-share]
                [--exclude-path]
                [--exclude-pattern]
                [--follow-symlinks]
                [--include-path]
                [--include-pattern]
                [--preserve-s2s-access-tier {false, true}]
                [--put-md5]
                [--recursive]
                [--sas-token]
                [--service-endpoint]
                [--source]
                [--source-account-key]
                [--source-account-name]
                [--source-blob]
                [--source-connection-string --src-conn]
                [--source-container]
                [--source-file-path]
                [--source-local-path]
                [--source-sas]
                [--source-share]
                []
```
Examples
Upload a single file to Azure Blob using url.
```
az storage copy -s /path/to/file.txt -d https://[account].blob.core.windows.net/[container]/[path/to/blob]
```
Upload a single file to Azure Blob using account name and container name.
```
az storage copy -s /path/to/file.txt --destination-account-name mystorageaccount --destination-container mycontainer
```
Upload a single file to Azure Blob with MD5 hash of the file content and save it as the blob's Content-MD5 property.
```
az storage copy -s /path/to/file.txt -d https://[account].blob.core.windows.net/[container]/[path/to/blob] --put-md5
```
Upload an entire directory to Azure Blob using url.
```
az storage copy -s /path/to/dir -d https://[account].blob.core.windows.net/[container]/[path/to/directory] --recursive
```
Upload an entire directory to Azure Blob using account name and container name.
```
az storage copy -s /path/to/dir --destination-account-name mystorageaccount --destination-container mycontainer --recursive
```
Upload a set of files to Azure Blob using wildcards with url.
```
az storage copy -s /path/*foo/*bar/*.pdf -d https://[account].blob.core.windows.net/[container]/[path/to/directory]
```
Upload a set of files to Azure Blob using wildcards with account name and container name.
```
az storage copy -s /path/*foo/*bar/*.pdf --destination-account-name mystorageaccount --destination-container mycontainer
```
Upload files and directories to Azure Blob using wildcards with url.
```
az storage copy -s /path/*foo/*bar* -d https://[account].blob.core.windows.net/[container]/[path/to/directory] --recursive
```
Upload files and directories to Azure Blob using wildcards with account name and container name.
```
az storage copy -s /path/*foo/*bar* --destination-account-name mystorageaccount --destination-container mycontainer --recursive
```
Download a single file from Azure Blob using url, and you can also specify your storage account and container information as above.
```
az storage copy -s https://[account].blob.core.windows.net/[container]/[path/to/blob] -d /path/to/file.txt
```
Download an entire directory from Azure Blob, and you can also specify your storage account and container information as above.
```
az storage copy -s https://[account].blob.core.windows.net/[container]/[path/to/directory] -d /path/to/dir --recursive
```
Download a subset of containers within a storage account by using a wildcard symbol (*) in the container name, and you can also specify your storage account and container information as above.
```
az storage copy -s https://[account].blob.core.windows.net/[container*name] -d /path/to/dir --recursive
```
Download a subset of files from Azure Blob. (Only jpg files and file names don't start with test will be included.)
```
az storage copy -s https://[account].blob.core.windows.net/[container] --include-pattern "*.jpg" --exclude-pattern test* -d /path/to/dir --recursive
```
Copy a single blob to another blob, and you can also specify the storage account and container information of source and destination as above.
```
az storage copy -s https://[srcaccount].blob.core.windows.net/[container]/[path/to/blob] -d https://[destaccount].blob.core.windows.net/[container]/[path/to/blob]
```
Copy an entire account data from blob account to another blob account, and you can also specify the storage account and container information of source and destination as above.
```
az storage copy -s https://[srcaccount].blob.core.windows.net -d https://[destaccount].blob.core.windows.net --recursive
```
Copy a single object from S3 with access key to blob, and you can also specify your storage account and container information as above.
```
az storage copy -s https://s3.amazonaws.com/[bucket]/[object] -d https://[destaccount].blob.core.windows.net/[container]/[path/to/blob]
```
Copy an entire directory from S3 with access key to blob virtual directory, and you can also specify your storage account and container information as above.
```
az storage copy -s https://s3.amazonaws.com/[bucket]/[folder] -d https://[destaccount].blob.core.windows.net/[container]/[path/to/directory] --recursive
```
Copy all buckets in S3 service with access key to blob account, and you can also specify your storage account information as above.
```
az storage copy -s https://s3.amazonaws.com/ -d https://[destaccount].blob.core.windows.net --recursive
```
Copy all buckets in a S3 region with access key to blob account, and you can also specify your storage account information as above.
```
az storage copy -s https://s3-[region].amazonaws.com/ -d https://[destaccount].blob.core.windows.net --recursive
```
Upload a single file to Azure File Share using url.
```
az storage copy -s /path/to/file.txt -d https://[account].file.core.windows.net/[share]/[path/to/file]
```
Upload a single file to Azure File Share using account name and share name.
```
az storage copy -s /path/to/file.txt --destination-account-name mystorageaccount --destination-share myshare
```
Upload an entire directory to Azure File Share using url.
```
az storage copy -s /path/to/dir -d https://[account].file.core.windows.net/[share]/[path/to/directory] --recursive
```
Upload an entire directory to Azure File Share using account name and container name.
```
az storage copy -s /path/to/dir --destination-account-name mystorageaccount --destination-share myshare --recursive
```
Upload a set of files to Azure File Share using wildcards with account name and share name.
```
az storage copy -s /path/*foo/*bar/*.pdf --destination-account-name mystorageaccount --destination-share myshare
```
Upload files and directories to Azure File Share using wildcards with url.
```
az storage copy -s /path/*foo/*bar* -d https://[account].file.core.windows.net/[share]/[path/to/directory] --recursive
```
Upload files and directories to Azure File Share using wildcards with account name and share name.
```
az storage copy -s /path/*foo/*bar* --destination-account-name mystorageaccount --destination-share myshare --recursive
```
Download a single file from Azure File Share using url, and you can also specify your storage account and share information as above.
```
az storage copy -s https://[account].file.core.windows.net/[share]/[path/to/file] -d /path/to/file.txt
```
Download an entire directory from Azure File Share, and you can also specify your storage account and share information as above.
```
az storage copy -s https://[account].file.core.windows.net/[share]/[path/to/directory] -d /path/to/dir --recursive
```
Download a set of files from Azure File Share using wildcards, and you can also specify your storage account and share information as above.
```
az storage copy -s https://[account].file.core.windows.net/[share]/ --include-pattern foo* -d /path/to/dir --recursive
```
Upload a single file to Azure Blob using url with azcopy options pass-through.
```
az storage copy -s /path/to/file.txt -d https://[account].blob.core.windows.net/[container]/[path/to/blob] -- --block-size-mb=0.25 --check-length
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--account-key
Storage account key. Must be used in conjunction with storage account name or service endpoint. Environment variable: AZURE_STORAGE_KEY.
Property
Value
Parameter group:
Storage Account Arguments
--account-name
Storage account name of copy destination.
Property
Value
Parameter group:
Storage Account Arguments
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--auth-mode
The mode in which to run the command. "login" mode will directly use your login credentials for the authentication. The legacy "key" mode will attempt to query for an account key if no authentication parameters for the account are provided. Environment variable: AZURE_STORAGE_AUTH_MODE.
Property
Value
Accepted values:
key, login
--blob-type
The type of blob at the destination.
Property
Value
Parameter group:
Additional Flags Arguments
Accepted values:
AppendBlob, BlockBlob, PageBlob
--cap-mbps
Caps the transfer rate, in megabits per second. Moment-by-moment throughput might vary slightly from the cap. If this option is set to zero, or it is omitted, the throughput isn't capped.
Property
Value
Parameter group:
Additional Flags Arguments
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--connection-string
Storage account connection string. Environment variable: AZURE_STORAGE_CONNECTION_STRING.
Property
Value
Parameter group:
Storage Account Arguments
--content-type
Specify content type of the file.
Property
Value
Parameter group:
Additional Flags Arguments
--destination -d
The path/url of copy destination. It can be a local path, an url to azure storage server. If you provide destination parameter here, you do not need to provide arguments in copy destination arguments group and copy destination arguments will be deprecated in future.
--destination-account-name
Deprecated
Storage account name of copy destination.
Property
Value
Parameter group:
Storage Account Arguments
--destination-blob
Blob name in blob container of copy destination storage account.
Property
Value
Parameter group:
Copy destination Arguments
--destination-container
Container name of copy destination storage account.
Property
Value
Parameter group:
Copy destination Arguments
--destination-file-path
File path in file share of copy destination storage account.
Property
Value
Parameter group:
Copy destination Arguments
--destination-local-path
Deprecated
The path/url of copy destination. It can be a local path, an url to azure storage server. If you provide destination parameter here, you do not need to provide arguments in copy destination arguments group and copy destination arguments will be deprecated in future.
--destination-share
File share name of copy destination storage account.
Property
Value
Parameter group:
Copy destination Arguments
--exclude-path
Exclude these paths. This option does not support wildcard characters (*). Checks relative path prefix. For example: myFolder;myFolder/subDirName/file.pdf.
Property
Value
Parameter group:
Additional Flags Arguments
--exclude-pattern
Exclude these files where the name matches the pattern list. For example:
.jpg;
.pdf;exactName. This option supports wildcard characters (*).
Property
Value
Parameter group:
Additional Flags Arguments
--follow-symlinks
Follow symbolic links when uploading from local file system.
Property
Value
Parameter group:
Additional Flags Arguments
--include-path
Include only these paths. This option does not support wildcard characters (*). Checks relative path prefix. For example:myFolder;myFolder/subDirName/file.pdf.
Property
Value
Parameter group:
Additional Flags Arguments
--include-pattern
Include only these files where the name matches the pattern list. For example:
.jpg;
.pdf;exactName. This option supports wildcard characters (*).
Property
Value
Parameter group:
Additional Flags Arguments
--preserve-s2s-access-tier
Preserve access tier during service to service copy. Please refer to
https://learn.microsoft.com/azure/storage/blobs/storage-blob-storage-tiers
to ensure destination storage account support setting access tier. In the cases that setting access tier is not supported, please use
--preserve-s2s-access-tier false
to bypass copying access tier. (Default true).
Property
Value
Parameter group:
Additional Flags Arguments
Accepted values:
false, true
--put-md5
Create an MD5 hash of each file, and save the hash as the Content-MD5 property of the destination blob/file.Only available when uploading.
Property
Value
Parameter group:
Additional Flags Arguments
--recursive -r
Look into sub-directories recursively.
--sas-token
A Shared Access Signature (SAS). Must be used in conjunction with storage account name or service endpoint. Environment variable: AZURE_STORAGE_SAS_TOKEN.
Property
Value
Parameter group:
Storage Account Arguments
--service-endpoint
Storage data service endpoint. Must be used in conjunction with either storage account key or a SAS token. You can find each service primary endpoint with
az storage account show
. Environment variable: AZURE_STORAGE_SERVICE_ENDPOINT.
Property
Value
Parameter group:
Storage Account Arguments
--source -s
The path/url of copy source. It can be a local path, an url to azure storage server or AWS S3 buckets. If you provide source parameter here, you do not need to provide arguments in copy source arguments group and copy source arguments will be deprecated in future.
--source-account-key
Account key of copy source storage account. Must be used in conjunction with source storage account name.
Property
Value
Parameter group:
Copy source Arguments
--source-account-name
Account name of copy source storage account.
Property
Value
Parameter group:
Copy source Arguments
--source-blob
Blob name in blob container of copy source storage account.
Property
Value
Parameter group:
Copy source Arguments
--source-connection-string --src-conn
Connection string of source storage account.
Property
Value
Parameter group:
Copy source Arguments
--source-container
Container name of copy source storage account.
Property
Value
Parameter group:
Copy source Arguments
--source-file-path
File path in file share of copy source storage account.
Property
Value
Parameter group:
Copy source Arguments
--source-local-path
Deprecated
The path/url of copy source. It can be a local path, an url to azure storage server or AWS S3 buckets. If you provide source parameter here, you do not need to provide arguments in copy source arguments group and copy source arguments will be deprecated in future.
--source-sas
Shared Access Signature (SAS) token of copy source. Must be used in conjunction with source storage account name.
Property
Value
Parameter group:
Copy source Arguments
--source-share
File share name of copy source storage account.
Property
Value
Parameter group:
Copy source Arguments
<EXTRA_OPTIONS>
Experimental
Other options which will be passed through to azcopy as it is. Please put all the extra options after a
--
.
Property
Value
Parameter group:
Positional
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
az storage remove
Edit
Delete blobs or files from Azure Storage.
```
az storage remove [--account-key]
                  [--account-name]
                  [--acquire-policy-token]
                  [--auth-mode {key, login}]
                  [--change-reference]
                  [--connection-string]
                  [--container-name]
                  [--exclude-path]
                  [--exclude-pattern]
                  [--include-path]
                  [--include-pattern]
                  [--name]
                  [--path]
                  [--recursive]
                  [--sas-token]
                  [--service-endpoint]
                  [--share-name]
```
Examples
Remove a single blob.
```
az storage remove -c mycontainer -n MyBlob
```
Remove an entire virtual directory.
```
az storage remove -c mycontainer -n path/to/directory --recursive
```
Remove only the top blobs inside a virtual directory but not its sub-directories.
```
az storage remove -c mycontainer --recursive
```
Remove all the blobs in a Storage Container.
```
az storage remove -c mycontainer -n path/to/directory
```
Remove a subset of blobs in a virtual directory (For example, only jpg and pdf files, or if the blob name is "exactName" and file names don't start with "test").
```
az storage remove -c mycontainer --include-path path/to/directory --include-pattern "*.jpg;*.pdf;exactName" --exclude-pattern "test*" --recursive
```
Remove an entire virtual directory but exclude certain blobs from the scope (For example, every blob that starts with foo or ends with bar).
```
az storage remove -c mycontainer --include-path path/to/directory --exclude-pattern "foo*;*bar" --recursive
```
Remove a single file.
```
az storage remove -s MyShare -p MyFile
```
Remove an entire directory.
```
az storage remove -s MyShare -p path/to/directory --recursive
```
Remove all the files in a Storage File Share.
```
az storage remove -s MyShare --recursive
```
Optional Parameters
The following parameters are optional, but depending on the context, one or more might become required for the command to execute successfully.
--account-key
Storage account key. Must be used in conjunction with storage account name or service endpoint. Environment variable: AZURE_STORAGE_KEY.
Property
Value
Parameter group:
Storage Account Arguments
--account-name
Storage account name. Related environment variable: AZURE_STORAGE_ACCOUNT. Must be used in conjunction with either storage account key or a SAS token. If neither are present, the command will try to query the storage account key using the authenticated Azure account. If a large number of storage commands are executed the API quota may be hit.
Property
Value
Parameter group:
Storage Account Arguments
--acquire-policy-token
Acquiring an Azure Policy token automatically for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--auth-mode
The mode in which to run the command. "login" mode will directly use your login credentials for the authentication. The legacy "key" mode will attempt to query for an account key if no authentication parameters for the account are provided. Environment variable: AZURE_STORAGE_AUTH_MODE.
Property
Value
Accepted values:
key, login
--change-reference
The related change reference ID for this resource operation.
Property
Value
Parameter group:
Global Policy Arguments
--connection-string
Storage account connection string. Environment variable: AZURE_STORAGE_CONNECTION_STRING.
Property
Value
Parameter group:
Storage Account Arguments
--container-name -c
The container name.
--exclude-path
Exclude these paths. This option does not support wildcard characters (*). Checks relative path prefix. For example: myFolder;myFolder/subDirName/file.pdf.
Property
Value
Parameter group:
Additional Flags Arguments
--exclude-pattern
Exclude these files where the name matches the pattern list. For example:
.jpg;
.pdf;exactName. This option supports wildcard characters (*).
Property
Value
Parameter group:
Additional Flags Arguments
--include-path
Include only these paths. This option does not support wildcard characters (*). Checks relative path prefix. For example:myFolder;myFolder/subDirName/file.pdf.
Property
Value
Parameter group:
Additional Flags Arguments
--include-pattern
Include only these files where the name matches the pattern list. For example:
.jpg;
.pdf;exactName. This option supports wildcard characters (*).
Property
Value
Parameter group:
Additional Flags Arguments
--name -n
The blob name.
--path -p
The path to the file within the file share.
--recursive -r
Look into sub-directories recursively.
--sas-token
A Shared Access Signature (SAS). Must be used in conjunction with storage account name or service endpoint. Environment variable: AZURE_STORAGE_SAS_TOKEN.
Property
Value
Parameter group:
Storage Account Arguments
--service-endpoint
Storage data service endpoint. Must be used in conjunction with either storage account key or a SAS token. You can find each service primary endpoint with
az storage account show
. Environment variable: AZURE_STORAGE_SERVICE_ENDPOINT.
Property
Value
Parameter group:
Storage Account Arguments
--share-name -s
The file share name.
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