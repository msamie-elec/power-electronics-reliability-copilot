function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-WarningMessage {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-ErrorMessage {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Import-AzureConfig {
    param([string]$ConfigPath)

    if (-not (Test-Path $ConfigPath)) {
        Write-ErrorMessage "Config file not found: $ConfigPath"
        exit 1
    }

    $config = @{}

    Get-Content $ConfigPath | ForEach-Object {
        $line = $_.Trim()

        if (-not $line) { return }
        if ($line.StartsWith("#")) { return }

        $parts = $line -split "=", 2

        if ($parts.Count -eq 2) {
            $config[$parts[0].Trim()] = $parts[1].Trim()
        }
    }

    return [PSCustomObject]$config
}

function Set-AzureSubscription {
    param([string]$SubscriptionId)

    if (-not $SubscriptionId) {
        Write-ErrorMessage "SUBSCRIPTION_ID is not configured."
        exit 1
    }

    az account set --subscription $SubscriptionId
}

function Assert-AzureLoggedIn {

    az account show 1>$null 2>$null

    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "Azure CLI is not logged in."
        Write-Host ""
        Write-Host "Run:"
        Write-Host "    .\infra\azure\powershell\01-login.ps1"
        exit 1
    }
}

function Show-AzureAccount {

    Write-Info "Using Azure account"

    az account show `
        --query "{Subscription:name, State:state, Tenant:tenantId}" `
        --output table
}