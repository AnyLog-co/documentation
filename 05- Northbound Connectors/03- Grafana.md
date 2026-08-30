---
title: "Using Grafana"
description: Query and visualize AnyLog data in Grafana — increments/period/aggregations queries, blockchain visualizations, and importing sample dashboards.
layout: page
---

<!---
### 📜 Change Log

| **Date** | **Name** | **Change** |
|---|---|---|
| 2026-04-17 | | Created document |
| 2026-07-17 / 2026-07-20 | Eric Aquaronne | Added change log |
| 2026-07-25 | Ori Shadmon | Split from the deployment/connection content (now in **AnyLog & Grafana**) — this file
  covers what to do once Grafana is already connected. Backbone is "03-1 Connecting Grafana.md" (already a clean
  rewrite that added an Aggregations query type missing from the older docs), with the dropped screenshots restored
  from "Using Grafana.md" and the dashboard-import walkthrough merged in from "Importing Grafana Dashboard.md". Its
  duplicate, "03-2 Importing Grafana Dashboard.md", was corrupted (broken HTML from what looks like a bad export —
  stray `>text</a>` fragments after every image/link) and contributed nothing usable; excluded rather than repaired. |
| 2026-08-29 | Moshe Shadmon | Updated document |

--->
---
title: "Grafana"
description: "Connect Grafana to AnyLog and visualize distributed operational data and metadata."
layout: page
---

# Grafana

[Grafana](https://grafana.com/) can be used to visualize operational data and metadata available through an AnyLog network.

Grafana connects to an AnyLog node through the **AnyLog REST API**. The connected node acts as a client to the AnyLog network and provides Grafana with access to distributed data without requiring Grafana to connect directly to each Operator or underlying database.

```text
                         Grafana
                            │
                            │ REST
                            ▼
                       AnyLog Node
                            │
                     Metadata Lookup
                            │
               ┌────────────┼────────────┐
               ▼            ▼            ▼
           Operator 1   Operator 2   Operator 3
               │            │            │
               └────────────┼────────────┘
                            ▼
                      Unified Result
                            │
                            ▼
                         Grafana
```

AnyLog uses the network metadata to determine where the requested data is physically maintained, distributes the query to the relevant Operators, and returns a unified result to Grafana.

Grafana can be used to visualize:

- time-series data,
- tabular query results,
- aggregated operational data,
- data distributed across multiple tables and Operators,
- AnyLog metadata,
- and the geographic distribution of AnyLog nodes.

---

## Prerequisites

To use Grafana with AnyLog, you need:

- A running Grafana instance.
- The Grafana JSON data source plugin supported by AnyLog.
- An AnyLog node accessible from the Grafana server.
- The AnyLog REST service running on that node.
- Network access from Grafana to the AnyLog REST IP and port.

---

## Running Grafana with Docker

The following example starts Grafana with the JSON data source and world map plugins:

~~~bash
docker run --name=grafana \
  -e GRAFANA_ADMIN_USER=admin \
  -e GRAFANA_ADMIN_PASSWORD=admin \
  -e GF_AUTH_DISABLE_LOGIN_FORM=false \
  -e GF_AUTH_ANONYMOUS_ENABLED=true \
  -e GF_SECURITY_ALLOW_EMBEDDING=true \
  -e GF_INSTALL_PLUGINS=simpod-json-datasource,grafana-worldmap-panel \
  -e GF_SERVER_HTTP_PORT=3000 \
  -v grafana-data:/var/lib/grafana \
  -v grafana-log:/var/log/grafana \
  -v grafana-config:/etc/grafana \
  -it -d -p 3000:3000 \
  grafana/grafana:9.5.16
~~~

Grafana is then available on port `3000`.

For example:

~~~text
http://localhost:3000
~~~

---

## Configure the AnyLog REST Service

The AnyLog node used by Grafana must provide a REST connection.

The REST service is normally started as part of the node configuration.

For example:

~~~anylog
<run rest server where
    external_ip=!external_ip and
    external_port=!anylog_rest_port and
    internal_ip=!ip and
    internal_port=!anylog_rest_port and
    bind=!rest_bind and
    threads=!rest_threads and
    timeout=!rest_timeout
>
~~~

The external IP and REST port must be reachable from the Grafana server.

Verify that the REST service is running:

~~~anylog
get processes
~~~

---

## Configure the Grafana Data Source

In Grafana:

1. Open **Connections → Data Sources**.
2. Add the JSON data source supported by the AnyLog Grafana interface.
3. Provide a unique name for the connection.
4. Set the URL to the REST address exposed by the AnyLog node.

For example:

~~~text
http://10.0.0.25:2049
~~~

5. Optionally configure a default logical database using the Custom HTTP Headers supported by the AnyLog interface.
6. Select **Save & Test**.

A successful connection should report:

~~~text
Data source is working
~~~

If no default database is specified, the databases accessible through the AnyLog node can be made available to Grafana.

The connected AnyLog node does **not** need to physically host the requested data. AnyLog uses the network metadata to locate the Operators that maintain the requested table.

---

## Authentication

If authentication is enabled on the AnyLog REST interface, configure the Grafana data source with the corresponding authentication settings.

For REST authentication using username and password, enable **Basic Auth** in the Grafana data source.

When using SSL certificates, configure the corresponding TLS options in Grafana, including **TLS Client Auth** when required.

The Grafana authentication configuration must match the authentication and security configuration of the AnyLog REST service.

---

## Troubleshooting the Connection

If **Save & Test** fails, verify:

- the AnyLog node is running,
- the REST service is running,
- the configured REST IP and port are correct,
- the REST port is reachable from the Grafana server,
- firewall rules allow the connection,
- Grafana authentication settings match the AnyLog REST configuration,
- the AnyLog node has synchronized metadata,
- and the requested databases and tables are represented in the metadata.

Useful AnyLog commands include:

~~~anylog
get processes
test node
test network
blockchain get table
~~~

If Grafana reports:

~~~text
Error: No table connected
~~~

verify that the connected AnyLog node can discover the tables associated with the selected logical database.

---

# Querying AnyLog from Grafana

Grafana can present AnyLog data primarily in two formats:

- **Time Series** — values displayed as a function of time.
- **Table** — query results displayed as rows and columns.

AnyLog provides predefined query types optimized for Grafana, including:

- `increments`
- `period`

Grafana can also issue custom SQL queries and AnyLog metadata requests.

Query behavior is controlled using the panel's **Additional JSON Data**.

---

## Additional JSON Data

The Additional JSON Data payload provides instructions to AnyLog about how the query should be executed.

For example:

~~~json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": {
    "format_as": "timeseries",
    "data_points": 1000
  }
}
~~~

