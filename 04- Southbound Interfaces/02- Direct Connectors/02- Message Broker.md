---
title: "Message Broker"
description: Configure an AnyLog node as a message broker — enable it, subscribe via MQTT or Kafka, register reusable mapping policies, and confirm data lands in the local database.
layout: page
source_path: "background processes.md#message-broker"
---

<!---
### 📜 Change Log

| **Date** | **Name** | **Change** |
|---|---|---|
| 2026-07-20 | Eric Aquaronne | Added change log (both source docs) |
| 2026-07-24 | Ori Shadmon | Merged the "Message Broker" stub (enable command) and "Setting AnyLog as a Message Broker" example
  walkthrough into this single file. Restructured around dedicated MQTT and Kafka Message Client sections, each with
  a worked example, plus "Registering a Mapping Policy" (policy-based mapping as an alternative to inline topic
  mapping). Cross-linked rather than duplicated: full MQTT client / `bring` / QoS syntax reference lives in *Using a
  Message Broker*. |
--->

As described in the [networking](../../06-%20Networking%20&%20Security) section, AnyLog contains a built-in message broker that can be used for MQTT,
Kafka, REST, and other services — simply by defining the message-client mapping logic for the topic. Setting AnyLog
as a message broker is referenced as **Option B** in the Southbound Connectors diagram.

The [Northbound Interfaces](../../05-%20Northbound%20Connectors) cover using an AnyLog agent as a producer; this document covers AnyLog as a consumer.

This document demonstrates:
1. Configuring an AnyLog node as a broker.
2. Associating published data with a topic.
3. Mapping the data to a table structure (inline, or via a reusable mapping policy).
4. Confirming the data lands in the local database.

---

## Enable the Message Broker

```anylog
<run message broker where
    external_ip = [ip] and external_port = [port] and
    internal_ip = [local_ip] and internal_port = [local_port] and
    bind = [true/false] and threads = [threads count]>
```

The first IP/port pair binds to the external network; the second (optional) pair binds to the local network, if
applicable.

---

## MQTT Message Client

The MQTT Message client is "identical" to [REST POST](01-%20REST.md#publishing-data-via-post), except AnyLog is
both the MQTT message broker and MQTT message client.

When data is published on a broker, it's assigned to a **topic**. An AnyLog node can subscribe to messages published
on a third-party broker, or — if the same node is configured as a broker — to messages published on the AnyLog node
itself, using `run mqtt client`:

* If subscribing to a third-party broker, provide that broker's IP and port.
* If the same node acts as the broker, set `broker = local` and the process resolves that the data is published
  locally. This is also what happens automatically if you set `broker` to this node's own IP and the message
  broker's port — AnyLog resolves it to the same thing as `broker = local`.

**Sample Command**:
```anylog
<run msg client where
  broker=local and
  log=false and topic=(
   name=my-data and
   dbms="bring [dbms]" and
   table="bring [sensor]" and
   column.timestamp.timestamp="bring [timestamp]" and
   column.value.float="bring [value]"
)>
```

> **To verify:** the previous draft of this example included `user-agent=anylog`, which is the parameter used for
> **REST**-broker mode (`broker=rest and user-agent=anylog`), not local MQTT. I've removed it here since `broker=local`
> shouldn't need it — confirm that's correct before publishing, in case there's an MQTT-specific reason it was there.

**Subscribing to an external (third-party) broker** instead of AnyLog's own uses the same command, but with the
broker's address in place of `local` — and credentials if the broker requires them:

```anylog
<run msg client where
  broker=[broker ip or hostname] and
  port=[port] and
  user=[user] and
  password=[password] and
  log=false and topic=(
   name=my-data and
   dbms="bring [dbms]" and
   table="bring [sensor]" and
   column.timestamp.timestamp="bring [timestamp]" and
   column.value.float="bring [value]"
)>
```

* `broker` — the third-party broker's IP or hostname (required; this is what distinguishes it from `broker=local`).
* `port` — the broker's port (required for third-party brokers).
* `user` / `password` — only needed if the broker requires authentication; omit both for an open broker.

---

## Kafka Message Client

Similarly to MQTT, AnyLog can also act as a Kafka-like interface for data processing.

The `run kafka consumer` command subscribes to one or more Kafka topics and maps incoming messages to database
tables using the same column mapping syntax as MQTT.

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
<run kafka consumer where ip = local and reset = latest and topic = (
    name=my-data and
    dbms="bring [dbms]" and
    table="bring [sensor]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.value.float="bring [value]"
)>
```

> **To verify:** fixed a duplicated `and and` in this example. Also worth double-checking: the parameter table above
> lists `ip`/`port` as the Kafka broker's address, with no mention of a `local` shorthand the way MQTT has
> `broker = local`. Confirm `ip = local` is actually supported by `run kafka consumer` before publishing — if not,
> this example needs a real IP/port (or a documented local-broker convention for Kafka specifically).

---

## Registering a Mapping Policy

Rather than writing the topic's mapping inline on every `run msg client` call, you can register the mapping once as
a **policy** on the blockchain, and reference it by name. This is useful when the same mapping is reused across
multiple subscriptions, or when you want the mapping managed centrally rather than duplicated in each command.

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

Once inserted, `topic=(name=... and policy=!new_policy)` replaces the inline `dbms=... and table=... and column....`
parameters entirely — the mapping lives in the policy instead.

> **Fixed two bugs in this example:** (1) `"id"` was hardcoded as `"my-policy"`, ignoring the `policy_id` variable
> set right above it — now it references `!policy_id` so that variable actually does something. (2) The final
> command referenced `policy=!my_policy`, but the policy was defined as `!new_policy` — that variable name was never
> set, so the original example wouldn't have resolved. Now consistent throughout.

---

## Monitor

```anylog
get msg client      -- clients subscribed + messages processed by each
get msg broker      -- subscriptions per broker
```

For the full connection/config/topic parameter reference, QoS levels, the `bring` command, and debugging options
(`log`, `log_error`, `persist`, `set mqtt debug`), see **Using a Message Broker**.

---

## Confirm It's Working

Check the streaming buffers (data is held here until flushed):
```anylog
get streaming
```

Once buffers flush, query the data directly:
```anylog
run client () sql my_dbms format=table "select timestamp, value from rand_data"
```