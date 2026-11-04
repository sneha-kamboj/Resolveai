from app.db.models import Order, Product, Return, Refund, Replacement, Ticket
from app.rules import engine

def get_order(db, order_id, customer_id):
    order = db.get(Order, order_id)
    if order is None or order.customer_id != customer_id:
        return None
    return order

def get_order_status(db, order_id, customer_id):
    order = get_order(db, order_id, customer_id)
    if order is None:
        return {"found": False}
    return {"found": True, "status": order.status, "amount": order.amount, "delivered_at": order.delivered_at}

def create_return(db, order_id, customer_id):
    order = get_order(db, order_id, customer_id)
    if order is None:
        return {"ok": False, "reason": "Order nahi mila"}
    existing = db.query(Return).filter(Return.order_id == order_id, Return.status == "initiated").first()
    if existing:
        return {"ok": True, "return_id": existing.id, "reason": "Return pehle se initiated hai"}
    ok, reason = engine.check_return(order, db.get(Product, order.product_id))
    if not ok:
        return {"ok": False, "reason": reason}
    r = Return(order_id=order.id, customer_id=customer_id)
    db.add(r); db.commit()
    return {"ok": True, "return_id": r.id, "reason": reason}

def initiate_refund(db, order_id, customer_id):
    order = get_order(db, order_id, customer_id)
    if order is None:
        return {"ok": False, "reason": "Order nahi mila"}
    existing = db.query(Refund).filter(Refund.order_id == order_id).first()
    if existing:
        return {"ok": True, "refund_id": existing.id, "reason": "Refund pehle se processed hai"}
    ok, reason = engine.check_auto_refund(order)
    if not ok:
        return {"ok": False, "reason": reason, "escalate": True}
    rf = Refund(order_id=order.id, amount=order.amount)
    db.add(rf); db.commit()
    return {"ok": True, "refund_id": rf.id, "reason": reason}

def create_replacement(db, order_id, customer_id):

    order = get_order(db, order_id, customer_id)
    if order is None:
        return {"ok": False, "reason": "Order nahi mila"}
    ok, reason = engine.check_replacement(order, db.get(Product, order.product_id))
    if not ok:
        return {"ok": False, "reason": reason}
    rp = Replacement(order_id=order.id, customer_id=customer_id)
    db.add(rp); db.commit()
    return {"ok": True, "replacement_id": rp.id, "reason": reason}

def escalate_to_human(db, ticket_id):
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        return {"ok": False, "reason": "Ticket nahi mila"}
    ticket.status = "escalated"
    db.commit()
    return {"ok": True, "reason": "Human team ko bhej diya"}
