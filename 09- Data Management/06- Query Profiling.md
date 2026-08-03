---
title: "Profiling and Monitoring Queries"
description: ""
layout: page
source_path: "profiling and monitoring 01 Queries.md"
---

<!---
### 📜 Change Log
 **Date**   | **Name**      | **Change**         | **Version** |
 |------------|---------------|---------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-28 | Ori Shadmon    | query profiling | |
--->

## Overview

Profiling and monitoring queries is about answering three questions: how long did a query take, which queries are 
slow, and — for any given query — exactly what SQL ran on each node and how long each step took. AnyLog surfaces all 
three through commands issued on the CLI or via REST: aggregate execution-time stats, a slow-query log, per-query 
drill-down (`query status`/`destination`/`explain`), the Operator-side view of the same query, and an opt-in profiler 
for deeper timing on inserts and REST calls.

## Statistical Information

To get a summary of the execution time of queries:
```anylog
get queries time
```
Example reply:
```anylog
Up to  1 sec.: 43
Up to  2 sec.: 12
Up to  3 sec.: 5
Up to  4 sec.: 1
Up to  5 sec.: 0
Total queries: 4
Time interval: 231 (sec.) : 0:3:51 (H:M:S)
```

Reset the statistical information:
```anylog
reset query timer
```

## Identifying Slow Queries

Slow queries can be redirected to the query log:
```anylog
set query log profile [n] seconds
```
`set query log on` records all queries in the query log, whereas adding `profile [n] seconds` logs only queries with 
execution time greater or equal to `[n]` seconds. The example below logs queries taking 5 seconds or more:
```anylog
set query log profile 5 seconds
```

View the slow query log:
```anylog
get query log
```

## Command Options for Monitoring Queries

When a query is executed, AnyLog maintains information on its status — which Operators participated, how much data was 
transferred, and execution time. Since multiple queries run concurrently, each is assigned a Job ID.

