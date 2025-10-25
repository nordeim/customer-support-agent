# backend/app/vector_store/embeddings.py
import torch
from transformers import AutoTokenizer, AutoModel
from typing import List
from ..core.logging import logger
from ..core.config import settings

class EmbeddingModel:
    """Wrapper for the embedding model from HuggingFace"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.embedding_model_name
        
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            
            # Move model to GPU if available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            
            logger.info(
                f"Loaded embedding model: {self.model_name} on {self.device}",
                extra={"tool_name": "embedding_model", "model": self.model_name, "device": str(self.device)}
            )
        except Exception as e:
            logger.error(
                f"Failed to load embedding model {self.model_name}: {str(e)}",
                extra={"tool_name": "embedding_model", "model": self.model_name}
            )
            raise
    
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a query"""
        try:
            # Tokenize input
            inputs = self.tokenizer(query, return_tensors="pt", truncation=True, padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use mean pooling of the last hidden state
                embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            
            # Convert to list
            return embeddings[0].tolist()
        except Exception as e:
            logger.error(
                f"Failed to embed query: {str(e)}",
                extra={"tool_name": "embedding_model"}
            )
            raise
    
    def embed_document(self, document: str) -> List[float]:
        """Generate embedding for a document"""
        # For now, use the same method as query embedding
        # In a more advanced implementation, we might chunk the document
        # and embed each chunk separately
        return self.embed_query(document)
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents"""
        embeddings = []
        for doc in documents:
            try:
                embedding = self.embed_document(doc)
                embeddings.append(embedding)
            except Exception as e:
                logger.error(
                    f"Failed to embed document: {str(e)}",
                    extra={"tool_name": "embedding_model"}
                )
                # Add a zero embedding as a fallback
                embeddings.append([0.0] * self.model.config.hidden_size)
        
        return embeddings
