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

HiveMQ is a standard MQTT broker, so any MQTT client can publish to it. `hivemq_publisher.sh` publishes a random 
reading for three devices every second using `mosquitto_pub`. If `mosquitto_pub` is not installed, the script 
re-runs itself inside the `eclipse-mosquitto` Docker image, so only Docker is required.

```shell
#!/bin/sh
# hivemq_publisher.sh - publish random sensor readings to an MQTT broker (HiveMQ)
# Message: {"device_name":"sensor-1","timestamp":"2026-10-22T18:00:00Z","value":42.17}
#
# Usage:   ./hivemq_publisher.sh
# Options: BROKER=10.0.0.5 TOPIC=plant/line1 INTERVAL=5 ./hivemq_publisher.sh
#
# MODE=flat (default)  topic: sensors/data           payload: {"device_name":"sensor-1","timestamp":...,"value":...}
# MODE=uns             topic: sensors/data/sensor-1  payload: {"timestamp":...,"value":...}
#
# If mosquitto_pub is not installed locally, the script re-runs itself inside the
# eclipse-mosquitto Docker image (requires Docker).
#
# Save with LF line endings. If you see "$'\r': command not found", run:  sed -i 's/\r$//' hivemq_publisher.sh

if ! command -v mosquitto_pub >/dev/null 2>&1; then
  echo "mosquitto_pub not found locally - running inside eclipse-mosquitto container"
  tr -d '\r' < "$0" | docker run --rm -i --init --network host \
    -e BROKER -e PORT -e TOPIC -e INTERVAL -e DEVICES -e MODE \
    eclipse-mosquitto:2 sh -s
  exit $?
fi

BROKER=${BROKER:-localhost}
PORT=${PORT:-1883}
TOPIC=${TOPIC:-sensors/data}
INTERVAL=${INTERVAL:-1}
DEVICES=${DEVICES:-"sensor-1 sensor-2 sensor-3"}
MODE=${MODE:-flat}

echo "Publishing to ${BROKER}:${PORT} topic '${TOPIC}' (mode: ${MODE}) every ${INTERVAL}s (Ctrl+C to stop)"

while true; do
  for DEVICE in $DEVICES; do
    TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    R=$(( $(od -An -N2 -tu2 /dev/urandom) % 10000 ))
    VALUE=$(printf '%d.%02d' $((R / 100)) $((R % 100)))
    if [ "$MODE" = "uns" ]; then
      T="$TOPIC/$DEVICE"
      PAYLOAD=$(printf '{"timestamp":"%s","value":%s}' "$TS" "$VALUE")
    else
      T="$TOPIC"
      PAYLOAD=$(printf '{"device_name":"%s","timestamp":"%s","value":%s}' "$DEVICE" "$TS" "$VALUE")
    fi
    mosquitto_pub -h "$BROKER" -p "$PORT" -t "$T" -q 1 -m "$PAYLOAD" && echo "$T $PAYLOAD"
  done
  sleep "$INTERVAL"
done
```

Run it (Linux / macOS / Git Bash / WSL):

```shell
chmod +x hivemq_publisher.sh
./hivemq_publisher.sh

# override defaults
BROKER=10.0.0.5 TOPIC=plant/line1 INTERVAL=5 ./hivemq_publisher.sh

# device in the topic (UNS-style) - see Method 3
MODE=uns ./hivemq_publisher.sh
```

> **Windows:** save the script with **LF** line endings. If you see `$'\r': command not found`, run 
> `sed -i 's/\r$//' hivemq_publisher.sh`.

Sample output (`MODE=flat`, default):

```
sensors/data {"device_name":"sensor-1","timestamp":"2026-10-22T22:16:47Z","value":12.33}
sensors/data {"device_name":"sensor-2","timestamp":"2026-10-22T22:16:47Z","value":87.88}
```

Confirm the data reaches HiveMQ with the subscriber from the previous section (`-t 'sensors/#'`).


## Accepting Data in AnyLog

AnyLog subscribes to HiveMQ as a regular MQTT broker (Option A). `dynamic=true` does two things:

1. **Table name from the topic** – if no table name is provided, the table is generated from the topic.
2. **Unified Namespace (UNS)** – a namespace is built from the topic path and stored as `uns` / `object` policies.

Because the topic drives both, the topic layout decides the table layout:

