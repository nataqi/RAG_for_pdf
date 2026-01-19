from sentence_transformers import SentenceTransformer
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
            Initialize embedding service.

            Args:
                model_name: Name of the sentence-transformer model
        """
        logger.info("Loading embedding model...")
        self.model = SentenceTransformer(model_name)
        logger.info(f"Model loaded succesfully: {model_name}")
        
    def encode_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text

        Returns:
            Embedding vector as list of floats
        """

        embedding = self.model.encode(text, convert_to_tensor=False)

        return embedding.tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        logger.info(f"Encoding batch of {len(texts)} texts...")
        embeddings = self.model.encode(texts, convert_to_tensor=False)

        return [emb.tolist() for emb in embeddings]