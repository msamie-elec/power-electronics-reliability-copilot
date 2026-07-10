# Azure Infrastructure

This folder contains Azure infrastructure automation used by the **Power Electronics Reliability Copilot**.

The goal is to provide a repeatable, secure and cost-controlled Azure workflow for development, validation and future production deployment.

The infrastructure scripts are intentionally separated from the application code so cloud resources can be created, verified and removed independently.

---

# Folder Structure

```text
infra/
└── azure/
    ├── README.md
    │
    ├── env/
    │   ├── azure.env.example
    │   ├── azure.local.env             (ignored by Git)
    │   └── azure.secrets.local.env     (ignored by Git)
    │
    ├── powershell/
    │   ├── common.ps1
    │   ├── 00-deploy-cloud-foundation.ps1
    │   ├── 01-login.ps1
    │   ├── 02-create-resource-group.ps1
    │   ├── 03-create-storage.ps1
    │   ├── 04-create-openai.ps1
    │   ├── 04a-list-openai-models.ps1
    │   ├── 04b-deploy-openai-models.ps1
    │   ├── 05-create-keyvault.ps1
    │   ├── 05b-import-keyvault-secrets.ps1
    │   ├── 05c-validate-keyvault.ps1
    │   ├── 06a-create-log-analytics.ps1
    │   ├── 06b-create-application-insights.ps1
    │   ├── 06c-validate-monitoring.ps1
    │   ├── 06-create-container-app.ps1
    │   ├── 07-check-resources.ps1
    │   ├── 08-deploy-backend.ps1
    │   ├── 09-deploy-frontend.ps1
    │   ├── 10-deploy-complete.ps1
    │   └── 99-cleanup.ps1
    │
    └── tests/
```

---

# Configuration Files

## `azure.local.env`

Contains non-secret Azure infrastructure configuration such as:

- Tenant ID
- Subscription ID
- Resource Group
- Location
- Storage Account name
- Blob Container name
- Azure OpenAI resource name
- Azure OpenAI deployment names
- Key Vault name
- Log Analytics Workspace name
- Application Insights name
- Container App names

This file is local to the development environment and should not be committed.

## `azure.secrets.local.env`

Contains local-only secret values used for importing secrets into Azure Key Vault.

Expected values include:

```env
AZURE_OPENAI_API_KEY=
AZURE_STORAGE_CONNECTION_STRING=
NEO4J_PASSWORD=
OPENAI_API_KEY=
```

This file must not be committed.

## `azure.env.example`

Template file containing non-secret placeholders for Azure infrastructure configuration.

---

# Deployment Workflow

## Foundation workflow

Run from the repository root:

```powershell
.\infra\azure\powershell\01-login.ps1
.\infra\azure\powershell\02-create-resource-group.ps1
.\infra\azure\powershell\03-create-storage.ps1
.\infra\azure\powershell\04-create-openai.ps1
.\infra\azure\powershell\04b-deploy-openai-models.ps1
.\infra\azure\powershell\05-create-keyvault.ps1
```

## Key Vault workflow

```powershell
.\infra\azure\powershell\05b-import-keyvault-secrets.ps1
.\infra\azure\powershell\05c-validate-keyvault.ps1
```

The Key Vault workflow imports required secrets without printing secret values.

Required Key Vault secrets:

- `azure-openai-api-key`
- `azure-storage-connection-string`
- `neo4j-password`

Optional Key Vault secret:

- `openai-api-key`

## Observability workflow

```powershell
.\infra\azure\powershell\06a-create-log-analytics.ps1
.\infra\azure\powershell\06b-create-application-insights.ps1
.\infra\azure\powershell\06c-validate-monitoring.ps1
```

This creates or verifies:

- Log Analytics Workspace
- Application Insights
- `applicationinsights-connection-string` stored in Azure Key Vault

## Validation workflow

```powershell
.\infra\azure\powershell\05c-validate-keyvault.ps1
.\infra\azure\powershell\06c-validate-monitoring.ps1
```

Backend validation:

