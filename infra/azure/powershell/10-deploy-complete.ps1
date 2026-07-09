param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig $ConfigPath

Assert-AzureLoggedIn

Set-AzureSubscription $Config.SUBSCRIPTION_ID

Show-AzureAccount

Write-Info "======================================================="
Write-Info "Power Electronics Reliability Copilot"
Write-Info "Complete Azure Deployment"
Write-Info "======================================================="

Write-Info "Foundation deployment"

& "$PSScriptRoot\02-create-resource-group.ps1" `
    -ConfigPath $ConfigPath

& "$PSScriptRoot\03-create-storage.ps1" `
    -ConfigPath $ConfigPath

& "$PSScriptRoot\04-create-openai.ps1" `
    -ConfigPath $ConfigPath

& "$PSScriptRoot\04b-deploy-openai-models.ps1" `
    -ConfigPath $ConfigPath

& "$PSScriptRoot\05-create-keyvault.ps1" `
    -ConfigPath $ConfigPath

& "$PSScriptRoot\06-create-container-app.ps1" `
    -ConfigPath $ConfigPath

& "$PSScriptRoot\07-check-resources.ps1" `
    -ConfigPath $ConfigPath

Write-Info "Application deployment"

& "$PSScriptRoot\08-deploy-backend.ps1" `
    -ConfigPath $ConfigPath

& "$PSScriptRoot\09-deploy-frontend.ps1" `
    -ConfigPath $ConfigPath

Write-Host ""
Write-Success "======================================================="
Write-Success "Azure deployment completed successfully."
Write-Success "======================================================="