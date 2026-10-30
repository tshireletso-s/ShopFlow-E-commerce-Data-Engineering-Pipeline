import csv

from shopflow.reporting import save_validation_errors


def test_save_validation_errors(tmp_path):
    output_path = tmp_path / "reports" / "errors.csv"

    errors = [
        {
            "record": {"customer_id": "1"},
            "field": "email",
            "reason": "Invalid email format"
        }
    ]

    save_validation_errors(errors, output_path)

    with open(output_path, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["field"] == "email"
    assert rows[0]["reason"] == "Invalid email format"
    assert "customer_id" in rows[0]["record"]