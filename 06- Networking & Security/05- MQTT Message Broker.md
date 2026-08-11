---
title: "MQTT Message Broker"
description: Configure AnyLog for MQTT ingestion, including external brokers, AnyLog as the broker, dynamic UNS policies, table naming, TLS, debugging, and worked use cases.
layout: page
source_path: "background processes.md#message-broker"
---

<!---
### Change Log
 **Date**   | **Name** | **Change** | **Version** |
 |------------|--|------------|----------|
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-25 | Ori Shadmon | Consolidated prior message-broker, broker setup, TLS, and mapping-policy MQTT material. |
 | 2026-08-10 | | Split Kafka into its own page and refocused this document on MQTT. Added dynamic topic/table use cases, broker topology guidance, query examples, and configuration caveats. |
--->

## Overview

MQTT is useful when devices, gateways, and applications need to publish telemetry through a lightweight
publish/subscribe protocol. AnyLog handles MQTT with two cooperating services:

* **Message broker**: receives MQTT messages from publishers. This can be an external broker such as Mosquitto,
  HiveMQ, CloudMQTT, or AnyLog's built-in broker.
* **Message client**: subscribes to MQTT topics and maps matching messages into AnyLog tables and UNS policies.

Even when AnyLog is the broker, the `AnyLog Message Client` is still required. The broker accepts the MQTT packet;
the message client decides how the topic and payload become tables, columns, and Unified Namespace metadata. The
advantage is that publishers can send directly to the AnyLog operator's MQTT broker port, removing the separate
external broker hop. For example, a sensor publishing to `[topic]` can be mapped by the local message client into
`[dbms].[table]` and made available to distributed SQL queries.

| External broker pattern | AnyLog-as-broker pattern   |
|---|----------------------------|
| `Sensor / Publisher` | `Sensor / Publisher`       |
| ↓ | ↓                          |
| `External MQTT Broker` | `AnyLog MQTT Broker` & `AnyLog Message Client`    |
| ↓ |                           |
| `AnyLog Message Client` |                            |
| ↓ | ↓                          |
| `AnyLog table + UNS policies` | `AnyLog table + UNS policies` |

This AnyLog as a broker pattern reduces latency, network egress, failure points, and the need to manage an additional software
service. Here, AnyLog manages both the broker and the client, which simplifies deployments and operational
management. Another advantage is that AnyLog enables broker and client parallelization:
multiple AnyLog Brokers and Message Clients can run across operators, sites, or locations while still
presenting distributed data as if it is hosted on a single logical system through the AnyLog network.

External brokers are still useful when a site already has MQTT infrastructure, when multiple AnyLog or non-AnyLog
consumers must read the same feed, or given a specific use case or requirement. In that pattern, configure AnyLog
as a subscriber to the external broker and the same single logical system view is still provided.

## Page Summary

Use this page as a configuration reference and jump to the section that matches the task:

* <a href="#enable-anylog-as-an-mqtt-broker" target="_blank">Enable AnyLog as an MQTT Broker</a>: start the built-in broker, review broker
  options, and validate that the MQTT port is active.
* <a href="#run-an-mqtt-message-client" target="_blank">Run an MQTT Message Client</a>: subscribe to MQTT topics and define the connection,
  client, and topic options that map messages into AnyLog.
* <a href="#topic-matching-and-table-naming" target="_blank">Topic matching and table naming</a>: understand MQTT case sensitivity, AnyLog
  name normalization, generated table precedence, and possible case-only table collisions.
* <a href="#mapping-json-payloads" target="_blank">Mapping JSON Payloads</a>: use `bring` expressions and explicit column mappings when
  dynamic table generation is not used.
* <a href="#dynamic-uns-policies" target="_blank">Dynamic UNS Policies</a>: generate tables and UNS policies automatically from matching
  topics and JSON payloads.
* <a href="#registering-a-mapping-policy" target="_blank">Registering a Mapping Policy</a>: store reusable mappings on the blockchain and
  reference them from message-client subscriptions.
