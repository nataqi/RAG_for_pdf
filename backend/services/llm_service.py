from anthropic import Anthropic
from typing import Optional, List, Dict
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """Handles Claude API interactions"""

    def __init__(self):
        """Initialize Claude client"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-haiku-20241022"
        logger.info(f"LLMService initialized with model: {self.model}")
        
        
    def generate_answer(self,
                        question: str,
                        context_chunks:List[str],
                        max_tokens: int = 1024
                        ) -> str:
        
        """
        Generate answer using Claude with retrieved context.

        Args:
            question: User's question
            context_chunks: Retrieved relevant document chunks
            max_tokens: Maximum tokens in response

        Returns:
            Generated answer as string
        """
        
        # Format context chunks with numbering
        context = "\n\n".join([
            f"[Document {i+1}]:\n{chunk}"
            for i, chunk in enumerate(context_chunks)
        ])

        prompt = f"""You are a helpful assistant that answers questions based on provided document contexts.

        Context from documents:
        {context}

        Question: {question}

        Instructions:
        - Answer the question based primarily on the provided context
        - If the context doesn't contain enough information, say so
        - Be concise but complete
        - If you reference specific information, indicate which document it came from

        Answer:"""

        try:
            logger.info(f"Generating answer for question: {question[:50]}...")

            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            answer = message.content[0].text
            logger.info(f"Answer generated successfully ({len(answer)} chars)")
            return answer

        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
       