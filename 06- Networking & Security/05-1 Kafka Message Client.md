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
 | 2026-08-11 | | Local Kafka for development (Docker container) section from earlier Using Kafka docs. |
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
message clients. See <a href="./05-%20MQTT%20Message%20Broker.md#mapping-json-payloads" target="_blank">MQTT Message Broker</a> for the JSON
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

## Local Kafka for development

Use a local Docker-based Kafka broker for testing consumer mappings without a production cluster.

### Start the broker

```bash
docker run -d --rm --name kafka-dev -p 9092:9092 apache/kafka:latest
```

> Use `localhost:9092` as `--bootstrap-server` when running Kafka CLI commands inside the container via `docker exec`. Use the broker machine's LAN IP (e.g. `192.168.1.101:9092`) when connecting from another host.

### Create a topic

```bash
docker exec kafka-dev /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --if-not-exists \
  --topic test --partitions 1 --replication-factor 1
```

### Publish a message

```bash
echo '{"timestamp":1776294106000,"value":42.0,"deviceID":"d1"}' | \
docker exec -i kafka-dev /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic test
```

### Verify messages

```bash
docker exec kafka-dev /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic test \
  --group "tmp-$(date +%s)" \
  --consumer-property auto.offset.reset=earliest \
  --max-messages 5
```

### Connect AnyLog and start consuming

On the Operator node, connect the database and start the consumer:

```anylog
connect dbms new_company where type = sqlite

<run kafka consumer where ip = localhost and
    port = 9092 and
    reset = earliest and
    topic = (name = test and
        dbms = new_company and
        table = kafka_demo and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value.float = "bring [value]" and
        column.deviceid.str = "bring [deviceID]")
>
```

Topic mapping for Kafka uses the same JSON/`bring` model as MQTT — see
<a href="./05-%20MQTT%20Message%20Broker.md#mapping-json-payloads" target="_blank">MQTT Message Broker</a> and
<a href="../04-%20Southbound%20Interfaces/02-%20Mapping%20Policy.md" target="_blank">Mapping Policy</a>.

**Verify data is flowing**:

```anylog
get streaming
sql new_company "select * from kafka_demo"
```

### Stop the broker

```bash
docker stop kafka-dev
```

The `--rm` flag on `docker run` removes the container automatically when it stops.

## Notes

Unlike MQTT's `broker = local` shorthand, Kafka has no AnyLog-local broker. For local testing, run a real Kafka
endpoint (see <a href="#local-kafka-for-development" target="_blank">Local Kafka for development</a>) and point `ip` / `port` at it
(for example `localhost` and `9092`).

For deployments that use both MQTT and Kafka, keep the topic-to-table naming rules consistent across consumers so
queries can target predictable AnyLog tables.

## Related

* <a href="./05-%20MQTT%20Message%20Broker.md" target="_blank">MQTT Message Broker</a>
* <a href="./05-2%20Connectors%20To%20Data%20Sources.md" target="_blank">Connectors To Data Sources</a>
* <a href="../04-%20Southbound%20Interfaces/08-%20Data%20Ingestion.md" target="_blank">Data Ingestion</a>
