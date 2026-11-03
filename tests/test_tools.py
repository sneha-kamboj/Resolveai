from app.db.base import Base, engine, SessionLocal
from app.agent import tools

Base.metadata.create_all(engine)
db = SessionLocal()

def test_status_owner(): assert tools.get_order_status(db, 496, 1)["found"] == True
def test_status_other_customer(): assert tools.get_order_status(db, 496, 2)["found"] == False
def test_return_idempotent():
    r1 = tools.create_return(db, 496, 1)
    r2 = tools.create_return(db, 496, 1)
    assert r1["ok"] and r1["return_id"] == r2["return_id"]
def test_return_window_fail(): assert tools.create_return(db, 497, 1)["ok"] == False
def test_refund_5000_pass(): assert tools.initiate_refund(db, 498, 1)["ok"] == True
def test_refund_5001_escalate():
    res = tools.initiate_refund(db, 499, 1)
    assert res["ok"] == False and res["escalate"] == True
