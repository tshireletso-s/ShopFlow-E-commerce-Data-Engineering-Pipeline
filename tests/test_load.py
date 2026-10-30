import sqlite3

from shopflow.load import create_tables, insert_customers, insert_products, insert_orders, insert_order_items


def test_create_tables_creates_required_tables(tmp_path):
    database_path = tmp_path / "test_shopflow.db"

    connection = sqlite3.connect(database_path)

    create_tables(connection)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tables = {row[0] for row in cursor.fetchall()}

    assert {
        "customers",
        "products",
        "orders",
        "order_items"
    }.issubset(tables)

    connection.close()


def test_insert_customers_stores_records(tmp_path):
    database_path = tmp_path / "test_shopflow.db"
    connection = sqlite3.connect(database_path)

    create_tables(connection)

    customers = [
        {
            "customer_id": 1,
            "full_name": "Tshireletso Seodigeng",
            "email": "tshireseodigeng@gmail.com",
            "created_at": "2026-10-12 14:00:00"
        },
        {
            "customer_id": 2,
            "full_name": "Sipho Dlamini",
            "email": "siphodlamini@gmail.com",
            "created_at": "2026-09-03 11:30:00"
        }
    ]

    insert_customers(connection, customers)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM customers")

    stored_customers = cursor.fetchall()

    assert len(stored_customers) == 2
    assert stored_customers[0][1] == "Tshireletso Seodigeng"
    assert stored_customers[1][1] == "Sipho Dlamini"

    connection.close()    


def test_insert_products_stores_records(tmp_path):
    database_path = tmp_path / "test_shopflow.db"
    connection = sqlite3.connect(database_path)

    create_tables(connection)

    products = [
        {
            "product_id": 1,
            "product_name": "rich aunt blonde unit",
            "unit_price": "5400",
            "stock_quantity": "13"
        },
        {
            "product_id": 2,
            "product_name": "deep burgundy unit",
            "unit_price": "4300",
            "stock_quantity": "21"
        }
    ]

    insert_products(connection, products)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")

    stored_products = cursor.fetchall()

    assert len(stored_products) == 2
    assert stored_products[0][1] == "rich aunt blonde unit"
    assert stored_products[1][1] == "deep burgundy unit"

    connection.close()    


def test_insert_orders_stores_records(tmp_path):
    database_path = tmp_path / "test_shopflow.db"
    connection = sqlite3.connect(database_path)

    create_tables(connection)

    customers = [
        {
            "customer_id": 1,
            "full_name": "Tshireletso Seodigeng",
            "email": "tshireseodigeng@gmail.com",
            "created_at": "2026-10-12 14:00:00"
        }
    ]

    orders = [
        {
            "order_id": 1001,
            "customer_id": 1,
            "order_date": "2026-10-18",
            "status": "completed"
        }
    ]

    insert_customers(connection, customers)
    insert_orders(connection, orders)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders")

    stored_orders = cursor.fetchall()

    assert len(stored_orders) == 1
    assert stored_orders[0][0] == 1001
    assert stored_orders[0][1] == 1
    assert stored_orders[0][3] == "completed"

    connection.close()   


def test_insert_order_items_stores_records(tmp_path):
    database_path = tmp_path / "test_shopflow.db"
    connection = sqlite3.connect(database_path)

    create_tables(connection)

    customers = [
        {
            "customer_id": 1,
            "full_name": "Tshireletso Seodigeng",
            "email": "tshireseodigeng@gmail.com",
            "created_at": "2026-10-12 14:00:00"
        }
    ]

    products = [
        {
            "product_id": 1,
            "product_name": "rich aunt blonde unit",
            "unit_price": "5400",
            "stock_quantity": "13"
        }
    ]

    orders = [
        {
            "order_id": 1001,
            "customer_id": 1,
            "order_date": "2026-10-18",
            "status": "completed"
        }
    ]

    order_items = [
        {
            "order_item_id": 1,
            "order_id": 1001,
            "product_id": 1,
            "quantity": "2",
            "unit_price": "5400"
        }
    ]

    insert_customers(connection, customers)
    insert_products(connection, products)
    insert_orders(connection, orders)
    insert_order_items(connection, order_items)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM order_items")

    stored_items = cursor.fetchall()

    assert len(stored_items) == 1
    assert stored_items[0][0] == 1
    assert stored_items[0][1] == 1001
    assert stored_items[0][2] == 1
    assert stored_items[0][3] == 2

    connection.close()     