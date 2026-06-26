---
title: Telegraf
description: How to publish Telegraf metrics into AnyLog via MQTT or REST
layout: page
---

<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-18 | Simplified to Telegraf setup only; mapping details moved to mapping-policies.md
- 2026-04-21 | Remove title (#Telegraf) 
- 2026-04-25 | hyperlinks
-->

<a href="https://www.influxdata.com/time-b-platform/telegraf/" target="_blank">Telegraf</a> is _InfluxData_'s 
open-source agent for collecting, processing, and forwarding metrics and events. It connects southbound data sources — 
system logs, hardware sensors, applications — to a storage or analytics layer.

This page covers how to configure Telegraf to publish metrics into AnyLog over MQTT. A REST alternative is included 
in the config but commented out. For details on how AnyLog interprets and stores the incoming data, see 
<a href="{{ '/docs/Managing-Data-Southbound/mapping-policies/' | relative_url }}">Mapping Policies</a>.

---

## How It Works

Telegraf collects metrics from input plugins (CPU, memory, network, etc.) and forwards them as JSON payloads to 
AnyLog's local message broker. Because Telegraf metrics vary in structure across input plugins — different field 
names, value types, and tags — AnyLog uses a **wildcard mapping policy** that dynamically infers column names and 
types from each payload rather than requiring a rigid per-column schema.

The table name is derived from the metric name and host tag, so each Telegraf input lands in its own table 
automatically.

---

## Setup

### 1. Deploy an AnyLog Operator Node
To query the ingested data directly: 
Deploy an AnyLog operator node with a local message broker enabled. See 
<a href="{{ '/docs/Network-Services/background-services/#operator-process' | relative_url }}">background processes</a> for configuration details.

### 2. Attach to the AnyLog Node

Connect to the AnyLog CLI on your operator node.

### 3. Register the Mapping Policy

```anylog
policy_id = telegraf-mapping

<new_policy = {"mapping": {
    "id": !policy_id,
    "dbms": !default_dbms,
    "table": "bring [name]",
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
            "bring": ["fields", "tags"]
        }
    }
}}>

blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

The `"*"` schema entry tells AnyLog to extract all keys from the `fields` and `tags` objects and create columns 
for them dynamically, inferring each type from the value. One policy handles all Telegraf inputs.

### 4. Start the Message Client

```anylog
topic_name = telegraf

<run msg client where broker=local and port=!anylog_broker_port and log=false and topic=(
    name=!topic_name and
    policy=!policy_id
)>
```

> Steps 3 and 4 can be run together:  
> <code>process <a href="https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/sample-scripts/telegraf.al" target="_blank">`!local_scripts/demo-scripts/telegraf.al`</a></code>

### 5. Configure Telegraf

Create a `telegraf.conf` file:

```toml
[agent]
  interval = "5s"
  flush_interval = "5s"

# -----------------------
# INPUTS
# -----------------------

[[inputs.cpu]]
  percpu = true
  totalcpu = true

[[inputs.mem]]

[[inputs.swap]]

[[inputs.net]]

# -----------------------
# OUTPUT: MQTT
# -----------------------

[[outputs.mqtt]]
  servers = ["tcp://192.168.65.3:32150"]  # replace with your broker address
  topic = "telegraf"
  qos = 1
  data_format = "json"
  json_timestamp_units = "1s"

# -----------------------
# OUTPUT: REST (alternative)
# -----------------------

# [[outputs.http]]
#   url = "http://192.168.65.3:32149"
#   method = "POST"
#
#   [outputs.http.headers]
#     command = "data"
#     topic = "telegraf"
#     User-Agent = "AnyLog/1.23"
#     Content-Type = "application/json"
#
#   data_format = "json"
#   json_timestamp_units = "1s"
```

### 6. Start Telegraf

```shell
docker run --rm \
  -v $(pwd)/telegraf.conf:/etc/telegraf/telegraf.conf \
  telegraf
```

---

## Validation
Once Telegraf is running, use the following AnyLog commands to verify data is flowing correctly through each stage 
of the pipeline:

* `get msg client` - Confirms messages are being received on the topic; shows message counts per policy
```anylog
AL anylog-standalone-operator > get msg client 

Subscription ID: 0001
User:         unused
Broker:       local
Connection:   Connected to local Message Server

     Messages    Success     Errors      Last message time    Last error time      Last Error
     ----------  ----------  ----------  -------------------  -------------------  ----------------------------------
           6636        6635           1  2026-04-18 00:11:09  2026-04-17 23:52:18  File move to watch dir failed

     Subscribed Topics:
     Topic         Dynamic QOS DBMS Table Column name Column Type Mapping Function Optional                                                          Policies
     -------------|-------|---|----|-----|-----------|-----------|----------------|-----------------------------------------------------------------|--------|
     telegraf-data|      0|   |    |     |           |           |                |blockchain get (mapping,transform) where [id] == telegraf-mapping|
```

* `get streaming` - Shows how incoming data is being split across tables; useful for verifying wildcard column expansion
```anylog
AL anylog-standalone-operator > get streaming 

Statistics
            Put    Put     Streaming Streaming Cached Counter    Threshold   Buffer   Threshold  Time Left Last Process
DBMS-Table  files  Rows    Calls     Rows      Rows   Immediate  Volume(KB)  Fill(%)  Time(sec)  (Sec)     HH:MM:SS
-----------|------|-----|-|---------|---------|------|----------|-----------|--------|----------|---------|------------|
mydb.mem   |     0|    0| |      557|      557|     7|       524|         10|   69.73|        60|       39|00:00:06    |
mydb.swap  |     0|    0| |    1,077|    1,077|    27|       916|         10|   32.91|        60|       38|00:00:06    |
mydb.net   |     0|    0| |      534|      534|    20|       464|         10|   57.86|        60|       22|00:00:06    |
mydb.cpu   |     0|    0| |    4,806|    4,806|    28|     4,230|         10|   94.68|        60|       53|00:00:06    |
```

* `get operator` - Confirms data has been processed and written to the database
```shell
AL anylog-standalone-operator > get operator 

Stats: OPERATOR JSON
DBMS Table Files Immediate Timestamp  Elapsed_time
----|-----|-----|---------|----------|------------|
mydb|mem  |    2|       47|1776471116|00:00:22    |
    |cpu  |   20|      146|1776471131|00:00:07    |
    |swap |    2|       18|1776471116|00:00:22    |
    |net  |    2|       18|1776471100|00:00:38    |


Stats: OPERATOR SQL
DBMS Table                                Files Immediate Timestamp  Elapsed_time
----|------------------------------------|-----|---------|----------|------------|
mydb|mem.2026_04_01_d14_insert_timestamp |    2|        0|1776469958|00:19:40    |
    |cpu.2026_04_01_d14_insert_timestamp |   20|        0|1776469970|00:19:28    |
    |net.2026_04_01_d14_insert_timestamp |    2|        0|1776469985|00:19:13    |
    |swap.2026_04_01_d14_insert_timestamp|    2|        0|1776470001|00:18:57    |


Stats: OPERATOR INSERTS
DBMS Table First insert Last insert Batch inserts Immediate inserts DBMS Seconds
----|-----|------------|-----------|-------------|-----------------|------------|
mydb|mem  |00:19:56    |00:00:07   |           22|              524|       7.330|
    |cpu  |00:19:41    |00:00:07   |          576|             4230|      58.280|
    |swap |00:19:41    |00:00:07   |          161|              916|      12.757|
    |net  |00:19:40    |00:00:07   |           70|              464|       6.211|


Stats: OPERATOR ERROR
Type        Counter Timestamp Elapsed time Dbms name Table name Last error Last error text
-----------|-------|---------|------------|---------|----------|----------|---------------|
JSON Errors|      0|        0|00:00:00    |         |          |         0|               |
SQL Errors |      0|        0|00:00:00    |         |          |         0|               |

```

* To query the ingested data directly:

```anylog
AL anylog-standalone-operator > run client () sql !default_dbms format=table "select * from cpu limit 10"

row_id insert_timestamp           tsd_name tsd_id timestamp             fields_usage_guest fields_usage_guest_nice fields_usage_idle fields_usage_iowait fields_usage_irq fields_usage_nice fields_usage_softirq fields_usage_steal fields_usage_system fields_usage_user tags_cpu tags_host
------ -------------------------- -------- ------ --------------------- ------------------ ----------------------- ----------------- ------------------- ---------------- ----------------- -------------------- ------------------ ------------------- ----------------- -------- ------------
     1 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0 99.79959919835603                 0.0                0                 0                    0                  0 0.20040080160310225               0.0 cpu0     e105d03c4ac6
     2 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0  99.7995991984288 0.20040080160324836                0                 0                    0                  0                 0.0               0.0 cpu1     e105d03c4ac6
     3 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0  99.7995991984288 0.20040080160324836                0                 0                    0                  0                 0.0               0.0 cpu1     e105d03c4ac6
     4 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0 99.79959919842894                 0.0                0                 0                    0                  0 0.20040080160310225               0.0 cpu2     e105d03c4ac6
     5 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0 99.79959919842894                 0.0                0                 0                    0                  0 0.20040080160310225               0.0 cpu2     e105d03c4ac6
     6 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0             100.0                 0.0                0                 0                    0                  0                 0.0               0.0 cpu3     e105d03c4ac6
     7 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0             100.0                 0.0                0                 0                    0                  0                 0.0               0.0 cpu3     e105d03c4ac6

row_id insert_timestamp           tsd_name tsd_id timestamp             fields_usage_guest fields_usage_guest_nice fields_usage_idle fields_usage_iowait fields_usage_irq fields_usage_nice fields_usage_softirq fields_usage_steal fields_usage_system fields_usage_user tags_cpu tags_host
------ -------------------------- -------- ------ --------------------- ------------------ ----------------------- ----------------- ------------------- ---------------- ----------------- -------------------- ------------------ ------------------- ----------------- -------- ------------
     8 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0             100.0                 0.0                0                 0                    0                  0                 0.0               0.0 cpu4     e105d03c4ac6
     9 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0             100.0                 0.0                0                 0                    0                  0                 0.0               0.0 cpu4     e105d03c4ac6
    10 2026-04-17 23:52:37.875177        5     22 2026-04-17 23:50:41.0                  0                       0             100.0                 0.0                0                 0                    0                  0                 0.0               0.0 cpu5     e105d03c4ac6

{"Statistics":[{"Count": 10,
                "Time":"00:00:00",
                "Nodes": 1}]}
```


