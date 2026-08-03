---
title: "SQL Commands"
description: "Run SQL queries across distributed operator nodes, with time-series functions, casting, and formatting options."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon | Fixed `SUMt` → `SUM`, `foramt` → `format` in the cast example (would have failed if copy-pasted), `increment` → `increments`, `dive` → `divide` with a tense fix, `---` → `--` for the Postgres comment. Fixed the still-open `period` intro sentence (missing "The", "allows to find" → "allows you to find"). Renamed "Disclaimer" → "Note" for the period/increments limitation and added the missing colon. Flagged several new items inline: a stray `[38]` and trailing semicolon in the `period` worked example, a node-name mismatch in the `increments` worked example, and `NOW() - 1 hour` vs the shorthand (`-3d`) form used elsewhere in this doc | |
 | 2026-07-28 | Ori Shadmon | Rewrote/reorganized. Fixed `format=true` (not a valid format value) in the worked example; fixed "Replated Topics" typo; restored the "Discover tables and columns" pointer section the changelog already described trimming (it had gone missing from the body); grammar fixes. Flagged and left open: `increments`' optimized-form parameter order still contradicts its own example, the REST example's missing JSON comma, `User-Agent` vs `AnyLog-Agent`, and `count(distinct())` vs `count distinct` (this doc's own earlier draft used the latter) | |
 | 2026-07-14 |             | Trimmed "Discover tables and columns" down to a pointer — that content (`get virtual tables`, `get data nodes`, `get columns`) now lives in Databases & Tables.md (03- Training & Tutorials), which is the better home for table/column discovery than a page about querying the data itself | |
 | 2026-04-17 |             | Created document | |
--->

At its core, AnyLog is intended to provide access to data from devices and sensors in real-time — transforming small
sections of a factory line or a power plant into a unified data lake at the edge. Each AnyLog agent connects to the
appropriate logical database and a shared blockchain network; one node on that network, the Query Node, holds a logical
database called system_query and uses blockchain metadata to locate the relevant Operator nodes, distribute the query,
and assemble a unified result — letting a query behave as though all the data resides locally on a single machine.

**Related Topics**:
* [Data Storage](../09-%20Data%20Management/02-%20Databases.md)
* Data Discovery
* [Query Blob Data](../09-%20Data%20Management/02-1%20Databases/02-%20Blob%20Storage.md)

## SQL + `run client ()`

In the [previous sections](01-%20CLI.md#executing-on-peer-nodes) we had talked about the idea of `run client` and
how to specify the proper IP and ports for sending requests between nodes. With the exception of the `sql` command,
the content in `run client` must be filled in.

**Invalid**: The example is invalid because `run client` does not know where to send the request.
```anylog
run client () get processes 
```

**Valid**: This example is valid because `run client` knows where to send the request — either via the actual
IP:Ports or the blockchain.
```anylog
run client (blockchain get master bring.ip_port) get processes 
run client (10.0.0.14:32148,10.0.0.15:32158) get processes  
```

However, when you specify `run client () sql ...` the platform knows that this is a SQL request and is able to utilize the
blockchain in order to locate where the data resides.

When using REST, the `-H "destination: network"` replaces `run client ()`.

## The `sql` Command

The `sql` command is able to run SQL commands locally or across the network if initiated by `run client ()`.

Before defining the actual `SELECT` statement, and since this is a distributed network, the command contains a
set of options that allow it to better unify the result set — whether in terms of formatting or timezone.

| Key | Values | Default | Description                                                         |
|---|---|---|---------------------------------------------------------------------|
| `format` | `json` / `table` / `json:list` / `json:output` | `json` | Output format                                                       |
| `timezone` | `utc` / `local` / `pt` / `mt` / `ct` / `et` / tz name | `local` | Timezone for timestamps when data is returned                       |
| `stat` | `true` / `false` | `true` | Include processing statistics                                       |
| `max_time` | seconds | — | Cap query execution time                                            |
| `drop` | `true` / `false` | `true` | Drop local output table after query                                 |
| `dest` | `stdout` / `rest` / `dbms` / `file` | dynamic | Destination for result set                                          |
| `include` | `dbms.table` | — | Treat a differently-named remote table as the queried table         |
| `extend` | column list | — | Include node variables (e.g. `@ip`, `@port`) in results             |
| `nodes` | `main` / `all` | `main` | HA: `main` uses designated primary operators; `all` uses round-robin |
| `committed` | `true` / `false` | `false` | HA: only return data confirmed synced across cluster nodes          |


```anylog
sql [db name] format=table and stat=true and timezone=utc and extend=(+node_name) "SELECT ...." 
```

## Supported SQL

AnyLog is a time-series focused platform, providing SQL support across different database types as though they are
unified. While we support much of the standard functionality, we also support extended functionality or lack certain
functionality that may be of interest. Please reach out to [info@anylog.network](mailto:info@anylog.network) if you
are looking to get support for something that's not there.

**Supported Aggregation functions**:
* `MIN`
* `MAX`
* `AVG` - since this is a distributed network, when executing `SELECT AVG` the query node asks each operator to bring
it the `SUM` and `COUNT` for said column, and then aggregates the results into a unified average value.
* `SUM`
* `COUNT` 
* `COUNT(DISTINCT())`
* `RANGE` - the difference between the min and max value of a column

In addition, AnyLog also supports `WHERE`, `GROUP BY`, `ORDER BY` and `LIMIT`.

> When doing `SELECT *` or `SELECT COUNT(*)` the Query node utilizes the table policy in the blockchain to convert `*` 
> into actual columns before forwarding the request across the network. As such, if the table policy is not on the 
> blockchain then the query could fail not because it doesn't see where the data resides, but rather it fails to define 
> how the data is organized.

## Cast data & Formatting Options

Apply casts to projected columns using `::`:

| Cast | Description |
|---|---|
| `float(x)` | Float rounded to x decimal places. Add `%` before x for comma-separated thousands |
| `int` | Cast to integer |
| `str` | Cast to string |
| `ljust(x)` | Left-justified string, x bytes wide |
| `rjust(x)` | Right-justified string, x bytes wide |
| `format(type)` | Apply formatting (see below) |
| `datetime(code)` | Parse datetime and reformat using format code |
| `function(expr)` | Evaluate expression per row (can reference other columns as `[col_name]`) |
| `lstrip` / `rstrip` | Remove leading/trailing spaces |
| `timediff` | Time difference vs `now()` or a datetime string, returned as `HH:MM:SS.f` |
| `timezone` | Override query timezone for this column |
| `replace(old by new)` | Replace a substring once |

> | Type | Description |
> |---|---|
> | `:,` | Comma as thousands separator |
> | `:b` | Binary |
> | `:x` | Hex |
> | `:o` | Octal |
> | `:e` | Scientific notation |
> | `:.3f` | Float with 3 decimal places |
> | `:08.3f` | Float with zero-padded width |

```anylog
# Single Casting 
SELECT reading_time, speed::float(2) FROM performance WHERE reading_time >= NOW() -3d

# Multiple Casting 
SELECT reading_time, speed::float(2)::format(:,) FROM performance WHERE reading_time >= NOW() -3d
```

## Time-series optimised queries

In addition to the standard SQL functions mentioned above, AnyLog also has its own time-series optimization windowing
functions.
* [`period`](#period) which brings the last before a given timestamp
* [`increments`](#increments) which aggregate the data into buckets of time.

> **Note:** the two functions cannot co-exist on the same query at this time.

### `period`

The `period` function is a component of the `WHERE` condition that allows you to find the last occurrence of data
before a certain date.

```anylog
period(time-interval, units, date-time, date-column, filter-criteria)
```

In most SQL languages in order to find the last occurrence of data the user usually needs to (slowly) increment the WHERE
condition. Thus lets say data hasn't came in for over 12 hours the user is not aware of this, they'd probably run
something like this:

```SQL 
-- first iteration 
WHERE timestamp <= NOW() - 1 hour 

-- second iteration 
WHERE timestamp <= NOW() - 12 hours

-- third iteration: data is found 
WHERE timestamp <= NOW() - 1 day 
```

The `period` function does that for the user automatically.

**Examples**: Get the last 10 rows from July 19 2026
```anylog
AL anylog-query +> <run client () sql cos format=table 
    "SELECT 
        timestamp, value 
    FROM 
        pv 
    WHERE 
        period(hour, 12, '2026-07-20 00:00:00', timestamp) 
    ORDER BY timestmap DESC 
    LIMIT 10;">

timestamp                  value
-------------------------- ------------------ 
2026-07-19 23:59:57.595244 1.9200000762939453 
2026-07-19 23:59:51.726978 1.9200000762939453 
2026-07-19 23:59:46.030184 1.9200000762939453 
2026-07-19 23:59:40.180862 1.9200000762939453 
2026-07-19 23:59:34.552881 1.9200000762939453 
2026-07-19 23:59:28.864503 1.9200000762939453 
2026-07-19 23:59:23.043708 1.9200000762939453 
2026-07-19 23:59:17.386626 1.9200000762939453 
2026-07-19 23:59:11.535526 1.9200000762939453 
2026-07-19 23:59:05.795202 1.9200000762939453 

{"Statistics":[{"Count": 10,
                "Time":"00:00:00",
                "Nodes": 1}]}
```

### `increments`

The `increments` function buckets or groups content into interval-based result sets.

```anylog
increments(time-unit, interval, date-column)
```
> Valid time units: `second`, `minute`, `hours`, `days`, `weeks`, `month`, `year`

Unlike the `period` function, this is something standard SQL can do natively — however, the syntax differs per SQL
dialect:

```SQL
-- Postgres 
SELECT date_trunc('hour', ts) AS hour_bucket, AVG(value)
FROM readings
WHERE ts >= NOW() - INTERVAL '3 hours'
GROUP BY hour_bucket
ORDER BY hour_bucket;

-- SQLite 
SELECT strftime('%Y-%m-%d %H:00:00', ts) AS hour_bucket, AVG(value)
FROM readings
WHERE ts >= datetime('now', '-3 hours')
GROUP BY hour_bucket
ORDER BY hour_bucket;
```

By defining `increments` as a way to divide a time range into fixed buckets and aggregate per bucket, AnyLog is
able to accomplish this across its network no matter the database engine underneath.


**Example** — Get 5 minute increments of data over the last 1 hour (from now)
```anylog
AL anylog-query +> <run client () sql cos format=table 
    "SELECT 
        increments(minute, 5, timestamp),  MIN(timestamp)::ljust(19), MAX(timestamp)::ljust(19), 
        MIN(value)::float(3), MAX(value)::float(3), AVG(value)::float(3), COUNT(*) 
    FROM 
        pv 
    WHERE 
        timestamp >= NOW() - 1 hour;">

min(timestamp)      max(timestamp)      min(value) max(value) avg(value) count(*)
------------------- ------------------- ---------- ---------- ---------- -------- 
2026-07-28 16:26:52 2026-07-28 16:29:58       3.87       3.87       3.87       34 
2026-07-28 16:30:03 2026-07-28 16:34:57       2.88       3.88      3.426       53 
2026-07-28 16:35:03 2026-07-28 16:39:56       2.88       2.89       2.88       48 
2026-07-28 16:40:01 2026-07-28 16:44:54       1.92       2.88      2.672       52 
2026-07-28 16:45:00 2026-07-28 16:49:56       1.91       1.92      1.919       52 
2026-07-28 16:50:02 2026-07-28 16:54:54       1.91       1.92      1.919       52 
2026-07-28 16:55:00 2026-07-28 16:59:56       1.91       1.92      1.919       52 
2026-07-28 17:00:01 2026-07-28 17:04:59       1.91       1.92      1.919       53 
2026-07-28 17:05:05 2026-07-28 17:09:59       1.91       1.92      1.919       52 
2026-07-28 17:10:04 2026-07-28 17:14:59       1.91       1.92      1.919       52 
2026-07-28 17:15:05 2026-07-28 17:19:58       1.91       1.92      1.919       52 
2026-07-28 17:20:03 2026-07-28 17:24:56       1.91       1.92      1.919       52 
2026-07-28 17:25:02 2026-07-28 17:26:43       1.91       1.92      1.918       18 

{"Statistics":[{"Count": 13,
                "Time":"00:00:00",
                "Nodes": 1}]}
```

## Via REST

For queries sent through an application (via REST) it is recommended to use `format=json:list and stat=false`.
That way the content returns as a list of JSONs that's machine readable without extra statistics or complex formatting.

```bash
curl -X GET 127.0.0.1:32349 \
  -H "command: sql mydb format=table SELECT timestamp, value FROM rand_data WHERE period(minute, 1, now(), timestamp)" \
  -H "User-Agent: AnyLog/1.23" \
  -H "destination: network" \
  -w "\n"

curl -X GET 127.0.0.1:32349 \
  -H "Content-Type: application/json" \
  -d '{"command": "sql mydb format=table SELECT timestamp, value FROM rand_data WHERE period(minute, 1, now(), timestamp)", "AnyLog-Agent": "AnyLog/1.23", "destination": "network"}' \
  -w "\n"
```

## Query Examples

Some more SQL examples with AnyLog.

```anylog
# Last minute of readings
run client () sql mydb format=table "select max(timestamp), avg(value) from ping_sensor where period(minute, 1, now(), timestamp)"

# 5-minute trends over a range
run client () sql mydb format=table "SELECT increments(minute, 5, timestamp), max(timestamp), avg(value) from ping_sensor where timestamp >= '2019-06-01' and timestamp < '2019-09-29'"

# Speed as formatted int with thousands separator
run client () sql lsl_demo "select reading_time, speed::int::format(':,') from performance where reading_time >= now() -3d"

# Time difference from last reading to now
run client () sql orics stat=false "select max(insert_timestamp)::timediff(now()) as time_diff FROM r_50"

# Per-second buckets with timezone and datetime formatting
<run client () sql new_company format=table and stat=false "
  SELECT increments(second, 1, timestamp),
    min(timestamp)::timezone(local)::datetime('%d-%b-%Y %H:%M') as min_ts,
    max(timestamp)::timezone(local)::datetime('%d-%b-%Y %H:%M') as max_ts,
    min(value), avg(value)::float(3), max(value)
  FROM rand_data
  WHERE timestamp >= '2024-12-20 00:00:00' AND timestamp <= '2025-01-10 23:59:59'
  ORDER BY min_ts DESC LIMIT 1">
```