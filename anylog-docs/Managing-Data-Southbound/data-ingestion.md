---
title: Data Ingestion
description: How to get data into AnyLog using REST, MQTT, Kafka, OPC-UA, and gRPC.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlinks
--> 

## Southbound services overview

AnyLog supports multiple data ingestion methods. All incoming data — regardless of source — passes through a mapping layer that translates it into the correct database structure, making it immediately queryable.

| Method | Description |
|---|---|
| **REST PUT** | AnyLog maps the request directly to a database, table, and key/value pairs |
| **REST POST** | AnyLog consumes messages and applies mapping to database tables |
| **Remote Message Broker** | Kafka or MQTT — AnyLog subscribes and applies mapping to DB tables |
| **Local Message Broker** | AnyLog acts as the MQTT broker itself |
| **OPC-UA / EtherIP** | Values stored in timestamp/value format for time-series applications |
| **gRPC** | Used for KubeArmor, monitoring tools, and video/inference streaming |

AnyLog supports a **Universal Namespace (UNS)** — either built-in or customer-defined — providing consistent variable names across all nodes. Note that EdgeLake does not include a built-in UNS.

---

## Data path

Data reaches operator nodes either directly (via a supported southbound service) or through an intermediary:

```
[ Sensor / Device ]
        │
  ┌─────┴──────────────────────────────────┐
  │ Direct                                  │ Via Publisher
  ▼                                         ▼
[ Operator Node ] ←──── [ AnyLog Publisher Node ]
                                  ▲
                         (fans data across
                          multiple operators)
```

A **publisher node** is an optional AnyLog edge node that accepts data from sensors and automatically routes it to the appropriate operator nodes. It is used when:
- Data from a single ingestion point needs to be split across different clusters
- The sensor or device cannot directly reach the operator nodes due to network topology

In parallel, a **query node** can always be used to retrieve data and metadata from operator nodes for use by customer applications.

---

## REST PUT

The simplest ingestion method. AnyLog maps the HTTP headers to a target database and table, and the body is parsed as key/value pairs.

```bash
curl -X PUT "http://127.0.0.1:32149" \
  -H "type: json" \
  -H "dbms: mydb" \
  -H "table: rand_data" \
  -H "mode: streaming" \
  -H "Content-Type: text/plain" \
  --data '[
    {"timestamp":"2026-03-12T10:00:00Z","value":12.5},
    {"timestamp":"2026-03-12T10:00:01Z","value":18.2},
    {"timestamp":"2026-03-12T10:00:02Z","value":9.7}
  ]'
```

Expected response: `{"AnyLog.status":"Success", "AnyLog.hash": "0"}`

---

## REST POST

Used when data is published through the message client mapping layer (see <a href="{{ '/docs/msg-client//' | relative_url }}">`run msg client`</a> below). The POST goes to the operator's REST port with a topic header instead of direct table/database headers.

```bash
curl -X POST "http://127.0.0.1:32149" \
  -H "command: data" \
  -H "topic: my-data" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: text/plain" \
  -d '[
    {"dbms":"mydb","table":"rand_data","timestamp":"2026-04-03 18:31:10.125431","value":12.48},
    {"dbms":"mydb","table":"rand_data","timestamp":"2026-04-03 18:31:10.625812","value":87.29}
  ]'
```

---

## The message broker / client relationship

When data arrives via MQTT, Kafka, or REST POST, AnyLog uses two components:

**Part 1 — Message broker:** Decides where messages come from.
- **Local broker:** AnyLog itself acts as the MQTT broker. The node must have the broker service enabled.
- **Remote broker:** An external broker (e.g. Mosquitto, Kafka). AnyLog connects as a consumer.

**Part 2 — Message client (`run msg client`):** Connects to the broker and maps incoming content to the correct database and table structure.

> Unlike generic message brokers, AnyLog instances cannot connect to one another's MQTT broker to pull messages. Only the message client service bridges that gap.

---

## `run msg client`

