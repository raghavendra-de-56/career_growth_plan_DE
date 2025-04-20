### What is Dimensional Modeling? ###

Dimensional modeling is a data design technique optimized for analytical querying. It structures data in a way that makes it easy for users (analysts, BI tools, data scientists) to slice and dice information.

It revolves around two main types of tables:

Fact Tables – store measurable, quantitative data (e.g., sales, orders)

Dimension Tables – store descriptive attributes (e.g., customer name, product details)

### Core Concepts ###

1. Facts

Central table that contains numerical measures.

Examples: sales_amount, order_quantity, revenue, clicks.


2. Dimensions

Descriptive entities related to facts.

Examples: product, customer, store, date, region.


3. Star Schema

One fact table connected to multiple dimension tables directly.

Easy for reporting tools and query optimization.

```
            +-----------+
            | Customer  |
            +-----------+
                  |
+---------+   +-----------+   +---------+
| Product |---|  Sales    |---|  Date   |
+---------+   +-----------+   +---------+
                  |
            +-----------+
            |  Store     |
            +-----------+
```

4. Snowflake Schema

Dimensions are normalized into sub-dimensions.

More storage-efficient but slightly complex.

5. Slowly Changing Dimensions (SCD)

Track changes in dimension attributes over time:

Type 1: Overwrite old data

Type 2: Preserve history with versioned rows

Type 3: Add new columns for versioned values

---

### Example: Retail Sales Data Model ###

Fact Table: fact_sales

Dimension Tables:

dim_product: product_id, name, category, brand

dim_customer: customer_id, name, age, location

dim_store: store_id, name, city, region

dim_date: date_id, date, day_of_week, month, year

### Databricks: Dimensional Model Example (PySpark) ###

Here’s how you'd define these in PySpark (Delta Tables):
```
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

# Example: dim_product
dim_product = spark.createDataFrame([
    (1, 'Nike Shoes', 'Footwear', 'Nike'),
    (2, 'Adidas T-Shirt', 'Apparel', 'Adidas')
], ['product_id', 'name', 'category', 'brand'])

dim_product.write.format("delta").mode("overwrite").saveAsTable("dim_product")

# Example: fact_sales
fact_sales = spark.createDataFrame([
    (101, 1, 1001, 10, 20230401, 2, 200.0),
    (102, 2, 1002, 11, 20230402, 1, 100.0)
], ['sale_id', 'product_id', 'customer_id', 'store_id', 'date_id', 'quantity', 'revenue'])

fact_sales.write.format("delta").mode("overwrite").saveAsTable("fact_sales")
```

### Querying in Dimensional Model

Example: Total revenue by category and month
```
SELECT
  dp.category,
  dd.month,
  SUM(fs.revenue) as total_revenue
FROM fact_sales fs
JOIN dim_product dp ON fs.product_id = dp.product_id
JOIN dim_date dd ON fs.date_id = dd.date_id
GROUP BY dp.category, dd.month

```

### Real-World Scenarios:

1. Design and own enterprise-wide semantic layer
2. Implement SCD Type 2 for customer profile changes
3. Optimize queries using materialized views or data marts
4. Build data contracts between fact/dimension providers and consumers

Advanced dimensional modeling techniques—aggregate fact tables, bridge tables, and multi-fact star schemas—are essential for designing scalable, performant, and flexible analytics solutions. These are critical for production-grade data modeling.

### Aggregate Fact Tables 

What it is:

An aggregate fact table stores pre-summarized metrics (e.g., daily, weekly, monthly totals), which significantly improves query performance.

Why it matters:

Avoids scanning large raw fact tables for each query.

Powers dashboards and KPIs with low latency.

Example:

This table may be derived from a base fact_sales table.

How to build (PySpark):
```
agg_sales = spark.sql("""
SELECT
  product_id,
  date_id,
  SUM(quantity) AS total_quantity,
  SUM(revenue) AS total_revenue
FROM fact_sales
GROUP BY product_id, date_id
""")

agg_sales.write.format("delta").mode("overwrite").saveAsTable("fact_sales_daily_agg")
```

### Bridge Tables

What it is:

A bridge table is used to model many-to-many relationships between a fact table and a dimension.

Why it matters:

Dimensional modeling typically assumes 1-to-many relationships, but real-world data isn’t always that clean.

Real-world Example:

A customer can belong to multiple loyalty programs, and a loyalty program can include many customers.

Tables:

dim_customer

dim_loyalty_program

bridge_customer_program (customer_id, program_id)


Bridge Table Sample:

Querying (SQL):
```
SELECT
  lp.program_name,
  COUNT(DISTINCT fs.customer_id) AS unique_customers,
  SUM(fs.revenue) AS total_revenue
FROM fact_sales fs
JOIN bridge_customer_program bcp ON fs.customer_id = bcp.customer_id
JOIN dim_loyalty_program lp ON bcp.program_id = lp.program_id
GROUP BY lp.program_name
```

### Multi-Fact Star Schema

What it is:

A schema with multiple fact tables that may share common dimensions (conformed dimensions).

Why it matters:

You often have different types of business processes—orders, shipments, inventory, returns—each modeled as separate fact tables.

Example:

Fact Tables:

fact_orders (order_id, product_id, date_id, quantity_ordered)

fact_shipments (shipment_id, product_id, date_id, quantity_shipped)

Shared Dimensions:

dim_product, dim_date, dim_customer

This allows you to:

Compare orders vs. shipments

Analyze delays or fulfillment rates


Visualization:
```
                +------------+
                | dim_product|
                +------------+
                      |
+-------------+   +-------------+   +-------------+
| fact_orders |   | fact_returns|   | fact_shipments |
+-------------+   +-------------+   +-------------+
                      |
                +------------+
                |  dim_date  |
                +------------+
```

You are expected to:

1. Build data models that power self-service analytics for thousands of users.
2. Make performance trade-offs using aggregation or denormalization.
3. Handle complex relationships (many-to-many, temporal joins).
4. Own data contract enforcement across multi-source facts and conformed dimensions.


