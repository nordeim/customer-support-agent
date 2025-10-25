# backend/app/metrics.py
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, generate_latest
from typing import Dict, Any

# Create a custom registry
metrics_registry = CollectorRegistry()

# Define metrics
message_counter = Counter(
    "chat_messages_total",
    "Total number of chat messages",
    ["session_id", "role"],
    registry=metrics_registry
)

message_duration = Histogram(
    "chat_message_duration_seconds",
    "Time spent processing chat messages",
    ["session_id"],
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
    ["session_id"],
    registry=metrics_registry
)

rag_query_duration = Histogram(
    "rag_query_duration_seconds",
    "Time spent processing RAG queries",
    ["session_id"],
    registry=metrics_registry
)

attachment_processing = Counter(
    "attachment_processing_total",
    "Total number of attachments processed",
    ["session_id", "content_type"],
    registry=metrics_registry
)

attachment_processing_duration = Histogram(
    "attachment_processing_duration_seconds",
    "Time spent processing attachments",
    ["session_id", "content_type"],
    registry=metrics_registry
)

active_sessions = Gauge(
    "active_sessions",
    "Number of active chat sessions",
    registry=metrics_registry
)

def increment_message_counter(session_id: str, role: str):
    """Increment the message counter"""
    message_counter.labels(session_id=session_id, role=role).inc()

def observe_message_duration(session_id: str, duration: float):
    """Observe message processing duration"""
    message_duration.labels(session_id=session_id).observe(duration)

def increment_escalation_counter(session_id: str, reason: str):
    """Increment the escalation counter"""
    escalation_counter.labels(session_id=session_id, reason=reason).inc()

def increment_rag_queries(session_id: str):
    """Increment the RAG queries counter"""
    rag_queries.labels(session_id=session_id).inc()

def observe_rag_query_duration(session_id: str, duration: float):
    """Observe RAG query processing duration"""
    rag_query_duration.labels(session_id=session_id).observe(duration)

def increment_attachment_processing(session_id: str, content_type: str):
    """Increment the attachment processing counter"""
    attachment_processing.labels(session_id=session_id, content_type=content_type).inc()

def observe_attachment_processing_duration(session_id: str, content_type: str, duration: float):
    """Observe attachment processing duration"""
    attachment_processing_duration.labels(session_id=session_id, content_type=content_type).observe(duration)

def set_active_sessions(count: int):
    """Set the number of active sessions"""
    active_sessions.set(count)
