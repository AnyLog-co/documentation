---
title: Kafka
description: Configure AnyLog as a Kafka consumer to ingest data, or as a producer to direct query results to a Kafka topic.
layout: page
---


<!---
### 📜 Change Log
 **Date**   | **Name** | **Change**    | **Version** |
 |------------|--|---------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-22 | Ori | file cleanup  |  |
 | 2026-07-22 | Massimiliano | file cleanup  |  |
 | 2026-07-17 |  | file creation |  |
--->

AnyLog interacts with Kafka in two directions:

- **[Consumer](#consumer--ingest-from-kafka)** — subscribe to Kafka topics and ingest messages into local databases
- **[Producer](#producer--send-query-results-to-kafka)** — direct query result sets to a Kafka topic

---

## Consumer — ingest from Kafka

The `run kafka consumer` command subscribes to one or more Kafka topics and maps incoming messages to database tables using the same column mapping syntax as MQTT.

```anylog
run kafka consumer where ip = [ip] and port = [port] and reset = [latest|earliest] and topic = [topic and mapping instructions]
```

| Option | Description | Default |
|---|---|---|
| `ip` | Kafka broker IP | |
| `port` | Kafka broker port | |
| `reset` | Offset policy: `latest` or `earliest` | `latest` |
| `topic` | One or more topics with mapping instructions | |

### Single table example

```anylog

```

### Dynamic table mapping

Use a `bring` expression for `table` to route messages into different tables based on a field value — for example one table per device:

```anylog
<run kafka consumer where ip = 198.74.50.131 and
    port = 9092 and
    topic = (name = stream1 and
        dbms = new_company and
        table = "bring kafka_stream _ [deviceID]" and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value.float = "bring [value]" and
        column.deviceid.str = "bring [deviceID]")
>
```

A message with `"deviceID": "d1"` is stored in `kafka_stream_d1`; `"deviceID": "d2"` goes to `kafka_stream_d2`, and so on. Tables are created automatically if `create_table = true` is set on the Operator.

### Monitor the consumer

```anylog
get msg client          # subscription config and message counts
get streaming           # buffer status per dbms.table
get operator            # ingestion stats
get processes           # confirm Kafka consumer is running
```

---

## Producer — send query results to Kafka

Any AnyLog query result set can be directed to a Kafka topic by adding `dest = kafka@[ip]:[port]` and `topic = [topic]` to the query:

```anylog
run client () sql [dbms] format = json:list and stat = false and dest = kafka@[ip]:[port] and topic = [topic] "[sql query]"
```

Example — send 10 rows from a table to a Kafka instance:

```anylog
run client () sql litsanleandro format = json:list and stat = false and dest = kafka@198.74.50.131:9092 and topic = ping_data "select device_name, timestamp, value from ping_sensor where timestamp > now() - 1 day limit 10"
```

- `format = json:output` — formats each row as a JSON object
- `dest = kafka@[ip]:[port]` — routes output to the Kafka broker
- `topic` — the Kafka topic that receives the data

---

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

> <a href="{{ '/docs/Managing-Data-Southbound/mapping-policies/' | relative_url }}">Mapping Policies</a> define how to interpret incoming data from Kafka — the same way they work for MQTT and REST POST requests.

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