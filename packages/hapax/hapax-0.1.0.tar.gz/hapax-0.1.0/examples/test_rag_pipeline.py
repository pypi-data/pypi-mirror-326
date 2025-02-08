"""Test script for the RAG pipeline with observability."""

import os
import asyncio
import requests
from rag_with_observability import Element, RagState, create_workflow, HAPAX_URL

def check_hapax_server():
    """Check if the Hapax server is running."""
    try:
        response = requests.get(f"{HAPAX_URL}/health")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

async def test_rag_pipeline():
    """Test the RAG pipeline with various queries."""
    # Create workflow
    workflow = create_workflow()
    
    # Add more test data
    elements = [
        Element(
            type="text",
            content="""
            Claude is an AI assistant created by Anthropic. It is known for its 
            strong performance on tasks requiring reasoning and analysis.
            """
        ),
        Element(
            type="table",
            content="""
            | Model     | Creator   | Release Date | Key Features                    |
            |-----------|-----------|--------------|----------------------------------|
            | Claude    | Anthropic | 2023        | Reasoning, Analysis             |
            | GPT-4     | OpenAI   | 2023        | General Intelligence, Safety    |
            | LLaMA2    | Meta     | 2023        | Open Source, Customizable       |
            """
        ),
        Element(
            type="text",
            content="""
            GPT-4 is a large language model developed by OpenAI. It demonstrates 
            strong capabilities across a wide range of tasks and has improved safety features.
            """
        )
    ]
    
    # Test queries
    test_queries = [
        "What are the different AI models and who created them?",
        "What are the key features of GPT-4?",
        "When was LLaMA2 released and what makes it special?",
        "Compare the features of Claude and GPT-4.",
    ]
    
    # Run tests
    for query in test_queries:
        print(f"\n{'='*80}\nTesting query: {query}\n{'='*80}")
        
        try:
            # Initialize state
            state = RagState(query=query)
            
            # Run the workflow
            result = await workflow.run(state)
            
            # Print results
            print("\nContext:")
            if result.context:
                for i, ctx in enumerate(result.context, 1):
                    print(f"{i}. {ctx}")
            else:
                print("No context found")
            
            print("\nAnswer:", result.answer or "No answer generated")
            
            if result.error:
                print("\nError:", result.error)
                
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")

async def main():
    """Main function to run tests."""
    # Check if Hapax server is running
    if not check_hapax_server():
        print(f"""
Error: Hapax server is not running!

Please start the mock Hapax server:
1. Open a new terminal
2. Run: python examples/mock_hapax_server.py

The server should be running on {HAPAX_URL}
""")
        return
    
    print(f"Hapax server is running on {HAPAX_URL}")
    await test_rag_pipeline()

if __name__ == "__main__":
    # Ensure you have set your OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("""
Error: OpenAI API key not found!

Please set your OpenAI API key using one of these methods:

1. Export as environment variable:
   export OPENAI_API_KEY=your-api-key-here

2. Create a .env file in the project root:
   OPENAI_API_KEY=your-api-key-here

You can get an API key from: https://platform.openai.com/api-keys
""")
        exit(1)
    
    asyncio.run(main())
