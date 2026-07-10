<#
==============================================================================
Power Electronics Reliability Copilot
Azure Key Vault Validation Script

File
----
05c-validate-keyvault.ps1

Purpose
-------
Validates that the project Azure Key Vault exists and contains the required
application secrets for cloud-based backend execution.

This script verifies secret presence only. It never prints, exports, or logs
secret values.

Configuration Files
-------------------
- infra/azure/env/azure.local.env
  Non-secret Azure infrastructure configuration.

Validated Secrets
-----------------
Required:
- azure-openai-api-key
- azure-storage-connection-string
- neo4j-password

Optional:
- openai-api-key

Security
--------
- Does not print secret values.
- Does not write secrets to logs.
- Uses Azure RBAC / Key Vault permissions through Azure CLI.
- Reports only whether required secrets are present and accessible.

Version
-------
v0.6.0
==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

function Assert-RequiredValue {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Config,

        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string]$Source
    )

    $value = $Config.$Name

    if ([string]::IsNullOrWhiteSpace($value)) {
        Write-ErrorMessage "$Name is missing or empty in $Source."
        exit 1
    }
}

function Test-KeyVaultSecretExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$VaultName,

        [Parameter(Mandatory = $true)]
        [string]$SecretName,

        [Parameter(Mandatory = $true)]
        [bool]$Required
    )

    Write-Info "Checking Key Vault secret: $SecretName"

    az keyvault secret show `
        --vault-name $VaultName `
        --name $SecretName `
        --query "id" `
        --only-show-errors `
        --output tsv 1>$null

    if ($LASTEXITCODE -eq 0) {
        Write-Success "Secret is present: $SecretName"
        return $true
    }

    if ($Required) {
        Write-ErrorMessage "Required secret is missing or inaccessible: $SecretName"
        return $false
    }

    Write-WarningMessage "Optional secret is missing or inaccessible: $SecretName"
    return $true
}

Write-Info "Loading Azure infrastructure configuration."
$Config = Import-AzureConfig -ConfigPath $ConfigPath

Assert-RequiredValue -Config $Config -Name "SUBSCRIPTION_ID" -Source $ConfigPath
Assert-RequiredValue -Config $Config -Name "KEY_VAULT_NAME" -Source $ConfigPath

Assert-AzureLoggedIn
Set-AzureSubscription -SubscriptionId $Config.SUBSCRIPTION_ID
Show-AzureAccount

Write-Info "Validating Key Vault exists: $($Config.KEY_VAULT_NAME)"
az keyvault show `
    --name $Config.KEY_VAULT_NAME `
    --only-show-errors `
    --output none

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMessage "Key Vault not found or not accessible: $($Config.KEY_VAULT_NAME)"
    Write-Host ""
    Write-Host "Run first:"
    Write-Host "    .\infra\azure\powershell\05-create-keyvault.ps1"
    exit 1
}

$RequiredSecrets = @(
    "azure-openai-api-key",
    "azure-storage-connection-string",
    "neo4j-password"
)

$OptionalSecrets = @(
    "openai-api-key"
)

$AllRequiredPresent = $true

foreach ($SecretName in $RequiredSecrets) {
    $result = Test-KeyVaultSecretExists `
        -VaultName $Config.KEY_VAULT_NAME `
        -SecretName $SecretName `
        -Required $true

    if (-not $result) {
        $AllRequiredPresent = $false
    }
}

foreach ($SecretName in $OptionalSecrets) {
    Test-KeyVaultSecretExists `
        -VaultName $Config.KEY_VAULT_NAME `
        -SecretName $SecretName `
        -Required $false | Out-Null
}

if (-not $AllRequiredPresent) {
    Write-ErrorMessage "Key Vault validation failed. One or more required secrets are missing."
    Write-Host ""
    Write-Host "Run:"
    Write-Host "    .\infra\azure\powershell\05b-import-keyvault-secrets.ps1"
    exit 1
}

Write-Success "Key Vault validation completed. Required secrets are present and accessible."
