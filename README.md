# E-commerce Sales Insights

End-to-end, portfolio-ready analytics project for e-commerce: star schema, RFM & CLV, market-basket rules, forecasting, and an interactive Streamlit dashboard.

## Key features
- **Warehouse:** DuckDB (embedded) with SQL/star schema.
- **Data quality:** Great Expectations-style assertions (lightweight script).
- **Analytics:** RFM segmentation, Cohorts/retention, CLV (BG/NBD + Gamma-Gamma), market-basket (Apriori), forecasting (Prophet).
- **App:** Streamlit dashboard with KPIs and time series.
- **CI:** pytest + ruff on GitHub Actions.

## Data
Recommended primary dataset: **Olist Brazilian E-commerce** (multi-table orders, payments, items, customers, reviews, geo).  
Place extracted CSVs under `data/raw/olist/` with the original filenames, e.g.:

```
olist_orders_dataset.csv
olist_customers_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
olist_geolocation_dataset.csv
olist_order_reviews_dataset.csv
```

> You can swap in other retail datasets (UCI Online Retail II / Instacart / GA4 BigQuery sample) by adapting `ingest` and star-schema SQL.

## Quickstart
```bash
# 1) Setup env
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# 2) Load data into DuckDB (expects CSVs in data/raw/olist/)
python src/ingest/ingest_olist.py

# 3) Build star schema tables
python src/utils/io.py --run-sql src/transform/sql

# 4) Run analytics
python src/features/rfm.py
python src/features/clv_bg_nbd.py
python src/features/basket_rules.py
python src/models/forecast_prophet.py

# 5) Launch dashboard
streamlit run app/streamlit_app.py
```

## Project layout
```
ecommerce-sales-insights/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ .github/workflows/ci.yml
├─ data/ (raw & external; gitignored)
├─ warehouse/duckdb/retail.duckdb
├─ src/
│  ├─ ingest/ingest_olist.py
│  ├─ transform/sql/*.sql
│  ├─ features/[rfm.py, cohorts.py, clv_bg_nbd.py, basket_rules.py]
│  ├─ models/[forecast_prophet.py, churn_propensity.py]
│  ├─ quality/expectations.py
│  └─ utils/io.py
├─ app/streamlit_app.py
├─ tests/
│  ├─ test_structure.py
│  └─ test_imports.py
└─ dashboards/
```

## Notes
- This repo uses **DuckDB** for fast, portable analytics. You can point to Postgres by swapping connection bits.
- `dbt_project/` is included as a *placeholder* if you want to convert SQL to dbt models later.
- For CLV, ensure you have enough order history for stable fit; small samples may need smoothing or simpler heuristics.

## Author

**Vishnu Mallampalli**  
Data & Analytics | ML & MLOps | E-commerce Insights

*Last updated: 2025-08-22*

## Screenshots

- **Dashboard Home (KPIs + Revenue trend)**  
  ![Dashboard Home](dashboards/screenshot_dashboard_home.png)

- **Customer Segmentation (RFM)**  
  ![Customer Segmentation](dashboards/screenshot_rfm.png)

- **Forecast (90-day)**  
  ![Forecast](dashboards/screenshot_forecast.png)

> Tip: Take a full-window screenshot and save the PNG files under `dashboards/`. They’re gitignored by default; remove from `.gitignore` or paste images in your GitHub README via drag & drop.

## Personal Experience

The E-commerce Sales Insights project let me practice the whole process of a professional data analytics project, just as what would happen in a real business setting.  The main goal of the project was to provide a production-ready, portfolio-ready solution for figuring out sales patterns, consumer behavior, and revenue forecasts in an online store.  From the start, I saw the exercise as a whole process that included meticulous data ingestion, warehouse design, advanced analytics, visualization, and automation through continuous integration.

 The initial step was to model the data and set up the warehouse.  I made a star schema in DuckDB to manage the Olist Brazilian E-commerce dataset, which has millions of records on customers, orders, payments, goods, reviews, and geolocation.  This technique turned raw transactional files into structured fact and dimension tables that could handle large analytical queries.  The experience was quite helpful in helping me remember what I knew about relational architecture and SQL optimization.  In addition to developing the schema, I included lightweight data quality tests based on Great Expectations to make sure that criteria like unique primary keys and non-negative prices were met.  These processes made sure that the analysis that followed was based on solid data, which is a very important requirement in professional analytics settings.

 After setting up the warehouse, I turned my attention to more complex analytics.  I used RFM (Recency, Frequency, Monetary) segmentation to group clients into different behavioral clusters. Marketing teams commonly use this strategy to run targeted advertisements.  I then used cohort studies to look at how customer retention changed over time, which helped me measure loyalty trends.  I used the Beta-Geometric/NBD and Gamma-Gamma frameworks to create Customer Lifetime Value (CLV) models for financial evaluation.  These models needed rigorous data preparation, especially making sure that the money values were stable and that the customer histories had enough transactions to make accurate estimates.  The result was a set of future value projections that can be understood and used to help with client relationship management.

 At the same time, I used the Apriori algorithm to do market-basket research and find product affinity rules. These rules helped me learn about cross-selling potential and buying habits.  I also used Prophet to combine time-series forecasting with Prophet to guess how income would change over the next 90 days.  This was especially important because it added a predictive element, showing how forward-looking analytics may help with business planning in retail settings.  I then incorporated all of these analytical outputs onto an interactive Streamlit dashboard, where I showed KPIs, revenue time series, client segmentation, and forecasts in a way that was easy for business people to understand.  Designing this interface made it clear how important it is to connect technical analytics with communication with stakeholders.

 I used GitHub Actions to set up continuous integration (CI) pipelines to finish the project.  Using Ruff and Black, the workflow automatically enforced code quality and ran lightweight pytest checks to make sure everything worked.  I learned how to customize procedures to find a compromise between stability and efficiency by splitting lightweight tests from full local runs. This helped me deal with CI issues with larger libraries like Prophet and lifetimes.  This made the project more professional and showed how things are done in modern data engineering setups.

 In general, this project helped me get better at a wide range of data engineering, machine learning analytics, visualization, and DevOps methods.  More significantly, it taught me how to think like a data professional: how to turn raw data into useful insights, how to use advanced models to create money for the business, and how to convey results in ways that make sense to decision-makers.  This project helped me become more technically skilled and gave me the confidence to deal with real-world data problems in a systematic and professional way.
