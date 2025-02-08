"""Tests for workflow function validation and type compatibility."""
import pytest
from typing import Any, Dict, List, Optional, Union, TypeVar, Callable
from hapax.workflow.core import Workflow, validate_callable, validate_workflow, is_compatible_type

T = TypeVar('T')

def test_basic_function_validation(test_functions):
    """Test validation of basic function signatures."""
    # Should pass - proper typed function
    validate_callable(test_functions["basic_typed"])
    
    # Should fail - no parameters
    def no_params() -> str:
        return "test"
    
    with pytest.raises(ValueError, match="must take exactly one parameter"):
        validate_callable(no_params)
    
    # Should fail - too many parameters
    def many_params(x: int, y: int) -> int:
        return x + y
    
    with pytest.raises(ValueError, match="must take exactly one parameter"):
        validate_callable(many_params)
    
    # Should fail - *args
    def var_args(*args: List[Any]) -> List[Any]:
        return list(args)
    
    with pytest.raises(ValueError, match="must take exactly one parameter"):
        validate_callable(var_args)

def test_method_validation(test_functions):
    """Test validation of different method types."""
    # Instance method
    validate_callable(test_functions["method"])
    
    # Class method
    validate_callable(test_functions["class_method"])
    
    # Static method
    validate_callable(test_functions["static_method"])

def test_async_function_validation(test_functions):
    """Test validation of async functions."""
    validate_callable(test_functions["async"])

def test_type_hint_validation():
    """Test validation of type hints."""
    # Should fail - no type hints
    def no_hints(x):
        return x
    
    with pytest.raises(ValueError, match="must have a type hint"):
        validate_callable(no_hints)
    
    # Should pass - various type hints
    def optional_hint(x: Optional[str]) -> str:
        return x or ""
    validate_callable(optional_hint)
    
    def union_hint(x: Union[int, str]) -> str:
        return str(x)
    validate_callable(union_hint)
    
    def any_hint(x: Any) -> Any:
        return x
    validate_callable(any_hint)

def test_workflow_type_compatibility():
    """Test type compatibility between workflow steps."""
    workflow = Workflow()
    
    # Compatible types
    def step1(x: str) -> int:
        return len(x)
    
    def step2(x: int) -> str:
        return "x" * x
    
    workflow.add(step1).add(step2)
    validate_workflow(workflow)
    
    # Incompatible types
    def step3(x: List[str]) -> List[int]:
        return [ord(c) for c in x[0]]
    
    workflow = Workflow()
    workflow.add(step1).add(step3)
    with pytest.raises(TypeError, match="is not compatible with"):
        validate_workflow(workflow)

def test_subclass_compatibility():
    """Test type compatibility with subclasses.
    
    This test demonstrates correct type relationships in workflow steps:
    
    Covariance (return types):
        - If a function returns a Dog, it can be used where an Animal is expected
        - This is safe because anywhere that expects an Animal can handle a Dog
    
    Contravariance (parameter types):
        - If a function accepts an Animal, it can handle any Animal, including Dogs
        - This is safe because the function promises to only use Animal behaviors
    """
    class Animal:
        pass
    
    class Dog(Animal):
        pass
    
    workflow = Workflow()
    
    def step1(x: str) -> Dog:
        return Dog()
    
    def step2(x: Animal) -> str:
        return "ok"
    
    # This should work because:
    # 1. step1 returns Dog (specific)
    # 2. step2 accepts Animal (general)
    # 3. Since Dog is-an Animal, step2 can safely handle step1's output
    workflow.add(step1).add(step2)
    validate_workflow(workflow)
    
    # Test the opposite relationship (should fail)
    workflow = Workflow()
    
    def step3(x: str) -> Animal:
        return Animal()
    
    def step4(x: Dog) -> str:
        return "ok"
    
    # This should fail because:
    # 1. step3 returns Animal (general)
    # 2. step4 accepts Dog (specific)
    # 3. Not every Animal is a Dog, so this is unsafe
    workflow.add(step3).add(step4)
    with pytest.raises(TypeError):
        validate_workflow(workflow)

def test_optional_type_compatibility():
    """Test compatibility with Optional types."""
    workflow = Workflow()
    
    def step1(x: str) -> Optional[int]:
        return len(x)
    
    def step2(x: Optional[int]) -> str:
        return str(x or 0)
    
    # Optional[int] -> Optional[int] should work
    workflow.add(step1).add(step2)
    validate_workflow(workflow)
    
    def step3(x: int) -> str:
        return str(x)
    
    # Optional[int] -> int should fail
    workflow = Workflow()
    workflow.add(step1).add(step3)
    with pytest.raises(TypeError, match="is not compatible with"):
        validate_workflow(workflow)

def test_collection_type_compatibility():
    """Test compatibility with collection types."""
    workflow = Workflow()
    
    def step1(x: str) -> List[int]:
        return [ord(c) for c in x]
    
    def step2(x: List[int]) -> List[str]:
        return [chr(i) for i in x]
    
    # List[int] -> List[int] should work
    workflow.add(step1).add(step2)
    validate_workflow(workflow)
    
    def step3(x: List[str]) -> List[int]:
        return [len(s) for s in x]
    
    # List[int] -> List[str] should fail
    workflow = Workflow()
    workflow.add(step1).add(step3)
    with pytest.raises(TypeError, match="is not compatible with"):
        validate_workflow(workflow)

def test_any_type_compatibility():
    """Test compatibility with Any type."""
    workflow = Workflow()
    
    def step1(x: Any) -> Any:
        return x
    
    def step2(x: int) -> str:
        return str(x)
    
    # Any -> Any should work
    workflow.add(step1).add(step2)
    validate_workflow(workflow)
    
    def step3(x: str) -> Any:
        return x
    
    # Any -> Any should work
    workflow.add(step3).add(step1)
    validate_workflow(workflow)

def test_empty_workflow_validation():
    """Test validation of empty workflow."""
    workflow = Workflow()
    with pytest.raises(ValueError, match="must have at least one step"):
        validate_workflow(workflow)
