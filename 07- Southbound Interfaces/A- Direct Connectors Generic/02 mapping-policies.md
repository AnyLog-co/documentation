---
title: MQTT & Message Broker
description: Connecting to an external MQTT broker, running AnyLog as a message broker, and ingesting via run msg client with or without a mapping policy
layout: page
---
### 📜 Change Log
 **Date**   | **Name**       | **Change**    | **Version** |
 |------------|----------------|---------------|----------|
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-04-18 |                | Switched examples to REST ingestion; added curl publish examples  |  |
 | 2026-04-18 |                | file creation covers policy structure, inline vs policy mapping, wildcard schemas, split and combined table patterns|  |

<<<<<<<< HEAD:07- Southbound Interfaces/A- Direct Connectors Generic/message-broker.md
<!--
## Changelog
- 2026-04-18 | (as mapping-policies.md) Created document; covers policy structure, inline vs policy mapping,
              wildcard schemas, split and combined table patterns
- 2026-04-18 | (as mapping-policies.md) Switched examples to REST ingestion; added curl publish examples
- 2026-07-14 | Moved from mapping-policies.md to mqtt.md. Added: connecting to an external MQTT broker,
              running AnyLog as a message broker (`run message broker`, MQTT or Kafka), and a no-mapping
              (`dynamic=true`) ingestion mode alongside the existing mapping-based content, which now sits as
              one section of this broader page rather than the whole page.
-->
========
>>>>>>>> origin/pre-develop:07- Southbound Interfaces/A- Direct Connectors Generic/02 mapping-policies.md

# MQTT & Message Broker

AnyLog has two distinct roles it can play with respect to a broker, and it's worth keeping them separate before
getting into ingestion details:

- **`run msg client`** — AnyLog acts as a **client**, connecting outward to a broker (an external MQTT broker, a
  Kafka topic, a REST endpoint, or AnyLog's own local broker) and consuming/ingesting whatever arrives on a topic.
- **`run message broker`** — AnyLog acts as the **broker itself**, opening a port that other systems publish
  into — either as an MQTT broker or a Kafka broker — rather than AnyLog reaching out to one that already exists
  elsewhere.

| Command | Role |
|---|---|
| `run msg client where broker=rest and user-agent=anylog and ...` | REST POST ingestion — AnyLog receives data pushed directly via HTTP POST (see [Using REST](../Using%20REST.md)) |
| `run msg client where broker=<external-host> and port=<port> and ...` | Subscribe to an external MQTT broker |
| `run msg client where broker=local and ...` | Subscribe to AnyLog's own local broker, started via `run message broker` |
| `run kafka consumer where broker=local and ...` | Consume from AnyLog's own local broker acting as a Kafka broker |
| `get msg client` | Shows message counts, subscribed topics, and column/policy mapping per topic |

---

## Connecting to an External MQTT Broker

To ingest from an MQTT broker you don't control — a 3rd-party broker, or one run elsewhere in your own
infrastructure — point `run msg client` at its host and port directly:

```anylog
<run msg client where
    broker = 172.104.228.251 and port = 1883 and
    user = anyloguser and password = mqtt4AnyLog! and
    master_node = !ledger_conn and log = false and
    topic = (
        name = "Enterprise C/tff/PCV7X/#" and
        dbms = !default_dbms and
        dynamic = true
    )>
```

`broker`/`port` are the external broker's address; `user`/`password` are only needed if that broker requires
authentication. Everything else about the `topic` clause — mapping, dynamic ingestion, UNS registration — works
the same regardless of whether the broker is external or local; see
[Ingesting with `run msg client`](#ingesting-with-run-msg-client) below for those options, and
[Unified Namespace](../../13-%20UNS%20%28Unified%20Name%20Spaces%29/UNS.md) for what `dynamic=true` does with the
topic path.

---

## Running AnyLog as a Message Broker (`run message broker`)

Rather than connecting out to a broker that already exists, a node can open its own port and act as the broker
directly — either as an MQTT broker or a Kafka broker — so that other systems (devices, gateways, other AnyLog
nodes) publish *into* this node instead of AnyLog reaching out to them.

```anylog
run message broker where ...
```

Once running, a `run msg client` (or `run kafka consumer`, for the Kafka case) on the same node — or a different
one — can subscribe to it using `broker = local` instead of an external host:

```anylog
run msg client where broker=local and ...        # subscribe via MQTT to this node's own broker
run kafka consumer where broker=local and ...     # subscribe via Kafka to this node's own broker
```

> The full parameter reference for `run message broker` (port, protocol selection between MQTT/Kafka,
> authentication options) isn't captured in this page yet — worth filling in from the command's actual `help`
> output or source before treating the snippet above as complete.

---

## Ingesting with `run msg client`

Once a client is connected — to an external broker, a local broker, Kafka, or REST — there are two ways to tell
AnyLog what to do with each incoming message: no mapping at all, or an explicit mapping (inline or policy-based).

### No Mapping (`dynamic=true`)

If each message carries a single scalar value, `dynamic=true` needs no schema at all — AnyLog derives both the
table name and the UNS namespace directly from the topic path:

```anylog
<run msg client where
    broker = 192.168.1.88 and port = 1883 and
    master_node = !ledger_conn and
    topic = (
        name = M2/PL1/# and
        dbms = new_company and
        dynamic = true
    )>
```

This is the right mode for simple scalar telemetry where you don't need control over column names or table
layout — see [Unified Namespace](../../13-%20UNS%20%28Unified%20Name%20Spaces%29/UNS.md) for the full walkthrough
of how the topic path becomes the table/namespace structure, and
[Dynamic Ingestion with Custom UNS](../../13-%20UNS%20%28Unified%20Name%20Spaces%29/UNS-dynamic-custom-example.md)
for the case where messages carry full JSON rather than a bare scalar, still under `dynamic=true`.

### With Mapping (Inline or Policy-Based)

When you need explicit control over column names, types, table names, or which JSON fields go where, define a
mapping instead. There are two ways to do this.

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
production integrations — policies can be updated on the blockchain without restarting the message client, and
the same policy can be reused across multiple topics or nodes.

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

The rest of this page covers policy-based mapping in detail: policy structure, wildcard schemas, and worked
examples.

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