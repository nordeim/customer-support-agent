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
```

### Rollback
```bash
# Rollback to previous version
./scripts/rollback.sh

# Rollback to specific version
./scripts/rollback.sh to 1.0.0

# Restore from backup
./scripts/rollback.sh restore /path/to/backup
```

### Database Operations
```bash
# Run migrations
./scripts/deploy.sh migrate

# Create backup
docker-compose exec postgres pg_dump -U postgres customer_support > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U postgres customer_support < backup.sql
```

## Health Checks
- Frontend: http://localhost:80/health
- Backend: http://localhost:8000/health
- Prometheus: http://localhost:9090/-/healthy
- Grafana: http://localhost:3000/api/health

## Monitoring
- Grafana Dashboard: http://localhost:3000
- Prometheus: http://localhost:9090
- AlertManager: http://localhost:9093

## Common Issues

### High Response Times
1. Check Grafana dashboard for bottlenecks
2. Verify Redis cache is working
3. Check database connection pool
4. Scale backend services if needed

### High Error Rates
1. Check application logs
2. Verify Agent Framework connectivity
3. Check Chroma vector database status
4. Review recent deployments

### Database Issues
1. Check connection pool settings
2. Monitor slow queries
3. Verify disk space
4. Check PostgreSQL logs

## Emergency Contacts
- DevOps Team: devops@example.com
- Development Team: dev@example.com
- On-call Engineer: +1-555-0123

## SLAs
- Response Time: 95th percentile < 2s
- Error Rate: < 1%
- Availability: > 99.5%
- Recovery Time: < 15 minutes
