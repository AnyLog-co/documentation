---
title: Using REST
description: Execute AnyLog commands and publish data over HTTP using GET, PUT, and POST.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-23 | Moved to Network and Services; added POST as GET alternative, AnyLog-Agent header, blockchain insert command, Python examples
- 2026-04-24 | there was an issue with the REST POST of commands example 
- 2026-04-25 | REST GET via browser support 
- 2026-04-25 | hyperlink support
-->

Any AnyLog node with the REST service enabled, can receive commands and data over HTTP. This lets external applications, 
dashboards, and scripts interact with the network without running AnyLog themselves.

---

## HTTP method mapping

| Method | Used for |
|---|---|
| `GET` | Retrieve information — `sql`, `get`, `blockchain get`, `help` |
| `GET` (query string) | Browser-native GET — command and options passed as `?key=value?key=value` parameters |
| `POST` | All commands (alternative to GET) and data publishing via topic mapping |
| `PUT` | Publish time-series data directly to a node |

---

## Headers and the AnyLog-Agent

Every request requires an identity header. AnyLog accepts either `User-Agent` or `AnyLog-Agent`:

| Header | Value | Notes |
|---|---|---|
| `User-Agent: AnyLog/1.23` | Standard HTTP header | Works in server-side scripts (curl, Python `requests`, etc.) |
| `AnyLog-Agent: AnyLog/1.23` | Custom AnyLog header | **Preferred when calling from a browser** — avoids CORS preflight (see below) |

Both are accepted by the node and treated identically. For server-side code either works. For browser-based clients, use `AnyLog-Agent`.

### Why AnyLog-Agent for browser clients

Browsers treat `User-Agent` as a reserved header — `fetch()` cannot set it manually, and its presence in a cross-origin 
request triggers a CORS preflight (`OPTIONS`) that AnyLog nodes are not configured to answer. `AnyLog-Agent` is a 
custom header that both the browser and the node control explicitly, allowing the node to whitelist it:

```
Access-Control-Allow-Headers: AnyLog-Agent, Content-Type
```

 
See <a href="{{ '/docs/network-services/using-rest/#rest-service' | relative_url }}">Network and Services — REST service</a> 
and the <a href="https://github.com/AnyLog-co/MCP-Examples" target="_blank">MCP-Examples CORS guide</a> for 
proxy-based solutions when direct browser access is not possible.

---

## GET requests

GET passes the command and options as HTTP headers.

### Common GET headers

| Header | Description |
|---|---|
| `command: [anylog command]` | The command to execute |
| `User-Agent: AnyLog/1.23` | Required (or `AnyLog-Agent: AnyLog/1.23`) |
| `destination: network` | Route a query across all relevant nodes |
| `destination: [IP:Port]` | Send to a specific node |

### Check node status
```bash
curl -X GET 'http://10.0.0.78:32349' \
  -H 'command: get status' \
  -H 'User-Agent: AnyLog/1.23'
```

### Get running processes
```bash
curl -X GET 'http://10.0.0.78:32349' \
  -H 'command: get processes' \
  -H 'User-Agent: AnyLog/1.23'
```

### Query metadata
```bash
curl -X GET 'http://10.0.0.78:32349' \
  -H 'command: blockchain get operator where company="AnyLog Co."' \
  -H 'User-Agent: AnyLog/1.23'
```

### SQL query across the network
```bash
curl -X GET 'http://10.0.0.78:32349' \
  -H 'command: sql mydb format=table "select * from rand_data where timestamp >= now() - 1 minute limit 10"' \
  -H 'User-Agent: AnyLog/1.23' \
  -H 'destination: network' \
  -w "\n"
```

> Always add `-w "\n"` to GET/SQL requests to avoid chunked-encoding display issues.

### Get help
```bash
curl -X GET 'http://10.0.0.78:32349' \
  -H 'command: help blockchain get' \
  -H 'User-Agent: AnyLog/1.23'
```

### Browser GET (query string)

When calling from a browser directly — where custom headers cannot be set — pass the command and options as query 
string parameters instead. Each parameter is separated by `?` rather than `&`:

```
http://10.0.0.78:7849/?command=get status where format=json?AnyLog-Agent=AnyLog/1.23

http://10.0.0.78:7849/?command=sql anotherpeak select * from battery_pack_logs where period(minute, 5, now(), timestamp) limit 10?AnyLog-Agent=AnyLog/1.23?destination=network
```

