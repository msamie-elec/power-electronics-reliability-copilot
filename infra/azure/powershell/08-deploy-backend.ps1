param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig $ConfigPath

Assert-AzureLoggedIn

Set-AzureSubscription $Config.SUBSCRIPTION_ID

Show-AzureAccount

Write-Info "Deploying backend"

Write-WarningMessage "Backend deployment will be implemented after Docker containerisation."

Write-Info "Future deployment target"

Write-Host "Container App:"
Write-Host "    $($Config.CONTAINER_APP_NAME)"

Write-Success "Backend deployment finished."