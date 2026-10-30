from decimal import Decimal


def transform_customers(customers):
    return [
        {
            **customer,
            "customer_id": int(customer["customer_id"])
        }
        for customer in customers
    ]


def transform_products(products):
    return [
        {
            **product,
            "product_id": int(product["product_id"]),
            "unit_price": Decimal(product["unit_price"]),
            "stock_quantity": int(product["stock_quantity"])
        }
        for product in products
    ]


def transform_orders(orders):
    return [
        {
            **order,
            "order_id": int(order["order_id"]),
            "customer_id": int(order["customer_id"])
        }
        for order in orders
    ]


def transform_order_items(order_items):
    return [
        {
            **item,
            "order_item_id": int(item["order_item_id"]),
            "order_id": int(item["order_id"]),
            "product_id": int(item["product_id"]),
            "quantity": int(item["quantity"]),
            "unit_price": Decimal(item["unit_price"])
        }
        for item in order_items
    ]