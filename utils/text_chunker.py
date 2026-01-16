from typing import List
import logging 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextChunker:
    """Handles document chunking with overlap"""
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Initialize chunker.

        Args:
            chunk_size: Target size of each chunk in characters
            overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: The text to chunk

        Returns:
            List of text chunks
        """
        
        start = 0
        text_length = len(text)
        chunks = []
        
        if not text or not text.strip():
            logger.warning("Empty text provided for chunking")
            return []

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]

            # Try to break at sentence/word boundary if possible
            if end < text_length:
                # Look for last period, question mark, or exclamation
                last_sentence = max(chunk.rfind('.'), chunk.rfind('?'), chunk.rfind('!'))
                if last_sentence > self.chunk_size * 0.5:
                    end = start + last_sentence + 1
                    chunk = text[start:end] 

            chunks.append(chunk.strip())
            start = end - self.chunk_overlap

            logger.info(f"Created chunk {len(chunks)}")

        logger.info(f"Total chunks created: {len(chunks)} from text of length {text_length}")
        return chunks