---
title: "Message Broker"
description: AnyLog's built-in message broker — one of the network's three core services. Covers subscribing to MQTT/Kafka/REST sources, publishing, mapping, UNS policies, TLS, and debugging.
layout: page
source_path: "background processes.md#message-broker"
---

<!---
### 📜 Change Log
 **Date**   | **Name** | **Change** | **Version** |
 |------------|--|------------|----------|
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-25 | Ori Shadmon | Consolidated four previously separate documents into this single Networking &
   Security reference, per request: (1) this file's own prior content ("Using a Message Broker" — the deep
   connection/config/topic-param reference, QoS, `bring`, REST-broker mode, UNS policies, and debugging); (2)
   "02 Broker Setup Example.md" (the worked subscribe/publish/validate walkthrough); (3) "02-1 Broker Setup TLS
   Example.md" (MQTT TLS/mTLS setup); (4) the "Registering a Mapping Policy" section from the southbound
   Message Broker doc (policy-based mapping via the blockchain — genuinely new content not covered here
   before). The southbound "Message Broker" doc and the northbound "Data Forwarding" doc are being trimmed to
   summaries that link here, rather than maintaining three overlapping copies of the same mechanics.
   Fixed grammar throughout ("user are" → "users are", "ALl" → "All", "the the", "returns" → "is returned",
   missing "the" in a few places). **Flagging, not resolving:** this document (like several source docs before
   it) uses `run msg client` and `run mqtt client` interchangeably, sometimes in the same section, with no
   indication of whether these are true aliases or one is a typo carried forward repeatedly. Also flagging one
   port that doesn't match this doc set's established convention: `master_node = 10.0.0.185:2548` in the UNS
   example — every other Master TCP port example elsewhere is `32048`; `2548` looks like it may be missing a
   leading `3`, but I'm not certain enough to silently "fix" a working example.
--->

## Overview

