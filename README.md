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

Add your screenshots here after running the app locally.

- Dashboard Home (KPIs + Revenue trend)  
  `dashboards/screenshot_dashboard_home.png`

- Customer Segmentation (RFM)  
  `dashboards/screenshot_rfm.png`

- Forecast (90-day)  
  `dashboards/screenshot_forecast.png`

> Tip: Take a full-window screenshot and save the PNG files under `dashboards/`. They’re gitignored by default; remove from `.gitignore` or paste images in your GitHub README via drag & drop.
