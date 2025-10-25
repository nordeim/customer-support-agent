# Customer Support AI Agent - Runbook

## System Overview
Customer Support AI Agent is a production-ready system consisting of:
- React frontend (TypeScript)
- Python FastAPI backend with Microsoft Agent Framework
- PostgreSQL database
- Redis cache
- Chroma vector database for RAG
- Prometheus/Grafana monitoring

## Quick Start Commands

### Deployment
```bash
# Deploy the system
./scripts/deploy.sh

# Check deployment status
./scripts/deploy.sh health

# View logs
./scripts/deploy.sh logs [service_name]
