---
title: MCP & AI Integration
description: Connect Claude and other LLM clients to AnyLog via the Model Context Protocol for live data queries, dashboard generation, and AI-driven edge analytics.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-23 | updates based on changes in MCP-Examples related to CORs + AnyLog-Agent 
--> 

Every AnyLog query node exposes a **Model Context Protocol (MCP) server** that gives any compatible AI client — Claude Desktop, Claude.ai, Base44 — live access to your network's schema, data, and node topology. No SQL required on your end.

> **Prerequisite:** The query node must have `SYSTEM_QUERY=true` and `ENABLE_MCP=true` set in `node_configs.env`, and the 
> REST service must be running. See <a href="{{ '/docs/deployment-scripts//#southbound--data-ingestion-all-off-by-default' | relative_url }}">Deployment Scripts</a>.

---

## MCP endpoint

Every query node exposes SSE at:

```
http://[HOST]:[REST_PORT]/mcp/sse
```

> ⚠️ Always include the `/mcp/sse` suffix. Connecting to the bare node URL (`http://HOST:PORT`) will appear to succeed but all tool calls will fail silently.

---

## Three ways to use MCP

| Mode | What you get |
|---|---|
| **Dashboard generation** | Claude connects once via MCP to discover schema and topology, then generates a standalone `.html` dashboard wired to the correct tables and queries |
| **Conversational queries** | Keep Claude Desktop connected — ask natural-language questions about live data at any time (no extra setup beyond mode 1) |
| **MCP-backed live dashboards** | A running dashboard that routes every data fetch through the MCP proxy at runtime (experimental) |

---

## Supported MCP clients

| Client | Status |
|---|---|
| Claude Desktop | ✅ |
| Claude.ai (web) | ✅ |
| Base44 | ✅ |
| Cursor | 🔜 Planned |
| Continue.dev | 🔜 Planned |

---

## Setup — Claude Desktop

### 1. Install prerequisites

