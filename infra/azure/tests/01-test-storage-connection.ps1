<#
==============================================================================
Power Electronics Reliability Copilot
Azure Infrastructure Test

File
----
01-test-storage-connection.ps1

Purpose
-------
Verifies that the Azure Storage Account is accessible and that the configured
Blob Container exists.

This test does not modify Azure resources.

------------------------------------------------------------------------------
Prerequisites
------------------------------------------------------------------------------

The following should have been completed successfully before running this test:

1. Azure CLI installed

2. Azure login

   .\infra\azure\powershell\01-login.ps1

3. Azure infrastructure deployed

   .\infra\azure\powershell\02-create-resource-group.ps1

   .\infra\azure\powershell\03-create-storage.ps1

4. Local configuration completed

   infra/azure/env/azure.local.env

------------------------------------------------------------------------------
How to Run
------------------------------------------------------------------------------

From the project root:

.\infra\azure\tests\01-test-storage-connection.ps1

------------------------------------------------------------------------------
Expected Result
------------------------------------------------------------------------------

The script should report:

- Connection string retrieved successfully.
- Blob container exists.
- Azure Storage Connection Test PASSED.

------------------------------------------------------------------------------
Common Failure Causes
------------------------------------------------------------------------------

- Azure CLI not logged in.
- Resource Group does not exist.
- Storage Account does not exist.
- Blob Container has not been created.
- Incorrect Azure configuration in azure.local.env.

==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\..\powershell\common.ps1"

Write-Info "Azure Storage Connection Test"

$config = Import-AzureConfig -ConfigPath $ConfigPath

Set-AzureSubscription -SubscriptionId $config.SUBSCRIPTION_ID

Write-Info "Retrieving Storage Account connection string..."

$connectionString = az storage account show-connection-string `
    --name $config.STORAGE_ACCOUNT `
    --resource-group $config.RESOURCE_GROUP `
    --query connectionString `
    --output tsv

if ([string]::IsNullOrWhiteSpace($connectionString)) {
    Write-ErrorMessage "Unable to retrieve Storage Account connection string."
    exit 1
}

Write-Success "Connection string retrieved successfully."

Write-Info "Checking Blob Container..."

$exists = az storage container exists `
    --name $config.BLOB_CONTAINER `
    --connection-string $connectionString `
    --query exists `
    --output tsv

if ($exists -ne "true") {
    Write-ErrorMessage "Blob container '$($config.BLOB_CONTAINER)' does not exist."
    exit 1
}

Write-Success "Blob container exists."

Write-Host ""
Write-Success "Azure Storage Connection Test PASSED"