The `run msg client` command starts the mapping service that subscribes to a topic and routes data into storage.

### Parameter reference

| Section | Parameter | Description |
|---|---|---|
| **Connection** | `broker` | IP address, `local` (AnyLog broker), or `rest` (for REST POST) |
| | `port` | Port associated with the broker |
| **Auth** *(optional)* | `user` | Username for remote broker |
| | `password` | Password for the user above |
| | `user-agent` | Set to `anylog` — required only for REST POST |
| | `log` | `true` / `false` — write events to screen |
| **Routing** | `name` | Broker topic to subscribe to |
| | `dbms` | Target logical database — hardcoded or from payload |
| | `table` | Target table — hardcoded or from payload |
| **Schema** | `column.timestamp.timestamp` | Use `"bring [field]"` to pull from payload, or `now()` for ingestion time |
| | `column.[name]` | Any non-timestamp column: set `type` and `value` to map from a payload key |

### Full syntax

```
<run msg client where
  broker    = [IP | local | rest] and
  port      = [PORT] and
  user      = [USERNAME] and       # optional
  password  = [PASSWORD] and       # optional
  log       = [true | false] and
  user-agent= anylog and           # REST POST only
  topic = (
    name    = [TOPIC] and
    dbms    = [DB NAME] and
    table   = [TABLE NAME] and
    column.timestamp.timestamp = "bring [field]" | now() and
    column.[col_name] = (
      type  = [float | int | bool | str] and
      value = "bring [PAYLOAD KEY]"
    )
  )>
```

### Example — local MQTT broker

```
<run msg client where
  broker = local and
  port   = 32150 and
  log    = false and
  topic  = (
    name  = my-data and
    dbms  = mydb and
    table = rand_data and
    column.timestamp.timestamp = "bring [timestamp]" and
    column.value = (
      type  = float and
      value = "bring [value]"
    )
  )>
```

### Example — REST POST client

```
<run msg client where
  broker     = rest and
  port       = 32149 and
  log        = false and
  user-agent = anylog and
  topic      = (
    name  = my-data and
    dbms  = mydb and
    table = rand_data and
    column.timestamp.timestamp = "bring [timestamp]" and
    column.value = (
      type  = float and
      value = "bring [value]"
    )
  )>
```

---

## Using a mapping policy

For more complex scenarios, the same mapping can be expressed as a **policy** stored on the blockchain. Policies offer:

- Easier reusability across nodes
- Better data type support (epoch timestamps, blob integration)
- Ability to split data across multiple tables

### Define the policy

```
<new_policy = {
  "mapping": {
    "id": "my-policy",
    "dbms": "mydb",
    "table": "rand_data",
    "schema": {
      "timestamp": {
        "type": "timestamp",
        "bring": "[timestamp]",
        "default": "now()"
      },
      "value": {
        "type": "float",
        "value": "[value]"
      }
    }
  }
}>
```

### Publish the policy to the blockchain

```
<blockchain insert where
  policy = !new_policy and
  local  = true and
  master = !ledger_conn>
```

### Reference the policy in `run msg client`

```
<run msg client where
  broker = local and
  log    = false and
  topic  = (
    name   = my-data and
    policy = my-policy
  )>
```

---

## Validating ingestion

### Check the message client is running

```bash
curl -X GET 127.0.0.1:32149 \
  -H "command: get msg client" \
  -H "User-Agent: AnyLog/1.23"
```

### Check streaming status

```bash
curl -X GET 127.0.0.1:32149 \
  -H "command: streaming" \
  -H "User-Agent: AnyLog/1.23"
```

### Query data back out

```bash
curl -X GET 127.0.0.1:32349 \
  -H "command: sql mydb format=table SELECT timestamp, value FROM rand_data WHERE period(minute, 1, now(), timestamp)" \
  -H "User-Agent: AnyLog/1.23" \
  -H "destination: network"
```

---

## Live data generator

