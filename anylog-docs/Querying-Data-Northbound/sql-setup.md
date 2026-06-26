---
title: SQL & Database Setup
description: Connect databases, configure partitioning, and understand AnyLog's SQL dialect for querying distributed edge data.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlinks
--> 

AnyLog stores data in local relational databases on Operator nodes. Queries issued against the network are translated into SQL and executed on the relevant Operators, with results aggregated and returned to the querying node.

---

## Supported databases

| Database | Best for |
|---|---|
| **SQLite** | Edge nodes, gateways, small deployments, in-memory use |
| **PostgreSQL** | Larger nodes, high-volume data, production deployments |

A node can connect to multiple databases simultaneously. Each database is identified by a **logical name** (the `dbms` parameter used in commands and queries).

---

## Connecting a database

```anylog
connect dbms [logical-name] where type = [sqlite|psql] and [options]
```

### SQLite
```anylog
connect dbms my_data where type = sqlite
connect dbms my_data where type = sqlite and memory = true    # in-memory only
```

### PostgreSQL
```anylog
connect dbms my_data where type = psql and user = anylog and password = demo and ip = 127.0.0.1 and port = 5432
```

### Verify connection
```anylog
get databases                               # list all connected databases
get tables where dbms = my_data            # list tables in a database
get columns where dbms = my_data and table = my_table   # list columns
```

---

## Disconnecting a database

```anylog
disconnect dbms my_data
```

---

## Tables

Tables are created automatically when data arrives (if `create_table = true` is set in the Operator config), or can be created manually:

```anylog
create table [table-name] where dbms = [dbms-name]
```

Drop a table:
```anylog
drop table [table-name] where dbms = [dbms-name]
```

---

## Partitioning

Partitioning splits large tables into time-based segments, enabling efficient data management and automatic cleanup of old data. AnyLog partitions by a timestamp column.

### Create a partition

```anylog
partition [dbms-name] [table-name] using [timestamp-column] by [interval]
```

Intervals: `1 day`, `1 week`, `1 month`, etc.

Examples:
```anylog
partition my_data ping_sensor using timestamp by 1 day
partition my_data rand_data using insert_timestamp by 1 week
```

### View partitions

```anylog
get partitions
get partitions where dbms = my_data
get partitions where dbms = my_data and table = ping_sensor
```

### Drop a partition

Drops the **oldest** partition (the active partition is never dropped):

```anylog
drop partition where dbms = my_data and table = ping_sensor
```

Drop a specific partition by name:
```anylog
drop partition [partition-name] where dbms = my_data and table = ping_sensor
```

Automate cleanup via the scheduler:
```anylog
schedule time = 1 day and start = +1d and name = "Drop old data" task drop partition where dbms = my_data and table = ping_sensor
```

---

## Querying data

AnyLog uses a SQL dialect that routes queries across the network. See <a href="{{ '/docs/Querying-Data-Northbound/queries/' | relative_url }}">Queries</a> for the full reference. Key points:

### Local query
```anylog
sql my_data "select * from ping_sensor limit 10"
```

### Network query (distributed across all relevant Operators)
```anylog
run client () sql my_data format = table "select timestamp, value from ping_sensor where timestamp >= NOW() - 1 hour"
```

### Supported SQL features

| Feature | Supported |
|---|---|
| `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY`, `LIMIT` | ✅ |
| Aggregations: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | ✅ |
| Time functions: `NOW()`, `DATE()`, `PERIOD()` | ✅ |
| `INCREMENTS()` — time-bucketed aggregation | ✅ |
| `JOIN` across tables | ❌ |
| Nested queries | ❌ |
| `INTERVAL` syntax (use `NOW() - N hours` instead) | ❌ |

### Time filter syntax

Always use `NOW() - N unit` for time-based filters:

```anylog
WHERE timestamp >= NOW() - 24 hours
WHERE timestamp >= NOW() - 7 days
WHERE timestamp >= NOW() - 30 minutes
```

### Output formats

```anylog
run client () sql my_data format = table "select ..."     # formatted table
run client () sql my_data format = json "select ..."      # JSON array
run client () sql my_data format = json:list "select ..."  # JSON list
```

---

## Increments — time-bucketed queries

`INCREMENTS` divides a time range into equal buckets and returns aggregated values per bucket. This is the primary function for time-series charting.

```anylog
SELECT increments([time-unit], [count], [timestamp-col]), [aggregations]
FROM [table]
WHERE [timestamp-col] >= [start] AND [timestamp-col] <= [end]
```

Example — average value per minute over the last hour:
```anylog
run client () sql my_data format = json "
  SELECT increments(minute, 1, timestamp), MIN(timestamp), MAX(value), AVG(value)
  FROM ping_sensor
  WHERE timestamp >= NOW() - 1 hour"
```

---

## The system_query database

AnyLog uses a special internal database called `system_query` (SQLite, in-memory) to process and aggregate query results from multiple Operator nodes. This database is always present on any node that handles queries and does not need to be created manually.

```anylog
get databases    # system_query will always appear here
```

---

## Row count and table status

```anylog
get rows count                                          # all tables, all databases
get rows count where dbms = my_data                    # all tables in a database
get rows count where dbms = my_data and table = ping_sensor
get rows count where dbms = my_data and format = json
get rows count where dbms = my_data and group = table  # aggregate per table
```

---

## Backup and restore

### Backup a partition to a file

```anylog
backup table where dbms = my_data and table = ping_sensor and partition = [partition-name] and dest = [path]
```

### Archive and cleanup

The Operator service can be configured to archive processed JSON and SQL files. See <a href="{{ '/docs/Network-Services/background-services/#operator-service' | relative_url }}">Background Services — Operator</a> for `archive_json` and `archive_sql` options.

Delete archived files older than N days:
```anylog
delete archive where days = 60
```