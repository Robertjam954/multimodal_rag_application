<!-- source: https://learn.microsoft.com/en-us/cli/azure/ad?view=azure-cli-latest -->

# az ad

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
az ad
Note
This command group has commands that are defined in both Azure CLI and at least one extension. Install each extension to benefit from its extended capabilities.
Learn more
about extensions.
Manage Microsoft Entra ID (formerly known as Azure Active Directory, Azure AD, AAD) entities needed for Azure role-based access control (Azure RBAC) through Microsoft Graph API.
Commands
Name
Description
Type
Status
az ad app
Manage Microsoft Entra applications.
Core
GA
az ad app create
Create an application.
Core
GA
az ad app credential
Manage an application's password or certificate credentials.
Core
GA
az ad app credential delete
Delete an application's password or certificate credentials.
Core
GA
az ad app credential list
List an application's password or certificate credential metadata. (The content of the password or certificate credential is not retrievable.).
Core
GA
az ad app credential reset
Reset an application's password or certificate credentials.
Core
GA
az ad app delete
Delete an application.
Core
GA
az ad app federated-credential
Manage application federated identity credentials.
Core
GA
az ad app federated-credential create
Create application federated identity credential.
Core
GA
az ad app federated-credential delete
Delete application federated identity credential.
Core
GA
az ad app federated-credential list
List application federated identity credentials.
Core
GA
az ad app federated-credential show
Show application federated identity credential.
Core
GA
az ad app federated-credential update
Update application federated identity credential.
Core
GA
az ad app list
List applications.
Core
GA
az ad app owner
Manage application owners.
Core
GA
az ad app owner add
Add an application owner.
Core
GA
az ad app owner list
List application owners.
Core
GA
az ad app owner remove
Remove an application owner.
Core
GA
az ad app permission
Manage an application's OAuth2 permissions.
Core
GA
az ad app permission add
Add an API permission.
Core
GA
az ad app permission admin-consent
Grant Application & Delegated permissions through admin-consent.
Core
GA
az ad app permission delete
Remove an API permission.
Core
GA
az ad app permission grant
Grant the app an API Delegated permissions.
Core
GA
az ad app permission list
List API permissions the application has requested.
Core
GA
az ad app permission list-grants
List Oauth2 permission grants.
Core
GA
az ad app show
Get the details of an application.
Core
GA
az ad app update
Update an application.
Core
GA
az ad ds
Manage domain service with azure active directory.
Extension
Experimental
az ad ds create
Create a new domain service with the specified parameters.
Extension
Experimental
az ad ds delete
The Delete Domain Service operation deletes an existing Domain Service.
Extension
Experimental
az ad ds list
List domain services in resource group or in subscription.
Extension
Experimental
az ad ds show
Get the specified domain service.
Extension
Experimental
az ad ds update
Update the existing deployment properties for domain service.
Extension
Experimental
az ad ds wait
Place the CLI in a waiting state until a condition of the ad ds is met.
Extension
Experimental
az ad group
Manage Microsoft Entra groups.
Core
GA
az ad group create
Create a group.
Core
GA
az ad group delete
Delete a group.
Core
GA
az ad group get-member-groups
Get a collection of object IDs of groups of which the specified group is a member.
Core
GA
az ad group list
List groups in the directory.
Core
GA
az ad group member
Manage group members.
Core
GA
az ad group member add
Add a member to a group.
Core
GA
az ad group member check
Check if a member is in a group.
Core
GA
az ad group member list
Get the members of a group.
Core
GA
az ad group member remove
Remove a member from a group.
Core
GA
az ad group owner
Manage group owners.
Core
GA
az ad group owner add
Add a group owner.
Core
GA
az ad group owner list
List group owners.
Core
GA
az ad group owner remove
Remove a group owner.
Core
GA
az ad group show
Get the details of a group.
Core
GA
az ad signed-in-user
Show graph information about current signed-in user in CLI.
Core
GA
az ad signed-in-user list-owned-objects
Get the list of directory objects that are owned by the user.
Core
GA
az ad signed-in-user show
Get the details for the currently logged-in user.
Core
GA
az ad sp
Manage Microsoft Entra service principals.
Core
GA
az ad sp create
Create a service principal.
Core
GA
az ad sp create-for-rbac
Create an application and its associated service principal, optionally configure the service principal's RBAC role assignments.
Core
GA
az ad sp credential
Manage a service principal's password or certificate credentials.
Core
GA
az ad sp credential delete
Delete a service principal's password or certificate credentials.
Core
GA
az ad sp credential list
List a service principal's password or certificate credential metadata. (The content of the password or certificate credential is not retrievable.).
Core
GA
az ad sp credential reset
Reset a service principal's password or certificate credentials.
Core
GA
az ad sp delete
Delete a service principal.
Core
GA
az ad sp list
List service principals.
Core
GA
az ad sp owner
Manage service principal owners.
Core
GA
az ad sp owner list
List service principal owners.
Core
GA
az ad sp show
Get the details of a service principal.
Core
GA
az ad sp update
Update a service principal.
Core
GA
az ad user
Manage Microsoft Entra users.
Core
GA
az ad user create
Create a user.
Core
GA
az ad user delete
Delete a user.
Core
GA
az ad user get-member-groups
Get groups of which the user is a member.
Core
GA
az ad user list
List users.
Core
GA
az ad user show
Get the details of a user.
Core
GA
az ad user update
Update a user.
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