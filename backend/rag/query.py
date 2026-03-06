import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load index
index = faiss.read_index("legal_index.faiss")

# Load stored chunks
with open("legal_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


def search_legal_docs(query, top_k=1):
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding)

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(chunks[idx])

    # Create a simple structured answer
    combined_text = "\n\n".join(results)

    formatted_response = {
        "answer": combined_text,
        "chunks_used": len(results)
    }

    return formatted_response
