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
