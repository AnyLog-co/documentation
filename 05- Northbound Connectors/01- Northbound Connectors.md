---
title: A- Northbound Connectors
description: Connect BI tools, dashboards, and applications to AnyLog for querying distributed edge data.
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name** | **Change**       | **Version** |
 |------------|--|------------------|----------|
 | 2026-04-17 |  | created document |  |
 | 2026-04-25 |  | hyperlinks       |  |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-25 | Ori Shadmon | Rewritten as a summary/index page rather than a second, shorter copy of each
   connector's content — this page previously described PostgreSQL, Google Drive, Grafana, and PowerBI mechanics
   in ways that didn't match their own dedicated docs (some flatly contradicted them — see each doc's changelog
   for the corrected version). Kept one worked cURL example as the generic REST pattern every connector builds on,
   and replaced each connector's inline walkthrough with a one-line summary + link to its dedicated doc. Fixed the
   broken Edge Data Manager link (unescaped parentheses in the path) and the invalid bash/JSON in the REST examples
   (`{-H "..."}` isn't valid optional-header syntax; `["destination": "network"]` isn't valid JSON). |
--->

AnyLog exposes query and data access through a REST API, enabling standard BI tools, dashboards, and applications to query 
distributed edge data as if it were a single database.

All northbound connectors communicate with a **Query Node** over REST. The Query Node resolves which Operator nodes hold 
the relevant data, distributes the SQL query, and returns aggregated results.

---

## Generic REST API

Any application can query AnyLog directly via HTTP GET or POST — this is the pattern every connector below is built on.

**GET:**

```bash
curl -X GET 'http://[ip]:[port]' \
  -H 'command: sql my_data format=json "select * from ping_sensor limit 10"' \
  -H 'User-Agent: AnyLog/1.23' \
  -H 'destination: network'
```

**Equivalent POST:**

```bash
curl -X POST 'http://[ip]:[port]' \
  -H 'Content-Type: application/json' \
  -d '{
    "command": "sql my_data format=json \"select * from ping_sensor limit 10\"",
    "AnyLog-Agent": "AnyLog/1.23",
    "destination": "network"
  }'
```

`destination: network` scans the whole network for matching data — the REST equivalent of `run client ()` with
empty parentheses. If `destination` is omitted, the request runs only against the local node. (Noting this as my
best understanding of the default — worth a quick confirm if you're relying on the omitted-header behavior
specifically.)

See <a href="{{ '/docs/Querying-Data-Northbound/using-rest/' | relative_url }}">Using REST</a> for the full REST API
reference.

---

## Connectors

| Tool | What it's for | Doc                                                                                           |
|---|---|-----------------------------------------------------------------------------------------------|
| **Postman** | Testing AnyLog REST endpoints during development, with or without SSL | <a href="02-%20Postman%20Integration.md" target="_blank">Postman Integration</a>                                         |
| **Grafana** | Dashboards over live/historical AnyLog data — increments, period, aggregations, and blockchain metadata visualizations | <a href="03-%20Grafana.md" target="_blank">Using Grafana</a>                                                             |
| **PostgreSQL / Tableau** | For tools that only support a PostgreSQL connector (not REST) — routes results through `system_query` into a real Postgres instance | <a href="04-%20Postgres%20Connector%20%28Tableau%29.md" target="_blank">PostgreSQL Connector & Tableau Visualization</a> |
| **PowerBI / Excel** | Pull AnyLog data into PowerBI or Excel via the Web connector and PowerQuery | <a href="05-%20Microsoft%20%28PowerBI%29.md" target="_blank">AnyLog with PowerBI + Microsoft Office Suite</a>            |
| **Google Drive / Sheets** | Pull AnyLog query results into Sheets via the third-party Two Minute Reports add-on | <a href="06-%20Google.md" target="_blank">Google Drive</a>                                                               |
| **Qlik** | Qlik Sense's REST connector plugin, with worked increments/period examples | <a href="07-%20Qlik.md" target="_blank">Qlik</a>                                                                         |
| **Edge Data Manager** | AnyLog's own management/monitoring UI | <a href="../10-%20Edge%20Data%20Manager/01-%20EDM.md" target="_blank">Edge Data Manager</a>                                                                    |                                                                          |

**Sending data the other way:** the connectors above all *pull* data from AnyLog. To *push* data or a message out —
a SQL result over REST, or a one-off MQTT message — see <a href="08-%20Data%20Forwarding.md" target="_blank">Forwarding Data</a>.