AnyLog's message broker is one of the network's three core services (alongside TCP and REST — see
[Network Processing](B-%20Network%20Processing.md#network-services)). It's a TCP-based listener that can accept
data from different sources (MQTT, Kafka, Modbus, REST, etc.) from a single point, and understands how to interpret
each source based on a correlating message client (topic mapping) service.

There are three ways to configure a node around it:

* As a [subscriber to a third-party message broker](#subscribing-to-a-broker) — pulling data from an external MQTT/Kafka broker.
* As [the message broker itself](#enable-the-message-broker) — receiving data pushed directly from clients using standard APIs like MQTT.
* As a [broker receiving REST commands](#rest-broker-mode) — mapping data delivered over REST/POST to the needed schema, based on the provided topic.

In all three cases:

* Users can subscribe to and retrieve data from one or more topics on a broker.
* Users can publish data directly to an AnyLog node configured as a broker.
* When configured as a message broker, an AnyLog node can automatically generate UNS policies describing data
  relationships, enabling hierarchical navigation through the Unified Namespace — see
  [Generating UNS Policies](#generating-uns-policies).

---

## Enable the Message Broker

```anylog
<run message broker where 
    external_ip = [ip] and external_port = [port] and 
    internal_ip = [local_ip] and internal_port = [local_port] and 
    bind = [true/false] and threads = [threads count]>
```

The first IP/port pair binds to the external network; the second (optional) pair binds to the local network, if
applicable. `threads` defaults to `6`.

**Validate & monitor:**

```anylog
get connections        -- confirm the process is configured and bound
get broker              -- monitor messages received by the broker
get msg broker          -- monitor messages per topic by broker
get local broker        -- summary of messages processed on AnyLog as a broker (broker IP/port only — data
                        --   published via "local" is not included in this command's statistics)
```

**Helper commands** — if the broker process fails to bind:

```anylog
get ip list                                   -- list available IPs on the node
get machine connections                       -- list active connections + the process ID holding each socket
get machine connections where port = 7850     -- detail the process using a specific port
```

---

## Subscribing to a Broker

This process initiates a client that subscribes to a list of topics registered on a broker. When a new message is
added to the broker and matches a subscribed topic, the broker pushes the message to the AnyLog instance, where
it's mapped to a JSON structure and aggregated into files, processed according to the node's configuration (e.g.
ingested to a local database, or sent to another node). This message data is treated as **streaming data** — see
[File Mode and Streaming Mode](adding%20data.md#file-mode-and-streaming-mode).

### Command structure

```anylog
run msg client where [connection parameters] and [config parameters] and topic = (topic 1 params) and topic = (topic 2 params) ...
```

Options are `key = value` pairs joined with `and`. Providing `broker` is mandatory; everything else is optional
depending on the broker and how messages need to be processed. A single command can subscribe to multiple topics —
each topic's details go in their own parentheses.

There are three types of parameters:
1. **Connection params** — how to connect to the broker.
2. **Config params** — settings that apply to all messages, regardless of topic.
3. **Topic params** — the topic name and the rules for mapping the message so AnyLog can process it.

### Connection params

| Option | Details |
|---|---|
| `broker` | The URL or IP of the broker. Set to `local` to subscribe to this node's own broker instead of a third party. |
| `port` | The broker's port. Default `1883`. |
| `user` | The authorized user's name. |
| `password` | The password for that user. |
| `client_id` | A client ID associated with the account. |
| `project_id` | A project ID associated with the broker account. |
| `location` | A name identifying the service location. |
| `private_key` | A private key to authenticate requests. |

If `run msg client` references the same IP/port used in the `run message broker` command, it resolves the same as
`broker = local` explicitly.

### Config params

| Option | Details |
|---|---|
| `log` | `true`/`false` — output the broker log messages (the MQTT `on_log()` callback). No effect if this node *is* the broker. |
| `log_error` | `true` — log messages that failed to process to a file named `err_<broker ID>_<topic>` in the error directory. |
| `qos` | Quality of Service — default `0`. |
| `prep_dir` | Directory for organizing incoming message data. |
| `watch_dir` | The watch directory location. |
| `err_dir` | The error directory location. |
| `persist` | `true` — flush incoming messages to a file (named by broker ID + topic) instead of processing them, useful for capturing raw source data. |

### Topic params

| Option | Details |
|---|---|
| `name` | The topic to subscribe to. `#` subscribes to all topics — matching messages are processed per their own subscription; anything else is flushed to a log file. |
| `qos` | Per-topic QoS override — falls back to the Config-level value, then the default, if omitted. |
| `dbms` | The logical dbms for the topic's data, or a `bring` command to extract the name from the message. |
| `table` | The table name, or a `bring` command to extract it. |
| `column.[name].[type]` | A column name + data type, paired with a `bring` command extracting that column's value from the message. |
| `dynamic` | `true` — auto-generate [UNS policies](#generating-uns-policies) instead of using inline/explicit mapping. |
| `policy` | Reference a [reusable mapping policy](#registering-a-mapping-policy) instead of inline `dbms`/`table`/`column...` params. |

**Naming rule:** for both `dbms` and `table`, uppercase letters are converted to lowercase and spaces to underscores.

### QoS — Quality of Service

| Level | Meaning |
|---|---|
| `0` | No delivery guarantee — the recipient doesn't acknowledge receipt. Default. |
| `1` | Delivered at least once — the same message may arrive more than once. |
| `2` | Delivered exactly once — the highest guarantee. |

### The `bring` command

`bring` extracts data from a JSON structure — the same command used in blockchain queries elsewhere in AnyLog. See
[JSON Data Transformation](json%20data%20transformation.md#json-data-transformation) for the full syntax.

**Mapping the message data:**

| Field | Command form | Comments |
|---|---|---|
| `dbms` | `dbms=value` or `dbms=[bring command]` | Uppercase→lowercase, space→underscore |
| `table` | `table=value` or `table=[bring command]` | Uppercase→lowercase, space→underscore |
| `column` | `column.[name].[type] = [bring command]` | One entry per column |

**Column value/type — two equivalent forms:**

```anylog
# Form 1: type in the key, value via bring
column.value.float = "bring [readings][][value]"

# Form 2: type and value both via bring
column.value = (value="bring [readings][][value]" and type="bring [readings][][valueType]")
```

Supported data types: `str`, `int`, `float`, `timestamp`, `bool`.

By default, an error is returned if a `bring` command fails to produce a value. Set `optional = true` on that
column to continue processing without erroring instead:

```anylog
column.info = (type=str and value="bring [info]" and optional=true)
```

**Examples:**
```anylog
dbms = machines_data
table = "bring [metadata][machine_name] _ [metadata][serial_number]"
column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]"
```

### Worked example — subscribing to a third-party broker

```anylog
<run msg client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo
    and log = false and topic = (
        name = test and 
        dbms = "bring [metadata][company]" and 
        table = "bring [metadata][machine_name] _ [metadata][serial_number]" and 
        column.timestamp.timestamp = "bring [ts]" and 
        column.value = (type=int and value="bring [value]")
)>
```

### Worked example — subscribing to this node's own broker

```anylog
<run mqtt client where broker=local and log=false and topic=(name=mqtt-test and dbms=my_dbms and table=rand_data and column.timestamp.timestamp=now and column.value.float='bring [readings][][value]')>
```

Equivalent, written with an explicit IP/port that happens to match this node's own broker (`10.0.0.78:7850`):

```anylog
<run mqtt client where broker=10.0.0.78 and port=7850 and log=false and topic=(name=mqtt-test and dbms=my_dbms and table=rand_data and column.timestamp.timestamp=now and column.value.float='bring [readings][][value]')>
```

---

## Kafka Message Client

AnyLog can also act as a Kafka-like interface, using the same column-mapping syntax as MQTT.

| Option | Description | Default |
|---|---|---|
| `ip` | Kafka broker IP | |
| `port` | Kafka broker port | |
| `reset` | Offset policy: `latest` or `earliest` | `latest` |
| `topic` | One or more topics with mapping instructions | |

```anylog
<run kafka consumer where 
    ip = [ip] and 
    port = [port] and 
    reset = [latest|earliest] and 
    topic = [topic and mapping instructions]>
```

**Example:**
```anylog
<run kafka consumer where ip = [ip] and port = [port] and reset = latest and topic = (
    name=my-data and
    dbms="bring [dbms]" and
    table="bring [sensor]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.value.float="bring [value]"
)>
```

> **To verify:** unlike MQTT's `broker = local` shorthand, nothing here documents an equivalent for a Kafka
> consumer pointed at this node's own broker. Use a real `ip`/`port` until that's confirmed.

---

## Registering a Mapping Policy

Rather than writing a topic's mapping inline on every `run msg client` call, register the mapping once as a
**policy** on the blockchain and reference it by name — useful when the same mapping is reused across multiple
subscriptions, or when you want it managed centrally.

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

blockchain insert where policy=!new_policy and local=true and master=!ledger_conn

run msg client where broker=local and log=false and topic=(name=my-topic and policy=!new_policy)
```

Once inserted, `topic=(name=... and policy=!new_policy)` replaces the inline `dbms=... and table=... and column...`
parameters entirely — the mapping lives in the policy instead.

---

## REST-Broker Mode

Lets you map data streamed to AnyLog over REST to the needed schema, based on a topic — no third-party broker
involved at all. Requires two settings:

1. `broker = rest` — data delivered to the REST server via `POST` is mapped as defined in the topic assignment.
2. `user-agent = anylog` — identifies the target API so the call is routed to AnyLog's native process.

```anylog
run msg client where broker = rest and user-agent = anylog and [config parameters] and topic = (topic 1 params) and topic = (topic 2 params) ...
```

**Subscribe:**
```anylog
run msg client where broker = rest and user-agent=anylog and user = mqwdtklv and password = uRimssLO4dIo and topic = (name = test and dbms = "bring [metadata][company]" and table = "bring [metadata][machine_name] _ [metadata][serial_number]" and column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]")
```

**Publish via REST:**
```shell
curl --location --request POST '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: data' \
--header 'topic: test' \
--header 'Content-Type: text/plain' \
--data-raw '[{"value":210,
            "ts":1607959427550,
            "protocol":"modbus",
            "measurement":"temp02",
            "metadata":{
                    "company":"Anylog",
                    "machine_name":"cutter 23",
                    "serial_number":"1234567890"}}]'
```

### Debugging REST-broker POST calls

```anylog
trace level = 1 run rest server    -- shows the REST command issued by a client
trace level = 2 run rest server    -- also shows headers and message body
```

---

## Generating UNS Policies

Setting `dynamic = true` on a topic (in message-broker mode) enables automatic generation of UNS policies
describing data relationships, letting users navigate the data hierarchically through the Unified Namespace.

* There are no inline mapping instructions or mapping policies in this mode — table names are generated
  automatically from the topics.
* If the data is JSON, the entire object is ingested: attribute names → column names, attribute values → column
  values.
* If the data isn't JSON, column names are derived from the topic structure (the last segment of each topic).
* The **UNS Streamer** must be enabled in this mode (see below) — it periodically writes the updated data.

```anylog
BROKER = "virtualfactory.proveit.services"
PORT = 1883
USERNAME = "proveitreadonly"
PASSWORD = "proveitreadonlypassword"
default_dbms = my_dbms

<run msg client where 
	broker = !BROKER and port=!PORT and 
	user = !USERNAME and password = !PASSWORD and 
	master_node = 10.0.0.185:2548 and
	topic = (
		name="Enterprise B/Site1/#" and 
		dbms=proveit and 
		dynamic = true 
	)>
```

> **Worth double-checking:** `master_node = 10.0.0.185:2548` — every other Master TCP port example in this doc set
> uses the `32xxx` convention (e.g. `32048`). `2548` doesn't match that pattern and may be missing a leading `3`.

### Enabling the UNS Streamer

```anylog
run uns streamer where frequency = [time in seconds]
```

```anylog
run uns streamer
run uns streamer where frequency = 3
```

---

## Publishing Data

With a broker configured and a subscription mapping in place, data assigned to that topic gets processed according
to the subscription's rules. Two ways to publish:

### Direct MQTT publish

```anylog
mqtt publish where broker = [url] and port = [port] and user = [user] and password = [password] and topic = [topic] and qos = [value] and message = [message]
```

If the broker and publishing node are the same, use `broker = local` to send directly without network overhead:

```anylog
mqtt publish where broker = local and topic = [topic] and qos = [value] and message = [message]
```

**Plain string example:**
```anylog
mqtt publish where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = test and message = "hello world"
```

### Publishing structured JSON data

For anything beyond a quick string test — or to simulate a device sending a real reading — define the message as a
JSON object first, then reference it by variable name:

```anylog
<message = {"value":210,
            "ts":1607959427550,
            "protocol":"modbus",
            "measurement":"temp02",
            "metadata":{
                    "company":"Anylog",
                    "machine_name":"cutter 23",
                    "serial_number":"1234567890"}}>
```

The `< >` wrapper lets the AnyLog CLI treat this multi-line JSON as a single command — paste the block directly
into the CLI as-is. Validate the structure before publishing:

```anylog
json !message test
```

**Publish it** — `!message` refers back to the variable just defined:

```anylog
mqtt publish where broker = !ip and port = 7850 and user = mqwdtklv and password = uRimssLO4dIo and topic = test and message = !message
```

The data is received by the node as a broker (on the IP/port configured in `run message broker`), then processed
by the mapping instructions tied to the topic declared in the corresponding `run msg client` command.

---

## MQTT over TLS (mTLS)

For securing MQTT with certificate-based client authentication, in brief:

1. **Create a CA** for self-signed TLS certificates (`id generate certificate authority`).
2. **Create and sign a server certificate request** (`id generate certificate request` → `id sign certificate request`), writing `.crt`/`.key`/`.csr`/`.pem` files under `!pem_dir`.
3. **Start the broker with TLS enabled:**
   ```anylog
   <run message broker where external_ip = [ip] and external_port = 8883 and threads = 6
     and enable_tls = true
     and tls_cert = ./data/pem/server_tls.crt
     and tls_key = ./data/pem/server_tls.key
     and users_ca = ./data/pem/CA_users.crt
     and allowed_users = (user1, user2)
   >
   ```
   `allowed_users` is optional — when set, the listed names are the **CN** values in client certificates permitted
   to connect. `users_ca` is the CA that issued the *client* certificates (mTLS) — typically provided by the
   connecting organization, not the same file as the broker's own listener CA.
4. **Issue user certificates** for the connecting organization (one CA-signed cert/key pair per user), sharing only
   the user cert/key pairs and the broker's public CA cert — never any private key beyond what that user needs.
5. **Subscribe locally** the same way as any local broker subscription (see above).
6. **Publish from a TLS client** (e.g. `mosquitto_pub --cafile ... --cert ... --key ...`, or MQTT Explorer with the
   CA/cert/key configured in its connection settings).
7. **(Optional) Share the CA in the blockchain** — publish the organization's CA public certificate as a `ca`
   policy, and load `users_ca` from that policy at broker startup instead of a static file path.

> This section is condensed from a much more detailed worked example (full commands, directory structure, and a
> blockchain-based CA-sharing walkthrough) — see **Broker Setup TLS Example** for the complete version, including
> [mosquitto-tls](https://mosquitto.org/man/mosquitto-tls-7.html) reference links.

---

## Debugging

* **`log = true`** on `run msg client` — enables the MQTT `on_log()` callback, displaying MQTT processing/calls for
  third-party brokers. No effect if this node is the broker.
* **`set mqtt debug on/off`** — streams incoming messages and processing status to stdout.
* **`persist = true`** on a topic — flushes incoming messages to a file (named by broker ID + topic) instead of
  processing them.
* **`log_error = true`** on `run msg client` — writes failed-to-process messages to `err_<broker ID>_<topic>` in
  the error directory.
* **Subscribing to `#`** — matches all topics; anything with an actual subscription is processed normally,
  everything else is flushed to a log file.

---

## Validating Data Storage

```anylog
get databases                                          -- confirm the logical dbms maps to a physical database
get processes                                          -- confirm Operator config
get operator                                           -- track Operator status
get streaming                                          -- view streaming buffer status
get tables where dbms=*                                -- tables created
get columns where dbms=my_dbms and table=rand_data     -- columns created
get msg clients                                        -- status/config of all subscribed clients
get msg client where id = [n]                          -- status/config of one client
```

Once buffers flush, query the data directly:
```anylog
run client () sql my_dbms format=table "select timestamp, value from rand_data"
run client () sql my_dbms format=table and extend=(+ip, +node_name) "select count(*) from rand_data"
```

**Terminating clients:**
```anylog
exit msg client [ID/all]
```

---

## Related

* **Network Processing** — the three core network services (TCP, REST, Broker), and how `NETWORK_TYPE`/`NIC_TYPE`/binding determine reachability.
* **Broker Setup TLS Example** — full mTLS setup walkthrough.
* **Using REST** — the REST GET/POST reference this doc's REST-broker mode builds on.