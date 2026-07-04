---
title: Background Services
description: Enable and monitor the core services that run on each AnyLog node — TCP, REST, operator, broker, Kafka, scheduler, and more.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

Background services are optional processes that, when activated, run on dedicated threads according to the 
node's configuration. Services can be enabled in any of the following ways:

- Command line arguments when starting AnyLog
- Directly on the AnyLog CLI
- A script file processed with: `process [path/file]`
- A configuration policy associated with the node

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

---

## Network services

### TCP service

Enables AnyLog's peer-to-peer protocol for sending and receiving messages between nodes. The IP and ports used by 
this process are published to the blockchain, making the node recognizable and accessible to network peers.

Each node can be identified by up to two IP addresses:
- **External IP** — accessible from the Internet
- **Internal IP** — accessible from a private/local network

If both are provided, the node listens on the internal IP. If only one is provided, the node listens on that IP. 
Setting `bind = false` causes the node to listen on all reachable IPs on the specified port.

```anylog
<run tcp server where
  external_ip = [ip] and external_port = [port] and
  internal_ip = [local_ip] and internal_port = [local_port] and
  bind = [true/false] and threads = [count]>
```

| Option | Description | Default |
|---|---|---|
| `external_ip` | IP accessible from the Internet | |
| `external_port` | Port for external connections | |
| `internal_ip` | IP on the local/private network | |
| `internal_port` | Port for internal connections | |
| `bind` | `true` — bind to one IP only; `false` — listen on all IPs | `true` |
| `threads` | Worker threads for incoming requests | 6 |

Examples:
```anylog
run tcp server where external_ip = !ip and external_port = !port and threads = 3

<run tcp server where
  external_ip = !external_ip and external_port = 7850 and
  internal_ip = !ip and internal_port = 7850 and
  bind = false and threads = 6>
```

Check connection info:
```anylog
get connections
```

---

### REST service

Enables HTTP/HTTPS communication from external applications and data sources that are not AnyLog nodes.

```anylog
<run rest server where
  external_ip = [ip] and external_port = [port] and
  internal_ip = [local_ip] and internal_port = [local_port] and
  timeout = [seconds] and threads = [count] and
  ssl = [true/false] and bind = [true/false]>
```

| Option | Description | Default |
|---|---|---|
| `external_ip` | IP accessible from the Internet | |
| `external_port` | Port for external REST connections | |
| `internal_ip` | IP on the local/private network | |
| `internal_port` | Port for internal REST connections | |
| `timeout` | Seconds before timeout error (0 = no limit) | 20 |
| `threads` | Worker threads for HTTP requests | 5 |
| `ssl` | Enable HTTPS with client certificates | `false` |
| `bind` | `true` — bind to one IP only | `true` |

Example:
```anylog
<run rest server where
  internal_ip = !ip and internal_port = 7849 and
  timeout = 0 and threads = 6 and ssl = false>
```

Monitor the REST service:
```anylog
get rest server info    # configuration
get rest calls          # request statistics
get rest pool           # thread pool status
```

Debug incoming REST calls:
```anylog
trace level = 1 run rest server    # show REST commands received
trace level = 2 run rest server    # show REST commands with headers and body
```

---

### MCP service


Exposes the node as <a href="https://modelcontextprotocol.io" target="_blank">Model Context Protocol (MCP)</a> server, 
enabling AI assistants and LLM-based tools to query and interact with the AnyLog network.

```anylog
run mcp server
set mcp client config where external_ip = [ip] and external_port = [port] and internal_ip = [local_ip] and internal_port = [local_port]
```

---

### Message broker service (local)

Configures the AnyLog node itself as an MQTT broker, allowing third-party clients and devices to publish data directly 
to it. See <a href="{{ '/docs/Managing-Data-Southbound/node-red/' | relative_url }}">node-RED</a> for an example integration.

```anylog
<run message broker where
  external_ip = [ip] and external_port = [port] and
  internal_ip = [local_ip] and internal_port = [local_port] and
  bind = [true/false] and threads = [count]>
```

