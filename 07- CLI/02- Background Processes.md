---
title: Background Services
description: Enable and monitor the core services that run on each AnyLog node — TCP, REST, operator, broker, Kafka, scheduler, and more.
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-04-25 |                | Created document |          |
--->

AnyLog is a service-based deployment, which means the services enabled or disabled (along with the database configs)
ultimately define the capabilities and services provided by the node.

Except for the `Operator` and `Publisher` services — which cannot coexist — any combination of services (and databases)
can co-exist; however, in order for an AnyLog agent to act as an Operator and/or Metadata data manager node, for example,
there are a few services that must co-exist.

The reason `Operator` and `Publisher` services cannot co-exist is that they would share the same `!data_dir` path in the
instance, which could cause the system to get confused. Furthermore, an AnyLog agent configured to act as a _Publisher_ is
intended to distribute data (from devices) into operator node(s); whereas an AnyLog agent configured to act as an _Operator_
is intended to store generated data.

---

## Services overview

| Command | Description |
|---|---|
| `run tcp server` | Peer-to-peer messaging between AnyLog nodes |
| `run rest server` | HTTP/HTTPS listener for external applications and data sources |
| `run mcp server` | Model Context Protocol server for AI/LLM integration |
| `run message broker` | Configures the node as a local MQTT broker |
| `run msg client` | Subscribes to an external MQTT or REST broker |
| `run kafka consumer` | Subscribes to a Kafka topic and ingests data |
| `run grpc client` | Subscribes to a gRPC service and maps data |
| `run operator` | Ingests data from the watch directory into local databases |
| `run publisher` | Distributes data files to Operator nodes (cannot run alongside Operator) |
| `run data distributor` | Replicates data to peer Operators in the same cluster (HA) |
| `run data consumer` | Validates and retrieves missing data from cluster peers (HA) |
| `run blockchain sync` | Periodically syncs metadata from the blockchain or master node |
| `run scheduler` | Runs user-defined tasks on a periodic schedule |
| `run smtp client` | Enables email/SMS notifications via SMTP |
| `run streamer` | Flushes streaming data buffers to disk based on time/volume thresholds |
| `run blobs archiver` | Manages storage of large objects (images, video, audio) |

---

## Viewing service status

The following command lists all background services, their current status, and key configuration details:

```anylog
get processes
get processes where format = json
```

Example output:

```
AL anylog-node > get processes

    Process         Status       Details
    ---------------|------------|------------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.233.208.217:32348, Threads Pool: 21                         |
    REST           |Running     |Listening on: 172.233.208.217:32349, Threads Pool: 12, Timeout: 20, SSL: False|
    MCP            |Not declared|                                                                              |
    Operator       |Not declared|                                                                              |
    Blockchain Sync|Running     |Sync every 60 seconds with master using: 45.79.73.39:32048                    |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                                |
    Blobs Archiver |Not declared|                                                                              |
    MQTT           |Not declared|                                                                              |
    MSG Client Pool|Not declared|                                                                              |
    MSG Broker     |Running     |Listening on: 172.233.208.217:32550, Threads Pool: 6                          |
    SMTP           |Not declared|                                                                              |
    Streamer       |Not declared|                                                                              |
    UNS Streamer   |Not declared|                                                                              |
    Query Pool     |Running     |Threads Pool: 3                                                               |
    Kafka Consumer |Not declared|                                                                              |
    gRPC           |Not declared|                                                                              |
    PLC Client     |Not declared|                                                                              |
    Pull Processes |Not declared|                                                                              |
    Video Processes|Not declared|                                                                              |
    Publisher      |Not declared|                                                                              |
    Distributor    |Not declared|                                                                              |
    Consumer       |Not declared|                                                                              |
```

Detailed information for each service can be retrieved using its corresponding `get` command — see each section below.

To terminate a running service:
```anylog
exit TCP
exit REST
exit operator
exit broker
exit MQTT
exit SMTP
```

## Trace Level

