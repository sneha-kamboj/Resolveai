import json
import os
from app.rag.retriever import search

QUESTIONS = [
    ("What is the return policy?", "return_policy"),
    ("How many days do I have to return an item?", "return_policy"),
    ("When will I receive my refund?", "refund_timeline"),
    ("How long does it take for the money to be refunded?", "refund_timeline"),
    ("Which account will receive my refund if I paid through UPI?", "refund_method"),
    ("How will I receive a refund for a COD order?", "refund_method"),
    ("Can I get a replacement for a damaged item?", "replacement_policy"),
    ("I received a broken item and have sent a photo.", "damaged_item"),
    ("I received a different product that I did not order.", "wrong_item"),
    ("When will my parcel arrive and where can I find the tracking link?", "shipping_delivery"),
    ("I want to cancel my order. It has not been dispatched yet.", "order_cancellation"),
    ("I want to cancel my order before it gets shipped.", "order_cancellation"),
    ("Can I return an opened perfume?", "non_returnable_items"),
    ("How many months is the warranty for earbuds?", "warranty"),
    ("My smartwatch suddenly stopped working. Is it covered under warranty?", "warranty"),
    ("I purchased through EMI. When will the bank adjust my refund?", "emi_refund"),
    ("When will I receive a refund for an EMI purchase?", "emi_refund"),
    ("My shoes are too small. I want a different size.", "size_exchange"),
    ("Can I exchange the size of my T-shirt?", "size_exchange"),
    ("How are refunds above Rs. 5,000 approved?", "refund_method"),
]


def run_eval():
    top1 = 0
    hit3 = 0
    detail = []
    for q , expected in QUESTIONS:
         res = search(q)
         ids = [r["id"] for r in res]
         is_top1 = len(ids)>0 and ids[0] == expected
         is_hit3 = expected in ids
         top1 +=is_top1
         hit3 +=is_hit3
         detail.append({
			 "q": q,"expected": expected,
			 "got":ids,
			 "top1":is_top1,
			 "hit3":is_hit3,
		 })
         print(("PASS" if is_top1 else "miss"), "|", q, "->", ids[:1], "| expected:", expected)
    total = len(QUESTIONS)
    print("TOP1", top1, "/", total)
    print("HIT@3", hit3, "/", total)
    report = {"total": total, "top1": top1, "hit3": hit3, "detail": detail}
    os.makedirs("data", exist_ok=True)
    with open("data/rag_baseline_report.json", "w", encoding="utf-8") as f:
     json.dump(report, f, ensure_ascii=False, indent=2)
    print("SAVED data/rag_baseline_report.json")
    return report

if __name__ == "__main__":
    run_eval()



