# SellerStream — Cloud Data Engineering Pipeline

SellerStream is an end-to-end data engineering project that ingests raw e-commerce order data, validates and transforms it, stores curated datasets in Amazon S3, and enables SQL-based analytics using Amazon Athena.

The project demonstrates cloud ETL workflows, data quality validation, data cataloging, and business analytics using AWS services and Python.

## Project Status

**Implemented:** AWS S3 data storage, AWS Glue ETL, Glue Data Catalog, curated Parquet output, Amazon Athena SQL analytics, and local Python data processing and validation.

**Dataset:** 10 sample e-commerce orders in the AWS analytics dataset.

## Architecture

```text
Raw E-commerce Orders (CSV)
           |
           v
Amazon S3 — Raw Data Lake
           |
           v
AWS Glue Crawler
           |
           v
AWS Glue Data Catalog
           |
           v
AWS Glue ETL Job (PySpark)
           |
           v
Amazon S3 — Curated Parquet Data
           |
           v
AWS Glue Crawler
           |
           v
Curated Table in AWS Glue Data Catalog
           |
           v
Amazon Athena — SQL Analytics
           |
           v
Business KPIs and Data Quality Checks
```

## Technology Stack

* **Python & Pandas:** Local data ingestion, transformation, and validation.
* **Amazon S3:** Storage for raw CSV data, curated Parquet data, and Athena query results.
* **AWS Glue:** Managed ETL processing, crawlers, and Data Catalog.
* **PySpark:** Distributed data transformation within the Glue ETL job.
* **Amazon Athena:** Serverless SQL analytics on curated data.
* **SQL:** Revenue analysis, monthly trends, seller performance, order status, and data-quality checks.
* **PostgreSQL:** Relational data modeling and additional analytical SQL practice.

## ETL Workflow

1. **Ingestion:** Load raw e-commerce order data from CSV files.
2. **Validation:** Check missing values, duplicate order IDs, invalid numeric values, order statuses, and amount consistency.
3. **Transformation:** Standardize order statuses and create business-oriented fields such as gross amount and discount percentage.
4. **Curation:** Generate curated order data and derived fields, including net revenue, order month, completed-order flag, and cancelled-order flag.
5. **Cloud ETL:** Use an AWS Glue ETL job to transform raw CSV data and write curated data in Parquet format to Amazon S3.
6. **Cataloging:** Use AWS Glue crawlers to discover the schema and update the Glue Data Catalog.
7. **Analytics:** Run SQL queries in Amazon Athena to calculate business KPIs and validate curated records.

## Data Quality Checks

The pipeline includes checks for:

* Missing values
* Duplicate order IDs
* Invalid quantities and prices
* Negative discounts or order amounts
* Order amount consistency
* Invalid order statuses
* Unique order counts and invalid records in Athena

## Business Analytics

Athena queries are used to analyze:

* Total orders, revenue, and average order value
* Monthly revenue trends
* Seller-level order and revenue performance
* Order status distribution
* Curated dataset quality

## Current AWS Sample Results

| Metric              | Verified result |
| ------------------- | --------------: |
| Total orders        |              10 |
| Total revenue       |      ₹65,186.00 |
| Average order value |       ₹6,518.60 |
| Unique order IDs    |              10 |
| Invalid rows        |               0 |

*Results are based on the current 10-order AWS sample dataset.*

## Local Setup

### Prerequisites

* Python 3.12+
* Git
* AWS account for the cloud pipeline
* AWS CLI (optional, for command-line AWS access)

### Run the Local Python Pipeline

1. Clone the repository:

   ```bash
   git clone https://github.com/Ayeshafirdous5/SellerStream.git
   cd SellerStream
   ```

2. Create and activate a virtual environment on Windows:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Run ingestion and validation:

   ```powershell
   python src/ingestion/load_raw_data.py
   ```

5. Generate curated data:

   ```powershell
   python src/transformation/create_curated_orders.py
   ```

6. Run data-quality validation:

   ```powershell
   python src/validation/validate_orders.py
   ```

### AWS Analytics

The cloud pipeline uses Amazon S3, AWS Glue, the Glue Data Catalog, and Amazon Athena in the Mumbai region (`ap-south-1`).

The AWS pipeline is configured in the AWS Console. Athena query results depend on the current S3 dataset and Glue Catalog schema.

## Future Improvements

* Automate incremental ingestion and handling of deleted or updated records.
* Add automated tests for valid and invalid input records.
* Orchestrate ingestion, transformation, and catalog updates.
* Expand the sample dataset to demonstrate larger-scale processing.
* Explore Amazon Redshift for advanced data warehousing and analytics.

## Disclaimer

This project uses synthetic sample e-commerce data for learning and demonstration purposes. Reported metrics reflect the current sample dataset and are not real business results.
