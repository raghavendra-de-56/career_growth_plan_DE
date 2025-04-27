# Create Sample Data Products

# Retail: Orders table
USE CATALOG retail_domain;
USE SCHEMA orders;

CREATE TABLE IF NOT EXISTS retail_orders (
  order_id STRING,
  customer_id STRING,
  order_date DATE,
  total_amount DOUBLE
)
USING DELTA;

INSERT INTO retail_orders VALUES
('O1', 'C1', current_date(), 500.0),
('O2', 'C2', current_date(), 1200.5);

# Marketing: Campaigns table
USE CATALOG marketing_domain;
USE SCHEMA campaigns;

CREATE TABLE IF NOT EXISTS marketing_campaigns (
  campaign_id STRING,
  campaign_name STRING,
  start_date DATE,
  end_date DATE
)
USING DELTA;

INSERT INTO marketing_campaigns VALUES
('CP1', 'Diwali Sale', current_date(), date_add(current_date(), 10)),
('CP2', 'Black Friday', current_date(), date_add(current_date(), 5));
