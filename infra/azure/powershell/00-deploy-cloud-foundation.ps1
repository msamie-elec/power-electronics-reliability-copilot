param(
    [string]$ConfigPath = "$PSScriptRoot\..\env\azure.local.env"
)

. "$PSScriptRoot\common.ps1"

Write-Info "Starting Azure cloud foundation deployment."

Write-Info "Step 1: Login"
& "$PSScriptRoot\01-login.ps1" -ConfigPath $ConfigPath

Write-Info "Step 2: Resource Group"
& "$PSScriptRoot\02-create-resource-group.ps1" -ConfigPath $ConfigPath

Write-Info "Step 3: Storage"
& "$PSScriptRoot\03-create-storage.ps1" -ConfigPath $ConfigPath

Write-Info "Step 4: Azure OpenAI"
& "$PSScriptRoot\04-create-openai.ps1" -ConfigPath $ConfigPath

Write-Info "Step 5: Key Vault"
& "$PSScriptRoot\05-create-keyvault.ps1" -ConfigPath $ConfigPath

Write-Info "Step 6: Container App placeholder"
& "$PSScriptRoot\06-create-container-app.ps1" -ConfigPath $ConfigPath

Write-Info "Step 7: Resource Check"
& "$PSScriptRoot\07-check-resources.ps1" -ConfigPath $ConfigPath

Write-Success "Azure cloud foundation deployment completed."