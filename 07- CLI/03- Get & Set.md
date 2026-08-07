---
title: "Get and Set Reference"
description: "Reference for AnyLog's get and set commands — node status, dictionary, resource monitoring, configuration, and the node dictionary."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-26 | Ori Shadmon    | Consolidated "get-cmds.md", "node-status commands.md", and the Set/Reset/Get tables from "01 Anylog Commands.md" into a single reference; `test node`/`test network` moved to Test & Network Validation | |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
--->

AnyLog's `get` commands provide a unified interface for inspecting every aspect of a running node — its services, data
volumes, resource usage, configuration, and connectivity. `set` and `reset` commands configure variables and runtime
behavior. All of these commands can be issued locally on the CLI or remotely via `run client`.

---

## The node dictionary

Every node maintains a dictionary that associates keys with values. When a node is initialized, some keys are
preassigned with values. Users and processes can assign new values to new or existing keys.

Assigning a value to a key is done with the following call:
```anylog
[key] = [value]
```
Or use the set command:
```anylog
set [key] = [value]
```

The following example assigns a path to the key dbms_dir:
```anylog
dbms_dir = D:\AnyLog-Code\AnyLog-Network\data\dbms
```

Use the following command to delete an assignment:
```anylog
[key] = ""
```
Or:
```anylog
set [key] = ""
```

To retrieve the value assigned to a key, prefix the key name with an exclamation point:
```anylog
![key]
```
Or use the get command:
```anylog
get ![key]
```

### get dictionary

```anylog
get dictionary                          # all key-value pairs
get dictionary where format = json      # JSON output
get dictionary _dir                     # keys containing substring '_dir'
!my_key                                 # retrieve a single value on the CLI
get !my_key                             # retrieve via REST or remote CLI
```

### get env var

Lists OS-level environment variables:

```anylog
get env var
get env var where format = json
$MY_VAR                                 # retrieve a single env var
```

---

## Node status

### get status

Returns whether the node is running, its assigned name, and optional extra metrics:

```anylog
get status
get status where format = json
```

Extend the response to include monitored variables:
```anylog
get status where include = !!cpu_percent and include = !!disk_free
```

Example response:
```json
{
  "assigned_name": "bachelor-query@172.233.208.212:32348",
  "status": "running",
  "profiling": false
}
```

Issue against a peer node:
```anylog
run client 10.0.0.78:7848 get status
```

### get processes

Lists all background services, their status, and key configuration details. See [Background Processes](02-%20Background%20Processes.md).

```anylog
get processes
get processes where format = json
```

### get connections

Returns the IPs and ports the node is listening on:

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

A static IP:Port (rather than `0.0.0.0`) in the Bind column means the service is bound to that specific address.

### get platform info

Returns OS type, version, node name, and processor type:

```anylog
get platform info
```

### get node name

