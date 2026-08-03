---
title: Forwarding Data
description: Two basic ways to send data out of AnyLog — a SQL query over REST, and a one-off message via mqtt publish.
layout: page
---
<!--
## Changelog
- 2026-07-14 | Created document
- 2026-07-25 | Ori Shadmon | Added a structured-JSON publish example (the `<message={...}>` + `message=!message`
  pattern) alongside the existing plain-string example — the original only showed publishing a bare "hello world"
  string, which undersells what `mqtt publish` is actually used for in practice. Filled out the `help mqtt` usage
  line, which was missing `message=` (a required parameter) and the other optional keys the examples below it
  actually use.
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
  -H "destination: network" \
  -w "\n"
```

**Equivalent POST:**

```bash
curl -X POST 'http://10.0.0.78:32349' \
  -H 'Content-Type: application/json' \
  -d '{
    "command": "sql mydb format=table \"select * from ping_sensor where timestamp >= now() - 1 hour limit 10\"",
    "AnyLog-Agent": "AnyLog/1.23",
    "destination": "network"
  }' \
  -w "\n"
```

Both return the same result set. See [Using REST](../06-%20Networking%20%26%20Security/04-%20Using%20REST.md)
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
        mqtt publish where broker = [url] and port = [port] and user = [user] and password = [password]
        and topic = [topic] and message = [message] and qos = [value]

Explanation:
        Publish a message to the MQTT broker
```

`user`/`password` are only needed if the broker requires authentication; `qos` defaults to `0` if omitted.

### Publishing a plain string

```anylog
mqtt publish where broker = "driver.cloudmqtt.com" and port = 18975 and user = [user] and password = [password] and topic = test and message = "hello world"
```

Replace `[user]`/`[password]` with your own broker credentials — never hard-code real ones into a saved script or
shared document.

### Publishing structured JSON data

For anything beyond a quick string test, define the message as a JSON object first, then reference it by variable
name in the `mqtt publish` command. This is also how you'd simulate a device sending a real reading.

**Define the message:**

```anylog
<message={"id":"ec798767-617c-467c-984f-ba5fddd474f1",
	"device":"Random-Integer-Generator01",
	"created":1625862443151,
	"origin":1625862443149315045,
	"readings":[{	"id":"4b553911-e41f-4146-a863-a8e5a9ad1cfc",
			"origin":1625862443149271124,
			"device":"Random-Integer-Generator01",
			"name":"RandomValue_Int32",
			"value":"-998060882",
			"valueType":"Int32"}]}>
```

The `< >` wrapper lets the AnyLog CLI treat this multi-line JSON as a single command — you can paste the block
above directly into the CLI as-is.

**Publish it** — `!message` refers back to the variable just defined:

```anylog
mqtt publish where broker=!ip and port=7850 and topic=mqtt-test and message=!message
```

Here `broker=!ip` publishes to this node's own broker (assuming one is running on port `7850`) rather than a
third-party one — swap in a real broker address and credentials the same way as the plain-string example above if
publishing externally.

See [Message Broker](../07-%20Southbound%20Interfaces/A-%20Direct%20Connectors%20Generic/message%20broker.md) for
the broader picture of AnyLog's MQTT roles (subscribing as a client vs. running as the broker itself) — `mqtt publish`
is a separate, simpler command from either of those: it just sends one message and returns, rather than starting a
standing process.