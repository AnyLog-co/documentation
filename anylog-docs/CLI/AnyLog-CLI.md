---
title: AnyLog CLI
description: Use and navigate the AnyLog Command Line Interface — help, status checks, running commands on peer nodes, and scripting.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | updated hyperlinks
--> 

Each AnyLog node exposes a Command Line Interface (CLI) for direct interaction. The CLI lets you inspect node state, 
issue commands locally or to peer nodes, run scripts, and manage configuration — all from a text prompt.

> If AnyLog is running as a background process, the local CLI is disabled. Use the <a href="{{ '/docs/Tools-UI/remote-gui/' | relative_url }}">Remote-GUI</a> 
> instead to interact with the node over REST.

---

## The command prompt

When a node starts, it presents the following prompt:

```
AL >
```

You can personalise the prompt by assigning a node name:

```anylog
set node name Operator_3
```

The prompt then becomes:

```
AL Operator_3 >
```

A `+` suffix on the prompt means there is a message waiting in the buffer queue:

```
AL +>
```

Retrieve it with:

```anylog
get echo queue
```

---

## help

`help` is the fastest way to discover and understand AnyLog commands. It can be used at any level of specificity.

List all available command categories:
```anylog
help
```

Get help on a specific command:
```anylog
help get
help run
help blockchain
```

Get help on a specific sub-command:
```anylog
help get processes
help run operator
help blockchain sync
```

The `help` output includes a description, usage syntax, and examples — making it the best starting point when exploring any unfamiliar command.

---

### get processes

Lists all background services, their current status, and key configuration details. See <a href="{{ '/docs/Network-Services/background-services/' | relative_url }}">Background Services</a> 
for how to enable each service.

```anylog
get processes
get processes where format = json
```

Example output:
```
    Process         Status       Details
    ---------------|------------|------------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.233.208.212:32348, Threads Pool: 21                         |
    REST           |Running     |Listening on: 172.233.208.212:32349, Threads Pool: 12, Timeout: 20, SSL: False|
    Blockchain Sync|Running     |Sync every 60 seconds with master using: 45.79.74.39:32048                    |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                                |
    MSG Broker     |Running     |Listening on: 172.233.208.212:32550, Threads Pool: 6                          |
    ...            |            |                                                                              |
```

### get connections

Returns the IP and port the node is listening on for TCP, REST, and messaging:

```anylog
get connections
```

Example output:
```
Type      External               Local                  Bind
---------|----------------------|-----------------------|----------------------|
TCP      |172.233.208.212:32348 |172.233.208.212:32348  |172.233.208.212:32348 |
REST     |172.233.208.212:32349 |172.233.208.212:32349  |0.0.0.0:32349         |
Messaging|172.233.208.212:32550 |172.233.208.212:32550  |0.0.0.0:32550         |
```

### get dictionary

Displays all key-value pairs currently set in the node's local dictionary — including paths, IPs, ports, and any user-defined variables:

```anylog
get dictionary
get dictionary [key]    # retrieve a specific key
```

---

## Running commands on peer nodes

By default, a command runs on the local node. Adding `run client` routes the command to one or more peer nodes, with results returned to the issuing node.

**Single node:**
```anylog
run client 10.0.0.78:7848 get processes
```

**Multiple nodes:**
```anylog
run client (10.0.0.78:7848, 10.0.0.25:2548) get processes
```

**All nodes of a given type (via metadata lookup):**
```anylog
run client (blockchain get operator bring.ip_port) get status
```

**With partial results allowed** (does not abort if a node is unresponsive):
```anylog
run client (blockchain get operator bring.ip_port, subset = true) get status
```

**Capture results into a variable:**
```anylog
nodes_stat[] = run client (blockchain get operator bring.ip_port, subset = true) get status
nodes_stat{} = run client (blockchain get operator bring.ip_port, subset = true) get status
```

**Filter nodes by metadata attribute** (e.g. country):
```anylog
run client (operator where [country] contains US bring.ip_port, subset = true) get status
```

**Target nodes by the data they host:**
```anylog
run client (dbms = my_dbms, table = my_table) get status
```

> The `blockchain get` prefix inside parentheses is optional and can be omitted.

---

## CLI operations

### Variables and the dictionary

Assign and reference variables using `!` for local dictionary keys and `$` for system environment variables:

```anylog
ip = 192.168.1.10
port = 7848
connection = !ip + ':' + !port
```

### `incr`

Increments a variable by a given value (default: 1):

```anylog
a = 1
b = incr !a 3    # b = 4
```

### String concatenation with `+`

The `+` operator concatenates strings, dictionary variables, and environment variables:

```anylog
a = 12
b = 3
c = !a + !b     # c = '1234'
```

Mixed example with an environment variable:
```anylog
export PATH=/status
a = 127.0.0.1
b = 5432
c = !a + ':' + !b + $PATH    # c = '127.0.0.1:5432/status'
```

### `python`

Executes a subset of Python expressions inline, with dictionary keys resolved before execution:

```anylog
ip_port = python !ip + ':4028'
date_time = python "datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')"
new_dir = python !watch_dir.rsplit('/', 1)[0] + '.out'
```

Type coercion:
```anylog
a = 12
b = 45
new_value1 = python !a.str + !b.str    # '1245'
new_value2 = python !a.int + !b.int    # 57
new_value3 = python !a.float + !b.float    # 57.0
```