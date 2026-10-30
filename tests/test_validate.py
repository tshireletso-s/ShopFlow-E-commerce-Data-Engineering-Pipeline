import pytest
from shopflow.validation.common import validate_records




def test_valid_records_are_accepted():
    records = [
        {
            "customer_id": "1",
            "full_name": "Tshire",
            "email": "tshire@gmail.com"
        },
        {
            "customer_id": "2",
            "full_name": "Sipho",
            "email": "sipho@yahoo.com"
        }
    ]

    result = validate_records(
        records,
        required_fields=["customer_id", "full_name", "email"],
        id_field="customer_id"
    )

    assert len(result["valid_records"]) == 2
    assert result["errors"] == []


def test_missing_required_field_is_rejected():
    records = [
        {
            "customer_id": "1",
            "full_name": "Tshire",
            "email": ""
        }
    ]

    result = validate_records(
        records,
        required_fields=["customer_id", "full_name", "email"],
        id_field="customer_id"
    )

    assert result["valid_records"] == []
    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "email"


def test_duplicate_ids_are_rejected():
    records = [
        {
            "customer_id": "1",
            "full_name": "Tshire",
            "email": "tshire@gmail.com"
        },
        {
            "customer_id": "1",
            "full_name": "Sipho",
            "email": "sipho@yahoo.com"
        }
    ]

    result = validate_records(
        records,
        required_fields=["customer_id", "full_name", "email"],
        id_field="customer_id"
    )

    assert len(result["valid_records"]) == 1
    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "customer_id"


def test_missing_id_is_rejected():
    records = [
        {
            "customer_id": "",
            "full_name": "Tshire",
            "email": "tshire@gmail.com"
        }
    ]

    result = validate_records(
        records,
        required_fields=["customer_id", "full_name", "email"],
        id_field="customer_id"
    )

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "customer_id"


def test_multiple_invalid_records_are_rejected():
    records = [
        {
            "customer_id": "1",
            "full_name": "",
            "email": "tshire@gmail.com"
        },
        {
            "customer_id": "2",
            "full_name": "Sipho",
            "email": ""
        },
        {
            "customer_id": "3",
            "full_name": "Lerato",
            "email": "lerato@yahoo.com"
        }
    ]

    result = validate_records(
        records,
        required_fields=["customer_id", "full_name", "email"],
        id_field="customer_id"
    )

    assert len(result["valid_records"]) == 1
    assert len(result["errors"]) == 2

def test_missing_id_is_rejected_even_if_not_in_required_fields():
    records = [
        {"name": "Tshireletso"}
    ]

    result = validate_records(
        records,
        required_fields=["name"],
        id_field="customer_id"
    )

    assert result["valid_records"] == []
    assert result["errors"][0]["field"] == "customer_id"

def test_invalid_first_record_does_not_reserve_id():
    records = [
        {"customer_id": 1, "name": ""},
        {"customer_id": 1, "name": "Tshireletso"}
    ]

    result = validate_records(
        records,
        required_fields=["name"],
        id_field="customer_id"
    )

    assert result["valid_records"] == [
        {"customer_id": 1, "name": "Tshireletso"}
    ]
    assert len(result["errors"]) == 1
    assert result["errors"][0]["reason"] == "Required field is missing or empty"



def test_first_valid_record_wins_when_ids_are_duplicated():
    records = [
        {"customer_id": 1, "name": "Tshireletso"},
        {"customer_id": 1, "name": "Sipho"}
    ]

    result = validate_records(
        records,
        required_fields=["name"],
        id_field="customer_id"
    )

    assert result["valid_records"] == [
        {"customer_id": 1, "name": "Tshireletso"}
    ]
    assert len(result["errors"]) == 1
    assert result["errors"][0]["reason"] == "Duplicate ID"