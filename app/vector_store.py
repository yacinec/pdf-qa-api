from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def build_faiss_index(chunks):
    vectors = model.encode(chunks)
    dimension = vectors[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))
    return index, vectors, model