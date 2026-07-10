# Observability Validation

## Purpose

This document records the validation workflow for Azure Monitor, Application Insights and backend health diagnostics in **v0.6.0**.

---

# Observability Components

Version **v0.6.0** introduces the following observability components:

| Component | Purpose |
|----------|---------|
| Log Analytics Workspace | Central workspace for Azure logs and telemetry. |
| Application Insights | Application monitoring, request telemetry, failures, performance and traces. |
| Key Vault secret | Stores `applicationinsights-connection-string`. |
| `/health` | Lightweight health probe. |
| `/health/details` | Detailed dependency diagnostics. |

---

# Infrastructure Validation

Run from the repository root:

```powershell
.\infra\azure\powershell\01-login.ps1
.\infra\azure\powershell\06a-create-log-analytics.ps1
.\infra\azure\powershell\06b-create-application-insights.ps1
.\infra\azure\powershell\06c-validate-monitoring.ps1
```

Expected result:

- Log Analytics Workspace exists.
- Application Insights exists.
- Application Insights connection string is available.
- Key Vault contains `applicationinsights-connection-string`.

Validated result:

```text
[SUCCESS] Log Analytics Workspace is available: law-powerelec-copilot-dev
[SUCCESS] Application Insights is available: appi-powerelec-copilot-dev
[SUCCESS] Application Insights connection string secret is present.
[SUCCESS] Azure monitoring validation completed.
```

---

# Backend Configuration

Set the following backend environment values:

```env
ENABLE_TELEMETRY=true
LOG_LEVEL=INFO
APPLICATIONINSIGHTS_CONNECTION_STRING=
```

When `SECRET_PROVIDER=azure_key_vault`, the Application Insights connection string can be retrieved through Key Vault using:

```text
applicationinsights-connection-string
```

For local test execution, telemetry can remain disabled:

```env
ENABLE_TELEMETRY=false
```

---

# API Validation

Run the backend and validate:

```powershell
curl http://localhost:8000/health
curl http://localhost:8000/health/details
```

Expected endpoints:

- `/health` returns lightweight application status.
- `/health/details` returns provider and dependency diagnostics without exposing secrets.

Validated dependency checks:

- Azure Key Vault
- Azure Blob Storage
- Azure OpenAI configuration
- Neo4j

Expected healthy result:

```json
{
  "status": "healthy",
  "service": "Power Electronics Reliability Copilot API",
  "version": "0.6.0-dev",
  "environment": "development",
  "providers": {
    "ai": "azure_openai",
    "storage": "azure_blob",
    "secrets": "azure_key_vault",
    "graph": "neo4j"
  }
}
```

---

# Application Insights Portal Checks

After the backend has generated traffic, inspect the Application Insights resource in Azure Portal:

```text
Application Insights
→ appi-powerelec-copilot-dev
```

Useful areas:

- Overview
- Logs
- Metrics
- Failures
- Performance
- Transaction search
- Workbooks
- Dashboards with Grafana

Example KQL query:

```kusto
requests
| order by timestamp desc
```

If the backend is only running locally and telemetry is disabled, Application Insights may show limited or no runtime request data. This is expected until telemetry export is enabled and the application receives traffic.

---

# Regression Validation

Run from `backend`:

```powershell
pytest -v
```

Expected result:

```text
25 passed
```

Validated result:

```text
25 passed, 5 warnings
```

---

# Frontend Validation

Run from `frontend`:

```powershell
npm run build
```

Expected result:

```text
built
```

---

# Security Notes

- Health diagnostics must not return secret values.
- Application Insights connection strings must not be printed in script output.
- API keys, storage connection strings and Neo4j passwords must remain in Azure Key Vault or local git-ignored environment files.
- Azure Portal telemetry inspection should not expose sensitive user or secret data.

---

# Version

v0.6.0 — Observability and Health Diagnostics
