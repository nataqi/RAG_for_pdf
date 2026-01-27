from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models.schemas import UploadResponse, QuestionRequest, AnswerResponse, StatsResponse
from backend.services.rag_service import RAGService


import os
from dotenv import load_dotenv
import shutil

load_dotenv()

router = APIRouter()
rag_service = RAGService()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./data/uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a PDF document"""
    
    #validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer) # Copies from MEMORY to DISK 
            
        # Process document
        result = rag_service.process_document(file_path, file.filename)
        
        return UploadResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        file.file.close()
        
        
@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about uploaded documents"""
    try:
        result = rag_service.answer_question(request.question, request.n_results)
        
        return AnswerResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get database statistics"""
    stats = rag_service.get_stats()
    return StatsResponse(**stats)


    