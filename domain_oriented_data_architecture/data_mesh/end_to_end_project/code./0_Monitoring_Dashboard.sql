-- Notebook 6: Monitoring and Dashboarding

-- Filename: 5.0_Monitoring_Dashboard.ipynb

-- Example SQL for Databricks SQL Dashboard

-- 1. Volume Trend
SELECT date_trunc('day', order_date) as day, COUNT(*) as orders_count
FROM delta./mnt/datalake/silver/orders/
GROUP BY day
ORDER BY day;

-- 2. Daily Sales Amount
SELECT date_trunc('day', order_date) as day, SUM(order_amount) as total_sales
FROM delta./mnt/datalake/silver/orders/
GROUP BY day
ORDER BY day;

-- Create SQL Queries → Pin them as Dashboard Widgets in Databricks SQL.
