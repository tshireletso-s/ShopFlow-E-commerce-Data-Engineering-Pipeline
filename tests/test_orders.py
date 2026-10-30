
from shopflow.validation.orders import validate_order_records


def test_valid_order_is_accepted():
    records = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "2026-10-01",
            "status": "completed"
        }
    ]

    result = validate_order_records(records)

    assert result["valid_records"] == records
    assert result["errors"] == []


def test_missing_customer_id_is_rejected():
    records = [
        {
            "order_id": "1001",
            "customer_id": "",
            "order_date": "2026-10-01",
            "status": "completed"
        }
    ]

    result = validate_order_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "customer_id" for error in result["errors"])


def test_missing_order_date_is_rejected():
    records = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "",
            "status": "completed"
        }
    ]

    result = validate_order_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "order_date" for error in result["errors"])


def test_invalid_order_date_is_rejected():
    records = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "01-10-2026",
            "status": "completed"
        }
    ]

    result = validate_order_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "order_date" for error in result["errors"])


def test_invalid_calendar_date_is_rejected():
    records = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "2026-02-30",
            "status": "completed"
        }
    ]

    result = validate_order_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "order_date" for error in result["errors"])


def test_invalid_order_status_is_rejected():
    records = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "2026-10-01",
            "status": "shipped"
        }
    ]

    result = validate_order_records(records)

    assert result["valid_records"] == []
    assert any(error["field"] == "status" for error in result["errors"])


def test_all_allowed_statuses_are_accepted():
    statuses = ["completed", "processing", "pending", "cancelled"]

    records = [
        {
            "order_id": str(index + 1001),
            "customer_id": "1",
            "order_date": "2026-10-01",
            "status": status
        }
        for index, status in enumerate(statuses)
    ]

    result = validate_order_records(records)

    assert result["valid_records"] == records
    assert result["errors"] == []


def test_duplicate_order_id_is_rejected():
    records = [
        {
            "order_id": "1001",
            "customer_id": "1",
            "order_date": "2026-10-01",
            "status": "completed"
        },
        {
            "order_id": "1001",
            "customer_id": "2",
            "order_date": "2026-10-02",
            "status": "pending"
        }
    ]

    result = validate_order_records(records)

    assert len(result["valid_records"]) == 1
    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "order_id"
