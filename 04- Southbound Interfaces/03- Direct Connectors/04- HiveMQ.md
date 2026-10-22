---
title: HiveMQ
description: HiveMQ as a southbound service to AnyLog 
layout: page
source_path: "04- HiveMQ.md"
---

<!---
### 📜 Change Log
 **Date**   | **Name** | **Change**       | **Version** |
 |------------|--|------------------|----------|
 | 2026-10-22 |  | Created document |  |
 | 2026-10-22 | Ori Shadmon | utilize Claude to build documentation file + testing | | 
 | 2026-10-22 | Ori Shadmon | replaced HiveMQ Platform simulator with shell publisher | | 
--->

# HiveMQ 

HiveMQ helps industrial organizations move faster and operate smarter by turning industrial data into real-time 
intelligence and autonomous action at the edge.

* <a href="https://docs.hivemq.com/hivemq/latest/user-guide/" target="_blank">HiveMQ Documentation</a>
* <a href="https://hub.docker.com/u/hivemq" target="_blank">HiveMQ Docker</a>

There are two ways to get data from HiveMQ into AnyLog:

| Option | Data flow | Requires |
|---|---|---|
| **A. AnyLog subscribes to HiveMQ** | Publisher → HiveMQ → `run msg client` (broker = HiveMQ IP) | Nothing extra – simplest |
| **B. HiveMQ forwards to AnyLog** | Publisher → HiveMQ → (Bridge / Kafka extension) → AnyLog local broker or Kafka → `run msg client` / `run kafka consumer` | HiveMQ Enterprise Bridge or Kafka extension (trial mode in the `hivemq4` image) |

