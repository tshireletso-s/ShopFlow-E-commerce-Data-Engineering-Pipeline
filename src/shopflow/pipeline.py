import sqlite3
from pathlib import Path

from shopflow.extract import data_extraction
from shopflow.validation.customers import validate_customer_records
from shopflow.validation.products import validate_product_records
from shopflow.validation.orders import validate_order_records
from shopflow.validation.order_items import validate_order_item_records
from shopflow.validation.data_relationships import validate_relationships
from shopflow.reporting import save_validation_errors
from shopflow.load import (
    create_tables,
    insert_customers,
    insert_products,
    insert_orders,
    insert_order_items
)
from shopflow.transform import (
    transform_customers,
    transform_products,
    transform_orders,
    transform_order_items
)


def run_pipeline(data_directory, database_path):
    data_directory = Path(data_directory)

    # Extract records from CSV files
    customers = data_extraction(data_directory / "customers.csv")
    products = data_extraction(data_directory / "products.csv")
    orders = data_extraction(data_directory / "orders.csv")
    order_items = data_extraction(data_directory / "order_items.csv")

    # Stop if a file is missing or empty
    datasets = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items
    }

    for name, records in datasets.items():
        if records == "This csv file is empty":
            datasets[name] = []
        elif isinstance(records, str):
            raise ValueError(f"{name}: {records}")

    customers = datasets["customers"]
    products = datasets["products"]
    orders = datasets["orders"]
    order_items = datasets["order_items"]    

    # Validate individual datasets
    customer_result = validate_customer_records(customers)
    product_result = validate_product_records(products)
    order_result = validate_order_records(orders)
    order_item_result = validate_order_item_records(order_items)

    # Extract valid records
    valid_customers = customer_result["valid_records"]
    valid_products = product_result["valid_records"]
    valid_orders = order_result["valid_records"]
    valid_order_items = order_item_result["valid_records"]

    # Validate relationships
    relationship_result = validate_relationships(
        valid_customers,
        valid_products,
        valid_orders,
        valid_order_items
    )

    valid_orders = relationship_result["valid_orders"]
    valid_order_items = relationship_result["valid_order_items"]


    valid_customers = transform_customers(valid_customers)
    valid_products = transform_products(valid_products)
    valid_orders = transform_orders(valid_orders)
    valid_order_items = transform_order_items(valid_order_items)

    # Combine validation errors
    errors = (
        customer_result["errors"]
        + product_result["errors"]
        + order_result["errors"]
        + order_item_result["errors"]
        + relationship_result["errors"]
    )

    # Load accepted records
    connection = sqlite3.connect(database_path)

    try:
        create_tables(connection)

        insert_customers(connection, valid_customers)
        insert_products(connection, valid_products)
        insert_orders(connection, valid_orders)
        insert_order_items(connection, valid_order_items)

    finally:
        connection.close()
        
    # Save validation errors
    save_validation_errors(
        errors,
        data_directory.parent / "reports" / "validation_errors.csv"
    )

    return {
        "loaded": {
            "customers": len(valid_customers),
            "products": len(valid_products),
            "orders": len(valid_orders),
            "order_items": len(valid_order_items)
        },
        "rejected": {
            "customers": len(customers) - len(valid_customers),
            "products": len(products) - len(valid_products),
            "orders": len(orders) - len(valid_orders),
            "order_items": len(order_items) - len(valid_order_items)
        },
        "errors": errors
    }