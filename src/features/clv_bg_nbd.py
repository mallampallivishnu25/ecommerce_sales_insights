import os
import duckdb, pandas as pd
from lifetimes import BetaGeoFitter, GammaGammaFitter

DB = os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb")


def main():
    con = duckdb.connect(DB)
    tx = con.sql(
        """
        SELECT customer_id,
               MIN(order_date) AS first_date,
               MAX(order_date) AS last_date,
               COUNT(*)-1 AS frequency,
               DATE_DIFF('day', MIN(order_date), MAX(order_date)) AS recency,
               DATE_DIFF('day', MIN(order_date), CURRENT_DATE) AS T,
               AVG(gross_revenue) AS monetary_value
        FROM fact_orders
        GROUP BY 1
        HAVING monetary_value > 0
        """
    ).df()
    if tx.empty:
        print("Empty dataset for CLV. Ensure fact_orders is populated.")
        return
    bgf = BetaGeoFitter()
    bgf.fit(tx["frequency"], tx["recency"], tx["T"])
    ggf = GammaGammaFitter()
    ggf.fit(tx["frequency"], tx["monetary_value"])
    tx["clv_90d"] = ggf.customer_lifetime_value(
        bgf,
        tx["frequency"], tx["recency"], tx["T"], tx["monetary_value"],
        time=3,  # 3 months ~ 90 days
        freq="W",
    )
    os.makedirs("data/external", exist_ok=True)
    tx.to_parquet("data/external/clv.parquet", index=False)
    print("Saved data/external/clv.parquet")


if __name__ == "__main__":
    main()