Install [Claude Desktop](https://claude.ai/download), then install `mcp-proxy` (bridges Claude's stdio MCP to the AnyLog SSE endpoint):

```bash
pip install --upgrade mcp-proxy
```

Find where `mcp-proxy` was installed:

```bash
# macOS / Linux
which mcp-proxy

# Windows (PowerShell)
(Get-Command mcp-proxy).Source
```

| Platform | Typical path |
|---|---|
| macOS | `/usr/local/bin/mcp-proxy` |
| Linux | `/usr/local/bin/mcp-proxy` |
| Windows | `C:\Users\USERNAME\AppData\Local\Programs\Python\Python311\Scripts\mcp-proxy.exe` |

### 2. Edit the Claude Desktop config

Open the config file for your platform:

| Platform | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

Add an entry under `mcpServers`:

```json
{
  "mcpServers": {
    "anylog": {
      "command": "/usr/local/bin/mcp-proxy",
      "args":    ["http://HOST:PORT/mcp/sse"],
      "env":     {},
      "timeout": 30000
    }
  }
}
```

**Windows example:**
```json
{
  "mcpServers": {
    "anylog": {
      "command": "C:\\Users\\you\\AppData\\Local\\Programs\\Python\\Python311\\Scripts\\mcp-proxy.exe",
      "args":    ["http://66.175.217.145:32349/mcp/sse"],
      "env":     {},
      "timeout": 30000
    }
  }
}
```

### 3. Restart Claude Desktop

Quit and reopen. The AnyLog tools will appear in the tool selector (🔨 icon).

### 4. Test the connection

In a new conversation:
```
What databases are available on this AnyLog network?
```

Claude calls `listNetworkDatabases` and returns a live list from your network.

### Connecting multiple nodes

Add one entry per node — each gets its own key:

```json
{
  "mcpServers": {
    "anylog-wind-farm": {
      "command": "/usr/local/bin/mcp-proxy",
      "args":    ["http://66.175.217.145:32349/mcp/sse"],
      "timeout": 30000
    },
    "anylog-power-plant": {
      "command": "/usr/local/bin/mcp-proxy",
      "args":    ["http://24.5.219.50:32349/mcp/sse"],
      "timeout": 30000
    }
  }
}
```

---

## Generating dashboards with Claude + MCP

The MCP connection lets Claude discover your live schema, sample data, and node topology. It then generates a single self-contained `.html` dashboard wired to the correct tables and queries — drop it into a browser and it works immediately.

### Quick start

1. Connect Claude Desktop to AnyLog MCP (steps above)
2. Pick a prompt template from [AnyLog-co/MCP-Examples/prompts/](https://github.com/AnyLog-co/MCP-Examples/tree/main/prompts)
3. Fill in the parameters at the top:
   ```
   DATA_TYPE      = "Wind Turbine"
   QUERY_NODE     = "10.0.0.1:32349"
   DBMS           = "wind_turbine"
   TABLE          = "wind_turbine"
   UNS_NAMESPACE  = "MyOrg"
   ```
4. Paste into Claude — it discovers the schema via MCP, then generates the `.html` file
5. Open the file in a browser

### Available prompt templates

| Template | Dashboard type |
|---|---|
| `power_plant.md` | SQL queries, UNS panel, charts, drill-down |
| `node_status.md` | Node health — no SQL, diagnostic commands only |
| `rig_data.md` | Multi-rig industrial monitor with `increments()` queries |
| `wind_turbine_mcp.md` | MCP-backed live dashboard — every fetch routed through the MCP proxy at runtime (experimental) |
| `base44.md` | Hosted Base44 app — generates backend + frontend prompts |

---

## MCP-backed live dashboards (experimental)

Unlike generated dashboards that run over plain REST, an MCP-backed dashboard routes **every data fetch** through the MCP proxy at runtime:

```
Browser → POST /api/query → anylog_proxy.py (MCP mode) → MCP/SSE → AnyLog
```

This requires the Flask proxy running in MCP mode — nginx alone cannot support this.

**Costs and constraints to be aware of:**

| Concern | Detail |
|---|---|
| **Cost** | Every dashboard refresh triggers LLM-mediated MCP calls — billable on every poll cycle |
| **Latency** | MCP calls are serialized; polling frequently across many sensors will queue |
| **Proxy required** | Requires `anylog_proxy.py` in MCP mode |
| **Query discipline** | All SQL must be bounded (`LIMIT`, narrow time windows) — never `SELECT *` |

**When it makes sense:** prototyping or demos, low-frequency dashboards (refresh ≥ 5 min), or when the MCP endpoint is the only available access path. The `wind_turbine_mcp.html` dashboard includes a built-in query log, error log with `curl` reproduction, and prompt evolution log.

→ See `html/wind_turbine_mcp.html` for a working example  
→ Use `prompts/wind_turbine_mcp.md` to generate your own

---

## Ready-made dashboards

The [MCP-Examples repo](https://github.com/AnyLog-co/MCP-Examples) ships three production-ready dashboards in `html/`:

| File | Description |
|---|---|
| `dashboard-node-status.html` | Node and network health — `get status`, `test node`, `test network` |
| `dashboard-power-plant.html` | Smart City Power Plant live monitor — KPI cards, phase breakdown, trend charts, UNS panel |
| `rig_data.html` | Timbergrove oil rig fleet — SVG rig diagram, per-sensor KPIs, time-series charts |

All dashboards support three connection modes selectable from an in-page config bar.

---

## Browser connection modes

Browsers cannot POST directly to AnyLog nodes in most environments due to CORS. The root cause is that browsers treat `User-Agent` as a reserved header — any attempt to set it via `fetch()` is silently ignored, and cross-origin requests can trigger a CORS preflight (`OPTIONS`) that AnyLog nodes are not configured to answer by default.

**`AnyLog-Agent` is the solution for direct browser calls.** It is a custom header that both the browser and the node control explicitly, allowing the node to whitelist it without triggering preflight. Use it as a body key in POST requests from the browser:

```json
{ "AnyLog-Agent": "AnyLog/1.23", "command": "...", "destination": "network" }
```

For environments where the node cannot be configured to return CORS headers at all, route through a proxy instead:

| Mode | How it works | Best for |
|---|---|---|
| **Direct** | Browser → AnyLog node directly | Node has CORS enabled, or dev/local testing |
| **nginx proxy** | Browser → nginx (Docker) → AnyLog node | Production, shared access, no Python needed |
| **Flask proxy** | Browser → `anylog_proxy.py` → AnyLog node | REST or MCP mode, more control |

### nginx proxy (recommended for production)

```bash
git clone https://github.com/AnyLog-co/MCP-Examples
cd MCP-Examples/proxy-nginx
```

Edit `docker-compose.yaml` — set your AnyLog node URL:
```yaml
environment:
  - ANYLOG_NODE_URL=http://HOST:PORT/
```

Start:
```bash
docker compose up -d --build
```

Open any dashboard at `http://localhost/<filename>.html`, set **Mode → nginx**, **nginx URL → `http://localhost`**.

**If AnyLog is on the same Windows machine**, use `host.docker.internal` instead of `localhost`:
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
environment:
  - ANYLOG_NODE_URL=http://host.docker.internal:PORT/
```

Adding a new dashboard: drop a `.html` file into `html/` — no nginx restart needed, the directory is bind-mounted.

### Flask proxy

```bash
cd MCP-Examples/proxy-generic

# REST mode
python3 anylog_proxy.py --anylog-url http://HOST:PORT --html-dir ../html

# MCP mode (routes through the MCP server)
python3 anylog_proxy.py --anylog-url http://HOST:PORT/mcp/sse --html-dir ../html

# Or via Docker
docker compose up -d
```

Open a dashboard, set **Mode → proxy**, **Proxy URL → `http://localhost:8080`**.

---

## AnyLog REST API (for dashboard developers)

All requests use `POST` with a JSON body.

### SQL queries — always include `destination: "network"`

```bash
curl -X POST http://HOST:PORT \
  -H "Content-Type: application/json" \
  -d '{
    "AnyLog-Agent": "AnyLog/1.23",
    "command":      "sql mydb format=json:list and stat=false SELECT * FROM mytable LIMIT 10",
    "destination":  "network"
  }'
```

- `destination: "network"` fans the query out to all operator nodes
- `format=json:list and stat=false` returns a plain JSON array — no trailing stats object

### Node / blockchain commands — no `destination`

```bash
curl -X POST http://HOST:PORT \
  -H "Content-Type: application/json" \
  -d '{
    "AnyLog-Agent": "AnyLog/1.23",
    "command":      "get status where format=json"
  }'
```

Examples: `get status where format=json`, `test node`, `test network`, `blockchain get uns where namespace = Smart_City`

### Via Flask proxy

```bash
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"dbms": "mydb", "sql": "SELECT * FROM mytable LIMIT 10"}'
```

Response: `{"results": [...], "row_count": N, "dbms": "mydb"}`

---

## Base44 integration

[Base44](https://base44.com) is an AI-native app builder. Instead of a static HTML file, Base44 produces a hosted application. The workflow is two phases:

```
Phase 1 — Claude + AnyLog MCP          Phase 2 — Claude (no MCP)
  Discover schema, UNS, topology    →     Given backend API from phase 1
  Generate: backend prompt               Generate: frontend prompt
         ↓                                        ↓
  Paste into Base44                       Paste into Base44
  (creates AnyLog REST backend)           (creates UI calling backend)
```

The Base44 backend calls AnyLog directly over REST (no proxy needed — Base44 runs server-side, so CORS is not an issue). Use `AnyLog-Agent` in the HTTP header and `format=json:list and stat=false`, then parse with:

```js
const rows = Array.isArray(response) ? response : [];
```

**SQL queries** — require `destination: "network"`:
```json
POST http://{node_ip}:{port}
Headers: { "AnyLog-Agent": "AnyLog/1.23", "Content-Type": "application/json" }
Body: {
  "command":     "sql {dbms} format=json:list and stat=false {SQL}",
  "destination": "network"
}
```

**Blockchain / node commands** — no `destination`:
```json
POST http://{node_ip}:{port}
Headers: { "AnyLog-Agent": "AnyLog/1.23", "Content-Type": "application/json" }
Body: {
  "command": "blockchain get uns where namespace = {namespace}"
}
```

Use the `prompts/base44.md` template from the MCP-Examples repo.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Failed to fetch` / CORS error in browser | Node not returning CORS headers | Switch to nginx or Flask proxy mode, or use `AnyLog-Agent` as a body key for direct POST |
| Preflight (`OPTIONS`) blocked — `No 'Access-Control-Allow-Origin' header` | Browser triggered CORS preflight due to reserved header or method | Use `AnyLog-Agent` instead of `User-Agent` in the POST body; ensure node whitelists `Access-Control-Allow-Headers: AnyLog-Agent, Content-Type` |
| All MCP tool calls fail silently | Missing `/mcp/sse` suffix in config | Verify the full URL: `http://HOST:PORT/mcp/sse` |
| CORS banner persists after switching proxy mode | Stale state | Click ↻ Refresh — clears on next successful fetch |
| `Is a directory` error on proxy startup | Docker created config as a directory | `docker compose down && rm -rf nginx.conf`, recreate as file |
| `502 Bad Gateway` from nginx | nginx can't reach AnyLog node | Check `ANYLOG_NODE_URL`; on Windows use `host.docker.internal` |
| SQL queries return empty, status works | Missing `destination: "network"` | Add `"destination": "network"` to SQL request body |
| MCP tools not visible in Claude Desktop | Config not loaded | Quit and fully reopen Claude Desktop |