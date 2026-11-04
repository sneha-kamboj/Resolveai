from datetime import datetime

RETURN_WINDOW_DAYS = 7
REPLACEMENT_DAYS = 15
AUTO_REFUND_LIMIT = 5000


VALID_REPLACEMENT_REASONS = ("damaged", "defective", "wrong",
                             "toota", "toot", "phata", "kharab", "galat")

def _days_since(delivered_date, today=None):
    if delivered_date is None:
        return None
    today = today or datetime.now()
    return (today - delivered_date).days

def check_return(order, product, today=None):

    days = _days_since(order.delivered_at, today)

    if order.status != "delivered":
        return False, f"Order status is '{order.status}', not 'delivered'. Returns apply only to delivered orders."

    if days is None:
        return False, "Order has no delivery date."

    if days > RETURN_WINDOW_DAYS:
        return False, f"Delivered {days} days ago — outside the 7-day return window."

    if product is not None and not product.returnable:
        return False, "This product is marked non-returnable."

    return True, "Delivered within 7 days and product is returnable."
def check_replacement(order, product, now=None):

    if order.status != "delivered":
        return False, "Order abhi delivered nahi hai"
    if _days_since(order.delivered_at, now) > REPLACEMENT_DAYS:
        return False, f"Replacement window ({REPLACEMENT_DAYS} din) khatam ho gaya"
    return True, "Replacement eligible hai"


def check_auto_refund(order):
    if order.amount is None:
        return False, "Amount unknown."
    if order.amount <= AUTO_REFUND_LIMIT:
        return True, f"Amount Rs.{order.amount} is within the Rs.{AUTO_REFUND_LIMIT} auto-refund limit."

    return False, f"Amount Rs.{order.amount} exceeds the Rs.{AUTO_REFUND_LIMIT} auto-refund limit; human approval required."

