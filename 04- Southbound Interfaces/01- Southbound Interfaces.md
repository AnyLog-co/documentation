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

> **See also:** <a href="../05-%20Northbound%20Connectors" target="_blank">Northbound Interfaces (data egress)</a> — the counterpart to this page, covering how AnyLog forwards
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
* <a href="./02-%20Direct%20Connectors/01-%20REST.md" target="_blank">REST</a>
  * **PUT** — data is stored as-is.
  * **POST** — requires a <a href="./02-%20Direct%20Connectors/01-%20REST.md" target="_blank">message client</a> to translate the payload before it's stored.
* <a href="02-%20Direct%20Connectors/02-%20Message%20Broker.md" target="_blank">MQTT / Kafka</a> — utilizes AnyLog's built-in MQTT / Kafka message broker.
* <a href="03-%20Industrial%20Connectors/02-%20OPC-UA.md" target="_blank">OPC-UA</a>
* <a href="03-%20Industrial%20Connectors/01-%20Modbus.md" target="_blank">Modbus</a>
* <a href="03-%20Industrial%20Connectors/04-%20DNP3.md" target="_blank">DNP3</a>
* <a href="03-%20Industrial%20Connectors/03-%20EtherIP.md" target="_blank">EtherIP</a>
* <a href="05-%20RPC%20&%20Media%20Streaming/01-%20gRPC.md" target="_blank">gRPC</a>
* <a href="05-%20RPC%20&%20Media%20Streaming/02-%20Video%20Streaming.md" target="_blank">Video</a>

### Third-Party Southbound Connectors

AnyLog focuses on the data management side rather than pulling data directly from every device and protocol. Where
we don't have a built-in connector, we recommend placing a third-party app between the device and AnyLog to bridge
the gap — the app talks to the device/sensor, and forwards the result to AnyLog over REST, MQTT, or Kafka.

* <a href="02-%20Direct%20Connectors/02-%20Message%20Broker.md" target="_blank">External MQTT / Kafka</a>
* <a href="06-%20Third-Party/03-%20EdgeX.md" target="_blank">EdgeX</a>
* <a href="06-%20Third-Party/01-%20node-RED.md" target="_blank">Node-RED</a>
* <a href="06-%20Third-Party/02-%20Telegraf.md" target="_blank">Telegraf</a>

### Node Monitoring

Node and container health metrics (CPU, memory, disk, container status) are themselves ingested through this same
southbound pipeline — which is why monitoring configuration lives here rather than under Extended Services.

* <a href="04-%20Monitoring/01-%20Node%20Monitoring.md" target="_blank">Node Monitoring</a>
* <a href="04-%20Monitoring/01-%20Node%20Monitoring.md" target="_blank">Docker Monitoring</a>
* <a href="04-%20Monitoring/02-%20Syslog.md" target="_blank">Syslog</a>

## Dummy Data 

We provide an MQTT connection to an array of different data sets. For details visit <a href="07-%20Data%20Ingestion.md" target="_blank">Data Ingestion</a>
or <a href="../13-%20Support%20&%20Troubleshooting/05-%20Data%20Generator.md" target="_blank">Live Data Generator</a> to run locally. 