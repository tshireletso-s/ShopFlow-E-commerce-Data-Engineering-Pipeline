from datetime import datetime

def validate_relationships(customers, products, orders, order_items):

    errors = []
    valid_orders = []
    valid_order_items = []

    customer_lookup = {
    customer["customer_id"]: customer
    for customer in customers
}

    for order in orders:
        customer_id = order["customer_id"]
        customer = customer_lookup.get(customer_id)

        if customer is None:
            errors.append({
                "record": order,
                "field": "customer_id",
                "reason": "Customer does not exist"
            })
            continue

        order_date = datetime.strptime(
            order["order_date"], "%Y-%m-%d"
        )

        created_at = datetime.strptime(
            customer["created_at"], "%Y-%m-%d %H:%M:%S"
        )

        if order_date.date() < created_at.date():
            errors.append({
                "record": order,
                "field": "order_date",
                "reason": "Order date is before customer creation date"
            })
            continue

        valid_orders.append(order)

    product_ids = {product["product_id"] for product in products}
    valid_order_ids = {order["order_id"] for order in valid_orders}

    for item in order_items:
        order_id = item["order_id"]
        product_id = item["product_id"]

        if order_id not in valid_order_ids:
            errors.append({
                "record": item,
                "field": "order_id",
                "reason": "Order does not exist or was rejected"
            })
            continue

        if product_id not in product_ids:
            errors.append({
                "record": item,
                "field": "product_id",
                "reason": "Product does not exist"
            })
            continue

        valid_order_items.append(item)

    return {
        "valid_orders": valid_orders,
        "valid_order_items": valid_order_items,
        "errors": errors
    }