AnyLog provides a shared MQTT broker with continuously published sample data across several real-world use cases. See 
the <a href="{{ '/docs/Managing-Data-Southbound/live-data-generator/' | relative_url }}">Live Data Generator</a> page 
for connection details, the full script directory, and how to run each generator.

---

## Sample scripts

Each script below is a ready-to-run AnyLog script (`.al` file) that sets up a `run msg client` to subscribe to the live broker for a specific use case. Where relevant, a companion data generator script is linked.

### Basic — random timestamp/value pairs

The simplest example. Subscribes to the `anylog-demo` topic and maps `timestamp` and `value` fields into your default database.

- **Script:** [basic_msg_client.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/sample-scripts/basic_msg_client.al) — configurable via node env vars (`ENABLE_MQTT=true`)
- **Live generator:** [rand_data.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/data-generator/rand_data.al)

Sample data published:
```json
{"timestamp": "2026-04-05T05:23:49.997386", "value": 0.186, "dbms": "mydb", "table": "rand_data"}
```

```anylog
<run msg client where
    broker = 172.104.228.251 and port = 1883 and
    user = anyloguser and password = mqtt4AnyLog! and
    log = false and topic = (
        name = anylog-demo and
        dbms = !default_dbms and
        table = "bring [table]" and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value = (type = float and value = "bring [value]")
    )>
```

---

### Oil rig drilling data — policy-based, multiple topics

Ingests real-time drilling metrics (depth, ROP, WOB, torque, pressure, flow rate, mud weight) from multiple rig topics. Uses a **mapping policy** for schema definition, making it easy to fan across many topics with a single `run msg client`.

- **Script:** [edgex.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/sample-scripts/edgex.al) (policy-based msg client)
- **Live generator:** [oil_rig_data.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/data-generator/oil_rig_data.al)
- **Mapping policy:** [rig_rig-data.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/data-generator/mapping/rig_rig-data.al)

Sample data:
```json
{
  "rig_id": "RIG-TX-001", "rig_name": "Permian Star", "location": "West Texas",
  "activity": "circulating", "measured_depth": 12518.66, "rop": 0.0, "wob": 0.0,
  "rpm": 69.94, "torque": 8729.09, "standpipe_pressure": 3012.69,
  "dbms": "timbergrove_rigs", "table": "rig_data"
}
```

```anylog
<run msg client where
    broker = 172.104.228.251 and port = 1883 and
    user = anyloguser and password = mqtt4AnyLog! and
    log = false and
    topic = (name = rig-data/rig-1 and policy = rig-data) and
    topic = (name = rig-data/rig-7 and policy = rig-data) and
    topic = (name = rig-data/rig-12 and policy = rig-data) and
    topic = (name = rig-data/rig-23 and policy = rig-data)>
```

---

### Telegraf — node monitoring data

