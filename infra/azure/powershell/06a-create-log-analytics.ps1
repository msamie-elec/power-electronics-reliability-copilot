<#
==============================================================================
Power Electronics Reliability Copilot
Create Azure Log Analytics Workspace

File
----
06a-create-log-analytics.ps1

Purpose
-------
Creates or verifies the Azure Log Analytics Workspace used by Azure Monitor and
workspace-based Application Insights.

Security
--------
- Does not handle application secrets.
- Uses Azure CLI authenticated identity and configured subscription.

Version
-------
v0.6.0
==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

function Get-ConfigValueOrDefault {
    param(
        [Parameter(Mandatory = $true)] [object]$Config,
        [Parameter(Mandatory = $true)] [string]$Name,
        [Parameter(Mandatory = $true)] [string]$DefaultValue
    )

    $value = $Config.$Name
    if ([string]::IsNullOrWhiteSpace($value)) { return $DefaultValue }
    return $value
}

Write-Info "Loading Azure infrastructure configuration."
$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID
Show-AzureAccount

$WorkspaceName = Get-ConfigValueOrDefault `
    -Config $Config `
    -Name "LOG_ANALYTICS_WORKSPACE" `
    -DefaultValue "law-powerelec-copilot-dev"

Write-Info "Creating or verifying Log Analytics Workspace: $WorkspaceName"

az monitor log-analytics workspace create `
    --resource-group $Config.RESOURCE_GROUP `
    --workspace-name $WorkspaceName `
    --location $Config.LOCATION `
    --sku PerGB2018 `
    --only-show-errors `
    --output none

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Failed to create or verify Log Analytics Workspace: $WorkspaceName"
    exit 1
}

Write-Success "Log Analytics Workspace created or verified: $WorkspaceName"
