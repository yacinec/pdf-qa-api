from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import numpy as np
import faiss

from app import config
from app.pdf_utils import extract_text_from_pdf, split_text_into_chunks
from app.vector_store import build_faiss_index, model as sentence_model
from app.llm_interface import ask_llm

app = FastAPI()

# Global cache
chunks_list = []
faiss_index = None

# Ensure upload folder exists
os.makedirs(config.UPLOAD_DIR, exist_ok=True)

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global chunks_list, faiss_index

    # --- Validations ---
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Incorrect MIME type.")

    contents = await file.read()
    if len(contents) > config.MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 10MB).")

    pdf_path = os.path.join(config.UPLOAD_DIR, config.PDF_FILENAME)
    with open(pdf_path, "wb") as f:
        f.write(contents)

    # --- Processing PDF ---
    try:
        text = extract_text_from_pdf(pdf_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error reading PDF.")

    chunks_list = split_text_into_chunks(text)
    if not chunks_list:
        raise HTTPException(status_code=400, detail="PDF is empty or unreadable.")

    faiss_index, _, _ = build_faiss_index(chunks_list)

    return {
        "message": "PDF uploaded and indexed successfully.",
        "nb_chunks": len(chunks_list),
        "vector_dim": faiss_index.d
    }


@app.get("/answer")
def answer_question(question: str, top_k: int = 3):
    global faiss_index, chunks_list

    if faiss_index is None or not chunks_list:
        raise HTTPException(status_code=400, detail="No PDF indexed yet. Upload one first.")

    question_vec = sentence_model.encode([question])
    D, I = faiss_index.search(np.array(question_vec), top_k)

    selected_chunks = [chunks_list[idx] for idx in I[0]]
    context = "\n\n".join(selected_chunks)

    answer = ask_llm(question, context)

    return {
        "question": question,
        "answer": answer,
        "chunks_used": selected_chunks
    }


@app.get("/")
def home():
    return {
        "message": "Ready to receive PDF. Upload via /upload_pdf."
    }
