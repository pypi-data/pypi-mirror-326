"""Semantic conventions for AI/LLM telemetry."""
from enum import Enum
from typing import Final

class LLMRequestTypeValues(str, Enum):
    """Values for LLM request types."""
    COMPLETION = "completion"
    CHAT = "chat"
    RERANK = "rerank"
    EMBEDDINGS = "embeddings"

class SpanAttributes:
    """Semantic attributes for AI/LLM spans."""
    # LLM attributes
    LLM_VENDOR: Final[str] = "ai.llm.vendor"
    LLM_REQUEST_TYPE: Final[str] = "ai.llm.request.type"
    LLM_REQUEST_MODEL: Final[str] = "ai.llm.request.model"
    LLM_RESPONSE_MODEL: Final[str] = "ai.llm.response.model"
    LLM_REQUEST_MAX_TOKENS: Final[str] = "ai.llm.request.max_tokens"
    LLM_RESPONSE_COMPLETION_TOKENS: Final[str] = "ai.llm.response.completion_tokens"
    LLM_RESPONSE_PROMPT_TOKENS: Final[str] = "ai.llm.response.prompt_tokens"
    LLM_RESPONSE_TOTAL_TOKENS: Final[str] = "ai.llm.response.total_tokens"
    LLM_TEMPERATURE: Final[str] = "ai.llm.temperature"
    LLM_TOP_P: Final[str] = "ai.llm.top_p"
    LLM_TOP_K: Final[str] = "ai.llm.top_k"
    LLM_FREQUENCY_PENALTY: Final[str] = "ai.llm.frequency_penalty"
    LLM_PRESENCE_PENALTY: Final[str] = "ai.llm.presence_penalty"
    
    # Embeddings attributes
    EMBEDDING_MODEL: Final[str] = "ai.embedding.model"
    EMBEDDING_DIMENSIONS: Final[str] = "ai.embedding.dimensions"
    
    # RAG attributes
    RAG_CHUNKS: Final[str] = "ai.rag.chunks"
    RAG_CHUNK_SIZE: Final[str] = "ai.rag.chunk_size"
    RAG_OVERLAP: Final[str] = "ai.rag.overlap"
    RAG_RETRIEVER: Final[str] = "ai.rag.retriever"
    RAG_QUERY: Final[str] = "ai.rag.query"
    RAG_DOCUMENTS: Final[str] = "ai.rag.documents"
    RAG_SCORE: Final[str] = "ai.rag.score"
