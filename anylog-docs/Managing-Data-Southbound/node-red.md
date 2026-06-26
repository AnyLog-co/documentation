---
title: Node-RED
description: Send data from Node-RED flows into AnyLog via REST POST.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlinks
--> 

[Node-RED](https://nodered.org/) is an open-source flow-based programming tool for connecting hardware, APIs, and services visually. This guide shows how to stream timestamp/value data from a Node-RED flow into an AnyLog operator via REST POST.

---

## Prerequisites

- [Node-RED installed](https://nodered.org/docs/getting-started/local)
- An AnyLog operator node running with REST service enabled (see <a href="{{ '/docs/Network-Services/background-services//#rest-service' | relative_url }}">Background Services</a>)

---

## Step 1 — Create the flow

Build a flow with these nodes:

- **Inject** — triggers the flow
- **Function** — generates the payload
- **JSON** — serialises the output
- **HTTP request** — sends the POST to AnyLog
- **HTTP response** — handles the reply
- **Trigger** — repeats every N seconds

A [sample flow JSON](https://github.com/AnyLog-co/documentation/blob/master/examples/node_red_sample_flow.json) is available in the AnyLog documentation repo.

---

## Step 2 — Write the function node

This function generates a random value with a timestamp and wraps it with a table name:

```javascript
var timestamp = new Date();

var min = 1;
var max = 100;
var randomValue = Math.floor(Math.random() * (max - min + 1)) + min;

var combinedResults = {
    table: "rand_data",
    timestamp: timestamp,
    value: randomValue
};

msg.payload = combinedResults;
return msg;
```

---

## Step 3 — Configure the HTTP request node

Set the method to **POST** with these headers:

| Header | Value |
|---|---|
| `command` | `data` |
| `topic` | `node-red` |
| `User-Agent` | `AnyLog/1.23` |
| `Content-Type` | `text/plain` |

Set the URL to your operator's REST endpoint: `http://[operator-ip]:[rest-port]`

---

## Step 4 — Configure the AnyLog operator

On the operator node, start a message client that subscribes to the `node-red` topic on the REST port:

```anylog
<run msg client where
  broker = rest and
  port = !anylog_rest_port and
  user-agent = anylog and
  log = false and
  topic = (
    name = node-red and
    dbms = !default_dbms and
    table = "bring [table]" and
    column.timestamp.timestamp = "bring [timestamp]" and
    column.value.int = "bring [value]"
  )>
```

---

## Step 5 — Run the flow and verify

Start the Node-RED flow, then query the data from a query node:

```anylog
run client () sql new_company format=table "SELECT * FROM rand_data LIMIT 15;"
```

Expected output:

```
row_id  insert_timestamp            timestamp                value
------- --------------------------- ----------------------- -----
     1  2024-02-24 00:14:41.157796  2024-02-24 00:13:34.402    15
     2  2024-02-24 00:14:41.157796  2024-02-24 00:13:58.632    35
     3  2024-02-24 00:14:41.157796  2024-02-24 00:13:58.750    97
    ...
```

---

## How it fits in the southbound picture

Node-RED uses the same **REST POST + msg client** pattern as any other POST-based ingestion. The `topic` header is the bridge between the HTTP request and the `run msg client` mapping rule on the operator. See <a href="{{ '/docs/Monitoring-Data-Southbound/data-ingestion/' | relative_url }}">Data Ingestion</a> for the full pattern.