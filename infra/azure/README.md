# Azure Infrastructure

This folder contains the Azure infrastructure automation used by the **Power Electronics Reliability Copilot**.

The goal is to provide a repeatable, secure and low-cost deployment workflow for local development, testing and future production deployment.

The infrastructure scripts are intentionally separated from the application code so cloud resources can be created, verified and removed independently.

---

# Folder Structure

```text
infra/
└── azure/
    ├── README.md
    │
    ├── env/
    │   ├── azure.env.template
    │   └── azure.env.local      (ignored by Git)
    │
    ├── powershell/
    │   ├── common.ps1
    │   ├── 00-deploy-cloud-foundation.ps1
    │   ├── 01-login.ps1
    │   ├── 02-create-resource-group.ps1
    │   ├── 03-create-storage.ps1
    │   ├── 04-create-openai.ps1
    │   ├── 05-create-keyvault.ps1
    │   ├── 06-create-container-app.ps1
    │   ├── 07-check-resources.ps1
    │   ├── 08-deploy-backend.ps1
    │   ├── 09-deploy-frontend.ps1
    │   ├── 10-deploy-complete.ps1
    │   └── 99-cleanup.ps1
    │
    └── bicep/
```

---

# Configuration

The scripts read their configuration from

```
infra/azure/env/azure.env.local
```

This file contains developer-specific Azure settings such as:

- Subscription ID
- Tenant ID
- Resource Group
- Storage Account
- Azure OpenAI resource name
- Key Vault name
- Container App names

This file is excluded from Git.

A template version is provided as

```
infra/azure/env/azure.env.template
```

which contains only placeholder values.

---

# Deployment Workflow

Typical development workflow:

```text
Login
   ↓
Deploy Foundation
   ↓
Deploy Backend
   ↓
Deploy Frontend
   ↓
Verify Resources
   ↓
Run Application
   ↓
Cleanup Resources
```

The recommended scripts are:

```powershell
01-login.ps1
```

Authenticate with Azure.

```powershell
00-deploy-cloud-foundation.ps1
```

Create or verify the shared Azure infrastructure.

```powershell
08-deploy-backend.ps1
```

Deploy the backend application.

```powershell
09-deploy-frontend.ps1
```

Deploy the frontend application.

```powershell
10-deploy-complete.ps1
```

Run the complete deployment sequence.

```powershell
99-cleanup.ps1
```

Remove Azure resources after development to minimise cloud costs.

---

# Idempotent Design

Infrastructure scripts are designed to be **idempotent**.

Running a deployment script multiple times should not create duplicate resources.

Typical messages such as

```
Resource already exists
```

or

```
Storage account found. Updating existing account.
```

are expected behaviour and are **not errors**.

---

# Security

These scripts are designed so that secrets are never committed to Git.

The following values should never be printed or committed:

- Azure Storage connection strings
- Azure OpenAI API keys
- Azure Key Vault secrets
- Access tokens
- Passwords
- SAS tokens

Secrets should be stored only in one of the following:

- Local configuration files excluded by Git
- Azure Key Vault
- Azure environment variables
- GitHub Secrets (for CI/CD)

---

# Cost Management

This project follows an **ephemeral cloud infrastructure** approach.

Azure resources should exist only while development or testing is being performed.

After testing is complete, use

```powershell
99-cleanup.ps1
```

to remove unnecessary resources and minimise Azure costs.

---

# Future Enhancements

The following deployment stages will be implemented in future releases:

- Azure OpenAI deployment
- Container Apps deployment
- Static Web App deployment
- Azure AI Search
- Managed Identity
- CI/CD using GitHub Actions
- Bicep Infrastructure as Code