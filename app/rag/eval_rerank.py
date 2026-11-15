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