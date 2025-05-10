### Real-time Data Processing Pipeline
Design a real-time data processing pipeline to process streaming data from IoT devices and detect anomalies in real-time.

System Design
- Use a streaming data processing engine (e.g., Apache Kafka Streams, Apache Flink) to process streaming data from IoT devices.
- Implement anomaly detection using machine learning algorithms (e.g., One-Class SVM, Isolation Forest).
- Store processed data in a NoSQL database (e.g., Apache Cassandra, MongoDB) for real-time analytics.

Architecture Diagram
```
                      +---------------+
                      |  IoT Devices   |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Streaming Data  |
                      |  Processing Engine  |
                      |  (Apache Kafka    |
                      |   Streams, Apache  |
                      |   Flink)          |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Anomaly Detection|
                      |  (Machine Learning) |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  NoSQL Database  |
                      |  (Apache Cassandra, |
                      |   MongoDB)        |
                      +---------------+
```
