from typing import List, Dict, Optional
from backend.services.embedding_service import EmbeddingService
from backend.services.vector_store import VectorStore
from backend.services.llm_service import LLMService
from utils.pdf_processor import PDFProcessor
from utils.text_chunker import TextChunker
import logging
import os
import hashlib
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        """Initialize all services"""
        self.pdf_processor = PDFProcessor()
        self.text_chunker = TextChunker(chunk_size=500, overlap=50)
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm_service = LLMService()
        logger.info("RAG service initialized")
        
    def process_document(self, file_path: str, filename: str) -> Dict:
        """
        Process a document through the complete pipeline.

        Args:
            file_path: Path to the PDF file
            filename: Original filename

        Returns:
            Dictionary with processing results
        """
        logger.info(f"Processing document: {filename}")
        
        # Extract text from PDF
        text = self.pdf_processor.extract_text(file_path)
        if not text:
            logger.error(f"Failed to extract text from {filename}")
            return {"success": False, "error": "Text extraction failed"}
        
        #chunk text
        chunks = self.text_chunker.chunk_text(text)
        if not chunks:
            logger.error(f"No chunks created from {filename}")
            return {"success": False, "error": "No text chunks created"}
        
        # Generate embeddings
        embeddings = self.embedding_service.generate_embeddings(chunks)
        if not embeddings:
            logger.error(f"Embedding generation failed for {filename}")
            return {"success": False, "error": "Embedding generation failed"}
        
        # Store in vector database
        doc_id = self._generate_doc_id(filename)
        for i in range(len(chunks)):
            metadatas = {
                "source_file": filename,
                "chunk_index": i,
                "doc_id": doc_id,
                "timestamp": datetime.now().isoformat()
            }
            
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        
        logger.info(f"Document processed successfully: {len(chunks)} chunks stored")

        return {
            "success": True,
            "filename": filename,
            "doc_id": doc_id,
            "chunks_count": len(chunks),
            "total_chars": len(text)
        }
        
    def answer_question(self, question: str, n_results: int = 5) -> Dict:
        """
        Answer a question using RAG.

        Args:
            question: User's question
            n_results: Number of chunks to retrieve

        Returns:
            Dictionary with answer and sources
        """
        # generate question embedding
        question_embedding = self.embedding_service.encode_text(question)

        # retrieve relevant chunks
        search_results = self.vector_store.search(query_embedding=question_embedding, n_results=n_results)
        if not search_results['documents'][0]:
            return {
                "success": False,
                "error": "No documents found in database"
            }

        # generate answer using LLM
        context_chunks = search_results['documents'][0]
        answer = self.llm_service.generate_answer(question, context_chunks)
        
        #format response with sources
        sources = []
        for i, (doc, metadata, distance) in enumerate(zip(
            search_results['documents'][0],
            search_results['metadatas'][0],
            search_results['distances'][0]
        )):
            sources.append({
                "chunk_text": doc[:200] + "..." if len(doc) > 200 else doc,
                "filename": metadata.get('filename', 'Unknown'),
                "chunk_index": metadata.get('chunk_index', i),
                "relevance_score": float(1 - distance)  # Convert distance to similarity
            })

        logger.info("Question answered successfully")

        return {
            "success": True,
            "question": question,
            "answer": answer,
            "sources": sources
        }
        
    def _generate_doc_id(self, filename: str) -> str:
        """Generate unique document ID"""
        return hashlib.md5(
        f"{filename}_{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]

    def get_stats(self) -> Dict:
        """Get database statistics"""
        return {
            "total_chunks": self.vector_store.count()
        }
    