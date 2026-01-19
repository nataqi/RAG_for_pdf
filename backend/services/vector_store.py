import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorStore:
    """Handles vector database operations with ChromaDB"""

    def __init__(self, collection_name: str = "documents"):
        """Initialize ChromaDB client and collection"""
        db_path = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")

        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Document chunks with embeddings"}
        )
        logger.info(f"Vector store initialized with collection: {collection_name}")

    def add_documents(
        self, 
        documents: List[str],
        embeddings: List[List[float]], 
        metadatas: Optional[List[Dict]] = None, 
        ids: Optional[List[str]] = None
    ):
        """
        Add documents with their embeddings to the vector store.

        Args:
            documents: List of text chunks
            embeddings: List of embedding vectors
            metadatas: Optional metadata for each document
            ids: Optional custom IDs for documents
        """
        if not ids:
            [f"doc_{i}" for i in range(len(documents))]
            
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(documents)} documents to vector store")
        
    

    def search(self, query_embedding: List[float], n_results: int = 5) -> Dict:
        """
        Search for similar documents.

        Args:
            query_embedding: Embedding vector of the query
            n_results: Number of results to return

        Returns:
            Dictionary containing documents, distances, and metadata
        """
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
        logger.info(f"Search completed, found {len(results['documents'][0])} results")
        
        return results
    
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(self.collection.name)
        logger.info(f"Deleted collection: {self.collection.name}")
    
    def count(self) -> int:
        """Return the number of documents in the collection"""
        return self.collection.count()