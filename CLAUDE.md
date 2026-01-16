# RAG Document Q&A Assistant

## Project Overview
A full-stack application for uploading PDF documents and asking questions about them using Retrieval-Augmented Generation (RAG). This is a learning project focused on understanding ML pipelines, vector databases, and modern web frameworks.

## Tech Stack
- **Frontend/UI:** Streamlit
- **Backend API:** FastAPI  
- **Vector Database:** ChromaDB
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **LLM:** Claude API (Anthropic)
- **PDF Processing:** PyPDF2 or pdfplumber

## Project Structure
```
backend/
├── api/          # FastAPI endpoints
├── services/     # RAG logic, embeddings, vector DB
├── models/       # Data models/schemas
frontend/         # Streamlit UI
data/
├── uploads/      # User-uploaded PDFs
├── chroma_db/    # Vector database storage
```

## Key Decisions
- **Secrets:** Using .env file, never commit to git
- **Environment:** Virtual environment (venv/) per project
- **Development approach:** Build incrementally, understand each piece

## How RAG Works Here
1. User uploads PDF → extract text → chunk into pieces
2. Generate embeddings for each chunk → store in ChromaDB
3. User asks question → embed question → find similar chunks
4. Send chunks + question to Claude API → get answer

## Current Status
[Update as you progress]
- [x] Project structure created
- [x] Basic FastAPI setup
- [x] PDF upload and processing
- [ ] Embedding generation
- [ ] Vector DB integration
- [ ] Query and retrieval
- [ ] LLM integration
- [ ] Streamlit UI

## Communication Preferences

### When Answering Clarifying Questions
When I ask questions while learning:
1. **Start with a concise explanation** - Give me the core concept in 2-3 paragraphs
2. **Wait before providing code examples** - Only include detailed code if I ask for it
3. **Use simple language first** - Explain the "why" before the "how"
4. **Provide code examples when I ask** - If I say "show me an example" or "can you explain with code", then provide detailed examples

**Example:**
- ❌ Don't: Immediately paste 50+ lines of code with detailed examples
- ✅ Do: Explain the concept clearly, then ask if I want to see code examples

This helps me understand concepts without getting overwhelmed by code initially.

## Resources
- Project description: `description.md`
- Implementation plan: `IMPLEMENTATION_PLAN.md`
- Learnings: `learnings/` folder