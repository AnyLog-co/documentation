# AnyLog Dashboard Generation Guide

## Overview

This guide explains how to ask an LLM (Claude) to generate an HTML dashboard that queries data from an AnyLog node. Four connection modes are supported:

| Mode | Description | Use When |
|------|-------------|----------|
| **Direct HTTP** | Command embedded in the URL, called directly from the browser | Node is accessible over HTTP on the local network |
| **Direct POST** | AnyLog headers and command delivered as JSON in the POST body, called directly from the browser | Node is accessible over HTTP and POST is preferred over URL embedding |
| **POST to Flask Proxy** | Browser POSTs to a local Flask proxy which forwards to AnyLog using mTLS | Node requires mTLS certificates or HTTPS |
| **CLI** | Returns the native AnyLog command string for manual testing | Verifying a query before building a dashboard |

---

## How to Ask for a Dashboard

### Minimum Required Information

Every dashboard request must include all of the following:

| Information | Why It's Needed | Example |
|-------------|----------------|---------|
| **Connection type** | Determines how the dashboard calls AnyLog | `direct HTTP`, `direct POST`, or `Flask proxy` |
| **Node address** | The IP and port of the AnyLog node | `24.5.219.50:7849` |
| **Database name** | The AnyLog database (dbms) to query | `agg_anotherpeak` |
| **Table name** | The table to query | `battery_pack_logs_gcurrent` |
| **What data to show** | The SQL query intent | `last 10 rows` |
| **Response format** | Tells the LLM how to parse the response | `json:list` |
| **Editable node** | Whether the user can change the node at runtime | `yes / no` |

### Prompt Template

```
Create an HTML dashboard that uses <connection type> against AnyLog node <IP>:<PORT>
to show <query description> from dbms <database> and table <table>.
The AnyLog response is in json:list format — an array of JSON objects.
Allow the user to change the node address in the dashboard.
```

---

## Recommended Workflow — Test Before You Build

Before building a dashboard, verify the query works by testing it step by step.

### Step 1 — Test on the AnyLog CLI

Ask the LLM for the native CLI command and paste it directly into the AnyLog CLI:

```
Show me the AnyLog CLI command to query the last 10 rows from dbms agg_anotherpeak
and table battery_pack_logs_gcurrent.
```

Returns:
```
sql agg_anotherpeak format = json:list and stat = false SELECT * FROM battery_pack_logs_gcurrent ORDER BY timestamp DESC LIMIT 10
```

Other CLI examples:

| What to say | CLI command returned |
|-------------|---------------------|
| `"Show me the CLI command to get node status"` | `get status where format = mcp` |
| `"Show me the CLI command to list all tables in dbms agg_anotherpeak"` | `blockchain get (table) where dbms = agg_anotherpeak bring.json.unique [*][name]` |
| `"Show me the CLI command to count rows in battery_pack_logs_gcurrent"` | `sql agg_anotherpeak format = json:list and stat = false SELECT COUNT(*) FROM battery_pack_logs_gcurrent` |

### Step 2 — Verify via HTTP in the browser

Ask the LLM for the HTTP URL and paste it into a browser address bar to confirm the response:

```
Show me the HTTP URL to query the last 10 rows from dbms agg_anotherpeak
and table battery_pack_logs_gcurrent against node 24.5.219.50:7849.
```

### Step 3 — Build the dashboard

Once the query is confirmed to return the right data, ask for the dashboard using one of the connection types below.

---

## Connection Types

### 1. Direct HTTP

The browser calls the AnyLog node directly. The AnyLog headers and command are embedded in the URL as query parameters.

- Say: **"use a direct HTTP call"**

**URL format:**
```
http://<IP>:<PORT>/?User-Agent=AnyLog/1.23?destination=network?command=<command>
```

**JavaScript `fetch` call:**
```javascript
const cmd  = `sql agg_anotherpeak format = json:list and stat = false SELECT * FROM battery_pack_logs_gcurrent ORDER BY timestamp DESC LIMIT 10`;
const url  = `http://24.5.219.50:7849/?User-Agent=AnyLog/1.23?destination=network?command=${encodeURIComponent(cmd)}`;

