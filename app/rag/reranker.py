from sklearn.metrics.pairwise import cosine_similarity

from app.rag.policies import POLICIES
from app.rag import retriever as R

MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"
_model = None

def _load():
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder
        _model = CrossEncoder(MODEL_NAME)
    return _model

def _norm(scores):
    lo, hi = min(scores), max(scores)
    if hi == lo:
        return [1.0 for _ in scores]
    return [(s - lo) / (hi - lo) for s in scores]

def _mmr(cands, rel, top_k=3, lam=0.7):
    selected = []
    pool = list(range(len(cands)))
    while pool and len(selected) < top_k:
        best_i, best_val = None, -1e9
        for i in pool:
            if not selected:
                val = rel[i]
            else:
                sims = [float(cosine_similarity(R._matrix[cands[i]["idx"]],
                                                R._matrix[cands[j]["idx"]])[0][0])
                        for j in selected]
                val = lam * rel[i] - (1 - lam) * max(sims)
            if val > best_val:
                best_val, best_i = val, i
        selected.append(best_i)
        pool.remove(best_i)
    return [cands[i] for i in selected]

def rerank(query, top_k=3):
    cands = R.search(query, top_k=10)
    if not cands:
        return []
    model = _load()
    pairs = [(query, c["title"] + " " + c["text"]) for c in cands]
    scores = [float(s) for s in model.predict(pairs)]
    rel = _norm(scores)
    id_to_idx = {p["id"]: i for i, p in enumerate(POLICIES)}
    for c, s in zip(cands, scores):
        c["idx"] = id_to_idx[c["id"]]
        c["rerank_score"] = round(s, 3)
    ordered = _mmr(cands, rel, top_k=top_k)
    for c in ordered:
        c.pop("idx", None)
    return ordered

if __name__ == "__main__":
    demo = [
        "How many days do I have to return an item?",
        "When will I receive my refund?",
        "Can I return an opened perfume?",
    ]
    for q in demo:
        before = R.search(q)
        after = rerank(q)
        print("\nQ:", q)
        print("  pehle :", before[0]["id"] if before else "NO RESULT")
        print("  rerank:", after[0]["id"] if after else "NO RESULT")
