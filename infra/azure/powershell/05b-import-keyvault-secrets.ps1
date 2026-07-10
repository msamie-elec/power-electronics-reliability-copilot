<#
==============================================================================
Power Electronics Reliability Copilot
Azure Key Vault Secret Import Script

File
----
05b-import-keyvault-secrets.ps1

Purpose
-------
Imports local development secrets into Azure Key Vault without printing secret
values to the console.

This script is part of the Azure cloud foundation workflow for v0.6.0. It keeps
infrastructure configuration separate from sensitive secret values.

Configuration Files
-------------------
- infra/azure/env/azure.local.env
  Non-secret Azure infrastructure configuration.

- infra/azure/env/azure.secrets.local.env
  Local-only secret values. This file must never be committed.

Security
--------
- Does not print secret values.
- Does not write secrets to logs.
- Validates required secrets before import.
- Uses Azure Key Vault as the cloud secret store.
- Safe to run multiple times; existing Key Vault secret versions are updated.

Version
-------
v0.6.0
==============================================================================
#>

param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env",
    [string]$SecretsPath = "$PSScriptRoot\..\env\azure.secrets.local.env"
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

function Import-KeyVaultSecret {
    param(
        [Parameter(Mandatory = $true)]
        [string]$VaultName,

        [Parameter(Mandatory = $true)]
        [string]$SecretName,

        [Parameter(Mandatory = $true)]
        [string]$SecretValue
    )

    Write-Info "Importing secret: $SecretName"

    az keyvault secret set `
        --vault-name $VaultName `
        --name $SecretName `
        --value $SecretValue `
        --only-show-errors `
        --output none

    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "Failed to import secret: $SecretName"
        exit 1
    }

    Write-Success "Secret imported: $SecretName"
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

if (-not (Test-Path $SecretsPath)) {
    Write-ErrorMessage "Secret file not found: $SecretsPath"
    Write-Host ""
    Write-Host "Create this local-only file with:"
    Write-Host "    AZURE_OPENAI_API_KEY=<secret>"
    Write-Host "    AZURE_STORAGE_CONNECTION_STRING=<secret>"
    Write-Host "    NEO4J_PASSWORD=<secret>"
    Write-Host ""
    Write-Host "Do not commit this file."
    exit 1
}

Write-Info "Loading local secret configuration."
$Secrets = Import-AzureConfig -ConfigPath $SecretsPath

$RequiredSecrets = @(
    @{ LocalName = "AZURE_OPENAI_API_KEY"; VaultName = "azure-openai-api-key" },
    @{ LocalName = "AZURE_STORAGE_CONNECTION_STRING"; VaultName = "azure-storage-connection-string" },
    @{ LocalName = "NEO4J_PASSWORD"; VaultName = "neo4j-password" }
)

foreach ($secret in $RequiredSecrets) {
    Assert-RequiredValue -Config $Secrets -Name $secret.LocalName -Source $SecretsPath
}

foreach ($secret in $RequiredSecrets) {
    Import-KeyVaultSecret `
        -VaultName $Config.KEY_VAULT_NAME `
        -SecretName $secret.VaultName `
        -SecretValue $Secrets.($secret.LocalName)
}

if (-not [string]::IsNullOrWhiteSpace($Secrets.OPENAI_API_KEY)) {
    Import-KeyVaultSecret `
        -VaultName $Config.KEY_VAULT_NAME `
        -SecretName "openai-api-key" `
        -SecretValue $Secrets.OPENAI_API_KEY
}
else {
    Write-Info "OPENAI_API_KEY is empty; skipping optional secret: openai-api-key"
}

Write-Success "Key Vault secret import completed."
