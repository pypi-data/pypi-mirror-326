"""Test fixtures and utilities for workflow tests."""
from typing import List, Dict, Any, Optional, Union
import pytest
from dataclasses import dataclass
from hapax.workflow.core import Workflow
import asyncio
from typing import Generator

@dataclass
class TestData:
    """Test data structure."""
    value: Any
    metadata: Dict[str, Any] = None

@pytest.fixture
def simple_workflow() -> Workflow:
    """Create a simple workflow for testing."""
    return Workflow()

@pytest.fixture
def test_functions():
    """Collection of test functions with different signatures."""
    
    # Basic typed functions
    def func_with_type(x: int) -> str:
        return str(x)
    
    def func_no_types(x):
        return x
    
    async def async_func(x: str) -> str:
        return x.upper()
    
    # Class-based functions
    class TestClass:
        def method(self, x: str) -> str:
            return x
        
        @classmethod
        def class_method(cls, x: int) -> int:
            return x * 2
        
        @staticmethod
        def static_method(x: float) -> float:
            return x + 1.0
    
    # Functions with different type patterns
    def func_with_optional(x: Optional[str]) -> str:
        return x or ""
    
    def func_with_list(x: List[int]) -> int:
        return sum(x)
    
    def func_with_any(x: Any) -> Any:
        return x
    
    def func_with_union(x: Union[int, str]) -> str:
        return str(x)
    
    return {
        "basic_typed": func_with_type,
        "no_types": func_no_types,
        "async": async_func,
        "method": TestClass().method,
        "class_method": TestClass.class_method,
        "static_method": TestClass.static_method,
        "optional": func_with_optional,
        "list": func_with_list,
        "any": func_with_any,
        "union": func_with_union,
    }

@pytest.fixture
def mock_llm():
    """Mock LLM for testing."""
    class MockLLM:
        def __init__(self, responses=None):
            self.responses = responses or ["Mock response"]
            self.calls = []
        
        async def complete(self, prompt: str) -> str:
            self.calls.append(prompt)
            return self.responses[len(self.calls) - 1]
    
    return MockLLM()

@pytest.fixture
def sample_data() -> Dict:
    """Sample data for testing."""
    return {
        "text": "Sample text for testing",
        "numbers": [1, 2, 3, 4, 5],
        "nested": {
            "key": "value",
            "list": ["a", "b", "c"]
        }
    }

@pytest.fixture
def error_functions():
    """Collection of functions that raise errors."""
    def value_error(x: str) -> None:
        raise ValueError("Test value error")
    
    def type_error(x: str) -> None:
        raise TypeError("Test type error")
    
    async def async_error(x: str) -> None:
        raise RuntimeError("Test async error")
    
    return {
        "value_error": value_error,
        "type_error": type_error,
        "async_error": async_error,
    }