Common attributes include:

| Attribute | Description |
| --- | --- |
| `dbms` | Logical database to query. Overrides the default database configured for the data source. |
| `table` | Table to query. Overrides the table selected or specified by the SQL statement. |
| `type` | Query type, such as `increments`, `period`, `info`, or `map`. |
| `sql` | SQL statement to execute. |
| `details` | AnyLog command to execute instead of SQL. |
| `where` | Additional SQL `WHERE` condition. |
| `functions` | List of aggregation functions to apply. |
| `timezone` | Determines timestamp handling. |
| `time_column` | Timestamp column used by time-series queries. |
| `value_column` | Value column used by the visualization. |
| `time_range` | Determines whether the Grafana-selected time range is applied. |
| `servers` | Explicitly identifies Operators instead of using metadata-based routing. |
| `include` | Adds additional tables to the logical query. |
| `extend` | Adds source metadata to the returned rows. |
| `instructions` | Additional AnyLog query instructions. |
| `grafana.format_as` | Grafana result format, typically `timeseries` or `table`. |
| `grafana.data_points` | Approximate number of data points requested from an `increments` query. |

Values in Additional JSON Data override corresponding default values where applicable.

---

# Time-Series Visualization

## Increments Query

The `increments` query is designed for visualizing time-series data over a selected Grafana time range.

AnyLog divides the requested time range into intervals and applies functions such as `min`, `max`, and `avg` to each interval.

A basic payload is:

~~~json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": {
    "format_as": "timeseries",
    "data_points": 1000
  }
}
~~~

AnyLog translates the Grafana request into a distributed SQL query.

Conceptually, the generated query is similar to:

~~~sql
SELECT
    increments(second, 1, timestamp),
    max(timestamp) AS timestamp,
    avg(value) AS avg_val,
    min(value) AS min_val,
    max(value) AS max_val
FROM percentagecpu_sensor
WHERE
    timestamp >= '2024-02-19T19:42:02.133Z'
    AND timestamp <= '2024-02-19T19:57:02.133Z'
LIMIT 2128;
~~~

The actual interval is determined from the requested time range and query configuration.

---

## Data Points

The `data_points` attribute allows AnyLog to dynamically determine an appropriate interval for an `increments` query.

For example:

~~~json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": {
    "format_as": "timeseries",
    "data_points": 1000
  }
}
~~~

AnyLog attempts to return approximately the requested number of time buckets.

This provides a balance between:

- query performance,
- graph resolution,
- and the amount of data returned to Grafana.