* <a href="#publishing-mqtt-data" target="_blank">Publishing MQTT Data</a>: publish test messages from AnyLog or Mosquitto.
* <a href="#mqtt-over-tls-and-mtls" target="_blank">MQTT over TLS and mTLS</a>: configure certificate-based broker security.
* <a href="#debugging-and-validation" target="_blank">Debugging and Validation</a>: inspect clients, broker activity, streaming status,
  generated tables, and ingestion errors.
* <a href="#example-use-cases" target="_blank">Example Use Cases</a>: walk through multi-operator ingestion, `table_prefix`,
  `table_name_as_topic`, schema-change behavior, case-sensitive topics, and AnyLog as the broker.

## Enable AnyLog as an MQTT Broker

Use this command when publishers should connect directly to the AnyLog node:

```anylog
<run message broker where
    external_ip = [ip] and external_port = [port] and
    internal_ip = [local_ip] and internal_port = [local_port] and
    bind = [true|false] and threads = [threads count]>
```

### Broker options

| Option | Description |
|---|---|
| `external_ip` | IP address advertised or used by external publishers. |
| `external_port` | MQTT broker port exposed to external publishers. Common defaults are `1883` for MQTT and `8883` for MQTT over TLS. |
| `internal_ip` | Optional internal/local network IP. |
| `internal_port` | Optional internal/local broker port. |
| `bind` | `true` binds to the configured address; `false` commonly binds to all interfaces for the exposed port. |
| `threads` | Number of broker worker threads. Default is `6` when omitted. |
| `enable_tls` | `true` enables TLS for the broker listener. |
| `tls_cert` | Server certificate file used by the broker. |
| `tls_key` | Server private key file used by the broker. |
| `users_ca` | CA certificate used to validate client certificates for mTLS. |
| `allowed_users` | Optional list of permitted client certificate CN values. |

### Example: starting an AnyLog MQTT broker
```anylog
<run message broker where
    external_ip = 192.168.0.138 and external_port = 2001 and
    internal_ip = 192.168.0.138 and internal_port = 2001 and
    bind = true and threads = 3>
```

Validate that the broker is bound:

```anylog
AL operator1 > get connections
Type      External Address    Internal Address    Bind Address
---------|-------------------|-------------------|-------------------|
TCP      |192.168.0.138:32148|192.168.0.138:32148|192.168.0.138:32148|
REST     |192.168.0.138:32149|192.168.0.138:32149|0.0.0.0:32149      |
Messaging|192.168.0.138:2001 |192.168.0.138:2001 |192.168.0.138:2001 |
```
You will see broker and topic information once you assign a Message Client
```anylog
AL operator1 > get msg broker
     Broker Topic    Client ID Messages Success Failure
     ------|--------|---------|--------|-------|-------|
     local |broker/#|        1|       0|      0|      0|
```
You will MQTT stats after the first publish
```anylog
AL operator1 > get local broker
Message Broker Stat
Protocol IP            Event   TLS User Success Last message time   Error Last error time     Error Code              Details
--------|-------------|-------|---|----|-------|-------------------|-----|-------------------|-----------------------|-----------|
MQTT    |192.168.0.138|CONNECT|no |    |      1|2026-08-10 09:53:12|    0|                   |                       |           |

AL operator1 > get streaming
Statistics
                 Put    Put     Streaming Streaming Cached Counter    Threshold   Buffer   Threshold  Time Left Last Process
DBMS-Table       files  Rows    Calls     Rows      Rows   Immediate  Volume(KB)  Fill(%)  Time(sec)  (Sec)     HH:MM:SS
----------------|------|-----|-|---------|---------|------|----------|-----------|--------|----------|---------|------------|
mydb.broker_data|     0|    0| |        1|        1|     0|         0|         10|     0.0|         1|        1|00:00:30    |
```

If a port fails to bind:

