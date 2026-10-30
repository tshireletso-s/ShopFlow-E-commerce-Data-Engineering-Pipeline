
from shopflow.validation.customers import validate_customer_records


def test_valid_customer_records_are_accepted():
    records = [
        {
            "customer_id": "1",
            "full_name": "Tshireletso Seodigeng",
            "email": "tshireseodigeng@gmail.com",
            "created_at": "2026-10-12 14:00:00"
        }
    ]

    result = validate_customer_records(records)

    assert result["valid_records"] == records
    assert result["errors"] == []


def test_missing_full_name_is_rejected():
    records = [
        {
            "customer_id": "1",
            "full_name": "",
            "email": "tshireseodigeng@gmail.com",
            "created_at": "2026-10-12 14:00:00"
        }
    ]

    result = validate_customer_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "full_name"


def test_invalid_email_is_rejected():
    records = [
        {
            "customer_id": "1",
            "full_name": "Tshireletso Seodigeng",
            "email": "not-an-email",
            "created_at": "2026-10-12 14:00:00"
        }
    ]

    result = validate_customer_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "email"


def test_invalid_created_at_is_rejected():
    records = [
        {
            "customer_id": "1",
            "full_name": "Tshireletso Seodigeng",
            "email": "tshireseodigeng@gmail.com",
            "created_at": "12 October 2026"
        }
    ]

    result = validate_customer_records(records)

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "created_at"


def test_duplicate_customer_ids_are_rejected():
    records = [
        {
            "customer_id": "1",
            "full_name": "Tshireletso Seodigeng",
            "email": "tshireseodigeng@gmail.com",
            "created_at": "2026-10-12 14:00:00"
        },
        {
            "customer_id": "1",
            "full_name": "Sipho Dlamini",
            "email": "sipho@example.com",
            "created_at": "2026-09-03 11:30:00"
        }
    ]

    result = validate_customer_records(records)

    assert len(result["valid_records"]) == 1
    assert len(result["errors"]) == 1
    assert result["errors"][0]["reason"] == "Duplicate ID"
