CREATE OR REPLACE TABLE fact_orders AS
WITH pay AS (
  SELECT order_id, SUM(payment_value) AS payment_value
  FROM stg_order_payments GROUP BY 1
),
items AS (
  SELECT
    order_id,
    SUM(price + freight_value) AS gross_revenue,
    COUNT(*) AS items_cnt
  FROM stg_order_items GROUP BY 1
)
SELECT
  o.order_id,
  o.customer_id,
  o.order_status,
  CAST(o.order_purchase_timestamp AS DATE) AS order_date,
  i.gross_revenue,
  COALESCE(p.payment_value, 0) AS payment_value,
  i.items_cnt
FROM stg_orders o
LEFT JOIN items i USING(order_id)
LEFT JOIN pay p USING(order_id);
