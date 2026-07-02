---
title: Querying Data (Northbound)
description: Run SQL queries across distributed operator nodes, with time-series functions, casting, and formatting options.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

Queries are issued to a **Query Node** which uses blockchain metadata to locate the relevant Operator nodes, distributes the query, and assembles a unified result. See <a href="{{ '/docs/introduction//#how-querying-works' | relative_url }}">How Querying Works</a> for the architecture background.

---

## Discover tables and columns

Before querying, you can inspect what data is available across the network.

```anylog
# List all virtual tables
get virtual tables
get virtual tables where table = ping_sensor

# Show which nodes host each table
get data nodes
get data nodes where table = ping_sensor
get data nodes where sort = (1,2)    # sort by DBMS (col 1), table (col 2)

# List columns of a table
get columns where dbms = [dbms] and table = [table] and format = [table|json]
```

> The first four columns AnyLog adds to every table — `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id` — are for internal data management. You can safely ignore them in SELECT statements.

---

## Network queries with `run client`

Without `run client`, a query executes only on the local node. To query across the network:

```anylog
run client () sql [dbms name] [options] "SELECT ..."
```

The empty `()` tells AnyLog to determine target nodes from metadata automatically. To target specific nodes:

```anylog
run client (24.23.250.144:7848, 16.87.143.85:7848) sql litsanleandro format = table "select * from ping_sensor limit 100"
```

Via REST, use the header `-H "destination: network"` instead of specifying a node.

---

## Query options

Options are expressed as `key = value` pairs separated by `and`:

| Key | Values | Default | Description |
|---|---|---|---|
| `format` | `json` / `table` / `json:list` / `json:output` | `json` | Output format |
| `timezone` | `utc` / `local` / `pt` / `mt` / `ct` / `et` / tz name | `local` | Timezone for timestamps |
| `stat` | `true` / `false` | `true` | Include processing statistics |
| `max_time` | seconds | — | Cap query execution time |
| `drop` | `true` / `false` | `true` | Drop local output table after query |
| `dest` | `stdout` / `rest` / `dbms` / `file` | dynamic | Destination for result set |
| `include` | `dbms.table` | — | Treat a differently-named remote table as the queried table |
| `extend` | column list | — | Include node variables (e.g. `@ip`, `@port`) in results |
| `nodes` | `main` / `all` | `main` | HA: `main` uses designated primary operators; `all` uses round-robin |
| `committed` | `true` / `false` | `false` | HA: only return data confirmed synced across cluster nodes |

### Format values

| Value | Description |
|---|---|
| `json` | Default — result in `{"Query": [...]}` with optional `Statistics` key |
| `json:output` | Newline-delimited JSON rows (matches data load format) |
| `json:list` | List format — use with PowerBI |
| `table` | Human-readable table |

---

## Supported SQL

**Projection:** column names, `min`, `max`, `sum`, `count`, `avg`, `count distinct`, `range`, time functions

**WHERE clause:** `>`, `<`, `=`, `!=`, `group by`, `order by`, `limit`

---

## Time functions

Use `now()`, `date()`, and `timestamp()` in WHERE clauses:

```anylog
# Last 3 days
select * from ping_sensor where reading_time >= now() -3d

# Start of month modifiers
select * from ping_sensor where reading_time = date('now','start of month','+1 month','-1 day')

# Relative shorthand: t = minutes
select * from ping_sensor where reading_time >= now() -4t
```

Time unit shorthands: `s` (seconds), `t` (minutes), `h` (hours), `d` (days), `w` (weeks), `m` (months), `y` (years)

Get the current datetime string for a timezone:
```anylog
get datetime et now()
get datetime local now() + 3 days
get datetime Asia/Shanghai timestamp('now','start of month','+1 month','-1 day')
```

---

## Cast data

Apply casts to projected columns using `::`:

```anylog
select reading_time, speed::float(2) from performance where reading_time >= now() -3d
```

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

Multiple casts can be chained: `speed::float(2)::format(:,)`

### Formatting options

| Type | Description |
|---|---|
| `:,` | Comma as thousands separator |
| `:b` | Binary |
| `:x` | Hex |
| `:o` | Octal |
| `:e` | Scientific notation |
| `:.3f` | Float with 3 decimal places |
| `:08.3f` | Float with zero-padded width |

---

## Time-series optimised queries

### `period` — last occurrence before a timestamp

Finds the first occurrence of data at or before a given date, within a time window:

```anylog
period(time-interval, units, date-time, date-column, filter-criteria)
```

Examples:
```anylog
# Last minute of readings right now
select max(timestamp), avg(value) from ping_sensor where period(minute, 1, now(), timestamp)

# Last minute before a specific time
select max(timestamp), avg(value) from ping_sensor where period(minute, 1, '2019-09-29 19:34:09', timestamp)

# With filter
select max(timestamp), avg(value) from ping_sensor where period(minute, 1, '2019-09-29 19:34:09', timestamp, and device_name = 'APC SMART X 3000')
```

### `increments` — time-bucket aggregation

Divides a time range into fixed buckets and aggregates per bucket:

```anylog
increments(time-unit, interval, date-column)
```

Valid time units: `second`, `minute`, `hours`, `days`, `weeks`, `month`, `year`

Example — 5-minute buckets over a date range:
```anylog
SELECT increments(minute, 5, timestamp), max(timestamp), avg(value)
from ping_sensor
where timestamp >= '2019-06-01 19:34:09' and timestamp < '2019-09-29 19:34:09'
```

### `increments` (optimised) — auto-sized buckets

Let AnyLog choose the interval to return approximately N data points:

```anylog
increments(number_of_points, date_column)
```

> Requires a WHERE clause filtering on the date column.

```anylog
select increments(timestamp, 1000), min(timestamp), max(timestamp), count(value)
from t13
where timestamp >= '2025-04-08' and timestamp < '2025-04-09'
```

### Get optimal increment params

Pre-calculate the best increment parameters for a visualization:

```anylog
get increments params where dbms = my_dbms and table = t13 and column = timestamp
    and where = "timestamp >= '2025-04-08 17:30:19' and timestamp <= '2025-04-08 19:12:01'"
    and data_points = 1000
    and format = table
```

---

## Query examples

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
run client () sql new_company format=table and stat=false "
  SELECT increments(second, 1, timestamp),
    min(timestamp)::timezone(local)::datetime('%d-%b-%Y %H:%M') as min_ts,
    max(timestamp)::timezone(local)::datetime('%d-%b-%Y %H:%M') as max_ts,
    min(value), avg(value)::float(3), max(value)
  FROM rand_data
  WHERE timestamp >= '2024-12-20 00:00:00' AND timestamp <= '2025-01-10 23:59:59'
  ORDER BY min_ts DESC LIMIT 1"
```

---

## Via REST

```bash
curl -X GET 127.0.0.1:32349 \
  -H "command: sql mydb format=table SELECT timestamp, value FROM rand_data WHERE period(minute, 1, now(), timestamp)" \
  -H "User-Agent: AnyLog/1.23" \
  -H "destination: network" \
  -w "\n"
```

> Always add `-w "\n"` and keep the command on one line to avoid chunked-encoding errors.