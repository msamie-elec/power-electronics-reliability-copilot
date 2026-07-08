param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID
Show-AzureAccount

Write-Info "Container App deployment will be implemented after backend containerisation."
Write-Info "Target environment: $($Config.CONTAINER_APP_ENV)"
Write-Info "Target app: $($Config.CONTAINER_APP_NAME)"