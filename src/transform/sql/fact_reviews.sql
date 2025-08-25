CREATE OR REPLACE TABLE fact_reviews AS
SELECT
  order_id,
  review_score,
  review_creation_date::DATE AS review_date
FROM stg_reviews;
