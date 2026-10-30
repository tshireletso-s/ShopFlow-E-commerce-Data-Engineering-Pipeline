def create_tables(connection):
    cursor = connection.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            unit_price NUMERIC NOT NULL CHECK (unit_price > 0),
            stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,

            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        );

        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            unit_price NUMERIC NOT NULL CHECK (unit_price > 0),

            FOREIGN KEY (order_id)
                REFERENCES orders(order_id),

            FOREIGN KEY (product_id)
                REFERENCES products(product_id)
        );
    """)

    connection.commit()

def insert_customers(connection, customers):
    cursor = connection.cursor()

    cursor.executemany("""
        INSERT INTO customers (
            customer_id,
            full_name,
            email,
            created_at
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(customer_id) DO NOTHING
    """, [
        (
            customer["customer_id"],
            customer["full_name"],
            customer["email"],
            customer["created_at"]
        )
        for customer in customers
    ])

    connection.commit()


def insert_products(connection, products):
    cursor = connection.cursor()

    cursor.executemany("""
        INSERT INTO products (
            product_id,
            product_name,
            unit_price,
            stock_quantity
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(product_id) DO NOTHING
    """, [
        (
            product["product_id"],
            product["product_name"],
            str(product["unit_price"]),
            product["stock_quantity"]
        )
        for product in products
    ])

    connection.commit()


def insert_orders(connection, orders):
    cursor = connection.cursor()

    cursor.executemany("""
        INSERT INTO orders (
            order_id,
            customer_id,
            order_date,
            status
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT(order_id) DO NOTHING
    """, [
        (
            order["order_id"],
            order["customer_id"],
            order["order_date"],
            order["status"]
        )
        for order in orders
    ])

    connection.commit()

def insert_order_items(connection, order_items):
    cursor = connection.cursor()

    cursor.executemany("""
        INSERT INTO order_items (
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(order_item_id) DO NOTHING
    """, [
        (
            item["order_item_id"],
            item["order_id"],
            item["product_id"],
            item["quantity"],
            str(item["unit_price"])
        )
        for item in order_items
    ])

    connection.commit()