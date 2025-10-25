# backend/app/monitoring/sli_slo.py
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from prometheus_client import Gauge, Histogram
from ..metrics import metrics_registry
from ..core.logging import logger

@dataclass
class SLIDefinition:
    """Service Level Indicator definition"""
    name: str
    description: str
    unit: str
    query: str

@dataclass
class SLODefinition:
    """Service Level Objective definition"""
    name: str
    sli_name: str
    target: float  # Target percentage (e.g., 95.0 for 95%)
    time_window: timedelta
    alerting_threshold: float  # Alert if below this percentage

class SLIMonitor:
    """Service Level Indicator Monitor"""
    
    def __init__(self):
        self.slis: Dict[str, SLIDefinition] = {}
        self.slos: Dict[str, SLODefinition] = {}
        self.sli_values: Dict[str, List[float]] = {}
        
        # Initialize SLIs
        self._initialize_slis()
        
        # Initialize SLOs
        self._initialize_slos()
    
    def _initialize_slis(self):
        """Initialize Service Level Indicators"""
        self.slis = {
            "response_time": SLIDefinition(
                name="response_time",
                description="95th percentile response time for chat messages",
                unit="seconds",
                query="histogram_quantile(0.95, rate(chat_message_duration_seconds_bucket[5m]))"
            ),
            "error_rate": SLIDefinition(
                name="error_rate",
                description="Percentage of failed requests",
                unit="percent",
                query="(rate(errors_total[5m]) / rate(chat_messages_total[5m])) * 100"
            ),
            "availability": SLIDefinition(
                name="availability",
                description="Service availability percentage",
                unit="percent",
                query="(sum(up) / count(up)) * 100"
            ),
            "rag_relevance": SLIDefinition(
                name="rag_relevance",
                description="Average relevance score of RAG results",
                unit="percent",
                query="avg(rag_relevance_score)"
            )
        }
    
    def _initialize_slos(self):
        """Initialize Service Level Objectives"""
        self.slos = {
            "response_time_slo": SLODefinition(
                name="response_time_slo",
                sli_name="response_time",
                target=95.0,  # 95% of requests under 2 seconds
                time_window=timedelta(days=7),
                alerting_threshold=90.0
            ),
            "error_rate_slo": SLODefinition(
                name="error_rate_slo",
                sli_name="error_rate",
                target=1.0,  # Error rate below 1%
                time_window=timedelta(days=7),
                alerting_threshold=2.0
            ),
            "availability_slo": SLODefinition(
                name="availability_slo",
                sli_name="availability",
                target=99.5,  # 99.5% availability
                time_window=timedelta(days=30),
                alerting_threshold=99.0
            ),
            "rag_relevance_slo": SLODefinition(
                name="rag_relevance_slo",
                sli_name="rag_relevance",
                target=85.0,  # 85% relevance score
                time_window=timedelta(days=7),
                alerting_threshold=80.0
            )
        }
    
    def record_sli_value(self, sli_name: str, value: float):
        """Record a new SLI value"""
        if sli_name not in self.sli_values:
            self.sli_values[sli_name] = []
        
        self.sli_values[sli_name].append({
            "value": value,
            "timestamp": datetime.utcnow()
        })
        
        # Keep only values within the last 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        self.sli_values[sli_name] = [
            entry for entry in self.sli_values[sli_name]
            if entry["timestamp"] > cutoff_time
        ]
    
    def calculate_sli_compliance(self, sli_name: str, time_window: timedelta) -> float:
        """Calculate SLI compliance over a time window"""
        if sli_name not in self.sli_values:
            return 0.0
        
        cutoff_time = datetime.utcnow() - time_window
        recent_values = [
            entry["value"] for entry in self.sli_values[sli_name]
            if entry["timestamp"] > cutoff_time
        ]
        
        if not recent_values:
            return 0.0
        
        # Calculate compliance based on SLI type
        if sli_name == "response_time":
            # For response time, calculate percentage of values under target
            target = 2.0  # 2 seconds
            compliant_values = [v for v in recent_values if v <= target]
            return (len(compliant_values) / len(recent_values)) * 100
        elif sli_name == "error_rate":
            # For error rate, calculate average
            return 100 - sum(recent_values) / len(recent_values)
        elif sli_name == "availability":
            # For availability, calculate average
            return sum(recent_values) / len(recent_values)
        elif sli_name == "rag_relevance":
            # For RAG relevance, calculate average
            return sum(recent_values) / len(recent_values)
        
        return 0.0
    
    def check_slo_compliance(self) -> Dict[str, Dict[str, Any]]:
        """Check compliance for all SLOs"""
        compliance_report = {}
        
        for slo_name, slo in self.slos.items():
            compliance = self.calculate_sli_compliance(slo.sli_name, slo.time_window)
            
            compliance_report[slo_name] = {
                "sli_name": slo.sli_name,
                "target": slo.target,
                "current_compliance": compliance,
                "is_compliant": compliance >= slo.target,
                "is_alerting": compliance < slo.alerting_threshold,
                "time_window_hours": slo.time_window.total_seconds() / 3600
            }
            
            # Log if SLO is not compliant
            if compliance < slo.target:
                logger.warning(
                    f"SLO {slo_name} not compliant: {compliance:.2f}% < {slo.target}%",
                    extra={
                        "slo_name": slo_name,
                        "sli_name": slo.sli_name,
                        "current_compliance": compliance,
                        "target": slo.target
                    }
                )
            
            # Log alert if below threshold
            if compliance < slo.alerting_threshold:
                logger.error(
                    f"SLO {slo_name} alerting: {compliance:.2f}% < {slo.alerting_threshold}%",
                    extra={
                        "slo_name": slo_name,
                        "sli_name": slo.sli_name,
                        "current_compliance": compliance,
                        "alerting_threshold": slo.alerting_threshold
                    }
                )
        
        return compliance_report
    
    def get_sli_definitions(self) -> Dict[str, SLIDefinition]:
        """Get all SLI definitions"""
        return self.slis
    
    def get_slo_definitions(self) -> Dict[str, SLODefinition]:
        """Get all SLO definitions"""
        return self.slos

# Global SLI monitor instance
sli_monitor = SLIMonitor()

# Decorators for automatic SLI tracking
def track_response_time(func):
    """Decorator to track response time for SLI monitoring"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            response_time = time.time() - start_time
            
            # Record SLI value
            sli_monitor.record_sli_value("response_time", response_time)
            
            return result
        except Exception as e:
            response_time = time.time() - start_time
            
            # Record SLI value even for failed requests
            sli_monitor.record_sli_value("response_time", response_time)
            
            # Record error
            sli_monitor.record_sli_value("error_rate", 1.0)
            
            raise
    
    return wrapper

def track_availability(func):
    """Decorator to track availability for SLI monitoring"""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            
            # Record successful availability
            sli_monitor.record_sli_value("availability", 100.0)
            
            return result
        except Exception as e:
            # Record failed availability
            sli_monitor.record_sli_value("availability", 0.0)
            
            raise
    
    return wrapper
