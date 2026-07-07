---
title: Aggregations
description: Configure rolling time-interval aggregations on streaming data for real-time analytics without batch processing.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

> **AnyLog only.** Aggregation functions are not available in EdgeLake.

Aggregation functions summarize streaming data over defined time intervals. For each table, you configure the interval duration and the number of intervals to retain, enabling continuous rolling statistics (count, sum, avg, min, max) as data arrives.

---

## Aggregations and database write modes

By default, raw source data is written to the database and aggregations are maintained **in memory only**. You can change this:

```anylog
set aggregation ingest where dbms = [dbms] and table = [table] and source = [true/false] and derived = [true/false]
```

| Option | Default | Description |
|---|---|---|
| `source` | `true` | Whether raw source data is written to the DB |
| `derived` | `false` | Whether aggregation results are written to the DB |

View current ingest mode:
```anylog
get aggregation ingest
```

---

## Declaring aggregations

```anylog
set aggregation where dbms = [dbms name]
      and table = [table name]
      and intervals = [count]
      and time = [interval time]
      and time_column = [time column name]
      and value_column = [value column name]
      and target_dbms = [target dbms name]
      and target_table = [target table name]
```

| Parameter | Default | Description |
|---|---|---|
| `dbms` | — | Source database name |
| `table` | — | Source table name. If omitted, applies to all tables in the database |
| `intervals` | 10 | Number of intervals to keep in memory |
| `time` | 1 minute | Interval length: seconds, minutes, hours, or days |
| `time_column` | `timestamp` | Name of the timestamp column |
| `value_column` | `value` | Column being aggregated |
| `target_dbms` | same as source | Database to store aggregation results |
| `target_table` | same as source | Table to store aggregation results |

### Metrics computed per interval

| Metric | Description |
|---|---|
| Min | Lowest value in the interval |
| Max | Highest value in the interval |
| Avg | Average value in the interval |
| Count | Number of events in the interval |
| Events/sec | Count ÷ interval duration |

### Example

```anylog
set aggregation where dbms = dmci and table = sensor_table and intervals = 10 and time = 1 minute and time_column = timestamp and value_column = value
```

---

## Declaring thresholds

Thresholds can be used by the rule engine to trigger alerts or influence processing:

```anylog
set aggregation thresholds where dbms = [dbms] and table = [table] and column = [column] and min = [value] and max = [value] and avg = [value] and count = [count]
```

---

## Aggregation encoding

Encoding compresses time-interval data into compact representations, reducing storage volume significantly for high-frequency streams.

```anylog
set aggregations encoding where dbms = lsl_demo and table = ping_sensor and encoding = [type] and tolerance = [value]
```

| Encoding type | Description |
|---|---|
| `none` | No encoding (default) |
| `bounds` | Each interval → single row with `timestamp`, `end_interval`, `min_val`, `max_val`, `avg_val`, `events` |
| `arle` | Approximated Run-Length Encoding — groups consecutive similar values. `tolerance` is the % difference allowed within a group |

The encoded table is named with the encoding type as a prefix: e.g. `arle_my_table`.

---

## Retrieving aggregations

### Current values (in-memory)

```anylog
get aggregation
get aggregation where dbms = orics
get aggregation where dbms = orics and table = r_50
get aggregation where dbms = orics and table = r_50 and value_column = seal_storage
```

Get the most recent value for a specific function:
```anylog
get aggregation where dbms = lsl_demo and table = ping_sensor and function = max
```

### By time range

```anylog
get aggregation by time where dbms = [dbms] and table = [table] and value_column = [col] and function = [fn] and limit = [n] and format = [table/json]
```

| Parameter | Default | Description |
|---|---|---|
| `value_column` | — | Column(s) to retrieve. Use `*` for all |
| `function` | count, avg, min, max | One or more aggregation functions |
| `timezone` | local | Timezone for timestamps |
| `format` | table | `table` or `json` |
| `limit` | 0 (no limit) | `limit = 1` returns the latest values |

Examples:
```anylog
get aggregation by time where dbms = orics and table = r_50 and value_column = *
get aggregation by time where dbms = orics and table = r_50 and value_column = * and limit = 1
get aggregation by time where dbms = orics and table = r_50 and value_column = cy_min and function = min and function = max and function = avg::float(3) and format = json
```

---

## Ingestion frequency for aggregation tables

```anylog
set ingestion in aggregations where dbms = [dbms] and table = [table] and frequency = [continuous|time|none] and interval = [interval]
```

| frequency | Description |
|---|---|
| `continuous` | Real-time ingestion |
| `time` | Ingestion at set interval (requires `interval` parameter, e.g. `1 minute`) |
| `none` | Stop ingestion |

Examples:
```anylog
set ingestion in aggregations where dbms = orics and table = r_50 and frequency = continuous
set ingestion in aggregations where dbms = orics and frequency = time and interval = 1 minute
set ingestion in aggregations where dbms = orics and table = r_50 and frequency = none
```

---

## Reset and inspect

```anylog
# Remove aggregation declarations
reset aggregations where dbms = [dbms] and table = [table] and value_column = [col]

# View aggregation configs
get aggregation configs
get aggregation configs where dbms = lsl_demo and table = ping_sensor

# View aggregation table ingestion status
get aggregation tables where dbms = orics and table = r_50
```

---

## Grafana integration

To pull aggregations from Grafana, set the following in the dashboard **Payload** section:

```json
{
  "servers": ["10.0.0.78:7848"],
  "type": "aggregations",
  "functions": ["min", "max", "avg", "count"],
  "table": "r_50",
  "timestamp_column": "timestamp",
  "value_column": ["filler_cyc_time", "run_hours"],
  "limit": 0
}
```

---

## OPC-UA with aggregations

See <a href="{{ '/docs/opcua//#example---declaring-opc-ua-with-aggregations' | relative_url }}">OPC-UA — Declaring aggregations</a> for a full configuration walkthrough.