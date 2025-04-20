### Data Vault Modeling

Data Vault Modeling is a methodology used to design data warehouses. It's a flexible, scalable, and highly adaptable architecture that allows you to track historical data and integrate information from different sources while minimizing ETL complexity.

### What is Data Vault Modeling?

Data Vault is a modeling methodology that:

1. Focuses on agility in data modeling.
2. Tracks historical data efficiently.
3. Enables a scalable architecture that can handle growing amounts of data.

Data Vault consists of three main components:

1. Hubs
2. Links
3. Satellites

Let’s dive deeper into each component and explain how they come together in a Data Vault system.

### 1. Hubs

A Hub represents business keys. These are the unique identifiers of core entities, like customers, products, or transactions.

Purpose: Store the unique, non-redundant business keys and their metadata (hash, load date, and record source).

Key characteristics: Hubs don’t store the descriptive data about the entity; instead, they store only the business key and metadata.

Example:

If we want to model Customer as a Hub:

### 2. Links

A Link represents the relationship between two or more Hubs. Links capture the connections between business keys in the Hubs.

Purpose: Capture relationships, associations, or transactions between different business entities.

Key characteristics: Links don’t store data about the relationship; they just link the Hubs with a unique combination of keys.

Example:

If we want to model a Sales Transaction between a Customer and a Product, we would create a Link between hub_customer and hub_product.

### 3. Satellites

A Satellite holds descriptive data that changes over time about the Hubs or Links. This is where the actual business data (e.g., customer name, product price, order amount) is stored. Satellites are crucial because they allow for historical tracking.

Purpose: Store descriptive data related to Hubs and Links. Keep track of how these attributes change over time.

Key characteristics: Satellites hold historical data with timestamps and track changes to the Hubs or Links they relate to.

Example:

A customer's demographic information in the customer_satellite.

Notice how the end_date for Alice’s old address marks when she moved to her new address, preserving the historical nature of the data.

### Why Data Vault?

Scalability: Data Vault is built to scale and adapt to growing data and changing business requirements.

Agility: It supports rapid changes to source systems (without affecting downstream consumers).

Historical Tracking: Data Vault allows for full historical tracking of changes, so you can see the evolution of your data over time.

Separation of Concerns: By separating the Hub, Link, and Satellite, Data Vault supports the separation of concerns. You can update descriptive data (Satellite) without affecting relationships (Link), and vice versa.

### Data Vault Modeling Example (Customer and Product)

Let’s walk through an example Data Vault model for a simple business scenario where you need to model Customer and Product data.

Step 1: Hubs

Hubs for Customer and Product
```
# Hub Customer
CREATE TABLE hub_customer (
    hub_customer_id STRING,    -- Business Key
    customer_hash_key STRING,  -- Hash of Business Key
    load_date DATE,            -- Date of record load
    record_source STRING       -- Source system
);

-- Hub Product
CREATE TABLE hub_product (
    hub_product_id STRING,     -- Business Key
    product_hash_key STRING,   -- Hash of Business Key
    load_date DATE,            -- Date of record load
    record_source STRING       -- Source system
);
```
Step 2: Links

Link between Customer and Product (Sales Transaction)
```
# Link between Customer and Product
CREATE TABLE link_sales_transaction (
    link_transaction_id STRING, -- Business Key for this relationship
    customer_hash_key STRING,   -- Link to Hub Customer
    product_hash_key STRING,    -- Link to Hub Product
    load_date DATE,             -- Date of record load
    record_source STRING        -- Source system
);
```
Step 3: Satellites

Customer Satellite
```
# Satellite for Customer data
CREATE TABLE satellite_customer (
    customer_hash_key STRING,   -- Link to Hub Customer
    name STRING,                -- Customer's Name
    address STRING,             -- Customer's Address
    start_date DATE,            -- When this record started being valid
    end_date DATE,              -- When this record ended being valid
    load_date DATE,             -- Date of record load
    record_source STRING        -- Source system
);
```
Product Satellite
```
# Satellite for Product data
CREATE TABLE satellite_product (
    product_hash_key STRING,    -- Link to Hub Product
    product_name STRING,        -- Product name
    product_category STRING,    -- Product category
    price DOUBLE,               -- Product price
    start_date DATE,            -- When this record started being valid
    end_date DATE,              -- When this record ended being valid
    load_date DATE,             -- Date of record load
    record_source STRING        -- Source system
);
```

### ETL Process with Data Vault

1. Extract:

Extract data from source systems (e.g., CRM for customers, sales system for product transactions).

2. Load:

1. Hubs: Load business keys with hash values.
2. Links: Identify relationships between business entities and load.
3. Satellites: Load descriptive data with timestamps and track changes.

3. Transform:

For the Satellites, make sure to:

Track historical changes.

Maintain the validity period for data.


4. Incremental Updates:

Handle incremental data updates in Hubs, Links, and Satellites:

For Hubs: Only new unique business keys are added.

For Links: Add new relationships.

For Satellites: Add new records for new versions or changes.

### Real-World Use Case for Data Vault:

Sales Analytics

1. Hub: Customer, Product, Sales_Transaction
2. Link: Sales_Transaction linking Customer and Product
3. Satellite: Customer demographics, Product details, Sales dates

Reporting: Using this structure, you can easily perform complex analyses such as:

Sales by region using the Sales_Transaction link and Product satellite.

Customer behavior using the Customer satellite and Sales_Transaction link.

### Advantages of Data Vault Modeling

1. Flexibility: Can handle any changes to source data without affecting the entire model.
2. Scalability: Perfect for growing organizations with evolving data.
3. Agility: Quickly adapt to new data sources and systems.
4. Historical Data: Traces every change in the data with effective dates.

### Conclusion

Data Vault is ideal for large-scale, historical, and scalable data warehouses. Its separation of business keys (Hubs), relationships (Links), and historical data (Satellites) offers great flexibility, especially when there are frequent changes in source systems or evolving business requirements.
