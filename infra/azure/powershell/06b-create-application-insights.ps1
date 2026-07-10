<#
==============================================================================
Power Electronics Reliability Copilot
Create Application Insights

File
----
06b-create-application-insights.ps1

Purpose
-------
Creates or verifies the workspace-based Application Insights resource used for
backend telemetry, request tracing, dependency tracing and exception analysis.

Security
--------
- Does not print the Application Insights connection string.
- Stores the connection string in Azure Key Vault when a Key Vault is configured.

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

Write-Info "Resolving Log Analytics Workspace resource ID."
$WorkspaceId = az monitor log-analytics workspace show `
    --resource-group $Config.RESOURCE_GROUP `
    --workspace-name $WorkspaceName `
    --query id `
    --output tsv

if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($WorkspaceId)) {
    Write-ErrorMessage "Log Analytics Workspace was not found: $WorkspaceName"
    Write-Host "Run first:"
    Write-Host "    .\infra\azure\powershell\06a-create-log-analytics.ps1"
    exit 1
}

Write-Info "Creating or verifying Application Insights: $ApplicationInsightsName"

az monitor app-insights component create `
    --app $ApplicationInsightsName `
    --location $Config.LOCATION `
    --resource-group $Config.RESOURCE_GROUP `
    --application-type web `
    --kind web `
    --workspace $WorkspaceId `
    --only-show-errors `
    --output none

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Failed to create or verify Application Insights: $ApplicationInsightsName"
    exit 1
}

$ConnectionString = az monitor app-insights component show `
    --app $ApplicationInsightsName `
    --resource-group $Config.RESOURCE_GROUP `
    --query connectionString `
    --output tsv

if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($ConnectionString)) {
    Write-ErrorMessage "Application Insights connection string could not be resolved."
    exit 1
}

if (-not [string]::IsNullOrWhiteSpace($Config.KEY_VAULT_NAME)) {
    Write-Info "Storing Application Insights connection string in Key Vault."

    az keyvault secret set `
        --vault-name $Config.KEY_VAULT_NAME `
        --name applicationinsights-connection-string `
        --value $ConnectionString `
        --only-show-errors `
        --output none

    if ($LASTEXITCODE -ne 0) {
        Write-WarningMessage "Application Insights was created, but the connection string could not be stored in Key Vault."
    }
    else {
        Write-Success "Application Insights connection string stored in Key Vault."
    }
}

Write-Success "Application Insights created or verified: $ApplicationInsightsName"
