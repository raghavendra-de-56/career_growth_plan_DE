-- Querying Streams with Databricks SQL
SELECT region, COUNT(*) as order_count
FROM orders
WHERE order_time >= current_date()
GROUP BY region;
