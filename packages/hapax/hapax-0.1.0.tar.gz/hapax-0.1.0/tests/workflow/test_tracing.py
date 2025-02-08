"""Tests for workflow tracing and monitoring."""
import pytest
import asyncio
from typing import Any, Dict, List, Optional, Union, Callable
from unittest.mock import MagicMock, patch
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from hapax.workflow.core import Workflow
from hapax.observability.semconv import SpanAttributes

@pytest.fixture
def mock_tracer():
    """Create a mock tracer for testing."""
    tracer = MagicMock()
    span = MagicMock()
    context = MagicMock()
    
    # Mock context manager behavior
    context.__enter__ = MagicMock(return_value=span)
    context.__exit__ = MagicMock(return_value=None)
    
    # Mock start_span and start_as_current_span to return context
    tracer.start_span = MagicMock(return_value=context)
    tracer.start_as_current_span = MagicMock(return_value=context)
    
    # Ensure span attributes are properly tracked
    span.set_attribute = MagicMock()
    span.set_status = MagicMock()
    span.record_exception = MagicMock()
    
    return tracer

async def test_basic_tracing(mock_tracer):
    """Test basic span creation and attributes."""
    with patch("hapax.workflow.core.telemetry.get_tracer", return_value=mock_tracer):
        workflow = (
            Workflow()
            .add(lambda x: str(x.upper()))  # type: Callable[[str], str]
            .add(lambda x: str(f"Hello {x}"))  # type: Callable[[str], str]
        )
        
        result = await workflow.run("world", trace=True)
        
        # Should create spans for workflow and each step
        assert mock_tracer.start_span.call_count >= 1
        assert result == "Hello WORLD"
        
        # Check span attributes
        span = mock_tracer.start_span.return_value.__enter__.return_value
        assert span.set_attribute.called
        assert span.set_status.called
        assert span.set_status.call_args[0][0].status_code == StatusCode.OK

async def test_error_tracing(mock_tracer, error_functions):
    """Test span attributes for errors."""
    with patch("hapax.workflow.core.telemetry.get_tracer", return_value=mock_tracer):
        workflow = Workflow().add(error_functions["value_error"])
        
        with pytest.raises(ValueError):
            await workflow.run("test", trace=True)
        
        # Should set error status and attributes
        span = mock_tracer.start_span.return_value.__enter__.return_value
        assert span.set_status.called
        assert span.set_status.call_args[0][0].status_code == StatusCode.ERROR
        assert span.record_exception.called

async def test_nested_spans(mock_tracer):
    """Test nested span creation for complex workflows."""
    from typing import Callable

    # Define functions with proper type hints
    def to_upper(x: str) -> str:
        return x.upper()

    def check_length(x: str) -> bool:
        return len(x) > 3

    def format_long(x: str) -> str:
        return f"Long: {x}"

    def format_short(x: str) -> str:
        return f"Short: {x}"

    def add_long_branch(w: Workflow) -> Workflow:
        return w.add(format_long)

    def add_short_branch(w: Workflow) -> Workflow:
        return w.add(format_short)

    with patch("hapax.workflow.core.telemetry.get_tracer", return_value=mock_tracer):
        workflow = (
            Workflow()
            .add(to_upper)
            .when(
                check_length,
                then=add_long_branch,
                else_=add_short_branch
            )
        )

        result = await workflow.run("test", trace=True)
        assert result == "Long: TEST"

        # Verify spans were created correctly
        # Should create spans for:
        # 1. Main workflow
        # 2. to_upper function
        # 3. check_length function
        # 4. format_long function
        assert mock_tracer.start_span.call_count >= 4

async def test_parallel_tracing(mock_tracer):
    """Test span creation for parallel execution."""
    def to_upper(x: str) -> str:
        return x.upper()

    def to_lower(x: str) -> str:
        return x.lower()

    with patch("hapax.workflow.core.telemetry.get_tracer", return_value=mock_tracer):
        workflow = (
            Workflow()
            .map([to_upper, to_lower])
        )

        result = await workflow.run("Test", trace=True)
        assert isinstance(result, list)
        assert len(result) == 2
        assert "TEST" in result
        assert "test" in result

        # Should create spans for main workflow and each parallel function
        assert mock_tracer.start_span.call_count >= 3

async def test_trace_context_propagation(mock_tracer):
    """Test trace context propagation between steps."""
    parent_span = MagicMock()
    mock_tracer.start_span.return_value.__enter__.return_value = parent_span
    
    with patch("hapax.workflow.core.telemetry.get_tracer", return_value=mock_tracer):
        workflow = (
            Workflow()
            .add(lambda x: str(x))  # type: Callable[[str], str]
            .add(lambda x: str(x))  # type: Callable[[str], str]
        )
        
        await workflow.run("test", trace=True)
        
        # Child spans should be created with parent context
        child_calls = mock_tracer.start_span.call_args_list
        assert len(child_calls) >= 2
        for call in child_calls[1:]:
            assert "parent" in str(call) or "context" in str(call)

async def test_metric_recording(mock_tracer):
    """Test metric recording during workflow execution."""
    with patch("hapax.workflow.core.telemetry.get_tracer", return_value=mock_tracer):
        async def slow_step(x: str) -> str:
            await asyncio.sleep(0.1)
            return x
        
        workflow = Workflow().add(slow_step)
        
        await workflow.run("test", trace=True)
        
        # Should record duration metric
        span = mock_tracer.start_span.return_value.__enter__.return_value
        assert any(
            "duration" in str(call) or "latency" in str(call)
            for call in span.set_attribute.call_args_list
        )

async def test_resource_tracing(mock_tracer, tmp_path):
    """Test tracing of resource acquisition and cleanup."""
    file_path = tmp_path / "test.txt"
    
    def write_file(text: str) -> str:
        with open(file_path, "w") as f:
            f.write(text)
        return str(file_path)
    
    def read_file(path: str) -> str:
        with open(path) as f:
            return f.read()
    
    with patch("hapax.workflow.core.telemetry.get_tracer", return_value=mock_tracer):
        workflow = (
            Workflow()
            .add(write_file)
            .add(read_file)
        )
        
        result = await workflow.run("test", trace=True)
        
        # Should trace file operations
        span = mock_tracer.start_span.return_value.__enter__.return_value
        span.set_attribute.assert_any_call("file.path", str(file_path))

async def test_trace_sampling(mock_tracer):
    """Test trace sampling behavior."""
    with patch("hapax.workflow.core.telemetry.get_tracer", return_value=mock_tracer):
        # Run workflow multiple times
        workflow = Workflow().add(lambda x: str(x))  # type: Callable[[str], str]
        
        for _ in range(10):
            await workflow.run("test", trace=True)
        
        # Should respect sampling configuration
        assert mock_tracer.start_span.call_count >= 10
