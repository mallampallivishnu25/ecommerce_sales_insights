import duckdb, pandas as pd
from sklearn.cluster import KMeans
import os

DB = os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb")

def main():
    con = duckdb.connect(DB)
    rfm = con.sql(
        """
        SELECT customer_id,
               DATE_DIFF('day', MAX(order_date), CURRENT_DATE) AS recency,
               COUNT(DISTINCT order_id) AS frequency,
               SUM(gross_revenue) AS monetary
        FROM fact_orders
        GROUP BY 1
        """
    ).df()
    if rfm.empty:
        print("No data in fact_orders. Did you run ingest and transforms?")
        return
    rfm[["R","F","M"]] = rfm[["recency","frequency","monetary"]].rank(pct=True)
    km = KMeans(n_clusters=5, n_init="auto", random_state=42)
    rfm["segment"] = km.fit_predict(rfm[["R","F","M"]])
    os.makedirs("data/external", exist_ok=True)
    rfm.to_parquet("data/external/rfm.parquet", index=False)
    print("Saved data/external/rfm.parquet")

if __name__ == "__main__":
    main()