| Option | Description | Default |
|---|---|---|
| `external_ip` | IP accessible from the Internet | |
| `external_port` | Port for external broker connections | |
| `internal_ip` | IP on the local/private network | |
| `internal_port` | Port for internal broker connections | |
| `bind` | `true` — bind to one IP only | `true` |
| `threads` | Worker threads | 6 |

Examples:
```anylog
run message broker where external_ip = !ip and external_port = !port and threads = 3

run message broker where external_ip = !external_ip and external_port = 7850 and internal_ip = !ip and internal_port = 7850 and threads = 6
```

Monitor:
```anylog
get local broker
```

---

## Data storage

### Operator service

The Operator monitors the watch directory, identifies or creates schemas, and ingests data into local databases. 
An Operator must be associated with an <a href="{{ '/docs/Network-Services/policies-metadata/#operator-policy' | relative_url }}">Operator policy</a> 
and a <a href="{{ '/docs/Network-Services/policies-metadata/#cluster-policy' | relative_url }}">Cluster policy</a> 
published to the metadata layer.

> **Note:** The Operator and Publisher services cannot run on the same node. A node acts as either an Operator (stores data) or a Publisher (routes data to Operators), not both.

```anylog
run operator where [option] = [value] and ...
```

| Option | Description | Default |
|---|---|---|
| `policy` | ID of the Operator policy | |
| `create_table` | Auto-create tables if they don't exist | `true` |
| `update_tsd_info` | Update the `tsd_info` summary table (used for HA sync) | |
| `archive_json` | Archive JSON files after processing | `true` |
| `archive_sql` | Archive SQL files after processing | `false` |
| `compress_json` | Compress JSON files after processing | `true` |
| `compress_sql` | Compress SQL files after processing | `true` |
| `limit_tables` | Comma-separated list of table names to process | |
| `master_node` | IP:Port of the master node | |
| `distributor` | Enable HA data distribution to peer Operators | |
| `threads` | Worker thread count | |

Example:
```anylog
run operator where create_table = true and update_tsd_info = true and archive_json = true and distributor = true and master_node = !master_node and policy = !operator_policy and threads = 3
```

> See <a href="{{ '/docs/Managing-Data-Southbound/southbound-overview/#the-file-naming-convention' | relative_url }}">File Naming Convention</a> · 
> <a href="{{ '/docs/Managing-Data-Southbound/mapping-policies/' | relative_url }}">Mapping Data to Tables</a> · 
> <a href="{{ '/docs/Managing-Data-Southbound/data-ingestion/' | relative_url }}">Setting Streaming Thresholds</a>

Monitor the Operator:
```anylog
get operator
get operator inserts
get operator summary
get operator config
get operator summary where format = json
```

---

### Publisher service

The Publisher monitors the watch directory and distributes data files to the appropriate Operator nodes based on 
metadata policies. It does not store data locally.

> **Note:** The Publisher and Operator services cannot run on the same node. A node acts as either a Publisher (routes data) or an Operator (stores data), not both.

```anylog
run publisher where [option] = [value] and ...
```

| Option | Description | Default |
|---|---|---|
| `watch_dir` | Directory monitored for new files | `!watch_dir` |
| `bkup_dir` | Directory for successfully processed files | `!bkup_dir` |
| `error_dir` | Directory for files that failed processing | `!error_dir` |
| `delete_json` | Delete JSON file after successful processing | `false` |
| `delete_sql` | Delete SQL file after successful processing | `false` |
| `compress_json` | Compress JSON file after processing | `false` |
| `compress_sql` | Compress SQL file after processing | `false` |
| `company` | Company name associated with the data | Derived from database name |
| `master_node` | IP:Port of the master node | |

Examples:
```anylog
run publisher where delete_json = true and delete_sql = true

run publisher where company = anylog and delete_json = true and delete_sql = true
```

Monitor the Publisher:
```anylog
get publisher
```

---

### HA: Data distributor and data consumer

These two services work together to provide High Availability (HA) by keeping data consistent across all Operators in 
the same cluster.

- **Data distributor** — copies new data files from the local node to all peer Operators in the cluster.
- **Data consumer** — periodically validates the completeness of the local data set and retrieves any missing data from cluster peers.

