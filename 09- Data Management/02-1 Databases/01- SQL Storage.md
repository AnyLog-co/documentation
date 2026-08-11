---
title: "SQL & Database Setup"
description: "Connect databases, configure partitioning, and understand AnyLog's SQL dialect for querying distributed edge data."
layout: page
---
<!---
### 📜 Change Log
    - 2026-07-14 | Created document, consolidating database/table administration content that was split across
                  05- Northbound Connectors/sql-setup.md (newer, cleaner, but missing most administrative depth)
                  and 15- Appendices/C- Reference Materials/sql setup.md (older, far more complete on connection
                  options, system databases, and the get local/global/table/columns/rows/distribution family of
                  inspection commands, but never migrated forward). This page is the canonical version; both
                  sql-setup.md files can be retired/redirected here. Querying the data itself (SELECT syntax,
                  period/increments, run client ()) is deliberately out of scope — see Query Data (Training &
                  Tutorials), which now fully absorbs queries.md as the single canonical querying doc.
    - 2026-07-14 | Fixed relative links (this file lives in 03- Training & Tutorials, one level deep, not two as
                  originally assumed) and corrected the querying on-ramp's actual filename (Query Data.md, not
                  "Introduction to Querying Data.md"). Pulled the "Discover tables and columns" content (get
                  virtual tables, get data nodes) forward from queries.md's own discovery section, since it's
                  about what tables/nodes exist rather than about querying — added under Inspecting and monitoring,
                  alongside the get columns command that was already here.
    - 2026-07-14 | Rewrote Partitioning with the correct/fuller command spec: transparent-to-users framing, correct
                  interval syntax (bare year/month/week/day with an optional counter — including a documented
                  counter-plus-one quirk, `3 months` sets 4-month partitions), the wildcard table/database forms,
                  the `info table` command (exists/columns/partitions/partitions last/first/count/dates), and
                  `drop partition`'s `keep` parameter and wildcard behaviors, which weren't previously documented.
    - 2026-08-05 | Ori Shadmon | enhanced partitioning comment to support aggregation logic 
 **Date**   | **Name**       | **Change** | **Version** |
 |------------|----------------|------------|----------|
 | 2026-07-28 | Ori Shadmon    | Fixed a direct contradiction in "Drop a partition": one sentence said it drops only the single oldest partition, another said it drops all but the newest. Confirmed behavior is all-but-newest; rewrote to state that consistently and added a warning since running it unqualified (no `keep`) can remove a lot of history at once. Also flagged a mismatch between the drop-by-name example's partition (hourly, `insert_timestamp`) and this doc's own earlier partitioning example for the same table (daily, `timestamp`) | |
 | 2026-07-28 | Ori Shadmon    | Fixed "PostgresSQL" → "PostgreSQL", "Commends" → "Commands", stray backslash artifact, and several typos (actaully/persistance/separetly/e-defined). Standardized `{keep=X}` optional-parameter notation to match the square-bracket convention used elsewhere | |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-04-25 |                | hyperlinks | |
 | 2026-04-17 |                | created document | |
--->

AnyLog stores data in local relational databases on Operator nodes. Queries issued against the network are translated
into SQL and executed on the relevant Operators, with results aggregated and returned to the querying node.

A node can connect to multiple databases simultaneously. Each database is identified by a **logical name** (the
`dbms` parameter used in commands and queries). Additionally, the capabilities and limitations of the supported
<a href="../../07-%20CLI/04-%20SQL.md" target="_blank">SQL</a> derive from the incompatibility between the different databases.

Every AnyLog node hosts its data in a local relational database, but you never address that physical database
directly. Instead, you work with a **logical database** — a name you choose, associated with whatever physical
database actually backs it on that node. The same logical name can be backed by different physical databases on
different nodes; a node operates identically either way. This decoupling is what lets AnyLog present data spread
across many physical databases, on many machines, as a single queryable collection.

### Supported databases

* **SQLite** is a serverless, self-contained SQL database engine designed to be embedded within applications — i.e. a
file annotated by the extension `.db`. In general the content is stored under `!dbms_dir`; though unless persistence
is configured (ex. Docker volumes), the data may not continue to exist once the AnyLog agent reboots.

* **PostgreSQL** (Postgres or _psql_) is an open source relational database that resides separately from the AnyLog
agent.

While the two can be used interchangeably, Postgres is preferred when data needs to be persistent (ex. AnyLog agents
of type operator and master/metadata manager); while SQLite is a better in-memory solution for a query Agent
with logical database `system_query`.

With that said, small devices that are able to run AnyLog but not Postgres can utilize the SQLite (not in memory) option.

## Database Commands

When defining a database connection, there's no need to pre-create the logical database outside of AnyLog.
In Postgres (and other actual databases) AnyLog is able to pre-connect to the "postgres" db and automatically create
the new logical database. While with SQLite, the system automatically creates a new file for the database under
`!dbms_dir`.

Disconnecting & Dropping database(s) works the same way but from the other direction. This means that AnyLog is also
intelligent enough to tell you "this db is being used" and blocks the user from actually dropping the database.

> Warning, when connecting to a database that's not file-based, the user credentials being used to connect need to have
> the proper read/write permissions.

* Connect to Database - `connect dbms` associates a logical database name with a physical database. Different physical 
databases need different connection details, all supplied as options on the same command:

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

> Notes:
> - For SQLite, the logical name can include a path to control where the data is kept; otherwise it's placed
>  under the default location (`!dbms_dir`).
> - `unlog = true` is recommended for `system_query` (below), since query results there are disposable — but not
>  for your actual user data.

