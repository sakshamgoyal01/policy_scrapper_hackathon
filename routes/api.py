from fastapi import APIRouter, HTTPException
from models.schema import QueryRequest, QueryResponse
from services.parser import load_and_parse_documents
from services.embedding import retrieve_relevant_clauses
from services.query_eval import generate_answer_response

router = APIRouter()

@router.post("/hackrx/run", response_model=QueryResponse)
async def run_query(payload: QueryRequest):
    try:
        print("⚙️ Loading document")
        clauses = await load_and_parse_documents(payload.documents)
        print("✅ Parsed clauses:", len(clauses))
        results = []
        for q in payload.questions:
            relevant = retrieve_relevant_clauses(q, clauses)
            print(f"→ Q: {q} → Clauses:", [c["number"] for c in relevant])
            ans = await generate_answer_response(q, relevant)
            results.append(ans)
        return {"answers": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