The `query` command (issued on the Query Node) reports on the last executed queries. To see the same query from the 
Operator side, use [`get operator execution`](#retrieving-the-status-of-queries-on-an-operator-node).

Usage:
```anylog
query [operation] [id/all]
```

| Operation | Command | Details |
|---|---|---|
| status | `query status` | The status of each executed query |
| destination | `query destination` | The participating Operator Nodes |
| explain | `query explain` | The SQL executed on the local databases |

`id`/`all` are optional:
- Not provided → info on the last executed query
- ID provided → info for that job
- `all` → currently and recently executed queries

Note: query status info is kept in a stack — old entries are dropped over time.

### `query status`

```anylog
AL > query status

Job  ID Output   Run Time Operator              Par Status    Blocks Rows Command
----|--|--------|--------|---------------------|---|---------|------|----|----------------------------------------------------------------------------------------------------|
0009|10|['rest']|00:00:01|All                  |---|Completed|     2|   0|select increments(minute, 1, timestamp), device_name, min(timestamp) as min_ts... from ping_sensor  |
    |  |        |00:00:00|172.105.112.207:32148|  0|Completed|     1|   0|                                                                                                    |
    |  |        |00:00:00|172.105.13.202:32148 |  0|Completed|     1|   0|                                                                                                    |
```

| Attribute | Details |
|---|---|
| Job | Slot number holding the query info (500 slots by default) |
| ID | Unique ID of the query |
| Output | Where the output is directed: stdout, rest, DBMS table, file, kafka |
| Run Time | Total and per-partition reply time on each Operator |
| Operator | IP and Port of each participating Operator |
| Par | Partition ID on each Operator |
| Status | Status of each Operator/Partition (see below) |
| Blocks | Number of blocks returned |
| Rows | Number of rows returned |
| Command | The query or pushdown function executed |

Status values: **Completed**, **Sending**, **Delivered** (sent, no reply yet), **Processing**, **Empty Set**, **Error**.

### `query destination`

```anylog
AL +> query destination

Job Destination           DBMS          Table        Command
---|---------------------|-------------|------------|----------------------------------------------------------------------------------------------------|
  9|172.105.112.207:32148|litsanleandro|ping_sensor |select increments(minute, 1, timestamp), device_name... from ping_sensor                            |
   |172.105.13.202:32148 |litsanleandro|ping_sensor |                                                                                                    |
```

### `query explain`

Shows the SQL processed on each participating database:
```anylog
AL +> query explain

Job ID        |                                         0|
Remote DBMS   |lsl_demo                                  |
Remote Table  |ping_sensor                               |
Source Command|select count(*) from ping_sensor          |
Remote Query  |select count(*) from ping_sensor          |
Local Create  |create table query_0 (count_all integer );|
Local Query   |select sum(count_all) from query_0        |
```

| Attribute | Details |
|---|---|
| Remote DBMS | Logical database name on the Operator Nodes |
| Remote Table | Logical table name on the Operator Nodes |
| Source Command | The SQL or pushdown function used |
| Remote Query | The SQL actually executed on the database node |
| Local Create | Statement creating the intermediary result-set table on the Query Node |
| Local Query | SQL run on the Query Node that produces the final result |

## Retrieving the Status of Queries on an Operator Node

Each Operator can process many concurrent queries. Get the same execution-time statistics (or log them to the **query log**) with:
```anylog
get queries time
```

### `get operator execution`

Shows how a query executed on the Operator side.

Usage:
```anylog
get operator execution where node = [node id] and job = [job id]
```
`[node id]` is the IP of the Query Node that issued the query; `[job id]` is the job ID assigned there (visible via `query status`).

If both are omitted, all recently executed queries are shown; if only `node` is given, that node's queries are shown.

```anylog
get operator execution where node = 10.0.0.78 and job = 12
get operator execution where node = 10.0.0.78
get operator execution
```

Example walkthrough — a query run on the query node:
```anylog
run client () sql lsl_demo format = table "select count(*) from ping_sensor"
```
returns `[2]` (the Job ID) plus the result. Check how it ran:
```anylog
query status 2
```
Then pull the Operator-side execution details for that job:
```anylog
run client 10.0.0.78:7848 get operator execution where node = 10.0.0.85 and job = 1

Node      Job ID Rows limit threads Completed DBMS     Table       Par ID Par Name                                 Error blocks Rows SQL Time Fetch Time Network Time
---------|---|--|----|-----|-------|---------|--------|-----------|------|----------------------------------------|-----|------|----|--------|----------|------------|
10.0.0.78|  1| 2|   3|    0|      3|        3|lsl_demo|ping_sensor|     1|par_ping_sensor_2019_11_01_d07_timestamp|    0|     1|   1|00:00:00|00:00:00  |00:00:00    |
```

| Attribute | Details |
|---|---|
| Node | IP of the node that issued the query |
| Job | The job ID |
| ID | Unique Query ID (on the query node) |
| Rows | Total rows returned |
| Limit | A limit value included in the query |
| Threads | Number of query threads that participated |
| DBMS / Table | Logical dbms/table name |
| Par ID / Par Name | Partition ID/name participating in the query |
| Error | 0 = no error; otherwise the error number from that partition |
| Blocks | Data blocks delivered to the app by that partition |
| Rows | Data rows retrieved from the database by that partition |
| SQL Time | Physical database execution time |
| Fetch Time | Processing time (including DB time) on the operator node |
| Network Time | Time to send data blocks (high value = busy Query Node) |

Notes:
1. `get operator execution` gives the Operator-side view paired with `query status` on the Query Node.
2. Info is kept in a stack; older entries are dropped.

## Profiling

Profiling requires starting AnyLog with the system variable `PROFILER=true`, which loads the profiling libraries.

Turn the profiler on/off per process:
```anylog
set profiler [on/off] where target = [process name]
```
Retrieve profiler output:
```anylog
get profiler output where target = [process name]
```

| Process Name | Details |
|---|---|
| operator | Profile data inserts in the Operator node |
| get | Profile REST GET |
| put | Profile REST PUT |
| post | Profile REST POST |

Example:
```anylog
# with PROFILER=true set in the environment
set profiler on where target = operator         # Start operator profiling
set profiler off where target = operator        # Stop profiling
get profiler output where target = operator     # Get profiling output
```