```anylog
get error log
get ip list
```

## Run an MQTT Message Client

The message client subscribes to MQTT topics and maps matching messages into AnyLog.

```anylog
run msg client where [connection parameters] and [config parameters] and topic = (topic params)
```

A single `run msg client` command can include multiple `topic = (...)` blocks.

### Connection options

| Option | Description |
|---|---|
| `broker` | Broker URL or IP. Use `local` for this node's own AnyLog broker. If the IP/port matches a local `run message broker`, it resolves like `local`. |
| `port` | Broker port. Default is `1883`. |
| `user` | MQTT username, if required. |
| `password` | MQTT password, if required. |
| `client_id` | MQTT client ID, if required by the broker. |
| `project_id` | Broker/project identifier for brokers that require it. |
| `location` | Name identifying the broker/service location. |
| `private_key` | Private key used by broker integrations that require key-based authentication. |
| `master_node` | Master node TCP address used when `dynamic = true` creates UNS policies. |

### Client options

| Option | Description |
|---|---|
| `log` | `true` enables MQTT client log callback output. No effect when the node itself is the broker. |
| `log_error` | `true` writes messages that fail processing to `err_<broker ID>_<topic>` in the error directory. |
| `qos` | Default MQTT Quality of Service for subscriptions. Default is `0`. |
| `prep_dir` | Directory for organizing incoming message data. |
| `watch_dir` | Watch directory location. |
| `err_dir` | Error directory location. |
| `persist` | `true` writes incoming messages to files instead of processing them immediately. Useful for capturing raw input. |

### Topic options

| Option | Description |
|---|---|
| `name` | MQTT topic subscription. `#` subscribes to all topics. A suffix such as `A/#` dynamically matches child topics under `A/`. |
| `qos` | Per-topic QoS override. |
| `dbms` | Logical AnyLog database name, or a `bring` command that extracts it from the message. |
| `table` | Explicit table name, or a `bring` command that extracts it from the message. In `dynamic = true`, omit this when AnyLog should derive table names from topics. |
| `table_prefix` | In `dynamic = true`, when `table` is omitted, writes to `{table_prefix}_{last_topic_segment}`. Ignored when `table` is set or `table_name_as_topic = true`. |
| `table_name_as_topic` | `true` derives the table from the full topic path. For example, `C/A/data` becomes `c_a_data`. Ignores `table` and `table_prefix`. |
| `column.[name].[type]` | Explicit column mapping paired with a `bring` command. Used when `dynamic` is omitted or `false`. |
| `dynamic` | `true` auto-generates tables and UNS policies from the topic and JSON payload. |
| `policy` | Reusable mapping policy previously inserted into the blockchain. Replaces inline `dbms`, `table`, and `column...` mappings. |

## Topic matching and table naming

MQTT topic matching is traditionally case-sensitive. A subscription to `C/#` matches `C/data`; it does not match `c/data`.

AnyLog preserves MQTT's case-sensitive subscription behavior.
However, AnyLog does more than subscribe to and forward MQTT messages.
It ingests MQTT data directly into local storage at the edge, automatically
creating and managing the database objects needed to make that data immediately queryable.

Because these database objects become part of a distributed AnyLog environment and can be
queried across many independent nodes, AnyLog normalizes generated database, table, prefix,
and column names to provide a consistent naming convention across the system. Uppercase letters
are converted to lowercase, while spaces and unsupported characters are converted to underscores.
This prevents logically equivalent objects from being created under names that differ only by
capitalization and provides consistent references across local storage, distributed queries,
metadata, and applications, especially because databases are case insensitive.

> **Important:** MQTT subscription matching itself remains case-sensitive. `C/#` does not match `c/data`. To ingest both topic paths, configure subscriptions for both `C/#` and `c/#`. If they represent different data sources, ensure that their generated or explicitly configured AnyLog table names do not collide.

For example, MQTT considers these two topics different:

