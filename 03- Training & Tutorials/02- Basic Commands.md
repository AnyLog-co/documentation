---
title: "The Basic Guided Tour"
description: "a basic understanding of using AnyLog"
layout: page
source_path: "training/02- Basic Commands.md"
---

<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**            | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-24 | Ori Shadmon    | rewrote          |          |
--->

# Basic AnyLog Commands

This document covers the basics of AnyLog commands. These commands can be executed on the CLI (once attached) or via
REST — usually via GET unless stated otherwise.

The assumption for this document is that the node is already running and configured.

## REST Formatting

A quick reference for connecting to AnyLog via REST. A more detailed document can be found <a href="../06-%20Networking%20&%20Security/04-%20Using%20REST.md" target="_blank">here</a>.

**REST `GET` example**

```shell
curl -X GET http://[Node ip]:[Node port] \
  -H "command: [AnyLog Command]" \
  -H "AnyLog-Agent: AnyLog/1.23"
```

**REST `POST` examples**

```shell
# GET commands via POST

curl -X POST http://[Node ip]:[Node port] \
  -H "Content-Type: application/json" \
  -d '{"command": "[AnyLog Command]", "AnyLog-Agent": "AnyLog/1.23" }'

# Pure POST command — used for non-`get` commands

curl -X POST http://[Node ip]:[Node port] \
  -H "command: [AnyLog Command]" \
  -H "AnyLog-Agent: AnyLog/1.23"
```

---

## Help Commands

The `help` command provides dynamic information on AnyLog commands.

**List all commands** — type `help` on the CLI:

```anylog
help
```

**List commands by prefix** — for example, `get` is the prefix of a group of commands, listed via `help get`:

```anylog
help get
help set
help reset
help blockchain
```

**List usage and examples for a specific command** — type `help` followed by the command text:

```shell
help connect dbms
help blockchain insert
help get msg client
```

`help` returns the usage, examples, an explanation, and a link to the relevant documentation. For example:

```anylog
help blockchain get

Usage:
        blockchain get [policy type] [where] [attribute name value pairs] [bring] [bring command variables]

Explanation:
        Get the policies or information from the policies that satisfy the search criteria.

Examples:
        blockchain get *
        blockchain get operator where dbms = lsl_demo
        blockchain get cluster where table[dbms] = purpleair and table[name] = air_data bring [cluster][id] separator = ,
        blockchain get operator bring.table [*] [*][name] [*][ip] [*][port]
        blockchain get * bring.table.unique [*]

Index:
        ['blockchain']
```

---

## Logged Events

Like an operating system, AnyLog has a built-in logging mechanism that tracks events and errors within the agent.
Each node maintains buffers to record events and errors so that users and applications can retrieve recent events
and errors as they accrue.

**Command format:**

```anylog
get [log type] log where format = [format type] and keys = key1 key2 ...
```

| Parameter | Description |
|---|---|
| `[log type]` | `event`, `error`, `file`, `query`, or `msg` |
| `format` | Output format — `table` (default) or `json` |
| `key` | One or more keywords to filter logged events by content |

**Examples:**

```anylog
get event log where format = json and keys = SQL Error

get error log where format = json and keys = rest
```

### Event Log

The event log records the events processed on the node, including the AnyLog commands executed and any error
messages.

```anylog
get event log
```

### Error Log

The error log records recent errors on the node — these could be "human errors" (an invalid command) or internal
issues (a failure to send a message from one machine to another).

```anylog
get error log
```

### Echo Queue

AnyLog has two print commands — `echo` and `print`. `print` **always** returns output to screen, like Python's
`print`. `echo` does the same thing unless a logging config is enabled (done through the deployment-scripts) —
this lets you run a "print" that's stored in a log rather than only shown on screen.

```anylog
# Enable echo queue
set echo queue on

# Use echo queue
echo "hello world"

# View the echo queue
get echo queue

# Disable echo queue
set echo queue off
```

