import sqlite3

from shopflow.load import create_tables
from shopflow.analytics import (
    get_total_revenue,
    get_best_selling_products,
    get_revenue_by_product,
    get_repeat_customers,
    get_orders_by_status
)


def setup_database():
    connection = sqlite3.connect(":memory:")
    create_tables(connection)

    connection.execute("""
        INSERT INTO customers VALUES
        (1, 'Customer One', 'one@example.com', '2026-09-01 10:00:00'),
        (2, 'Customer Two', 'two@example.com', '2026-09-02 10:00:00')
    """)

    connection.execute("""
        INSERT INTO products VALUES
        (1, 'Blonde Unit', 5400, 13),
        (2, 'Burgundy Unit', 4300, 21)
    """)

    connection.execute("""
        INSERT INTO orders VALUES
        (1001, 1, '2026-09-10', 'completed'),
        (1002, 1, '2026-09-11', 'completed'),
        (1003, 2, '2026-09-12', 'pending')
    """)

    connection.execute("""
        INSERT INTO order_items VALUES
        (1, 1001, 1, 2, 5400),
        (2, 1002, 2, 1, 4300),
        (3, 1003, 1, 1, 5400)
    """)

    connection.commit()
    return connection


def test_get_total_revenue():
    connection = setup_database()

    assert get_total_revenue(connection) == 20500

    connection.close()


def test_get_best_selling_products():
    connection = setup_database()

    assert get_best_selling_products(connection) == [
        ("Blonde Unit", 3),
        ("Burgundy Unit", 1)
    ]

    connection.close()


def test_get_revenue_by_product():
    connection = setup_database()

    assert get_revenue_by_product(connection) == [
        ("Blonde Unit", 16200),
        ("Burgundy Unit", 4300)
    ]

    connection.close()


def test_get_repeat_customers():
    connection = setup_database()

    assert get_repeat_customers(connection) == [
        (1, "Customer One", 2)
    ]

    connection.close()


def test_get_orders_by_status():
    connection = setup_database()

    assert get_orders_by_status(connection) == [
        ("completed", 2),
        ("pending", 1)
    ]

    connection.close()


def test_get_data_quality_scorecard():
    from shopflow.analytics import get_data_quality_scorecard

    pipeline_result = {
        "loaded": {
            "customers": 9,
            "products": 10
        },
        "rejected": {
            "customers": 1,
            "products": 0
        }
    }

    result = get_data_quality_scorecard(pipeline_result)

    assert result["customers"] == {
        "total_records": 10,
        "valid_records": 9,
        "rejected_records": 1,
        "quality_score": 90.0
    }

    assert result["products"] == {
        "total_records": 10,
        "valid_records": 10,
        "rejected_records": 0,
        "quality_score": 100.0
    }    