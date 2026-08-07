---
title: "Nodes: The start-up commands"
description: "a basic understanding of using AnyLog"
layout: page
source_path: "training/06- Nodes.md"
---
<!--
## Changelog PUT LATEST CHANGES AT THE TOP PLEASE
-
- 2026-08-07 | Eric Aquaronne | change log format adding ref version | 2.0.2606 
- 2026-07-24 | Ori Shadmon | file created 
--->

The following document provides directions on the different node types and the critical component needed in each one for
them to actually be configured properly.

> **Note:** in a real deployment, all the commands below are normally generated and run for you automatically —
> driven by your dotenv configuration and the node's configuration policy (see the Deployment Integration and
> Deployment Scripts docs). They're shown here manually so you understand what each node type actually needs
> under the hood. The < > notation is used to merge multiple lines into a single line when executing long commands on 
> the CLI. It's used in the examples below for two reasons:
> 1. To demonstrate its usage. 
> 2. To keep the output clean and readable.

## Contents

1. [General Process](#general-process)
2. [Common Setup](#common-setup)
   * [Network Setup](#network-setup)
   * [Blockchain Sync](#blockchain-sync)
3. [The Master / Metadata Node](#the-master--metadata-node)
4. [Query Node](#query-node)
5. [The Operator Node](#the-operator-node)
6. [The Publisher Node](#the-publisher-node)

## General Process

1. AnyLog agent starts.
2. A configuration policy, based on the node type, is created — if one does not already exist.
3. Network is configured.
4. Logical databases are defined.
5. Node policy gets defined — for operator nodes this includes the cluster policy.
6. Blockchain sync is enabled.
7. Scheduler is enabled.
8. AnyLog-agent-type-specific configs are enabled.

> **Colocation note:** any combination of AnyLog services / logical databases can reside on the same physical
> machine — **except** `run operator` and `run publisher`, which cannot run on the same node as each other. Keep
> this in mind when planning node placement, before you get into the per-node-type sections below.

## Common Setup

Every node type — Master, Query, Operator, and Publisher — shares the same network setup and blockchain sync
mechanism (just with different sync intervals). Both are covered here once; the per-node-type sections below only
show what's *additional* for that node type.

### Network Setup

```anylog
<run tcp server where 
    external_ip = !external_ip and external_port = !anylog_server_port and 
    internal_ip = !ip and internal_port = !anylog_server_port and 
    bind = true and threads = 8>
    
<run rest server where 
    external_ip = !external_ip and external_port = !anylog_rest_port and 
    internal_ip = [internal ip] and internal_port = !anylog_rest_port and 
    timeout = 30 and ssl = false and bind = false>
```

> **Exception:** the Query node uses `timeout = 90` instead of `timeout = 30`, to accommodate longer-running queries
> across the network. This is called out again in the Query Node section below.

### Blockchain Sync

Every node keeps an accessible local copy of the blockchain — but how *fresh* that copy needs to be depends on the
node type:

* **Master & Query** — sync every **60–90 seconds**. These nodes route queries and resolve policy in real time, so
  they need a near-current view of the ledger.
* **Operator & Publisher** — sync every **~5 minutes**. These nodes primarily ingest and store data; they don't need
  as tight a refresh on the ledger to do their job.

```anylog
# Master / Query
<run blockchain sync where 
  source = master and 
  time = 60 seconds and 
  dest = file>

# Operator / Publisher
<run blockchain sync where 
  source = master and 
  time = 5 minutes and 
  dest = file>
```

## The Master / Metadata Node

The metadata node is our blockchain emulator, and requires 2 things beyond the [common setup](#common-setup)
(using the 60–90 second sync interval):

* `blockchain` Database + `ledger` table
```anylog
<connect dbms blockchain where 
    type = psql and 
    user = [db user] and password = [db passwd] and 
    ip = [db ip] and port = [db port]>

create table ledger where dbms=blockchain
```

AnyLog has built-in table definitions for:
* `blockchain.ledger` — the blockchain emulator storage layer.
* `almgm.tsd_info` — the metadata / hash value record of the data coming in.
* `table` policies on the blockchain.

## Query Node

This is a node dedicated to querying data across the network. Beyond the [common setup](#common-setup) (remember:
`timeout = 90` for network setup, and the 60–90 second sync interval), it needs:

* `system_query` logical database — where results get aggregated. We recommend using SQLite (in-memory), unless
the Northbound Services have a [Postgres direct](../05-%20Northbound%20Connectors/04-%20Postgres%20Connector%20%28Tableau%29.md) connection as opposed to using REST.

```anylog
<connect dbms system_query where 
    type = sqlite and 
    memory=true>
```

## The Operator Node

This node is dedicated to storing the actual data coming in from devices and sensors. Beyond the
[common setup](#common-setup) (using the ~5 minute sync interval), it needs:

* Define Cluster + Blockchain policy — unlike the other nodes, this is a **must** so that the network knows where the data
resides and how to reach it.

> **Note:** the example below uses a fictional company/IP for illustration. `True`/`False` (capitalized) is AnyLog's
> own accepted policy syntax, not a typo of JSON's lowercase `true`/`false`.

```json
{"cluster" : {
    "company" : "Acme Co",
    "name" : "acme-site-1",
    "status" : "active",
    "id" : "353495722981c88e3a5e4ffff486075e",
    "date" : "2026-07-18T19:49:32.437491Z",
    "ledger" : "global"
}},
{"operator" : {
    "name" : "site-operator-1",
    "company" : "Acme Co",
    "hostname" : "acme-site-1",
    "ip" : "10.0.1.11",
    "port" : 32148,
    "rest_port" : 32149,
    "broker_port" : 32150,
    "cluster" : "353495722981c88e3a5e4ffff486075e",
    "main" : True,
    "loc" : "32.7767, 96.7970",
    "country" : "US",
    "state" : "TX",
    "city" : "Dallas",
    "id" : "fca91d1eedcb2472a02954be6e276da8",
    "date" : "2026-07-18T19:49:37.501204Z",
    "member" : 140,
    "ledger" : "global"
}}
```

* Connect to the logical database where data will ultimately be stored:
```anylog
<connect dbms !default_dbms where 
    type = psql and 
    user = [db user] and password = [db passwd] and 
    ip = [db ip] and port = [db port]>
```

> We recommend defining partitioning of the data for better query performance and data maintenance.

* Connect to the `almgm.tsd_info` logical database + table. This keeps a record of the files coming in, for HA and to
remove replication of data (based on file hash):
```anylog
<connect dbms almgm where 
    type = psql and 
    user = [db user] and password = [db passwd] and 
    ip = [db ip] and port = [db port]>
```

* Archiver for blob data — this can be used with or without a NoSQL logical database:
```anylog
# if a NoSQL logical database is set to true, switch True/False between dbms + folder. 

<run blobs archiver where
    dbms=false and
    folder=true and
    compress=true and
    reuse_blobs=true
>
```

* Set buffer size — data buffer size before storing into AnyLog:
```anylog
<set buffer threshold where 
    time=!threshold_time and 
    volume=!threshold_volume and 
    write_immediate=!write_immediate>

run streamer
```

* Enable HA — ⚠️ **Enterprise feature** <!-- CONFIRM: mark HA as Enterprise-only? --> — whether a secondary operator
is planned, or a primary already exists, it's good practice to enable HA now. That way, adding an additional operator
later is as simple as joining it to the network:

```anylog
run data distributor
run data consumer where start_date=-30 days
```

* Enable the Operator service:

```anylog 
<run operator where 
    create_table=true and 
    update_tsd_info=true and 
    compress_json=true and 
    compress_sql=true and
    archive_json=true and 
    archive_sql=true and 
    master_node=!ledger_conn and 
    policy=!operator_id and 
    threads=!operator_threads>
```

## The Publisher Node

⚠️ **Enterprise feature** <!-- CONFIRM: mark the Publisher node itself as Enterprise-only? -->

This is a unique node type — it acts as a mediator between the device/sensor and the operator nodes, allowing data
from one device to be processed across multiple operators using a round-robin approach, where each file is sent to a
different operator (ideally within the same cluster group).

**Why use a Publisher?**

* **Scale** — round-robin spreads load across operators so no single one becomes a bottleneck under high-volume or high-frequency data.
* **Simplicity for the device** — the device only needs to know one destination (the publisher), not the whole cluster topology or which operator is currently healthy.
* **Buffering** — the publisher aggregates incoming messages into files before distributing them, smoothing bursty traffic into steady batches.
* **Policy-based routing** — beyond round-robin, `set data distribution` (see below) can force specific tables to specific operators — e.g. table A always to operator group 1, table B to operator group 2 — rather than spreading evenly.
* **Reduced attack/complexity surface** — only the publisher needs to be reachable by external devices; operators can sit behind it.
* **Cleanup/lifecycle management** — the publisher's `delete_json` / `delete_sql` flags also manage what happens to source files/records after a successful distribution.

Beyond the [common setup](#common-setup) (using the ~5 minute sync interval), it needs:

> **To verify:** if the Publisher receives southbound traffic directly (MQTT/REST push, syslog, etc.) rather than
> picking up files already dropped to disk, it likely also needs `run message broker` — the same as an Operator
> accepting syslog (see the Syslog Integration doc). Confirm whether that step belongs here before publishing.

* Connect to the `almgm.tsd_info` logical database + table. This keeps a record of the files coming in, for HA and to
remove replication of data (based on file hash):
```anylog
<connect dbms almgm where 
    type = psql and 
    user = [db user] and password = [db passwd] and 
    ip = [db ip] and port = [db port]>
```

* Run publisher:

```anylog
# sample file: `my_db.table3.0.0.json` 

<run publisher where 
    dbms_name = file_name[0] and 
    table_name = file_name[1] and
    delete_json = false and 
    compress_json = true and 
    delete_sql = true and 
    master_node = !ledger_conn>
```

* Definition on how to distribute the data from the publisher into different operators:

```anylog 
<set data distribution where 
    dbms = [dbms_name] and 
    table = * and 
    dest = [Operator1 - ip:port] and 
    dest = [Operator2 - ip:port]>
```