param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig $ConfigPath

Assert-AzureLoggedIn

Set-AzureSubscription $Config.SUBSCRIPTION_ID

Show-AzureAccount

Write-Info "Deploying frontend"

Write-WarningMessage "Frontend deployment will be implemented after Azure Static Web App configuration."

Write-Success "Frontend deployment finished."