If `data_points` is not specified, the Grafana interval configured in **Query Options** is used.

Grafana's **Max data points** setting may also limit the number of rows displayed.

---

## Query Multiple Tables

The `include` option allows multiple tables to be processed as a single logical query.

For example:

~~~json
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
~~~

If the selected table is `t99`, the query processes data from both:

~~~text
t99
t98
~~~

The corresponding AnyLog distributed query includes:

~~~anylog
run client () sql nov timezone = utc and pass_through = false and include = (t98) and extend = (@dbms_name,@table_name)
~~~

followed by the SQL statement.

The `include` option is useful when operational data with the same logical structure is distributed across multiple tables.

---

## Extend Query Results with Source Metadata

The `extend` option adds metadata about the source of each returned row.

For example:

~~~json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "extend": ["@table_name"],
  "grafana": {
    "format_as": "timeseries"
  }
}
~~~

This allows Grafana to preserve information about where each value originated.

Depending on the query, extensions can include values such as:

~~~text
@dbms_name
@table_name
@ip
~~~

This is particularly useful when a Grafana panel combines data from multiple tables, nodes, or data sources.

---

## Add a WHERE Condition

Additional filtering can be applied using `where`.

For example:

~~~json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "where": "device_name='ADVA FSP3000R7'",
  "grafana": {
    "format_as": "timeseries"
  }
}
~~~

The condition is added to the SQL query generated for the panel.

---

# Period Query

A `period` query retrieves values associated with the end of the selected time range.

If a value is not available exactly at the end of the range, AnyLog identifies the latest available time and calculates the requested statistics for the corresponding period.

For example:

~~~json
{
  "type": "period",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": {
    "format_as": "timeseries"
  }
}
~~~

The resulting SQL is conceptually similar to:

~~~sql
SELECT
    max(timestamp) AS timestamp,
    avg(value) AS avg_val,
    min(value) AS min_val,
    max(value) AS max_val
FROM ping_sensor;
~~~

`period` queries are useful for Grafana visualizations such as:

- Gauge
- Stat
- Current-value panels

---

## Period Query with Filtering

A `where` condition can also be applied to a period query:

~~~json
{
  "type": "period",
  "time_column": "timestamp",
  "value_column": "value",
  "where": "device_name='ADVA FSP3000R7'",
  "grafana": {
    "format_as": "timeseries"
  }
}
~~~

---

## Specify Aggregation Functions

The functions applied by a query can be explicitly specified.

For example:

~~~json
{
  "type": "period",
  "time_column": "timestamp",
  "value_column": "value",
  "time_range": false,
  "functions": ["min", "max", "avg", "count"],
  "grafana": {
    "format_as": "timeseries"
  }
}
~~~

In this example:

~~~json
"time_range": false
~~~

instructs AnyLog not to restrict the query using the Grafana-selected time range.

---

# Metadata Visualization

Grafana can also visualize the AnyLog metadata layer.

This allows dashboards to display information about the network itself, including nodes, locations, clusters, and other metadata policies.

The metadata may be maintained by either an AnyLog Master Node or a blockchain platform. The same AnyLog metadata commands are used in either configuration.

---

## Network Map from Metadata

A Grafana **Geomap** panel can display the geographic distribution of AnyLog nodes.

In Grafana:

1. Create or edit a panel.
2. Select **Geomap** as the visualization.
3. Select a table in the Metric section.
4. Add the following payload:

~~~json
{
  "type": "map",
  "member": ["master", "query", "operator", "publisher"],
  "metric": [0, 0, 0],
  "attribute": ["name", "name", "name", "name"]
}
~~~

AnyLog retrieves the relevant node metadata and returns the information required by the map visualization.

---

## Metadata Table

A Grafana **Table** panel can display AnyLog metadata policies.

For example, to display Operator information:

~~~json
{
  "type": "info",
  "details": "blockchain get operator bring.json [*][cluster] [*][name] [*][company] [*][ip] [*][country] [*][state] [*][city]"
}
~~~

The `details` attribute contains an AnyLog command rather than SQL.

In this example, Grafana receives information describing Operators, including:

- cluster,
- name,
- company,
- IP,
- country,
- state,
- and city.

Although the command is named `blockchain get`, it queries the AnyLog metadata available to the node and works with metadata synchronized from either a Master Node or a blockchain platform.

---

# Using a Different Logical Database

A Grafana data source can be configured with a default logical database.

A panel can override that database using `dbms`.

For example:

~~~json
{
  "dbms": "manufacturing",
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "temperature",
  "grafana": {
    "format_as": "timeseries"
  }
}
~~~

AnyLog then resolves the requested table within the `manufacturing` logical database.