const res  = await fetch(url);
const text = await res.text();
const rows = JSON.parse('[' + text.trim().replace(/,\s*$/, '') + ']');
```

**Example prompt:**
```
Create an HTML dashboard using a direct HTTP call to AnyLog node 24.5.219.50:7849.
Show the last 10 rows from dbms agg_anotherpeak and table battery_pack_logs_gcurrent.
The response is in json:list format.
Allow the user to change the node address.
```

---

### 2. Direct POST to AnyLog

The browser sends a `POST` request directly to the AnyLog node. The AnyLog headers and command are delivered as a JSON object in the message body. No proxy is needed.

- Say: **"use a direct POST to AnyLog"**

**POST body format:**
```json
{
  "User-Agent":  "AnyLog/1.23",
  "destination": "network",
  "command":     "sql agg_anotherpeak format = json:list and stat = false SELECT * FROM battery_pack_logs_gcurrent ORDER BY timestamp DESC LIMIT 10"
}
```

**JavaScript `fetch` call:**
```javascript
const res  = await fetch("http://24.5.219.50:7849", {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify({
        "User-Agent":  "AnyLog/1.23",
        "destination": "network",
        "command":     "sql agg_anotherpeak format = json:list and stat = false SELECT * FROM battery_pack_logs_gcurrent ORDER BY timestamp DESC LIMIT 10"
    })
});

const text = await res.text();
const rows = JSON.parse('[' + text.trim().replace(/,\s*$/, '') + ']');
```

> **Important:** The node URL must include the scheme — `http://` or `https://`. A bare `IP:PORT` without a scheme will cause an `InvalidSchema` error.

**Example prompt:**
```
Create an HTML dashboard using a direct POST to AnyLog node 24.5.219.50:7849.
Show the last 10 rows from dbms agg_anotherpeak and table battery_pack_logs_gcurrent.
The response is in json:list format.
Allow the user to change the node address.
```

---

### 3. POST to Flask Proxy (`anylog_proxy.py`)

The browser POSTs to a local **Flask proxy** (`anylog_proxy.py`), which holds the mTLS certificates and forwards the request to the AnyLog node over HTTPS. The proxy is not generated by the LLM — it must already be running before the dashboard is opened.

- Say: **"use the AnyLog Flask proxy"**

#### Starting the proxy

```bash
pip install flask flask-cors requests

python anylog_proxy.py \
    --cert   /path/to/server-acme-inc-public-key.crt \
    --key    /path/to/server-acme-inc-private-key.key \
    --cacert /path/to/ca-anylog-public-key.crt \
    --port   5000
```

The proxy runs at `http://localhost:5000` by default.

#### How the proxy works

The proxy exposes a single endpoint — `POST /api/query` — that:
- Accepts a JSON body containing the node URL and the full AnyLog headers and command
- Forwards the request to the AnyLog node using the mTLS certificates
- Returns the parsed JSON response to the dashboard

#### POST body sent from the dashboard to the proxy

```json
{
  "url":         "https://24.5.219.50:7849",
  "User-Agent":  "AnyLog/1.23",
  "destination": "network",
  "command":     "sql agg_anotherpeak format = json:list and stat = false SELECT * FROM battery_pack_logs_gcurrent ORDER BY timestamp DESC LIMIT 10"
}
```

> **Important:** The `url` field must include the scheme — `http://` or `https://`. A bare `IP:PORT` without a scheme will cause an `InvalidSchema` error in the proxy.

#### JavaScript `fetch` call:

```javascript
const PROXY   = 'http://localhost:5000';
const NODE    = 'https://24.5.219.50:7849';  // must include https://
const command = 'sql agg_anotherpeak format = json:list and stat = false SELECT * FROM battery_pack_logs_gcurrent ORDER BY timestamp DESC LIMIT 10';

const res  = await fetch(`${PROXY}/api/query`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({
        url:           NODE,
        "User-Agent":  "AnyLog/1.23",
        destination:   "network",
        command:       command
    })
});

const data = await res.json();
const rows = Array.isArray(data) ? data : (data.raw ? [] : [data]);
```

