from itertools import product

from unicodedata import category
import datetime
from app.db.models import Customer
import random

random.seed(42)
FIRST = ["Aarav", "Priya", "Rohan", "Ananya", "Karan", "Neha", "Vikram", "Kavya", "Arjun", "Ishita"]
LAST = ["Sharma", "Vermaa", "Gupta", "Singh", "Yadav", "Malik", "Chauhan", "Kamboj"]
DOMAINS = ["gmail.com"] * 7 + ["yahoo.in", "outlook.com", "hotmail.com"]
PRODUCTS = [("Running Shoes", "Footwear", 2999, True), ("Cotton T-Shirt", "Fashion", 799, True),
            ("Wireless Earbuds", "Electronics", 1999, True), ("Steel Bottle", "Home", 499, True),
            ("Backpack", "Fashion", 1499, True), ("Face Cream", "Beauty", 349, False),
            ("Phone Case", "Electronics", 599, True), ("Wrist Watch", "Fashion", 2499, True),
            ("Yoga Mat", "Fitness", 899, True), ("Vitamin Supplements", "Health", 649, False)]
VARIANTS = ["Black", "Navy", "Maroon", "Olive"]


def generate_customers(n):
	customer = []
	used =set()
	for i in range(100):
		f = random.choice(FIRST)
		l = random.choice(LAST)
		email = f"{f.lower()}{l.lower()}{random.randint(1,999)}@{random.choice(DOMAINS)}"

		if email in used:
			email = f"{f.lower()}{l.lower()}{random.randint(1, 999)}@{random.choice(DOMAINS)}"
		used.add(email)




def generate_products():
    products = []


	for product in PRODUCTS:
		name, category,price, delivered = product
		for var in VARIANTS:

		    pdt = product(
				name=name,
				category = category,
				price=price,
				delivered = delivered,
				variant=var
			)

		products.append(pdt)
	return products


def generate_orders(customers,products,n):
	orders = []
	for i in range(n):
	customer = random.choice(customers)
	product = random.choice(products)
	status = random.choice(STATUSES)

    now = datetime.datetime.now()
    days_ago = random.randint(0,90)
    order_date = now - datetime.timedelta(days=days_ago)
    delivery_date = None
    qnt = random.randint(1,3)

	amount = product.price*qnt

	order = Order(
            customer=customer,
            product=product,
            status=status,
            order_date=order_date,
            delivery_date=delivery_date,
            quantity=quantity,
            amount=amount

	)
	    order.append(order)
    return orders