```text
Plant/CX1/Motor1
plant/cx1/motor1
```

With:

```text
table_name_as_topic = true
```

both are normalized by AnyLog to:

```text
plant_cx1_motor1
```

Similarly:

```text
C/data
c/data
```

both generate `c_data` when `table_name_as_topic = true`, and both generate `data` when using the default last-segment table naming.

If publishers use capitalization to distinguish different data sources, configure those sources to map to distinct database objects by assigning different `table` values, unique `table_prefix` values, separate `dbms` names, or by changing the MQTT topic convention so that the distinction is not based only on case.

For the topic `Plant/CX1/Motor1`, table naming precedence is:

| Topic settings                          | Resulting table    |
| --------------------------------------- | ------------------ |
| `table_name_as_topic = true`            | `plant_cx1_motor1` |
| `table = some_table`                    | `some_table`       |
| `table_prefix = prefix1` and no `table` | `prefix1_motor1`   |
| `dynamic = true` with no table settings | `motor1`           |

### Example Message Client Commands
Say you want to subscribe to the topic `data/#`, and publish data like:
```bash
mosquitto_pub \
  -p 2001 \
  -h 192.168.0.138 \
  -t data/my_data \
  -m '{"Broker":"A","value":50.7, "temp": 12.2}'
 ```
Data will be written to `dbms=mydb` and `table_name = data_my_data`
```anylog
<run msg client where
	broker = 192.168.0.138 and port = 2001 and
	master_node = 192.168.0.138:32048 and
	topic = (
		name = "data/#" and
		dbms = mydb and
		dynamic = true and
		table_name_as_topic = true
	)>
```
Data will be written to `dbms=mydb` and `table_name = my_prefix_my_data`:
```anylog
<run msg client where
	broker = 192.168.0.138 and port = 1884 and
	master_node = 192.168.0.138:32048 and
	topic = (
		name = "data/#" and
		dbms = mydb and
		dynamic = true and
		table_prefix = my_prefix
	)>
```
Data will be written to `dbms=mydb` and `table_name = my_data`:
```anylog
<run msg client where
	broker = 192.168.0.138 and port = 1884 and
	master_node = 192.168.0.138:32048 and
	topic = (
		name = "data/#" and
		dbms = mydb and
		dynamic = true
	)>
```
Data will be written to `dbms=mydb` and `table_name = my_new_table`:
```anylog
<run msg client where
	broker = 192.168.0.138 and port = 1884 and
	master_node = 192.168.0.138:32048 and
	topic = (
		name = "data/#" and
		table = my_new_table
		dbms = mydb and
		dynamic = true
	)>
```
Data will be written to `dbms=mydb` and `table_name = my_new_table` (table overwrites prefix):
```anylog
<run msg client where
	broker = 192.168.0.138 and port = 1884 and
	master_node = 192.168.0.138:32048 and
	topic = (
		name = "data/#" and
		table = my_new_table and
		table_prefix = my_prefix and
		dbms = mydb and
		dynamic = true
	)>
```

### QoS

| Level | Meaning |
|---|---|
| `0` | No delivery guarantee. The recipient does not acknowledge receipt. Default. |
| `1` | Delivered at least once. Duplicate messages may arrive. |
| `2` | Delivered exactly once. Highest guarantee. |

## Mapping JSON Payloads

When `dynamic = false` or omitted, define the table and each column explicitly:

```anylog
<run msg client where broker = local and topic = (
    name = mqtt-test and
    dbms = my_dbms and
    table = rand_data and
    column.timestamp.timestamp = now and
    column.value.float = "bring [readings][][value]"
)>
```

`bring` extracts values from JSON payloads. Two equivalent column forms are supported:

```anylog
column.value.float = "bring [readings][][value]"
column.value = (value = "bring [readings][][value]" and type = "bring [readings][][valueType]")
```

Supported data types include `str`, `int`, `float`, `timestamp`, and `bool`.

