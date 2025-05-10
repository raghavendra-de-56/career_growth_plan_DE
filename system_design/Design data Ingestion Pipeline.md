### Data Ingestion Pipeline

Design a data ingestion pipeline to collect data from multiple sources (e.g., APIs, databases, files) and load it into a centralized data warehouse (e.g., Amazon Redshift, Google BigQuery).

System Design
- Use a message broker (e.g., Apache Kafka, Amazon SQS) to handle data ingestion from multiple sources.
- Implement data processing and transformation using a data processing engine (e.g., Apache Spark, Apache Beam).
- Load processed data into a centralized data warehouse.

Architecture Diagram
```
                      +---------------+
                      |  Data Sources  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Message Broker  |
                      |  (Apache Kafka,   |
                      |   Amazon SQS)     |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Data Processing  |
                      |  (Apache Spark,    |
                      |   Apache Beam)    |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Data Warehouse  |
                      |  (Amazon Redshift, |
                      |   Google BigQuery) |
                      +---------------+
```
