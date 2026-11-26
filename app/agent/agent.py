import re

from app.db.models import Ticket
from app.agent import tools
from app.triage.predict import predict
from app.rag import retriever as R


def extract_order_id(text):
    m = re.search(r"order[^0-9]*(\d+)", text.lower())
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d{3,6})\b", text)
    return int(m.group(1)) if m else None


def _result(status, intent, conf, reply, ticket_id, order_id=None, citation=None):
    return {
        "status": status,
        "intent": intent,
        "confidence": round(conf, 3),
        "reply": reply,
        "ticket_id": ticket_id,
        "order_id": order_id,
        "citation": citation,
    }


def _escalate(db, ticket, intent, conf, reply):
    tools.escalate_to_human(db, ticket.id)
    return _result("escalated", intent, conf, reply, ticket.id, order_id=ticket.order_id)


def handle_message(db, customer_id, text, order_id=None):
    intent, conf = predict(text)
    oid = order_id or extract_order_id(text)

    ticket = Ticket(customer_id=customer_id, order_id=oid, message=text, intent=intent)
    db.add(ticket)
    db.commit()

    if intent == "escalate" or conf < 0.45:
        return _escalate(db, ticket, intent, conf,
                         "I am forwarding this to our support team. They will help you from here.")

    if intent == "policy_question":
        hits = R.search(text)
        if not hits:
            return _escalate(db, ticket, intent, conf,
                             "I could not find this in our policies, so I am forwarding it to our team.")
        top = hits[0]
        ticket.status = "resolved"
        db.commit()
        reply = top["text"] + f"\n(Source: {top['title']})"
        return _result("answered", intent, conf, reply, ticket.id, citation=top["id"])

    if oid is None:
        return _result("need_order", intent, conf,
                       "Please share your order ID so I can check right away.", ticket.id)

    order = tools.get_order(db, oid, customer_id)
    if order is None:
        return _result("not_found", intent, conf,
                       "No order associated with your account was found with this ID. Please check the ID and try again.",
                       ticket.id, order_id=oid)

    if intent == "order_status":
        info = tools.get_order_status(db, oid, customer_id)
        reply = f"Order #{oid}: status = {info['status']}, amount = Rs. {info['amount']}."
        if info["delivered_at"]:
            reply += f" Delivered on {info['delivered_at'].date()}."
        ticket.status = "resolved"
        db.commit()
        return _result("answered", intent, conf, reply, ticket.id, order_id=oid)

    action = {
        "return": tools.create_return,
        "refund": tools.initiate_refund,
        "replacement": tools.create_replacement,
    }[intent]
    res = action(db, oid, customer_id)

    if res["ok"]:
        ticket.status = "resolved"
        db.commit()
        return _result("resolved", intent, conf, res["reason"], ticket.id, order_id=oid)

    if res.get("escalate"):
        return _escalate(db, ticket, intent, conf,
                         res["reason"] + " I am forwarding this to our team for approval.")

    return _result("rejected", intent, conf, res["reason"], ticket.id, order_id=oid)


if __name__ == "__main__":
    from app.db.base import SessionLocal

    db = SessionLocal()
    demo = [
        (1, "Where is my order 496?"),
        (1, "I want to return order 496"),
        (1, "I want to return order 497"),
        (1, "Refund for order 499 please"),
        (1, "How long does it take for the money to be refunded?"),
        (2, "Where is my order 496?"),
        (1, "xyz abcdefghi"),
    ]
    for cid, text in demo:
        r = handle_message(db, cid, text)
        print("\n>", text, "| Customer:", cid)
        print(" ", r["status"], "|", r["intent"], "|", r["confidence"], "| ticket", r["ticket_id"])
        print(" ", r["reply"][:150])
    db.close()