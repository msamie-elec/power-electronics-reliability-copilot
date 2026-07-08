param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID
Show-AzureAccount

az storage account create `
    --name $Config.STORAGE_ACCOUNT `
    --resource-group $Config.RESOURCE_GROUP `
    --location $Config.LOCATION `
    --sku Standard_LRS

$ConnectionString = az storage account show-connection-string `
    --name $Config.STORAGE_ACCOUNT `
    --resource-group $Config.RESOURCE_GROUP `
    --query connectionString `
    --output tsv

az storage container create `
    --name $Config.BLOB_CONTAINER `
    --connection-string $ConnectionString

Write-Success "Storage account and Blob container created or verified."
Write-Info "Do not print or commit connection strings."