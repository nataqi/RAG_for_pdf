from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router

# Create FastAPI instance
app = FastAPI(
    title = "Document Q&A API",
    description = "RAG-based document question answering system",
    version = "1.0.0"
)

# Add CORS middleware (allow frontend to call API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["RAG"])

@app.get("/")
async def root():
    return {
        "message": "Document Q&A API",
        "docs": "/docs",
        "endpoints": {
            "upload": "/api/upload",
            "ask": "/api/ask",
            "stats": "/api/stats"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

