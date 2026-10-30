
from datetime import datetime

from shopflow.validation.common import validate_records


ALLOWED_STATUSES = {
    "completed",
    "processing",
    "pending",
    "cancelled"
}


def validate_order_records(records):
    order_errors = []
    candidate_records = []

    for record in records:
        record_errors = []

        # Validate order_date
        order_date = record.get("order_date")

        if order_date is not None and str(order_date).strip() != "":
            try:
                datetime.strptime(str(order_date), "%Y-%m-%d")
            except ValueError:
                record_errors.append({
                    "record": record,
                    "field": "order_date",
                    "reason": "Invalid date format"
                })

        # Validate status
        status = record.get("status")

        if status is not None and str(status).strip() != "":
            if status not in ALLOWED_STATUSES:
                record_errors.append({
                    "record": record,
                    "field": "status",
                    "reason": "Invalid order status"
                })

        if record_errors:
            order_errors.extend(record_errors)
        else:
            candidate_records.append(record)

    # Apply generic validation to order records
    common_result = validate_records(
        candidate_records,
        required_fields=["customer_id", "order_date", "status"],
        id_field="order_id"
    )

    return {
        "valid_records": common_result["valid_records"],
        "errors": order_errors + common_result["errors"]
    }
