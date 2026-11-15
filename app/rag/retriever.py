from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.rag.policies import POLICIES

MIN_SCORE = 0.08

_vectorizer = TfidfVectorizer(ngram_range=(1, 2))
_corpus = [p["title"] + " " + p["text"] for p in POLICIES]
_matrix = _vectorizer.fit_transform(_corpus)

def search(query, top_k=3):
    if not query or not query.strip():
        return []
    q_vec = _vectorizer.transform([query])
    scores = cosine_similarity(q_vec, _matrix)[0]
    order = scores.argsort()[::-1]
    results = []
    for i in order:
        score = float(scores[i])
        if score < MIN_SCORE:
            break
        p = POLICIES[int(i)]
        results.append({
            "id": p["id"],
            "title": p["title"],
            "text": p["text"],
            "score": round(score, 3),
        })
        if len(results) == top_k:
            break
    return results

if __name__ == "__main__":
    demo = [
		"i have alredy gave the cash on delivery but the app is asking to pay again"
        "return policy kya hai kitne din me item wapas kar sakte hain",
        "refund kitne din me milega paise kab aayenge",
        "mera item toota hua damaged aaya hai",
        "asdf qwer zxcv",
    ]
    for q in demo:
        res = search(q)
        print("\nQ:", q)
        if not res:
            print("  NO RESULT")
        for r in res:
            print(" ", r["score"], r["id"])