> **Note:** The proxy parses the AnyLog response and returns it as JSON — the dashboard does not need to handle raw text parsing.

#### Proxy health check

```
GET http://localhost:5000/api/health
```

```json
{
  "status": "ok",
  "cert":   "/path/to/cert.crt",
  "key":    "/path/to/key.key",
  "cacert": "/path/to/ca.crt"
}
```

#### Example prompt

```
Create an HTML dashboard using the AnyLog Flask proxy at http://localhost:5000.
The AnyLog node is at https://24.5.219.50:7849.
Show the last 10 rows from dbms agg_anotherpeak and table battery_pack_logs_gcurrent.
The response is in json:list format.
Allow the user to change both the proxy address and the node address.
```

---

### 4. CLI Only

Returns the native AnyLog command string for manual execution on the node CLI. Used for testing before building a dashboard — see the Recommended Workflow section above.

- Say: **"show me the AnyLog CLI command"**

---

## AnyLog Response Format

AnyLog SQL queries using `format = json:list` return rows as JSON objects separated by commas and newlines, wrapped in `[ ]`:

```json
 [{"row_id": 11, "timestamp": "2026-03-11 21:27:41", "avg_val": -0.125, "events": 8},
{"row_id": 10, "timestamp": "2026-03-11 21:26:32", "avg_val": -0.125, "events": 8},
{"row_id": 9,  "timestamp": "2026-03-11 21:25:24", "avg_val": -0.125, "events": 8}]
```

**Direct HTTP and Direct POST dashboards** must read the response as text and parse manually:
```javascript
const text = await res.text();
const rows = JSON.parse('[' + text.trim().replace(/,\s*$/, '') + ']');
```

**Flask proxy dashboards** receive already-parsed JSON from the proxy — no manual text parsing needed.

Always include `"json:list format"` in your prompt so the LLM generates the correct parsing logic.

---

## Optional Dashboard Features

| Feature | What to say |
|---------|-------------|
| Editable node address | `"allow the user to change the node address"` |
| Editable proxy address | `"allow the user to change the proxy address"` |
| Auto-refresh | `"auto-refresh every 30 seconds"` |
| Debug panel | `"include a debug panel showing the request sent, the raw response, and any errors"` |
| Summary statistics | `"show summary statistics above the table"` |
| Specific columns only | `"show only the timestamp, avg_val and events columns"` |
| Time filter | `"show data from the last 24 hours"` |
| Multiple tables | `"show data from table A and table B side by side"` |

---

## Common Mistakes and How to Avoid Them

### Query returns wrong data or no data

**Cause:** The SQL query or dbms/table names are wrong.

**Fix:** Always test with the CLI command first. Ask `"Show me the AnyLog CLI command for <your query>"`, run it on the CLI, and confirm data is returned before asking for the dashboard.

---

### Direct HTTP or POST dashboard fails to parse the response

**Cause:** The LLM used `res.json()` directly, which fails because AnyLog's `json:list` response has leading whitespace or non-standard formatting.

**Fix:** Always mention `"json:list format"` in the prompt so the LLM reads the response as text first and wraps it in `[ ]` before parsing.

---

### Node address is hardcoded and cannot be changed

**Cause:** The LLM hardcoded the node address without making it editable.

**Fix:** Always include `"allow the user to change the node address"` in your prompt.

---

### Flask proxy returns 405 Method Not Allowed

**Cause:** The dashboard is POSTing to the wrong URL on the proxy — e.g. `POST /` instead of `POST /api/query`. The proxy root `/` only handles `GET` requests (it serves the dashboard HTML page).

**Fix:** Specify `"use the AnyLog Flask proxy"` in your prompt. The proxy endpoint is always `POST /api/query`. Verify the dashboard is calling the correct endpoint with the full body:
```json
{
  "url":         "https://<node>",
  "User-Agent":  "AnyLog/1.23",
  "destination": "network",
  "command":     "<anylog command>"
}
```

