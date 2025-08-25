import os
import duckdb, pandas as pd
from prophet import Prophet

DB = os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb")


def main():
    con = duckdb.connect(DB)
    daily = con.sql(
        """
        SELECT order_date AS ds, SUM(gross_revenue) AS y
        FROM fact_orders GROUP BY 1 ORDER BY 1
        """
    ).df()
    if daily.empty:
        print("No daily data for forecast.")
        return
    m = Prophet(seasonality_mode="multiplicative")
    m.fit(daily)
    future = m.make_future_dataframe(periods=90)
    fcst = m.predict(future)
    os.makedirs("data/external", exist_ok=True)
    fcst[["ds","yhat","yhat_lower","yhat_upper"]].to_parquet("data/external/forecast.parquet", index=False)
    print("Saved data/external/forecast.parquet")


if __name__ == "__main__":
    main()
