param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID
Show-AzureAccount

az keyvault create `
    --name $Config.KEY_VAULT_NAME `
    --resource-group $Config.RESOURCE_GROUP `
    --location $Config.LOCATION

Write-Success "Key Vault created or verified."