CREATE OR REPLACE TABLE fact_order_items AS
SELECT
  order_id,
  order_item_id,
  product_id,
  price,
  freight_value
FROM stg_order_items;
