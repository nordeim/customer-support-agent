# backend/app/api/routes/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any

from ...db.database import get_db
from ...core.logging import logger
from ...core.config import settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Basic health check endpoint"""
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        
        # Check Agent Framework connection
        # This is a placeholder for actual health check
        agent_framework_status = "healthy"
        
        # Check Chroma connection
        # This is a placeholder for actual health check
        chroma_status = "healthy"
        
        overall_status = "healthy" if all(
            status == "healthy" for status in [agent_framework_status, chroma_status]
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "version": settings.app_version,
            "components": {
                "database": "healthy",
                "agent_framework": agent_framework_status,
                "chroma": chroma_status
            }
        }
    except Exception as e:
        logger.error(
            f"Health check failed: {str(e)}",
            extra={"tool_name": "health_check"}
        )
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Detailed health check endpoint with more information"""
    try:
        # Check database connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
        
        # Check Agent Framework connection
        # This is a placeholder for actual health check
        agent_framework_status = "healthy"
        
        # Check Chroma connection
        # This is a placeholder for actual health check
        chroma_status = "healthy"
        
        overall_status = "healthy" if all(
            status == "healthy" for status in [db_status, agent_framework_status, chroma_status]
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "version": settings.app_version,
            "components": {
                "database": {
                    "status": db_status,
                    "connection_string": settings.database_url
                },
                "agent_framework": {
                    "status": agent_framework_status,
                    "endpoint": settings.agent_framework_endpoint
                },
                "chroma": {
                    "status": chroma_status,
                    "persist_directory": settings.chroma_persist_directory
                }
            }
        }
    except Exception as e:
        logger.error(
            f"Detailed health check failed: {str(e)}",
            extra={"tool_name": "health_check"}
        )
        return {
            "status": "unhealthy",
            "error": str(e)
        }
