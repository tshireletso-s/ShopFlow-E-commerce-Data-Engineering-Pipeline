
from decimal import Decimal, InvalidOperation

from shopflow.validation.common import validate_records


def validate_order_item_records(records):
    order_item_errors = []
    candidate_records = []

    for record in records:
        record_errors = []

        # Validate quantity
        quantity = record.get("quantity")

        if quantity is not None and str(quantity).strip() != "":
            try:
                parsed_quantity = int(quantity)

                if parsed_quantity <= 0:
                    record_errors.append({
                        "record": record,
                        "field": "quantity",
                        "reason": "Must be a positive integer"
                    })

            except (ValueError, TypeError):
                record_errors.append({
                    "record": record,
                    "field": "quantity",
                    "reason": "Must be a positive integer"
                })

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

        if record_errors:
            order_item_errors.extend(record_errors)
        else:
            candidate_records.append(record)

    # Apply generic validation to order item records
    common_result = validate_records(
        candidate_records,
        required_fields=[
            "order_id",
            "product_id",
            "quantity",
            "unit_price"
        ],
        id_field="order_item_id"
    )

    return {
        "valid_records": common_result["valid_records"],
        "errors": order_item_errors + common_result["errors"]
    }
