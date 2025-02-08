"""Example of using the DAG-based pipeline system."""
import asyncio
from typing import Any, Dict
from hapax.pipeline.dag import (
    DAGPipeline,
    PipelineNode,
    ExecutionMode,
    branch_if
)

async def extract_text(data: Dict[str, Any]) -> str:
    """Extract text from input data."""
    await asyncio.sleep(0.1)  # Simulate work
    return data["text"]

async def analyze_sentiment(text: str) -> Dict[str, float]:
    """Analyze sentiment of text."""
    await asyncio.sleep(0.2)  # Simulate work
    return {"positive": 0.8, "negative": 0.2}

async def check_toxicity(text: str) -> Dict[str, bool]:
    """Check text for toxicity."""
    await asyncio.sleep(0.15)  # Simulate work
    return {"is_toxic": False}

async def summarize_text(text: str) -> str:
    """Summarize text."""
    await asyncio.sleep(0.3)  # Simulate work
    return "Summary: " + text[:50] + "..."

async def store_results(data: Dict[str, Any]) -> Dict[str, Any]:
    """Store analysis results."""
    await asyncio.sleep(0.1)  # Simulate work
    return {"status": "stored", "data": data}

async def notify_if_toxic(data: Dict[str, bool]) -> None:
    """Send notification if content is toxic."""
    if data["is_toxic"]:
        print("ALERT: Toxic content detected!")

def is_toxic(data: Dict[str, bool]) -> bool:
    """Check if content is toxic."""
    return data["is_toxic"]

async def main():
    # Create pipeline
    pipeline = DAGPipeline("text_analysis")
    
    # Add nodes with different execution modes and dependencies
    pipeline.add_node(
        PipelineNode(
            name="extract",
            func=extract_text,
            execution_mode=ExecutionMode.SEQUENTIAL
        )
    )
    
    # These can run in parallel after extract
    pipeline.add_node(
        PipelineNode(
            name="sentiment",
            func=analyze_sentiment,
            inputs=["extract"],
            execution_mode=ExecutionMode.PARALLEL
        ),
        dependencies=["extract"]
    )
    
    pipeline.add_node(
        PipelineNode(
            name="toxicity",
            func=check_toxicity,
            inputs=["extract"],
            execution_mode=ExecutionMode.PARALLEL
        ),
        dependencies=["extract"]
    )
    
    # Summarize runs after sentiment analysis
    pipeline.add_node(
        PipelineNode(
            name="summarize",
            func=summarize_text,
            inputs=["extract"],
            execution_mode=ExecutionMode.SEQUENTIAL
        ),
        dependencies=["sentiment"]
    )
    
    # Store results after all analysis
    pipeline.add_node(
        PipelineNode(
            name="store",
            func=store_results,
            inputs=["sentiment", "toxicity", "summarize"],
            execution_mode=ExecutionMode.SEQUENTIAL
        ),
        dependencies=["summarize", "toxicity"]
    )
    
    # Notify runs conditionally based on toxicity check
    pipeline.add_node(
        PipelineNode(
            name="notify",
            func=notify_if_toxic,
            inputs=["toxicity"],
            execution_mode=ExecutionMode.CONCURRENT
        ),
        dependencies=[("toxicity", branch_if(is_toxic))]
    )
    
    # Execute pipeline
    try:
        input_data = {
            "text": "This is a sample text that needs to be analyzed."
        }
        
        results = await pipeline.execute(input_data)
        
        print("\nPipeline Results:")
        print("----------------")
        for node, result in results.items():
            if node != "__input__":
                print(f"{node}: {result}")
    
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