---

### 1. Current-Value Gauge

Use:

~~~json
{
  "type": "period",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": {
    "format_as": "timeseries"
  }
}
~~~

### 2. Operator Metadata Table

Use:

~~~json
{
  "type": "info",
  "details": "blockchain get operator bring.json [*][name] [*][company] [*][ip] [*][cluster]"
}
~~~

Together, these panels verify:

- REST connectivity,
- metadata access,
- distributed SQL processing,
- time-series formatting,
- and metadata queries.

---

# Troubleshooting Queries

If Grafana is connected but a panel does not return data, first verify that AnyLog can discover the requested table:

~~~anylog
blockchain get table
~~~

Verify the network:

~~~anylog
test network
~~~

Check the node services:

~~~anylog
get processes
~~~

Review errors:

~~~anylog
get error log
~~~

For distributed SQL, the equivalent query can also be tested directly from the AnyLog CLI:

~~~anylog
run client () sql <dbms> format = table and stat = <SQL statement>
~~~

Testing the query from the CLI helps determine whether an issue is related to the AnyLog query itself or to the Grafana panel configuration.

---

# Related Documentation

- [SQL Commands](/docs/07-cli/04-sql/) — distributed SQL syntax and query options.
- [Blockchain & Metadata](/docs/08-blockchain-and-metadata/) — metadata policies, synchronization, and metadata commands.
- [Unified Namespace](/docs/08-blockchain-and-metadata/04-unified-namespace/) — logical navigation over distributed operational data.
- **REST API** — configuring and using the AnyLog REST interface.
- **Networking & Security** — authentication, TLS, permissions, and network configuration.

<!---


This assumes Grafana is already deployed and connected to an AnyLog node as a JSON data source — see
**AnyLog & Grafana** if you haven't done that yet.

Grafana can display AnyLog data in two ways: **Time Series** (values over time) and **Table** (rows and columns).
Queries are issued via the **Additional JSON Data** panel field, either using AnyLog's two optimized query types
(`increments`, `period`) or a plain SQL statement.

<img src="../../imgs/grafana_dashboard_layout.png" alt="Grafana Page Layout" />

---

## Query types reference

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
| `time_range` | `true`/`false` — whether to apply the Grafana time range to the query |
| `servers` | Override network-determined nodes with a specific IP:Port list |
| `grafana.format_as` | `timeseries` or `table` |
| `grafana.data_points` | Approximate number of data points — auto-tunes the increments interval |

---

## Increments query (time-series)

The default query type. Divides the selected time range into intervals and returns min/max/avg/count per interval.

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

Adding `data_points` lets AnyLog automatically calculate the optimal time interval/unit for the requested number of
buckets — balancing performance, readability, and visual resolution. If omitted, Grafana's own **Interval** setting
is used instead. Grafana's **limit** (Query Options) is also applied; if the result exceeds it, only a subset is
returned.

**With `include` and `extend`:**
```json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "extend": ["@table_name"],
  "include": ["t98"],
  "grafana": { "format_as": "timeseries" }
}
```

`include` treats multiple tables as one logical source (querying `t99` with `include: ["t98"]` pulls and merges
data from both). `extend` appends source metadata to the result — `@table_name` groups results by their table of
origin, preserving context.

**With a WHERE filter:**
```json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "where": "device_name='ADVA FSP3000R7'",
  "grafana": { "format_as": "timeseries" }
}
```

### Increments graph

1. Visualization: **Time series**
2. Metric: select the table to query
3. Payload:
```json
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": { "format_as": "timeseries" }
}
```
4. Under **Query Options**, set **Max data points** — otherwise min/max/avg collapse into what looks like a single line.

<img src="../../imgs/grafana_increments_graph.png" alt="Increments Graph" width="75%" height="75%" />

---

## Period query (latest value)

Returns the most recent value within the selected time range (or nearest to the end of it), then aggregates over a
window ending at that point.

```json
{
  "type": "period",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": { "format_as": "timeseries" }
}
```

**Without a time range** (all data, explicit functions):
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

### Period graph

1. Visualization: **Gauge**
2. Metric: select the table to query
3. Payload:
```json
{
  "type": "period",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": { "format_as": "timeseries" }
}
```
4. Under **Query Options**, set **Max data points** — same reason as above.

<img src="../../imgs/grafana_period_gauge.png" alt="Period Gauge" width="75%" height="75%" />

---

## Aggregations query

Pulls rolling aggregations — configured via `set aggregation` on the AnyLog side — directly into Grafana:

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

> `servers` must name a single operator node for aggregations queries.

---

## Network map (blockchain metadata)

