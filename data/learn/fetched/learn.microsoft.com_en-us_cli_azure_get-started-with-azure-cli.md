<!-- source: https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli -->

# Get started with Azure CLI

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
Get started with Azure CLI
Summarize this article for me
Azure CLI is a cross-platform tool that simplifies managing Azure resources from the command line.
Optimized for automation and ease of use, it supports interactive sessions and scripting with
straightforward commands that integrate seamlessly with the Azure Resource Manager model. You can
start using it in your browser with
Azure Cloud Shell
or install it locally to use
from your preferred terminal.
Install or run in Azure Cloud Shell
The easiest way to try Azure CLI is through
Azure Cloud Shell
, a
browser-based shell with no installation required. Cloud Shell supports Bash and PowerShell and
comes with the latest version of Azure CLI preinstalled.
To install Azure CLI locally, see
How to install Azure CLI
.
To check your version, run:
```
az version

```
Sign in to Azure
To start using Azure CLI with a local install, sign in:
Run the
az login
command.
```
az login

```
If Azure CLI can open your default browser, it initiates
authorization code flow
and opens
the default browser to load an Azure sign-in page.
Otherwise, it initiates the
device code flow
and instructs you to open a browser page at
https://aka.ms/devicelogin
. Then, enter the code displayed in your terminal.
If no web browser is available or the web browser fails to open, you can force device code flow
with
az login --use-device-code
.
Sign in with your account credentials in the browser.
Important
Starting in September 2025, Microsoft will require multifactor authentication (MFA) for Azure CLI
and other command-line tools. This change applies only to Microsoft Entra ID
user identities
and doesn't affect workload identities such as
service principals
or
managed identities
.
If you're using
az login
with a username and password to authenticate scripts or automated
workflows, now is the time to migrate to a workload identity. For more information, see
The impact of multifactor authentication on Azure CLI in automation scenarios
.
After you sign in, a list of your subscriptions appears. The one marked
isDefault: true
is
currently active. To change to a different subscription, run:
```
az account set --subscription "<subscription-id>"

```
For more information about subscription selection, see
Manage Azure subscriptions
. For advanced sign-in options, see
Sign in with Azure CLI
.
Find commands
Azure CLI commands are organized as command groups. Each group represents an area of an Azure
service. There are two options to find command groups:
Use the
az find
command. For example, to search for command names containing
vm
, use
the following example:
```
az find vm

```
Use the
--help
argument to get a complete list of subgroups within a reference group. The
following example returns all subgroups for virtual machines:
```
az vm --help

```
The following example shows the relevant portion of the output.
```
Subgroups:
  application            : Manage applications for VM.
  availability-set       : Group resources into availability sets.
  boot-diagnostics       : Troubleshoot the startup of an Azure Virtual Machine.
  ...

```
The help output includes subgroups, parameters, authentication options, and examples.
Here's another example that finds the Azure CLI commands for grouping virtual machines into
availability sets, a
subgroup
of
az vm
:
```
az vm availability-set --help

```
You can also use
--help
to get parameter lists and command examples for a reference
command
.
```
az vm create --help

```
Here is the relevant section of the example output:
```
Arguments
    --name  [Required] : Name of the virtual machine.
    ...
Authentication Arguments
    --admin-password   : Password for the VM if authentication type is 'Password'.
    --admin-username   : Username for the VM...
    ...
Managed Service Identity Arguments
    ...
Examples
    Create a VM from a custom managed image.
      az vm create -g MyResourceGroup -n MyVm --image MyImage
    ...

```
Use the
reference index
that lists all command groups alphabetically.
Explore samples and articles
For usage examples, see:
The
Samples index
for Azure CLI examples by
subject
,
reference group
, or
GitHub repo
.
The
Article index
to find in-depth guides. Use your keyboard
find
shortcut
keys, like
Ctrl + F
, to quickly find the reference command group in which you're interested. For
example, the article index for
az vm
looks like the following table:
Reference subgroup
Azure CLI article showing reference use
az vm
Output formats for Azure CLI commands
How to use variables in Azure CLI commands
Get VM information with queries
{More articles listed here.}
az vm aem
New Version of Azure VM extension for SAP solutions
Standard Version of Azure VM extension for SAP solutions
az vm application
{...}
Use tab completion
Azure CLI supports tab completion in Bash. To enable it in PowerShell, see
Enable tab completion in PowerShell
.
Understand global arguments
Common arguments available to most commands include:
Argument
Description
--help
View command help
--output
Change output format:
json
,
jsonc
,
tsv
,
table
,
yaml
--query
Filter output using
JMESPath
--verbose
Print more execution details
--debug
Show low-level REST calls for debugging
--subscription
Specify subscription name or ID
--only-show-errors
Suppress noncritical output
For more information, see
Output formats
and
Query results
.
Use interactive mode
Run interactive mode with:
```
az interactive

```
Interactive mode launches an enhanced Azure CLI experience with inline help and command suggestions.
For more, see
Interactive Mode
.
An optional
VS Code extension
provides similar features with autocomplete and
hover tips.
Learn through tutorials and quickstarts
Get hands-on with Azure CLI basics using the
onboarding tutorial
. You learn
how to:
Manage your default subscription
Create resources with randomized names
Use environment variables
Debug commands and parse JSON files
Delete resources efficiently
Note
Azure CLI examples on Microsoft Learn are written for Bash. One-liners usually work across shells,
but multiline scripts may require adjustments. For more information, see
Learn syntax differences between Bash, PowerShell, and Cmd
Provide feedback
We welcome your feedback. Submit issues on
GitHub
or run:
```
az feedback

```
See also
Onboarding cheat sheet
Azure CLI tutorial
Use Azure CLI in Bash
PowerShell considerations
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
Additional resources