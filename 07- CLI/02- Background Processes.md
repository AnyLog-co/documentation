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
---
title: "Background Services"
description: "Background services that define the capabilities of an AnyLog node, including networking, data ingestion, metadata synchronization, scheduling, and high availability."
layout: page
---

# Background Services

## Overview

AnyLog uses a **service-based architecture**. An AnyLog node starts as a common software instance, and its role and capabilities are determined by the background services that are enabled, together with its database and metadata configuration.

For example, a node can provide services for:

- peer-to-peer communication,
- REST and MCP access,
- data ingestion,
- MQTT, Kafka, and gRPC connectivity,
- local data management,
- metadata synchronization,
- data distribution and replication,
- scheduling,
- and notifications.

Services are started using `run` commands and continue operating in the background until they are stopped or the node terminates.

For example:

~~~anylog
run tcp server ...
run rest server ...
run operator ...
run blockchain sync ...
~~~

A node can run multiple services simultaneously. The combination of services determines what the node does in the AnyLog network.

For example, an **Operator node** typically runs the networking services, metadata synchronization, and the `operator` service that processes incoming data into its local databases. A node providing access to applications may run REST and MCP services without itself hosting the requested operational data.

> **Note:** The `operator` and `publisher` services cannot run together on the same node because both operate on the node's data processing directories. A Publisher is designed to distribute incoming data to Operator nodes, while an Operator manages data locally.

---

## Service Lifecycle

Background services are normally started by the node's configuration or deployment scripts when the node starts.

A typical configuration may include commands such as:

~~~anylog
<run tcp server where
    external_ip = !external_ip and
    external_port = !anylog_server_port and
    internal_ip = !ip and
    internal_port = !anylog_server_port and
    bind = false and
    threads = 6>

<run rest server where
    external_ip = !external_ip and
    external_port = !anylog_rest_port and
    internal_ip = !ip and
    internal_port = !anylog_rest_port and
    timeout = 20 and
    threads = 12 and
    ssl = false>

<run blockchain sync where
    source = master and
    time = 60 seconds and
    dest = file and
    connection = !ledger_conn>
~~~

Once started, these services operate independently in the background while the node continues to process CLI, REST, and network requests.

---

## Viewing Background Services

Use:

~~~anylog
get processes
~~~

to view the background services known to the node, their current status, and relevant configuration information.

For JSON output:

~~~anylog
get processes where format = json
~~~

Example:

~~~text
AL anylog-node > get processes

Process          Status        Details
----------------|-------------|--------------------------------------------------------------
TCP             |Running      |Listening on: 172.233.208.217:32348, Threads Pool: 21
REST            |Running      |Listening on: 172.233.208.217:32349, Threads Pool: 12
MCP             |Not declared |
Operator        |Running      |
Blockchain Sync |Running      |Sync every 60 seconds with master
Scheduler       |Running      |Schedulers IDs in use: [0 (system)] [1 (user)]
Blobs Archiver  |Not declared |
MQTT            |Not declared |
MSG Client Pool |Running      |
MSG Broker      |Running      |Listening on: 172.233.208.217:32550
SMTP            |Not declared |
Streamer        |Running      |
Kafka Consumer  |Not declared |
gRPC            |Not declared |
Publisher       |Not declared |
Distributor     |Running      |
Consumer        |Running      |
~~~

The status indicates whether each service is running or has been configured on the node.

Individual services also provide service-specific `get` commands for retrieving more detailed status and statistics.

---

## Common Background Services

