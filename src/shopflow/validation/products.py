from decimal import Decimal, InvalidOperation

from shopflow.validation.common import validate_records


def validate_product_records(records):
    product_errors = []
    candidate_records = []

    for record in records:
        record_errors = []

        # Validate unit_price
        unit_price = record.get("unit_price")

        if unit_price is not None and str(unit_price).strip() != "":
            try:
                price = Decimal(str(unit_price))

                if not price.is_finite():
                    record_errors.append({
                        "record": record,
                        "field": "unit_price",
                        "reason": "Invalid numeric value"
                    })
                elif price <= 0:
                    record_errors.append({
                        "record": record,
                        "field": "unit_price",
                        "reason": "Must be greater than zero"
                    })

            except InvalidOperation:
                record_errors.append({
                    "record": record,
                    "field": "unit_price",
                    "reason": "Invalid numeric value"
                })

        # Validate stock_quantity
        stock_quantity = record.get("stock_quantity")

        if stock_quantity is not None and str(stock_quantity).strip() != "":
            try:
                quantity = int(stock_quantity)

                if quantity < 0:
                    record_errors.append({
                        "record": record,
                        "field": "stock_quantity",
                        "reason": "Must be a non-negative integer"
                    })

            except (ValueError, TypeError):
                record_errors.append({
                    "record": record,
                    "field": "stock_quantity",
                    "reason": "Must be a non-negative integer"
                })

        if record_errors:
            product_errors.extend(record_errors)
        else:
            candidate_records.append(record)

    # Apply generic validation to product records
    common_result = validate_records(
        candidate_records,
        required_fields=["product_name", "unit_price", "stock_quantity"],
        id_field="product_id"
    )

    return {
        "valid_records": common_result["valid_records"],
        "errors": product_errors + common_result["errors"]
    }