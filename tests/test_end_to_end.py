import csv
import sqlite3

from shopflow.pipeline import run_pipeline


def create_csv(file_path, fieldnames, records):
    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def create_test_data(data_directory):
    data_directory.mkdir(parents=True)

    # One valid customer and one customer with an invalid email
    create_csv(
        data_directory / "customers.csv",
        ["customer_id", "full_name", "email", "created_at"],
        [
            {
                "customer_id": "1",
                "full_name": "Customer One",
                "email": "one@example.com",
                "created_at": "2026-09-01 10:00:00"
            },
            {
                "customer_id": "2",
                "full_name": "Customer Two",
                "email": "invalid-email",
                "created_at": "2026-09-02 10:00:00"
            }
        ]
    )

    create_csv(
        data_directory / "products.csv",
        ["product_id", "product_name", "unit_price", "stock_quantity"],
        [
            {
                "product_id": "1",
                "product_name": "Blonde Unit",
                "unit_price": "5400",
                "stock_quantity": "10"
            }
        ]
    )

    # One valid order, one referencing an invalid customer,
    # and one dated before the customer's creation date
    create_csv(
        data_directory / "orders.csv",
        ["order_id", "customer_id", "order_date", "status"],
        [
            {
                "order_id": "1001",
                "customer_id": "1",
                "order_date": "2026-09-10",
                "status": "completed"
            },
            {
                "order_id": "1002",
                "customer_id": "2",
                "order_date": "2026-09-11",
                "status": "completed"
            },
            {
                "order_id": "1003",
                "customer_id": "1",
                "order_date": "2026-08-20",
                "status": "pending"
            }
        ]
    )

    # One valid item, one referencing a rejected order,
    # one referencing a missing product, and one invalid quantity
    create_csv(
        data_directory / "order_items.csv",
        ["order_item_id", "order_id", "product_id", "quantity", "unit_price"],
        [
            {
                "order_item_id": "1",
                "order_id": "1001",
                "product_id": "1",
                "quantity": "2",
                "unit_price": "5400"
            },
            {
                "order_item_id": "2",
                "order_id": "1002",
                "product_id": "1",
                "quantity": "1",
                "unit_price": "5400"
            },
            {
                "order_item_id": "3",
                "order_id": "1001",
                "product_id": "999",
                "quantity": "1",
                "unit_price": "5400"
            },
            {
                "order_item_id": "4",
                "order_id": "1001",
                "product_id": "1",
                "quantity": "0",
                "unit_price": "5400"
            }
        ]
    )


def get_table_counts(database_path):
    connection = sqlite3.connect(database_path)

    try:
        tables = ["customers", "products", "orders", "order_items"]

        return {
            table: connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            for table in tables
        }
    finally:
        connection.close()


def test_complete_pipeline_end_to_end(tmp_path):
    data_directory = tmp_path / "raw"
    database_path = tmp_path / "shopflow.db"

    create_test_data(data_directory)

    # First pipeline run
    result = run_pipeline(data_directory, database_path)

    assert result["loaded"] == {
        "customers": 1,
        "products": 1,
        "orders": 1,
        "order_items": 1
    }

    assert result["rejected"] == {
        "customers": 1,
        "products": 0,
        "orders": 2,
        "order_items": 3
    }

    assert len(result["errors"]) == 6

    expected_counts = {
        "customers": 1,
        "products": 1,
        "orders": 1,
        "order_items": 1
    }

    assert get_table_counts(database_path) == expected_counts

    # Confirm the validation error report was created
    report_path = tmp_path / "reports" / "validation_errors.csv"
    assert report_path.exists()

    # Second pipeline run: records must not be duplicated
    second_result = run_pipeline(data_directory, database_path)

    assert second_result["loaded"] == result["loaded"]
    assert second_result["rejected"] == result["rejected"]

    assert get_table_counts(database_path) == expected_counts