| Service | Start Command | Purpose |
| --- | --- | --- |
| TCP | `run tcp server` | Peer-to-peer communication between AnyLog nodes. |
| REST | `run rest server` | HTTP/HTTPS access for applications, APIs, and external data sources. |
| MCP | `run mcp server` | Model Context Protocol access for AI agents and LLM applications. |
| Message Broker | `run message broker` | Runs a local MQTT broker on the AnyLog node. |
| Message Client | `run msg client` | Subscribes to MQTT or REST data sources and maps incoming data. |
| Kafka Consumer | `run kafka consumer` | Subscribes to Kafka topics and ingests data. |
| gRPC Client | `run grpc client` | Subscribes to gRPC services and maps incoming data. |
| Operator | `run operator` | Processes incoming data files and stores the data in local databases. |
| Publisher | `run publisher` | Distributes incoming data to Operator nodes. |
| Data Distributor | `run data distributor` | Replicates data between Operators assigned to the same cluster for HA. |
| Data Consumer | `run data consumer` | Identifies and retrieves missing data from peer Operators in the same cluster. |
| Metadata Sync | `run blockchain sync` | Synchronizes metadata from the Master Node or blockchain. |
| Scheduler | `run scheduler` | Executes scheduled AnyLog tasks. |
| SMTP Client | `run smtp client` | Provides email/SMS notification support through SMTP. |
| Streamer | `run streamer` | Flushes streaming data buffers based on configured time or volume thresholds. |
| Blobs Archiver | `run blobs archiver` | Manages large objects such as images, video, and audio. |

---

# Network Services

Network services allow an AnyLog node to communicate with other AnyLog nodes, applications, devices, and external systems.

The primary network services are:

- **TCP** — communication between AnyLog nodes.
- **REST** — communication with external applications and APIs.
- **MCP** — access for AI agents and applications using Model Context Protocol.
- **Message Broker** — local MQTT broker functionality.

---

## TCP Service

The TCP service provides AnyLog's peer-to-peer network protocol.

It is used for communication such as:

- `run client` requests,
- distributed SQL,
- data distribution,
- metadata-related communication,
- and other node-to-node operations.

Start the TCP service using:

~~~anylog
<run tcp server where
    external_ip = !external_ip and
    external_port = 7848 and
    internal_ip = !ip and
    internal_port = 7848 and
    bind = false and
    threads = 6>
~~~

Check the configured network connections:

~~~anylog
get connections
~~~

---

## REST Service

The REST service provides HTTP/HTTPS access to an AnyLog node for applications and external systems.

Most, but not all, AnyLog commands can be issued to a node through REST.

Start the REST service:

~~~anylog
<run rest server where
    external_ip = !external_ip and
    external_port = 7849 and
    internal_ip = !ip and
    internal_port = 7849 and
    timeout = 20 and
    threads = 12 and
    ssl = false>
~~~

Monitor the REST service:

~~~anylog
get rest server info
get rest calls
get rest pool
~~~

---

## Message Broker

The Message Broker service allows an AnyLog node to operate as a local MQTT broker.

~~~anylog
<run message broker where
    external_ip = !external_ip and
    external_port = 7850 and
    internal_ip = !ip and
    internal_port = 7850 and
    threads = 6>
~~~

The broker accepts messages from MQTT clients. Processing the content of those messages is handled separately by a message client.

Monitor the local broker:

~~~anylog
get local broker
~~~

---

# Data Ingestion Services

AnyLog supports background services for receiving operational data from different protocols and systems.

---

## MQTT Message Client

`run msg client` subscribes to an MQTT broker and maps incoming messages to AnyLog data.

For example:

~~~anylog
<run msg client where
    broker = local and
    port = 7850 and
    topic = (
        name = sensors and
        dbms = plant_data and
        table = sensor_data
    )>
~~~

Monitor configured message clients:

~~~anylog
get msg clients
~~~

Retrieve a particular client:

~~~anylog
get msg client where id = 3
~~~

or locate one by broker and topic:

~~~anylog
get msg client where
    broker = driver.cloudmqtt.com:18785 and
    topic = mydata
~~~

---

## Kafka Consumer

The Kafka Consumer service subscribes to Kafka topics and maps incoming messages into AnyLog data structures.

For example:

~~~anylog
<run kafka consumer where
    ip = [url|local] and
    port = [port] and
    reset = [earliest|latest] and
    user = [user] and
    password = [password] and
    topic = (
        name = sensor and
        dbms = lsl_demo and
        table = ping_sensor and
        column.timestamp.timestamp = "bring [timestamp]" and
        column.value.int = "bring [value]"
    )>
