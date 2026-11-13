import random, csv, os

random.seed(42)

PRODUCTS = ["shoes", "t-shirt", "earbuds", "watch", "backpack", "bottle"]

TEMPLATES = {
    "order_status": [
        "Where is my order?",
        "Tell me the status of order #{oid}",
        "When will my {p} arrive?",
        "My {p} order has not arrived yet",
        "What is the delivery date for order #{oid}?",
        "Track my order please",
        "Has order #{oid} been delivered or not?",
        "Where is my parcel stuck?",
        "How much time will shipping take?",
        "When will I receive my {p} order?"
    ],

    "return": [
        "I want to return my {p}",
        "I want to return this {p} because the size is incorrect",
        "How can I return order #{oid}?",
        "I didn't like the {p}, I want to return it",
        "I want to send this item back",
        "When will the return pickup arrive?",
        "I received the wrong {p}, I want to return it",
        "I don't want this product, please take it back",
        "I want to place a return request for order #{oid}",
        "The colour of my {p} is different, I want to return it"
    ],

    "refund": [
        "When will I receive my refund?",
        "When will I get my money back for order #{oid}?",
        "What is the status of my refund?",
        "I returned the item but haven't received my refund",
        "Please return my money",
        "How many days will the refund take?",
        "I want a refund for my {p}",
        "My refund has been pending for many days",
        "When will the money be credited to my account?",
        "Has the refund been initiated for order #{oid}?"
    ],

    "replacement": [
        "My {p} is defective, please replace it",
        "The item is damaged, I need a replacement",
        "My {p} is broken, please send another one",
        "I received the wrong size, I want an exchange",
        "The product is defective, please replace it",
        "The colour of this item has faded, send another one",
        "My {p} is not working, I need a replacement",
        "I received the wrong item, please send the correct one",
        "Can I exchange my {p}?",
        "I received a damaged item in order #{oid}"
    ],

    "policy_question": [
        "What is your return policy?",
        "How many days does a refund take?",
        "Can I return an item after 10 days?",
        "Which items are non-returnable?",
        "Tell me about your replacement policy",
        "Can I return an item without a bill?",
        "What does your return policy say?",
        "How does a refund work for EMI orders?",
        "Can sale items be returned?",
        "What is the warranty period for {p}?"
    ],
}


def build_rows():
    rows = []

    for intent, temps in TEMPLATES.items():
        for t in temps:
            for p in random.sample(PRODUCTS, 5):
                rows.append(
                    (t.format(p=p, oid=random.randint(100, 500)), intent)
                )

    random.shuffle(rows)
    return rows


if __name__ == "__main__":
    rows = build_rows()

    os.makedirs("data", exist_ok=True)

    with open("data/triage_data.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "intent"])
        w.writerows(rows)

    print("ROWS", len(rows))