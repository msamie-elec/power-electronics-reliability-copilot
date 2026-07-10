# Observability Validation

## Purpose

This document records the validation workflow for Azure Monitor, Application Insights and backend health diagnostics in v0.6.0.

---

## Infrastructure Validation

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
- Key Vault contains `applicationinsights-connection-string` when Key Vault is configured.

---

## Backend Configuration

Set the following backend environment values:

```env
ENABLE_TELEMETRY=true
LOG_LEVEL=INFO
APPLICATIONINSIGHTS_CONNECTION_STRING=<value from Application Insights or Key Vault>
```

For local test execution, telemetry can remain disabled:

```env
ENABLE_TELEMETRY=false
```

---

## API Validation

Run the backend and validate:

```powershell
curl http://localhost:8000/health
curl http://localhost:8000/health/details
```

Expected endpoints:

- `/health` returns lightweight application status.
- `/health/details` returns provider and dependency diagnostics without exposing secrets.

---

## Regression Validation

Run from `backend`:

```powershell
pytest -v
```

Expected result:

```text
25 passed
```

---

## Security Notes

- Health diagnostics must not return secret values.
- Application Insights connection strings must not be printed in script output.
- API keys, storage connection strings and Neo4j passwords must remain in Azure Key Vault or local git-ignored environment files.

---

## Version

v0.6.0 — Enterprise Observability
