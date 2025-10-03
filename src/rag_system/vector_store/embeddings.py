import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer
import torch

from .base import EmbeddingModel


class SentenceTransformerEmbedding(EmbeddingModel):
    """Sentence Transformer based embedding model"""
    
    def __init__(
        self, 
        model_name: str = "all-MiniLM-L6-v2",
        device: str = "cpu",
        batch_size: int = 32
    ):
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        
        # Load model
        self.model = SentenceTransformer(model_name, device=device)
        
        # Get model info
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.max_seq_length = self.model.max_seq_length
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts into embeddings"""
        if not texts:
            return np.array([])
        
        # Process in batches
        embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i + self.batch_size]
            batch_embeddings = self.model.encode(
                batch_texts,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            embeddings.append(batch_embeddings)
        
        return np.vstack(embeddings) if embeddings else np.array([])
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.dimension
    
    def get_max_sequence_length(self) -> int:
        """Get maximum sequence length"""
        return self.max_seq_length
    
    def encode_single(self, text: str) -> np.ndarray:
        """Encode a single text"""
        return self.model.encode([text], convert_to_numpy=True)[0]


class TransformerEmbedding(EmbeddingModel):
    """Hugging Face Transformers based embedding model"""
    
    def __init__(
        self, 
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        device: str = "cpu",
        batch_size: int = 32
    ):
        from transformers import AutoTokenizer, AutoModel
        
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(device)
        self.model.eval()
        
        # Set max sequence length
        self.max_seq_length = self.tokenizer.model_max_length
        if self.max_seq_length > 512:
            self.max_seq_length = 512
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts into embeddings"""
        if not texts:
            return np.array([])
        
        embeddings = []
        
        with torch.no_grad():
            for i in range(0, len(texts), self.batch_size):
                batch_texts = texts[i:i + self.batch_size]
                
                # Tokenize
                inputs = self.tokenizer(
                    batch_texts,
                    padding=True,
                    truncation=True,
                    max_length=self.max_seq_length,
                    return_tensors="pt"
                )
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                # Get embeddings
                outputs = self.model(**inputs)
                
                # Use mean pooling
                batch_embeddings = self._mean_pooling(outputs, inputs['attention_mask'])
                embeddings.append(batch_embeddings.cpu().numpy())
        
        return np.vstack(embeddings) if embeddings else np.array([])
    
    def _mean_pooling(self, model_output, attention_mask):
        """Apply mean pooling to get sentence embeddings"""
        token_embeddings = model_output.last_hidden_state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.model.config.hidden_size
    
    def get_max_sequence_length(self) -> int:
        """Get maximum sequence length"""
        return self.max_seq_length


def create_embedding_model(model_name: str, device: str = "cpu", batch_size: int = 32) -> EmbeddingModel:
    """Factory function to create embedding models"""
    
    # Try SentenceTransformer first (more optimized)
    try:
        return SentenceTransformerEmbedding(model_name, device, batch_size)
    except Exception:
        # Fallback to Transformers
        return TransformerEmbedding(model_name, device, batch_size)