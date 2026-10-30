
import re
from datetime import datetime

from shopflow.validation.common import validate_records


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_customer_records(records):
    customer_errors = []
    candidate_records = []

    for record in records:
        record_errors = []

        # Validate email format
        email = record.get("email")

        if email is not None and str(email).strip() != "":
            if not EMAIL_PATTERN.fullmatch(str(email)):
                record_errors.append({
                    "record": record,
                    "field": "email",
                    "reason": "Invalid email format"
                })

        # Validate created_at format
        created_at = record.get("created_at")

        if created_at is not None and str(created_at).strip() != "":
            try:
                datetime.strptime(
                    str(created_at),
                    "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                record_errors.append({
                    "record": record,
                    "field": "created_at",
                    "reason": "Invalid datetime format"
                })

        if record_errors:
            customer_errors.extend(record_errors)
        else:
            candidate_records.append(record)

    # Apply generic validation to customer records
    common_result = validate_records(
        candidate_records,
        required_fields=["full_name", "email", "created_at"],
        id_field="customer_id"
    )

    return {
        "valid_records": common_result["valid_records"],
        "errors": customer_errors + common_result["errors"]
    }
