# 🧠 PDF Question-Answering API with Mistral

This project is a local API that allows you to upload a PDF, automatically index its content using FAISS and SentenceTransformers, and ask semantic questions answered by a local LLM (Mistral 7B Instruct via `llama-cpp-python`).

---

## Features

- Upload and validate PDF files
- Extract and chunk text from PDF
- Create vector index (FAISS + `all-MiniLM-L6-v2`)
- Ask semantic questions using a local Mistral model
- No internet required — works fully offline after model download

---

## Project Structure

```
pdf_qa_api/
├── app/
│ ├── main.py
│ ├── pdf_utils.py
│ ├── vector_store.py
│ ├── llm_interface.py
│ └── config.py
├── models/
├── uploads/
├── requirements.txt
└── README.md
```

---

## Quickstart

1. Clone this repo
2. Download a `.gguf` model (e.g. Mistral 7B Instruct) into `models/`
3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the API:
```bash
uvicorn app.main:app --reload
```

5. Open the docs: http://localhost:8000/docs

## Endpoints

- `POST /upload_pdf`: Upload a PDF (max 10MB) → triggers indexing
- `GET /answer?question=...`: Ask a semantic question about the PDF

## Dependencies

- FastAPI
- PyMuPDF
- sentence-transformers
- faiss-cpu
- llama-cpp-python


## Security

- Validates MIME type and size
- Refuses non-PDF files


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
