---
title: EdgeX Integration
description: Connect EdgeX Foundry to AnyLog as a southbound data source using MQTT.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlink
--> 

[EdgeX Foundry](https://www.edgexfoundry.org) is an open source, vendor-neutral edge computing framework under the LF Edge umbrella. It provides a southbound platform for connecting IoT devices using standard protocols including Modbus, MQTT, BACnet, SNMP, OPC-UA, REST, and more.

Integration between EdgeX and AnyLog is achieved by configuring EdgeX to publish sensor data to an MQTT broker — either a third-party broker or an AnyLog node acting as the broker — and having AnyLog subscribe to that broker to ingest the data.

> **EdgeX version note:** This guide is written for EdgeX 3.x/4.x (Napa / Odesa). EdgeX 4.0 uses MQTT as the default internal message bus and PostgreSQL as its default database. If you are running an older EdgeX release, API ports and endpoint paths will differ.

---

## Integration options

### Option A — AnyLog as the MQTT broker (direct)

Configure EdgeX to publish directly to an AnyLog node running the message broker service. No third-party broker needed. The AnyLog node receiving data can be an Operator (stores data locally) or a Publisher (routes data to Operators).

```
EdgeX  →  AnyLog Message Broker  →  AnyLog Operator
```

### Option B — Third-party broker

Configure EdgeX to publish to an external MQTT broker (e.g. [Eclipse Mosquitto](https://mosquitto.org/), HiveMQ), and configure AnyLog to subscribe to that broker.

```
EdgeX  →  MQTT Broker (Mosquitto / HiveMQ)  →  AnyLog msg client
```

---

## Prerequisites

- EdgeX deployed via Docker (see [EdgeX Quick Start](https://docs.edgexfoundry.org/latest/getting-started/quick-start/))
- An AnyLog node with TCP, REST, Streamer, and Operator services running — see <a href="{{ '/docs/Network-Services/background-services/' | relative_url }}">Background Services</a>
- For Option A: the AnyLog Message Broker service running on the receiving node

---

## Option A — AnyLog as broker

### 1. Start the AnyLog message broker

On the AnyLog node that will receive EdgeX data:

```anylog
<run message broker where
    external_ip = !external_ip and external_port = !anylog_broker_port and
    internal_ip = !ip and internal_port = !anylog_broker_port and
    bind = false and threads = 6>
```

Verify it is running:
```anylog
get processes       # MSG Broker row should show Running
get local broker
```

### 2. Subscribe to the EdgeX topic

Map the incoming EdgeX event structure to an AnyLog database table. The `broker=local` keyword tells AnyLog to subscribe to its own broker:

```anylog
<run msg client where
    broker = local and
    log = false and
    topic = (
        name = anylogEdgeX and
        dbms = edgex and
        table = "bring [device]" and
        column.timestamp.timestamp = now and
        column.value.float = "bring [readings][][value]" and
        column.name.str = "bring [readings][][name]"
    )>
```

Verify the subscription:
```anylog
get msg clients
```

### 3. Configure EdgeX to publish to AnyLog

In your EdgeX deployment, add an **application service** (app-service-configurable) configured to export events to your AnyLog broker address. In your `docker-compose.override.yml`:

```yaml
app-mqtt-export:
  container_name: edgex-app-mqtt-export
  environment:
    EDGEX_PROFILE: mqtt-export
    EDGEX_SECURITY_SECRET_STORE: "false"
    SERVICE_HOST: edgex-app-mqtt-export
    WRITABLE_PIPELINE_FUNCTIONS_MQTTEXPORT_PARAMETERS_BROKERADDRESS: tcp://[anylog-node-ip]:[broker-port]
    WRITABLE_PIPELINE_FUNCTIONS_MQTTEXPORT_PARAMETERS_TOPIC: anylogEdgeX
    WRITABLE_PIPELINE_FUNCTIONS_MQTTEXPORT_PARAMETERS_CLIENTID: edgex-anylog
  image: nexus3.edgexfoundry.org:10004/app-service-configurable:latest
  networks:
    edgex-network:
```

Replace `[anylog-node-ip]` and `[broker-port]` with your AnyLog node's IP and broker port (default `32550`).

---

## Option B — Third-party broker

### 1. Configure EdgeX to publish to the broker

Add an MQTT export application service to your EdgeX compose file pointing to your third-party broker:

```yaml
app-mqtt-export:
  container_name: edgex-app-mqtt-export
  environment:
    EDGEX_PROFILE: mqtt-export
    EDGEX_SECURITY_SECRET_STORE: "false"
    SERVICE_HOST: edgex-app-mqtt-export
    WRITABLE_PIPELINE_FUNCTIONS_MQTTEXPORT_PARAMETERS_BROKERADDRESS: tcp://[broker-ip]:[broker-port]
    WRITABLE_PIPELINE_FUNCTIONS_MQTTEXPORT_PARAMETERS_TOPIC: edgex-events
    WRITABLE_PIPELINE_FUNCTIONS_MQTTEXPORT_PARAMETERS_CLIENTID: edgex-export
  image: nexus3.edgexfoundry.org:10004/app-service-configurable:latest
  networks:
    edgex-network:
```

### 2. Subscribe AnyLog to the broker

```anylog
<run msg client where
    broker = [broker-ip] and
    port = [broker-port] and
    user = [user] and
    password = [password] and
    log = false and
    topic = (
        name = edgex-events and
        dbms = edgex and
        table = "bring [device]" and
        column.timestamp.timestamp = now and
        column.value.float = "bring [readings][][value]" and
        column.name.str = "bring [readings][][name]"
    )>
```

---

## Verifying data flow

### Check EdgeX is running and producing readings

```bash
# List devices (EdgeX v2/v3/v4 API)
curl http://localhost:59881/api/v3/device/all | jq

# View recent readings
curl http://localhost:59880/api/v3/reading/all?limit=10 | jq
```

### Check AnyLog is receiving data

```anylog
get msg clients                    # subscription status
get streaming                      # buffer status
get operator                       # ingestion status
get rows count where dbms = edgex  # confirm rows are landing
```

Query the data:
```anylog
run client () sql edgex format=table "select * from rand_data limit 10"
```

---

## Data mapping notes

EdgeX publishes events in this structure:

```json
{
  "device": "my-sensor",
  "origin": 1700000000,
  "readings": [
    {
      "name": "temperature",
      "value": "23.5",
      "origin": 1700000000
    }
  ]
}
```

The `bring` expressions in the `run msg client` command extract values from this structure:

| AnyLog column | Mapping | Notes |
|---|---|---|
| `table` | `bring [device]` | Uses the device name as the table name |
| `timestamp` | `now` | Uses AnyLog ingestion time |
| `value` | `bring [readings][][value]` | First reading value |
| `name` | `bring [readings][][name]` | First reading name |

Adjust the mapping to match the actual structure of your EdgeX device readings. 
See <a href="{{ '/docs/Managing-Data-Southbound/Managing-Data-Southbound/data-ingestion/' | relative_url }}">Data Ingestion — column mapping</a> 
for the full `bring` syntax reference.

---

## Deploying EdgeX

For a quick local EdgeX deployment using the EdgeX compose builder:

```bash
git clone https://github.com/edgexfoundry/edgex-compose.git
cd edgex-compose/compose-builder

# Generate a compose file with MQTT support and no security (for dev/test)
make gen no-secty mqtt-broker ui

# Start EdgeX
docker compose up -d

# Verify services are running
docker ps
```

See the [EdgeX Quick Start](https://docs.edgexfoundry.org/latest/getting-started/quick-start/) for full deployment instructions.

---

## Further reading

- [EdgeX Foundry documentation](https://docs.edgexfoundry.org/latest/)
- [EdgeX Device Services — supported protocols](https://wiki.edgexfoundry.org/display/FA/Device+Services)
- <a href="{{ '/docs/Network-Services/background-services/#message-broker-service-local' | relative_url }}">AnyLog Message Broker service</a>
- <a href="{{ '/docs/Managing-Data-Southbound/data-ingestion/' | relative_url }}">AnyLog Data Ingestion — run msg client</a>