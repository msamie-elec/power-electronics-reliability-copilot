<#
==============================================================================
Power Electronics Reliability Copilot
Azure Deployment Script

File
----
04-create-openai.ps1

Purpose
-------
Creates or verifies the Azure OpenAI resource used by the Engineering Copilot.

This script creates the Azure OpenAI service resource only. Model deployments
are handled separately after confirming model availability in the selected
Azure region.

Prerequisites
-------------
1. Azure login completed:

   .\infra\azure\powershell\01-login.ps1

2. Resource group created:

   .\infra\azure\powershell\02-create-resource-group.ps1

3. Local Azure configuration completed:

   infra/azure/env/azure.local.env

How to Run
----------
From the project root:

.\infra\azure\powershell\04-create-openai.ps1

Expected Result
---------------
- Azure OpenAI resource exists.
- Endpoint can be retrieved.
- API key is not printed.

Security
--------
This script must not print Azure OpenAI keys.

==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID
Show-AzureAccount

Write-Info "Creating or verifying Azure OpenAI resource..."

az cognitiveservices account create `
    --name $Config.AZURE_OPENAI_NAME `
    --resource-group $Config.RESOURCE_GROUP `
    --location $Config.LOCATION `
    --kind $Config.AZURE_OPENAI_KIND `
    --sku $Config.AZURE_OPENAI_SKU `
    --yes

if ($LASTEXITCODE -ne 0) {
    Write-WarningMessage "Azure OpenAI resource creation failed."
    Write-WarningMessage "This may be because a resource with the same name was soft-deleted."

    $RestoreChoice = Read-Host "Recover the soft-deleted Azure OpenAI resource? (Y/N)"

    if ($RestoreChoice -eq "Y" -or $RestoreChoice -eq "y") {
        Write-Info "Attempting to recover soft-deleted Azure OpenAI resource..."

        az cognitiveservices account recover `
            --name $Config.AZURE_OPENAI_NAME `
            --resource-group $Config.RESOURCE_GROUP `
            --location $Config.LOCATION

        if ($LASTEXITCODE -ne 0) {
            Write-ErrorMessage "Azure OpenAI resource recovery failed."
            exit 1
        }

        Write-Success "Azure OpenAI resource recovered."
    }
    else {
        Write-ErrorMessage "Azure OpenAI resource was not created or recovered."
        Write-Info "If you want a fresh resource, purge the soft-deleted Azure OpenAI resource first."
        exit 1
    }
}

Write-Success "Azure OpenAI resource created, recovered, or verified."

Write-Info "Retrieving Azure OpenAI endpoint..."

$Endpoint = az cognitiveservices account show `
    --name $Config.AZURE_OPENAI_NAME `
    --resource-group $Config.RESOURCE_GROUP `
    --query properties.endpoint `
    --output tsv

if ([string]::IsNullOrWhiteSpace($Endpoint)) {
    Write-ErrorMessage "Unable to retrieve Azure OpenAI endpoint."
    exit 1
}

Write-Success "Azure OpenAI endpoint retrieved."

Write-Host ""
Write-Host "================ backend/.env ================"
Write-Host "AI_PROVIDER=$($Config.AI_PROVIDER)"
Write-Host "AZURE_OPENAI_ENDPOINT=$Endpoint"
Write-Host "AZURE_OPENAI_CHAT_DEPLOYMENT=$($Config.AZURE_OPENAI_CHAT_DEPLOYMENT)"
Write-Host "AZURE_OPENAI_EMBEDDING_DEPLOYMENT=$($Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT)"
Write-Host "AZURE_OPENAI_API_KEY=<retrieve securely>"
Write-Host "=============================================="

Write-Success "Azure OpenAI resource setup completed."