from pydantic import BaseModel
from typing import List, Optional


class UploadResponse(BaseModel):
    success: bool
    filename: Optional[str] = None
    doc_id: Optional[str] = None
    chunks_count: Optional[int] = None
    total_chars: Optional[int] = None
    error: Optional[str] = None

class QuestionRequest(BaseModel):
    question: str
    n_results: int = 5

class Source(BaseModel):
    chunk_text: str
    filename: str
    chunk_index: int
    relevance_score: float

class AnswerResponse(BaseModel):
    success: bool
    question: Optional[str] = None
    answer: Optional[str] = None
    sources: Optional[List[Source]] = None
    error: Optional[str] = None

class StatsResponse(BaseModel):
    total_chunks: int