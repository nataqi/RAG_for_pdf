from backend.services.embedding_service import EmbeddingService
import numpy as np

def cosine_similarity(emb1, emb2):
    return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

if __name__ == "__main__":
    service = EmbeddingService()
    
    
    text1 = "The cat sits on the mat"
    text2 = "A cat is sitting on a mat"
    text3 = "The weather is sunny today"
    
    emb1 = service.encode_text(text1)
    emb2 = service.encode_text(text2)
    emb3 = service.encode_text(text3)
    
    sim_1_2 = cosine_similarity(emb1, emb2)
    sim_1_3 = cosine_similarity(emb1, emb3)
    
    print(f"Cosine similarity between text1 and text2: {sim_1_2}")
    print(f"Cosine similarity between text1 and text3: {sim_1_3}")
    
    print(len(emb1), len(emb2), len(emb3))
    
    
