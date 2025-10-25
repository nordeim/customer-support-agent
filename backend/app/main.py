# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uuid

from .core.config import settings
from .core.logging import logger, setup_logging
from .api.routes import chat, health, metrics
from .metrics import set_active_sessions
from .db.database import engine
from .db.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Customer Support AI Agent API",
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Add logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
            "request_id": getattr(request.state, "request_id", None)
        }
    )
    
    return response

# Include routers
app.include_router(chat.router)
app.include_router(health.router)
app.include_router(metrics.router)

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc):
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "request_id": getattr(request.state, "request_id", None)
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(
        f"Starting {settings.app_name} v{settings.app_version}",
        extra={"event": "startup"}
    )

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(
        f"Shutting down {settings.app_name}",
        extra={"event": "shutdown"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
