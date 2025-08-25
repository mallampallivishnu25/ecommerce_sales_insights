CREATE OR REPLACE TABLE dim_customer AS
SELECT DISTINCT
  c.customer_id,
  c.customer_unique_id,
  c.customer_city,
  c.customer_state
FROM stg_customers c;
