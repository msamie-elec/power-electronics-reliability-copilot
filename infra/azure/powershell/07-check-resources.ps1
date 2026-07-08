param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID
Show-AzureAccount

Write-Info "Current Azure account:"
az account show --output table

Write-Info "Resource groups:"
az group list --output table

Write-Info "Storage accounts:"
az storage account list --output table

Write-Info "Key Vaults:"
az keyvault list --resource-group $Config.RESOURCE_GROUP --output table