If a `bring` expression is allowed to be missing, set `optional = true`:

```anylog
column.info = (type = str and value = "bring [info]" and optional = true)
```

## Dynamic UNS Policies

Set `dynamic = true` when AnyLog should infer schema and generate UNS policies from matching MQTT topics.

```anylog
<run msg client where
    broker = 192.168.1.88 and port = 1883 and
    master_node = 192.168.1.60:32048 and
    topic = (
        name = "Plant/#" and
        dbms = new_company and
        dynamic = true and
        table_name_as_topic = true
    )>
```

Dynamic mode behavior:

* JSON object attributes become columns.
* The initial table schema controls later inserts. If a later message includes a new field that is not in the
  table, the existing columns can still insert while the new field is ignored.
* UNS policies are generated from matched topics. If the topic configuration is too broad or the table naming mode
  is not what was intended, policies can be created for topic paths that do not successfully insert data.
* Run the UNS streamer so generated UNS metadata is written regularly.

```anylog
run uns streamer
run uns streamer where frequency = 3
```

## Registering a Mapping Policy

Instead of repeating inline mapping in every `run msg client` command, register a mapping policy on the blockchain
and reference it by name.

```anylog
policy_id = telegraf-mapping

<new_policy = {"mapping": {
    "id": !policy_id,
    "dbms": "bring [dbms]",
    "table": "bring [sensor]",
    "readings": "",
    "schema": {
        "timestamp": {
            "type": "timestamp",
            "default": "now()",
            "bring": "[timestamp]"
        },
        "value": {
          "type": "float",
          "default": null,
          "bring": "[value]"
        }
    }
}}>

blockchain insert where policy = !new_policy and local = true and master = !ledger_conn

run msg client where broker = local and log = false and topic = (name = my-topic and policy = !new_policy)
```

## Publishing MQTT Data

From AnyLog:

```anylog
mqtt publish where broker = [url] and port = [port] and user = [user] and password = [password] and topic = [topic] and qos = [value] and message = [message]
```

When publishing from the same node that runs the broker:

```anylog
mqtt publish where broker = local and topic = [topic] and qos = [value] and message = [message]
```

From Mosquitto:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t A/data \
  -m '{"Broker":"A","value":42.7}'
```

For structured payloads in the AnyLog CLI, define JSON first and publish the variable:

```anylog
<message = {"value":210,
            "ts":1607959427550,
            "protocol":"modbus",
            "measurement":"temp02",
            "metadata":{
                    "company":"Anylog",
                    "machine_name":"cutter 23",
                    "serial_number":"1234567890"}}>

json !message test

mqtt publish where broker = local and topic = test and message = !message
```

## MQTT over TLS and mTLS

For certificate-based MQTT security:

1. Create a CA for self-signed TLS certificates.
2. Create and sign a server certificate request.
3. Start the broker with TLS enabled.

```anylog
<run message broker where external_ip = [ip] and external_port = 8883 and threads = 6
  and enable_tls = true
  and tls_cert = ./data/pem/server_tls.crt
  and tls_key = ./data/pem/server_tls.key
  and users_ca = ./data/pem/CA_users.crt
  and allowed_users = (user1, user2)
>
```

`allowed_users` is optional. When set, the listed names are the CN values in client certificates permitted to
connect. `users_ca` is the CA that issued the client certificates.

Publish from a TLS-capable MQTT client such as `mosquitto_pub`:

```shell
mosquitto_pub \
  --cafile ./data/pem/CA.crt \
  --cert ./data/pem/user1.crt \
  --key ./data/pem/user1.key \
  -h 192.168.0.138 \
  -p 8883 \
  -t broker/data \
  -m '{"Broker":"A","value":50.7}'