### Reset the Log

The `reset` command clears variables and configuration parameters — in this case, it deletes the log entries in
the specified file:

```anylog
reset [event/error/echo queue] log
```

---

## Dictionary

The local dictionary enables hardware abstraction by mapping configuration values — which are specific to the
hardware in use — to generic keys shared across all deployments. Configuration, queries, and AnyLog commands
reference these shared keys, which are translated to the node-specific values. For example, IPs, ports, and file
or directory paths are referenced by key name and translated on each node to the appropriate value.

Some entries represent default setups and configurations; users can add or modify entries as needed.

For example, every directory in the default folder structure can be referenced by key, even though the physical
location of each folder may differ per deployment. Using this pattern, the archive directory is referenced via the
key `!archive_dir`, the blobs directory via `!blobs_dir`, and so on — allowing a shared configuration process while
the physical path to each folder can differ per node.

Users can add any key/value pair needed to support a process — for example, storing values generated by data
ingestion or representing node state. A user could declare a key called `disk_usage` and configure the scheduler to
update its value with the percentage of free space every 15 seconds, then reference that value in processes that
monitor node state.

The dictionary is also used to construct, maintain, and update policies before their persistent storage in the
shared metadata.

### Retrieve Dictionary Values

`get dictionary` returns all dictionary values:

```anylog
# Table format
get dictionary

# JSON format
get dictionary where format = json
```

A single value is retrieved as follows:

```anylog
!var_name
```

Via REST, specify `get` before the key:

```shell
curl -X GET http://[Node ip]:[Node port] \
  -H "command: get !var_name" \
  -H "AnyLog-Agent: AnyLog/1.23"
```

* On the AnyLog CLI, it's sufficient to reference the value without the `get` keyword.
* System variables are referenced with a dollar sign — for example, `$TMP` or `$HOME`.
* Paths and file names can be referenced by key + relative value. For example, `!local_scripts/node-deployment/main.al`
  is transformed on each node into the full path `/app/deployment-scripts/node-deployment/main.al`, using the
  physical path associated with the key `!anylog_path`.

By default, a variable is returned as a string. To return it as a different type (e.g. int or bool), append a
conversion suffix:

```anylog
AL > !anylog_rest_port

"2148"

AL > !anylog_rest_port.int

2148

AL > set tcp_bind = true
AL > !tcp_bind

"true"

AL > !tcp_bind.bool

True
```

### Defining a Variable

To define a variable, set its name followed by `=` and the desired value. When the value is itself an AnyLog
command (e.g. `test`), prefix the assignment with `set` — otherwise, the *result* of the command is stored instead
of the command text.

```anylog
my_var = 1
my_var2 = "hello world"
```

```anylog
# Stores the result of the query — true / false depending on whether the file exists
is_file = file test !blockchain_dir/blockchain.json

# Stores the literal command text `file test ...`
set is_file = file test !blockchain_dir/blockchain.json
```

---

## Networking & Services

By default, user-defined configurations and the config policy set the network IPs and ports. A more detailed
document can be found <a href="../02-%20Installation%20&%20Deployment/01-%20Install.md" target="_blank">here</a>.

> **Note:** IP addresses and node names shown in the examples below are illustrative placeholders, not a real
> network.

### Checks Using `get`

**View connections** — each row shows 3 addresses: External, Internal, and Bind.

```anylog
get connections
```

```
Type       External Address     Internal Address     Bind Address
---------  -------------------  -------------------  ----------------
TCP        10.0.0.10:32048      10.0.0.10:32048       10.0.0.10:32048
REST       10.0.0.10:32049      10.0.0.10:32049       0.0.0.0:32049
Messaging  10.0.0.10:32250      10.0.0.10:32250       0.0.0.0:32250
```

If the Bind address is `0.0.0.0`, the node replies on any of the machine's IPs for that port. If bound to a specific
IP, AnyLog only accepts messages sent to that address.

