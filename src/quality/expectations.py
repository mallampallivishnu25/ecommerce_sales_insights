# Lightweight data quality checks. Extend as needed.
import duckdb, os

DB = os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb")


def main():
    con = duckdb.connect(DB)
    # Example: no negative prices
    neg_prices = con.sql("SELECT COUNT(*) c FROM stg_order_items WHERE price < 0").fetchone()[0]
    assert neg_prices == 0, f"Found {neg_prices} negative prices"
    # Example: PK uniqueness on (order_id, order_item_id)
    dups = con.sql(
        """
      SELECT COUNT(*) FROM (
        SELECT order_id, order_item_id, COUNT(*) c
        FROM stg_order_items
        GROUP BY 1,2 HAVING COUNT(*) > 1
      )
    """
    ).fetchone()[0]
    assert dups == 0, "Duplicate (order_id, order_item_id) found"
    print("Basic quality checks passed.")


if __name__ == "__main__":
    main()
