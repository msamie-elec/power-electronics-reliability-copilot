<#
==============================================================================
Power Electronics Reliability Copilot
Azure Infrastructure Test

File
----
02-test-blob-upload.ps1

Purpose
-------
Uploads a temporary engineering document to Azure Blob Storage and verifies
that the upload succeeds.

This test validates Azure Blob Storage connectivity and upload capability.

------------------------------------------------------------------------------
Prerequisites

1. Azure CLI installed

2. Azure login

   .\infra\azure\powershell\01-login.ps1

3. Azure infrastructure deployed

   .\infra\azure\powershell\02-create-resource-group.ps1

   .\infra\azure\powershell\03-create-storage.ps1

4. Azure Storage Connection Test passed

   .\infra\azure\tests\01-test-storage-connection.ps1

------------------------------------------------------------------------------
How to Run

.\infra\azure\tests\02-test-blob-upload.ps1

------------------------------------------------------------------------------
Expected Result

- Temporary file created.
- File uploaded successfully.
- Local temporary file removed.
- Blob remains in Azure.

==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

Write-Info "Azure Blob Upload Test"

$config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $config.SUBSCRIPTION_ID

$connectionString = az storage account show-connection-string `
    --name $config.STORAGE_ACCOUNT `
    --resource-group $config.RESOURCE_GROUP `
    --query connectionString `
    --output tsv

if ([string]::IsNullOrWhiteSpace($connectionString)) {
    Write-ErrorMessage "Unable to retrieve Storage Account connection string."
    exit 1
}

$tempFile = Join-Path $env:TEMP "engineering-test-upload.txt"

Set-Content `
    -Path $tempFile `
    -Value "Power Electronics Reliability Copilot Azure Blob Upload Test"

$blobName = "engineering-test-upload.txt"

Write-Info "Uploading test blob..."

az storage blob upload `
    --connection-string $connectionString `
    --container-name $config.BLOB_CONTAINER `
    --name $blobName `
    --file $tempFile `
    --overwrite `
    --only-show-errors

if ($LASTEXITCODE -ne 0) {
    Remove-Item $tempFile -Force
    Write-ErrorMessage "Blob upload failed."
    exit 1
}

Remove-Item $tempFile -Force

Write-Success "Blob uploaded successfully."

Write-Success "Azure Blob Upload Test PASSED"