| Method | Publisher topic | Device stored as | Tables |
|---|---|---|---|
| 1 – Inline mapping | `sensors/data` | `device_name` column | one |
| 2 – Mapping policy | `sensors/data` | `device_name` column, UNS grouped by device | one (`my_data`) |
| 3 – Device in topic | `sensors/data/<device>` | table name | one per device |

### Method 1 – Inline mapping (table from topic)

The table name is derived from the last level of the topic (`sensors/data` → `data_1`).

```anylog
<run msg client where
    broker=<HIVEMQ_IP> and
    port=1883 and
    log=false and
    master_node=!ledger_conn and
    topic=(
        name="sensors/#" and
        dbms=!default_dbms and
        dynamic=true and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.device_name.str = "bring [device_name]" and
        column.value.float = "bring [value]"
    )>
```

Resulting UNS (`blockchain get (uns, object)`):

```json
[{"object" : {"name" : "sensors", "description" : "object for MQTT sensors", "ledger" : "global"}},
 {"uns" : {"name" : "sensors", "namespace" : "sensors", "object_id" : "748c797a53ab937b51659573b7c20688"}},
 {"object" : {"name" : "data_1", "description" : "object for MQTT data_1", "dbms" : "mydb", "table" : "data_1"}},
 {"uns" : {"name" : "data", "namespace" : "sensors/data", "parent" : "0a8fd51f26b92f6966f11aa1f0161620",
           "object_id" : "0412966d267b13e8220694d168331d8a"}}]
```

### Method 2 – Mapping policy with `group_by_attributes`

The mapping is stored as a policy and referenced by `run msg client`. `group_by_attributes` lets the UNS 
objects be defined per attribute value (e.g. per `device_name`).

1. Declare the mapping policy:

```anylog
<new_policy = {
    "mapping": {
        "id": "my-data",
        "dbms": !default_dbms,
        "table": "my_data",
        "group_by_attributes": ["device_name"],
        "readings": "",
        "schema": {
            "timestamp": {"type": "timestamp", "bring": "[timestamp]"},
            "device_name": {"type": "string", "bring": "[device_name]"},
            "value": {"type": "float", "bring": "[value]"}
        }
    }
}>

process !local_scripts/node-deployment/policies/publish_policy.al
```

2. Subscribe using the policy:

```anylog
<run msg client where
    broker=<HIVEMQ_IP> and
    port=1883 and
    log=false and
    master_node=!ledger_conn and
    topic=(
        name="sensors/#" and
        policy="my-data" and
        dynamic=true
    )>
```

Resulting UNS – the object for `sensors/data` carries a `where` condition from the group-by attribute:

```json
{"object" : {"name" : "my_data", "description" : "object for MQTT sensors/data",
             "dbms" : "mydb", "table" : "my_data", "where" : "device_name = 'sensor-1'"}}
```

### Method 3 – Device in the topic (table per device)

Common in UNS deployments: the device is part of the topic and the payload holds only the reading. Run the 
publisher with `MODE=uns`:

```
sensors/data/sensor-1 {"timestamp":"2026-10-22T23:16:03Z","value":77.05}
sensors/data/sensor-2 {"timestamp":"2026-10-22T23:16:03Z","value":53.65}
```

With `dynamic=true` and no table name, each device topic becomes its own table and UNS node 
(`sensors/data/sensor-1`, `sensors/data/sensor-2`, ...):

```anylog
<run msg client where
    broker=<HIVEMQ_IP> and
    port=1883 and
    log=false and
    master_node=!ledger_conn and
    topic=(
        name="sensors/#" and
        dbms=!default_dbms and
        dynamic=true and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value.float = "bring [value]"
    )>
```

### Option B – HiveMQ forwards to AnyLog's message broker (Bridge)

Used when HiveMQ is the customer's central broker / UNS and should **push** data to AnyLog (e.g. AnyLog cannot 
reach HiveMQ). The <a href="https://docs.hivemq.com/hivemq-bridge-extension/latest/index.html" target="_blank">HiveMQ Enterprise Bridge Extension</a> 
ships with HiveMQ (disabled by default) and is covered by the Lab license. 

Data flow: `publisher → HiveMQ (sensors/#) → Bridge → AnyLog message broker → run msg client (broker=local)`

1. On AnyLog, make sure the message broker is running and note its port:

```anylog
get connections                  # "Messaging" line shows the broker IP:port
```