The TCP connection is the internal IP + port AnyLog agents use to communicate with one another — it is **not**
intended for a user to send data through directly; that's what the REST and Message Broker ports are for, covered
<a href="../06-%20Networking%20&%20Security/02-%20Network%20Processing.md" target="_blank">here</a>.

**View services** — lists all services available to enable/disable, and which are currently active. By default,
TCP, REST, and Blockchain Sync should be active.

```anylog
get processes
```

```
Process           Status        Details
----------------  ------------  ----------------------------------------------------------------------
TCP               Running       Listening on: 10.0.0.10:32148, Threads Pool: 6
REST              Running       Listening on: 10.0.0.10:32149, Threads Pool: 6, Timeout: 20, SSL: False
MCP               Not declared
Operator          Running       Cluster Member: True, Using Master: 10.0.0.10:32048, Threads Pool: 3
Blockchain Sync   Running       Sync every 120 seconds with master using: 10.0.0.10:32048
Scheduler         Running       Schedulers IDs in use: [0 (system)] [1 (user)]
Blobs Archiver    Running       Flags: dbms = False, folder = True, compress = True, reuse_blobs = True
MQTT              Running
MSG Client Pool   Not declared
MSG Broker        Running       Listening on: 10.0.0.10:32150, Threads Pool: 6
SMTP              Not declared
Streamer          Running       Default streaming thresholds are 60 seconds and 10,240 bytes
UNS Streamer      Not declared
Query Pool        Running       Threads Pool: 3
Kafka Consumer    Not declared
gRPC              Not declared
PLC Client        Not declared
Pull Processes    Running       1 pull processes active
Video Processes   Not declared
Publisher         Not declared
Distributor       Not declared
Consumer          Not declared
```

**View databases** — lists databases directly accessible on the AnyLog agent.

```anylog
get databases
```

```
Active DBMS Connections
Logical DBMS     Database Type  Owner    IP:Port          Configuration                                  Storage
---------------  -------------  -------  ---------------  ---------------------------------------------  ----------------------------------------------
almgm            psql           system   127.0.0.1:5432   Autocommit On, Fsync on                        Persistent
blockchain       psql           system   10.0.0.10:5432   Autocommit On, Fsync on                        Persistent
monitoring       sqlite         user     Local            Autocommit On, Fsync full (after each write)    /app/AnyLog-Network/data/dbms/monitoring.dbms
demo_data        psql           user     127.0.0.1:5432   Autocommit On, Fsync on                         Persistent
system_query     sqlite         system   Local            Autocommit On, RAM, Fsync full (after write)    MEMORY
```

### Checking Using `test`

There are two types of tests that can be run on a given node:

**`test node`** — tests whether the node is configured properly and able to communicate with itself.

```anylog
test node
```

```
Test                                       Status
------------------------------------------ ----------------------------------------------------------------
Metadata Version                           d2ef59e6735872529f81c5c86702db76
Metadata Test                              Pass
TCP test using 10.0.0.10:32048             [From Node 10.0.0.10:32048] anylog-master@10.0.0.10:32048 running
REST test using http://10.0.0.10:32049     anylog-master@10.0.0.10:32048 running
```

**`test network`** — checks whether the node can communicate with other agents on the blockchain.

```anylog
test network
```

```
Test Network
[****************************************************************]

AL anylog-master +>
Address              Node Type  Node Name              Status
-------------------  ---------  ---------------------  ------
10.0.0.10:32048      master     anylog-master             +
10.0.0.11:32148      operator   operator-demo-1           +
10.0.0.12:32148      operator   operator-demo-2           +
10.0.0.13:32148      operator   operator-demo-3           +
10.0.0.14:32348      query      query-demo-1               +
10.0.0.15:32348      query      query-demo-2               +
10.0.0.16:32148      operator   operator-demo-4 (backup)
```

A `+` status means the nodes can ping one another; a blank status means they cannot.