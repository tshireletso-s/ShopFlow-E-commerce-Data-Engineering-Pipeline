from datetime import datetime
from shopflow.validation.data_relationships import validate_relationships


def test_order_with_existing_customer_is_accepted():
    customers = [
        {
            "customer_id": "1",
            "created_at": "2026-09-01 10:00:00"
        }
    ]

    products = []
    orders = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "2026-10-01",
            "status": "completed"
        }
    ]
    order_items = []

    result = validate_relationships(
        customers, products, orders, order_items
    )

    assert result["valid_orders"] == orders
    assert result["errors"] == []


def test_order_with_nonexistent_customer_is_rejected():
    customers = []
    products = []
    orders = [
        {
            "order_id": "1001",
            "customer_id": "999",
            "order_date": "2026-10-01",
            "status": "completed"
        }
    ]
    order_items = []

    result = validate_relationships(
        customers, products, orders, order_items
    )

    assert result["valid_orders"] == []
    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "customer_id"


def test_order_before_customer_creation_date_is_rejected():
    customers = [
        {
            "customer_id": "1",
            "created_at": "2026-10-05 10:00:00"
        }
    ]

    products = []
    orders = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "2026-10-01",
            "status": "completed"
        }
    ]
    order_items = []

    result = validate_relationships(
        customers, products, orders, order_items
    )

    assert result["valid_orders"] == []
    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "order_date"


def test_order_item_with_existing_order_and_product_is_accepted():
    customers = [
    {
        "customer_id": "1",
        "created_at": "2026-09-01 10:00:00"
        }
    ]

    products = [{"product_id": "1"}]

    orders = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "2026-10-01",
            "status": "completed"
        }
    ]

    order_items = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "2",
            "unit_price": "5400"
        }
    ]

    result = validate_relationships(
        customers, products, orders, order_items
    )

    assert result["valid_order_items"] == order_items
    assert result["errors"] == []


def test_order_item_with_nonexistent_product_is_rejected():
    customers = [
    {
        "customer_id": "1",
        "created_at": "2026-09-01 10:00:00"
    }
    ]

    products = []

    orders = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "2026-10-01",
            "status": "completed"
        }
    ]

    order_items = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "999",
            "quantity": "2",
            "unit_price": "5400"
        }
    ]

    result = validate_relationships(
        customers, products, orders, order_items
    )

    assert result["valid_order_items"] == []
    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "product_id"


def test_order_item_with_rejected_parent_order_is_rejected():
    customers = []
    products = [{"product_id": "1"}]

    # This order will not be accepted.
    orders = []

    order_items = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "2",
            "unit_price": "5400"
        }
    ]

    result = validate_relationships(
        customers, products, orders, order_items
    )

    assert result["valid_order_items"] == []
    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "order_id"
