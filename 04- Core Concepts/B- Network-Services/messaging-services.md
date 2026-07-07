---
title: Messaging Service
description: The AnyLog Messaging service is a dedicated network port that accepts data from MQTT, Kafka, Syslog, and REST — the unified southbound ingestion endpoint.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlink
--> 

Every AnyLog node exposes three network services: **TCP** (peer-to-peer), **REST** (external API), and **Messaging** — a dedicated port that acts as a unified southbound ingestion endpoint. The Messaging service is started with `run message broker` and appears alongside TCP and REST in `get connections`.

Multiple protocols can deliver data to the Messaging port simultaneously. The protocol is determined by how the client connects and how the subscription is declared on the AnyLog side — there is no per-protocol configuration on the service itself.

```
get connections
```

```
Type       External                Local                  Bind
----------|----------------------|----------------------|---------------------|
TCP       |172.105.6.90:32148    |172.105.6.90:32148    |172.105.6.90:32148   |
REST      |172.105.6.90:32149    |172.105.6.90:32149    |0.0.0.0:32149        |
Messaging |172.105.6.90:32150    |172.105.6.90:32150    |0.0.0.0:32150        |
```

The `Messaging` port accepts:

| Protocol | How to connect |
|---|---|
| **MQTT** (external broker) | `run msg client where broker = [url] ...` |
| **MQTT** (AnyLog as broker) | `run msg client where broker = local ...` |
| **Kafka** | `run kafka consumer where ip = [local IP] and port = [broker port] ...` |
| **Syslog** | Direct TCP to the Messaging port + `set msg rule` |
| **REST POST** | `run msg client where broker = rest and user-agent = anylog ...` |

---

## Starting the Messaging service

```anylog
<run message broker where
    external_ip = !external_ip and external_port = !anylog_broker_port and
    internal_ip = !ip and internal_port = !anylog_broker_port and
    bind = false and threads = 6>
```

See <a href="{{ '/docs/Network-Services/background-services/#message-broker-service-local' | relative_url }}">Background Services</a> for full options.

## Prerequisites for data ingestion

The Messaging service accepts and buffers data. For that data to reach a database, the following must also be running:

```anylog
run streamer
run operator where create_table = true and update_tsd_info = true and archive_json = true and master_node = !master_node and policy = !operator_policy
```

See <a href="{{ '/docs/Network-Services/Managing-Data-Southbound/southbound-overview/' | relative_url }}">Managing Data (Southbound)</a>
for the full ingestion pipeline.

---

## MQTT — subscribe to an external broker

Subscribe to topics on a third-party MQTT broker (Mosquitto, HiveMQ, CloudMQTT, etc.):

```anylog
<run msg client where
    broker = [url] and port = [port] and
    user = [user] and password = [password] and
    log = false and
    topic = (
        name = [topic] and
        dbms = [dbms] and
        table = [table] and
        column.timestamp.timestamp = "bring [ts]" and
        column.value.float = "bring [value]"
    )>
```

Example:
```anylog
<run msg client where
    broker = driver.cloudmqtt.com and port = 18975 and
    user = mqwdtklv and password = uRimssLO4dIo and
    log = false and
    topic = (
        name = test and
        dbms = "bring [metadata][company]" and
        table = "bring [metadata][machine_name] _ [metadata][serial_number]" and
        column.timestamp.timestamp = "bring [ts]" and
        column.value = (type = int and value = "bring [value]")
    )>
```

---

## MQTT — AnyLog as the broker

With `broker = local`, AnyLog subscribes to its own Messaging service rather than a third-party broker. Data is 
delivered directly to the Messaging port without any external dependency.

```anylog
<run msg client where
    broker = local and
    log = false and
    topic = (
        name = [topic] and
        dbms = [dbms] and
        table = [table] and
        column.timestamp.timestamp = "bring [ts]" and
        column.value.float = "bring [value]"
    )>
```

Publish to the local broker:
```anylog
mqtt publish where broker = local and topic = [topic] and message = [json message]
```

View messages processed through the local broker:
```anylog
get local broker
```

### Dynamic mode (UNS)

Setting `dynamic = true` enables automatic table creation from topic structure and automatic generation of UNS policies 
— no explicit column mapping needed. If the data is JSON, attribute names become column names. If not JSON, column 
names are derived from the topic segments.

```anylog
<run msg client where
    broker = local and
    topic = (
        name = "Enterprise/Site1/#" and
        dbms = my_dbms and
        dynamic = true
    )>
```

When using dynamic mode with non-JSON data, enable the UNS Streamer:
```anylog
run uns streamer where frequency = 3
```

---

## Kafka

AnyLog can consume from Kafka topics and ingest the data into local databases. The `run kafka consumer` command 
connects to the Kafka broker and maps messages to database tables using the same topic mapping syntax as MQTT.

```anylog
<run kafka consumer where
    ip = [kafka broker ip] and port = [kafka broker port] and
    reset = [latest|earliest] and
    topic = (
        name = [topic] and
        dbms = [dbms] and
        table = [table] and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value.int = "bring [value]"
    )>
```

| Option | Description | Default |
|---|---|---|
| `ip` | Kafka broker IP | |
| `port` | Kafka broker port | |
| `reset` | Offset policy: `latest` or `earliest` | `latest` |
| `topic` | One or more topics with mapping instructions | |

