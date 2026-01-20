from backend.services.vector_store import VectorStore
from backend.services.embedding_service import EmbeddingService


if __name__ == "__main__":
    vector_store = VectorStore(collection_name="test_collection")
    embedding_service = EmbeddingService()
    
    docs = [
        "Python is a programming language",
        "Machine learning uses algorithms",
        "ChromaDB is a vector database",
        "FastAPI is a web framework"
    ]

    embeddings = embedding_service.encode_batch(docs)
    
    vector_store.add_documents(
        documents = docs,
        embeddings = embeddings,
        metadatas=[{"source": f"doc_{i}"} for i in range(len(docs))]
    )
    
    print(f"Total documents in store: {vector_store.count()}")
    
    query = "What is FastAPI?"
    query_embedding = embedding_service.encode_text(query)
    results = vector_store.search(query_embedding=query_embedding, n_results=2)
    
    print(f"\n Query : {query}")
    print(f" Top 2 Results:{results}")
    for doc, distance in zip(results['documents'][0], results['distances'][0]):
        print(f" Document: {doc} | Distance: {distance}")
        
    vector_store.delete_collection()