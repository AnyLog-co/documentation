---
title: "Message Broker"
description: Configure an AnyLog node as a message broker — enable it, validate the binding, subscribe to topics, register reusable mapping policies, publish, and confirm data lands in the local database.
layout: page
source_path: "background processes.md#message-broker"
---

<!---
### 📜 Change Log

| **Date** | **Name** | **Change** |
|---|---|---|
| 2026-07-20 | Eric Aquaronne | Added change log (both source docs) |
| 2026-07-24 | Ori Shadmon | Merged the "Message Broker" stub (enable command) and "Setting AnyLog as a Message Broker" example
  walkthrough into this single file. Added a new "Registering a Mapping Policy" section (policy-based mapping as an
  alternative to inline topic mapping). Cross-linked rather than duplicated: full MQTT client / `bring` / QoS syntax
  reference lives in *Using a Message Broker*, Kafka specifics in *Kafka*, and TLS/mTLS setup in *Broker Setup TLS
  Example* — this doc covers the core enable → subscribe → map → publish → validate flow shared by all of them. |
--->

As described in the [networking]() section, AnyLog contains a built-in message broker that can be used for MQTT,
Kafka, REST, and other services — simply by defining the message-client mapping logic for the topic. Setting AnyLog
as a message broker is referenced as **Option B** in the Southbound Connectors diagram.

This document demonstrates:
1. Configuring an AnyLog node as a broker.
2. Associating published data with a topic.
3. Mapping the data to a table structure (inline, or via a reusable mapping policy).
4. Ingesting the data into a local database.

```anylog
get msg client      -- clients subscribed + messages processed by each
get msg broker      -- subscriptions per broker
```

For the full connection/config/topic parameter reference, QoS levels, the `bring` command, and debugging options
(`log`, `log_error`, `persist`, `set mqtt debug`), see **Using a Message Broker**.

The [Northbound Interfaces]() provide directions on how to use an AnyLog agent as a producer, where as this document 
discusses AnyLog as a consumer. 

### Enable the Message Broker

```anylog
<run message broker where 
    external_ip = [ip] and external_port = [port] and 
    internal_ip = [local_ip] and internal_port = [local_port] and 
    bind = [true/false] and threads = [threads count]>
```

The first IP/port pair binds to the external network; the second (optional) pair binds to the local network, if
applicable.


## MQTT Message Client 

The MQTT Message client is "identical" to the [REST POST](01-%20REST.md#publishing-data-via-post), except AnyLog is 
both the MQTT message broker and MQTT message client. 

When data is published on a broker, it's assigned to a **topic**. An AnyLog node can subscribe to messages published
on a third-party broker, or — if the same node is configured as a broker — to messages published on the AnyLog node
itself, using `run mqtt client`:

* If subscribing to a third-party broker, provide that broker's IP and port.
* If the same node acts as the broker, set `broker = local` and the process resolves that the data is published
  locally.


**Sample Command**: 
```anylog
<run msg client where 
  broker=local and user-agent=anylog and 
  log=false and topic=(
   name=my-data and
   dbms="bring [dbms]" and
   table="bring [sensor]" and
   column.timestamp.timestamp="bring [timestamp]" and
   column.value.float="bring [value]"
)>
```

If a user defines `broker` to the local IP + port to the Message broker port, it'll automatically be defined the same as `broker=local`

> If `run mqtt client` references the same IP/port used in the `run message broker` command, it's equivalent to
> writing `broker=local` explicitly.


## Kafka Message Client

Similarly to _MQTT_, AnyLog can also act as a kafka like interface for data processing. 

The `run kafka consumer` command subscribes to one or more Kafka topics and maps incoming messages to database tables using the same column mapping syntax as MQTT.

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

**Example**: 
```anylog
<run kafka consumer where ip = local and and reset = latest and topic = (
    name=my-data and
    dbms="bring [dbms]" and
    table="bring [sensor]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.value.float="bring [value]"
)>
```


## Registering a Mapping Policy

Rather than writing the topic's mapping inline on every `run msg client` call, you can register the mapping once as
a **policy** on the blockchain, and reference it by name. This is useful when the same mapping is reused across
multiple subscriptions, or when you want the mapping managed centrally rather than duplicated in each command.

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

run msg client where broker=local and log=false and topic=(name=my-topic and policy=!my_policy)
```

Once inserted, `topic=(name=... and policy=!my_policy)` replaces the inline `dbms=... and table=... and column....`
parameters entirely — the mapping lives in the policy instead.




