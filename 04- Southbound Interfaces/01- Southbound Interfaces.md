---
title: Data Ingestion (Southbound)
description: Overview of southbound data ingestion in AnyLog — connectors, mapping, file pipeline, and prerequisites.
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**            | **Version** |
|------------|----------------|-----------------------|----------|
| 2026-04-17 |                | creation              |          |
| 2026-04-25 |                | hyperlinks            |          |
| 2026-07-20 | Eric Aquaronne | added change log      | 2.0.2606 |
| 2026-07-24 | Ori Shadmon    | rewrite               |          |
--->

AnyLog receives data from edge devices, sensors, and applications through a set of **southbound connectors**.
All connectors ultimately produce JSON files that flow through a common pipeline: Watch Directory → Operator → Local Database.

This page covers the pipeline, prerequisites, and mapping. For connector-specific configuration see the individual pages
linked below.

> **See also:** [Northbound Interfaces (data egress)]() — the counterpart to this page, covering how AnyLog forwards
> data onward once it's ingested and stored.

### The ingestion pipeline

```
Data Source
    │
    ▼
Southbound Connector
(MQTT, REST PUT, Kafka, gRPC, PLC/OPC-UA, Syslog, ...)
    │
    ▼
Internal Buffers / Streamer
(aggregates events, flushes on time or volume threshold)
    │
    ▼
Watch Directory  (JSON files)
    │
    ▼
Operator
(reads files, maps JSON → SQL, inserts to local DB)
    │
    ▼
Local Database (SQLite / PostgreSQL)
```

---

## The connectors

### Built-in Southbound connectors
* [REST](01-%20Direct%20Connectors/01-%20REST.md)
  * **PUT** — data is stored as-is.
  * **POST** — requires a [message client]() to translate the payload before it's stored.
* [MQTT / Kafka](01-%20Direct%20Connectors/02-%20Message%20Broker.md) — utilizes AnyLog's built-in MQTT / Kafka message broker.
* [OPC-UA]()
* [Modbus]()
* [DNP3]()
* [EtherIP]()
* [gRPC]()
* [Video]()

### Third-Party Southbound Connectors

AnyLog focuses on the data management side rather than pulling data directly from every device and protocol. Where
we don't have a built-in connector, we recommend placing a third-party app between the device and AnyLog to bridge
the gap — the app talks to the device/sensor, and forwards the result to AnyLog over REST, MQTT, or Kafka.

* [External MQTT / Kafka]()
* [EdgeX]()
* [Node-RED]()
* [Telegraf]()

### Node Monitoring

Node and container health metrics (CPU, memory, disk, container status) are themselves ingested through this same
southbound pipeline — which is why monitoring configuration lives here rather than under Extended Services.

* [Node Monitoring]()
* [Docker Monitoring]()
* [Syslog]()

## Dummy Data 

We provide an MQTT connection to an array of different data sets. For details visit [Data Ingestion](07-%20Southbound%20Interfaces.md)
or [Live Data Generator](99-%20live-data-generator.md) to run locally. 