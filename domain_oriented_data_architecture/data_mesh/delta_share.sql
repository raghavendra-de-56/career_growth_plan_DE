--Delta Sharing for Cross-Domain Data Sharing

--Suppose you want Retail Domain to share Orders Table with the Marketing Domain team.

-- Step-by-Step (High-level)

-- 1. Create a share
---2. Add retail_orders table into the share
---3. Grant access to marketing_team

---Sample SQL on Databricks

CREATE SHARE IF NOT EXISTS retail_orders_share;

ALTER SHARE retail_orders_share ADD TABLE retail_domain.orders.retail_orders;

GRANT SELECT ON SHARE retail_orders_share TO marketing_team;

--Now the Marketing team can query Retail orders without violating Data Mesh principles!
