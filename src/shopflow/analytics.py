def get_total_revenue(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT SUM(quantity * unit_price)
        FROM order_items
    """)

    return cursor.fetchone()[0]


def get_best_selling_products(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.product_name,
            SUM(oi.quantity) AS total_sold
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_sold DESC
    """)

    return cursor.fetchall()


def get_revenue_by_product(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            p.product_name,
            SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
    """)

    return cursor.fetchall()


def get_repeat_customers(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.customer_id,
            c.full_name,
            COUNT(o.order_id) AS order_count
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.full_name
        HAVING COUNT(o.order_id) > 1
        ORDER BY order_count DESC
    """)

    return cursor.fetchall()


def get_orders_by_status(connection):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM orders
        GROUP BY status
        ORDER BY status
    """)

    return cursor.fetchall()

def get_data_quality_scorecard(pipeline_result):
    scorecard = {}

    for dataset in pipeline_result["loaded"]:
        loaded = pipeline_result["loaded"][dataset]
        rejected = pipeline_result["rejected"][dataset]
        total = loaded + rejected

        scorecard[dataset] = {
            "total_records": total,
            "valid_records": loaded,
            "rejected_records": rejected,
            "quality_score": (
                round((loaded / total) * 100, 2)
                if total > 0 else 0
            )
        }

    return scorecard