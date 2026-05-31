Dataset:
Source: Demand Forecasting Dataset via KaggleHub
python import kagglehub
path = kagglehub.dataset_download("raminhuseyn/demand-forecasting-dataset")

What's in it:

76,000 rows of retail transaction records
Date range: January 2022 – January 2024
5 stores, 20 products, 5 categories (Electronics, Clothing, Groceries, Furniture, Toys)
Key columns: Date, Store ID, Product ID, Category, Region, Demand, Price, Competitor Pricing, Discount, Promotion, Inventory Level, Units Ordered, Seasonality

Part 1 — Dataset Exploration & Visualisation
File: part1_dataset.py
Loads and cleans the dataset, computes summary statistics, and produces three charts that each tell a distinct story about the data.
Charts generated:
1. Monthly Revenue Trend : trajectory over 25 months with peak by Category & Promotion
2.Demand by Category & Promotion : How promotions lift demand across all five categories
3. Seasonal Demand Heatmapchart : Which regions peak in which seasons

Key findings from EDA:

Promotions lift average demand by ~29.8% across all categories
Summer is the strongest season; Winter is weakest
The North region leads on total units sold

Part 2 — Weekly Sales Report (Excel Export)
File: part2_dataset.py
Builds a production-ready Excel workbook from the CSV using openpyxl with full formatting: colour-coded headers, alternating row fills, number formatting, KPI banners, and auto-column widths.

Contents:
- Week-by-week revenue, units sold, transactions, avg price, and promo rows — plus a KPI banner at the top
- Revenue, demand, pricing, and promotion rate by product category
- Units sold, revenue, and pricing metrics by region
- Top 10 products ranked by total revenue

Part 3 — Product Data Quality Audit
File: part3_dataset.py
Analyses the product database and flags five categories of data quality issues, then prints a scored summary report.

Checks performed:
- Missing descriptions : Products with a blank or null description field
- Zero or negative unit prices : Prices that would indicate bad data entry or import errors
- Cost exceeds selling price : Products being sold at a loss (cost_price > unit_price)
- No category assignedProducts missing a category, which breaks reporting
- Duplicate SKUs : The same Product ID appearing more than once in the catalogue


Part 1 (API) — Basic AI API Calls
File: part1_api.py
Demonstrates how to make API calls to a large language model from Python using five different prompt types. The goal is to get comfortable with the request/response pattern before doing anything complex.

Part 2 (API) — AI-Generated Data Summary
File: part2_api.py
Computes a detailed statistical summary from the dataset using Pandas, then passes that summary to an AI API with a structured prompt. The model returns a single, polished plain-English paragraph written for a retail executive audience.

Part 3 (API) — Structured Text Report Formatter
File: part3_api.py
A standalone Python formatter that takes nested dictionaries of structured data and renders them as clean, readable terminal reports. Designed to make data outputs presentable without any external libraries.

Four sample reports printed:

Business Performance Summary
Category Performance Breakdown
Regional & Seasonal Report
Product Spot Check