If it is not running:

```anylog
<run message broker where 
   external_ip = !external_ip and external_port = !anylog_broker_port and 
   internal_ip = !ip and internal_port = !anylog_broker_port and 
   bind = false and threads = 3
>
```

2. Stop any `run msg client` subscribed directly to HiveMQ (Option A), so data is not ingested twice, and 
   subscribe to AnyLog's local broker instead – any of Methods 1-3 with `broker=local` in place of 
   `broker=<HIVEMQ_IP> and port=1883`:

```anylog
<run msg client where
    broker=local and
    log=false and
    master_node=!ledger_conn and
    topic=(
        name="sensors/#" and
        policy="my-data" and
        dynamic=true
    )>
```

3. Create `bridge-config.xml` (replace `ANYLOG_IP` / `ANYLOG_BROKER_PORT`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  HiveMQ Enterprise Bridge Extension - forward sensors/# from HiveMQ to AnyLog's message broker.
  Location in the container: /opt/hivemq/extensions/hivemq-bridge-extension/conf/config.xml
  Replace ANYLOG_IP / ANYLOG_BROKER_PORT (AnyLog: `get connections` -> Messaging).
-->
<hivemq-bridge-extension>
    <bridges>
        <bridge>
            <name>hivemq-to-anylog</name>
            <remote-broker>
                <mqtt>
                    <!-- MQTT 3.1.1: AnyLog's broker is a lightweight broker; PUB mode supports 3.1.1 -->
                    <version>3</version>
                </mqtt>
                <authentication>
                    <mqtt-simple-authentication>
                        <client-identifier>hivemq-bridge</client-identifier>
                    </mqtt-simple-authentication>
                </authentication>
                <connection>
                    <static>
                        <host>ANYLOG_IP</host>
                        <port>ANYLOG_BROKER_PORT</port>
                    </static>
                </connection>
            </remote-broker>
            <topics>
                <topic>
                    <!-- PUB = HiveMQ -> AnyLog; topic is forwarded unchanged -->
                    <filter>sensors/#</filter>
                    <mode>PUB</mode>
                </topic>
            </topics>
        </bridge>
    </bridges>
</hivemq-bridge-extension>
```

4. Start HiveMQ with the config mounted, then enable the extension by removing its `DISABLED` file:

```shell
docker run --name hivemq \
  -p 8080:8080 \
  -p 1883:1883 \
  -e HIVEMQ_LICENSE_KEY='<HIVEMQ_LICENSE_KEY>' \
  -e HIVEMQ_LOG_BASED_CLUSTERING_ENABLED=true \
  -v "${PWD}/bridge-config.xml:/opt/hivemq/extensions/hivemq-bridge-extension/conf/config.xml" \
  --rm -d hivemq/hivemq4:latest

docker exec hivemq rm -f /opt/hivemq/extensions/hivemq-bridge-extension/DISABLED
docker logs -f hivemq            # look for the Bridge extension starting and connecting
```

> If the configuration is invalid, HiveMQ re-creates the `DISABLED` file and logs the error. 
> Without a license key the extension runs in a 5-hour trial.

5. Run the publisher against HiveMQ (unchanged – `./hivemq_publisher.sh`). Data now arrives in AnyLog through 
   its local broker; validate with the commands below.

## Validating

On the AnyLog node:

```anylog
get msg client                          # subscription status + message counters
blockchain get (uns, object)            # UNS generated from the topic hierarchy
blockchain get mapping                  # mapping policy (Method 2)
```

Query the data:

```anylog
AL anylog-standalone-operator +> run client () sql mydb format=table "SELECT * FROM my_data LIMIT 5;"

row_id insert_timestamp           tsd_name tsd_id timestamp           device_name value
------ -------------------------- -------- ------ ------------------- ----------- -----
     1 2026-10-22 16:08:36.190546      234      2 2026-10-22 16:07:31 sensor-1     43.4
     2 2026-10-22 16:08:36.190546      234      2 2026-10-22 16:07:31 sensor-2     5.09
     3 2026-10-22 16:08:36.190546      234      2 2026-10-22 16:07:31 sensor-3    54.13
     4 2026-10-22 16:08:36.190546      234      2 2026-10-22 16:07:36 sensor-1    78.62
     5 2026-10-22 16:08:36.190546      234      2 2026-10-22 16:07:36 sensor-2    10.73
```