---
title: "Databases & Tables"
description: Connecting logical databases to physical storage, creating and dropping tables, partitioning, discovering what exists, and inspecting/monitoring table state across the network.
layout: page
source_path: "Databases & Tables.md"
---
<!--
## Changelog
- 2026-07-14 | Created document, consolidating database/table administration content that was split across
              08- Northbound Connectors/sql-setup.md (newer, cleaner, but missing most administrative depth)
              and 19- Appendices/C- Reference Materials/sql setup.md (older, far more complete on connection
              options, system databases, and the get local/global/table/columns/rows/distribution family of
              inspection commands, but never migrated forward). This page is the canonical version; both
              sql-setup.md files can be retired/redirected here. Querying the data itself (SELECT syntax,
              period/increments, run client ()) is deliberately out of scope — see Query Data (Training &
              Tutorials) and queries.md (Northbound Connectors) for that.
- 2026-07-14 | Fixed relative links (this file lives in 03- Training & Tutorials, one level deep, not two as
              originally assumed) and corrected the querying on-ramp's actual filename (Query Data.md, not
              "Introduction to Querying Data.md"). Pulled the "Discover tables and columns" content (get
              virtual tables, get data nodes) forward from queries.md's own discovery section, since it's
              about what tables/nodes exist rather than about querying — added under Inspecting and monitoring,
              alongside the get columns command that was already here.
-->

# Databases & Tables

Every AnyLog node hosts its data in a local relational database, but you never address that physical database
directly. Instead, you work with a **logical database** — a name you choose, associated with whatever physical
database actually backs it on that node. The same logical name can be backed by different physical databases on
different nodes; a node operates identically either way. This decoupling is what lets AnyLog present data spread
across many physical databases, on many machines, as a single queryable collection.

