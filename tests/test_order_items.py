
from shopflow.validation.order_items import validate_order_item_records


def test_valid_order_item_is_accepted():
    records = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "2",
            "unit_price": "5400"
        }
    ]

    result = validate_order_item_records(records)

    assert result["valid_records"] == records
    assert result["errors"] == []


def test_missing_order_id_is_rejected():
    records = [
        {
            "order_item_id": "1",
            "order_id": "",
            "product_id": "1",
            "quantity": "2",
            "unit_price": "5400"
        }
    ]

    result = validate_order_item_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "order_id" for error in result["errors"])


def test_missing_product_id_is_rejected():
    records = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "",
            "quantity": "2",
            "unit_price": "5400"
        }
    ]

    result = validate_order_item_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "product_id" for error in result["errors"])


def test_zero_quantity_is_rejected():
    records = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "0",
            "unit_price": "5400"
        }
    ]

    result = validate_order_item_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "quantity" for error in result["errors"])


def test_negative_quantity_is_rejected():
    records = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "-2",
            "unit_price": "5400"
        }
    ]

    result = validate_order_item_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "quantity" for error in result["errors"])


def test_decimal_quantity_is_rejected():
    records = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "2.5",
            "unit_price": "5400"
        }
    ]

    result = validate_order_item_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "quantity" for error in result["errors"])


def test_non_numeric_unit_price_is_rejected():
    records = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "2",
            "unit_price": "expensive"
        }
    ]

    result = validate_order_item_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "unit_price" for error in result["errors"])


def test_zero_unit_price_is_rejected():
    records = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "2",
            "unit_price": "0"
        }
    ]

    result = validate_order_item_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "unit_price" for error in result["errors"])


def test_duplicate_order_item_id_is_rejected():
    records = [
        {
            "order_item_id": "1",
            "order_id": "1001",
            "product_id": "1",
            "quantity": "2",
            "unit_price": "5400"
        },
        {
            "order_item_id": "1",
            "order_id": "1002",
            "product_id": "2",
            "quantity": "1",
            "unit_price": "4300"
        }
    ]

    result = validate_order_item_records(records)

    assert len(result["valid_records"]) == 1
    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "order_item_id"
