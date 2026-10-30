def validate_records(records, required_fields, id_field):
    valid_records = []
    errors = []
    seen_ids = set()

    for record in records:
        record_errors = []

        # Check required fields
        for field in required_fields:
            value = record.get(field)

            if value is None or str(value).strip() == "":
                record_errors.append({
                    "record": record,
                    "field": field,
                    "reason": "Required field is missing or empty"
                })

        # Check whether ID is missing
        record_id = record.get(id_field)

        if record_id is None or str(record_id).strip() == "":
            record_errors.append({
                "record": record,
                "field": id_field,
                "reason": "Required field is missing or empty"
            })

        # Only check duplicates if required fields and ID are valid
        if not record_errors:
            if record_id in seen_ids:
                record_errors.append({
                    "record": record,
                    "field": id_field,
                    "reason": "Duplicate ID"
                })
            else:
                seen_ids.add(record_id)

        if record_errors:
            errors.extend(record_errors)
        else:
            valid_records.append(record)

    return {
        "valid_records": valid_records,
        "errors": errors
    }