---

### Flask proxy returns `InvalidSchema` error

**Cause:** The `url` field in the POST body is missing the scheme — e.g. `24.5.219.50:7849` instead of `https://24.5.219.50:7849`. The Python `requests` library requires a full URL with `http://` or `https://`.

**Fix:** Always include the scheme in the node URL. The dashboard should ensure it before sending:
```javascript
const nodeURL = node.startsWith('http') ? node : `https://${node}`;
```

The same applies to the Direct POST mode — the `fetch` URL must also include `http://` or `https://`.

---

### Dashboard shows an error but it's unclear why

**Cause:** No visibility into what was sent or received.

**Fix:** Add `"include a debug panel"` to your prompt. The debug panel shows the exact URL or POST body sent, the raw response received, the parse result, and the full error message — making it straightforward to identify the failure point.

---

## Full Example Prompts

### Step 1 — Test on CLI
```
Show me the AnyLog CLI command to query the last 10 rows from dbms agg_anotherpeak
and table battery_pack_logs_gcurrent.
```

### Step 2 — Verify in browser
```
Show me the HTTP URL to query the last 10 rows from dbms agg_anotherpeak
and table battery_pack_logs_gcurrent against node 24.5.219.50:7849.
```

### Step 3a — Direct HTTP dashboard
```
Create an HTML dashboard using a direct HTTP call to AnyLog node 24.5.219.50:7849.
Show the last 10 rows from dbms agg_anotherpeak and table battery_pack_logs_gcurrent.
The response is in json:list format.
Allow the user to change the node address.
Include a debug panel showing the URL sent, the raw response, and any errors.
```

### Step 3b — Direct POST dashboard
```
Create an HTML dashboard using a direct POST to AnyLog node 24.5.219.50:7849.
Show the last 10 rows from dbms agg_anotherpeak and table battery_pack_logs_gcurrent.
The response is in json:list format.
Allow the user to change the node address.
Include a debug panel showing the POST body sent, the raw response, and any errors.
```

### Step 3c — Flask proxy dashboard
```
Create an HTML dashboard using the AnyLog Flask proxy at http://localhost:5000.
The AnyLog node is at https://24.5.219.50:7849.
Show the last 10 rows from dbms agg_anotherpeak and table battery_pack_logs_gcurrent.
The response is in json:list format.
Allow the user to change both the proxy address and the node address.
Include a debug panel showing the POST body sent to the proxy, the raw response, and any errors.
```

---

## Quick Reference Card

```
✅ Recommended workflow:
   1. Ask for the CLI command → test on AnyLog CLI
   2. Ask for the HTTP URL   → verify in a browser
   3. Ask for the dashboard  → build with confidence

✅ Always specify in the prompt:
   - Connection type:  "direct HTTP", "direct POST", or "Flask proxy"
   - Node address:     IP:PORT  (e.g. 24.5.219.50:7849)
   - Database:         dbms name
   - Table:            table name
   - Query:            what data to show
   - Format:           "json:list format"
   - Editable node:    "allow the user to change the node address"

✅ For Flask proxy, also specify:
   - Proxy address:    e.g. http://localhost:5000
   - "allow the user to change the proxy address"

✅ Node URL scheme rules (applies to all POST modes):
   - The node URL must always include http:// or https://
   - A bare IP:PORT without a scheme causes an InvalidSchema error
   - Dashboard: const nodeURL = node.startsWith('http') ? node : `https://${node}`;

✅ POST body — Direct POST to AnyLog:
   {
     "User-Agent":  "AnyLog/1.23",
     "destination": "network",
     "command":     "<anylog command>"
   }

✅ POST body — Flask proxy (POST /api/query):
   {
     "url":         "https://<node>",   ← must include http:// or https://
     "User-Agent":  "AnyLog/1.23",
     "destination": "network",
     "command":     "<anylog command>"
   }

✅ Proxy health check: GET http://localhost:5000/api/health

✅ Recommended additions:
   - "include a debug panel" — makes failures easy to diagnose
   - "auto-refresh every N seconds" — for live data monitoring
```