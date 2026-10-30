# ShopFlow — E-commerce Data Engineering Pipeline

## Overview

ShopFlow is a Python-based e-commerce data engineering project that extracts, validates, transforms, and loads customer, product, order, and order-item data from CSV files into a relational SQLite database.

The pipeline applies data-quality checks, detects duplicate records, validates relationships between datasets, rejects invalid records, and generates a persistent validation error report.

It also provides SQL analytics and a data-quality scorecard to demonstrate how processed data can be used for reporting and business insights.

## Key Features

- **CSV Extraction:** Reads customer, product, order, and order-item datasets.
- **Data Validation:** Checks required fields, data formats, numeric values, and business rules.
- **Duplicate Detection:** Identifies duplicate record IDs.
- **Relationship Validation:** Checks foreign-key relationships between customers, orders, products, and order items.
- **Data Transformation:** Converts raw CSV string values into appropriate Python data types.
- **Database Loading:** Stores validated records in a relational SQLite database.
- **Idempotent Loading:** Prevents duplicate database records when the pipeline is rerun.
- **Error Reporting:** Exports rejected records and validation reasons to a CSV report.
- **SQL Analytics:** Provides revenue, best-selling product, repeat-customer, and order-status queries.
- **Data Quality Scorecard:** Calculates the percentage of valid records for each dataset.
- **Command-Line Interface:** Allows users to execute the pipeline from a terminal.

## Technologies Used

- Python 3
- SQLite
- SQL
- CSV
- pytest
- Git

## Project Structure

```text
ShopFlow-E-commerce-Data-Engineering-Pipeline/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   └── order_items.csv
│   └── reports/
│       └── validation_errors.csv
│
├── src/
│   └── shopflow/
│       ├── __main__.py
│       ├── extract.py
│       ├── transform.py
│       ├── load.py
│       ├── pipeline.py
│       ├── analytics.py
│       ├── reporting.py
│       └── validation/
│           ├── __init__.py
│           ├── common.py
│           ├── customers.py
│           ├── products.py
│           ├── orders.py
│           ├── order_items.py
│           └── data_relationships.py
│
├── tests/
│   ├── test_extract.py
│   ├── test_validate.py
│   ├── test_customers.py
│   ├── test_products.py
│   ├── test_orders.py
│   ├── test_order_items.py
│   ├── test_data_relationships.py
│   ├── test_load.py
│   ├── test_pipeline.py
│   ├── test_transform.py
│   ├── test_reporting.py
│   ├── test_analytics.py
│   ├── test_cli.py
│   └── test_end_to_end.py
│
└── README.md
```

## Getting Started

### Prerequisites

Before running ShopFlow, install:

- Python 3.10 or later
- Git

Check that Python and Git are installed:

```bash
python --version
git --version
```

On some Linux systems, use `python3 --version` instead.

### 1. Clone the Repository

Open a terminal and clone the project:

```bash
git clone https://github.com/tshirecodes/ShopFlow-E-commerce-Data-Engineering-Pipeline.git
```

Navigate into the project directory:

```bash
cd ShopFlow-E-commerce-Data-Engineering-Pipeline
```

### 2. Create a Virtual Environment

A virtual environment keeps project dependencies isolated from other Python projects.

**Windows — PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

**Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If the `venv` module is unavailable on Ubuntu or Debian, install it with:

```bash
sudo apt install python3-venv
```

### 3. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install pytest for running the test suite:

```bash
python -m pip install pytest
```

The pipeline itself uses Python's standard library, so no additional runtime packages are required.

### 4. Run the Tests

Set the Python source directory so Python can locate the ShopFlow package.

**Windows — PowerShell:**

```powershell
$env:PYTHONPATH = "src"
python -m pytest -v
```

**Linux:**

```bash
export PYTHONPATH=src
python -m pytest -v
```

The test suite checks extraction, validation, transformation, loading, analytics, reporting, CLI execution, and end-to-end pipeline behaviour.

### 5. Run the Pipeline

Execute ShopFlow from the project root.

**Windows — PowerShell:**

```powershell
$env:PYTHONPATH = "src"
python -m shopflow --data data/raw --database data/shopflow.db
```

**Linux:**

```bash
export PYTHONPATH=src
python -m shopflow --data data/raw --database data/shopflow.db
```

The pipeline accepts two command-line arguments:

| Argument | Description | Default |
|---|---|---|
| `--data` | Directory containing the raw CSV files | `data/raw` |
| `--database` | Location of the SQLite database | `data/shopflow.db` |

Both arguments are optional because default values are provided.

For example, to use a different input directory or database location:

```bash
python -m shopflow --data path/to/csv_files --database path/to/database.db
```

### 6. View the Results

After execution, ShopFlow displays:

- The number of valid and rejected records per dataset.
- The data-quality percentage for each dataset.
- The total number of validation errors.

The pipeline also creates:

- `data/shopflow.db` — the SQLite database containing validated records.
- `data/reports/validation_errors.csv` — a report containing rejected records, affected fields, and validation reasons.

The database and report are generated when the pipeline runs.

## Data Quality and Validation

ShopFlow validates incoming records before loading them into the database.

Examples of validation checks include:

- Missing or empty required fields.
- Invalid email and date formats.
- Invalid product prices and stock quantities.
- Invalid order statuses.
- Duplicate record identifiers.
- Orders referencing customers that do not exist.
- Order items referencing missing orders or products.
- Orders dated before the customer's creation date.

Invalid records are rejected while valid records continue through the pipeline.

## SQL Analytics

The project includes SQL queries for:

- Total revenue.
- Best-selling products.
- Revenue by product.
- Repeat customers.
- Orders grouped by status.

These queries demonstrate how validated relational data can support business reporting and analysis.

## Idempotency

ShopFlow uses conflict handling during database insertion to prevent duplicate records when the pipeline is executed repeatedly with the same data.

This allows the pipeline to be rerun without inserting the same primary-key records multiple times.

## Future Improvements

Potential extensions include:

- Scheduling automated pipeline executions.
- Integrating cloud storage.
- Implementing a data orchestration tool such as Apache Airflow.
- Adding larger datasets and more advanced analytics.
- Introducing structured logging and monitoring.

## Author

**Tshire**

GitHub: [@tshirecodes](https://github.com/tshirecodes)