<#
==============================================================================
Power Electronics Reliability Copilot
Validate Azure Monitoring Resources

File
----
06c-validate-monitoring.ps1

Purpose
-------
Validates that Log Analytics, Application Insights and the related Key Vault
secret are available for backend observability.

Security
--------
- Does not print connection strings.
- Reports only whether monitoring resources and required configuration exist.

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

$ApplicationInsightsName = Get-ConfigValueOrDefault `
    -Config $Config `
    -Name "APPLICATION_INSIGHTS_NAME" `
    -DefaultValue "appi-powerelec-copilot-dev"

Write-Info "Checking Log Analytics Workspace: $WorkspaceName"
az monitor log-analytics workspace show `
    --resource-group $Config.RESOURCE_GROUP `
    --workspace-name $WorkspaceName `
    --only-show-errors `
    --output none

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Log Analytics Workspace is missing or inaccessible: $WorkspaceName"
    exit 1
}
Write-Success "Log Analytics Workspace is available: $WorkspaceName"

Write-Info "Checking Application Insights: $ApplicationInsightsName"
az monitor app-insights component show `
    --app $ApplicationInsightsName `
    --resource-group $Config.RESOURCE_GROUP `
    --only-show-errors `
    --output none

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Application Insights is missing or inaccessible: $ApplicationInsightsName"
    exit 1
}
Write-Success "Application Insights is available: $ApplicationInsightsName"

if (-not [string]::IsNullOrWhiteSpace($Config.KEY_VAULT_NAME)) {
    Write-Info "Checking Key Vault secret: applicationinsights-connection-string"

    az keyvault secret show `
        --vault-name $Config.KEY_VAULT_NAME `
        --name applicationinsights-connection-string `
        --query id `
        --only-show-errors `
        --output tsv 1>$null

    if ($LASTEXITCODE -ne 0) {
        Write-WarningMessage "Application Insights connection string secret is missing or inaccessible."
        Write-Host "Run:"
        Write-Host "    .\infra\azure\powershell\06b-create-application-insights.ps1"
    }
    else {
        Write-Success "Application Insights connection string secret is present."
    }
}

Write-Success "Azure monitoring validation completed."
