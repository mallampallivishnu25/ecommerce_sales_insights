CREATE OR REPLACE TABLE dim_product AS
SELECT DISTINCT
  p.product_id,
  p.product_category_name,
  p.product_weight_g,
  p.product_length_cm,
  p.product_height_cm,
  p.product_width_cm
FROM stg_products p;