Like with [debug mode in scripts](01-%20CLI.md#debugging-scripts), AnyLog has a built-in trace mechanism to help trace
activity on the node.

```anylog
trace level = X [command name]
```

Trace levels range from 0–3 and can optionally be scoped to a specific command or service:
* Providing just a level (no command name) traces every command at that level.
* Providing a level **and** a command name limits the trace to that service only.

| Level | Description |
|:-----:|:---|
| 0 | Trace level is off |
| 1 | Shows basic activity — for example, whether a query was accepted from a different node, and which query |
| 2 | *(not separately documented — treat as an intermediate level between 1 and 3)* |
| 3 | Full trace level |

```anylog
# trace level of 1 for all commands
trace level = 1

# trace level 3 for the TCP service only
trace level = 3 tcp
```

## Network services

AnyLog's network services are critical for a node to participate in the network.

Each node can be identified by up to two IP addresses:
- **External IP** — accessible from the Internet
- **Internal IP** — accessible from a private/local network

If both are provided, the node listens on the internal IP. If only one is provided, the node listens on that IP.
Setting `bind = false` causes the node to listen on all reachable IPs on the specified port.

**Configuration Options**:

| Option | Description | Default | Rest Specific |
|:---:|:---:|:---:|:---:|
| `external_ip` | IP accessible from the Internet | | ❌ |
| `external_port` | Port for external connections | | ❌ |
| `internal_ip` | IP on the local/private network | | ❌ |
| `internal_port` | Port for internal connections | | ❌ |
| `bind` | `true` — bind to one IP only; `false` — listen on all IPs | `true` | ❌ |
| `threads` | Worker threads for incoming requests | 6 | ❌ |
| `timeout` | Seconds before timeout error (0 = no limit) | 20 | ✅ |
| `ssl` | Enable HTTPS with client certificates | `false` | ✅ |

* **TCP Service**: Enables AnyLog's peer-to-peer protocol for sending and receiving messages between nodes. The IP and ports used by
this process are published to the blockchain, making the node recognizable and accessible to network peers.

```anylog
<run tcp server where
  external_ip = !external_ip and external_port = 7848 and
  internal_ip = !ip and internal_port = 7848 and
  bind = false and threads = 6>
```

* **REST Service**: Enables HTTP/HTTPS communication from external applications and data sources that are not
AnyLog nodes.

```anylog
<run rest server where
    external_ip = !external_ip and external_port = 7849 and
    internal_ip = !ip and internal_port = 7849 and
    timeout = 0 and threads = 12 and ssl = false>
```

* **Message Broker**: Configures the AnyLog node itself as an MQTT broker, allowing third-party clients and devices to publish data directly
to it. See <a href="{{ '/docs/Managing-Data-Southbound/node-red/' | relative_url }}">node-RED</a> for an example integration.

```anylog
<run message broker where
    external_ip = !external_ip and external_port = 7850 and
    internal_ip = !ip and internal_port = 7850 and
    threads = 6>
```

The message broker enables the AnyLog agent to act as an MQTT or Kafka broker, but does not actually understand the data
flowing into said broker. For that the agent needs to have an active `msg client` that's either MQTT specific **or**
Kafka. A more detailed description of both can be found in [southbound services](../04-%20Southbound%20Interfaces/02-%20Direct%20Connectors/02-%20Message%20Broker.md).

```anylog
# MQTT Message Client descriptor command
<run msg client where
  broker = [url|local|rest] and port = [port] and
  user = [user] and password = [password] and log = [true/false] and
  topic = (
    name = [topic] and
    dbms = [dbms] and
    table = [table] and
    [column mapping]
)>

# Kafka Message Client descriptor command
<run kafka consumer where
  ip = [url|local] and port = [port] and
  reset = [earliest|latest] and user = [user] and password = [password] and
  topic = (
    name = sensor and
    dbms = lsl_demo and
    table = ping_sensor and
    column.timestamp.timestamp = "bring [timestamp]" and
    column.value.int = "bring [value]"
  )>
```

### Support Networking Commands

* Check connection info
```anylog
get connections
```

* Monitor the REST service:
```anylog
get rest server info    # configuration
get rest calls          # request statistics
get rest pool           # thread pool status
```

* Monitor the message broker:
```anylog
get local broker
```

* Monitor subscriptions:
```anylog
get msg clients
get msg client where id = 3
get msg client where broker = driver.cloudmqtt.com:18785 and topic = mydata
```

## Scheduler

Users can define one or more schedulers, each running a set of tasks at a configured interval. Scheduler `0` is the
system scheduler; scheduler `1` (and above) are user-defined.

```anylog
run scheduler [id]
```

Tasks can include AnyLog queries, script files, monitoring checks, or
<a href="{{ '/docs/Monitoring/alerts-and-monitoring/' | relative_url }}">alerts and monitoring</a> rules.

Monitor:
```anylog
get scheduler
get scheduler 1
```