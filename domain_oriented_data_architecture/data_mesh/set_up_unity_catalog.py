# Purpose: Create catalogs, schemas, tables separately per domain.

# Setup for Retail Domain
CREATE CATALOG IF NOT EXISTS retail_domain;
USE CATALOG retail_domain;
CREATE SCHEMA IF NOT EXISTS orders;
CREATE SCHEMA IF NOT EXISTS products;
CREATE SCHEMA IF NOT EXISTS customers;

# Setup for Marketing Domain
CREATE CATALOG IF NOT EXISTS marketing_domain;
USE CATALOG marketing_domain;
CREATE SCHEMA IF NOT EXISTS campaigns;
CREATE SCHEMA IF NOT EXISTS clicks;
