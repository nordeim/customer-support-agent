# backend/app/metrics.py
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
from typing import Dict, Any, Optional
import time
from functools import wraps

# Create a custom registry
metrics_registry = CollectorRegistry()

# Define metrics
message_counter = Counter(
    "chat_messages_total",
    "Total number of chat messages",
    ["session_id", "role", "status"],
    registry=metrics_registry
)

message_duration = Histogram(
    "chat_message_duration_seconds",
    "Time spent processing chat messages",
    ["session_id", "status"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
    registry=metrics_registry
)

escalation_counter = Counter(
    "chat_escalations_total",
    "Total number of escalations to human agents",
    ["session_id", "reason"],
    registry=metrics_registry
)

rag_queries = Counter(
    "rag_queries_total",
    "Total number of RAG queries",
    ["session_id", "status"],
    registry=metrics_registry
)

rag_query_duration = Histogram(
    "rag_query_duration_seconds",
    "Time spent processing RAG queries",
    ["session_id", "status"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    registry=metrics_registry
)

attachment_processing = Counter(
    "attachment_processing_total",
    "Total number of attachments processed",
    ["session_id", "content_type", "status"],
    registry=metrics_registry
)

attachment_processing_duration = Histogram(
    "attachment_processing_duration_seconds",
    "Time spent processing attachments",
    ["session_id", "content_type", "status"],
    buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
    registry=metrics_registry
)

active_sessions = Gauge(
    "active_sessions",
    "Number of active chat sessions",
    registry=metrics_registry
)

error_counter = Counter(
    "errors_total",
    "Total number of errors",
    ["component", "error_type"],
    registry=metrics_registry
)

health_check_status = Gauge(
    "health_check_status",
    "Health check status (1 for healthy, 0 for unhealthy)",
    ["component"],
    registry=metrics_registry
)

# Decorators for automatic metrics collection
def track_message_metrics(func):
    """Decorator to track message processing metrics"""
    @wraps(func)
    def wrapper(self, session_id: str, *args, **kwargs):
        start_time = time.time()
        status = "success"
        
        try:
            result = func(self, session_id, *args, **kwargs)
            
            # Track successful message
            message_counter.labels(
                session_id=session_id,
                role="assistant",
                status="success"
            ).inc()
            
            return result
        except Exception as e:
            status = "error"
            error_counter.labels(
                component="message_processing",
                error_type=type(e).__name__
            ).inc()
            raise
        finally:
            # Track duration
            duration = time.time() - start_time
            message_duration.labels(
                session_id=session_id,
                status=status
            ).observe(duration)
    
    return wrapper

def track_rag_metrics(func):
    """Decorator to track RAG query metrics"""
    @wraps(func)
    def wrapper(self, parameters: Dict[str, Any], *args, **kwargs):
        session_id = parameters.get("session_id", "unknown")
        start_time = time.time()
        status = "success"
        
        try:
            result = func(self, parameters, *args, **kwargs)
            
            # Track successful RAG query
            rag_queries.labels(
                session_id=session_id,
                status="success"
            ).inc()
            
            return result
        except Exception as e:
            status = "error"
            error_counter.labels(
                component="rag_query",
                error_type=type(e).__name__
            ).inc()
            raise
        finally:
            # Track duration
            duration = time.time() - start_time
            rag_query_duration.labels(
                session_id=session_id,
                status=status
            ).observe(duration)
    
    return wrapper

def track_attachment_metrics(func):
    """Decorator to track attachment processing metrics"""
    @wraps(func)
    def wrapper(self, parameters: Dict[str, Any], *args, **kwargs):
        session_id = parameters.get("session_id", "unknown")
        content_type = parameters.get("content_type", "unknown")
        start_time = time.time()
        status = "success"
        
        try:
            result = func(self, parameters, *args, **kwargs)
            
            # Track successful attachment processing
            attachment_processing.labels(
                session_id=session_id,
                content_type=content_type,
                status="success"
            ).inc()
            
            return result
        except Exception as e:
            status = "error"
            error_counter.labels(
                component="attachment_processing",
                error_type=type(e).__name__
            ).inc()
            raise
        finally:
            # Track duration
            duration = time.time() - start_time
            attachment_processing_duration.labels(
                session_id=session_id,
                content_type=content_type,
                status=status
            ).observe(duration)
    
    return wrapper

# Helper functions
def increment_message_counter(session_id: str, role: str, status: str = "success"):
    """Increment the message counter"""
    message_counter.labels(session_id=session_id, role=role, status=status).inc()

def observe_message_duration(session_id: str, duration: float, status: str = "success"):
    """Observe message processing duration"""
    message_duration.labels(session_id=session_id, status=status).observe(duration)

def increment_escalation_counter(session_id: str, reason: str):
    """Increment the escalation counter"""
    escalation_counter.labels(session_id=session_id, reason=reason).inc()

def increment_rag_queries(session_id: str, status: str = "success"):
    """Increment the RAG queries counter"""
    rag_queries.labels(session_id=session_id, status=status).inc()

def observe_rag_query_duration(session_id: str, duration: float, status: str = "success"):
    """Observe RAG query processing duration"""
    rag_query_duration.labels(session_id=session_id, status=status).observe(duration)

def increment_attachment_processing(session_id: str, content_type: str, status: str = "success"):
    """Increment the attachment processing counter"""
    attachment_processing.labels(session_id=session_id, content_type=content_type, status=status).inc()

def observe_attachment_processing_duration(session_id: str, content_type: str, duration: float, status: str = "success"):
    """Observe attachment processing duration"""
    attachment_processing_duration.labels(session_id=session_id, content_type=content_type, status=status).observe(duration)

def set_active_sessions(count: int):
    """Set the number of active sessions"""
    active_sessions.set(count)

def update_health_check_status(component: str, is_healthy: bool):
    """Update health check status for a component"""
    health_check_status.labels(component=component).set(1 if is_healthy else 0)
