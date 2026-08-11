---
title: "Kafka Message Client"
description: Configure AnyLog to consume Kafka topics and map Kafka messages into AnyLog tables.
layout: page
source_path: "background processes.md#message-broker"
---

<!---
### Change Log
 **Date**   | **Name** | **Change** | **Version** |
 |------------|--|------------|----------|
 | 2026-08-10 | | Split Kafka content out of the MQTT Message Broker page. |
--->

## Overview

AnyLog can subscribe to Kafka topics and ingest Kafka messages into local tables using the same mapping model used
by MQTT message clients. The Kafka consumer reads messages from a Kafka broker, applies the configured topic
mapping, and sends the resulting rows through AnyLog's normal streaming and storage workflow.

Use Kafka when the source system already publishes to Kafka, when Kafka is the site's event backbone, or when
Kafka-specific retention and consumer-group behavior are part of the deployment. Use MQTT when publishers are
lightweight devices or MQTT brokers are already deployed at the edge.

## Run a Kafka Consumer

```anylog
<run kafka consumer where
    ip = [ip] and
    port = [port] and
    reset = [latest|earliest] and
    topic = (
        name = [topic] and
        dbms = [dbms mapping] and
        table = [table mapping] and
        column.[name].[type] = [value mapping]
    )>
```

## Options

| Option | Description | Default |
|---|---|---|
| `ip` | Kafka broker IP address. | |
| `port` | Kafka broker port. | |
| `reset` | Offset policy. Use `latest` to consume new messages only, or `earliest` to consume available retained messages. | `latest` |
| `topic` | One or more topic blocks with mapping instructions. | |

Topic mapping supports the same `dbms`, `table`, `column.[name].[type]`, and `bring` expressions used by MQTT
message clients. See [MQTT Message Broker](./05-%20MQTT%20Message%20Broker.md#mapping-json-payloads) for the JSON
mapping syntax.

## Example

```anylog
<run kafka consumer where
    ip = [ip] and
    port = [port] and
    reset = latest and
    topic = (
        name = my-data and
        dbms = "bring [dbms]" and
        table = "bring [sensor]" and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value.float = "bring [value]"
    )>
```

After data is ingested, query it through the AnyLog network:

```anylog
run client () sql [dbms] format=table and extend=(+ip, +node_name, @table_name) "select * from [table] limit 10"
```

## Notes

Unlike MQTT's `broker = local` shorthand, this Kafka consumer syntax expects a concrete Kafka broker `ip` and
`port`. Use the actual Kafka endpoint until a local Kafka shorthand is explicitly documented.

For deployments that use both MQTT and Kafka, keep the topic-to-table naming rules consistent across consumers so
queries can target predictable AnyLog tables.

## Related

* [MQTT Message Broker](./05-%20MQTT%20Message%20Broker.md)
* [Connectors To Data Sources](./05-2%20Connectors%20To%20Data%20Sources.md)
* [Data Ingestion](../04-%20Southbound%20Interfaces/08-%20Data%20Ingestion.md)
