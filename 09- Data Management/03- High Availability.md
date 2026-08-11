---
title: "High Availability (HA) & Data Resilience (DR)"
description: "How AnyLog's cluster/operator model provides both data resilience and high availability, the push/pull replication mechanism, TSD-based data safety, and how to set up an operator for HA."
layout: page
source_path: "High Availability.md"
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-29 | Ori Shadmon    | Second consolidation pass: intro, Key Terminology, and How It Works still each partially re-explained "clusters replicate data via primary/backup" from a slightly different angle. Gave each section exactly one job — intro states bare HA/DR definitions only, Key Terminology covers pure structure/vocabulary (no replication mechanics), How It Works owns all replication/failover explanation, including now explicitly tying HA's "seamless switch" (previously just asserted in the intro with no mechanism ever given) back to the same replica structure. Unified the `get tsd` info-type keywords and where-conditions, previously a bullet list plus a separate table, into one table | |
 | 2026-07-29 | Ori Shadmon    | Fixed a swapped-command bug in "Setting Up Operator for HA" (the Distributor/Consumer steps had the wrong commands attached, contradicting the Pull/Push Data section earlier in this doc); fixed single-quoted (invalid) JSON in the operator policy; fixed "4 more rows" → "4 more columns"; fixed a mismatched file hash/ID in the final `wc -l` verification command; removed a literally duplicated sentence and a stray trailing backtick; repaired a corrupted ASCII diagram. Consolidated: push/pull was explained in full four separate times (intro, "How it works" ×2, "Data Ingestion Logic") — now explained once, with the other mentions pointing back to it. Reduced three overlapping diagrams to two, each showing something the other doesn't, using one consistent drawing style. Typo fixes ("Resilence" → "Resilience" throughout, including the title) | |
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
--->

> **AnyLog only.** High-Availability & Data Resilience  are not available in EdgeLake.

AnyLog's SQL data store layer has a unified solution for both high availability and data resilience — both are
built on the same underlying structure: clusters of replicated operators. <a href="#key-terminology" target="_blank">Key Terminology</a>
covers that structure; <a href="#how-it-works" target="_blank">How It Works</a> covers the replication and failover mechanism itself, so
neither is explained twice.

**Data Resilience** (DR) is the ability of a system to protect, retain, and recover data against loss.

**High Availability** (HA) is the ability to keep serving data even when a node is down.

> High Availability and Data Resilience are enterprise features that exist only within the operator node and its
> ability to serve the data. When a primary (or data-generating) operator node is down, it's up to the IT/engineer
> to reconfigure connectivity for data to come in from devices/sensors — HA does not reconfigure the data source
> itself.

## Key Terminology

**What is a Cluster?** While it may seem like an actual node, in reality a cluster is only a virtual policy that
groups operators together. A cluster policy represents a logical distribution of the data, and the collection of
clusters represents the network's complete data set. Clusters are the tool that tells the blockchain (and thus the
query node) what data exists on the network and where.

**What is an Operator?** This is the actual node where data coming from southbound services resides. An operator
must be associated with a cluster, otherwise the network wouldn't know what type of data the operator contains, or
which other nodes to replicate it with.

Operators are assigned to clusters (each operator can be assigned to only one cluster), and the number of operators
assigned to a cluster determines the number of copies of the data it hosts.

```diagram
Network (blockchain / metadata)
   |
   +-- Cluster A  (dbms = smart_city, table = ping_sensor)
   |      |
   |      +-- Operator A1 (main)
   |      +-- Operator A2 (backup)
   |      +-- Operator A3 (backup)        <-- 1 or more operators per cluster
   |
   +-- Cluster B  (dbms = monitoring, table = syslog)
   |      |
   |      +-- Operator B1 (main)          <-- a cluster can have just 1 operator
   |
   +-- Cluster C  (dbms = smart_city, table = co2_level)
          |
          +-- Operator C1 (main)
          +-- Operator C2 (backup)
```

> For HA specifically, at least 2 operators need to be assigned to each cluster — a single-operator cluster (like B
> above) has data resilience from the cluster/replication model in general, but no actual failover target if that
> one operator goes down.

## How It Works

Operators within the same cluster are full replicas of one another — one (usually the one closest to the data
source) is main/primary, the rest are backups. This one structure is what delivers both DR and HA:

**Data resilience** comes from replication. Each participating operator is configured with **push** and **pull**
processes that keep every member of a cluster holding the same data:

* When an operator receives new data, it stores it locally and **pushes** it out to its peer operators in the same
  cluster.
* Each operator also continuously **pulls** any data it's missing from its peers.

This push/pull sync happens automatically, without a central coordinator — every operator in a cluster ends up with
the same complete data set regardless of which operator any given piece of data originally arrived through.

**High availability** comes from that same replication: because every operator in a cluster holds identical data,
the query node can transparently retry a different operator in the cluster if the primary doesn't respond — this
is the "seamless switch" HA relies on. The exact retry mechanics (timeout, retry count) aren't covered in this
doc — flag if that level of detail is needed here.

For example: if Operator 5 (in Cluster 2) receives new data, that data is pushed to Operators 4 and 6 — the other
members of Cluster 2 — and each of those operators also independently pulls anything it doesn't yet have. A single
logical data set can also span more than one cluster — for example, a corporation with identical factories could
have the same logical table replicated into 2 separate clusters, one per physical factory, each backed up across
its own set of operators.

```diagram
Table 1..4 (logical database)
        |
        +-- Cluster 1
        |      +-- Operator 1
        |      +-- Operator 2
        |      +-- Operator 3
        |
        +-- Cluster 2
               +-- Operator 4
               +-- Operator 5  <-- receives new data
               +-- Operator 6
                      ^
                      |  pushed to peers / pulled from peers
                      +-- (both directions, automatically)
```

### Pull Data

`run data consumer` — the pull side; retrieves whatever source files this operator is missing from its cluster
peers, so its local data set stays complete.

### Push Data

`run data distributor` — the push side; transfers this operator's data files to the other members of its cluster.

## Data Ingestion Logic

1. A PLC or another device generates data and publishes it out.
2. Either a direct <a href="../04-%20Southbound%20Interfaces" target="_blank">southbound connection</a> built into AnyLog, or a third-party
   connector (e.g. Node-RED), accepts the data from the PLC device or sensor. If the data is first passed through
   a third-party application, that application then forwards the data into AnyLog — usually via MQTT or REST.
3. To avoid continuously writing to the database, incoming content resides in a configurable buffer.
4. Once the buffer is full, AnyLog then processes the data into the appropriate databases (assuming they are
   already connected) and tables.
5. For HA/clustered deployments, the receiving operator then pushes/pulls the data with its cluster peers — see
   <a href="#how-it-works" target="_blank">How It Works</a> above for that mechanism.

```diagram
PLC / Device-Sensor
        |
        +-------------------+
        |                   |
        v                   v
  Built-in Southbound   Third-Party Connector
      Connector             (e.g. Node-RED)
        |                   |
        |                   v
        |            Forwarded via MQTT/REST
        |                   |
        +---------+---------+
                   |
                   v
           Buffer (batches writes)
                   |
                   v
          JSON -> SQL Inserts
        (+ blockchain policies)
                   |
                   v
         Create Table (if needed)
                   |
                   v
         Insert Data (SQLite INSERT /
            PSQL COPY ... FROM)
                   |
                   v
        Cluster sync (HA only, see above)
```

## Data Replication Safety

Since data is seamlessly copied from one operator to another, one of the risks that appears is ensuring data isn't
being re-copied between nodes indefinitely. This is guaranteed by 2 things:

1. Operator Member ID
2. `tsd` info and the `almgm` database

### Member ID

Each operator node has a unique member ID, auto-generated. This gives HA a reference point for where data originally
came from. No 2 operators should have the same member ID; when resetting an operator node on the same IP (and port),
validate it's still using the old Member ID, since otherwise there can be conflicts when attempting to share data.

In other words, the member ID is used to validate that an operator isn't getting its own information back from
other nodes, and that other nodes have a full copy of the data it generates.

### TSD & `almgm` logical database

In addition to the member ID and enabling pull/push services on the operator node, the HA logic also requires the
`almgm` logical database and `tsd_info` to exist.

`almgm` stands for "AnyLog Management database" and is used to keep a record of data (files) being processed on the
operator node. `tsd_info` keeps a record of the data that's initiated locally. When deploying secondary operators,
the `almgm` logical database grows and includes `tsd_[operator Member ID]`, which contains information coming in
from that operator node.

#### `tsd` in table schema

When new data generates a table (policy) within AnyLog, the HA mechanism extends the table to include 4 more
columns:
* `row_id` - the order by which data came into the table
* `insert_timestamp` - database timestamp of insertion
* `tsd_name` - Operator's member ID
* `tsd_id` - file ID

