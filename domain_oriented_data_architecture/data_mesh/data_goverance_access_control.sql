# Column-level permissions using Unity Catalog:

GRANT SELECT (order_id, total_amount) 
ON TABLE retail_domain.orders.retail_orders 
TO marketing_team;

GRANT SELECT
ON TABLE marketing_domain.campaigns.marketing_campaigns 
TO retail_team;
