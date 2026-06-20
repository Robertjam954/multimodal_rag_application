<!-- source: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli -->

# How to install the Azure CLI

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
How to install the Azure CLI
Summarize this article for me
The Azure CLI is available to install in Windows, Linux, and macOS environments. It can also be run
in a Docker container and Azure Cloud Shell.
Install
The current version of the Azure CLI is
2.87.0
. For information about the latest release, see the
release notes
. To find your installed version and see if you need to update, run
az version
.
Install on Windows
Install on Windows using WinGet (Windows Package Manager)
Install on Windows using Microsoft Installer (MSI)
Install on Windows using Microsoft Installer (MSI) with PowerShell
Install on Windows using a ZIP package
Install on Linux or Windows Subsystem for Linux (WSL) (
What is WSL?
)
Install on RHEL/CentOS Stream with dnf
Install on SLES/OpenSUSE with zypper
Install on Ubuntu/Debian with apt
Install on Azure Linux with tdnf
Install on macOS
Install on macOS (preview)
Run in Docker container
Run in Azure Cloud Shell
FAQ
Where is the Azure CLI installed?
When installing the Azure CLI, you can't select an install location. In Windows, the 32-bit Azure
CLI installs in
C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2
and the 64-bit in
C:\Program Files\Microsoft SDKs\Azure\CLI2
. In Linux, the Azure CLI is installed in
/opt/az/
on
Ubuntu and Debian, and in
/lib64/az/
on CentOS Stream, RHEL, and Azure Linux.
User-specific configuration files are located in
$HOME/.azure
on Linux and macOS, and
%USERPROFILE%\.azure
on Windows. These locations are known as the
AZURE_CONFIG_DIR
.
What version of the Azure CLI is installed?
Type
az version
in a terminal window to determine what version of the Azure CLI is installed. Your
output looks like this:
```
{
  "azure-cli": "x.xx.x",
  "azure-cli-core": "x.xx.x",
  "azure-cli-telemetry": "x.x.x",
  "extensions": {}
}

```
What extensions are installed?
Use the
az extension list
command to see installed extensions. You can also use
az version
, but
az extension list
provides more information including the installation path and status. For
information on managing extensions, see
Use and manage extensions with the Azure CLI
.
See also
Sign in with the Azure CLI
Azure CLI Onboarding cheat sheet
Find Azure CLI
samples
and
published docs
Tips to use the Azure CLI successfully
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