```SQL
CREATE TABLE IF NOT EXISTS pp_pm (
-- data processing information --
    row_id SERIAL PRIMARY KEY,
    insert_timestamp TIMESTAMP NOT NULL,
    tsd_name character(3),
    tsd_id integer,
-- Actual device Data --
    monitor_id character(4),
    commsstatus boolean,
    energymultiplier integer,
    frequency integer,
    powerfactor integer,
    reactivepower integer,
    realpower integer,
    a_current integer,
    a_n_voltage integer,
    b_current integer,
    b_n_voltage integer,
    c_current integer,
    c_n_voltage integer,
    timestamp TIMESTAMP NOT NULL
);
CREATE INDEX pp_pm_insert_timestamp_index ON pp_pm(insert_timestamp);
CREATE INDEX pp_pm_timestamp_index ON pp_pm(timestamp);
```

When looking at the metadata information, the tsd info in the data table should be traceable back through
`tsd_info` and, ultimately, to the actual file.

1. Query the data

```anylog
AL anylog-query +> <run client () sql monitoring format=table and stat=false and extend=(+node_name)
    select
        row_id, insert_timestamp, tsd_id, tsd_name
    from
        docker_insight
    where
        period(minute, 1, now(), insert_timestamp)
    order by insert_timestamp desc limit 1>

node_name             row_id insert_timestamp           tsd_id tsd_name
--------------------- ------ -------------------------- ------ -------- 
power-plant-operator1   3099 2026-07-29 01:34:19.446337 320817      165 
```

2. Locate the corresponding file in tsd info

```anylog
AL power-plant-operator1 +> sql almgm format=table and stat=false select * from tsd_info where file_id=320817

file_id dbms_name table_name source file_hash                        instructions file_time                  rows status1 status2
------- --------- ---------- ------ -------------------------------- ------------ -------------------------- ---- ------- ------- 
 320817 cos       pp_pm           0 c2a8b167ab57afe4cf63ef78d922c1ca            0 2026-07-29 01:34:19.446337   38 None    None 
```

3. Using the `file_hash`, locate and view the data

```anylog 
# locate 
AL power-plant-operator1 +> system ls !archive_dir/26/07/29 | grep c2a8b167ab57afe4cf63ef78d922c1ca                             
cos.pp_pm.0.c2a8b167ab57afe4cf63ef78d922c1ca.0.157.320817.260729002143.json.gz

# decompress 
AL power-plant-operator1 +> file decompress !archive_dir/26/07/29/cos.pp_pm.0.c2a8b167ab57afe4cf63ef78d922c1ca.0.157.320817.260729002143.json.gz !prep_dir/cos.pp_pm.0.c2a8b167ab57afe4cf63ef78d922c1ca.0.157.320817.260729002143.json

# review 
AL power-plant-operator1 +> system cat !prep_dir/cos.pp_pm.0.c2a8b167ab57afe4cf63ef78d922c1ca.0.157.320817.260729002143.json
{"monitor_id":"DSP","A_Current":7,"A_N_Voltage":241,"B_Current":11,"B_N_Voltage":244,"C_Current":10,"C_N_Voltage":243,"CommsStatus":true,"EnergyMultiplier":1,"Frequency":5998,"PowerFactor":97,"ReactivePower":10,"RealPower":37,"timestamp":"2026-07-29T00:21:43.2704726Z"}
{"monitor_id":"DG2","A_Current":0,"A_N_Voltage":0,"B_Current":0,"B_N_Voltage":0,"C_Current":0,"C_N_Voltage":0,"CommsStatus":true,"EnergyMultiplier":1,"Frequency":6000,"PowerFactor":100,"ReactivePower":0,"RealPower":0,"timestamp":"2026-07-29T00:21:43.2704726Z"}
{"monitor_id":"DG3","A_Current":0,"A_N_Voltage":0,"B_Current":0,"B_N_Voltage":0,"C_Current":0,"C_N_Voltage":0,"CommsStatus":true,"EnergyMultiplier":1,"Frequency":6000,"PowerFactor":100,"ReactivePower":0,"RealPower":0,"timestamp":"2026-07-29T00:21:43.2704726Z"}
...

AL power-plant-operator1 +> system cat !prep_dir/cos.pp_pm.0.c2a8b167ab57afe4cf63ef78d922c1ca.0.157.320817.260729002143.json | wc -l 
38
```

