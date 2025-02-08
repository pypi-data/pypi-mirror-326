"""OpenLLMetry integration for Hapax."""
from typing import Optional, Dict, Any, List
from opentelemetry import trace
from opentelemetry.trace import Span, Status, StatusCode
from opentelemetry.metrics import get_meter
from .semconv import SpanAttributes, LLMRequestTypeValues
import time
import json

class LLMSpanAttributes:
    """OpenLLMetry span attributes for LLM operations."""
    MODEL_NAME = "llm.model.name"
    PROMPT_TEMPLATE = "llm.prompt.template"
    PROMPT_TEMPLATE_TEMPLATE = "llm.prompt.template.template"
    PROMPT_TEMPLATE_VARIABLES = "llm.prompt.template.variables"
    COMPLETION_TOKENS = "llm.completion.tokens"
    PROMPT_TOKENS = "llm.prompt.tokens"
    TOTAL_TOKENS = "llm.total.tokens"
    TEMPERATURE = "llm.temperature"
    TOP_P = "llm.top_p"
    MAX_TOKENS = "llm.max_tokens"
    RESPONSE = "llm.response"
    USAGE = "llm.usage"

class LLMMetrics:
    """OpenLLMetry metrics for LLM operations."""
    def __init__(self, name: str = "hapax.llm"):
        self.meter = get_meter(name)
        
        # Request counters
        self.request_counter = self.meter.create_counter(
            "llm.requests",
            description="Number of LLM requests",
            unit="1"
        )
        
        # Token usage
        self.token_counter = self.meter.create_counter(
            "llm.tokens",
            description="Number of tokens used",
            unit="1"
        )
        
        # Latency histogram
        self.latency = self.meter.create_histogram(
            "llm.request.duration",
            description="Duration of LLM requests",
            unit="s"
        )

class LLMTracer:
    """Tracer for LLM operations with OpenLLMetry integration."""
    
    def __init__(self, name: str = "hapax.llm"):
        self.tracer = trace.get_tracer(name)
        self.metrics = LLMMetrics(name)
    
    def start_llm_span(
        self,
        operation: str,
        model: str,
        inputs: Dict[str, Any],
        parent: Optional[Span] = None,
    ) -> Span:
        """Start a new LLM span with OpenLLMetry attributes."""
        # Create span
        span = self.tracer.start_span(
            operation,
            attributes={
                SpanAttributes.LLM_REQUEST_TYPE: LLMRequestTypeValues.COMPLETION.value,
                SpanAttributes.LLM_REQUEST_MODEL: model,
            }
        )
        
        # Add input attributes
        if "prompt" in inputs:
            span.set_attribute("llm.prompt", str(inputs["prompt"]))
        if "temperature" in inputs:
            span.set_attribute(LLMSpanAttributes.TEMPERATURE, inputs["temperature"])
        if "max_tokens" in inputs:
            span.set_attribute(LLMSpanAttributes.MAX_TOKENS, inputs["max_tokens"])
        
        # Record request
        self.metrics.request_counter.add(1, {"model": model, "operation": operation})
        
        return span
    
    def end_llm_span(
        self,
        span: Span,
        response: Any,
        usage: Optional[Dict[str, int]] = None,
        error: Optional[Exception] = None
    ):
        """End an LLM span with results and metrics."""
        try:
            # Set response attributes
            if isinstance(response, (str, int, float, bool)):
                span.set_attribute(LLMSpanAttributes.RESPONSE, str(response))
            elif isinstance(response, (dict, list)):
                span.set_attribute(
                    LLMSpanAttributes.RESPONSE,
                    json.dumps(response, ensure_ascii=False)
                )
            
            # Set usage metrics if available
            if usage:
                span.set_attribute(LLMSpanAttributes.USAGE, json.dumps(usage))
                if "total_tokens" in usage:
                    span.set_attribute(
                        LLMSpanAttributes.TOTAL_TOKENS,
                        usage["total_tokens"]
                    )
                    self.metrics.token_counter.add(
                        usage["total_tokens"],
                        {"type": "total"}
                    )
                if "completion_tokens" in usage:
                    span.set_attribute(
                        LLMSpanAttributes.COMPLETION_TOKENS,
                        usage["completion_tokens"]
                    )
                    self.metrics.token_counter.add(
                        usage["completion_tokens"],
                        {"type": "completion"}
                    )
                if "prompt_tokens" in usage:
                    span.set_attribute(
                        LLMSpanAttributes.PROMPT_TOKENS,
                        usage["prompt_tokens"]
                    )
                    self.metrics.token_counter.add(
                        usage["prompt_tokens"],
                        {"type": "prompt"}
                    )
            
            # Set status
            if error:
                span.set_status(Status(StatusCode.ERROR, str(error)))
            else:
                span.set_status(Status(StatusCode.OK))
        
        finally:
            # End span
            span.end()
