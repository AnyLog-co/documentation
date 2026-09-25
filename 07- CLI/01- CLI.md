---
title: "CLI Overview"
description: "The AnyLog command prompt, running commands locally or across the network, executing scripts, and working with CLI variables."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-26 | Ori Shadmon    | Reorganized CLI section: merged content previously split between "07- CLI" and "99- Commands & CLI"; moved control-flow (if/goto/for loop/wait) to its own "Conditional Execution & Control Flow" page | |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-08-29 | Moshe Shadmon  | Updated CLI overview | 2.0.2606 |
--->

# The AnyLog CLI

## Overview

Every AnyLog node provides a Command Line Interface (CLI) for executing commands, inspecting the node, managing services and metadata, running scripts, and interacting with peer nodes across the AnyLog network.

By default, commands entered at the CLI execute on the **local node**.

Using `run client`, the current node acts as a **client to the AnyLog network** and sends the command to one or more target nodes. Targets can be specified explicitly or resolved dynamically using the network metadata.

> **Note**
> Most, but not all, AnyLog commands can be issued to a node through the REST interface. From the CLI, the `run client` command 
> allows the current node to act as a client to the AnyLog network and issue a command to one or more target nodes.

---

## The Command Prompt

The default CLI prompt is:

```anylog
AL >
```

Users can assign a node name using `set node name`:

```anylog
AL > set node name Operator_3
AL Operator_3 >
```

This is useful when working with multiple AnyLog nodes because the active node is immediately visible in the prompt.

