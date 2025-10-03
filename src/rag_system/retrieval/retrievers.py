import logging
from typing import List, Dict, Any, Optional

from ..config import SystemConfig
from ..vector_store import VectorStore, EmbeddingModel
from ..knowledge_graph import KnowledgeGraph
from .base import Retriever, RetrievalContext


logger = logging.getLogger(__name__)


class RAGRetriever(Retriever):
    """Standard RAG retriever using vector search"""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        config: SystemConfig,
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.config = config

    def retrieve(self, query: str, top_k: int = 5) -> RetrievalContext:
        """Retrieve relevant chunks using vector similarity"""

        # Create query embedding
        query_embedding = self.embedding_model.encode([query])[0]

        # Search vector store
        search_results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            score_threshold=self.config.retrieval.similarity_threshold,
        )

        # Extract chunks and scores
        chunks = [result.chunk for result in search_results]
        scores = [result.score for result in search_results]

        return RetrievalContext(
            text_chunks=chunks,
            vector_scores=scores,
            metadata={
                "retrieval_method": "rag",
                "query": query,
                "top_k": top_k,
                "num_results": len(chunks),
            },
        )

    def get_name(self) -> str:
        return "RAG"


class GraphRAGRetriever(Retriever):
    """Graph RAG retriever combining vector and graph search"""

    def __init__(
        self,
        vector_store: VectorStore,
        embedding_model: EmbeddingModel,
        knowledge_graph: KnowledgeGraph,
        config: SystemConfig,
    ):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.knowledge_graph = knowledge_graph
        self.config = config

    def retrieve(self, query: str, top_k: int = 5) -> RetrievalContext:
        """Retrieve using both vector similarity and graph traversal"""

        # Step 1: Vector retrieval
        query_embedding = self.embedding_model.encode([query])[0]
        search_results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            score_threshold=self.config.retrieval.similarity_threshold,
        )

        chunks = [result.chunk for result in search_results]
        scores = [result.score for result in search_results]

        # Step 2: Find entities in retrieved chunks
        entity_ids = []
        for chunk in chunks:
            # Find entities related to this chunk
            entities = self.knowledge_graph.get_entities_by_text(chunk.content[:100])
            entity_ids.extend([entity.id for entity in entities])

        # Remove duplicates
        entity_ids = list(set(entity_ids))

        # Step 3: Graph expansion
        graph_data = None
        if entity_ids:
            try:
                graph_data = self.knowledge_graph.get_subgraph(
                    entity_ids=entity_ids[: self.config.retrieval.max_graph_nodes],
                    depth=self.config.retrieval.graph_traversal_depth,
                )
                logger.debug(
                    f"Retrieved graph data with {len(graph_data.nodes)} nodes and {len(graph_data.edges)} edges"
                )
            except Exception as e:
                logger.warning(f"Error retrieving graph data: {e}")

        return RetrievalContext(
            text_chunks=chunks,
            vector_scores=scores,
            graph_data=graph_data,
            metadata={
                "retrieval_method": "graph_rag",
                "query": query,
                "top_k": top_k,
                "num_text_results": len(chunks),
                "num_entities": len(entity_ids),
                "graph_traversal_depth": self.config.retrieval.graph_traversal_depth,
            },
        )

    def get_name(self) -> str:
        return "Graph RAG"


class KnowledgeGraphRetriever(Retriever):
    """Pure knowledge graph retriever"""

    def __init__(self, knowledge_graph: KnowledgeGraph, config: SystemConfig):
        self.knowledge_graph = knowledge_graph
        self.config = config

    def _extract_entities_from_query(self, query: str) -> List:
        """Extract key entities from a natural language query"""
        import re
        from typing import List

        # Simple keyword extraction - look for key business/technical terms
        # Split into words and filter out common stop words
        stop_words = {
            "what",
            "is",
            "are",
            "the",
            "how",
            "can",
            "to",
            "of",
            "in",
            "for",
            "and",
            "or",
            "but",
            "with",
            "a",
            "an",
            "that",
            "this",
            "be",
            "do",
            "does",
            "will",
            "would",
            "should",
            "could",
            "have",
            "has",
            "had",
            "who",
            "when",
            "where",
            "why",
            "which",
            "on",
            "at",
            "by",
            "from",
        }

        # Extract words, remove punctuation, convert to lowercase
        words = re.findall(r"\b[a-zA-Z]+\b", query.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]

        # Try to find entities for each keyword and combinations
        all_entities = []

        # Single keywords
        for keyword in keywords:
            entities = self.knowledge_graph.get_entities_by_text(keyword)
            all_entities.extend(entities)

        # Try two-word combinations for better matches
        for i in range(len(keywords) - 1):
            combo = f"{keywords[i]} {keywords[i+1]}"
            entities = self.knowledge_graph.get_entities_by_text(combo)
            all_entities.extend(entities)

        # Remove duplicates by entity id
        seen_ids = set()
        unique_entities = []
        for entity in all_entities:
            if entity.id not in seen_ids:
                unique_entities.append(entity)
                seen_ids.add(entity.id)

        return unique_entities

    def retrieve(self, query: str, top_k: int = 5) -> RetrievalContext:
        """Retrieve using only knowledge graph"""

        # Extract key terms from the query instead of searching for the full question
        entities = self._extract_entities_from_query(query)

        if not entities:
            logger.warning(f"No entities found for query: {query}")
            return RetrievalContext(
                text_chunks=[],
                vector_scores=[],
                metadata={
                    "retrieval_method": "kg_only",
                    "query": query,
                    "num_results": 0,
                },
            )

        # Get subgraph around found entities
        entity_ids = [
            entity.id for entity in entities[: self.config.retrieval.max_graph_nodes]
        ]

        try:
            graph_data = self.knowledge_graph.get_subgraph(
                entity_ids=entity_ids, depth=self.config.retrieval.graph_traversal_depth
            )
        except Exception as e:
            logger.error(f"Error retrieving subgraph: {e}")
            graph_data = None

        return RetrievalContext(
            text_chunks=[],  # No text chunks in pure KG retrieval
            vector_scores=[],
            graph_data=graph_data,
            metadata={
                "retrieval_method": "kg_only",
                "query": query,
                "num_entities": len(entities),
                "graph_traversal_depth": self.config.retrieval.graph_traversal_depth,
            },
        )

    def get_name(self) -> str:
        return "Knowledge Graph Only"


class HybridRetriever(Retriever):
    """Hybrid retriever that can switch between methods"""

    def __init__(
        self, retrievers: Dict[str, Retriever], default_method: str = "graph_rag"
    ):
        self.retrievers = retrievers
        self.default_method = default_method
        self.current_method = default_method

    def retrieve(self, query: str, top_k: int = 5) -> RetrievalContext:
        """Retrieve using current method"""
        if self.current_method not in self.retrievers:
            logger.warning(
                f"Method {self.current_method} not available, using {self.default_method}"
            )
            self.current_method = self.default_method

        retriever = self.retrievers[self.current_method]
        return retriever.retrieve(query, top_k)

    def set_method(self, method: str) -> None:
        """Set the retrieval method"""
        if method in self.retrievers:
            self.current_method = method
            logger.info(f"Switched to retrieval method: {method}")
        else:
            logger.error(f"Unknown retrieval method: {method}")

    def get_available_methods(self) -> List[str]:
        """Get list of available retrieval methods"""
        return list(self.retrievers.keys())

    def get_name(self) -> str:
        return f"Hybrid ({self.current_method})"
