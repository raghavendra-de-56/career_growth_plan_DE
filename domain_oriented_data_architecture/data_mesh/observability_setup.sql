# Observability Setup (Basic Metrics)

-- Create a view that tracks the volume and last load timestamp
CREATE OR REPLACE VIEW retail_domain.orders.orders_observability AS
SELECT
  count(*) as total_records,
  max(order_date) as latest_order_date
FROM retail_orders;

-- You can now query this view to monitor freshness!
