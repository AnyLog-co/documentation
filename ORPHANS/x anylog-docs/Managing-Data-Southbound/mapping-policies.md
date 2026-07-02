---
title: Mapping Policies
description: How to define mapping policies to store incoming JSON data into AnyLog tables
layout: page
---

<!--
## Changelog
- 2026-04-18 | Created document; covers policy structure, inline vs policy mapping, wildcard schemas, split and combined table patterns
- 2026-04-18 | Switched examples to REST ingestion; added curl publish examples
-->

When data arrives at an AnyLog node via REST, AnyLog needs to know how to interpret the incoming JSON — which 
database and table to write to, and how to extract and type-cast each field. This is defined in a **mapping policy**: 
a JSON structure stored in AnyLog's shared metadata layer and referenced by ID at ingestion time.

Mapping policies decouple the ingestion configuration from the data pipeline, making them reusable, version-controlled, 
and easier to manage across many devices or data sources.

---

## Inline vs. Policy-Based Mapping

There are two ways to tell AnyLog how to map incoming data.

**Inline mapping** embeds the schema directly in the `run msg client` command. This is convenient for simple, 
one-off cases but becomes unwieldy when field lists are long or schemas are shared across topics.

```anylog
<run msg client where
  broker = rest and
  user-agent = anylog and
  topic = (
    name = sensors and
    dbms = my_data and
    table = temperature_readings and
    column.timestamp.timestamp = "bring [timestamp]" and
    column.device_name.str = "bring [device]" and
    column.value.float = "bring [temperature]"
  )>
```

**Policy-based mapping** stores the schema separately and references it by ID. This is the preferred approach for 
production integrations — policies can be updated on the blockchain without restarting the message client, and the 
same policy can be reused across multiple topics or nodes.

```anylog
<run msg client where
  broker = rest and
  user-agent = anylog and
  max-time = 60 and
  topic = (
    name = sensors and
    policy = sensors
  )>
```

