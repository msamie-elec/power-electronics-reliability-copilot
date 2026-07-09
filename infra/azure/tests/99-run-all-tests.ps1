<#
==============================================================================
Power Electronics Reliability Copilot
Azure Infrastructure Test Runner

File
----
99-run-all-tests.ps1

Purpose
-------
Runs all Azure infrastructure validation tests in sequence.

------------------------------------------------------------------------------
Prerequisites
------------------------------------------------------------------------------

1. Azure login completed

   .\infra\azure\powershell\01-login.ps1

2. Azure infrastructure deployed

   .\infra\azure\powershell\10-deploy-complete.ps1

------------------------------------------------------------------------------
How to Run
------------------------------------------------------------------------------

From the project root:

.\infra\azure\tests\99-run-all-tests.ps1

==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

Write-Info "Running all Azure infrastructure tests"

& "$PSScriptRoot\01-test-storage-connection.ps1" -ConfigPath $ConfigPath
if ($LASTEXITCODE -ne 0) { exit 1 }

& "$PSScriptRoot\02-test-blob-upload.ps1" -ConfigPath $ConfigPath
if ($LASTEXITCODE -ne 0) { exit 1 }

& "$PSScriptRoot\03-test-blob-list.ps1" -ConfigPath $ConfigPath
if ($LASTEXITCODE -ne 0) { exit 1 }

& "$PSScriptRoot\04-test-blob-download.ps1" -ConfigPath $ConfigPath
if ($LASTEXITCODE -ne 0) { exit 1 }

& "$PSScriptRoot\05-test-openai-deployments.ps1" -ConfigPath $ConfigPath
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Success "All Azure infrastructure tests PASSED"