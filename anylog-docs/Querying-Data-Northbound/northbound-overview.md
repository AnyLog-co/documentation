---
title: Northbound Connectors
description: Connect BI tools, dashboards, and applications to AnyLog for querying distributed edge data.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlinks 
--> 

AnyLog exposes query and data access through a REST API, enabling standard BI tools, dashboards, and applications to query distributed edge data as if it were a single database.

All northbound connectors communicate with a **Query Node** over REST. The Query Node resolves which Operator nodes hold the relevant data, distributes the SQL query, and returns aggregated results.

---

## Prerequisites

- A Query node with REST service running:
  ```anylog
  run rest server where external_ip = !ip and external_port = !anylog_rest_port and timeout = 20
  ```
- The REST endpoint: `http://[node-ip]:[rest-port]`
- For authenticated access: a valid user/password or API key

---

## REST API (generic connector)

Any application can query AnyLog directly via HTTP GET or POST:

### GET — retrieve status or data

```bash
curl -X GET http://[ip]:[port] \
  -H "command: sql my_data format=json \"select * from ping_sensor limit 10\"" \
  -H "User-Agent: AnyLog/1.23"
```

### POST — issue any AnyLog command

```bash
curl -X POST http://[ip]:[port] \
  -H "Content-Type: application/json" \
  -d '{"command": "sql my_data format=json \"select * from ping_sensor limit 10\""}'
```

See <a href="{{ '/docs/Querying-Data-Northbound/using-rest/' | relative_url }}">Using REST</a> for the full REST API 
reference.

---

## Grafana

Grafana connects to AnyLog via the **JSON API** data source plugin. Once configured, you can build dashboards that query live and historical data from edge nodes.

Key configuration:
- **URL**: `http://[node-ip]:[rest-port]`
- **Plugin**: JSON API (or SimpleJSON)
- **Query**: AnyLog SQL passed as the metric/query body

See <a href="{{ '/docs/Querying-Data-Northbound/grafana' | relative_url }}">Grafana Integration</a> for step-by-step 
setup and dashboard examples.

---

## PowerBI

PowerBI connects to AnyLog through the **Web connector** using REST GET requests. Data is pulled as JSON and transformed using PowerQuery.

Setup steps:
1. In PowerBI Desktop: **Get Data → Web**
2. Enter the AnyLog REST URL with the SQL command as a header
3. Parse the returned JSON into a table
4. Schedule refresh as needed

Example REST URL (for HTTP mode):
```
http://[ip]:[port]?User-Agent=AnyLog/1.23&command=sql+my_data+format%3Djson+"select+*+from+ping_sensor+limit+100"
```

---

## Qlik

Qlik Sense and Qlik View connect to AnyLog via the **REST connector**:

1. Add a new **REST data connection** in Qlik
2. Set the base URL to `http://[node-ip]:[rest-port]`
3. Configure headers: `command: sql my_data format=json "select ..."`
4. Map the JSON response fields to Qlik dimensions and measures

Use `increments()` queries to build time-series line charts:
```sql
SELECT increments(minute, 5, timestamp), MIN(timestamp), AVG(value)
FROM ping_sensor
WHERE timestamp >= NOW() - 1 hour
```

---

## Postman

Postman is useful for testing AnyLog REST endpoints during development.

### GET request
- Method: `GET`
- URL: `http://[ip]:[port]`
- Headers:
  - `command`: `get status`
  - `User-Agent`: `AnyLog/1.23`

### POST request
- Method: `POST`
- URL: `http://[ip]:[port]`
- Body (JSON):
  ```json
  {"command": "sql my_data format=json \"select * from ping_sensor limit 10\""}
  ```

### SQL query via GET
```
Header: command: sql my_data format=json "select timestamp, value from ping_sensor where timestamp >= NOW() - 1 hour"
```

---

## PostgreSQL connector (pass-through)

AnyLog can act as a PostgreSQL-compatible endpoint using the `psycopg2` or standard PostgreSQL driver:

- Connect to the AnyLog node using the standard Postgres protocol on the configured port
- Issue SQL queries as normal
- AnyLog routes the query to the relevant Operator nodes and returns results

This allows tools that only support PostgreSQL (like Tableau or some BI platforms) to query AnyLog without any custom integration.

---

## Google Drive connector

AnyLog can export query results directly to Google Sheets or Google Drive for sharing and reporting:

1. Configure Google Drive credentials on the node
2. Use a scheduled task to run a query and push results:
   ```anylog
   schedule time = 1 hour and name = "Export to Drive" task ...
   ```

See the <a href="{{ '/docs/Querying-Data-Northbound/Google/' | relative_url }}">Google Drive connector documentation</a> for OAuth setup and examples.

---

## Notifications (Slack, webhook)

AnyLog can push alerts and query results to external systems via webhooks or Slack:

### Slack
```anylog
slack to [webhook-url] where message = "Alert: value exceeded threshold"
```

### Generic webhook (HTTP POST)
```anylog
http post where url = [webhook-url] and message = [json-payload]
```

Notifications are typically triggered from:
- **Streaming conditions** — fire when incoming data meets a threshold
- **Scheduled tasks** — run on a schedule and push results

See <a href="{{ '/docs/Monitoring-Operations/monitoring/#streaming-conditions-real-time-alerts' | relative_url }}">Monitoring & Alerts — streaming conditions</a> for configuration.

---

## Remote CLI

The Remote CLI is a browser-based interface for issuing AnyLog commands and queries without a local terminal. It connects to any node over REST.

See <a href="{{ '/docs/Tools-UI/remote-gui/' | relative_url }}">Remote CLI</a> for setup and usage.

---

## MCP (AI / LLM integration)

The MCP server exposes AnyLog to AI assistants and LLM-based tools via the Model Context Protocol. Once enabled, tools like Claude can query your edge network in natural language.

See <a href="{{ '/docs/Tools-UI/mcp/' | relative_url }}">MCP</a> for configuration.

---

## Query reference

All northbound connectors ultimately issue SQL queries through AnyLog. See <a href="{{ '/docs/Querying-Data-Northbound/queries/' | relative_url }}">Queries</a> for the full SQL reference including:

- Network-distributed queries (`run client ()`)
- Time filters (`NOW() - N hours`)
- `INCREMENTS()` for time-series charting
- Output formats (`format = json`, `format = table`)
- Query profiling and monitoring