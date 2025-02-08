# Hapax

A flexible workflow system for LLM applications with built-in observability.

## Features

- Simple, intuitive workflow creation
- Built-in OpenTelemetry tracing
- Type-safe workflow validation
- Parallel and conditional execution
- LangChain integration

## Installation

```bash
pip install hapax
```

## Quick Start

```python
from hapax.workflow import Workflow

# Create a simple workflow
workflow = (
    Workflow()
    .add(load_document)
    .add(split_text)
    .add(create_embeddings)
    .add(search_relevant)
    .add(generate_answer)
)

# Run with tracing
result = await workflow.run(
    input={"document": doc, "question": "What is...?"},
    trace=True
)
```

## RAG with Observability Example

The `examples/rag_with_observability.py` demonstrates how to build a Retrieval-Augmented Generation (RAG) pipeline with built-in observability using Hapax. This example showcases:

- Processing both text and tabular data
- Using LangChain's MultiVectorRetriever for improved retrieval
- Adding observability using the `@obs` decorator
- Error handling and state management
- Type-safe workflow validation

To run the example:

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your-api-key
```

3. Run the test script:
```bash
python examples/test_rag_pipeline.py
```

The example will demonstrate:
- Loading and processing semi-structured data (text and tables)
- Generating summaries for improved retrieval
- Answering questions using both context types
- Observability metrics and tracing throughout the pipeline

## Development

1. Clone the repository:
```bash
git clone https://github.com/teilomillet/hapax-py.git
cd hapax-py
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
```

3. Run tests:
```bash
pytest tests/ -v
```

## License

MIT License