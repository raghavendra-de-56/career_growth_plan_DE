Let’s build Mini Project A: Iceberg for Data Mesh — using Apache Iceberg to simulate a data mesh architecture where domain teams own their data products, but they’re discoverable, queryable, and governed centrally.

---

Mini Project: Iceberg-based Data Mesh on Databricks

Scenario:

Two domain teams own their respective data:

Inventory Team publishes inventory_status as an Iceberg table.

Orders Team publishes order_metrics as an Iceberg table.

The Planning Team consumes both via Unity Catalog and creates a combined view for planning decisions.

---

Catalog Setup

Let’s assume:

Unity Catalog = main

Schemas = inventory_domain, orders_domain, planning_domain

---

Step 1: Inventory Team - Create Iceberg Table

# Inventory team creates an Iceberg table
```
inventory_data = [
    (101, "SKU-001", 500, "2025-04-01"),
    (102, "SKU-002", 0, "2025-04-01"),
    (103, "SKU-003", 120, "2025-04-01")
]
df_inventory = spark.createDataFrame(inventory_data, ["store_id", "sku", "stock_qty", "inventory_date"])

df_inventory.writeTo("main.inventory_domain.inventory_status") \
    .using("iceberg") \
    .tableProperty("format-version", "2") \
    .createOrReplace()

```

Step 2: Orders Team - Create Iceberg Table
```
# Orders team publishes order metrics
orders_data = [
    (101, "SKU-001", 50, "2025-04-01"),
    (102, "SKU-002", 30, "2025-04-01"),
    (103, "SKU-003", 80, "2025-04-01")
]
df_orders = spark.createDataFrame(orders_data, ["store_id", "sku", "orders", "order_date"])

df_orders.writeTo("main.orders_domain.order_metrics") \
    .using("iceberg") \
    .tableProperty("format-version", "2") \
    .createOrReplace()
```


Step 3: Planning Team - Consume and Join Tables
```
# Planning team consumes both tables
df_inventory = spark.read.table("main.inventory_domain.inventory_status")
df_orders = spark.read.table("main.orders_domain.order_metrics")

# Join to generate stockout alerts
df_alerts = df_inventory.join(df_orders, ["store_id", "sku"]) \
    .withColumn("stockout_risk", (df_inventory.stock_qty < df_orders.orders))

df_alerts.select("store_id", "sku", "stock_qty", "orders", "stockout_risk").show()
```


Step 4: Publish a Derived Iceberg Table in Your Domain
```
# Planning publishes a derived data product
df_alerts.writeTo("main.planning_domain.stockout_risk_view") \
    .using("iceberg") \
    .tableProperty("format-version", "2") \
    .createOrReplace()
```
Step 5: Enable Governance & Discovery

Use Unity Catalog tags, owners, and comments to document data products.

Apply column-level access controls.

Use Auto Loader or workflows to keep domains up-to-date.

---

What This Project Demonstrates

Domain ownership with decentralized write access.

Centralized read and governance using Unity Catalog.

Time travel and schema evolution at domain level.

Reusable and composable data products.
