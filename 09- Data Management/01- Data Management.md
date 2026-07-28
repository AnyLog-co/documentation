---
title: "Data Management"
description: "Introduction to how AnyLog handles data: the distinction between metadata and actual data, how this section relates to Southbound/Northbound services, and the two-part data process (ingestion and query)."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon | Simplified both diagrams to short labels now that the numbered steps above each one spell out the detail in prose — the diagrams were repeating full sentences verbatim, which was pure duplication. Fixed step 3 of Part 1, which said the buffer exists "in order to continuously write to the database" — backwards; the buffer exists to avoid that, per the doc's own diagram. Fixed subject-verb agreement (singular "query node" throughout Part 2, "resides", "AnyLog then processes"); clarified the partition-pruning conditional in Part 2 step 3; typo fixes (node-RED → Node-RED, "wiht" → "with", doubled "the the") | |
 | 2026-07-27 | Ori Shadmon | Restructured Part 1's diagram as an actual fork/merge — the built-in and third-party ingestion paths are alternatives, not a sequence, and the old linear layout made it look like data passed through both one after another | |
 | 2026-07-27 | Ori Shadmon | Reframed the Southbound/Northbound relationship: this section isn't an "extension" of either, it's the internal layer between them (Southbound = data in, Northbound = data out, this section = how AnyLog itself writes/reads underneath) | |
 | 2026-07-27 | Ori Shadmon | Reframed "two types of data" so it doesn't contradict the third category (model/inference data) described right after it; fixed the `Extend Services` link (text said "Extend Services" but the path pointed at the sibling `09- Data Management` folder instead of `11- Extended Services`); fixed `COPY INTO` → Postgres's actual `COPY ... FROM` syntax; added frontmatter/H1 (missing entirely); typo fixes | |
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

1. A PLC or another device generates data and publishes it out.
2. Either a direct [southbound connection](../04-%20Southbound%20Interfaces) built into AnyLog, or a third-party
   connector (e.g. Node-RED), accepts the data from the PLC device or sensor. If the data is first passed through
   a third-party application, that application then forwards the data into AnyLog — usually via MQTT or REST.
3. To avoid continuously writing to the database, incoming content resides in a configurable buffer.
4. Once the buffer is full, AnyLog then processes the data into the appropriate databases (assuming they are
   already connected) and tables.

```
PLC / Device-Sensor
        |
        +-------------------+
        |                   |
        v                   v
  Built-in Southbound   Third-Party Connector
      Connector             (e.g. Node-RED)
        |                   |
        |                   v
        |            Forwarded via MQTT/REST
        |                   |
        +---------+---------+
                   |
                   v
           Buffer (batches writes)
                   |
                   v
          JSON -> SQL Inserts
        (+ blockchain policies)
                   |
                   v
         Create Table (if needed)
                   |
                   v
         Insert Data (SQLite INSERT /
            PSQL COPY ... FROM)
```

**Part 2**: Query the data across the network — for simplicity the discussion assumes the query is done via a
REST / API call, but the same logic applies with `run client`.

1. A user or an application executes a SQL request against the query node.
2. Using the blockchain — specifically `get data nodes` — the query node determines where the data resides and
   sends the request to the appropriate operator node(s).
3. On the operator node(s), a query extracting the raw content needed to satisfy the request runs against the
   correct partitioned tables: if the query includes a `WHERE timestamp` filter, only the relevant partitions are
   scanned; otherwise, all partitions are scanned.
4. The results from the operator node(s) are then aggregated into a single (temporary) table.
5. The query node re-runs the user's original request against this generated results table.
6. The appropriate content is returned to the user or application.

```
User / Application
   SQL query -> Query Node
          |
          v
  Locate data (blockchain: `get data nodes`)
          |
          v
   Query Operator Node(s)
  (partition-pruned if WHERE timestamp)
          |
          v
  Aggregate results (temp table)
          |
          v
  Re-run query on aggregated table
          |
          v
   Return result to user / application
```