See [Set Node Name](./03-%20Get%20%26%20Set.md#set-node-name).

### Pending Messages

A `+` in the prompt indicates that a message is waiting in the node's echo queue:

```anylog
AL +>
```

Retrieve queued messages using:

```anylog
get echo queue
```
Clear the messages from the echo queue using:

~~~anylog
reset echo queue
~~~

---

## CLI Help

Use `help` to list available command families:

```anylog
help
```

Search for commands associated with a command family:

```anylog
help blockchain
```

Retrieve help for a specific command:

```anylog
help blockchain get
```

Commands can also be searched by category:

```anylog
help index
```

For example:

```anylog
help index streaming
```

The built-in help provides command syntax, descriptions, examples, and links to the corresponding documentation.

---

## Executing Commands Locally

Commands are executed on the current node unless `run client` is specified.

For example:

```anylog
get processes
```

returns the processes running on the local node.

Other useful local commands include:

```anylog
get connections
test node
get dictionary
blockchain get *
```

---

# Basic CLI Operations

The CLI can operate on values maintained in the local AnyLog dictionary.

See [Get and Set Reference](./03-%20Get%20%26%20Set.md#get-dictionary) for the complete dictionary and variable command reference.

---

## Dictionary Variables

AnyLog maintains a local dictionary of key/value pairs that can be referenced from CLI commands and scripts.

Set a dictionary variable:

```anylog
set company_name = AnyLog
```

Reference the value using `!`:

```anylog
get !company_name
```

Use the value in another command:

```anylog
blockchain get operator where company = !company_name
```

View the complete dictionary:

```anylog
get dictionary
```

Search dictionary keys containing a string:

```anylog
get dictionary _dir
```

This is useful when looking for configuration variables without knowing their exact key names.

For example, `get dictionary _dir` can locate values such as:

```text
data_dir
watch_dir
prep_dir
error_dir
dbms_dir
```

---

## Environment Variables

Environment variables are referenced using `$`.

For example:

```anylog
get $HOME
```

Environment variables can also be created or changed directly from the AnyLog CLI:

```anylog
set $ANYLOG_SITE = plant_1
```

Retrieve the value:

```anylog
get $ANYLOG_SITE
```

Dictionary and environment variables can be used together in CLI commands and scripts.

---

## Concatenating with `+`

In AnyLog, the `+` operator concatenates values.

Numeric variables are also treated as strings when used with `+`. Specifying `.int` or `.float` does not by itself cause arithmetic evaluation.

Given:

```anylog
var1 = hello
var2 = world
var3 = 1
var4 = 3
```

Concatenating strings:

```anylog
AL > !var1 + !var2
"helloworld"

AL > !var1 + " " + !var2
"hello world"
```
### Casting Dictionary Values

CLI commands return values as **strings**. When a dictionary value needs to be used as another data type, it can be cast by adding a type suffix to the variable reference.

For example:

~~~anylog
set port = 7848
set threads = 6
set enabled = true
~~~

The values can be cast when they are used:

~~~anylog
!port.int
!threads.int
!enabled.bool
~~~

Common casts include:

- `.int` — integer
- `.float` — floating-point value
- `.bool` — Boolean value
- `.str` — string

For example:

~~~anylog
set value1 = 10
set value2 = 5

result = python !value1.int + !value2.int
~~~

The value assigned to `!result` is  (type: ```!result```):

~~~text
15
~~~

Without the `python` command, `+` performs string concatenation:

~~~anylog
result = !value1.int + !value2.int
~~~

resulting in:

~~~text
105
~~~

The cast determines how a dictionary value is represented when passed to a command or expression; it does not change the value stored in the dictionary.

---

## The `python` Command

The `python` command evaluates an expression using a subset of Python operations.

Dictionary variables referenced in the expression are replaced with their assigned values.

Using:

```anylog
var3 = 1
var4 = 3
```

integer addition:

```anylog
AL > python !var3.int + !var4.int
4
```

floating-point addition:

```anylog
AL > python !var3.float + !var4.float
4.0
```

or:

```anylog
AL > python !var3.float + !var4.int
4.0
```

Other examples:

```anylog
ip_port = python !ip + ':4028'
```

```anylog
python 'D:/Node/AnyLog-Network/data/watch/'.rsplit('/',1)[0] + '.out'
```

```anylog
new_dir = python !watch_dir.rsplit('/',1)[0] + '.out'
```

```anylog
date_time = python "datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')"
```

Dictionary variables and environment variables can also be combined when constructing strings.

For example:

```anylog
set $ANYLOG_PATH = /status
set host = 127.0.0.1
set port = 5432

address = !host + : + !port + $ANYLOG_PATH
```

The resulting value is:

```text
127.0.0.1:5432/status
```

---

## The `incr` Command

The `incr` command treats a variable as an integer and increments it by the specified value.

For example:

```anylog
AL > k = 3
AL > incr !k 4
7
```

If no increment value is specified, the default increment is `1`.

---

# Running Commands as a Client to the Network

The `run client` command causes the current AnyLog node to act as a **client to the AnyLog network**.

By default, an AnyLog command is executed locally. Adding `run client` sends the command to one or more target nodes and returns the results to the node that issued the request.

Targets can be determined in several ways:

- explicitly by IP address and TCP port,
- from network metadata,
- from the database and table being accessed,
- or dynamically as part of a distributed SQL query.

---

## Run on a Specific Node

Specify the AnyLog TCP IP address and port of the destination node:

```anylog
run client 10.1.1.10:32148 get processes
```

---

## Run on Multiple Nodes

Multiple destinations can be specified:

```anylog
run client (10.1.1.10:32148, 10.1.1.12:32148) get processes
```

The request is sent to each node and their replies are returned to the client node.

---

## Select Nodes Using Metadata

Targets can be discovered from AnyLog metadata.

For example, execute `get status` on all Operator nodes:

```anylog
run client (blockchain get operator bring.ip_port) get status
```

The shorter metadata lookup syntax can also be used:

```anylog
run client (operator bring.ip_port) get status
```

### Filter Nodes by Metadata

For example, select Operators whose `country` attribute contains `US`:

```anylog
run client (operator where [country] contains US bring.ip_port) get status
```

This allows the destination set to be resolved dynamically from the network metadata.

---

## Select Nodes by Database and Table

A request can also be routed to Operators that support a specific logical database and table.

For example:

```anylog
run client (dbms=litsanleandro, table=ping_sensor) get status
```

AnyLog uses the metadata to identify which Operators support the requested data.

The client therefore does not need to know the physical location of the data.

---

## Accept Partial Results

For requests involving multiple nodes, `subset=true` allows AnyLog to return the available results even if some nodes do not reply.

For example:

```anylog
run client (operator bring.ip_port, subset=true) get status
```

A TCP timeout can also be specified:

```anylog
run client (operator bring.ip_port, subset=true, timeout=30) get status
```

In this example:

- `subset=true` allows a partial result.
- `timeout=30` limits the TCP wait time to 30 seconds.

---

## Store Multi-Node Results

Results from a multi-node request can be assigned to a variable.

Use `[]` to organize the replies as a list:

```anylog
nodes_stat[] = run client (blockchain get operator bring.ip_port, subset=true) get status
```

Use `{}` to organize the replies as a dictionary:

```anylog
nodes_stat{} = run client (blockchain get operator bring.ip_port, subset=true) get status
```

---

# Distributed SQL

Distributed SQL is another use of `run client`.

When the destination is empty:

```anylog
run client () sql
```

AnyLog acts as a client to the network and uses the metadata to determine which Operators maintain the requested database and table.

For example:

```anylog
run client () sql plant_data format=table and stat=select timestamp, temperature from sensors
```

AnyLog:

1. Identifies the clusters that maintain the requested table.
2. Identifies the relevant Operators.
3. Distributes the SQL request.
4. Executes the query against the physical data on the Operator nodes.
5. Aggregates the replies.
6. Returns a unified result.

A distributed SQL request can also specify options such as:

```anylog
run client (subset=true, timeout=30) sql
```

See [SQL Commands](./04-%20SQL.md) for distributed SQL syntax, output formats, query options, and examples.

---

# Executing Commands at Startup

AnyLog commands can be executed automatically when the node starts.

Commands can be provided in several ways:

1. As startup arguments.
2. From `.al` scripts executed with `process`.
3. Through deployment scripts.
4. Through configuration policies.

Deployment scripts and configuration policies are commonly used to configure the services that define the role of a node in the network.

See [Deployment Scripts](../03-%20Training%20%26%20Tutorials/05-%20deployment-scripts.md).

---

## Commands as Startup Arguments

Commands can be passed to `anylog.py` as quoted arguments.

Multiple commands are separated using `and`.

For example:

```bash
python3 anylog.py "get connections" and "get processes"
```

---

## Execute a Startup Script

Commands are commonly organized in `.al` script files.

For example, assume `anylog_setup.al` contains:

```anylog
run tcp server where internal_ip=!ip and internal_port=7848 and external_ip=!external_ip and external_port=7848 and bind=false and threads=6

run rest server where internal_ip=!ip and internal_port=7849 and external_ip=!external_ip and external_port=7849 and bind=false
```

The script can be executed when the node starts:

```bash
python3 anylog.py "process !local_scripts/anylog_setup.al" and "get connections"
```

---

# Scripting

AnyLog scripts contain sequences of CLI commands and typically use the `.al` extension.

When an AnyLog node starts, deployment scripts and configuration policies commonly execute the commands that configure:

- node services,
- networking,
- databases,
- metadata synchronization,
- ingestion,
- high availability,
- and other node-specific behavior.

See [Training & Tutorials](../03-%20Training%20%26%20Tutorials) and [Deployment Scripts](../03-%20Training%20%26%20Tutorials/05-%20deployment-scripts.md).

For Docker and Kubernetes-related commands, see [Docker & K8s Commands](../13-%20Support%20%26%20Troubleshooting/04-%20Third-Party%20Support/01-%20Docker%20%26%20K8s%20Commands.md).

---

## `process`

Use `process` to execute a script on the main AnyLog processing thread:

```anylog
process !local_scripts/my-scripts/my_script3.al
```

Commands in the script execute sequentially.

This is useful when later commands depend on earlier commands completing first.

---

## `thread`

Use `thread` to execute a script on a separate thread:

```anylog
thread !local_scripts/my-scripts/my_script3.al
```

A script started with `thread` runs independently from the main processing thread.

When multiple scripts are started using `thread`, they execute independently and are not guaranteed to complete in sequential order relative to one another.

---

# Debugging Scripts

AnyLog provides two primary script debugging modes.

---

## `set debug on`

`set debug on` prints each command and its execution result.

For example:

```anylog
AL > process !local_scripts/my-scripts/script3.al
AL > [] [0002] set debug on --> Success
AL > [] [0003] run tcp server where internal_ip = !ip and internal_port = 7848 and external_ip = !external_ip and external_port = 7848 and bind = false and threads = 6 --> Success
AL > [] [0004] run rest server where internal_ip = !ip and internal_port = 7849 and external_ip = !external_ip and external_port = 7849 and bind = false --> Success
```

Disable debugging using:

```anylog
set debug off
```

This can also be used inside a script to enable debugging only for a particular section.

---

## `set debug interactive`

`set debug interactive` allows the user to control when each command in a script executes.

Interactive debugging cannot execute on the main thread, so the script must be started using `thread`.

For example:

```anylog
AL > thread !local_scripts/my-scripts/script3.al
AL > [Thread-9 (_process_script)] [0001] set debug interactive --> Success
```

Run the next command:

```anylog
AL > next
```

Example:

```text
AL > [Thread-9 (_process_script)] [0003] run tcp server where internal_ip = !ip and internal_port = 7848 and external_ip = !external_ip and external_port = 7848 and bind = false and threads = 6 --> Success
```

The node can be inspected between commands:

```anylog
get connections
```

Example:

```text
Type      External Address Internal Address    Bind Address
---------|----------------|-------------------|-------------|
TCP      |24.5.219.50:7848|192.168.86.29:7848|0.0.0.0:7848|
REST     |Not declared    |Not declared       |Not declared |
Messaging|Not declared    |Not declared       |Not declared |
```

Execute the next script command:

```anylog
next
```

Then inspect the connections again:

```anylog
get connections
```

Example:

```text
Type      External Address Internal Address    Bind Address
---------|----------------|-------------------|-------------|
TCP      |24.5.219.50:7848|192.168.86.29:7848|0.0.0.0:7848|
REST     |24.5.219.50:7849|192.168.86.29:7849|0.0.0.0:7849|
Messaging|Not declared    |Not declared       |Not declared |
```

Other commands can also be used while execution is paused:

```anylog
get processes
get dictionary
blockchain get *
```

Continue executing the rest of the script without pausing:

```anylog
continue
```

To stop using interactive debugging, remove:

```anylog
set debug interactive
```

from the script or use `set debug off` where appropriate.

---

# Script Control Flow

AnyLog scripts support conditional execution and control-flow operations including:

- `if`
- `else`
- `goto`
- labels
- loops
- `wait`
- `end_script`

For example:

```anylog
if $setup_type == query then goto query_node
else goto operator_node

:query_node:
connect dbms test where type=sqlite
end_script

:operator_node:
connect dbms sensor_data where
    type=psql and
    user=anylog and
    password=demo and
    ip=127.0.0.1 and
    port=5432

end_script
```

For complete scripting logic, labels, loops, conditions, and wait operations, see [Conditional Execution & Control Flow](./08-%20Conditional%20Execution%20and%20Control%20Flow.md).

---

# Related CLI Documentation

The CLI documentation is divided into focused sections:

- [Get & Set](./03-%20Get%20%26%20Set.md) — dictionary variables, environment variables, node names, and configuration values.
- [SQL Commands](./04-%20SQL.md) — local and distributed SQL queries.
- [Conditional Execution & Control Flow](./08-%20Conditional%20Execution%20and%20Control%20Flow.md) — conditions, loops, labels, `goto`, and `wait`.
- [Blockchain & Metadata](/docs/08-blockchain-and-metadata/) — metadata policies and metadata management commands.
- [Deployment Scripts](../03-%20Training%20%26%20Tutorials/05-%20deployment-scripts.md) — configuring node services using AnyLog scripts.
- [Docker & K8s Commands](../13-%20Support%20%26%20Troubleshooting/04-%20Third-Party%20Support/01-%20Docker%20%26%20K8s%20Commands.md) — container deployment and troubleshooting.

A useful way to think about CLI execution is:

```text
Local command
    │
    └──► Execute on this node

run client ...
    │
    └──► Act as a client to the AnyLog network
             │
             ├──► Explicit node
             ├──► Multiple nodes
             ├──► Metadata-selected nodes
             └──► Operators selected by the requested data
```