```

## Debugging and Validation

```anylog
set mqtt debug on
set mqtt debug off
get msg clients
get msg client where id = [n]
get streaming
get tables where dbms = *
get columns where dbms = mydb and table = data
get local broker
```

Useful client settings:

* `log = true` shows MQTT client processing callbacks for external brokers.
* `persist = true` writes incoming messages to files instead of processing them.
* `log_error = true` writes failed messages to the error directory.
* Subscribing to `#` captures all topics; matched subscriptions are processed and unmatched topics are flushed to
  log files.

Terminate clients:

```anylog
exit msg client [ID|all]
```
Note you can find the ID of a message client using the `get msg clients` AnyLog CLI command.

## Example Use Cases

The following examples assume two operators subscribe to two MQTT broker ports on the same host. Run each
`run msg client` command on the operator that should ingest from that broker port.

### Case 1: two operators, default dynamic table names

Operator subscribed to broker port `1883`:

```anylog
<run msg client where
    broker = 192.168.0.138 and port = 1883 and
    master_node = 192.168.0.138:32048 and
    log = true and
    topic = (
        name = "A/#" and
        dbms = mydb and
        dynamic = true
    )>
```

Operator subscribed to broker port `1884`:

```anylog
<run msg client where
    broker = 192.168.0.138 and port = 1884 and
    master_node = 192.168.0.138:32048 and
    topic = (
        name = "A/#" and
        dbms = mydb and
        dynamic = true
    )>
```

Publish one message to each broker:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t A/data \
  -m '{"Broker":"A","value":42.7}'

mosquitto_pub \
  -p 1884 \
  -h 127.0.0.1 \
  -t A/data \
  -m '{"Broker":"B","value":45.7}'
```

Both messages insert into `mydb.data`, which can be verified with AnyLog CLI command:
```anylog
AL operator2 > get data nodes
Company    DBMS Table       Cluster ID                       Cluster Status Node Name Member ID External IP/Port    Local IP/Port Main Node Status
----------|----|-----------|--------------------------------|--------------|---------|---------|-------------------|-------------|----|-----------|
AnyLog Co.|mydb|data       |fed71895ee0161ffe92bb79f7e85791c|active        |operator1|       68|192.168.0.138:32148|             | +  |active     |
          |    |           |6ca7df77cc8f4777cfd427dff870af5f|active        |operator2|      212|192.168.0.138:32248|             | +  |active     |
```

This data hosted by two AnyLog operators on two physical machines or sites can then be queried:
```anylog
AL operator2 > run client () sql mydb format=table and extend=(+ip, +node_name, @table_name) "select broker, value from data"
ip            node_name table_name broker value
------------- --------- ---------- ------ -----
192.168.0.138 operator2 data       B       45.7
ip            node_name table_name broker value
------------- --------- ---------- ------ -----
192.168.0.138 operator1 data       A       42.7
{"Statistics":[{"Count": 2,
                "Time":"00:00:00",
                "Nodes": 2}]}
```

Unintended configuration:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t A/B/data \
  -m '{"Broker":"A","value":42.7}'
```

This can create new UNS policies for `A/B/data`, but the data may fail to insert and leave those UNS policies
orphaned. If nested topic paths should be stored separately, configure the client with `table_name_as_topic = true`
before publishing. If nested paths should not be accepted, publish only to the intended topic shape, such as
`A/data`.

### Case 2: two operators with `table_prefix`

```anylog
<run msg client where
    broker = 192.168.0.138 and port = 1883 and
    master_node = 192.168.0.138:32048 and
    topic = (
        name = "B/#" and
        dbms = mydb and
        dynamic = true and
        table_prefix = PRE1
    )>

<run msg client where
    broker = 192.168.0.138 and port = 1884 and
    master_node = 192.168.0.138:32048 and
    topic = (
        name = "B/#" and
        dbms = mydb and
        dynamic = true and
        table_prefix = PRE1
    )>
```

Publish to both brokers:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t B/data \
  -m '{"Broker":"A","value":42.7}'

mosquitto_pub \
  -p 1884 \
  -h 127.0.0.1 \
  -t B/data \
  -m '{"Broker":"B","value":45.7}'
