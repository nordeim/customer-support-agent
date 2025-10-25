# Deployment Checklist

## Pre-deployment
- [ ] Backup current database
- [ ] Backup Redis data
- [ ] Verify all tests passing
- [ ] Check security scan results
- [ ] Verify environment variables
- [ ] Check disk space availability
- [ ] Notify stakeholders of deployment

## Deployment
- [ ] Run deployment script
- [ ] Monitor service startup
- [ ] Verify health checks
- [ ] Check application logs
- [ ] Test core functionality
- [ ] Verify monitoring dashboards

## Post-deployment
- [ ] Run smoke tests
- [ ] Check error rates
- [ ] Monitor response times
- [ ] Verify alerting rules
- [ ] Update documentation
- [ ] Communicate deployment status

## Rollback Criteria
- Error rate > 5%
- Response time > 5s
- Health check failures
- Critical functionality broken
- User complaints received

## Rollback Steps
1. Stop current deployment
2. Run rollback script
3. Verify system health
4. Communicate rollback status
5. Investigate root cause
