<#
==============================================================================
Power Electronics Reliability Copilot
Azure OpenAI Model Discovery Script

File
----
04a-list-openai-models.ps1

Purpose
-------
Lists Azure OpenAI models available for the configured Azure OpenAI resource.

This script helps identify deployable chat and embedding models before running:

.\infra\azure\powershell\04b-deploy-openai-models.ps1

Prerequisites
-------------
1. Azure login completed:

   .\infra\azure\powershell\01-login.ps1

2. Azure OpenAI resource created:

   .\infra\azure\powershell\04-create-openai.ps1

How to Run
----------
From the project root:

.\infra\azure\powershell\04a-list-openai-models.ps1

Security
--------
This script must not print API keys.

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

Write-Info "Listing Azure OpenAI models for resource: $($Config.AZURE_OPENAI_NAME)"

az cognitiveservices account list-models `
    --name $Config.AZURE_OPENAI_NAME `
    --resource-group $Config.RESOURCE_GROUP `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Unable to list Azure OpenAI models."
    exit 1
}

Write-Success "Azure OpenAI model listing completed."

Write-Host ""
Write-Host "================ Recommended Models ================"
Write-Host ""
Write-Host "Recommended chat model for this project:"
Write-Host "  AZURE_OPENAI_CHAT_MODEL=gpt-5-mini"
Write-Host "  AZURE_OPENAI_CHAT_MODEL_VERSION=2025-08-07"
Write-Host "  AZURE_OPENAI_CHAT_SKU=GlobalStandard"
Write-Host ""
Write-Host "Recommended embedding model for this project:"
Write-Host "  AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-3-small"
Write-Host "  AZURE_OPENAI_EMBEDDING_MODEL_VERSION=1"
Write-Host "  AZURE_OPENAI_EMBEDDING_SKU=GlobalStandard"
Write-Host ""
Write-Host "Avoid models with lifecycle status:"
Write-Host "  - Deprecated"
Write-Host "  - Deprecating"
Write-Host ""
Write-Host "Then update:"
Write-Host "  infra/azure/env/azure.local.env"
Write-Host ""
Write-Host "Finally run:"
Write-Host "  .\infra\azure\powershell\04b-deploy-openai-models.ps1"
Write-Host "===================================================="