"""
Core functionality for Hapax observability system.
Provides decorators and low-level tracing capabilities with logging support.
Integrates with Hapax's AI infrastructure monitoring.
"""
import functools
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional, Union, List
from datetime import datetime
from enum import Enum
from loguru import logger

class LogLevel(str, Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class MetricType(str, Enum):
    REQUEST = "request"
    LATENCY = "latency"
    ERROR = "error"
    PROVIDER = "provider"
    CIRCUIT_BREAKER = "circuit_breaker"

@dataclass
class Metric:
    name: str
    type: MetricType
    value: float
    labels: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

@dataclass
class Span:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    parent_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    log_level: LogLevel = LogLevel.INFO
    metrics: List[Metric] = field(default_factory=list)
    provider: Optional[str] = None
    endpoint: Optional[str] = None
    
    def add_metric(self, name: str, type: MetricType, value: float, **labels):
        """Add a metric to the span."""
        metric = Metric(
            name=name,
            type=type,
            value=value,
            labels={**labels, "span_id": self.id}
        )
        self.metrics.append(metric)
        return metric
    
    def end(self):
        self.end_time = time.time()
        duration_ms = (self.end_time - self.start_time) * 1000
        
        # Add standard metrics
        self.add_metric(
            "hapax_http_request_duration_seconds",
            MetricType.LATENCY,
            duration_ms / 1000,  # Convert to seconds
            endpoint=self.endpoint or "unknown",
            provider=self.provider or "unknown"
        )
        
        if "error" in self.attributes:
            self.add_metric(
                "hapax_errors_total",
                MetricType.ERROR,
                1,
                error_type=self.attributes.get("error_type", "unknown"),
                provider=self.provider or "unknown"
            )
        
        # Log the span completion with the specified log level
        log_func = getattr(logger, self.log_level.lower())
        log_func(
            f"Span '{self.name}' completed in {duration_ms:.2f}ms",
            span_id=self.id,
            parent_id=self.parent_id,
            provider=self.provider,
            endpoint=self.endpoint,
            **self.attributes
        )
        return self

class TraceContext:
    def __init__(self, default_log_level: LogLevel = LogLevel.INFO):
        self.current_span: Optional[Span] = None
        self.spans: Dict[str, Span] = {}
        self.default_log_level = default_log_level
        self.metrics: List[Metric] = []
    
    def start_span(
        self, 
        name: str, 
        attributes: Dict[str, Any] = None,
        log_level: Optional[LogLevel] = None,
        provider: Optional[str] = None,
        endpoint: Optional[str] = None
    ) -> Span:
        parent_id = self.current_span.id if self.current_span else None
        
        # Inherit log level from parent if not specified
        if log_level is None:
            log_level = (
                self.current_span.log_level if self.current_span 
                else self.default_log_level
            )
        
        # Inherit provider and endpoint from parent if not specified
        if provider is None and self.current_span:
            provider = self.current_span.provider
        if endpoint is None and self.current_span:
            endpoint = self.current_span.endpoint
        
        span = Span(
            name=name,
            parent_id=parent_id,
            attributes=attributes or {},
            log_level=log_level,
            provider=provider,
            endpoint=endpoint
        )
        
        # Add request metric
        if endpoint:
            span.add_metric(
                "hapax_http_requests_total",
                MetricType.REQUEST,
                1,
                endpoint=endpoint,
                provider=provider or "unknown"
            )
        
        # Log span start
        log_func = getattr(logger, log_level.lower())
        log_func(
            f"Starting span '{name}'",
            span_id=span.id,
            parent_id=parent_id,
            provider=provider,
            endpoint=endpoint,
            **span.attributes
        )
        
        self.spans[span.id] = span
        return span
    
    def get_metrics(self) -> List[Metric]:
        """Get all metrics from all spans."""
        metrics = []
        for span in self.spans.values():
            metrics.extend(span.metrics)
        return metrics

_trace_context = TraceContext()

def set_default_log_level(level: Union[LogLevel, str]):
    """Set the default log level for all spans without explicit level."""
    if isinstance(level, str):
        level = LogLevel(level.upper())
    _trace_context.default_log_level = level

def obs(
    name: Optional[str] = None, 
    log_level: Optional[Union[LogLevel, str]] = None,
    provider: Optional[str] = None,
    endpoint: Optional[str] = None,
    **attributes
):
    """
    Decorator for observing function execution with logging and metrics support.
    
    Args:
        name: Optional name for the span. Defaults to function name.
        log_level: Optional log level for this span. Overrides inherited level.
        provider: Optional AI provider name (e.g., "openai", "anthropic")
        endpoint: Optional API endpoint being called
        **attributes: Additional attributes to attach to the span.
    
    Usage:
        @obs()
        def my_function():
            pass
            
        @obs("llm_call", provider="openai", endpoint="/v1/completions")
        def call_llm():
            pass
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            span_name = name or func.__name__
            
            # Convert string log level to enum if needed
            span_log_level = None
            if log_level is not None:
                span_log_level = (
                    LogLevel(log_level.upper()) 
                    if isinstance(log_level, str) 
                    else log_level
                )
            
            span = _trace_context.start_span(
                name=span_name,
                attributes={
                    **attributes,
                    "function": func.__name__,
                    "timestamp": datetime.now().isoformat()
                },
                log_level=span_log_level,
                provider=provider,
                endpoint=endpoint
            )
            
            previous_span = _trace_context.current_span
            _trace_context.current_span = span
            
            try:
                result = func(*args, **kwargs)
                span.attributes["status"] = "success"
                return result
            except Exception as e:
                span.attributes["status"] = "error"
                span.attributes["error"] = str(e)
                span.attributes["error_type"] = e.__class__.__name__
                # Force ERROR level for exceptions
                span.log_level = LogLevel.ERROR
                raise
            finally:
                span.end()
                _trace_context.current_span = previous_span
        
        return wrapper
    return decorator

def get_trace_context() -> TraceContext:
    """Get the current trace context."""
    return _trace_context

def get_metrics() -> List[Metric]:
    """Get all metrics from the current trace context."""
    return _trace_context.get_metrics()