~~~

---

# Data Management Services

## Operator

The `operator` service processes incoming data and manages it in the databases assigned to the node.

Data arriving in the node's watch directory is processed according to its associated database, table, and mapping definitions.

~~~anylog
run operator
~~~

The Operator service is a core service on nodes that physically maintain operational data.

---

## Publisher

The Publisher service accepts incoming data and distributes it to the appropriate Operator nodes rather than maintaining the data locally.

~~~anylog
run publisher
~~~

A Publisher and Operator cannot run simultaneously on the same node.

---

# High Availability Services

When multiple Operators are assigned to the same cluster, AnyLog can replicate the cluster's data between those Operators.

The Operators in a cluster physically maintain replicas of the same cluster data. Over time, each Operator assigned to that cluster is expected to maintain the same data.

Two background services support this process.

## Data Distributor

~~~anylog
run data distributor
~~~

The Data Distributor sends newly received data to the other Operators assigned to the same cluster.

## Data Consumer

~~~anylog
run data consumer
~~~

The Data Consumer identifies data that is missing locally and retrieves it from peer Operators in the cluster.

Together, these services provide data replication and recovery within an HA cluster.

---

# Metadata Synchronization

Each AnyLog node maintains a local copy of the network metadata.

The Metadata Sync service periodically synchronizes this local metadata with the configured shared ledger — either an AnyLog Master Node or a blockchain.

For example:

~~~anylog
<run blockchain sync where
    source = master and
    time = 60 seconds and
    dest = file and
    connection = !ledger_conn>
~~~

The synchronization interval is determined by the node configuration. Once the service is running, metadata synchronization occurs automatically at that interval.

See [Blockchain & Metadata](/docs/08-blockchain-and-metadata/) for details on metadata policies, storage, synchronization, and the Master Node.

---

# Scheduler

AnyLog provides background schedulers for executing commands and tasks periodically.

Scheduler `0` is reserved for system tasks. Scheduler `1` and above can be used for user-defined tasks.

Start a scheduler:

~~~anylog
run scheduler 1
~~~

Tasks can include:

- AnyLog commands,
- queries,
- scripts,
- monitoring operations,
- and alert rules.

Monitor schedulers:

~~~anylog
get scheduler
~~~

or a particular scheduler:

~~~anylog
get scheduler 1
~~~

---

# Stopping a Background Service

Running services can be terminated using their corresponding `exit` command.

Examples:

~~~anylog
exit TCP
exit REST
exit operator
exit broker
exit MQTT
exit SMTP
~~~

Use:

~~~anylog
get processes
~~~

after stopping a service to verify its current state.

---

# Trace Level

AnyLog provides a trace mechanism for observing command and service activity.

The syntax is:

~~~anylog
trace level = <level>
~~~

A trace can also be limited to a particular command or service:

~~~anylog
trace level = <level> <command>
~~~

For example, enable basic tracing globally:

~~~anylog
trace level = 1
~~~

Enable more detailed tracing for TCP only:

~~~anylog
trace level = 3 tcp
~~~

Trace levels range from `0` through `3`:

| Level | Description |
| --- | --- |
| `0` | Tracing disabled. |
| `1` | Basic activity and request information. |
| `2` | Intermediate tracing. |
| `3` | Detailed tracing. |

For script-level debugging, see [CLI Overview](/docs/07-cli/01-cli/#debugging-scripts).

---

# Related Documentation

- [CLI Overview](/docs/07-cli/01-cli/) — issuing commands locally and to peer nodes using `run client`.
- [Get & Set](/docs/07-cli/03-get-set/) — dictionary and configuration values.
- [SQL Commands](/docs/07-cli/04-sql/) — querying distributed data.
- [Blockchain & Metadata](/docs/08-blockchain-and-metadata/) — metadata synchronization and policy management.
- **Southbound Connectors** — MQTT, Kafka, gRPC, OPC-UA, and other data ingestion interfaces.
- **Networking & Security** — node communication, TLS, authentication, and permissions.