Ingests system metrics (CPU, memory, network, swap) collected by [Telegraf](https://www.influxdata.com/time-series-platform/telegraf/). Telegraf agents installed on your machines publish metrics to the broker; AnyLog maps them into time-series tables.

The mapping policy uses a wildcard `"*"` schema to dynamically capture all fields from both `fields` and `tags` sections — ideal when the exact field set varies by metric type.

- **Script:** [telegraf.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/sample-scripts/telegraf.al)

Sample data published by Telegraf:
```json
{"metrics": [
  {"fields": {"used_percent": 58.28, "available": 7166590976},
   "name": "mem", "tags": {"host": "my-server"}, "timestamp": 1715018940},
  {"fields": {"usage_idle": 89.92, "usage_user": 7.36},
   "name": "cpu", "tags": {"cpu": "cpu0", "host": "my-server"}, "timestamp": 1715018940}
]}
```

**Telegraf output plugin config** (in `telegraf.conf`):
```toml
[[outputs.mqtt]]
  servers = ["tcp://172.104.228.251:1883"]
  topic = "telegraf-data"
  username = "anyloguser"
  password = "mqtt4AnyLog!"
  data_format = "json"
```

---

### Wind turbine — multiple policies per topic

Ingests wind turbine operational data (wind speed, RPM, power output, pitch, pressure, humidity) across multiple turbines. Each topic maps to several policies that route different metric groups into separate tables.

- **Live generator:** [wind_turbine_data.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/data-generator/wind_turbine_data.al)

Sample data:
```json
{
  "turbine_id": 6, "wind_avg": 6.7, "wind_max": 10.8, "rpm_avg": 0.85,
  "power_avg": -8, "pitch_avg": 56.7, "ambient_avg": 244,
  "dbms": "wind_turbine", "table": "wind_turbine"
}
```

```anylog
<run msg client where
    broker = 172.104.228.251 and port = 1883 and
    user = anyloguser and password = mqtt4AnyLog! and
    log = false and
    topic = (
        name = wind-turbine/turbine-1 and
        policy = available-power and policy = blade-pitch and
        policy = energy and policy = reactive-power
    ) and
    topic = (
        name = wind-turbine/turbine-2 and
        policy = available-power and policy = blade-pitch and
        policy = energy and policy = reactive-power
    )>
```

---

### Electric vessel — complex multi-table schema

Ingests high-density battery and charger telemetry from electric boats (DLT/DLB sides). Each topic carries multiple device types, each mapped to its own table via separate policies.

- **Live generator:** [vessel_data.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/data-generator/vessel_data.al)

Tables populated: `BATTERY-PACK-DEVICE-LOGS`, `BATTERY-PACK-LOGS`, `CHARGER-DEVICE-LOGS`, `CHARGER-LOGS`, `VESSEL-POWER-LOGS`, `VESSEL-STATE-LOGS`

```anylog
<run msg client where
    broker = 172.104.228.251 and port = 1883 and
    user = anyloguser and password = mqtt4AnyLog! and
    log = false and
    topic = (
        name = vessel-data/DLT and
        policy = BATTERY-PACK-DEVICE-LOGS and policy = BATTERY-PACK-LOGS and
        policy = CHARGER-DEVICE-LOGS and policy = CHARGER-LOGS and
        policy = VESSEL-POWER-LOGS and policy = VESSEL-STATE-LOGS
    ) and
    topic = (
        name = vessel-data/DLB and
        policy = BATTERY-PACK-DEVICE-LOGS and policy = BATTERY-PACK-LOGS and
        policy = CHARGER-DEVICE-LOGS and policy = CHARGER-LOGS and
        policy = VESSEL-POWER-LOGS and policy = VESSEL-STATE-LOGS
    )>
```

---

### Drone telemetry — REST POST with mapping policy

Ingests drone swarm telemetry (position, altitude, heading, speed, battery, leader estimation) via REST POST. Uses a mapping policy to define the schema, with `dbms` and `table` derived dynamically from the payload.

- **Live generator:** [drone_telemetry.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/data-generator/drone_telemetry.al)

Sample data:
```json
{
  "drone_id": "DRONE-001", "role": "follower", "leader_id": "DRONE-000",
  "latitude": 37.774, "longitude": -122.419, "altitude_m": 120.5,
  "speed_mps": 8.2, "battery_pct": 74.3, "status": "active",
  "dbms": "drone_ops", "table": "telemetry"
}
```

```anylog
<run msg client where
    broker = rest and
    log = false and
    user-agent = anylog and
    topic = (
        name = drone-telemetry and
        policy = drone-telemetry
    )>
```

---

## Kafka

The `run kafka consumer` command follows the same topic/mapping pattern as `run msg client`:

- **Script:** [basic_kafka_client.al](https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/sample-scripts/basic_kafka_client.al)

```anylog
<run kafka consumer where
    ip = [kafka-broker-ip] and port = 9092 and
    reset = earliest and
    topic = (
        name = my-topic and
        dbms = mydb and
        table = sensor_data and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value = (type = float and value = "bring [value]")
    )>
```