| Parameter | Description |
|---|---|
| `command` | The AnyLog command to execute |
| `AnyLog-Agent` | Identity header — use `AnyLog/1.23` |
| `destination` | Optional — `network` to broadcast, or `IP:Port` for a specific node |

> Note the separator between parameters is `?` not `&` — this is specific to AnyLog's query string parsing and differs 
> from standard URL convention.

This is the browser equivalent of the curl GET style. For browser-based applications making programmatic calls, prefer 
[POST with `AnyLog-Agent` in the body](#post-as-an-alternative-to-get) — it gives more control and avoids query string 
length limits.


---

## POST requests

POST serves four distinct purposes in AnyLog:

| Use                                               | Description |
|---------------------------------------------------|---|
| Publish Data                                      | Ingest time-series data via topic mapping (`run msg client` with `broker=rest`) |
| Publish metadata                            | Insert policies to the blockchain via `blockchain insert` |
| Execute commands | Send any AnyLog command to the node — same as GET but via JSON body |
| GET via JSON body                             | Pass GET-style headers as JSON keys — useful where custom HTTP headers are restricted |

--- 

### Publishing Data via POST


The logic with publishing data via _POST_ allows for a simple logic for getting data into AnyLog with the behavior 
of MQTT's [mapping policies](/docs/Managing-Data-Southbound/mapping-policies.md) logic.  

As such, POST data publishing requires a `run msg client` with `broker=rest` active on the receiving node. This maps 
incoming JSON fields to a target database and table; thus the actual idea of publishing data (entirely via REST). 

1. **Define Mapping Policy** - The policy describes how incoming JSON fields map to database columns:

```json
{
   "mapping": {
      "id": "my-mappigng1",
      "dbms": "bring [dbms]",
      "table": "bring [table]",
      "readings": "",
      "schema": {
         "timestamp": {
            "default": "now()", 
            "type": "timestamp",
            "bring": "[timestamp]"
         },
         "value": {
            "default": null,
            "type": "float",
            "bring": "[value]"
         }
     }
 }}   
```

2. **Publish Policy** - Publish mapping policy to the blockchain, this would be used in `run msg client` to understand the data coming in. 

```shell
curl -X POST 'http://10.0.0.69:32149' \
  -H 'command: blockchain insert where policy=!new_policy and local=true and master_node=!ledger_conn' \
  -H 'AnyLog-Agent: AnyLog/1.23' \
  --data-raw '<new_policy={"mapping": {
    "id": "my-mapping1",
    "dbms": "bring [dbms]",
    "table": "bring [table]",
    "readings": "",
    "schema": {
      "timestamp": {
        "default": "now()",
        "type": "timestamp",
        "bring": "[timestamp]"
      },
      "value": {
        "default": null,
        "type": "float",
        "bring": "[value]"
      }
    }
  }}>'
```

3. **Define `msg client`**  - Start message client logic on the operator node 

```shell
curl -X POST 'http://10.0.0.69:32149' \
   -H "command: run msg client where broker=rest and user-agent=anylog and log=false topic=(name=my-topic and policy=my-mapping1)" \
   -H "User-Agent: AnyLog/1.23"
```

4. **Publish data** - In the example all the JSON keys would be mapped to the mapping policy. 

```bash
curl -X POST 'http://10.0.0.69:32149' \
  -H 'command: data' \
  -H 'topic: my-topic' \
  -H 'User-Agent: AnyLog/1.23' \
  -H 'Content-Type: text/plain' \
  --data-raw '[
    {"dbms": "mydb", "table": "sensor_data", "value": 50, "timestamp": "2019-10-14T17:22:13Z"},
    {"dbms": "mydb", "table": "sensor_data", "value": 55, "timestamp": "2019-10-14T17:22:14Z"}
  ]'
```

5. **Validate data is being received** - using `get streaming` validate data is being inserted - this is usually done via REST-GET, however, in order to show 
the full scope of how to utilize POST, the example check the streaming status for operator (`10.0.0.69:32149`) through the 
query node `10.0.0.69:32349`. 
 
```shell
curl -X POST 'http://10.0.0.69:32349' \
  -H "Content-Type: application/json" \
  -d '{"command": "get streaming", "User-Agent: AnyLog/1.23", "destination": "10.0.0.69:32148"}'
```

> Full working examples can be found in
> <a href="#" onclick="openEnvModal('/assets/examples/sample-post.py'); return false;">sample-post.py</a>


--- 

### Execute commands via POST

POST can execute any AnyLog command by passing the command as an HTTP header, and can be used to bring services up and 
down as needed without interacting with the actual [CLI](/docs/CLI/AnyLog-CLI.md). Thus Anylog be configured or altered 
through third-party apps, via our API or simply when [running as a service](/docs/Getting-Started/anylog-as-service.md)
and the CLI is not enabled.

**Connect to logical database**
```bash
curl -X POST 'http://10.0.0.78:32349' \
  -H "command: connect dbms mydb where type=sqlite " \
  -H "AnyLog-Agent: AnyLog/1.23"
```

**Reset the error log**
```bash
curl -X POST 'http://10.0.0.78:32349' \
  -H "command: reset error log" \
  -H "AnyLog-Agent: AnyLog/1.23"
```

**Set a variable**
```bash
curl -X POST 'http://10.0.0.78:32349' \
  -H "command: set company_name = AnyLog" \
  -H "AnyLog-Agent: AnyLog/1.23"
```

---  

### POST as an alternative to GET

[_GET_](#get-requests) is the most common, and probably most natural form, of executing requests against via cURL. 
However, it is far more limited in fetch logic and may not be supported with all tooling example Kubernetes and some
browser-based GUIs; often preferring POST with JSON bodies in order to bypass their security restrictions. For those 
cases, AnyLog accepts GET request as POST, where the GET headers become the serialized JSON body content of the request. 

In addition, `AnyLog-Agent` as opposed to `User-Agent` is often prefer with browser-through requests as browsers 
silently ignore any attempt to set User-Agent manually, and its presence in a cross-origin request triggers a CORS 
preflight that AnyLog nodes are not configured to answer. 

Essentially, `AnyLog-Agent` is a custom header that both sides control, so the node can explicitly whitelist it and 
browsers can set it without restriction.

**GET style**:
* basic `get status`
```bash
curl -X GET 'http://10.0.0.69:32349' \
  -H 'command: get status' \
  -H 'AnyLog-Agent: AnyLog/1.23'
```

* Query against the data
```bash
curl -X GET 'http://10.0.0.69:32349' \
  -H "command: sql mydb format=json:list and stat=false select * from sensor_data where timestamp >= now() - 1 minute limit 10" \
  -H "AnyLog-Agent: AnyLog/1.23" \
  -H "destination: network" \
  -w "\n"
```


**Equivalent POST style**:
* basic `get status`
```bash
curl -X POST 'http://10.0.0.69:32349' \
  -H 'Content-Type: application/json' \
  -d '{"command": "get status", "AnyLog-Agent": "AnyLog/1.23"}'
```

* Query against the data
```bash
curl -X POST 'http://10.0.0.69:32349' \
  -H 'Content-Type: application/json' \
  -d '{
    "command": "sql mydb format=json:list and stat=false select * from sensor_data where timestamp >= now() - 1 minute limit 10",
    "AnyLog-Agent": "AnyLog/1.23",
    "destination": "network"
  }' \
  -w "\n"
```

Both return the same response. Use `AnyLog-Agent` in the body when calling from a browser.

--- 


## PUT requests — publish data directly

PUT bypasses topic mapping entirely. The target database and table are specified directly in the request headers, and 
data is written to the node immediately (or buffered in streaming mode).

### Required headers

| Header | Description |
|---|---|
| `type: json` | Data format (default) |
| `dbms: [name]` | Target logical database |
| `table: [name]` | Target logical table |
| `mode: streaming` | Optional — buffer data instead of writing immediately |
| `User-Agent: AnyLog/1.23` | Required (or `AnyLog-Agent: AnyLog/1.23`) |
| `Content-Type: text/plain` | Required |

### curl example

```bash
curl -X PUT 'http://10.0.0.78:32149' \
  -H 'type: json' \
  -H 'dbms: mydb' \
  -H 'table: sensor_data' \
  -H 'mode: streaming' \
  -H 'Content-Type: text/plain' \
  -H 'User-Agent: AnyLog/1.23' \
  -w "\n" \
  --data-raw '[
    {"device_name": "sensor-01", "value": 42.5, "timestamp": "2024-01-01T10:00:00Z"},
    {"device_name": "sensor-01", "value": 43.1, "timestamp": "2024-01-01T10:00:01Z"}
  ]'
```

Expected response: `{"AnyLog.status":"Success", "AnyLog.hash": "0dd6b959..."}`

> Full working examples can be found in
> <a href="#" onclick="openEnvModal('/assets/examples/sample-put.py'); return false;">sample-put.py</a>