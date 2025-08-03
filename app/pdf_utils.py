import fitz

def extract_text_from_pdf(path):
    with fitz.open(path) as doc:
        return chr(12).join([page.get_text() for page in doc])

def split_text_into_chunks(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks