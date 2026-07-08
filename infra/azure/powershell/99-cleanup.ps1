param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env",
    [switch]$Force
)

. "$PSScriptRoot\common.ps1"

$Config = Import-AzureConfig -ConfigPath $ConfigPath
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID

Write-WarningMessage "This will delete the entire resource group: $($Config.RESOURCE_GROUP)"

if (-not $Force) {
    $confirmation = Read-Host "Type DELETE to confirm"

    if ($confirmation -ne "DELETE") {
        Write-Info "Cleanup cancelled."
        exit 0
    }
}

az group delete `
    --name $Config.RESOURCE_GROUP `
    --yes `
    --no-wait

Write-Success "Delete request submitted."