Plot node locations on a world map.

1. Visualization: **Geomap**
2. Metric: any table (the map is populated from blockchain metadata, not table contents)
3. Payload:
```json
{
    "type" : "map",
    "member" : ["master", "query", "operator", "publisher"],
    "metric" : [0, 0, 0],
    "attribute" : ["name", "name", "name", "name"]
}
```

<img src="../../imgs/grafana_geomap.png" alt="Network Map" width="75%" height="75%" />

## Blockchain table

Display node metadata as a table.

1. Visualization: **Table**
2. Metric: any table
3. Payload:
```json
{
    "type": "info",
    "details": "blockchain get operator bring.json [*][cluster] [*][name] [*][company] [*][ip] [*][country] [*][state] [*][city]"
}
```

<img src="../../imgs/grafana_blockchain_table.png" alt="Blockchain Table" width="75%" height="75%" />

---

## Importing the sample dashboards

Rather than building panels one at a time as above, AnyLog provides pre-built dashboard JSON files you can import
wholesale:

* **[Network Map](../imgs/grafana_json/network_summary.json)** — a map of all nodes in the network, a list of
  operator nodes, and a list of tables supported across the network.

  <img src="../imgs/grafana_network_map.png" alt="grafana_network_map.png">

* **[EdgeX Diagram](../imgs/grafana_json/edgex_dashboard.json)** — a line graph of min/avg/max plus gauges for
  total and per-node row counts, fed from the EdgeX MQTT sample connection.

  <img src="../imgs/grafana_edgex_dashboard.png" alt="grafana_edgex_dashboard.png">

### Steps

1. In a new dashboard, go to **Settings**:

   <img src="../imgs/grafana_base_dashboard.png" alt="Empty Dashboard" />

2. Go to **JSON Model** and paste in the desired model — the JSON object that defines the dashboard (e.g. the
   [EdgeX Dashboard](../imgs/grafana_json/edgex_dashboard.json) above):

   | Empty JSON Model | Filled JSON Model |
   |:---:|:---:|
   | <img src="../imgs/grafana_json_model_empty.png" alt="Empty JSON Model" width="75%" height="75%" /> | <img src="../imgs/grafana_json_model.png" alt="JSON Model" width="75%" height="75%"/> |

3. Save changes.

4. You should now see the new dashboard:

   | Before | After |
   |:---:|:---:|
   | <img src="../imgs/grafana_no_dashboard.png" alt="No Dashboards" /> | <img src="../imgs/grafana_new_dashboard.png" alt="New Dashboard" /> |

5. For each widget, update:
   * **Data Source**
   * **Metric value** (the AnyLog table name)

   | View when accessing Dashboard | Update Data Source | Update Metric Value | Outcome |
   |:---:|:---:|:---:|:---:|
   | <img src="../../imgs/grafana_edit_button.png" alt="Edit Widget" /> | <img src="../../imgs/grafana_update_datasource.png" alt="Update Data Source" /> | <img src="../../imgs/grafana_update_table.png" alt="Update Metric Value" /> | <img src="../../imgs/grafana_outcome.png" alt="Outcome" /> |

> **Note:** the sample `edgex_dashboard.json` bundled with this doc set had two panels ("Total Rows - Server 1/2")
> with real, non-placeholder IPs hardcoded into their query payloads. Anonymized before publishing — if you're
> pulling a fresh copy of this dashboard from elsewhere, check the `servers` field in those two panels before
> sharing it further.

---

## Exporting a dashboard

To share a dashboard you've built (or to save a copy of a customized sample dashboard):

1. Open the dashboard, then go to its **Settings** (gear icon).
2. Go to **JSON Model**.
3. Either:
   * **Copy** the JSON directly from the editor, or
   * Use **Export → Save to file** (Grafana 9+) to download it as a `.json` file.

The exported file is the same format used for import above — it can be handed to someone else, checked into a
repo as a versioned example (like `network_summary.json` / `edgex_dashboard.json`), or re-imported later via
**JSON Model** on a fresh dashboard.

> Before sharing an exported dashboard outside your team, check it for anything environment-specific — data
> source UIDs, hardcoded `servers` IPs in query payloads (see the note above), or table/database names — the
> same way you'd review any other exported config before publishing it.

---

## Tips

- Set **Max data points** in Query Options to control result density for time-series panels — without it, min/max/avg lines collapse into a single line.
- Use `format_as: timeseries` for time-series panels (Time series, Gauge) and `table` for table panels.
- See [Querying Data](../07-%20CLI/04-%20SQL.md) for the full `increments`/`period` reference and query options like `include`/`extend`.
--->