#### Data distributor

```anylog
run data distributor where distr_dir = [data directory] and archive_dir = [archive directory]
```

Example:
```anylog
run data distributor where cluster_id = 87bd559697640dad9bdd4c356a4f7421 and distr_dir = !distr_dir
```

Monitor:
```anylog
get distributor
```

#### Data consumer

```anylog
run data consumer where start_date = [date] and end_date = [date] and mode = [active|suspend]
```

- `start_date` — required; format `YY-MM-DD HH:MM:SS` or relative (e.g. `-30d`)
- `end_date` — optional; defaults to current date/time
- `mode` — `active` (default) or `suspend`; can be changed at runtime:

```anylog
set consumer mode = suspend
set consumer mode = active
```

Example — sync the last 3 days of data:
```anylog
run data consumer where start_date = -3d
```

Monitor:
```anylog
get consumer
```

---

## Blockchain sync service

Periodically connects to the blockchain platform or a master node to update the local copy of metadata. This ensures 
the node can satisfy metadata queries locally, even if the upstream source is temporarily unreachable.

```anylog
run blockchain sync where source = [master|blockchain] and time = [interval] and dest = [file|dbms] and connection = [ip:port]
```

| Option | Description |
|---|---|
| `source` | `master` — use a master node; `blockchain` — use a blockchain platform |
| `dest` | `file` — store as local JSON; `dbms` — store in a local database |
| `connection` | IP:Port of the master node (when `source = master`) |
| `time` | Sync frequency (e.g. `30 seconds`, `1 minute`) |
| `platform` | Blockchain platform to use (e.g. `optimism`, `ethereum`) |

Examples:
```anylog
run blockchain sync where source = master and time = 30 seconds and dest = file and connection = !master_node

run blockchain sync where source = blockchain and time = !sync_time and dest = file and platform = optimism
```

> See <a href="{{ '/docs/Network-Services/master-node/' | relative_url }}">Master Node</a> for master node configuration.

Force an immediate sync (without waiting for the next scheduled interval):
```anylog
run blockchain sync
```

Switch to a different master node at runtime:
```anylog
blockchain switch network where master = [IP:Port]
```

Monitor sync status:
```anylog
get synchronizer
get metadata version
```

---

## Node status and network testing

### get status

Returns a summary of whether the node is running and responsive:

```anylog
get status
```

### test node

Validates the node's local services — checks that TCP and REST listeners are active and reachable:

```anylog
test node
```

### test node and test network

Validates connectivity to every node published on the metadata layer. For each node, AnyLog sends a test message and 
reports the response:

```anylog
test network
```

> See <a href="{{ '/docs/Network-Services/test-commands/#test-network' | relative_url }}">Test Commands</a> for full usage and output details.

---

## Data ingestion services

### Message client (subscribe to external broker)

Subscribes to a third-party MQTT or REST broker and maps incoming messages to database tables. 
See <a href="{{ '/docs/Managinin-Data-Southbound/data-ingestion/' | relative_url }}">Data Ingestion</a>
for full parameter reference and mapping examples.

```anylog
<run msg client where
  broker = [url|local|rest] and port = [port] and
  user = [user] and password = [password] and log = [true/false] and
  topic = (
    name = [topic] and
    dbms = [dbms] and
    table = [table] and
    [column mapping]
  )>
```

Monitor subscriptions:
```anylog
get msg clients
get msg client where id = 3
get msg client where broker = driver.cloudmqtt.com:18785 and topic = mydata
```

---

### UNS Streamer

The UNS (Unified Namespace) Streamer is automatically activated — no explicit `run` command is required — when data 
arrives through a dynamic southbound connector:

- **MQTT msg client** configured in dynamic mode (topic and schema determined at runtime)
- **PLC client** receiving data via <a href="{{ '/docs/Managing-Data-southbound/opcua/' | relative_url }}">OPC-UA</a> or <a href="{{ '/docs/Managing-Data-southbound/etherip/' | relative_url }}">EtherNet/IP</a>

When active, the UNS Streamer normalises incoming data into a unified namespace structure before routing it to the 
appropriate database table.

Monitor:
```anylog
get msg clients
```

