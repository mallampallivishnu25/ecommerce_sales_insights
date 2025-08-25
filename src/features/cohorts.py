import duckdb, pandas as pd, os

DB = os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb")


def main():
    con = duckdb.connect(DB)
    df = con.sql(
        """
        WITH firsts AS (
          SELECT customer_id, MIN(order_date) AS first_order
          FROM fact_orders GROUP BY 1
        )
        SELECT
          f.customer_id,
          f.first_order,
          o.order_date,
          DATE_TRUNC('month', f.first_order) AS cohort_month,
          DATE_TRUNC('month', o.order_date) AS order_month
        FROM firsts f
        JOIN fact_orders o USING(customer_id)
        """
    ).df()
    if df.empty:
        print("Empty cohorts source.")
        return
    df["cohort_index"] = ((df["order_month"] - df["cohort_month"]).dt.days // 30).astype(int)
    pivot = (
        df.groupby(["cohort_month", "cohort_index"])["customer_id"]
        .nunique()
        .reset_index()
        .pivot(index="cohort_month", columns="cohort_index", values="customer_id")
        .fillna(0)
    )
    os.makedirs("data/external", exist_ok=True)
    pivot.to_parquet("data/external/cohorts.parquet")
    print("Saved data/external/cohorts.parquet")


if __name__ == "__main__":
    main()
