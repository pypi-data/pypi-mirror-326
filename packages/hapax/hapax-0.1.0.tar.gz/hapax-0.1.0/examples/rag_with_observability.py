"""Example of using Hapax observability with a RAG pipeline for semi-structured data."""

from dataclasses import dataclass
from typing import List, Optional
from uuid import uuid4
import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.storage import InMemoryStore
from langchain.retrievers import MultiVectorRetriever

from hapax.core import obs
from hapax.pipeline import Pipeline
from hapax.workflow.core import Workflow


HAPAX_URL = os.getenv("HAPAX_URL", "http://localhost:9090")

class HapaxLLM:
    """LLM client that uses Hapax server."""
    
    def __init__(self):
        self.url = f"{HAPAX_URL}/v1/completions"
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True
    )
    def __call__(self, prompt):
        """Send completion request to Hapax server with retry logic."""
        try:
            # Convert prompt to string if it's a ChatPromptValue
            if hasattr(prompt, "to_string"):
                prompt = prompt.to_string()
            
            response = requests.post(
                self.url,
                json={"input": prompt},
                headers={"Content-Type": "application/json"},
                timeout=30  # Add timeout
            )
            response.raise_for_status()
            return response.json()["content"]
        except requests.exceptions.RequestException as e:
            if response := getattr(e, 'response', None):
                error_detail = response.json().get('error', str(e))
                raise RuntimeError(f"Hapax server error: {error_detail}")
            raise RuntimeError(f"Failed to connect to Hapax server: {str(e)}")


@dataclass
class Element:
    """A document element that can be either text or a table."""
    type: str
    content: str


@dataclass
class RagState:
    """State for the RAG pipeline."""
    query: str
    context: Optional[List[str]] = None
    answer: Optional[str] = None
    error: Optional[str] = None


class SemiStructuredRagPipeline(Pipeline):
    """Pipeline for RAG over semi-structured data (text and tables)."""
    
    def __init__(self):
        """Initialize the pipeline."""
        self.__name__ = "semi_structured_rag"  # Required for workflow compatibility
        self.name = "semi_structured_rag"
        # Initialize vectorstore and retriever
        self.vectorstore = Chroma(
            collection_name="summaries",
            embedding_function=OpenAIEmbeddings()
        )
        self.store = InMemoryStore()
        self.retriever = MultiVectorRetriever(
            vectorstore=self.vectorstore,
            docstore=self.store,
            id_key="doc_id",
        )
        
        # Initialize LLM and prompts
        self.llm = HapaxLLM()
        self.summary_prompt = ChatPromptTemplate.from_template(
            "You are an assistant tasked with summarizing tables and text. "
            "Give a concise summary of the table or text. Content: {element}"
        )
        self.qa_prompt = ChatPromptTemplate.from_template(
            "Answer the question based only on the following context, "
            "which can include text and tables:\n{context}\nQuestion: {question}"
        )
        
        # Initialize chains
        self.summarize_chain = (
            {"element": lambda x: x}
            | self.summary_prompt
            | self.llm
            | StrOutputParser()
        )
        self.qa_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.qa_prompt
            | self.llm
            | StrOutputParser()
        )
    
    def __call__(self, input_data: str) -> str:
        """Execute the pipeline.
        
        Args:
            input_data: The question to ask the RAG pipeline.
            
        Returns:
            The answer generated using both text and table context.
        """
        return self.run(input_data)
    
    @obs(name="add_elements", attributes={"num_elements": lambda self, elements: len(elements)})
    def add_elements(self, elements: List[Element]) -> None:
        """Add text and table elements to the retriever."""
        for element in elements:
            # Generate unique ID
            doc_id = str(uuid4())
            
            # Get summary using the chain
            @obs(name="summarize_element", attributes={"element_type": lambda self, element: element.type})
            def _summarize(element):
                return self.summarize_chain.invoke(element.content)
            
            summary = _summarize(element)
            
            # Add to retriever
            @obs(name="add_to_retriever")
            def _add_to_retriever(summary, doc_id, element):
                # Add summary to vectorstore
                self.vectorstore.add_documents([
                    Document(
                        page_content=summary,
                        metadata={"doc_id": doc_id}
                    )
                ])
                # Add raw content to docstore
                self.store.mset([(doc_id, Document(
                    page_content=element.content,
                    metadata={"type": element.type}
                ))])
            
            _add_to_retriever(summary, doc_id, element)
    
    @obs(name="rag_pipeline", attributes={"query": lambda self, state: state.query})
    def run(self, state: RagState) -> RagState:
        """Run the RAG pipeline."""
        try:
            # Get context using retriever
            @obs(name="retrieve_context")
            def _retrieve(state):
                context = self.retriever.invoke(state.query)
                state.context = [doc.page_content for doc in context]
            
            _retrieve(state)
            
            # Generate answer
            @obs(name="generate_answer")
            def _generate(state):
                state.answer = self.qa_chain.invoke(state.query)
            
            _generate(state)
            return state
        except Exception as e:
            state.error = str(e)
            return state


def create_workflow() -> Workflow:
    """Create a workflow that uses the RAG pipeline."""
    # Create sample elements
    elements = [
        Element(
            type="text",
            content="LLaMA2 is a large language model trained on 2 trillion tokens."
        ),
        Element(
            type="table",
            content="""
            | Model     | Parameters | Training Tokens |
            |-----------|------------|----------------|
            | LLaMA2-7B | 7B        | 2T            |
            | LLaMA2-13B| 13B       | 2T            |
            | LLaMA2-70B| 70B       | 2T            |
            """
        )
    ]
    
    # Create and initialize pipeline
    pipeline = SemiStructuredRagPipeline()
    pipeline.add_elements(elements)
    
    # Create workflow
    workflow = Workflow()
    workflow.add(pipeline)
    
    return workflow


if __name__ == "__main__":
    # Create and run workflow
    workflow = create_workflow()
    
    # Run query
    result = workflow.run(
        RagState(query="What is the number of training tokens for LLaMA2?")
    )
    
    # Print results
    print(f"Query: {result.query}")
    print(f"Context: {result.context}")
    print(f"Answer: {result.answer}")
    if result.error:
        print(f"Error: {result.error}")
