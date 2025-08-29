# E-commerce Sales Insights

End-to-end, portfolio-ready analytics project for e-commerce: star schema, RFM & CLV, market-basket rules, forecasting, and an interactive Streamlit dashboard.

## Key features
- **Warehouse:** DuckDB (embedded) with SQL/star schema.
- **Data quality:** Great Expectations-style assertions (lightweight script).
- **Analytics:** RFM segmentation, Cohorts/retention, CLV (BG/NBD + Gamma-Gamma), market-basket (Apriori), forecasting (Prophet).
- **App:** Streamlit dashboard with KPIs and time series.
- **CI:** pytest + ruff on GitHub Actions.

## Data
Recommended dataset: **Olist Brazilian E-commerce** (multi-table orders, payments, items, customers, reviews, geo).

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/ingest/ingest_olist.py
python src/utils/io.py --run-sql src/transform/sql
python src/features/rfm.py
python src/features/clv_bg_nbd.py
python src/features/basket_rules.py
python src/models/forecast_prophet.py
streamlit run app/streamlit_app.py
```

## Screenshots

- **Dashboard Home (KPIs + Revenue trend)**  
  ![Dashboard Home](dashboards/screenshot_dashboard_home.png)

- **Customer Segmentation (RFM)**  
  ![Customer Segmentation](dashboards/screenshot_rfm.png)

- **Forecast (90-day)**  
  ![Forecast](dashboards/screenshot_forecast.png)

## Author

**Vishnu Mallampalli**  
Data & Analytics | ML & MLOps | E-commerce Insights

*Last updated: 2025-08-22*
