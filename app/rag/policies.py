POLICIES = [
    {
        "id": "return_policy",
        "title": "Return Policy",
        "text": "Customers can return any delivered item within 7 days of delivery. The item must be unused and returned with its original tags and packaging. Once the return is approved, free pickup will be arranged. Returns are not accepted after 7 days. Cases involving damaged or incorrect items are handled separately.",
    },
    {
        "id": "refund_timeline",
        "title": "Refund Timeline",
        "text": "Once a refund is approved, the money is returned within 5-7 business days. Until then, the refund status may appear as pending because banks need time to process the transaction. If the money is not received even after 7 business days, the customer should contact support with their order ID.",
    },
    {
        "id": "refund_method",
        "title": "Refund Method",
        "text": "Refunds are always issued to the original payment method. If the customer paid through UPI, the refund goes to the same UPI account. If the customer paid by card, the refund goes to the same card. For Cash on Delivery (COD) orders, the refund is transferred to the customer's bank account or UPI. Refunds of up to Rs. 5,000 are automatically approved. Refunds above Rs. 5,000 require prior approval from the support team and may take additional time.",
    },
    {
        "id": "replacement_policy",
        "title": "Replacement Policy",
        "text": "Customers can request a replacement within 15 days of delivery if the item is damaged, defective, or incorrect. The same product will be sent as a replacement. If the same product is out of stock, the customer will receive a full refund. Replacements are not available after 15 days.",
    },
    {
        "id": "damaged_item",
        "title": "Damaged Item",
        "text": "If an item arrives broken, damaged, or defective, the customer must report the issue within 15 days of delivery and provide a photograph of the item. Free pickup will be arranged for damaged items. The customer can choose between a replacement and a refund. This policy does not apply to damage caused by the customer.",
    },
    {
        "id": "wrong_item",
        "title": "Wrong Item Delivered",
        "text": "If a customer receives an item different from what they ordered, the incorrect item will be picked up free of charge. The correct item will be sent to the customer. If the correct item is unavailable, the customer will receive a full refund. The standard 7-day return window does not apply to incorrect deliveries. Reporting the issue within 15 days is sufficient.",
    },
    {
        "id": "shipping_delivery",
        "title": "Shipping and Delivery",
        "text": "Orders are generally delivered within 3-5 business days after dispatch. Deliveries to remote areas may take up to 7 days. Once the order is shipped, a tracking link is sent through SMS and email. Customers can use this link to check their delivery status. If the parcel does not arrive by the promised date, the support team will investigate the issue using the order ID.",
    },
    {
        "id": "order_cancellation",
        "title": "Order Cancellation",
        "text": "Orders can be cancelled free of charge before dispatch, and the full payment will be refunded within 5-7 business days. Orders cannot be cancelled after dispatch. In such cases, customers can use the return policy after delivery. Only items that have not yet been dispatched can be cancelled.",
    },
    {
        "id": "non_returnable_items",
        "title": "Non-Returnable Items",
        "text": "Certain items cannot be returned due to hygiene and safety reasons. These include opened cosmetics, personal care products, and innerwear. However, if such an item is delivered damaged or incorrectly, the non-returnable restriction does not apply, and the customer can request a replacement or refund. Final sale items are also non-returnable, except in cases involving damage.",
    },
    {
        "id": "warranty",
        "title": "Warranty",
        "text": "Electronics such as earbuds and smartwatches come with a 6-month warranty from the date of purchase. The warranty covers manufacturing defects, such as a product suddenly stopping working or failing to charge. Physical damage caused by the customer or water damage is not covered. Once a claim is submitted, the product will be inspected, after which repair, replacement, or refund will be decided.",
    },
    {
        "id": "emi_refund",
        "title": "EMI Refund",
        "text": "For orders paid through EMI, the refund is first transferred to the bank. The bank may take 7-10 business days to adjust the EMI amount, which is longer than the standard refund processing time. Interest and bank charges applied to EMI transactions are governed by the bank's policies. Customers will receive a refund reference number that they can use to check the status with their bank.",
    },
    {
        "id": "size_exchange",
        "title": "Size Exchange",
        "text": "If a customer receives clothing or shoes in the wrong size, they can request a size exchange within 15 days of delivery. The exchange will be for a different size of the same product. The item must be unused and returned with its original tags. If the required size is unavailable, the customer can return the item and receive a refund. Free pickup is available for size exchanges.",
    },
]

if __name__ == "__main__":
    print("POLICIES", len(POLICIES))
    for p in POLICIES:
        print("-", p["id"])
