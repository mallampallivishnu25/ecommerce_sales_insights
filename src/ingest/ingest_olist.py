from pathlib import Path
import duckdb
import pandas as pd
import os

DB_PATH = os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb")
RAW = Path("data/raw/olist")

TABLES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
}

def main():
    if not RAW.exists():
        raise SystemExit(f"Expected CSVs under {RAW}.")
    con = duckdb.connect(DB_PATH)
    for t, f in TABLES.items():
        path = RAW / f
        if not path.exists():
            print(f"Warning: missing {path}, skipping.")
            continue
        print(f"Loading {path} -> stg_{t}")
        df = pd.read_csv(path)
        con.execute(f"""CREATE OR REPLACE TABLE stg_{t} AS SELECT * FROM df""")
    con.close()
    print("Loaded available Olist tables into DuckDB.")

if __name__ == "__main__":
    main()
