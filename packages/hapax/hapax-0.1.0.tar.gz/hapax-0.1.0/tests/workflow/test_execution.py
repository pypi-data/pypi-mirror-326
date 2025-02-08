"""Tests for workflow execution patterns."""
import pytest
import asyncio
from typing import Any, Dict, List, Optional, Union, Callable
from hapax.workflow.core import Workflow, ConditionalStep

async def test_sequential_execution(simple_workflow):
    """Test basic sequential execution."""
    def step1(x: str) -> int:
        return len(x)
    
    def step2(x: int) -> str:
        return "x" * x
    
    workflow = simple_workflow.add(step1).add(step2)
    result = await workflow.run("test")
    assert result == "xxxx"  # len("test") = 4

async def test_parallel_execution():
    """Test parallel execution of steps."""
    async def slow_upper(x: str) -> str:
        await asyncio.sleep(0.1)
        return x.upper()
    
    async def slow_lower(x: str) -> str:
        await asyncio.sleep(0.1)
        return x.lower()
    
    workflow = (
        Workflow()
        .map([slow_upper, slow_lower])
    )
    
    # Should execute both functions in parallel
    start_time = asyncio.get_event_loop().time()
    result = await workflow.run("Test")
    end_time = asyncio.get_event_loop().time()
    
    assert isinstance(result, list)
    assert "TEST" in result
    assert "test" in result
    assert end_time - start_time < 0.2  # Should take ~0.1s, not 0.2s

async def test_conditional_execution():
    """Test conditional branching."""
    def is_positive(x: int) -> bool:
        return x > 0

    def format_positive(x: int) -> str:
        return f"Positive: {x}"

    def format_negative(x: int) -> str:
        return f"Non-positive: {x}"
    
    workflow = (
        Workflow()
        .when(
            is_positive,
            then=lambda w: w.add(format_positive),
            else_=lambda w: w.add(format_negative)
        )
    )
    
    # Test positive case
    result = await workflow.run(5)
    assert result == "Positive: 5"
    
    # Test negative case
    result = await workflow.run(-5)
    assert result == "Non-positive: -5"

async def test_mixed_sync_async():
    """Test mixing synchronous and asynchronous functions."""
    def sync_step(x: str) -> str:
        return x.upper()
    
    async def async_step(x: str) -> str:
        await asyncio.sleep(0.1)
        return x + "!"
    
    workflow = (
        Workflow()
        .add(sync_step)
        .add(async_step)
    )
    
    result = await workflow.run("test")
    assert result == "TEST!"

async def test_error_handling(error_functions):
    """Test error handling in workflows."""
    # Test ValueError
    workflow = Workflow().add(error_functions["value_error"])
    with pytest.raises(ValueError, match="Test value error"):
        await workflow.run("test")
    
    # Test async error
    workflow = Workflow().add(error_functions["async_error"])
    with pytest.raises(RuntimeError, match="Test async error"):
        await workflow.run("test")
    
    # Test error in parallel execution
    workflow = (
        Workflow()
        .map([
            error_functions["value_error"],
            error_functions["type_error"]
        ])
    )
    with pytest.raises(Exception):  # Should raise first error encountered
        await workflow.run("test")

async def test_complex_workflow(sample_data):
    """Test a more complex workflow with multiple patterns."""
    def extract_text(data: Dict[str, Any]) -> str:
        return data["text"]

    def count_words(text: str) -> int:
        return len(text.split())

    async def process_numbers(data: Dict[str, Any]) -> List[int]:
        await asyncio.sleep(0.1)
        return [x * 2 for x in data["numbers"]]

    def process_text(data: Dict[str, Any]) -> int:
        """Process text by extracting it and counting words."""
        text = extract_text(data)
        return count_words(text)

    def format_result(x: List[Any]) -> Dict[str, Any]:
        return {
            "word_count": x[0],
            "processed_numbers": x[1]
        }

    def check_length(x: Dict[str, Any]) -> bool:
        return x["word_count"] > 3

    def format_long(x: Dict[str, Any]) -> str:
        return f"Long text with {x['word_count']} words"

    def format_short(x: Dict[str, Any]) -> str:
        return "Short text"

    # Create the conditional branches
    then_branch = Workflow().add(format_long)
    else_branch = Workflow().add(format_short)

    workflow = (
        Workflow()
        .map([
            # Branch 1: Process text
            process_text,
            # Branch 2: Process numbers
            process_numbers
        ])
        .add(format_result)
        .add(ConditionalStep(check_length, then_branch, else_branch))
    )

    result = await workflow.run(sample_data)
    assert isinstance(result, str)
    assert "Long text" in result or result == "Short text"

async def test_large_data_workflow():
    """Test workflow with large data structures."""
    large_list = list(range(10000))

    def process_chunk(chunk: List[int]) -> List[int]:
        return [x * 2 for x in chunk]

    def chunk_data(data: List[int]) -> List[List[int]]:
        return [data[i:i+100] for i in range(0, len(data), 100)]

    def flatten_results(data: List[List[int]]) -> List[int]:
        """Flatten a list of lists into a single list."""
        return [item for sublist in data for item in sublist]

    workflow = (
        Workflow()
        .add(chunk_data)
        .map([process_chunk] * 100)  # Process chunks in parallel
        .add(flatten_results)  # Flatten
    )

    result = await workflow.run(large_list)
    assert isinstance(result, list)
    assert len(result) == len(large_list)
    assert all(x == i * 2 for i, x in enumerate(result))

async def test_resource_cleanup(tmp_path):
    """Test resource cleanup in workflows."""
    file_path = tmp_path / "test.txt"
    
    def create_file(x: Any) -> str:
        with open(file_path, "w") as f:
            f.write("test")
        return str(file_path)
    
    def read_file(path: str) -> str:
        with open(path) as f:
            return f.read()
        
    def cleanup_file(result: str) -> str:
        if file_path.exists():
            file_path.unlink()
        return result
    
    workflow = (
        Workflow()
        .add(create_file)
        .add(read_file)
        .add(cleanup_file)
    )
    
    result = await workflow.run(None)
    assert result == "test"
    assert not file_path.exists()  # File should be cleaned up
