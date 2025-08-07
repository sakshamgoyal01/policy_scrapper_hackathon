from sentence_transformers import SentenceTransformer, util
from utils.splitter import split_into_clauses

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_clauses(question: str, clauses: list[dict]):
    texts = [c["text"] for c in clauses]
    embeddings = model.encode(texts, convert_to_tensor=True)
    q_emb = model.encode(question, convert_to_tensor=True)
    hits = util.semantic_search(q_emb, embeddings, top_k=5)[0]
    results = []
    for hit in hits:
        idx = hit["corpus_id"]
        results.append({**clauses[idx], "score": float(hit["score"])})
    return results
