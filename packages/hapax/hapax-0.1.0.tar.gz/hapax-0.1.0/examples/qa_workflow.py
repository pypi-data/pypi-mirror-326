"""Example of wrapping LangChain's QA pattern in a workflow."""
from typing import List, Dict, Any
from dataclasses import dataclass
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from hapax.workflow.core import Workflow

@dataclass
class Document:
    """Simple document wrapper."""
    text: str
    metadata: Dict[str, Any] = None

@dataclass
class QAInput:
    """Input for QA workflow."""
    document: str
    question: str

def split_text(input: QAInput) -> List[Document]:
    """Split document into chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = splitter.split_text(input.document)
    return [Document(text=t) for t in texts]

def create_embeddings(chunks: List[Document]) -> Chroma:
    """Create embeddings and store in vector store."""
    embeddings = OpenAIEmbeddings()
    texts = [doc.text for doc in chunks]
    return Chroma.from_texts(
        texts,
        embeddings
    )

def setup_qa(vectorstore: Chroma) -> RetrievalQA:
    """Create QA chain."""
    llm = ChatOpenAI(temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

def get_answer(qa_input: tuple[RetrievalQA, QAInput]) -> str:
    """Get answer from QA chain."""
    qa_chain, input_data = qa_input
    return qa_chain.run(input_data.question)

async def main():
    # Create workflow
    qa_workflow = (
        Workflow()
        .add(split_text)          # Split document into chunks
        .add(create_embeddings)   # Create embeddings and store
        .add(setup_qa)            # Setup QA chain
        .add(get_answer)          # Get answer
    )
    
    # Example usage
    input_data = QAInput(
        document="""
        Hapax is a powerful library for building LLM applications.
        It provides workflows, tracing, and monitoring out of the box.
        Workflows are simple to create and can be validated before running.
        """,
        question="What features does Hapax provide?"
    )
    
    # Run with tracing
    try:
        answer = await qa_workflow.run(
            input=input_data,
            trace=True  # Enable OpenLLMetry tracing
        )
        print(f"\nQuestion: {input_data.question}")
        print(f"Answer: {answer}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
