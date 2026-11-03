
from datetime import date

RETURN_WINDOW_DAYS = 7
REPLACEMENT_DAYS = 15
AUTO_REFUND_LIMIT = 5000


VALID_REPLACEMENT_REASONS = ("damaged", "defective", "wrong",
                             "toota", "toot", "phata", "kharab", "galat")

def _days_since(delivery_date, today=None):
    if delivery_date is None:
        return None
    today = today or date.today()
    return (today - delivery_date).days

def check_return(order, product, today=None):

    days = _days_since(order.delivery_date, today)
    if order.status != "delivered":
        return {"eligible": False, "reason": f"Order status is '{order.status}', not 'delivered'. Returns apply only to delivered orders.", "days_since_delivery": days}
    if days is None:
        return {"eligible": False, "reason": "Order has no delivery date.", "days_since_delivery": None}
    if days > RETURN_WINDOW_DAYS:
        return {"eligible": False, "reason": f"Delivered {days} days ago — outside the 7-day return window.", "days_since_delivery": days}
    if product is not None and not product.returnable:
        return {"eligible": False, "reason": "This product is marked non-returnable.", "days_since_delivery": days}
    return {"eligible": True, "reason": "Delivered within 7 days and product is returnable.", "days_since_delivery": days}
def check_replacement(order, product, now=None):

    if order.status != "delivered":
        return False, "Order abhi delivered nahi hai"
    if _days_since(order.delivered_at, now) > REPLACEMENT_DAYS:
        return False, f"Replacement window ({REPLACEMENT_DAYS} din) khatam ho gaya"
    return True, "Replacement eligible hai"

def check_refund(amount):

    if amount is None:
        return {"auto": False, "reason": "Amount unknown."}
    if amount <= AUTO_REFUND_LIMIT:
        return {"auto": True, "reason": f"Amount Rs.{amount} is within the Rs.{AUTO_REFUND_LIMIT} auto-refund limit."}
    return {"auto": False, "reason": f"Amount Rs.{amount} exceeds the Rs.{AUTO_REFUND_LIMIT} auto-refund limit; human approval required."}
