---
title: "CLI Overview"
description: "The AnyLog command prompt, running commands on startup and on peer nodes, and CLI-level operations like the dictionary, incr, and the python command."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-26 | Ori Shadmon    | Reorganized CLI section: merged content previously split between "07- CLI" and "99- Commands & CLI"; moved control-flow (if/goto/for loop/wait) to its own "Conditional Execution & Control Flow" page | |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
--->

# The AnyLog CLI

## Overview

Each node offers a Command Line Interface (CLI). The CLI allows users to interact with the program via the command line
or terminal.

The CLI is a text-based interface where users can enter commands to execute various functions or operations on the
AnyLog node or peer nodes.

**Notes**:
1. If AnyLog is executed as a background process, the CLI functionality is disabled. See details in the background
deployment section.
2. Most commands can be executed via REST using POST and/or GET.

## The Command Prompt

The node's CLI includes a prompt and by default is as follows:
```anylog
AL >
```
Users can change the node name using the command **set node name** to associate a node with a unique name.
The node name extends the CLI prompt. For example the following command changes the prompt:
```anylog
AL >  set node name Operator_3
AL Operator_3 >
```
See [Set node name](./03-%20Get%20&%20Set.md#set-node-name).

A prompt extended by a plus (+) sign indicates a message in the buffer queue.
For example:
```anylog
AL +>
```

Retrieve the message using the following command:
```anylog
get echo queue
```

## Basic Commands

The CLI can operate on values maintained in the local dictionary. Details on the dictionary are available in
[Get and Set Reference](./03-%20Get%20&%20Set.md#get-dictionary).

### Concatenating with `+`

In AnyLog, the `+` symbol concatenates strings by default — including numeric variables, which are treated as
strings unless a data type is specified with a `.int` or `.float` suffix (e.g. `!var.int`). On its own, `+` always
concatenates rather than performing arithmetic, even when a `.int`/`.float` suffix is present; to actually add
values as numbers rather than joining them as text, prefix the whole expression with the `python` command (see
[below](#the-python-command)).

Given the following values:
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

# a word + a number is still concatenation
AL > !var1 + !var3.int
"hello1"
```

### The `python` Command

Prefixing an expression with the `python` command evaluates it using a subset of Python operations, with minor
differences from the Python language itself — this is what turns a `+` between numeric variables into real
arithmetic instead of string concatenation. When these commands are executed, if a key from the dictionary is
specified, it is replaced with its assigned value.

Continuing from the values above (`var3 = 1`, `var4 = 3`):
```anylog
# without "python", + still just concatenates
AL > !var3.int + !var4
"13"

AL > !var3.int + !var4.int
"13"

# with "python", + performs actual addition
AL > python !var3.int + !var4.int
4

AL > python !var3.float + !var4.float
4.0

AL > python !var3.float + !var4.int
4.0
```

Other examples:
```anylog
ip_port = python !ip + ':4028'
python 'D:/Node/AnyLog-Network/data/watch/'.rsplit('/',1)[0] + '.out'
new_dir = python !watch_dir.rsplit('/',1)[0] + '.out'
date_time = python "datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')"
```

You can also concatenate set environment variables (`$MY_VAR`) alongside dictionary variables. In the example below,
the variable **c** is `127.0.0.1:5432/status`:
```anylog
export PATH=/status
a = 127.0.0.1
b = 5432
c = !a + : + !b + $PATH
```

### The `incr` Command

The `incr` command considers a variable as an integer and returns the result of adding a specified value to the
variable. If a value is not specified, it is considered to be 1.

```anylog
AL > k = 3
AL > incr !k 4
7
```

## Executing on peer nodes

By default, an AnyLog command is executed on the local node. Adding the keywords `run client` executes the command on
one or more target nodes; the command output is returned and displayed on the node from which the command was issued.

Target nodes can be specified in 3 different ways:

* By their IP and Port.

```anylog
# on a single node
run client (10.1.1.10:32148)

# against multiple nodes
run client (10.1.1.10:32148,10.1.1.12:32148)
```

* By a lookup from the metadata.

```anylog
# all operators
run client (blockchain get operator bring.ip_port) get status

# only operators in the United States
run client (operator where [country] contains US  bring.ip_port)
```

* SQL command without knowing where the data actually resides

```anylog
run client () sql

# run against the entire network - accept subset of results & a timeout of 30 seconds
run client (subset=true, timeout=30) sql
```

In addition to stating where data resides, the request can include a TCP timeout - in seconds (i.e. `timeout=30`), and
whether to accept only a subset of results (i.e. `subset=true`) if not all the nodes return a reply.

The results of a `run client` call against multiple nodes can be organized as a list or as a dictionary, depending on
how the assignment is written:

```anylog
nodes_stat[] = run client (blockchain get operator bring.ip_port, subset = true) get status
nodes_stat{} = run client (blockchain get operator bring.ip_port, subset = true) get status
```

## Scripting

As described in [section 3](../03-%20Training%20&%20Tutorials), when an AnyLog agent is brought up, a series of
commands, defined through [deployment scripts](../03-%20Training%20&%20Tutorials/05-%20deployment-scripts.md) and
configuration policies, define the node to be a part of the network with the correct services and database associated
with it.

When a user defines / creates their own script — see [Docker & K8s Commands](../13-%20Support%20%26%20Troubleshooting/04-%20Third-Party%20Support/01-%20Docker%20%26%20K8s%20Commands.md)
for support — they can then run their script in 2 ways:

* `process` - runs the script on the main AnyLog thread.

```anylog
process !local_scripts/my-scripts/my_script3.al
```

* `thread` - runs the script on its own thread.

```anylog
thread !local_scripts/my-scripts/my_script3.al
```

The distinction: when running a script with `process` (e.g. a script calling other scripts), the commands run in
consecutive order, and the process runs on the main thread. `thread` does not run on the main thread but in its own
sub-thread; when running multiple scripts this way, they will not run in consecutive order relative to each other.

### Debugging Scripts

There are 2 ways to debug scripts in AnyLog.

* `set debug on` - each command that follows is printed including the execution result.

```anylog
AL > process !local_scripts/my-scripts/script3.al
AL > [] [0002] set debug on --> Success
AL > [] [0003] run tcp server where internal_ip = !ip and internal_port = 7848 and external_ip = !external_ip and external_port = 7848 and bind = false and threads = 6 --> Success
AL > [] [0004] run rest server where internal_ip = !ip and internal_port = 7849 and external_ip = !external_ip and external_port = 7849 and bind = false --> Success
```

* `set debug interactive` - a debugging module that allows the user to control when each command in the script runs.
Unlike `set debug on`, `set debug interactive` cannot be run on the main thread, and thus must be run using the `thread` 
execution command.

```anylog
AL > thread !local_scripts/my-scripts/script3.al
AL > [Thread-9 (_process_script)] [0001] set debug interactive --> Success
AL > next
AL > [Thread-9 (_process_script)] [0003] run tcp server where internal_ip = !ip and internal_port = 7848 and external_ip = !external_ip and external_port = 7848 and bind = false and threads = 6 --> Success
AL > get connections

Type      External Address Internal Address   Bind Address
---------|----------------|------------------|------------|
TCP      |24.5.219.50:7848|192.168.86.29:7848|0.0.0.0:7848|
REST     |Not declared    |Not declared      |Not declared|
Messaging|Not declared    |Not declared      |Not declared|

AL > next
AL > [Thread-9 (_process_script)] [0004] run rest server where internal_ip = !ip and internal_port = 7849 and external_ip = !external_ip and external_port = 7849 and bind = false --> Success
AL > get connections

Type      External Address Internal Address   Bind Address
---------|----------------|------------------|------------|
TCP      |24.5.219.50:7848|192.168.86.29:7848|0.0.0.0:7848|
REST     |24.5.219.50:7849|192.168.86.29:7849|0.0.0.0:7849|
Messaging|Not declared    |Not declared      |Not declared|

AL > next
AL >
```

> To stop debugging simply remove `set debug [on/interactive]` from the top of the script, or specify `set debug off`
> when trying to debug a subsection of a script.

## Next: scripting and control flow

For conditional logic, labeled sections, loops, and the wait command, see
[Conditional Execution & Control Flow](./08-%20Conditional%20Execution%20and%20Control%20Flow.md).