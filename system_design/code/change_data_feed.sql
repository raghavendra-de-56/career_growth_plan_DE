-- Enable Change Data Feed on Delta Table
ALTER TABLE orders SET TBLPROPERTIES (delta.enableChangeDataFeed = true);

-- Read Changed Rows
SELECT * FROM table_changes('orders', '2024-05-01');
