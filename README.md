# RAG Document Q&A Assistant

A learning project for building a document question-answering system using Retrieval-Augmented Generation (RAG).

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Vector Database:** ChromaDB
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **LLM:** Claude API (Anthropic)
- **PDF Processing:** PyPDF2

## Setup

### 1. Activate virtual environment
```bash
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root with:
```
ANTHROPIC_API_KEY=your_key_here
```

### 4. Run the backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`

### 5. Run the frontend (Streamlit)
In a separate terminal:
```bash
streamlit run frontend/app.py
```
The UI will open at `http://localhost:8501`