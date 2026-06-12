$ErrorActionPreference = "Stop"
$root = Resolve-Path "$PSScriptRoot/.."
Set-Location $root
if (Test-Path "$root/.venv/Scripts/Activate.ps1") { . "$root/.venv/Scripts/Activate.ps1" }
Set-Location "$root/app/backend"
python prepdocs.py @args
