import json
from app.rag.eval_rag import QUESTIONS
from app.rag.reranker import rerank

def run_eval():
	top1 = 0
	hit3 = 0
	detail = []
	for q,expected in QUESTIONS:
		ids = [r["id"] for r in rerank(q)]
		is_top1 = len("ids") >0 and ids[0] == expected
		is_hit3 = expected in ids
		top1 += is_top1
		hit3 +=is_hit3
		detail.append(
			{
				"q": q,
				"expected": expected,
		 		"got":ids,
		        "top1":is_top1,
				"hit3":is_hit3,
			}
		)


		print(("PASS" if is_top1 else "miss"), "|", q, "->", ids[:1], "| expected:", expected)
	with open("data/rag_baseline_report.json",encoding="utf-8") as f:
		base = json.load(f)
		report = {
       "baseline": {"top1": base["top1"], "hit3": base["hit3"], "total": base["total"]},
        "rerank": {"top1": top1, "hit3": hit3, "total": len(QUESTIONS)},
        "detail": detail,
	}
	with open("data/rerank_report.json", "w", encoding="utf-8") as f:
		json.dump(report, f, ensure_ascii=False, indent=2)
		print("BASELINE  TOP1", base["top1"], "/", base["total"], "| HIT@3", base["hit3"], "/", base["total"])
		print("RERANK    TOP1", top1, "/", len(QUESTIONS), "| HIT@3", hit3, "/", len(QUESTIONS))
		print("SAVED data/rerank_report.json")

if __name__ == "__main__":
	run_eval()