Option A is recommended for testing. Option B is useful when AnyLog should be the endpoint that HiveMQ pushes to 
(e.g. AnyLog's broker is reachable but HiveMQ is behind a firewall).

## Deploying HiveMQ 

1. Deploy HiveMQ (via Docker). A free account on <a href="https://www.hivemq.com/" target="_blank">hivemq.com</a> 
   (**Try HiveMQ** → **Download HiveMQ Software** → **Docker**) generates a 30-day Lab license key and the matching 
   `docker run` command:

```shell
docker run --name hivemq \
  -p 8080:8080 \
  -p 1883:1883 \
  --pull=always \
  -e HIVEMQ_LICENSE_KEY='<HIVEMQ_LICENSE_KEY>' \
  -e HIVEMQ_LOG_BASED_CLUSTERING_ENABLED=true \
  --rm -d hivemq/hivemq4:latest
```

* `1883` – MQTT listener (publishers and AnyLog connect here)
* `8080` – HiveMQ Control Center

> **Without an account:** drop the two `-e` lines – HiveMQ starts in trial mode (limited connections), which is 
> enough for this integration. `hivemq/hivemq-ce` is the fully open-source option (MQTT only, no Control Center).

2. Goto Website: http://localhost:8080/ (**username**: admin | **password**: hivemq)

3. Validate the broker is accepting connections using the HiveMQ MQTT CLI – subscribe in one terminal: 

```shell
docker run --rm -it --network host hivemq/mqtt-cli \
  sub -h localhost -p 1883 -t 'sensors/#' -T
```

and publish a test message from a second terminal:

```shell
docker run --rm --network host hivemq/mqtt-cli \
  pub -h localhost -p 1883 -t sensors/test -m '{"timestamp": "2026-10-22T10:00:00Z", "value": 1.0}'

```

The message should appear in the subscriber, and the client should show up under **Clients** in the Control Center.

> If `--network host` is not available in your Docker setup, drop it and replace `localhost` with 
> `host.docker.internal`.

## Publishing Data

HiveMQ is a standard MQTT broker, so any MQTT client can publish to it. The script below 
(`hivemq_publisher.sh`) publishes a random reading for three devices every second, using `mosquitto_pub` inside 
the `eclipse-mosquitto` image – nothing to install locally.

```shell
#!/bin/sh
# hivemq_publisher.sh - publish random sensor readings to an MQTT broker
BROKER=${BROKER:-localhost}
PORT=${PORT:-1883}
TOPIC=${TOPIC:-sensors/data}
INTERVAL=${INTERVAL:-1}
DEVICES=${DEVICES:-"sensor-1 sensor-2 sensor-3"}

echo "Publishing to ${BROKER}:${PORT} topic '${TOPIC}' every ${INTERVAL}s (Ctrl+C to stop)"

while true; do
  for DEVICE in $DEVICES; do
    TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    R=$(( $(od -An -N2 -tu2 /dev/urandom) % 10000 ))
    PAYLOAD=$(printf '{"device_name":"%s","timestamp":"%s","value":%d.%02d}' "$DEVICE" "$TS" $((R / 100)) $((R % 100)))
    mosquitto_pub -h "$BROKER" -p "$PORT" -t "$TOPIC" -q 1 -m "$PAYLOAD" && echo "$TOPIC $PAYLOAD"
  done
  sleep "$INTERVAL"
done
```

Run it from the directory containing the script (Linux / macOS / PowerShell):

```shell
docker run --rm -it --network host \
  -v "${PWD}:/scripts" \
  --entrypoint sh eclipse-mosquitto:2 /scripts/hivemq_publisher.sh
```

Override defaults with environment variables, e.g. `-e BROKER=10.0.0.5 -e TOPIC=plant/line1 -e INTERVAL=5`.

> **Windows:** save the script with **LF** line endings (not CRLF), otherwise `sh` fails with `$'\r'` errors.

Sample output / message:

```
sensors/data {"device_name":"sensor-1","timestamp":"2026-10-22T22:16:47Z","value":12.33}
sensors/data {"device_name":"sensor-2","timestamp":"2026-10-22T22:16:47Z","value":87.88}
```

Confirm the data reaches HiveMQ with the subscriber from the previous section (`-t 'sensors/#'`).

### Alternative – Python Publisher

The same data using Python (`pip install paho-mqtt`):

```python
# hivemq_publisher.py   ->   pip install paho-mqtt
import json, random, time
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

BROKER = "localhost"      # HiveMQ host
PORT = 1883
TOPIC = "sensors/data"
DEVICES = ["sensor-1", "sensor-2", "sensor-3"]

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="anylog-demo-publisher")
client.connect(BROKER, PORT)
client.loop_start()

try:
    while True:
        for device in DEVICES:
            payload = {
                "device_name": device,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "value": round(random.uniform(0, 100), 2),
            }
            client.publish(TOPIC, json.dumps(payload), qos=1)
            print(TOPIC, payload)
        time.sleep(5)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
```

## Accepting Data in AnyLog

The policies below map the publisher's message into table `hivemq_sensor`. 
Use `!default_dbms` or replace it with your logical database name.

### Option A – Subscribe directly to HiveMQ

AnyLog acts as an MQTT client of the HiveMQ broker.

```anylog
<run msg client where 
   broker = <HIVEMQ_IP> and 
   port = 1883 and 
   log = false and 
   topic = (
      name = sensors/data and 
      dbms = !default_dbms and 
      table = hivemq_sensor and 
      column.timestamp.timestamp = "bring [timestamp]" and 
      column.device_name = (type = str and value = "bring [device_name]") and 
      column.value = (type = float and value = "bring [value]")
   )
>
```

If HiveMQ authentication is enabled, add `user = <USER> and password = <PASSWORD>` to the `where` clause.

### Option B (MQTT) – HiveMQ forwards to AnyLog's local broker

> **Untested** – Bridge / Kafka forwarding is documented from HiveMQ's docs only; validate Option A first.

1. Enable the message broker on the AnyLog node (skip if already running): 

```anylog
<run message broker where 
   external_ip = !external_ip and external_port = !anylog_broker_port and 
   internal_ip = !ip and internal_port = !anylog_broker_port and 
   bind = false and threads = 3
>
```

2. Configure the HiveMQ Enterprise Bridge Extension 
   (<a href="https://docs.hivemq.com/hivemq-bridge-extension/latest/index.html" target="_blank">docs</a>) to forward `sensors/#` to AnyLog. 
   Sample bridge configuration (verify element names against the extension version you deploy):

```xml
<hivemq-bridge-extension>
    <bridges>
        <bridge>
            <name>anylog</name>
            <remote-broker>
                <connection>
                    <static>
                        <host>ANYLOG_IP</host>
                        <port>ANYLOG_BROKER_PORT</port>
                    </static>
                </connection>
            </remote-broker>
            <topics>
                <topic>
                    <filter>sensors/#</filter>
                </topic>
            </topics>
        </bridge>
    </bridges>
</hivemq-bridge-extension>
```

3. Subscribe to the forwarded topic on AnyLog's local broker:

```anylog
<run msg client where 
   broker = local and 
   log = false and 
   topic = (
      name = sensors/data and 
      dbms = !default_dbms and 
      table = hivemq_sensor and 
      column.timestamp.timestamp = "bring [timestamp]" and 
      column.device_name = (type = str and value = "bring [device_name]") and 
      column.value = (type = float and value = "bring [value]")
   )
>
```

> If the bridge adds a prefix to forwarded topics, use the prefixed name (e.g. `hivemq/sensors/data`) in `name`.

### Option B (Kafka) – HiveMQ forwards to Kafka

The <a href="https://docs.hivemq.com/hivemq-kafka-extension/latest/index.html" target="_blank">HiveMQ Enterprise Extension for Kafka</a> 
writes MQTT messages from `sensors/#` into a Kafka topic (e.g. `hivemq-sensors`). The MQTT payload is forwarded 
as the Kafka record value, so the same JSON mapping applies.

> `run kafka consumer` connects to a Kafka cluster – point `ip` / `port` at the Kafka bootstrap server that 
> HiveMQ writes to.

```anylog
<run kafka consumer where 
   ip = <KAFKA_IP> and 
   port = 9092 and 
   reset = latest and 
   log = false and 
   topic = (
      name = hivemq-sensors and 
      dbms = !default_dbms and 
      table = hivemq_sensor and 
      column.timestamp.timestamp = "bring [timestamp]" and 
      column.device_name = (type = str and value = "bring [device_name]") and 
      column.value = (type = float and value = "bring [value]")
   )
>
```

## Validating

On the AnyLog node:

```anylog
get msg client                         # subscription status + message counters
get streaming                          # data being buffered for the table 
get operator                           # rows inserted (operator node)
```

Query the data:

```anylog
run client () sql !default_dbms format=table "select device_name, min(value), max(value), count(*) from hivemq_sensor group by device_name"
```