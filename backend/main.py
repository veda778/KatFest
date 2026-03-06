from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.user_form import UserForm
from rules.engine import check_eligibility
from rag.query import search_legal_docs
from rag.generator import generate_answer

app = FastAPI(title="AI Legal Literacy & Eligibility Assistant")

# ✅ Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------
# Root endpoint
# -------------------------------
@app.get("/")
def root():
    return {"message": "AI Legal Assistant Backend is Running"}


# -------------------------------
# Eligibility Endpoint
# -------------------------------
@app.post("/api/check-eligibility")
def eligibility(user: UserForm):
    eligible_schemes = check_eligibility(user)

    return {
        "eligible_schemes": eligible_schemes,
        "count": len(eligible_schemes)
    }


# -------------------------------
# Legal RAG Endpoint
# -------------------------------
@app.post("/api/legal-query")
def legal_query(request: dict):
    query = request.get("query")

    if not query:
        return {"error": "Query is required."}

    # Step 1: Retrieve relevant law chunks
    retrieval_result = search_legal_docs(query)

    context = retrieval_result["answer"]

    # Step 2: Generate final answer using LLM
    generated_answer = generate_answer(context, query)

    return {
        "query": query,
        "generated_answer": generated_answer,
        "sources_used": retrieval_result["chunks_used"],
        "disclaimer": "This system provides legal information, not legal advice. Please consult a qualified legal professional for formal guidance."
    }