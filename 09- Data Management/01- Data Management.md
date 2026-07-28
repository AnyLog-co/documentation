---
title: "Data Management"
description: "Introduction to how AnyLog handles data: the distinction between metadata and actual data, how this section relates to Southbound/Northbound services, and the two-part data process (ingestion and query)."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon | Reframed the Southbound/Northbound relationship: this section isn't an "extension" of either, it's the internal layer between them (Southbound = data in, Northbound = data out, this section = how AnyLog itself writes/reads underneath) | |
 | 2026-07-27 | Ori Shadmon | Reframed "two types of data" so it doesn't contradict the third category (model/inference data) described right after it; fixed the `Extend Services` link (text said "Extend Services" but the path pointed at the sibling `09- Data Management` folder instead of `09- Extended Services`); fixed `COPY INTO` → Postgres's actual `COPY ... FROM` syntax; added frontmatter/H1 (missing entirely); typo fixes | |
--->

# Data Management

There are two types of data within AnyLog: **metadata**, which is covered in
[Blockchain](../08-%20Blockchain%20&%20Metadata/01-%20Blockchain.md), and **actual data** — the content stored on an
operator node, whether it's sensor, device, monitoring, or other forms of blob data.

Actual data itself splits further: device/sensor/monitoring data is covered in this section, while model and
inference data is covered under [Extended Services](../09-%20Extended%20Services), which deals with MCP, LLMs, and
other ML/AI non-device data.

[Southbound](../04-%20Southbound%20Interfaces) services are how data gets **into** AnyLog (sensors,
devices, MQTT, etc.), and [Northbound](../05-%20Northbound%20Connectors) services are how data gets **out** of
AnyLog (BI tools and other consumers). This section sits between the two: it's what AnyLog does internally, once
data has arrived and before anything queries it back out — think of AnyLog as the application, and this section as
how that application actually writes to and reads from the database underneath it.

## Topics Covered

* [Database Connectors]()
* [Data Management](), whether it's HA, validation of what came in, or simply understanding how data works
* [Data Partitioning]()
* [Data Aggregation]()
* [Querying Data]()

## The Data Process

Data processing has 2 parts.

**Part 1**: Data coming from a device (PLC) and stored into AnyLog

```
PLC / Device-Sensor
        |
        +-------------------------+
        |                         |
        v                         v
Published directly into    Published into a third-party
AnyLog via built-in        connector (like Node-RED)
southbound connector               |
        |                          v
        |                   Forwarded into AnyLog,
        |                   usually via REST or MQTT
        |                          |
        +------------+-------------+
                      |
                      v
AnyLog's built-in buffer batches data (writes in batches rather than
continuously writing files to the database)
                      |
                      v
Convert JSON into SQL inserts (if needed, create blockchain policies for
table and cluster metadata)
                      |
                      v
Execute create table (if needed) for the physical table and/or partitioning
                      |
                      v
Execute insert of the data - in SQLite it's a straight _INSERT_, in PSQL
it's a CSV _COPY ... FROM_
```

**Part 2**: Query the data across the network

```
User or Application executes a SQL query against the query node (usually via REST)
        |
        v
The network figures out where the data resides (this is the `run client`)
        |
        v
Each operator generates a result based on the query
        |
        v
The content is merged into a single table on the query node
        |
        v
The user / application sees a unified result with data from multiple sources as though it's all one node (i.e. the cloud)
```