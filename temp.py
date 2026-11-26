import re

from app.triage.predict import predict
from app.rag import retriever as R
from app.agent import tools


def extract_order_id(text):
    m = re.search(r"order[^0-9]*(\d+)", text.lower())
    if m:
        return int(m.group(1))

    m = re.search(r"\b(\d{3,6})\b", text)
    return int(m.group(1)) if m else None


def _result(status, intent, conf, reply, order_id=None, citation=None):
    return {
        "status": status,
        "intent": intent,
        "confidence": round(conf, 3),
        "reply": reply,
        "order_id": order_id,
        "citation": citation
    }


def _escalate(db, customer_id, text, intent, conf, reply):
    tools.escalate_to_human(db, customer_id, text)
    return _result("escalated", intent, conf, reply)


def handle_message(db, customer_id, text, order_id=None):
    intent, conf = predict(text)

    if intent == "escalate" or conf < 0.45:
        return _escalate(
            db, customer_id, text, intent, conf,
            "I'm forwarding your request to our support team. They will assist you shortly."
        )

    if intent == "policy_question":
        hits = R.search(text)

        if not hits:
            return _escalate(
                db, customer_id, text, intent, conf,
                "I couldn't find an answer to your question in our policies. I'm forwarding it to our support team."
            )

        top = hits[0]
        reply = top["text"] + f"\n(Source: {top['title']})"

        return _result(
            "answered", intent, conf, reply,
            citation=top["id"]
        )

    oid = order_id or extract_order_id(text)

    if oid is None:
        return _result(
            "need_order", intent, conf,
            "Please provide your Order ID so I can check it for you."
        )

    order = tools.get_order(db, customer_id, oid)

    if order is None:
        return _result(
            "not_found", intent, conf,
            "No order associated with your account was found with this ID. Please check the ID and try again."
        )

    if intent == "order_status":
        reply = f"Order #{oid}: Status = {order.status}, Amount = Rs. {order.amount}."

        if order.delivered_at:
            reply += f" Delivered on {order.delivered_at.date()}."

        return _result("answered", intent, conf, reply, order_id=oid)

    action = {
        "return": tools.create_return,
        "refund": tools.initiate_refund,
        "replacement": tools.create_replacement
    }[intent]

    ok, msg = action(db, customer_id, oid)

    return _result(
        "resolved" if ok else "rejected",
        intent, conf, msg,
        order_id=oid
    )


if __name__ == "__main__":
    from app.db.base import SessionLocal

    db = SessionLocal()

    demo = [
        (1, "Where is my order 496?"),
        (1, "I want to return order 496."),
        (1, "I want to return order 497."),
        (1, "How many days does a refund take?"),
        (2, "Where is my order 496?"),
        (1, "xyz random nonsense"),
    ]

    for cid, text in demo:
        r = handle_message(db, cid, text)

        print("\n>", text, "| Customer:", cid)
        print(" ", r["status"], "|", r["intent"], "|", r["confidence"])
        print(" ", r["reply"][:120])

    db.close()