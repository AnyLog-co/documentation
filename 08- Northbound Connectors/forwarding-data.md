---
title: Forwarding Data
description: Two basic ways to send data out of AnyLog — a SQL query over REST, and a one-off message via mqtt publish.
layout: page
---
<!--
## Changelog
- 2026-07-14 | Created document
-->

Two basic ways to get data or a message out of AnyLog to an external system: querying data over REST, or publishing
a one-off message to an MQTT broker.

---

## 1. REST — SQL command via GET or POST

Issue a SQL query against a node over HTTP, either as a `GET` with the command in a header, or as a `POST` with the
command in a JSON body (useful where custom headers aren't available — browsers, some GUIs, etc.).

**GET:**

```bash
curl -X GET 'http://10.0.0.78:32349' \
  -H 'command: sql mydb format=table "select * from ping_sensor where timestamp >= now() - 1 hour limit 10"' \
  -H 'User-Agent: AnyLog/1.23' \
  -w "\n"
```

**Equivalent POST:**

```bash
curl -X POST 'http://10.0.0.78:32349' \
  -H 'Content-Type: application/json' \
  -d '{
    "command": "sql mydb format=table \"select * from ping_sensor where timestamp >= now() - 1 hour limit 10\"",
    "AnyLog-Agent": "AnyLog/1.23"
  }' \
  -w "\n"
```

Both return the same result set. See [Using REST](../07-%20Southbound%20Interfaces/A-%20Direct%20Connectors%20Generic/Using%20REST.md)
for the full GET/POST reference, including why `AnyLog-Agent` (not `User-Agent`) is the key to use in a POST body
specifically.

---

## 2. MQTT — `mqtt publish`

Publish a single message directly to an MQTT broker from the AnyLog CLI — useful for a one-off test message or a
simple manual alert, as opposed to `run msg client`/`run message broker`, which set up an ongoing
subscribe/host relationship.

```anylog
AL > help mqtt

Usage:
        mqtt publish where broker = [url] and topic = [topic]

Explanation:
        Publish a message to the MQTT broker
```

Example:

```anylog
mqtt publish where broker = "driver.cloudmqtt.com" and port = 18975 and user = [user] and password = [password] and topic = test and message = "hello world"
```

Replace `[user]`/`[password]` with your own broker credentials — never hard-code real ones into a saved script or
shared document.

See [Message Broker](../07-%20Southbound%20Interfaces/A-%20Direct%20Connectors%20Generic/message%20broker.md) for
the broader picture of AnyLog's MQTT roles (subscribing as a client vs. running as the broker itself) — `mqtt publish`
is a separate, simpler command from either of those: it just sends one message and returns, rather than starting a
standing process.