from backend.services.vector_store import VectorStore

vector_store = VectorStore()
results = vector_store.collection.get()

results = vector_store.collection.get()
print(f"Total chunks: {len(results['ids'])}\n")

for i, (id, doc, metadata) in enumerate(zip(
    results['ids'],
    results['documents'],
    results['metadatas']
)):
    print(f"=== Chunk {i+1} ===")
    print(f"ID: {id}")
    print(f"Text: {doc[:100]}...")
    print(f"Metadata: {metadata}")
    print()