#### `tsd` commands

Alternatively to the manual process above, users can utilize `tsd`-based commands to validate node synchronization
of the data.

```anylog
AL power-plant-operator1 +> get tsd list

tsd_166  -- data coming in from operator wieth memebr ID 166
tsd_240  -- data coming in from operator with member ID 240
tsd_info -- data being generated and stored locally 
```

## Retrieve information from TSD tables

The following command retrieves information from a TSD table. The information includes the details of each file
ingested to the local database.

```anylog 
Usage:
        get tsd [details/summary/error] where [options]

Explanation:
        Retrieve entries or summaries from one or more TSD tables.

Examples:
        get tsd details
        get tsd error details table = tsd_info and hash = a00e6d4636b9fd8e1742d673275a75f7 and format = json
        get tsd summary where table = *
        get tsd summary where table = tsd_61
```

| Parameter | Values | Default | Description |
|---|---|---|---|
| `[info type]` | `details` / `summary` / `errors` | `details` | `details` — the last entries in the requested TSD table(s) (limited to the last 100 entries per table by default). `summary` — a summary view of the requested TSD table(s). `errors` — entries representing sync processes that failed. |
| `limit` | integer (0 = no limit) | 100 | Limit on the number of rows retrieved from the table. |
| `table` | table name or `*` | `tsd_info` | Table to use. `table=*` considers all TSD tables; otherwise only `tsd_info` is considered. |
| `hash` | hash string | — | Retrieve a key with the specified hash value. |
| `start_date` | date | — | Retrieve entries with a date greater than or equal to `start_date`. |
| `end_date` | date | — | Retrieve entries with a date earlier than `end_date`. |
| `format` | `table` / `json` | `table` | Output format. |

**Example**:

```anylog 
AL power-plant-operator1 +> get tsd summary where table=tsd_123 

Info on TSD Table: tsd_123
DBMS       Table          Start Date          From ID End Date            To ID Files Count Source Count Status 1 Status 2 Total Rows 
----------|--------------|-------------------|-------|-------------------|-----|-----------|------------|--------|--------|----------|
monitoring|docker_insight|2026-05-16 05:45:00|      1|2026-05-21 20:30:41|31023|      13357|           1|       2|       2|    131886|
monitoring|node_insight  |2026-05-16 05:45:15|      3|2026-05-21 20:30:53|31024|      10096|           1|       2|       2|     15973|
monitoring|syslog        |2026-05-16 05:45:40|      4|2026-05-21 20:30:58|31025|       7572|           1|       2|       2|    141298|

Total all TSD Tables
DBMS       Table          Files Count Total Rows 
----------|--------------|-----------|----------|
monitoring|docker_insight|      13357|    131886|
monitoring|node_insight  |      10096|     15973|
monitoring|syslog        |       7572|    141298|
```

## Setting Up Operator for High-Availability

1. Cluster Policy

```json
{"cluster": {
  "company": "Lit San Leandro",
  "name": "lsl-cluster2",
  "status": "active",
  "id": "7a00b26006a6ab7b8af4c400a5c47f2a"
}}
```

2. Operator nodes — an Operator policy representing each operator; assign each operator to the same cluster for
   replication, or a unique cluster per operator otherwise.

```json
{"operator" : {"cluster" : "7a00b26006a6ab7b8af4c400a5c47f2a",
                "ip" : "24.23.250.144",
                "local_ip" : "10.0.0.78",
                "port" : 7848,
                "id" : "52612f21b18cf29f7d2e511e3ca56ca6",
                "date" : "2021-04-02T21:43:20.129597Z",
                "member" : 145}}
```

3. Enabling the following services on each Operator node:
   1. The Operator background process, to ingest data into the local databases.
   ```anylog
    <run operator where 
      create_table = true and 
      update_tsd_info = true and 
      archive_json = true and 
      distributor = true and 
      master_node = !ledger_conn and 
      policy = !operator_policy_id  and 
      threads = 3> 
    ```

   2. The Distributor background process, to push new data to the peer nodes that host a copy of the data.
   ```anylog
    run data distributor
    ```

   3. The Consumer background process, to pull data that's missing from the current node.
   ```anylog
    run data consumer
    ```

4. Enabling the TSD tables operations

   ```anylog 
connect dbms almgm where ... 

create table tsd_info where dbms=almgm 
```