Example:
```anylog
run kafka consumer where ip = 198.74.50.131 and port = 9092 and reset = latest and topic = (
    name = ping_data and
    dbms = lsl_demo and
    table = ping_sensor and
    column.timestamp.timestamp = "bring [timestamp]" and
    column.value.int = "bring [value]"
)
```

AnyLog can also produce to Kafka — directing a query result set to a Kafka topic:
```anylog
run client () sql my_dbms format = json:output and stat = false and dest = kafka@198.74.50.131:9092 and topic = my_topic "select * from my_table limit 10"
```

---

## Syslog

AnyLog's Messaging service accepts Syslog messages over TCP (BSD RFC 3164 and IETF RFC 5424 formats). Configure the 
syslog sender to direct output to the Messaging IP and port, then set a rule on the AnyLog node to route incoming 
messages to a database table.

### 1. Set a rule

```anylog
set msg rule [rule name] if ip = [source IP] and port = [source port] and header = [header] then dbms = [dbms] and table = [table] and syslog = [true/false] and extend = ip
```

| Option | Mandatory | Description |
|---|---|---|
| `rule name` | Y | Unique identifier for the rule |
| `ip` | N | Source IP — if omitted, applies to all sources |
| `port` | N | Source port — if omitted, applies to all ports |
| `header` | N | Match messages with this header prefix |
| `dbms` | Y | Target database |
| `table` | Y | Target table |
| `syslog` | N | `true` — parse as syslog (BSD by default, or IETF with `format = IETF`) |
| `extend` | N | Add extra fields to each row (e.g. `extend = ip` adds source IP) |
| `structure` | N | `included` — first event describes the column structure |

Examples:
```anylog
# Accept BSD syslog from a specific host
set msg rule my_rule if ip = 10.0.0.78 and port = 1468 then dbms = test and table = syslog and syslog = true

# Accept syslog with a header prefix (for journalctl piped via nc)
set msg rule my_rule if ip = 139.162.126.241 and header = al.sl.header.new_company.syslog then dbms = test and table = syslog and syslog = true
```

### 2. Configure the syslog sender

Direct syslog output over TCP to the AnyLog Messaging port. Example using `journalctl` and `nc`:

```bash
journalctl --since "${NOW}" | awk '{print "al.sl.header.new_company.syslog", $0}' | nc -w 1 [anylog-ip] [messaging-port]
```

### 3. Manage rules

```anylog
get msg rules                  # list all rules
reset msg rule [rule name]     # remove a rule
```

### 4. Debug

```anylog
trace level = 2 run message broker
```

---

## REST POST

Data can also be delivered to AnyLog via HTTP POST with `broker = rest`. AnyLog's REST service maps the posted payload 
to a database table based on the topic header.

```anylog
run msg client where broker = rest and user-agent = anylog and topic = (
    name = [topic] and
    dbms = [dbms] and
    table = [table] and
    column.timestamp.timestamp = "bring [ts]" and
    column.value.int = "bring [value]"
)
```

Publish data via curl:
```bash
curl -X POST http://[anylog-ip]:[rest-port] \
  -H "User-Agent: AnyLog/1.23" \
  -H "command: data" \
  -H "topic: [topic]" \
  -H "Content-Type: text/plain" \
  --data-raw '[{"ts": 1607959427550, "value": 210}]'
```

---

## Column mapping reference

All protocols use the same `bring` syntax to map message fields to database columns:

```anylog
column.[column name].[data type] = "bring [json path]"
```

Supported data types: `str`, `int`, `float`, `timestamp`, `bool`

| Pattern | Example |
|---|---|
| Fixed value | `dbms = my_data` |
| Extract from message | `dbms = "bring [metadata][company]"` |
| Concatenate fields | `table = "bring [device] _ [sensor]"` |
| Nested path | `column.value.float = "bring [readings][][value]"` |
| Type from message | `column.value = (value = "bring [v]" and type = "bring [type]")` |
| Optional field | `column.info = (type = str and value = "bring [info]" and optional = true)` |

### QoS (MQTT)

| Value | Meaning |
|---|---|
| `0` | No delivery guarantee (default) |
| `1` | At least once |
| `2` | Exactly once |

---

## Monitoring

```anylog
get msg clients                                           # all active subscriptions
get msg client where id = [n]                             # specific subscription
get msg client where broker = [url] and topic = [topic]   # filter by broker/topic
get local broker                                          # messages through local broker
get streaming                                             # buffer status and thresholds
get msg rules                                             # syslog rules
get msg brokers                                           # registered brokers
```

### Streaming thresholds

Incoming messages are buffered and flushed to files based on time and volume thresholds (default: 60 seconds or 
10,000 bytes):

```anylog
get streaming
set buffer threshold where time = 60 seconds and volume = 10000
set buffer threshold where write_immediate = true    # disable buffering
```

### Terminate subscriptions

```anylog
exit msg client [id]     # terminate a specific client
exit msg client all      # terminate all clients
```

### Debug
    
```anylog
set mqtt debug on        # print incoming messages to stdout
set mqtt debug off
trace level = 2 run message broker    # show source IP, port, and first 100 bytes of each message
```