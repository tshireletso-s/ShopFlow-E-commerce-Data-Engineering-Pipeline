
from shopflow.validation.products import validate_product_records


def test_valid_product_records_are_accepted():
    records = [
        {
            "product_id": "1",
            "product_name": "Rich Aunt Blonde Unit",
            "unit_price": "5400",
            "stock_quantity": "13"
        }
    ]

    result = validate_product_records(records)

    assert result["valid_records"] == records
    assert result["errors"] == []


def test_missing_product_name_is_rejected():
    records = [
        {
            "product_id": "1",
            "product_name": "",
            "unit_price": "5400",
            "stock_quantity": "13"
        }
    ]

    result = validate_product_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "product_name"


def test_invalid_unit_price_is_rejected():
    records = [
        {
            "product_id": "1",
            "product_name": "Rich Aunt Blonde Unit",
            "unit_price": "not-a-price",
            "stock_quantity": "13"
        }
    ]

    result = validate_product_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "unit_price"


def test_zero_unit_price_is_rejected():
    records = [
        {
            "product_id": "1",
            "product_name": "Rich Aunt Blonde Unit",
            "unit_price": "0",
            "stock_quantity": "13"
        }
    ]

    result = validate_product_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "unit_price"


def test_negative_unit_price_is_rejected():
    records = [
        {
            "product_id": "1",
            "product_name": "Rich Aunt Blonde Unit",
            "unit_price": "-5400",
            "stock_quantity": "13"
        }
    ]

    result = validate_product_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "unit_price"


def test_negative_stock_quantity_is_rejected():
    records = [
        {
            "product_id": "1",
            "product_name": "Rich Aunt Blonde Unit",
            "unit_price": "5400",
            "stock_quantity": "-1"
        }
    ]

    result = validate_product_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "stock_quantity"


def test_zero_stock_quantity_is_accepted():
    records = [
        {
            "product_id": "1",
            "product_name": "Rich Aunt Blonde Unit",
            "unit_price": "5400",
            "stock_quantity": "0"
        }
    ]

    result = validate_product_records(records)

    assert result["valid_records"] == records
    assert result["errors"] == []


def test_non_integer_stock_quantity_is_rejected():
    records = [
        {
            "product_id": "1",
            "product_name": "Rich Aunt Blonde Unit",
            "unit_price": "5400",
            "stock_quantity": "2.5"
        }
    ]

    result = validate_product_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "stock_quantity"


def test_duplicate_product_ids_are_rejected():
    records = [
        {
            "product_id": "1",
            "product_name": "Rich Aunt Blonde Unit",
            "unit_price": "5400",
            "stock_quantity": "13"
        },
        {
            "product_id": "1",
            "product_name": "Deep Burgundy Unit",
            "unit_price": "4300",
            "stock_quantity": "21"
        }
    ]

    result = validate_product_records(records)

    assert len(result["valid_records"]) == 1
    assert len(result["errors"]) == 1
    assert result["errors"][0]["reason"] == "Duplicate ID"