Return the node name including the IP and Port that identifies the node. The node name is assigned using
[set node name](#set-node-name). If a name was not assigned, the name returned is "AnyLog".

---

## Set command

The ***set*** command allows setting variables and configuration parameters.

| Option | Explanation |
|---|---|
| `set node name [node name]` | Declare the node name. The name appears on the local CLI. |
| `set query mode` | Setting execution instructions for issued queries. |
| `set query log on/off` | Enable/Disable a log to record the executed queries. |
| `set query log profile [n] seconds` | Applying the Query Log to queries with execution time higher than the threshold. |
| `set rest log on/off` | Enable/Disable a log to record the processed REST commands. Retrieved with `get rest log`. |
| `set debug [on/off]` | Displays the executed commands processed in scripts. |
| `set mqtt debug [on/off]` | Displays the MQTT messages and their processing status. |
| `set debug interactive` | Waits for the user interactive command `next` to move to the next command. |
| `set threads pool [n]` | Creates a pool of worker threads that distributes query processing to multiple threads. |
| `set echo queue [on/off]` | Creates a queue to contain echo commands and messages. |
| `set authentication [on/off]` | Enable / Disable user and message authentication. Default value is ON. |
| `set encryption [on/off]` | Enable / Disable encryption of TCP messages. Default value is OFF. |
| `set compression [on/off]` | Enable / Disable compression of data messages. Default value is OFF. |
| `set local password = [password]` | Password to protect sensitive information kept on the node (private keys, user passwords). |
| `set private password = [password] [in file]` | Password of the private key, with an optional [in file] to keep an encrypted copy on the filesystem. |
| `set anylog home [absolute path]` | Declare a path to the AnyLog data files. |
| `set traceback [on/off]` | Print the code path with every call to the error log. |
| `set reply ip = [ip]` | Set the IP address for a reply message. |
| `set self ip = [ip]` | Set the IP address when the sender and receiver are the same node. |
| `set consumer mode = [mode]` | Change the consumer mode of operation: `active` or `suspend`. |
| `set rest timeout [time and time-unit]` | Sets a time limit for a REST reply. If limit is 0, the process waits without timeout. |
| `set data distribution where ...` | Define how data is distributed to the storage nodes — see [below](#set-data-distribution). |
| `set streaming condition` | Declare a condition on streaming data. |
| `set output table width [table width]` | Configure the display width of a table in a report. |
| `set internal ip with [interface_name]` | Set the node's internal IP address based on a network interface (NIC). |

### Set node name

Declare the node name. The name appears on the CLI prompt.
Example:
```anylog
set node name Operator_3
```
The CLI prompt will appear as:
```anylog
AL Operator_3 >
```
Whereas **AL** stands for AnyLog and **Operator_3** is the assigned name.

Use the following command to reset the node name:
```anylog
set node name ""
```

### Set query mode

The query mode sets a cap on query execution at the Operator Node by setting a limit on execution time, data volume transferred, or both.

| Param | Explanation |
|---|---|
| `timeout` | Limit execution on each server by the provided time limit. |
| `max_volume` | Limit data volume returned by each participating operator. |
| `send_mode` | `all` returns an error if any participating server is not connected; `any` sends the query only to connected servers. Default is `all`. |
| `reply_mode` | `all` returns an error if any participating server did not reply after timeout; `any` returns results using the available data after timeout. Default is `all`. |

### Set data distribution

Define the destination of data based on the database and table assigned to the data. Force a publisher to a defined distribution of the data.

Usage:
```anylog
set data distribution where dbms = [dbms_name] and table = [table_name] and dest = [ip:port]
```
- `dbms` — the database associated with the data
- `table` — the table associated with the data
- `dest` — the destination ip and port (one or more)

Example:
```anylog
set data distribution where dbms = lsl_demo and table = * and dest = 10.12.32.148:2048 and dest = 10.181.231.18:2048
```

Removal of an existing distribution is done by adding `remove = true`:
```anylog
set data distribution where dbms = [dbms_name] and table = [table_name] and remove = true
```
Example:
```anylog
set data distribution where dbms = lsl_demo and table = ping_sensor and remove = true
```

View the distribution definitions using the command:
```anylog
get publisher distribution
```

---

## Reset command

The ***reset*** command allows resetting variables and configuration parameters.

| Option | Explanation |
|---|---|
| `reset [event/error/file/query] log` | Deletes the log entries in the specified file. |
| `reset query timer` | Reset the query timer. |
| `reset echo queue` | Reset the queue. |
| `reset echo queue where size = [n]` | Resets the queue and sets its size to maintain the last n messages (1–100). |
| `reset reply IP` | Identify a reply IP to be used by the replying node. |
| `reset self IP` | Identify an IP to be used when sender and receiver are the same node. |
| `reset streaming conditions` | Remove one or more streaming conditions. |

---

## Data monitoring

### get rows count

Lists tables and their row counts across local databases:

```anylog
get rows count
get rows count where dbms = my_dbms
get rows count where dbms = my_dbms and table = my_table
get rows count where dbms = my_dbms and format = json
get rows count where dbms = my_dbms and table = my_table and group = table
```

- `group = table` — aggregates counts per table rather than per partition

### get data nodes

Lists all Operator nodes in the network and the tables each one hosts:

```anylog
get data nodes
```

### get operator

Returns data ingestion details for the local Operator service:

```anylog
get operator
get operator stat format = json
get operator inserts
get operator summary
get operator config
```

### Get servers

The ***get servers*** command returns information on the Operators hosting data.

Usage:
```anylog
get servers where company = [company name] and dbms = [dbms name] and table = [table name] bring [key string]
```
The ***where*** condition and ***bring*** keyword are optional. If ***where*** is used, the process is satisfied with
Operators associated with the company, dbms, and table values provided — if a value is omitted, an asterisk (`*`) is
assumed. The ***bring*** command determines the values retrieved from the policies; if omitted, the IP and Port of
the servers are retrieved.

Examples:
```anylog
get servers
get servers where dbms = lsl_demo and table = ping_sensor
get servers where company = anylog and dbms = lsl_demo and table = ping_sensor
get servers where company = anylog bring [operator][ip] : [operator][port] --- [operator][id]
```

---

## Resource monitoring

These commands require <a href="https://psutil.readthedocs.io/en/latest/" target="_blank">psutil</a> to be installed on
the node.

### Memory, CPU, disk

```anylog
get memory info             # RAM usage
get cpu info                # CPU details
get cpu temperature         # CPU temperature (if supported)
get ip list                 # all IP addresses on the node
get disk usage [path]       # disk usage at path
get disk free [path]        # free space at path
get disk total [path]       # total capacity at path
get disk percentage [path]  # usage as a percentage
```

### get os process

```anylog
get os process              # AnyLog process (same as get os process anylog)
get os process anylog       # CPU and memory for the AnyLog process
get os process [pid]        # info for a specific PID
get os process all          # all processes (takes ~1 second for CPU measurement)
get os process list         # process names and PIDs
```

### get node info

Maps to psutil calls and returns structured system metrics. Values can be stored in a database table or sent to an
aggregator node.

```anylog
get node info cpu_percent
get node info cpu_times
get node info cpu_times_percent
get node info getloadavg
get node info swap_memory
get node info disk_io_counters
get node info disk_io_counters read_count
get node info net_io_counters
get node info net_io_counters bytes_recv
```

Store directly into a database table:
```anylog
get node info cpu_percent into dbms = monitor and table = cpu_percent
```

### Get pool info

A group of commands that provides statistical information on groups of threads leveraged by different processes.
Each returns, for each thread in the group, its current status and usage.

Usage:
```anylog
get [group name] pool where details = [true/false] and reset = [true/false]
```
* The ***where*** condition is optional.
* ***details*** provides additional details on the usage of each thread.
* ***reset***, if used, sets the pool statistics to 0.

Group names:

| Group Name | Usage |
|---|---|
| query | Threads supporting queries |
| operator | Threads supporting the operator process |
| rest | Threads supporting communications with applications |
| tcp | Threads supporting communications with network peers |
| msg | Threads supporting the message broker functionality |

Example 1:
```anylog
get tcp pool
```
returns:
```anylog
TCP Pool with 6 threads: [1, 1, 0, 0, 0, 0]
```
Meaning 2 of the 6 threads are busy, 4 are at rest.

Example 2:
```anylog
get query pool where details = true
```
Lists the threads and, for each thread: Status (0 = at rest, 1 = busy), Calls (number of times the thread was called), and Percentage of usage.

### Get DNS name

Returns the name assigned to an IP address using the Domain Name System (DNS).

Usage:
```anylog
get dns name where ip = [local or external ip]
```
If IP is not provided, the node's external (global) IP is used and the global DNS is returned.

Examples:
```anylog
get dns name
get dns name where ip = 24.5.219.50:7849
get dns name where ip = !ip
get dns name where ip = !external_ip
```

By default, the local dictionary assigns IPs and DNS values to the following keys:

| Key | Value |
|---|---|
| ip | The local ip value |
| external_ip | The global ip value |
| dns | The local DNS |
| external_dns | The global DNS |

The following commands can use IP values or DNS names interchangeably: `run tcp server`, `run rest server`, `run message broker`.

---

## Continuous monitoring

`continuous` repeats one or more monitoring commands on a fixed interval. Press any key to stop.

```anylog
continuous [seconds] [command1], [command2], ...
```

| Command | Description |
|---|---|
| `cpu` | System CPU usage |
| `cpu anylog` | AnyLog process CPU usage |
| `cpu [process]` | Named process CPU usage |
| `get cpu usage` | Per-CPU breakdown |
| `get operator` | Operator status |
| `get operator summary` | Operator summary |
| `get streaming` | Streaming buffer status |
| `get query pool` | Query thread pool |
| `get operator pool` | Operator thread pool |
| `get rest pool` | REST thread pool |
| `get tcp pool` | TCP thread pool |
| `get msg pool` | Message broker thread pool |

Examples:
```anylog
continuous cpu, cpu anylog, get operator summary, get streaming

continuous 10 run client () sql my_dbms select max(timestamp), count(*) from my_table where timestamp >= NOW() - 5 minutes
```

---

## Aggregator node

An aggregator node collects status pushed from multiple nodes and provides a unified view — without requiring a database.

### On each monitored node (via scheduler):

```anylog
schedule name = node_status and time = 15 seconds task node_status = get status where format = json
schedule name = monitor_node and time = 15 seconds task run client [aggregator_ip:port] monitor Nodes where info = !node_status
```

### On the aggregator node:

```anylog
get monitored              # list all monitored topics
get monitored Nodes        # status per node for topic 'Nodes'
reset monitored Nodes      # clear the node list for a topic
```

### monitor command

```anylog
monitor [topic] where ip = [node-ip] and name = [node-name] and info = [json-struct]
```

Example:
```anylog
monitor operators where ip = 127.0.0.1 and name = dmc-usa and info = {"total events": 1000, "events per second": 10}
```

---

## Security and encryption

| Option | Information provided |
|---|---|
| `get public key` | The node's public key. |
| `get public key using keys_file = [file name]` | Retrieves the public key from the specified file. |
| `get permissions` | The permissions for the current node using the node's public key. |
| `get permissions for member [member id]` | The permissions for the member identified by its public key. |
| `get authentication` | Returns ON or OFF depending on the current status. |
| `get encryption` | Returns ON or OFF depending on the current status. |
| `get compression` | Returns ON or OFF depending on the current status. |

---

## Other useful get commands

```anylog
get synchronizer            # blockchain sync status
get metadata version         # current metadata version ID
get scheduler                # scheduler status
get scheduler 1              # specific scheduler status
get streaming                # streaming buffer status and thresholds
get rest server info         # REST service configuration
get rest calls                # REST request statistics
get local broker              # message broker status
get msg clients                # active message client subscriptions
get blobs archiver             # blobs archiver status
get distributor                 # HA distributor status
get consumer                    # HA consumer status
get publisher                   # publisher status
get network info                # network-level info
get version                      # AnyLog version
get databases                    # connected local databases
get tables where dbms = [dbms]   # tables in a database
get columns where dbms = [dbms] and table = [table]  # columns in a table
get threads                      # threads executing user scripts
get hostname                     # name assigned to the node
get git [version/info] [path]    # git commit info for the AnyLog-Network directory
get queries time                 # query execution time statistics (set query log profile [n] seconds)
get watch directories            # list of watch directories on the node
get metadata info                # summary info on the metadata: version and time since last update
get database size [database name]  # size of the named database in bytes
get node id                      # unique identifier of the node
get hardware id                  # unique identifier of the hardware
get mcp status                   # info on the MCP clients connected to the node
get node resources               # info on resources available to the node
get installed packages           # list of installed Python packages
```

For the commands to test connectivity and validate node/network health (`test node`, `test network`, `test process`, etc.),
see [Test & Network Validation](06-%20Test%20&%20Node%20Status.md).
