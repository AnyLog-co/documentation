---
title: Get Commands
description: Reference for AnyLog's get commands — node status, dictionary, resource monitoring, and help.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | updated hyperlinks
--> 

AnyLog's `get` commands provide a unified interface for inspecting every aspect of a running node — its services, data 
volumes, resource usage, configuration, and connectivity. All `get` commands can be issued locally on the CLI or 
remotely via `run client`.

---

## Node status

### get status

Returns whether the node is running, its assigned name, and optional extra metrics:

```anylog
get status
get status where format = json
```

Extend the response to include monitored variables:
```anylog
get status where include = !!cpu_percent and include = !!disk_free
```

Example response:
```json
{
  "assigned_name": "bachelor-query@172.233.208.212:32348",
  "status": "running",
  "profiling": false
}
```

Issue against a peer node:
```anylog
run client 10.0.0.78:7848 get status
```

### get processes

Lists all background services, their status, and key configuration details. See <a href="{{ '/docs/Network-Services/background-services/' | relative_url }}">Background Services</a>.

```anylog
get processes
get processes where format = json
```

### get connections

Returns the IPs and ports the node is listening on:

```anylog
get connections
```

Example output:
```
Type      External               Local                  Bind
---------|----------------------|-----------------------|----------------------|
TCP      |172.233.208.212:32348 |172.233.208.212:32348  |172.233.208.212:32348 |
REST     |172.233.208.212:32349 |172.233.208.212:32349  |0.0.0.0:32349         |
Messaging|172.233.208.212:32550 |172.233.208.212:32550  |0.0.0.0:32550         |
```

### get platform info

Returns OS type, version, node name, and processor type:

```anylog
get platform info
```

---

## Dictionary

Each node maintains a key-value dictionary storing paths, IPs, ports, and user-defined variables. Variables are 
referenced in scripts and commands using the `!` prefix.

### get dictionary

```anylog
get dictionary                          # all key-value pairs
get dictionary where format = json      # JSON output
get dictionary _dir                     # keys containing substring '_dir'
!my_key                                 # retrieve a single value on the CLI
get !my_key                             # retrieve via REST or remote CLI
```

### get env var

Lists OS-level environment variables:

```anylog
get env var
get env var where format = json
$MY_VAR                                 # retrieve a single env var
```

---

## Data monitoring

### get rows count

Lists tables and their row counts across local databases:

```anylog
get rows count
get rows count where dbms = my_dbms
get rows count where dbms = my_dbms and table = my_table
get rows count where dbms = my_dbms and format = json
get rows count where dbms = my_dbms and table = my_table and group = table
```

- `group = table` — aggregates counts per table rather than per partition

### get data nodes

Lists all Operator nodes in the network and the tables each one hosts:

```anylog
get data nodes
```

### get operator

Returns data ingestion details for the local Operator service:

```anylog
get operator
get operator stat format = json
get operator inserts
get operator summary
get operator config
```

---

## Resource monitoring

These commands require <a href="https://psutil.readthedocs.io/en/latest/" target="_blank">psutil</a> to be installed on 
the node.

### Memory, CPU, disk

```anylog
get memory info             # RAM usage
get cpu info                # CPU details
get cpu temperature         # CPU temperature (if supported)
get ip list                 # all IP addresses on the node
get disk usage [path]       # disk usage at path
get disk free [path]        # free space at path
get disk total [path]       # total capacity at path
get disk percentage [path]  # usage as a percentage
```

### get os process

```anylog
get os process              # AnyLog process (same as get os process anylog)
get os process anylog       # CPU and memory for the AnyLog process
get os process [pid]        # info for a specific PID
get os process all          # all processes (takes ~1 second for CPU measurement)
get os process list         # process names and PIDs
```

### get node info

Maps to psutil calls and returns structured system metrics. Values can be stored in a database table or sent to an 
aggregator node.

```anylog
get node info cpu_percent
get node info cpu_times
get node info cpu_times_percent
get node info getloadavg
get node info swap_memory
get node info disk_io_counters
get node info disk_io_counters read_count
get node info net_io_counters
get node info net_io_counters bytes_recv
```

Store directly into a database table:
```anylog
get node info cpu_percent into dbms = monitor and table = cpu_percent
```

---

## Continuous monitoring

`continuous` repeats one or more monitoring commands on a fixed interval. Press any key to stop.

```anylog
continuous [seconds] [command1], [command2], ...
```

| Command | Description |
|---|---|
| `cpu` | System CPU usage |
| `cpu anylog` | AnyLog process CPU usage |
| `cpu [process]` | Named process CPU usage |
| `get cpu usage` | Per-CPU breakdown |
| `get operator` | Operator status |
| `get operator summary` | Operator summary |
| `get streaming` | Streaming buffer status |
| `get query pool` | Query thread pool |
| `get operator pool` | Operator thread pool |
| `get rest pool` | REST thread pool |
| `get tcp pool` | TCP thread pool |
| `get msg pool` | Message broker thread pool |

Examples:
```anylog
continuous cpu, cpu anylog, get operator summary, get streaming

continuous 10 run client () sql my_dbms select max(timestamp), count(*) from my_table where timestamp >= NOW() - 5 minutes
```

---

## Aggregator node

An aggregator node collects status pushed from multiple nodes and provides a unified view — without requiring a database.

### On each monitored node (via scheduler):

```anylog
schedule name = node_status and time = 15 seconds task node_status = get status where format = json
schedule name = monitor_node and time = 15 seconds task run client [aggregator_ip:port] monitor Nodes where info = !node_status
```

### On the aggregator node:

```anylog
get monitored              # list all monitored topics
get monitored Nodes        # status per node for topic 'Nodes'
reset monitored Nodes      # clear the node list for a topic
```

### monitor command

```anylog
monitor [topic] where ip = [node-ip] and name = [node-name] and info = [json-struct]
```

Example:
```anylog
monitor operators where ip = 127.0.0.1 and name = dmc-usa and info = {"total events": 1000, "events per second": 10}
```

---

## Other useful get commands

```anylog
get synchronizer            # blockchain sync status
get metadata version        # current metadata version ID
get scheduler               # scheduler status
get scheduler 1             # specific scheduler status
get streaming               # streaming buffer status and thresholds
get rest server info        # REST service configuration
get rest calls              # REST request statistics
get local broker            # message broker status
get msg clients             # active message client subscriptions
get blobs archiver          # blobs archiver status
get distributor             # HA distributor status
get consumer                # HA consumer status
get publisher               # publisher status
get network info            # network-level info
get version                 # AnyLog version
get databases               # connected local databases
get tables where dbms = [dbms]   # tables in a database
get columns where dbms = [dbms] and table = [table]  # columns in a table
```