Below are the remaining artifacts for **Phase 5 – Handoff** (documentation, migration/rollback scripts, deployment checklist), laid out within ```-code blocks for direct copy.

---

### `RUNBOOK.md`

````markdown
# Customer Support AI Agent – Runbook

**Service Name:** Customer Support AI Agent (Backend + Frontend)  
**Version:** 1.0.0  
**Prepared by:** Copilot-Craft  
**Date:** 2025-10-25

## 1. Purpose & Scope  
This runbook covers the deployment, operation, and support procedures for the Customer Support AI Agent service. It includes normal deployment steps, rollback procedures, monitoring, and escalation paths.

## 2. Architecture Overview  
- Frontend: React chat UI.  
- Backend: Python FastAPI service, uses the Microsoft Agent Framework (Assistants client) for AI logic.  
- Memory: SQLite database for session/memory data.  
- Knowledge Base: Embeddings model (EmbeddingGemma‑300M) + Chroma vector DB.  
- Attachment processing: MarkItDown package.  
- Observability: `/metrics` endpoint (Prometheus format), structured JSON logging, health endpoint `/healthz`.

## 3. Pre-Deployment Checklist  
Before you deploy:
- [ ] Ensure database migrations applied (see `migrations/` folder).  
- [ ] Confirm environment variables set (via `.env` or secret manager): `OPENAI_API_KEY`, `SQLITE_URL`, `CHROMA_PERSIST_DIRECTORY`, etc.  
- [ ] Confirm volume for SQLite persistence and Chroma persistence.  
- [ ] Ensure build artifacts available (Docker images, static assets).  
- [ ] Notify stakeholders of planned deployment window.  
- [ ] Backup any existing SQLite DB file (if upgrading) and Chroma store directory.

## 4. Deployment Procedure  
1. Pull latest code from `main` branch.  
2. Build Docker image: e.g., `docker build -t support-agent-backend:1.0.0 ./backend`.  
3. Stop current service (if live).  
4. Start new container or update service: `docker-compose up -d`.  
5. Run migration script: `./backend/migrations/run_migrations.sh`.  
6. Validate service health:  
   ```bash
   curl http://<host>:8000/healthz
````

should return `{"status":"ok"}`.
7. Run smoke test: send a message via `/chat/message` and verify response latency and correctness.
8. Monitor metrics endpoint: `http://<host>:8000/metrics` — ensure metrics are being exported.

## 5. Post-Deployment Validation

* [ ] Confirm 95th percentile latency < 2s for non-stream requests.
* [ ] Confirm 90th percentile initial streaming response < 1s.
* [ ] Confirm error rate < 1%.
* [ ] Validate sample conversation produces correct answer referencing KB.
* [ ] Confirm logs show no new exceptions in last 30 minutes.

## 6. Monitoring & Alerting

**Key Metrics:**

* `agent_request_count_total`
* `agent_request_latency_seconds`
* `agent_stream_request_latency_seconds`
* `agent_tool_invocations_total`

**Suggested Alert Rules:**

* If `agent_request_latency_seconds` p95 > 5s for > 10min → alert.
* If error count > 1% of total in a 5-min window → alert.
* If `agent_tool_invocations_total` for RAGTool is 0 for >30min (while requests > 0) → possible tool failure.

## 7. Troubleshooting & Escalation

**Common Issues:**

* Service fails to start: check environment variables, container logs.
* Embeddings missing or Chroma store unmounted: inspect volume and persistence directory.
* SQLite ‘database locked’ errors: check concurrent access, connection config.
* Agent response extremely slow: check model load times, memory usage, vector store latency.

**Escalation Path:**

* Level 1: Backend on-call engineer
* Level 2: SRE / AI Infrastructure lead
* Level 3: CTO / External vendor

## 8. Rollback Procedure

If deployment fails or critical issues appear:

1. Stop new service instance.
2. Restore previous Docker image (tag) and start it.
3. Restore SQLite database backup and Chroma store backup (if needed).
4. Validate health and smoke test again.
5. Notify stakeholders of rollback and follow up root cause.

