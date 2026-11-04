from datetime import datetime, timedelta
from app.db.models import Order, Product
from app.rules.engine import check_return, check_replacement, check_auto_refund

now = datetime.now()
def make_order(days_ago, amount=1000, status="delivered"):
    return Order(status=status, amount=amount,
                 delivered_at=now - timedelta(days=days_ago) if status == "delivered" else None)
ret = Product(name="Shoes", price=1000, returnable=True)
nonret = Product(name="Cream", price=300, returnable=False)

def test_return_last_day_pass():
    assert check_return(make_order(7), ret, now)[0] == True
def test_return_day8_fail():
    assert check_return(make_order(8), ret, now)[0] == False
def test_return_nonreturnable_fail():
    assert check_return(make_order(1), nonret, now)[0] == False
def test_return_not_delivered_fail():
    assert check_return(make_order(0, status="shipped"), ret, now)[0] == False

def test_replacement_day15_pass(): assert check_replacement(make_order(15), ret, now)[0] == True
def test_replacement_day16_fail(): assert check_replacement(make_order(16), ret, now)[0] == False
def test_refund_5000_pass(): assert check_auto_refund(make_order(1, amount=5000))[0] == True
def test_refund_5001_fail(): assert check_auto_refund(make_order(1, amount=5001))[0] == False