Data is then published to the node via MQTT or HTTP POST with the topic name passed in the request headers — see 
[Publishing Data](#publishing-data) below.

---

## Policy Structure

### Top-Level Keys

| Key | Required | Description |
|:---|:---:|:---|
| `id` | Yes | Unique policy identifier; used to reference the policy from `run msg client` |
| `dbms` | Yes | Target logical database name; supports AnyLog variables (e.g. `!default_dbms`) |
| `table` | Yes | Target table name; supports `bring` expressions for dynamic naming |
| `readings` | No | Key within the source JSON that holds a list of readings. Omit or leave empty for flat payloads; set to the list key (e.g. `"metrics"`) for nested reading arrays |
| `condition` | No | An `if` expression that must evaluate true for this policy to apply — used to route a single payload to different tables |
| `schema` | Yes | Column definitions and mapping instructions |

### Schema Column Keys

Each key in `schema` is a target column name. Its value describes how to populate that column:

| Key | Required | Description |
|:---|:---:|:---|
| `type` | Yes | Data type: `string`, `integer`, `float`, `decimal`, `timestamp`, `bool`, `varchar`, `char`, or `*` for dynamic inference |
| `bring` | No* | Expression or list of keys to extract from the source JSON |
| `default` | No* | Fallback value if `bring` returns nothing |
| `apply` | No | Transformation function applied after extraction (e.g. `epoch_to_datetime`) |
| `root` | No | When `true` and `readings` is set, extracts this field from the root JSON object rather than from each reading entry |
| `condition` | No | Per-column `if` expression; determines whether this column is populated for a given row |

> \* At least one of `bring` or `default` must be provided per column.

### Wildcard Schema (`*`)

When the incoming payload structure is not fully known ahead of time — or when different messages carry different 
field names — AnyLog supports a wildcard column entry using `"*"` as the column name and `"*"` as the type:

```json
"*": {
    "type": "*",
    "bring": ["field_a", "field_b"]
}
```

This tells AnyLog to extract all keys from the listed source objects, automatically create columns for each one, 
and infer the data type from the value. New fields in future messages are picked up without policy changes.

---

## Examples

The examples below use OPC-UA device readings published over REST. Each message represents a single tag read 
from a device:

**Successful read** — `value` is populated, `metadata` is empty:
```json
{
  "success": true, "datatype": "float", "timestamp": 1776294106000, "registerId": "a2",
  "value": 23.7, "deviceID": "d1", "tagName": "ns1_Device_Pressure", "deviceName": "opcua", 
  "description": "", "metadata": {}
}
```

**Failed read** — `value` is `null`, `metadata` contains the error:
```json
{
  "success": false, "datatype": "float", "timestamp": 1776294206000, "registerId": "b2",
  "value": null, "deviceID": "d1", "tagName": "ns1_Device_Pressure", "deviceName": "opcua", 
  "description": "", "metadata": {"error": "BadNodeIdUnknown"}
}
```

The table name is derived dynamically from `deviceName` and `deviceID` — device `d1` on `opcua` maps to a 
table named `opcua_d1`.

---

### Example 1: Split into Two Tables

This pattern separates successful readings from error records into two tables, keeping the readings table 
clean and queryable while preserving diagnostics separately.

**Step 1 — Register the readings policy:**

```anylog
data_policy_id = opcua-data

<data_policy = {"mapping": {
    "id": !data_policy_id,
    "dbms": !default_dbms,
    "table": "bring [deviceName] _ [deviceID]",
    "readings": "",
    "schema": {
        "timestamp": {
            "type": "timestamp",
            "default": "now()",
            "bring": "[timestamp]",
            "apply": "epoch_to_datetime"
        },
        "*": {
            "type": "*",
            "bring": ["success", "tagName", "value", "description"]
        }
    }
}}>

blockchain insert where policy=!data_policy and local=true and master=!ledger_conn
```

**Step 2 — Register the metadata policy** — captures error details alongside root-level fields:

```anylog
metadata_policy_id = opcua-metadata

<metadata_policy = {"mapping": {
    "id": !metadata_policy_id,
    "dbms": !default_dbms,
    "table": "bring [deviceName] _ [deviceID] _metadata",
    "readings": "metadata",
    "schema": {
        "timestamp": {
            "type": "timestamp",
            "default": "now()",
            "bring": "[timestamp]",
            "apply": "epoch_to_datetime",
            "root": true
        },
        "success": {
            "type": "bool",
            "default": null,
            "bring": "[success]",
            "root": true
        },
        "*": {
            "type": "*",
            "bring": ["*"]
        }
    }
}}>

blockchain insert where policy=!metadata_policy and local=true and master=!ledger_conn
```

> `"root": true` tells AnyLog to pull that field from the top-level JSON object even when `readings` points 
> to a nested structure. Without it, `timestamp` and `success` would not be found while iterating over 
> the `metadata` object.

**Step 3 — Start the message client**, associating both policies to the same topic:

```anylog
topic_name = opcua

<run msg client where
  broker = rest and
  user-agent = anylog and
  topic = (
    name = !topic_name and
    policy = !data_policy_id and
    policy = !metadata_policy_id
  )>
```

This produces two tables per device:

| Table | Contents |
|:---|:---|
| `opcua_d1` | Timestamp, tag name, value, success flag, description |
| `opcua_d1_metadata` | Timestamp, success flag, error details from the metadata object |

---

### Example 2: Combined into a Single Table

This pattern collapses readings and metadata into one table. Simpler to query, but mixes successful and 
failed reads in the same rows.

```anylog
policy_id = opcua-combined

<combined_policy = {"mapping": {
    "id": !policy_id,
    "dbms": !default_dbms,
    "table": "bring [deviceName] _ [deviceID]",
    "readings": "",
    "schema": {
        "timestamp": {
            "type": "timestamp",
            "default": "now()",
            "bring": "[timestamp]",
            "apply": "epoch_to_datetime"
        },
        "*": {
            "type": "*",
            "bring": ["success", "tagName", "value", "description"]
        },
        "metadata": {
            "type": "varchar",
            "bring": "[metadata]",
            "default": "{}"
        }
    }
}}>

blockchain insert where policy=!combined_policy and local=true and master=!ledger_conn
```

```anylog
<run msg client where
  broker = rest and
  user-agent = anylog and
  topic = (
    name = opcua and
    policy = !policy_id
  )>
```

The `metadata` object is stored as a `varchar` column — serialized JSON — keeping error details accessible 
without a join.

---

## Publishing Data

Data is sent to the AnyLog node via HTTP POST. The `topic` header maps the payload to the correct message 
client configuration, and `command: data` identifies this as an ingestion request.

```
POST http://<node-ip>:<rest-port>
Headers:
  command:       data
  topic:         <topic-name>
  User-Agent:    AnyLog/1.23
  Content-Type:  text/plain
```

### curl Examples

**Single successful reading:**
```bash
curl -X POST http://10.0.0.1:32149 \
  -H "command: data" \
  -H "topic: opcua" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: text/plain" \
  -d '{"success": true, "datatype": "float", "timestamp": 1776294106000, "registerId": "a2", "value": 23.7, "deviceID": "d1", "tagName": "ns1_Device_Pressure", "deviceName": "opcua", "description": "", "metadata": {}}'
```

**Single failed reading** (null value, error in metadata):
```bash
curl -X POST http://10.0.0.1:32149 \
  -H "command: data" \
  -H "topic: opcua" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: text/plain" \
  -d '{"success": false, "datatype": "float", "timestamp": 1776294206000, "registerId": "b2", "value": null, "deviceID": "d1", "tagName": "ns1_Device_Pressure", "deviceName": "opcua", "description": "", "metadata": {"error": "BadNodeIdUnknown"}}'
```

**Batch of readings** — mix of success and failure across devices:
```bash
curl -X POST http://10.0.0.1:32149 \
  -H "command: data" \
  -H "topic: opcua" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: text/plain" \
  -d '[
    {"success": true,  "datatype": "uint32",  "timestamp": 1776294105000, "registerId": "a1", "value": 12,   "deviceID": "d1", "tagName": "ns1_Device_Temperature", "deviceName": "opcua", "description": "", "metadata": {}},
    {"success": true,  "datatype": "float",   "timestamp": 1776294106000, "registerId": "a2", "value": 23.7, "deviceID": "d1", "tagName": "ns1_Device_Pressure",    "deviceName": "opcua", "description": "", "metadata": {}},
    {"success": false, "datatype": "boolean", "timestamp": 1776294207000, "registerId": "b3", "value": null, "deviceID": "d2", "tagName": "ns1_Device_Running",     "deviceName": "opcua", "description": "", "metadata": {"error": "ConnectionLost"}},
    {"success": false, "datatype": "int32",   "timestamp": 1776294208000, "registerId": "b4", "value": null, "deviceID": "d2", "tagName": "ns1_Device_ErrorCode",   "deviceName": "opcua", "description": "", "metadata": {"error": "Timeout"}}
  ]'
```

> Replace `10.0.0.1:32149` with your operator node's IP and REST port.

---

## Choosing Between Patterns

| | Split (2 tables) | Combined (1 table) |
|:---|:---:|:---:|
| Readings table stays clean | ✓ | ✗ |
| Error details preserved | ✓ | ✓ |
| Simpler queries | ✗ | ✓ |
| Metadata queryable as columns | ✓ | ✗ |
| Best for high read volumes | ✓ | ✗ |

Use the **split pattern** when failed reads are frequent or when you want to query readings and diagnostics 
independently. Use the **combined pattern** when failures are rare and query simplicity matters more.

---

## Validation

| Command | What to look for |
|:---|:---|
| `get msg client` | Messages received per topic; policy association confirmed |
| `get streaming` | Tables being created; column names inferred from wildcard |
| `get operator` | Rows written to the database |

```anylog
# All readings for device d1
run client () sql !default_dbms format=table "select * from opcua_d1 limit 10"

# Failed reads only
run client () sql !default_dbms format=table "select * from opcua_d1 where success=false limit 10"

# Metadata errors
run client () sql !default_dbms format=table "select * from opcua_d1_metadata limit 10"
```