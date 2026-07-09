<#
==============================================================================
Power Electronics Reliability Copilot
Azure OpenAI Model Deployment Script

File
----
04b-deploy-openai-models.ps1

Purpose
-------
Deploys Azure OpenAI chat and embedding models for the Engineering Copilot.

Prerequisites
-------------
1. Azure login completed:

   .\infra\azure\powershell\01-login.ps1

2. Azure OpenAI resource created:

   .\infra\azure\powershell\04-create-openai.ps1

3. Optional model discovery completed:

   .\infra\azure\powershell\04a-list-openai-models.ps1
    Purpose: 
    Model availability should be checked using 04a-list-openai-models.ps1 before
    changing model names, versions or SKUs in azure.local.env.

How to Run
----------
From the project root:

.\infra\azure\powershell\04b-deploy-openai-models.ps1

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


function Test-OpenAIDeploymentExists {
    param(
        [string]$DeploymentName
    )

    $ExistingDeployment = az cognitiveservices account deployment show `
        --name $Config.AZURE_OPENAI_NAME `
        --resource-group $Config.RESOURCE_GROUP `
        --deployment-name $DeploymentName `
        --output none 2>$null

    return ($LASTEXITCODE -eq 0)
}


Write-Info "Deploying or verifying Azure OpenAI chat model..."

$ChatDeploymentExists = Test-OpenAIDeploymentExists `
    -DeploymentName $Config.AZURE_OPENAI_CHAT_DEPLOYMENT

if ($ChatDeploymentExists) {
    Write-Success "Chat deployment already exists: $($Config.AZURE_OPENAI_CHAT_DEPLOYMENT)"
}
else {
    az cognitiveservices account deployment create `
        --name $Config.AZURE_OPENAI_NAME `
        --resource-group $Config.RESOURCE_GROUP `
        --deployment-name $Config.AZURE_OPENAI_CHAT_DEPLOYMENT `
        --model-name $Config.AZURE_OPENAI_CHAT_MODEL `
        --model-version $Config.AZURE_OPENAI_CHAT_MODEL_VERSION `
        --model-format $Config.AZURE_OPENAI_MODEL_FORMAT `
        --sku-capacity $Config.AZURE_OPENAI_CHAT_CAPACITY `
        --sku-name $Config.AZURE_OPENAI_CHAT_SKU

    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "Chat model deployment failed."
        exit 1
    }

    Write-Success "Chat model deployed: $($Config.AZURE_OPENAI_CHAT_DEPLOYMENT)"
}


Write-Info "Deploying or verifying Azure OpenAI embedding model..."

$EmbeddingDeploymentExists = Test-OpenAIDeploymentExists `
    -DeploymentName $Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT

if ($EmbeddingDeploymentExists) {
    Write-Success "Embedding deployment already exists: $($Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT)"
}
else {
    az cognitiveservices account deployment create `
        --name $Config.AZURE_OPENAI_NAME `
        --resource-group $Config.RESOURCE_GROUP `
        --deployment-name $Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT `
        --model-name $Config.AZURE_OPENAI_EMBEDDING_MODEL `
        --model-version $Config.AZURE_OPENAI_EMBEDDING_MODEL_VERSION `
        --model-format $Config.AZURE_OPENAI_MODEL_FORMAT `
        --sku-capacity $Config.AZURE_OPENAI_EMBEDDING_CAPACITY `
        --sku-name $Config.AZURE_OPENAI_EMBEDDING_SKU

    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "Embedding model deployment failed."
        exit 1
    }

    Write-Success "Embedding model deployed: $($Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT)"
}


Write-Host ""
Write-Host "================ backend/.env ================"
Write-Host "AZURE_OPENAI_CHAT_DEPLOYMENT=$($Config.AZURE_OPENAI_CHAT_DEPLOYMENT)"
Write-Host "AZURE_OPENAI_EMBEDDING_DEPLOYMENT=$($Config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT)"
Write-Host "=============================================="

Write-Success "Azure OpenAI model deployment completed."