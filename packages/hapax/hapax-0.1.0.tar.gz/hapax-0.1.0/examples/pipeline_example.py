"""Example of using Hapax's pipeline system with OpenLLMetry tracing."""
from hapax.pipeline import (
    PipelineManager,
    ResourceType,
)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import asyncio

# Example resource handlers
async def openai_handler(config):
    """Handle OpenAI LLM resources."""
    # In real implementation, this would initialize an OpenAI client
    return {"status": "initialized", "model": config.get("model")}

async def pinecone_handler(config):
    """Handle Pinecone vector database resources."""
    # In real implementation, this would initialize Pinecone
    return {"status": "initialized", "index": config.get("index")}

async def chain_handler(config):
    """Handle LLM chain resources."""
    # In real implementation, this would set up an LLM chain
    return {"status": "initialized", "chain_type": config.get("type")}

def setup_opentelemetry():
    """Set up OpenTelemetry tracing."""
    provider = TracerProvider()
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

async def main():
    # Set up tracing
    setup_opentelemetry()
    
    # Create pipeline manager
    manager = PipelineManager()
    
    # Register resource handlers
    manager.register_handler(ResourceType.LLM, "openai", openai_handler)
    manager.register_handler(ResourceType.VECTORDB, "pinecone", pinecone_handler)
    manager.register_handler(ResourceType.CHAIN, "basic", chain_handler)
    
    # Create pipeline from YAML
    yaml_config = """
    name: qa_pipeline
    resources:
      - name: gpt4
        type: llm
        provider: openai
        config:
          model: gpt-4
          temperature: 0.7
          
      - name: knowledge_base
        type: vectordb
        provider: pinecone
        config:
          index: qa-index
          
      - name: qa_chain
        type: chain
        provider: basic
        config:
          type: qa
        depends_on:
          - gpt4
          - knowledge_base
    """
    
    pipeline = PipelineManager.from_yaml(yaml_config)
    
    try:
        # Apply pipeline
        results = await manager.apply(pipeline)
        print("\nPipeline results:")
        for resource_name, result in results.items():
            print(f"{resource_name}: {result}")
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
