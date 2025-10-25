# backend/app/core/logging.py
import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional
from .config import settings

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""
    
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "service": settings.app_name,
            "version": settings.app_version,
        }
        
        # Add extra fields if present
        extra_fields = [
            "session_id", "user_id", "request_id", "thread_id", "tool_name",
            "execution_time_ms", "query", "n_results", "attachment_count",
            "escalation_reason", "error_type", "component_status"
        ]
        
        for field in extra_fields:
            if hasattr(record, field):
                log_entry[field] = getattr(record, field)
        
        # Add exception information if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

class ContextFilter(logging.Filter):
    """Filter to add context information to log records"""
    
    def filter(self, record):
        # Add request context if available
        if hasattr(record, "request"):
            request = record.request
            if hasattr(request, "state") and hasattr(request.state, "request_id"):
                record.request_id = request.state.request_id
            if hasattr(request, "client") and request.client:
                record.client_ip = request.client.host
        
        return True

def setup_logging():
    """Configure application logging"""
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    console_handler.addFilter(ContextFilter())
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    # Set specific logger levels
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return root_logger

logger = setup_logging()

def log_function_call(func):
    """Decorator to log function calls with execution time"""
    def wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        
        logger.info(
            f"Function {func.__name__} called",
            extra={
                "function": func.__name__,
                "module": func.__module__,
                "args_count": len(args),
                "kwargs_count": len(kwargs)
            }
        )
        
        try:
            result = func(*args, **kwargs)
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            logger.info(
                f"Function {func.__name__} completed successfully",
                extra={
                    "function": func.__name__,
                    "module": func.__module__,
                    "execution_time_ms": execution_time
                }
            )
            
            return result
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            logger.error(
                f"Function {func.__name__} failed with error: {str(e)}",
                extra={
                    "function": func.__name__,
                    "module": func.__module__,
                    "execution_time_ms": execution_time,
                    "error_type": type(e).__name__
                },
                exc_info=True
            )
            
            raise
    
    return wrapper
