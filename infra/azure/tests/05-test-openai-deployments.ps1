<#
==============================================================================
Power Electronics Reliability Copilot
Azure Infrastructure Test

File
----
05-test-openai-deployments.ps1

Purpose
-------
Verifies that the configured Azure OpenAI chat and embedding deployments exist.

This test validates Azure OpenAI deployment readiness before switching the
backend to AI_PROVIDER=azure_openai.

------------------------------------------------------------------------------
Prerequisites
------------------------------------------------------------------------------

1. Azure login completed

   .\infra\azure\powershell\01-login.ps1

2. Azure OpenAI resource created

   .\infra\azure\powershell\04-create-openai.ps1

3. Azure OpenAI models deployed

   .\infra\azure\powershell\04b-deploy-openai-models.ps1

4. Local Azure configuration completed

   infra/azure/env/azure.local.env

------------------------------------------------------------------------------
How to Run
------------------------------------------------------------------------------

From the project root:

.\infra\azure\tests\05-test-openai-deployments.ps1

------------------------------------------------------------------------------
Expected Result
------------------------------------------------------------------------------

- Azure OpenAI chat deployment exists.
- Azure OpenAI embedding deployment exists.
- Azure OpenAI Deployment Test PASSED.

------------------------------------------------------------------------------
Common Failure Causes
------------------------------------------------------------------------------

- Azure CLI is not logged in.
- Azure OpenAI resource does not exist.
- Chat model deployment has not been created.
- Embedding model deployment has not been created.
- Deployment names in azure.local.env do not match Azure.

==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

Write-Info "Azure OpenAI Deployment Test"

$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID

Write-Info "Checking chat deployment..."

az cognitiveservices account deployment show `
    --name $Config.AZURE_OPENAI_NAME `
    --resource-group $Config.RESOURCE_GROUP `
    --deployment-name $Config.AZURE_OPENAI_CHAT_DEPLOYMENT `
    --output none 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Chat deployment not found: $($Config.AZURE_OPENAI_CHAT_DEPLOYMENT)"
    exit 1
}

Write-Success "Chat deployment exists: $($Config.AZURE_OPENAI_CHAT_DEPLOYMENT)"

Write-Info "Checking embedding deployment..."

az cognitiveservices account deployment show `
    --name $Config.AZURE_OPENAI_NAME `
    --resource-group $Config.RESOURCE_GROUP `
    --deployment-name $Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT `
    --output none 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Embedding deployment not found: $($Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT)"
    exit 1
}

Write-Success "Embedding deployment exists: $($Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT)"

Write-Success "Azure OpenAI Deployment Test PASSED"