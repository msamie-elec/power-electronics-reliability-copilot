<#
==============================================================================
Power Electronics Reliability Copilot
Azure Infrastructure Test

File
----
03-test-blob-list.ps1

Purpose
-------
Lists blobs in the configured Azure Blob Storage container and verifies that
the test blob uploaded by 02-test-blob-upload.ps1 exists.

------------------------------------------------------------------------------
Prerequisites
------------------------------------------------------------------------------

1. Azure login completed

   .\infra\azure\powershell\01-login.ps1

2. Azure Storage deployed

   .\infra\azure\powershell\03-create-storage.ps1

3. Blob upload test passed

   .\infra\azure\tests\02-test-blob-upload.ps1

------------------------------------------------------------------------------
How to Run
------------------------------------------------------------------------------

From the project root:

.\infra\azure\tests\03-test-blob-list.ps1

------------------------------------------------------------------------------
Expected Result
------------------------------------------------------------------------------

- Blob container is listed successfully.
- engineering-test-upload.txt is found.
- Azure Blob List Test PASSED.

==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

Write-Info "Azure Blob List Test"

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

Write-Info "Listing blobs in container..."

$BlobExists = az storage blob exists `
    --connection-string $ConnectionString `
    --container-name $Config.BLOB_CONTAINER `
    --name $BlobName `
    --query exists `
    --output tsv

if ($BlobExists -ne "true") {
    Write-ErrorMessage "Expected test blob was not found: $BlobName"
    exit 1
}

Write-Success "Expected test blob found: $BlobName"
Write-Success "Azure Blob List Test PASSED"