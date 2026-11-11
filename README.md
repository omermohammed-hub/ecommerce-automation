
@'
# Automated E-Commerce Sales and Product Analytics Pipeline

An end-to-end data engineering and analytics project that automates the extraction, transformation, validation and storage of e-commerce sales data using Python, Pandas, SQLite and GitHub Actions.

## Business Objective

Analyse historical e-commerce sales and product performance to understand:

- Sales revenue and order volumes
- Monthly sales trends
- Average order value
- Product category performance
- Items sold and freight charges

## Data Source

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

The project uses four source files:

- Orders
- Order items
- Products
- Product category translations

The dataset contains historical transactions from 2016–2018. It is not a live data feed.

## Technology Stack

- Python
- Pandas
- Kaggle API
- SQLite
- SQL
- Git and GitHub
- GitHub Actions
- Power BI (planned reporting layer)

## Pipeline Architecture

Kaggle API
    |
    v
Data Extraction
    |
    v
Data Transformation and Quality Checks
    |
    v
SQLite Database
    |
    v
SQL Analysis and Validation
    |
    v
Power BI Dashboard (planned)

## Data Model

The SQLite database contains three tables:

| Table | Description |
|---|---|
| DimOrders | Order details, status and purchase timestamp |
| DimProducts | Product identifiers and English categories |
| FactOrderItems | Order items, product references, prices and freight |

The fact table has relationships to both dimension tables through order_id and product_id.

## Key Business Metrics

The analysis currently calculates:

- Delivered orders
- Items sold
- Item revenue
- Freight value
- Average order value
- Monthly delivered revenue
- Revenue by product category

Item revenue is calculated from the order item price. Freight charges are reported separately.

The main sales KPIs use delivered orders. Other order statuses are retained in the database for analysis.

All monetary amounts are in Brazilian reais (BRL).

## Project Structure

ecommerce-automation/
|
|-- data/
|   |-- raw/                 # Downloaded source data (not committed)
|   |-- processed/           # Transformed data and SQLite database (not committed)
|
|-- scripts/
|   |-- extract_data.py
|   |-- transform_data.py
|   |-- load_database.py
|   |-- validate_database.py
|
|-- .github/
|   |-- workflows/           # GitHub Actions workflows (to be added)
|
|-- data_pipeline.py
|-- requirements.txt
|-- .gitignore
|-- README.md

## Running the Pipeline Locally

### 1. Clone the repository

    git clone <your-repository-url>
    cd ecommerce-automation

### 2. Create and activate a virtual environment

    python -m venv venv

Windows PowerShell:

    .\venv\Scripts\Activate.ps1

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Configure Kaggle API authentication

Configure Kaggle API credentials securely on your local machine.

Do not commit API tokens or credential files to GitHub.

### 5. Run the complete pipeline

    python data_pipeline.py

The pipeline executes extraction, transformation, database loading and SQL validation in sequence.

## Automation

GitHub Actions automation will be configured to support manual and scheduled execution.

Kaggle credentials will be stored using GitHub repository secrets rather than hardcoded in the source code.

## Data Quality

The pipeline includes checks for:

- Missing and invalid timestamps
- Missing or invalid prices and freight values
- Duplicate dimension keys
- Missing key fields
- Unmatched order and product references
- Database foreign-key integrity

Products without an available English category translation are retained under the category "Unknown".

## Current Project Status

- [x] Kaggle data extraction script
- [x] Data transformation
- [x] Data quality checks
- [x] SQLite database creation
- [x] SQL validation and business analysis
- [x] End-to-end local pipeline orchestration
- [ ] GitHub Actions automation
- [ ] Power BI dashboard
- [ ] Final project documentation

## Dataset Licence and Attribution

The Olist dataset is distributed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International licence (CC BY-NC-SA 4.0). Refer to the Kaggle dataset page and its licence terms before redistributing or using the data.

This project is intended for learning and portfolio demonstration.

---
'@ | Set-Content -Path README.md -Encoding UTF8
