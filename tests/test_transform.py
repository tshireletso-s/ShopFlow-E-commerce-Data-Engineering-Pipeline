from decimal import Decimal

from shopflow.transform import (
    transform_customers,
    transform_products,
    transform_orders,
    transform_order_items
)


def test_transform_customers():
    records = [{"customer_id": "1", "full_name": "Test"}]

    result = transform_customers(records)

    assert result[0]["customer_id"] == 1
    assert isinstance(result[0]["customer_id"], int)


def test_transform_products():
    records = [{
        "product_id": "1",
        "unit_price": "5400",
        "stock_quantity": "13"
    }]

    result = transform_products(records)

    assert result[0]["product_id"] == 1
    assert result[0]["unit_price"] == Decimal("5400")
    assert result[0]["stock_quantity"] == 13


def test_transform_orders():
    records = [{"order_id": "1001", "customer_id": "1"}]

    result = transform_orders(records)

    assert result[0]["order_id"] == 1001
    assert result[0]["customer_id"] == 1


def test_transform_order_items():
    records = [{
        "order_item_id": "1",
        "order_id": "1001",
        "product_id": "1",
        "quantity": "2",
        "unit_price": "5400"
    }]

    result = transform_order_items(records)

    assert result[0]["order_item_id"] == 1
    assert result[0]["order_id"] == 1001
    assert result[0]["product_id"] == 1
    assert result[0]["quantity"] == 2
    assert result[0]["unit_price"] == Decimal("5400")