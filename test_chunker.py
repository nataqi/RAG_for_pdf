from utils.text_chunker import TextChunker


if __name__ == "__main__":
    sample_text = """
Artificial intelligence has transformed the way we interact with technology in the modern world. Machine learning algorithms power everything from recommendation systems on streaming platforms to autonomous vehicles navigating complex urban environments. The field of natural language processing has made remarkable strides, enabling computers to understand and generate human language with unprecedented accuracy. Deep learning models, particularly transformer architectures, have revolutionized tasks such as translation, summarization, and question answering.

The evolution of AI can be traced back to the 1950s when pioneers like Alan Turing first proposed the concept of machine intelligence. Early systems were rule-based and limited in scope, but the introduction of neural networks in the 1980s marked a significant turning point. The recent explosion in computing power and availability of large datasets has accelerated progress dramatically. Today's AI systems can recognize images, understand speech, play complex games at superhuman levels, and even create original artwork and music.

However, the rapid advancement of AI also raises important ethical considerations. Questions about bias in algorithms, privacy concerns, job displacement, and the potential for misuse of AI technologies are actively debated by researchers, policymakers, and the public. Ensuring that AI development proceeds responsibly and benefits all of humanity remains one of the most critical challenges facing our society. The future of AI will depend not only on technical innovations but also on our ability to address these broader societal implications and establish appropriate governance frameworks.

Looking ahead, the integration of AI into various sectors promises to continue reshaping our world. Healthcare is being revolutionized through AI-powered diagnostic tools and personalized treatment plans. Education is becoming more adaptive and accessible through intelligent tutoring systems. Scientific research is accelerating as AI helps analyze vast amounts of data and generate new hypotheses. Climate change mitigation efforts are benefiting from AI's ability to optimize energy systems and model complex environmental processes. As we navigate this transformative era, collaboration between technologists, domain experts, ethicists, and policymakers will be essential to harness AI's potential while mitigating its risks.
"""

chunker = TextChunker(chunk_size=500, chunk_overlap=50)
chunks = chunker.chunk_text(sample_text)

print(f"Total chunks created: {len(chunks)}")
for idx, chunk in enumerate(chunks):
    print(f"\n--- Chunk {idx + 1} ---\n{chunk}\n")


