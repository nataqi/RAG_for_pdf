from backend.services.rag_service import RAGService


if __name__ == "__main__":
    rag_service = RAGService()

    print("=== Testing Document Processing ===")
    result = rag_service.process_document(file_path="sample.pdf", filename="sample.pdf")
    print(f"Processing result: {result}")
  
    

    print("\n=== Testing Question Answering ===")
    question = "What is Natalias education?"
    answer_result = rag_service.answer_question(question)

    if not answer_result.get('success'):
        print(f"Error: {answer_result.get('error')}")
        exit(1)

    print(f"Question: {answer_result['question']}")
    print(f"Answer: {answer_result['answer']}")
    print(f"\nSources:")
    for i, source in enumerate(answer_result['sources']):
        print(f"\nSource {i+1}:")
        print(f"  Filename: {source['filename']}")
        print(f"  Chunk index: {source['chunk_index']}")
        print(f"  Relevance score: {source['relevance_score']:.2f}")
        print(f"  Text: {source['chunk_text']}")