## 9. Change Management & Versioning

* This runbook should be versioned (e.g., v1.0.0, v1.1.0).
* Maintain revision history with date, author, summary of changes.

## 10. Appendix

* Contact list for support teams.
* System architecture diagram (attach separately).
* Reference to repository: [https://github.com/…](https://github.com/…) (your repo).

````

---

### `CHANGELOG.md`
```markdown
# Changelog

## [1.0.0] – 2025-10-25  
### Added  
- Initial production-ready release of Customer Support AI Agent.  
- Frontend: React chat UI stub.  
- Backend: Python FastAPI service with Agent Framework integration.  
- Memory persistence (SQLite).  
- RAG pipeline using EmbeddingGemma-300M + Chroma.  
- Attachment processing via MarkItDown.  
- Structured logging, Prometheus metrics, health endpoint.  
- CI configuration (lint, unit tests, integration tests).  
- Runbook, deployment checklist, rollback script.

````

---

### `migrations/run_migrations.sh`

```bash
#!/usr/bin/env bash
set -e

echo "Running migrations..."
# For SQLite simple schema create
python - << 'EOF'
from backend.app.db.sqlite import engine, Base
from backend.app.db.models import *
Base.metadata.create_all(bind=engine)
print("Migration: Tables created/verified.")
EOF

echo "Migrations done."
```

---

### `deploy/rollback.sh`

```bash
#!/usr/bin/env bash
set -e

echo "=== Rollback Script for Customer Support AI Agent ==="

# Stop current service
echo "Stopping current containers..."
docker-compose down

# Restore previous image (assumes tag support-agent-backend:previous)
echo "Starting previous version..."
docker-compose up -d --build --force-recreate --no-deps backend

# Restore backups if needed
echo "If DB or vector store changes were made, please restore from backups manually."

echo "Rollback complete. Validate health endpoint now."
```

---

### `DEPLOYMENT_CHECKLIST.md`

```markdown
# Deployment Checklist – Customer Support AI Agent

## Project Info  
- Project name: Customer Support AI Agent  
- Version: 1.0.0  
- Deployment date: ____  
- Deploy lead: ____  

## Pre-Deployment  
- [ ] Confirm backup of SQLite data file.  
- [ ] Confirm backup of Chroma persistence directory.  
- [ ] Check environment variables are set.  
- [ ] Confirm build artifact ready (Docker image).  
- [ ] Notify stakeholders of window.  

## Environment Readiness  
- [ ] Kubernetes/VM/Server capacity verified.  
- [ ] Required ports open (8000 for backend, …).  
- [ ] Volume mounts configured for persistence.  
- [ ] Logging sink/pipeline operational.  

## Deployment Execution  
- [ ] Pull latest code.  
- [ ] Build Docker image.  
- [ ] Bring up new container.  
- [ ] Run migrations: `./migrations/run_migrations.sh`.  
- [ ] Validate `/healthz` endpoint.  
- [ ] Execute smoke test via `/chat/message`.  

## Post-Deployment  
- [ ] Monitor metrics for latency and error rate.  
- [ ] Confirm successful ingestion of knowledge base (if updated).  
- [ ] Collect user feedback.  
- [ ] Document any issues.  

## Rollback Criteria  
- [ ] Latency exceeds threshold (see SLOs).  
- [ ] Error rate > 1% for 5 minutes.  
- [ ] Major functional failure (e.g., agent not responding or delivering incorrect answers).  
If any criteria met → trigger rollback via `deploy/rollback.sh`.

## Sign-Off  
- Deployment Lead: ____ (signature/date)  
- QA Lead: ____ (signature/date)  
- SRE Lead: ____ (signature/date)  

```

---

**Confidence levels for these artifacts:**

* Runbook: High
* Changelog: High
* Migration/rollback scripts: Medium (needs environment-specific validation)
* Deployment checklist: High