```powershell
cd backend
pytest -v
```

Frontend validation:

```powershell
cd frontend
npm run build
```

## Cleanup workflow

```powershell
.\infra\azure\powershell\99-cleanup.ps1
```

The cleanup script removes the configured development resource group. Use this carefully because it deletes Azure resources inside the resource group.

---

# Script Summary

| Script | Purpose |
|--------|---------|
| `01-login.ps1` | Authenticate to Azure using tenant-specific login. |
| `02-create-resource-group.ps1` | Create or verify the development resource group. |
| `03-create-storage.ps1` | Create or verify Storage Account and Blob Container. |
| `04-create-openai.ps1` | Create or verify Azure OpenAI resource. |
| `04a-list-openai-models.ps1` | Inspect available Azure OpenAI models. |
| `04b-deploy-openai-models.ps1` | Deploy configured chat and embedding models. |
| `05-create-keyvault.ps1` | Create or verify Azure Key Vault. |
| `05b-import-keyvault-secrets.ps1` | Import local secrets into Key Vault without printing values. |
| `05c-validate-keyvault.ps1` | Validate required Key Vault secrets. |
| `06a-create-log-analytics.ps1` | Create or verify Log Analytics Workspace. |
| `06b-create-application-insights.ps1` | Create or verify Application Insights and store its connection string in Key Vault. |
| `06c-validate-monitoring.ps1` | Validate monitoring resources and Application Insights secret. |
| `06-create-container-app.ps1` | Placeholder for future Container Apps deployment. |
| `07-check-resources.ps1` | Check Azure resource availability. |
| `08-deploy-backend.ps1` | Placeholder for backend deployment. |
| `09-deploy-frontend.ps1` | Placeholder for frontend deployment. |
| `10-deploy-complete.ps1` | Complete deployment orchestrator. |
| `99-cleanup.ps1` | Delete the development resource group. |

---

# Idempotent Design

Infrastructure scripts are designed to be **idempotent**.

Running a deployment script multiple times should not create duplicate resources. Existing resources should be verified or updated as needed.

Typical messages such as:

```text
Resource already exists
Storage account found. Updating existing account.
Resource created or verified
```

are expected behaviour and are not errors.

---

# Security

These scripts are designed so that secrets are never committed to Git.

The following values must never be printed or committed:

- Azure Storage connection strings
- Azure OpenAI API keys
- Azure Key Vault secrets
- Application Insights connection strings
- Access tokens
- Passwords
- SAS tokens

Secrets should be stored only in one of the following:

- Local configuration files excluded by Git
- Azure Key Vault
- Azure environment variables
- GitHub Secrets for CI/CD

---

# Storage Authentication Note

In **v0.6.0**, Azure Blob Storage access uses a storage connection string stored in Azure Key Vault.

In **v0.7.0**, this should be replaced with **Managed Identity + Azure RBAC** so the backend can access Blob Storage without storing storage account keys or connection strings.

---

# Monitoring and Observability

Version **v0.6.0** introduces Azure monitoring infrastructure:

- Log Analytics Workspace
- Application Insights
- Application Insights connection string stored in Azure Key Vault
- Backend `/health` endpoint
- Backend `/health/details` dependency diagnostics endpoint

The Azure Portal can be used to inspect Application Insights logs, requests, failures, metrics, workbooks and dashboards after the backend is deployed and serving regular traffic.

---

# Cost Management

This project follows a cost-controlled development infrastructure approach.

Development Azure resources should exist only while development or validation is being performed.

After testing is complete, use:

```powershell
.\infra\azure\powershell\99-cleanup.ps1
```

to remove the development resource group and minimise Azure costs.

---

# Future Enhancements

The following deployment stages are planned for future releases:

- Managed Identity for Azure services
- Azure RBAC-based Blob Storage access
- Container Apps backend deployment
- Static Web Apps frontend deployment
- Azure AI Search
- CI/CD using GitHub Actions
- Bicep Infrastructure as Code
- Digitally signed PowerShell scripts
