# v0.6.0-04 Observability Implementation Notes

## Related files

```text
backend/app/core/logging_config.py
backend/app/core/telemetry.py
backend/app/services/health_service.py
backend/app/api/health.py
backend/app/main.py
infra/azure/powershell/06a-create-log-analytics.ps1
infra/azure/powershell/06b-create-application-insights.ps1
infra/azure/powershell/06c-validate-monitoring.ps1
docs/cloud/OBSERVABILITY_VALIDATION.md
```

Append the contents of these helper files to the corresponding project files:

```text
backend/.env.example.observability-additions -> backend/.env.example
backend/requirements-observability.txt -> backend/requirements.txt or install manually
infra/azure/env/azure.env.example.monitoring-additions -> infra/azure/env/azure.env.example and azure.local.env
```

## Dependency installation

From `backend`:

```powershell
pip install azure-monitor-opentelemetry opentelemetry-instrumentation-fastapi
pip freeze > requirements.txt
```

## Azure infrastructure execution

From repository root:

```powershell
.\infra\azure\powershell\06a-create-log-analytics.ps1
.\infra\azure\powershell\06b-create-application-insights.ps1
.\infra\azure\powershell\06c-validate-monitoring.ps1
```

## Backend validation

From `backend`:

```powershell
pytest -v
```

Then run the backend and check:

```powershell
curl http://localhost:8000/health
curl http://localhost:8000/health/details
```