```anylog
connect dbms [logical-name] where type = [sqlite|psql] and [options]

# SQLite 

connect dbms my_data where type = sqlite

connect dbms my_data where type = sqlite and memory = true    # in-memory only

# PostgreSQL 

connect dbms my_data where type = psql and user = anylog and password = demo and ip = 127.0.0.1 and port = 5432
```

* Verify connection
```anylog
get databases                               # list all connected databases
get tables where dbms = my_data            # list tables in a database
get columns where dbms = my_data and table = my_table   # list columns
```

* Disconnecting from database
```anylog 
disconnect dbms [db name]
```

* Drop database - note the database must be disconnected before being dropped

```anylog 
drop dbms [dbm name] where type = [sqlite|psql] and [options]

# SQLite 
drop dbms my_data where type = sqlite

# PostgreSQL 
drop dbms my_data where type = psql and user = anylog and password = demo and ip = 127.0.0.1 and port = 5432
```
> Dropping database means all its content will be gone.

## Tables

Table creation is based on the content coming into the operator node and associated mapping (if relevant).

Before defining a new logical table, the operator node first utilizes the database and table name from the file
name (ex. `[db name].[table name].0.0.json`) in order to check whether the table already exists locally, and if not,
whether it exists on the blockchain. Then, based on the blockchain (i.e. not the first time this database/table is
seen), it defines the table in the local operator node's database.

This means that while operators are separate entities, the moment they reside on the same blockchain it is not possible
for 2 operators to have the same database and table name but different schemas.

> Automation of the create process is done when specifying `create_table=true` as part of the `run operator` command.

* Create table - this function only works when the table schema exists as a `table` policy on the blockchain, or is
one of the pre-defined tables (`blockchain.ledger` and `almgm.tsd_info`) in the platform

```anylog
create table [table-name] where dbms = [dbms-name]
```

* Drop a table - if <a href="#table-partitioning" target="_blank">partitioning</a> is defined, then dropping the table will also remove the
associated partitioning.

```anylog
drop table [table-name] where dbms = [dbms-name]
```

> Dropping a table locally does not remove it from the blockchain. In order to remove the table from the blockchain a
> user needs to remove the `table` policy and the associated `cluster` policies.

* Drop table across all the operators in the network - no matter the cluster the table resides under. 

Unlike the standard `drop table` that only removes the local copy of the table, `drop network table` removes the table  
from operator containing the data *and* removes its metadata definition, in one call. Since some nodes may be offline 
when this runs, use `test network table` both before and after, to confirm which nodes actually had the table and which 
of those the drop actually reached.

```anylog
drop network table where name = [table name] and dbms = [dbms name] and master = [master_node]

drop network table where name = ping_sensor and dbms = lsl_demo and master = 10.0.0.25:2548
```

### Table Partitioning

Partitioning splits a large table into time-based segments, so queries only scan the relevant slice instead of
the entire table, and old data can be cleaned up automatically. Partitioning is **transparent to users and
applications** — you always interact with data using the table's name; AnyLog handles distributing the
processing across the underlying partitions itself. Any date-time column on the table can be used as the
partition column, not just `timestamp`/`insert_timestamp`.

* Creating Partitioning

```anylog
partition [dbms-name] [table-name] using [timestamp-column] by [interval]

# partition all the tables in the database 
partition my_data * using insert_timestamp by 1 week

# partition a specific table in the database 
partition my_data ping_sensor using timestamp by 1 day
```
> Time interval options: `year`, `month`, `week`, `day` — singular or plural, optionally with a counter:

> **If this database also stores aggregation output** (see <a href="../02-2%20Data%20Aggregations.md" target="_blank">Aggregation Functions</a> <!-- TODO: fill in the actual relative path once file locations are confirmed, e.g. ../02-%20.../02-2%20Data%20Aggregations.md#partitioning-and-aggregations -->),
> avoid the wildcard (`*`) form above for that database — it forces raw and aggregation tables onto the same
> interval and retention. Partition (and schedule cleanup for) the raw table and the aggregation table separately
> instead.

* View partitions

```anylog
get partitions
get partitions where dbms = my_data
get partitions where dbms = my_data and table = ping_sensor
```

* Drop a partition

Drops all partitions except the newest/active one (the active partition is never dropped):

```anylog
drop partition where dbms=[db name] and table=[table name] and [keep=X]

# example
drop partition where dbms = my_data and table = ping_sensor
```
> `keep` (optional) tells the system how many of the newest partitions to keep — e.g. `keep=3` removes everything
> except the last 3. Without `keep`, the command removes every partition except the newest one — this can drop a
> lot of history in one call if run without `keep` on a table with many partitions, so double-check before running
> it unqualified.

* Drop specific partitioned table
```anylog
drop partition [partition table name] where dbms = [db name] and table = [table name]

# example 
drop partition par_ping_sensor_2026_07_27_01_h12_insert_timestamp where dbms=my_data and table=ping_sensor
```

> The example above uses `insert_timestamp` with an hourly-style partition name, but the only partitioning example
> shown earlier in this doc for `ping_sensor` uses the `timestamp` column, partitioned daily. Worth using a name
> consistent with that (daily, on `timestamp`) unless `ping_sensor` is genuinely partitioned differently in this
> context.

* Scheduler process to clean old partitions

```anylog
schedule time = 1 day and name = "Drop old data" task drop partition where dbms = my_data and table = ping_sensor and keep=3 
```