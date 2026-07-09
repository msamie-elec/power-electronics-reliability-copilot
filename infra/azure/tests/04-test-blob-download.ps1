<#
==============================================================================
Power Electronics Reliability Copilot
Azure Infrastructure Test

File
----
04-test-blob-download.ps1

Purpose
-------
Downloads the test blob uploaded by 02-test-blob-upload.ps1 and verifies that
the downloaded file exists locally.

------------------------------------------------------------------------------
Prerequisites
------------------------------------------------------------------------------

1. Azure login completed

   .\infra\azure\powershell\01-login.ps1

2. Azure Storage deployed

   .\infra\azure\powershell\03-create-storage.ps1

3. Blob upload test passed

   .\infra\azure\tests\02-test-blob-upload.ps1

4. Blob list test passed

   .\infra\azure\tests\03-test-blob-list.ps1

------------------------------------------------------------------------------
How to Run
------------------------------------------------------------------------------

From the project root:

.\infra\azure\tests\04-test-blob-download.ps1

------------------------------------------------------------------------------
Expected Result
------------------------------------------------------------------------------

- Test blob is downloaded successfully.
- Downloaded file exists locally.
- Local temporary file is cleaned up.
- Azure Blob Download Test PASSED.

==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

Write-Info "Azure Blob Download Test"

$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID

$ConnectionString = az storage account show-connection-string `
    --name $Config.STORAGE_ACCOUNT `
    --resource-group $Config.RESOURCE_GROUP `
    --query connectionString `
    --output tsv

if ([string]::IsNullOrWhiteSpace($ConnectionString)) {
    Write-ErrorMessage "Unable to retrieve Storage Account connection string."
    exit 1
}

$BlobName = "engineering-test-upload.txt"
$DownloadPath = Join-Path $env:TEMP "engineering-test-download.txt"

Write-Info "Downloading test blob..."

az storage blob download `
    --connection-string $ConnectionString `
    --container-name $Config.BLOB_CONTAINER `
    --name $BlobName `
    --file $DownloadPath `
    --overwrite `
    --only-show-errors

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Blob download failed."
    exit 1
}

if (-not (Test-Path $DownloadPath)) {
    Write-ErrorMessage "Downloaded file was not found locally."
    exit 1
}

Remove-Item $DownloadPath -Force

Write-Success "Blob downloaded and local temporary file cleaned."
Write-Success "Azure Blob Download Test PASSED"