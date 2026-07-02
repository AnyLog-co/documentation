---
title: Data Ingestion (Southbound)
description: Overview of southbound data ingestion in AnyLog — connectors, mapping, file pipeline, and prerequisites.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlinks fixed
--> 


AnyLog receives data from edge devices, sensors, and applications through a set of **southbound connectors**. All connectors ultimately produce JSON files that flow through a common pipeline: Watch Directory → Operator → Local Database.

This page covers the pipeline, prerequisites, and mapping. For connector-specific configuration see the individual pages linked below.

---

## The ingestion pipeline

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

## Prerequisites before ingesting data

Before data can be ingested, the following services must be running:

| Service | Why |
|---|---|
| **TCP** | Node must be a network member |
| **REST** or **Message Broker** | Required for the connector receiving the data |
| **Streamer** | Required when using any streaming/buffered connector |
| **Operator** | Processes files and writes to the database |
| **Blockchain Sync** | Needed to resolve cluster and schema policies |

Minimal example for a streaming setup:
```anylog
run tcp server where external_ip = !ip and external_port = !anylog_server_port and threads = 6
run rest server where external_ip = !ip and external_port = !anylog_rest_port and timeout = 20
run streamer
run operator where create_table = true and update_tsd_info = true and archive_json = true and master_node = !master_node and policy = !operator_policy
run blockchain sync where source = master and time = 30 seconds and dest = file and connection = !master_node
```

---

## Connectors

| Connector | How data arrives | Page |
|---|---|---|
| **REST PUT/POST** | HTTP PUT or POST directly to the node | [Data Ingestion](/docs/managing-data-southbound/data-ingestion/) |
| **MQTT (msg client)** | Subscribe to external MQTT broker | [Data Ingestion](/docs/managing-data-southbound/data-ingestion/) |
| **Local Broker** | Node acts as the MQTT broker | [Background Services](/docs/network-services/background-services/#message-broker-service-local) |
| **Kafka** | Subscribe to Kafka topic | [Background Services](/docs/network-services/background-services/#kafka-consumer) |
| **gRPC** | Subscribe to gRPC stream | [gRPC](/docs/managing-data-southbound/grpc/) |
| **OPC-UA / PLC** | Active pull from industrial PLCs | [OPC-UA](/docs/managing-data-southbound/opcua/) |
| **EtherNet/IP** | Active pull from EtherNet/IP devices | [EtherNet/IP](/docs/managing-data-southbound/etherip/) |
| **Modbus TCP** | Active pull from Modbus TCP devices | [Modbus TCP](/docs/managing-data-southbound/modbus/) |
| **Syslog** | Receive syslog messages | [Syslog](/docs/managing-data-southbound/syslog/) |
| **Node-RED** | Via Node-RED flow (REST/MQTT) | [Node-RED](/docs/managing-data-southbound/node-red/) |
| **EdgeX** | Via EdgeX southbound framework | [EdgeX](/docs/managing-data-southbound/edgex/) |
| **Video** | Video stream ingestion | [Video Streaming](/docs/managing-data-southbound/video-streaming/) |


---

## Knowing your topics and schemas

Before connecting a data source you need to know:

1. **The broker / endpoint** — IP:Port of the MQTT broker, Kafka cluster, or REST endpoint
2. **The topic** — the MQTT topic name, Kafka topic, or URL path data is published to
3. **The message structure** — the JSON keys in the incoming message
4. **The target database and table** — where the data will be stored in AnyLog
5. **The column mapping** — which JSON keys map to which table columns

Example MQTT message:
```json
{"timestamp": "2024-01-01T12:00:00Z", "device": "sensor-01", "temperature": 23.5}
```

Corresponding `run msg client` mapping:
```anylog
<run msg client where
  broker = mqtt.mycompany.com and port = 1883 and
  topic = (
    name = sensors and
    dbms = my_data and
    table = temperature_readings and
    column.timestamp.timestamp = "bring [timestamp]" and
    column.device_name.str = "bring [device]" and
    column.value.float = "bring [temperature]"
  )>
```

---

## Mapping data to tables

AnyLog maps incoming JSON to table rows using either **inline column mapping** (in `run msg client`) or a **mapping policy** stored on the blockchain.

### Inline mapping (in the connector command)

Specify `column.[column-name].[data-type] = "bring [json-key]"` directly in the run command:

```anylog
column.timestamp.timestamp = "bring [timestamp]"
column.device_name.str = "bring [device]"
column.value.float = "bring [reading]"
column.status.str = "bring [status] default = active"
```

Supported data types: `str`, `int`, `float`, `timestamp`, `bool`

Use `default = [value]` for fields that may be absent in the message.

### Mapping policy

For complex or reusable mappings, store the mapping as a policy on the blockchain. The Operator references the policy ID when processing files.

```json
{
  "mapping": {
    "name": "sensor-mapping",
    "dbms": "my_data",
    "table": "ping_sensor",
    "schema": {
      "timestamp": {"type": "timestamp", "bring": "[timestamp]"},
      "device_name": {"type": "string", "bring": "[device]"},
      "value": {"type": "float", "bring": "[reading]"}
    }
  }
}
```

Publish and reference:
```anylog
blockchain insert where policy = !mapping_policy and local = true and master = !master_node
run operator where policy = !operator_policy and mapping = [mapping-policy-id] and ...
```

---

## The JSON file naming convention

When a connector produces a JSON file for the Operator, the file name encodes metadata that determines how it is processed:

```
[dbms-name].[table-name].[timestamp].[sequence].[mapping-id].json
```

Example:
```
my_data.ping_sensor.2024-01-01T12:00:00.000001.0.json
```

- `dbms-name` — the target logical database
- `table-name` — the target table
- `timestamp` — UTC timestamp of the first event in the file
- `sequence` — sequence number for ordering
- `mapping-id` — (optional) ID of the mapping policy to apply

---

## Streaming thresholds

When data arrives through a streaming connector (MQTT, gRPC, etc.), events are held in memory buffers and flushed to JSON files based on thresholds. The **Streamer** process enforces these thresholds.

View current thresholds:
```anylog
get streaming
```

Set thresholds:
```anylog
set buffer threshold where time = 60 seconds and volume = 10000
set buffer threshold where write_immediate = true    # no buffering, immediate write
```

Default: 60 seconds or 10,000 bytes, whichever comes first.

---

## The bring command (JSON data transformation)

The `bring` command extracts values from JSON structures. It is used both in column mapping and in blockchain queries.

Basic syntax:
```anylog
bring [key]                     # extract a top-level key
bring [outer-key][inner-key]    # nested key
bring [key] default = [value]   # with a default if key is absent
bring [key1] separator = ,      # concatenate multiple values
```

In a mapping context:
```anylog
column.value.float = "bring [readings][temperature]"
column.label.str = "bring [meta][device] default = unknown"
```

In a blockchain query context:
```anylog
blockchain get operator bring [name] [ip]:[port]
from !policies bring [name] [company]
```

---

## File pipeline monitoring

```anylog
get operator                    # ingestion status
get operator inserts            # insert counts per table
get operator summary            # summary of processed files
get streaming                   # buffer status and thresholds
get msg clients                 # active MQTT/Kafka subscriptions
```

Monitor the watch directory:
```anylog
get !watch_dir                  # path to the watch directory
get !bkup_dir                   # path to the backup directory
get !err_dir                    # path to the error directory
```