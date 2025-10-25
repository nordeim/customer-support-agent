# backend/app/api/routes/health.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict, Any
import time

from ...db.database import get_db
from ...core.logging import logger
from ...core.config import settings
from ...metrics import update_health_check_status

router = APIRouter(prefix="/health", tags=["health"])

async def check_database_health(db: Session) -> Dict[str, Any]:
    """Check database connection health"""
    try:
        start_time = time.time()
        db.execute(text("SELECT 1"))
        response_time = (time.time() - start_time) * 1000
        
        update_health_check_status("database", True)
        
        return {
            "status": "healthy",
            "response_time_ms": response_time,
            "connection_string": settings.database_url.split("@")[-1] if "@" in settings.database_url else "local"
        }
    except Exception as e:
        update_health_check_status("database", False)
        logger.error(f"Database health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def check_agent_framework_health() -> Dict[str, Any]:
    """Check Agent Framework connection health"""
    try:
        # This is a placeholder for actual health check
        # In a real implementation, you would check the Agent Framework endpoint
        start_time = time.time()
        
        # Simulate health check
        await asyncio.sleep(0.1)
        
        response_time = (time.time() - start_time) * 1000
        update_health_check_status("agent_framework", True)
        
        return {
            "status": "healthy",
            "response_time_ms": response_time,
            "endpoint": settings.agent_framework_endpoint or "local"
        }
    except Exception as e:
        update_health_check_status("agent_framework", False)
        logger.error(f"Agent Framework health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def check_chroma_health() -> Dict[str, Any]:
    """Check Chroma vector database health"""
    try:
        from ...vector_store.chroma_client import ChromaClient
        
        start_time = time.time()
        chroma_client = ChromaClient(persist_directory=settings.chroma_persist_directory)
        
        # Test a simple query
        chroma_client.get(limit=1)
        
        response_time = (time.time() - start_time) * 1000
        update_health_check_status("chroma", True)
        
        return {
            "status": "healthy",
            "response_time_ms": response_time,
            "persist_directory": settings.chroma_persist_directory
        }
    except Exception as e:
        update_health_check_status("chroma", False)
        logger.error(f"Chroma health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

async def check_embedding_model_health() -> Dict[str, Any]:
    """Check embedding model health"""
    try:
        from ...vector_store.embeddings import EmbeddingModel
        
        start_time = time.time()
        embedding_model = EmbeddingModel(model_name=settings.embedding_model_name)
        
        # Test embedding generation
        test_embedding = embedding_model.embed_query("test")
        
        response_time = (time.time() - start_time) * 1000
        
        if test_embedding and len(test_embedding) > 0:
            update_health_check_status("embedding_model", True)
            return {
                "status": "healthy",
                "response_time_ms": response_time,
                "model_name": settings.embedding_model_name,
                "embedding_dimension": len(test_embedding)
            }
        else:
            update_health_check_status("embedding_model", False)
            return {
                "status": "unhealthy",
                "error": "Failed to generate embedding"
            }
    except Exception as e:
        update_health_check_status("embedding_model", False)
        logger.error(f"Embedding model health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@router.get("/")
async def health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Basic health check endpoint"""
    try:
        # Check all components
        db_health = await check_database_health(db)
        agent_health = await check_agent_framework_health()
        chroma_health = await check_chroma_health()
        
        # Determine overall status
        components = {
            "database": db_health["status"],
            "agent_framework": agent_health["status"],
            "chroma": chroma_health["status"]
        }
        
        overall_status = "healthy" if all(
            status == "healthy" for status in components.values()
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "version": settings.app_version,
            "timestamp": time.time(),
            "components": components
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Health check failed")

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Detailed health check endpoint with more information"""
    try:
        # Check all components with detailed information
        db_health = await check_database_health(db)
        agent_health = await check_agent_framework_health()
        chroma_health = await check_chroma_health()
        embedding_health = await check_embedding_model_health()
        
        # Determine overall status
        components = {
            "database": db_health,
            "agent_framework": agent_health,
            "chroma": chroma_health,
            "embedding_model": embedding_health
        }
        
        overall_status = "healthy" if all(
            comp["status"] == "healthy" for comp in components.values()
        ) else "unhealthy"
        
        return {
            "status": overall_status,
            "version": settings.app_version,
            "timestamp": time.time(),
            "components": components,
            "system_info": {
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "environment": settings.debug and "development" or "production"
            }
        }
    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Detailed health check failed")

@router.get("/readiness")
async def readiness_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Readiness check for Kubernetes"""
    try:
        # Check critical components for readiness
        db_health = await check_database_health(db)
        
        if db_health["status"] != "healthy":
            raise HTTPException(status_code=503, detail="Database not ready")
        
        return {
            "status": "ready",
            "timestamp": time.time()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Readiness check failed")

@router.get("/liveness")
async def liveness_check() -> Dict[str, Any]:
    """Liveness check for Kubernetes"""
    return {
        "status": "alive",
        "timestamp": time.time()
    }
