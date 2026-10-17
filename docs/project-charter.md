# Problem Statement

E-commerce businesses generate data from multiple sources, including customer records, product catalogues, orders, and order items. When this data is stored in separate files, it can contain missing values, duplicate records, invalid prices or quantities, inconsistent order statuses, and broken relationships between datasets.

Poor data quality can lead to inaccurate revenue calculations, unreliable product performance reports, and misleading customer insights. Manually identifying and correcting these problems is time-consuming and makes it difficult to process data consistently as new records arrive.

ShopFlow addresses this problem by developing an automated data engineering pipeline that extracts, validates, transforms, and loads e-commerce data into a relational database. The pipeline will identify invalid records, detect duplicates and broken relationships, record rejection reasons, and generate data-quality reports and SQL-based business insights.

The project will demonstrate how structured data processing, database integrity, automated testing, and repeatable pipeline execution can improve the reliability and usability of e-commerce data.

# Project Objectives

The primary objective is to build a reliable, testable, and documented data pipeline that converts raw e-commerce data into validated, structured, and analysis-ready information.

The specific objectives are to:

1. Extract data: Read customer, product, order, and order-item records from CSV files using Python.

2. Validate data quality: Identify missing required fields, invalid values, negative prices or quantities, and unsupported order statuses.

3. Maintain data integrity: Detect duplicate identifiers and invalid relationships between customers, orders, products, and order items.

4. Transform and load data: Process valid records and load them into a relational SQLite database with appropriate primary keys, foreign keys, and constraints.

5. Handle rejected records: Record invalid records and their rejection reasons so that data-quality problems can be investigated.

6. Ensure repeatability: Make pipeline execution idempotent, meaning that rerunning the same input does not create unintended duplicate records or inconsistent results.

7. Generate business insights: Use SQL queries to calculate revenue, identify popular products, and identify repeat customers, according to documented business rules.

8. Monitor data quality: Produce a scorecard showing records processed, accepted and rejected, including rejection counts by reason and a documented data-quality percentage.

9. Verify correctness: Develop automated unit and integration tests covering normal processing, invalid records, database loading, and repeated executions.

10. Document the solution: Provide clear setup instructions, architecture documentation, a data dictionary, testing evidence, and a demonstration of the completed pipeline.