Supported physical databases: [SQLite](https://www.sqlite.org/) (default — no install needed, good for
lower-power/edge nodes), [PostgreSQL](https://www.postgresql.org/) (for stronger nodes, higher volume,
production), and [MongoDB](https://www.mongodb.com/) (blob storage only). A node can use different physical
databases for different logical databases at the same time.

This page covers the lifecycle: connecting/disconnecting, creating/dropping tables, partitioning, discovering
and inspecting what's declared where, and backup/archival. For running queries against the data once it's there,
see [Query Data](Query%20Data.md) (on-ramp) or
[Querying Data (Northbound)](../08-%20Northbound%20Connectors/queries.md) (full reference).

---

## Connecting a database

`connect dbms` associates a logical database name with a physical database. Different physical databases need
different connection details, all supplied as options on the same command:

```anylog
connect dbms [db name] where type = [db type] and user = [db user] and password = [db passwd] and ip = [db ip] and port = [db port] and memory = [true/false] and connection = [db string]
```

| Option | Description |
|---|---|
| `[db name]` | The logical name of the database |
| `type` | Physical database: `sqlite`, `psql`, or `pi` (PI System/OSIsoft historian — confirm current support before relying on this; not otherwise documented in this tree) |
| `user` / `password` | Credentials recognized by the physical database |
| `ip` / `port` | Physical database's network location |
| `memory` | If `true`, tables are kept in RAM rather than on disk (SQLite only — not supported by PostgreSQL) |
| `connection` | A raw database connection string, as an alternative to the individual fields above |
| `autocommit` | If `false`, groups multiple statements into a single transaction |
| `unlog` | If `true`, skips writing changes to the write-ahead log — faster inserts, at the cost of durability on failure |

Notes:
- For SQLite, the logical name can include a path to control where the data is kept; otherwise it's placed
  under the default location (`!dbms_dir`).
- `unlog = true` is recommended for `system_query` (below), since query results there are disposable — but not
  for your actual user data.

**Configuration support by physical database:**

| Config | Default | SQLite | PostgreSQL |
|---|---|:---:|:---:|
| `memory` | `false` | ✅ | ❌ |
| `autocommit` | `true` | ✅ | ✅ |
| `unlog` | `false` | ❌ | ✅ |

**Recommended configuration:**

| Config | `system_query` | User databases |
|---|:---:|:---:|
| `memory` | `true` | `false` |
| `autocommit` | `false` | `false` |
| `unlog` | `true` | `false` |

Examples:

```anylog
connect dbms test where type = sqlite
connect dbms system_query where type = sqlite and memory = true
connect dbms sensor_data where type = psql and user = anylog and password = demo and ip = 127.0.0.1 and port = 5432
```

## Disconnecting a database

Useful for switching which physical database backs a given logical name:

```anylog
disconnect dbms [dbms name]
```

Example:

```anylog
disconnect dbms test
```

---

## System databases

Depending on a node's role, it may need one or more system databases connected — each created once and
associated with a physical database, the same way as any user database.

**`system_query`** — used on a Query node to unify results returned to the application. No tables need to be
declared manually; they're created dynamically.

```anylog
# SQLite is typical — query results don't need to persist
connect dbms system_query where type = sqlite and memory = true

# PostgreSQL is typical when connecting to northbound services that can't use REST (e.g. Tableau, Looker)
connect dbms system_query where type = psql and ip = 127.0.0.1 and port = 5432 and user = admin and password = passwd
```

**`almgm`** — an optional internal management database on an Operator node, tracking data ingestion:

```anylog
connect dbms almgm where type = sqlite
# or
connect dbms almgm where type = psql and user = anylog and ip = 127.0.0.1 and password = demo and port = 5432
```

**`blockchain`** — an optional internal database on a master node, managing the metadata locally:

```anylog
connect dbms blockchain where type = sqlite
# or
connect dbms blockchain where type = psql and user = anylog and ip = 127.0.0.1 and password = demo and port = 5432
```

The `ledger` table in that database is created with:

```anylog
create table ledger where dbms = blockchain
```

---

## Creating tables

User tables are usually created automatically: since ingested data arrives as JSON, the receiving node can
detect whether a matching schema already exists, and if not, creates one and publishes it to the shared metadata
layer so other nodes with the same data converge on the same schema. This happens when `create_table = true` is
set in the Operator's configuration.

Tables can also be created manually, from a table definition already present in the metadata ledger:

```anylog
create table [table name] where dbms = [dbms name]
```

This only works if the metadata already includes a **table policy** for that database/table pair — it creates
the local physical table matching that policy, it doesn't invent a new schema.

| Example | Explanation | Prerequisite |
|---|---|---|
| `create table ping_sensor where dbms = lsl_demo` | Creates a user table; columns/indexes come from the table's policy | The `lsl_demo` logical database must already be connected |
| `create table ledger where dbms = blockchain` | Creates the system table hosting metadata | The `blockchain` logical database must already be connected |
| `create table tsd_info where dbms = almgm` | Creates the system table hosting HA info | The `almgm` logical database must already be connected |

---

## Dropping tables

Dropping a table fully means removing it from every node that hosts it *and* removing its policy from the
shared metadata — a single `drop table` only handles the first half, on one node.

### On a single node

```anylog
drop table [table name] where dbms = [dbms name]
```

```anylog
drop table ping_sensor where dbms = lsl_demo
drop table tsd_info where dbms = almgm    # system tables drop the same way
```

Dropping this way leaves the table's policy in the metadata; remove that separately with
`blockchain drop policy` if needed.

### Across the whole network

```anylog
drop network table where name = [table name] and dbms = [dbms name] and master = [master_node]
```

```anylog
drop network table where name = ping_sensor and dbms = lsl_demo and master = 10.0.0.25:2548
```

This drops the table from every node's local database *and* removes its metadata definition, in one call. Since
some nodes may be offline when this runs, use [`test network table`](#monitoring-a-table-across-the-network)
both before and after, to confirm which nodes actually had the table and which of those the drop actually
reached.

---

## Partitioning

Partitioning splits a large table into time-based segments, so queries only scan the relevant slice instead of
the entire table, and old data can be cleaned up automatically. AnyLog partitions by a timestamp column.

### Create a partition

```anylog
partition [dbms-name] [table-name] using [timestamp-column] by [interval]
```

Intervals: `1 day`, `1 week`, `1 month`, etc.

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

Drops the **oldest** partition; the active (current) partition is never dropped by this command:

```anylog
drop partition where dbms = my_data and table = ping_sensor
```

Or a specific partition by name:

```anylog
drop partition [partition-name] where dbms = my_data and table = ping_sensor
```

Automate cleanup on a schedule:

```anylog
schedule time = 1 day and start = +1d and name = "Drop old data" task drop partition where dbms = my_data and table = ping_sensor
```

---

## Discovering what exists

Before querying or managing a table, it's often useful to check what's actually out there across the network —
which tables are registered, and which nodes host each one.

### `get virtual tables` — every table known to the network

```anylog
get virtual tables
get virtual tables where table = ping_sensor
```

This is the network-wide view — tables registered in the shared metadata, regardless of which physical node(s)
actually hold their data.

### `get data nodes` — which nodes host a given table

```anylog
get data nodes
get data nodes where table = ping_sensor
get data nodes where sort = (1,2)    # sort by DBMS (col 1), table (col 2)
```

---

## Inspecting and monitoring

### `get databases` — what's connected

```anylog
get databases
```

Lists every logical database and the physical database backing it, e.g.:

```text
Active DBMS Connections
Logical DBMS Database Type IP:Port         Configuration             Storage
------------|-------------|---------------|-------------------------|----------------------------------------------|
almgm       |psql         |127.0.0.1:5432 |Autocommit On            |Persistent                                    |
lsl_demo    |psql         |127.0.0.1:5432 |Autocommit Off, Unflagged|Persistent                                    |
configs     |sqlite       |Local          |Autocommit On            |D:\Node\AnyLog-Network\data\dbms\configs.dbms |
```

### `get database size` — how big is it

```anylog
get database size [logical dbms name]
```

```anylog
get database size lsl_demo
```

### `test network table` — is this table consistent across nodes

Compares a table's definition on every node that hosts it against the definition in the metadata:

```anylog
test network table where name = [table name] and dbms = [dbms name]
```

### `get local tables` — what exists physically on this node

```anylog
get local tables where dbms = [dbms name] and format = [table|json]
```

```anylog
get local tables where dbms = dmci
get local tables where dbms = aiops and format = json
```

### `get global tables` — what's declared in the metadata

Lists tables declared in the shared metadata layer for a database, whether or not they exist on this node:

```anylog
get global tables where dbms = [dbms name] and format = [table|json]
```

```anylog
get global tables where dbms = dmci
```

### `get tables` — both, combined

```anylog
get tables where dbms = [dbms name] and format = [table|json]
```

Indicates, per table, whether it exists locally, globally, or both. Use `dbms = *` to list every table across
every database, local and global.

```anylog
get tables where dbms = dmci
get tables where dbms = *
```

### `get table [info type]` — status of one table

```anylog
get table [info type] where name = [table name] and dbms = [dbms name]
```

| Info type | Returns |
|---|---|
| `exist status` | Whether the table is declared locally and/or in the metadata |
| `local status` | Whether the table is declared locally |
| `blockchain status` | Whether the table is declared in the metadata |
| `rows count` | Number of rows in the table |
| `complete status` | All of the above at once |

```anylog
get table local status where dbms = aiops and name = lic1_s
get table complete status where name = ping_sensor and dbms = anylog
```

### `get columns` — schema of a table

```anylog
get columns where dbms = [dbms name] and table = [table name] and format = [table|json|list] and sys_col = [true/false] and type = [data types to project]
```

> The first four columns AnyLog adds to every table — `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id` — are
> for internal data management. They're included by default (see `sys_col` below); you can safely ignore them
> in your own `SELECT` statements.

| Option | Description |
|---|---|
| `sys_col` | `true` (default) includes the internal `row_id`/`insert_timestamp`/`tsd_name`/`tsd_id` columns; `false` hides them |
| `type` | Restrict to one or more data types |
| `format` | `table` (default), `json`, or `list` (flat column-name list, e.g. for Grafana variable projection) |

```anylog
get columns where dbms = aiops and table = ping_sensor and sys_col = false
get columns where dbms = lsl_demo and table = ping_sensor and sys_col = false and type = int and type = "character varying" and format = list
```

### `get rows count` — row totals

```anylog
get rows count where dbms = [dbms name] and table = [table name] and format = [table|json] and group = [partition|table]
```

`group = partition` (default) reports per-partition; `group = table` aggregates to one number per table. This
counts rows on **this node only** — to count a table's rows across the whole network, run an actual
`select count(*)` query instead.

```anylog
get rows count
get rows count where dbms = my_dbms and group = table
get rows count where dbms = my_dbms and table = my_table
```

### `get data distribution` — rows per node

```anylog
get data distribution where dbms = [dbms name] and table = [table name]
```

Shows how many rows of a given table live on each Operator node that hosts it.

```anylog
get data distribution where dbms = lsl_demo and table = ping_sensor
```

---

## Backup and archive

### Backup a partition to a file

```anylog
backup table where dbms = my_data and table = ping_sensor and partition = [partition-name] and dest = [path]
```

### Archive processed files

The Operator service can be configured to archive processed JSON and SQL files after ingestion — see
Background Services (Operator service) for the `archive_json`/`archive_sql` options.

Delete archived files older than N days:

```anylog
delete archive where days = 60
```

---

## See also

- [Query Data](Query%20Data.md) — a beginner walkthrough of actually querying the tables this page shows you
  how to set up
- [Querying Data (Northbound)](../08-%20Northbound%20Connectors/queries.md) — the full query reference
- [Aggregations](../06-%20Data%20Management/B-%20Query%20&%20Aggregations/Aggregations.md)