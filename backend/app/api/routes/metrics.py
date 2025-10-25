# backend/app/api/routes/metrics.py
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

from ...metrics import metrics_registry

router = APIRouter(prefix="/metrics", tags=["metrics"])

@router.get("/")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(metrics_registry), media_type=CONTENT_TYPE_LATEST)
