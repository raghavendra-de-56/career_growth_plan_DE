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