---

### Kafka consumer

Subscribes to a Kafka topic and ingests data into local databases.

```anylog
<run kafka consumer where
  ip = [ip] and port = [port] and
  reset = [latest|earliest] and
  topic = (
    name = [topic] and
    dbms = [dbms] and
    table = [table] and
    [column mapping]
  )>
```

- `reset` — `latest` (default) starts from the newest offset; `earliest` replays from the beginning

Example:
```anylog
<run kafka consumer where
  ip = 198.74.50.131 and port = 9092 and
  reset = earliest and
  topic = (
    name = sensor and
    dbms = lsl_demo and
    table = ping_sensor and
    column.timestamp.timestamp = "bring [timestamp]" and
    column.value.int = "bring [value]"
  )>
```

Monitor:
```anylog
get msg clients
```

---

### gRPC client

Subscribes to a gRPC service and maps incoming data to database tables using a mapping policy.

```anylog
run grpc client where name = [name] and ip = [ip] and port = [port] and policy = [policy id]
```

Example:
```anylog
run grpc client where name = kubearmor and ip = 127.0.0.1 and port = 32767 and policy = deff520f1096bcd054b22b50458a5d1c
```

Monitor:
```anylog
get grpc client
```

---

### PLC client

Connects to industrial PLCs and controllers via OPC-UA or EtherNet/IP and streams data into the AnyLog network.
See <a href="{{ '/docs/Managing-Data-Southbound/opcua/' | relative_url }}">OPC-UA</a> PLC Integration
for full configuration and examples.

---

### Video processes

Manages ingestion and archival of video streams and image data. 
See <a href="{{ '/docs/Managing-Data-Southbound/video_streaming/' | relative_url }}">Video Streaming</a> for full 
configuration and examples.

---

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

---

## SMTP client

Enables email and SMS notifications triggered by the scheduler or rule engine. 
See <a href="{{ '/docs/Monitoring/alerts-and-monitoring/' | relative_url }}">Alerts and Monitoring</a> for how to 
configure notification rules.

```anylog
<run smtp client where
  host = [host] and port = [port] and
  email = [address] and password = [password] and
  ssl = [true/false]>
```

| Option | Description | Default |
|---|---|---|
| `host` | SMTP server URL | `smtp.gmail.com` |
| `port` | SMTP server port | |
| `email` | Sender email address | |
| `password` | Sender email password | |
| `ssl` | Use secure SMTP connection | `false` |

Example:
```anylog
run smtp client where email = anylog.iot@gmail.com and password = mypassword
```


> To use a Gmail account as sender: <a href="https://accounts.google.com/signup" target="_blank">create a Google account</a> 
> and enable <a href="https://myaccount.google.com/lesssecureapps" target="_blank">Allow less secure apps</a>.

---

## Streamer

Required when using streaming mode for data ingestion. The Streamer enforces time-based and volume-based buffer flush 
thresholds, writing buffered data to files for the Operator to process.

```anylog
run streamer where prep_dir = [path] and watch_dir = [path] and err_dir = [path]
```

If directories are not specified, the default paths from the AnyLog dictionary are used (`get dictionary` to view them).

> See Setting and Retrieving Streaming Thresholds for threshold configuration.

Monitor streaming buffer status:
```anylog
get streaming
```

---

## Blobs archiver

Manages storage of large binary objects (images, video, audio) by routing them to a dedicated blobs database, a folder, 
or both.

```anylog
<run blobs archiver where
  blobs_dir = [data dir] and archive_dir = [archive dir] and
  dbms = [true/false] and file = [true/false] and compress = [true/false]>
```

| Option | Description | Default |
|---|---|---|
| `blobs_dir` | Directory where blobs are staged before archival | `!blobs_dir` |
| `archive_dir` | Root directory for archived blobs | `!archive_dir` |
| `dbms` | Store blobs in a dedicated database | `true` |
| `file` | Save blobs to a folder organised by date | `false` |
| `compress` | Apply compression | `false` |

Example:
```anylog
run blobs archiver where dbms = true and file = true and compress = false
```

Monitor:
```anylog
get blobs archiver
```