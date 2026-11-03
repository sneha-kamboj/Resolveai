import random
from datetime import datetime, timedelta
from app.db.base import Base, engine, SessionLocal
from app.db.models import Customer, Product, Order

random.seed(42)
FIRST = ["Aarav", "Priya", "Rohan", "Ananya", "Karan", "Neha", "Vikram", "Kavya", "Arjun", "Ishita",
         "Rahul", "Pooja", "Aditya", "Simran", "Nikhil", "Divya", "Manish", "Ritu", "Sahil", "Meera"]
LAST = ["Sharma", "Verma", "Gupta", "Singh", "Yadav", "Malik", "Chauhan", "Kamboj",
        "Rana", "Thakur", "Mishra", "Pandey", "Kaur", "Gill", "Saini", "Negi"]
DOMAINS = ["gmail.com"] * 7 + ["yahoo.in", "outlook.com", "hotmail.com"]
PRODUCTS = [("Running Shoes", "Footwear", 2999, True), ("Cotton T-Shirt", "Fashion", 799, True),
            ("Wireless Earbuds", "Electronics", 1999, True), ("Steel Bottle", "Home", 499, True),
            ("Backpack", "Fashion", 1499, True), ("Face Cream", "Beauty", 349, False),
            ("Phone Case", "Electronics", 599, True), ("Wrist Watch", "Fashion", 2499, True),
            ("Yoga Mat", "Fitness", 899, True), ("Vitamin Supplements", "Health", 649, False)]
VARIANTS = ["Black", "Navy", "Maroon", "Olive"]

def seed():
    Base.metadata.create_all(engine)
    db = SessionLocal()
    if db.query(Customer).count() > 0:
        print("Already seeded, skip")
        return
    customers, used = [], set()
    for i in range(100):
        f, l = random.choice(FIRST), random.choice(LAST)
        email = f"{f.lower()}.{l.lower()}{random.randint(1, 99)}@{random.choice(DOMAINS)}"
        while email in used:
            email = f"{f.lower()}.{l.lower()}{random.randint(100, 999)}@{random.choice(DOMAINS)}"
        used.add(email)
        customers.append(Customer(name=f"{f} {l}", email=email,
                                  phone=f"{random.choice('6789')}{random.randint(100000000, 999999999)}"))
    db.add_all(customers)
    products = [Product(name=f"{n} ({v})", category=c, price=p, returnable=r)
                for (n, c, p, r) in PRODUCTS for v in VARIANTS]
    db.add_all(products)
    db.commit()
    now = datetime.now()
    def order(cust, prod, status, ordered, delivered, amount=None):
        return Order(customer_id=cust.id, product_id=prod.id, status=status,
                     amount=prod.price if amount is None else amount,
                     ordered_at=ordered, delivered_at=delivered)
    orders = []
    for _ in range(495):
        cust, prod = random.choice(customers), random.choice(products)
        status = random.choices(["delivered", "shipped", "placed", "cancelled"], weights=[65, 15, 10, 10])[0]
        ordered = now - timedelta(days=random.randint(0, 90), hours=random.randint(0, 23))
        delivered = min(ordered + timedelta(days=random.randint(1, 7)), now) if status == "delivered" else None
        qty = random.choices([1, 2, 3], weights=[7, 2, 1])[0]
        orders.append(order(cust, prod, status, ordered, delivered, amount=prod.price * qty))
    ret = next(p for p in products if p.returnable)
    nonret = next(p for p in products if not p.returnable)
    orders.append(
        order(
            customers[0],
            ret,
            "delivered",
            now - timedelta(days=10),
            now - timedelta(days=7)))
    orders.append(order(customers[0], ret, "delivered", now - timedelta(days=11), now - timedelta(days=8)))
    orders.append(order(customers[0], ret, "delivered", now - timedelta(days=5), now - timedelta(days=2), amount=5000))  # refund cap PASS
    orders.append(order(customers[0], ret, "delivered", now - timedelta(days=5), now - timedelta(days=2), amount=5001))  # refund cap FAIL
    orders.append(order(customers[0], nonret, "delivered", now - timedelta(days=4), now - timedelta(days=1)))  # non-returnable FAIL
    db.add_all(orders)
    db.commit()
    print("SEEDED", db.query(Customer).count(), db.query(Product).count(), db.query(Order).count())
    db.close()

if __name__ == "__main__":
    seed()