```

Both messages insert into `mydb.pre1_data`. `PRE1` is normalized to lowercase.

This message also inserts into the same `pre1_data` table, because the last topic segment is still `data`:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t B/A/data \
  -m '{"Broker":"A","value":42.7}'
```

Unintended configuration: if `B/data` and `B/A/data` should be separate tables, use `table_name_as_topic = true`
instead of `table_prefix`.

Schema change behavior:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t B/A/data \
  -m '{"Broker":"A","value":42.7, "temp": 12.2}'
```

The new `temp` value is not inserted if the existing `pre1_data` table schema does not include that column. The
existing columns still insert. To ingest the new field, update the table/schema before publishing, or publish the
new schema to a new topic/table.

### Case 3: two operators with `table_name_as_topic`

```anylog
<run msg client where
    broker = 192.168.0.138 and port = 1883 and
    master_node = 192.168.0.138:32048 and
    topic = (
        name = "C/#" and
        dbms = mydb and
        dynamic = true and
        table_name_as_topic = true
    )>

<run msg client where
    broker = 192.168.0.138 and port = 1884 and
    master_node = 192.168.0.138:32048 and
    topic = (
        name = "C/#" and
        dbms = mydb and
        dynamic = true and
        table_name_as_topic = true
    )>
```

Publish to `C/data`:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t C/data \
  -m '{"Broker":"A","value":42.7}'

mosquitto_pub \
  -p 1884 \
  -h 127.0.0.1 \
  -t C/data \
  -m '{"Broker":"B","value":45.7}'
```

Both messages insert into `mydb.c_data`.

Publish to a nested topic:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t C/A/data \
  -m '{"Broker":"A","value":42.7}'
```

This inserts into `mydb.c_a_data`, because the full topic path becomes the table name.

Schema change behavior:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t C/data \
  -m '{"Broker":"A","value":50.7, "temp": 12.2}'
```

If `c_data` was already created without `temp`, the new `temp` column is not inserted; existing columns still
insert. Update the schema first, or route schema variants to separate tables.

Case-sensitive topic matching:

```shell
mosquitto_pub \
  -p 1883 \
  -h 127.0.0.1 \
  -t c/data \
  -m '{"Broker":"A","value":50.7, "temp": 12.2}'
```

This does not match `name = "C/#"` because MQTT topics are case-sensitive. Publish to `C/data`, or configure an
additional subscription for `c/#` if lowercase publishers are expected.

### Case 4: AnyLog as the broker

Start AnyLog's MQTT broker:

```anylog
<run message broker where
    external_ip = 192.168.0.138 and external_port = 2001 and
    internal_ip = 192.168.0.138 and internal_port = 2001 and
    bind = true and threads = 3>
```

Subscribe a message client to that broker:

```anylog
<run msg client where
    broker = 192.168.0.138 and port = 2001 and
    master_node = 192.168.0.138:32048 and
    topic = (
        name = "broker/#" and
        dbms = mydb and
        dynamic = true and
        table_name_as_topic = true
    )>
```

Publish directly into AnyLog:

```shell
mosquitto_pub \
  -p 2001 \
  -h 192.168.0.138 \
  -t broker/data \
  -m '{"Broker":"A","value":50.7, "temp": 12.2}'
```

The message inserts into `mydb.broker_data`, with no external MQTT broker hop.

## Related

* <a href="./05-1%20Kafka%20Message%20Client.md" target="_blank">Kafka Message Client</a>
* <a href="./05-2%20Connectors%20To%20Data%20Sources.md" target="_blank">Connectors To Data Sources</a>
* <a href="./02-%20Network%20Processing.md" target="_blank">Network Processing</a>
* <a href="./04-%20Using%20REST.md" target="_blank">Using REST</a>
* <a href="../08-%20Blockchain%20&%20Metadata/05-%20Unitfied%20Namespace.md" target="_blank">Unified Namespace</a>
