import os
import duckdb, pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

DB = os.getenv("DUCKDB_PATH", "warehouse/duckdb/retail.duckdb")


def main():
    con = duckdb.connect(DB)
    df = con.sql("""SELECT order_id, product_id FROM fact_order_items""").df()
    if df.empty:
        print("Empty fact_order_items. Build transforms first.")
        return
    basket = (df.assign(v=1)
                .pivot_table(index="order_id", columns="product_id", values="v", fill_value=0))
    freq = apriori(basket.astype(bool), min_support=0.01, use_colnames=True)
    if freq.empty:
        print("No frequent itemsets at min_support=0.01; try lowering support.")
        return
    rules = association_rules(freq, metric="lift", min_threshold=1.05) \            .sort_values("lift", ascending=False)
    os.makedirs("data/external", exist_ok=True)
    rules.to_parquet("data/external/basket_rules.parquet", index=False)
    print("Saved data/external/basket_rules.parquet")


if __name__ == "__main__":
    main()
