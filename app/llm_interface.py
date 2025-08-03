from llama_cpp import Llama
from app.config import MODEL_PATH

llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

def ask_llm(question, context):
    prompt = f"""### Instruction:
You're a clever assistant. Here is a document extracted from PDF.

{context}

### Question:
{question}

### Answer:"""
    response = llm(prompt, max_tokens=256, temperature=0.7)
    return response["choices"][0]["text"].strip()