import argparse
import sqlite3

from shopflow.pipeline import run_pipeline
from shopflow.analytics import get_data_quality_scorecard


def main():
    parser = argparse.ArgumentParser(
        description="Run the ShopFlow e-commerce data pipeline."
    )

    parser.add_argument(
        "--data",
        default="data/raw",
        help="Directory containing the raw CSV files."
    )

    parser.add_argument(
        "--database",
        default="data/shopflow.db",
        help="Path where the SQLite database will be stored."
    )

    args = parser.parse_args()

    try:
        result = run_pipeline(args.data, args.database)
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.exit(1, f"ShopFlow failed: {error}\n")

    print("\nShopFlow pipeline completed successfully.")

    # Display loaded and rejected records
    print("\nProcessing summary:")

    for dataset in result["loaded"]:
        loaded = result["loaded"][dataset]
        rejected = result["rejected"][dataset]

        print(
            f"{dataset}: "
            f"{loaded} valid, {rejected} rejected"
        )

    # Display data quality scores
    scorecard = get_data_quality_scorecard(result)

    print("\nData quality scorecard:")

    for dataset, metrics in scorecard.items():
        print(
            f"{dataset}: "
            f"{metrics['quality_score']}% "
            f"({metrics['valid_records']}/"
            f"{metrics['total_records']} valid)"
        )

    print(f"\nValidation errors: {len(result['errors'])}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())