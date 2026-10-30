import sqlite3

from shopflow.pipeline import run_pipeline


def test_pipeline_creates_database_tables(tmp_path):
    data_directory = tmp_path / "raw"
    data_directory.mkdir()

    database_path = tmp_path / "shopflow.db"

    # Create the four CSV files
    (data_directory / "customers.csv").write_text(
        "customer_id,full_name,email,created_at\n",
        encoding="utf-8"
    )
    (data_directory / "products.csv").write_text(
        "product_id,product_name,unit_price,stock_quantity\n",
        encoding="utf-8"
    )
    (data_directory / "orders.csv").write_text(
        "order_id,customer_id,order_date,status\n",
        encoding="utf-8"
    )
    (data_directory / "order_items.csv").write_text(
        "order_item_id,order_id,product_id,quantity,unit_price\n",
        encoding="utf-8"
    )

    result = run_pipeline(data_directory, database_path)

    connection = sqlite3.connect(database_path)
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

    assert isinstance(result, dict)

    connection.close()

def test_pipeline_loads_valid_records(tmp_path):
    data_directory = tmp_path / "raw"
    data_directory.mkdir()

    database_path = tmp_path / "shopflow.db"

    (data_directory / "customers.csv").write_text(
        "customer_id,full_name,email,created_at\n"
        "1,Tshireletso,test@example.com,2026-09-01 10:00:00\n",
        encoding="utf-8"
    )

    (data_directory / "products.csv").write_text(
        "product_id,product_name,unit_price,stock_quantity\n"
        "1,Blonde Unit,5400,13\n",
        encoding="utf-8"
    )

    (data_directory / "orders.csv").write_text(
        "order_id,customer_id,order_date,status\n"
        "1001,1,2026-09-10,completed\n",
        encoding="utf-8"
    )

    (data_directory / "order_items.csv").write_text(
        "order_item_id,order_id,product_id,quantity,unit_price\n"
        "1,1001,1,2,5400\n",
        encoding="utf-8"
    )

    result = run_pipeline(data_directory, database_path)

    assert result["loaded"] == {
        "customers": 1,
        "products": 1,
        "orders": 1,
        "order_items": 1
    }

    assert result["rejected"] == {
        "customers": 0,
        "products": 0,
        "orders": 0,
        "order_items": 0
    }

    assert result["errors"] == []

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    for table in ("customers", "products", "orders", "order_items"):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        assert cursor.fetchone()[0] == 1

    connection.close()

def test_pipeline_loads_valid_records_and_rejects_invalid_records(tmp_path):
    data_directory = tmp_path / "raw"
    data_directory.mkdir()
    database_path = tmp_path / "shopflow.db"

    (data_directory / "customers.csv").write_text(
        "customer_id,full_name,email,created_at\n"
        "1,Tshireletso,test@example.com,2026-09-01 10:00:00\n"
        "2,Invalid Customer,invalid-email,2026-09-02 10:00:00\n",
        encoding="utf-8"
    )

    (data_directory / "products.csv").write_text(
        "product_id,product_name,unit_price,stock_quantity\n"
        "1,Blonde Unit,5400,13\n",
        encoding="utf-8"
    )

    (data_directory / "orders.csv").write_text(
        "order_id,customer_id,order_date,status\n"
        "1001,1,2026-09-10,completed\n",
        encoding="utf-8"
    )

    (data_directory / "order_items.csv").write_text(
        "order_item_id,order_id,product_id,quantity,unit_price\n"
        "1,1001,1,2,5400\n",
        encoding="utf-8"
    )

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
        "orders": 0,
        "order_items": 0
    }

    assert len(result["errors"]) == 1
    assert result["errors"][0]["field"] == "email"        

def test_pipeline_rejects_invalid_relationships(tmp_path):
    data_directory = tmp_path / "raw"
    data_directory.mkdir()
    database_path = tmp_path / "shopflow.db"

    (data_directory / "customers.csv").write_text(
        "customer_id,full_name,email,created_at\n"
        "1,Valid Customer,test@example.com,2026-09-01 10:00:00\n",
        encoding="utf-8"
    )

    (data_directory / "products.csv").write_text(
        "product_id,product_name,unit_price,stock_quantity\n"
        "1,Blonde Unit,5400,13\n",
        encoding="utf-8"
    )

    (data_directory / "orders.csv").write_text(
        "order_id,customer_id,order_date,status\n"
        "1001,999,2026-09-10,completed\n",
        encoding="utf-8"
    )

    (data_directory / "order_items.csv").write_text(
        "order_item_id,order_id,product_id,quantity,unit_price\n"
        "1,1001,1,2,5400\n",
        encoding="utf-8"
    )

    result = run_pipeline(data_directory, database_path)

    assert result["loaded"] == {
        "customers": 1,
        "products": 1,
        "orders": 0,
        "order_items": 0
    }

    assert result["rejected"] == {
        "customers": 0,
        "products": 0,
        "orders": 1,
        "order_items": 1
    }

    assert len(result["errors"]) == 2    


def test_pipeline_can_run_twice_without_duplicate_records(tmp_path):
    data_directory = tmp_path / "raw"
    data_directory.mkdir()
    database_path = tmp_path / "shopflow.db"

    (data_directory / "customers.csv").write_text(
        "customer_id,full_name,email,created_at\n"
        "1,Test Customer,test@example.com,2026-09-01 10:00:00\n",
        encoding="utf-8"
    )

    (data_directory / "products.csv").write_text(
        "product_id,product_name,unit_price,stock_quantity\n"
        "1,Blonde Unit,5400,13\n",
        encoding="utf-8"
    )

    (data_directory / "orders.csv").write_text(
        "order_id,customer_id,order_date,status\n"
        "1001,1,2026-09-10,completed\n",
        encoding="utf-8"
    )

    (data_directory / "order_items.csv").write_text(
        "order_item_id,order_id,product_id,quantity,unit_price\n"
        "1,1001,1,2,5400\n",
        encoding="utf-8"
    )

    run_pipeline(data_directory, database_path)
    run_pipeline(data_directory, database_path)

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    for table in ("customers", "products", "orders", "order_items"):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        assert cursor.fetchone()[0] == 1

    connection.close()   