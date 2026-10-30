import csv
from pathlib import Path


def save_validation_errors(errors, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["record", "field", "reason"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for error in errors:
            writer.writerow({
                "record": str(error["record"]),
                "field": error["field"],
                "reason": error["reason"]
            })