---
title: Grafana
description: Connect Grafana to AnyLog to visualize time-series and metadata using increments, period, and custom SQL queries.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

Grafana is AnyLog's default demo BI tool. It connects via the JSON datasource plugin and issues SQL queries to AnyLog's query node over REST.

> We support Grafana 7.5+. Recommended: **9.5.16** or higher.

---

## Prerequisites

**1. Run Grafana** (Docker):
```bash
docker run --name=grafana \
  -e GF_AUTH_ANONYMOUS_ENABLED=true \
  -e GF_SECURITY_ALLOW_EMBEDDING=true \
  -e GF_INSTALL_PLUGINS=simpod-json-datasource,grafana-worldmap-panel \
  -e GF_SERVER_HTTP_PORT=3000 \
  -v grafana-data:/var/lib/grafana \
  -it -d -p 3000:3000 --rm grafana/grafana:9.5.16
```

**2. Enable REST on the AnyLog query node:**
```anylog
<run rest server where
  external_ip = !external_ip and external_port = !anylog_rest_port and
  internal_ip = !ip and internal_port = !anylog_rest_port and
  bind = false and threads = 6 and timeout = 0>
```

---

## Configure the data source

1. Open Grafana at `http://localhost:3000`
2. Go to **Configuration → Data Sources → Add data source**
3. Select **JSON** (from the `simpod-json-datasource` plugin)
4. Set:
   - **URL**: `http://[anylog-query-ip]:[rest-port]`  (e.g. `http://10.0.0.25:32349`)
   - **Custom HTTP Headers**: add `dbms` header with the default database name (optional — if omitted, all accessible databases are available)
5. Click **Save & Test** — expect a green "Data source is working" banner

### With authentication

- **Basic auth** (username/password): enable "Basic Auth" toggle in Grafana data source settings
- **SSL certificates**: enable "TLS Client Auth" and "Skip TLS Verify"

---

## Query types

AnyLog provides two optimised query types via the **Additional JSON Data** payload field, plus full custom SQL.

### Payload fields reference

| Field | Description |
|---|---|
| `type` | `increments` (default), `period`, `info`, `map`, `aggregations` |
| `sql` | Custom SQL statement |
| `details` | Any non-SQL AnyLog command |
| `where` | Additional WHERE condition appended to the query |
| `time_column` | Name of the timestamp column |
| `value_column` | Name of the value column |
| `functions` | List of aggregation functions to apply |
| `include` | Treat additional tables as part of the queried table |
| `extend` | Append node metadata to results (e.g. `@table_name`, `@ip`) |
| `timezone` | `utc` (default) or `local` |
| `time_range` | `true/false` — whether to apply the Grafana time range to the query |
| `servers` | Override network-determined nodes with specific IP:Port list |
| `grafana.format_as` | `timeseries` or `table` |
| `grafana.data_points` | Approximate number of data points — auto-tunes the increments interval |

---

## Increments query (time-series)

The default query type. Divides the selected time range into buckets and returns min/max/avg/count per bucket.

```json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": {
    "format_as": "timeseries",
    "data_points": 1000
  }
}
```

Adding `data_points` lets AnyLog automatically calculate the optimal time interval and unit for the requested number of buckets. If omitted, Grafana's **Interval** setting is used.

With `include` and `extend`:
```json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "extend": ["@table_name"],
  "include": ["t98"],
  "grafana": {
    "format_as": "timeseries"
  }
}
```

With a WHERE filter:
```json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "where": "device_name='ADVA FSP3000R7'",
  "grafana": { "format_as": "timeseries" }
}
```

---

## Period query (latest value)

Returns the most recent value within the selected time range (or nearest to the end of it), then aggregates over a window ending at that point.

```json
{
  "type": "period",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": { "format_as": "timeseries" }
}
```

Without time range (all data):
```json
{
  "type": "period",
  "time_column": "timestamp",
  "value_column": "value",
  "time_range": false,
  "functions": ["min", "max", "avg", "count"],
  "grafana": { "format_as": "timeseries" }
}
```

---

## Aggregations query

Pull rolling aggregations (configured via `set aggregation`) directly into Grafana:

```json
{
  "servers": ["10.0.0.78:32149"],
  "type": "aggregations",
  "functions": ["min", "max", "avg", "count"],
  "table": "r_50",
  "timestamp_column": "timestamp",
  "value_column": ["filler_cyc_time", "run_hours"],
  "limit": 0
}
```

> `servers` must specify a single operator node for aggregations queries.

---

## Network map (blockchain metadata)

Visualise node locations on a world map:

1. Visualisation: **Geomap**
2. Payload:
```json
{
  "type": "map",
  "member": ["master", "query", "operator", "publisher"],
  "metric": [0, 0, 0],
  "attribute": ["name", "name", "name", "name"]
}
```

## Blockchain table

Display node metadata in a table:

1. Visualisation: **Table**
2. Payload:
```json
{
  "type": "info",
  "details": "blockchain get operator bring.json [*][cluster] [*][name] [*][company] [*][ip] [*][country] [*][state] [*][city]"
}
```

---

## Tips

- Set **Max data points** in Query Options to control result density for time-series panels — without it, min/max/avg lines collapse into a single line
- Use `format_as: timeseries` for time-series panels (Time series, Gauge) and `table` for table panels
- See <a href="{{ '/docs/queries//' | relative_url }}">Querying Data</a> for full details on `increments`, `period`, and query options like `include` and `extend`