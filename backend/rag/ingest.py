import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

LEGAL_DOCS_PATH = "legal_docs"

# Load local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_documents():
    documents = []
    for filename in os.listdir(LEGAL_DOCS_PATH):
        if filename.endswith(".txt"):
            with open(os.path.join(LEGAL_DOCS_PATH, filename), "r", encoding="utf-8") as f:
                content = f.read()
                documents.append(content)
    return documents


def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks


def create_embeddings(text_chunks):
    embeddings = model.encode(text_chunks)
    return np.array(embeddings)


def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


if __name__ == "__main__":
    docs = load_documents()
    all_chunks = []

    for doc in docs:
        all_chunks.extend(chunk_text(doc))

    embeddings = create_embeddings(all_chunks)
    index = build_faiss_index(embeddings)

    faiss.write_index(index, "legal_index.faiss")

    # Save chunks separately
    with open("legal_chunks.pkl", "wb") as f:
        pickle.dump(all_chunks, f)

    print("FAISS index + chunks saved successfully (LOCAL model).")