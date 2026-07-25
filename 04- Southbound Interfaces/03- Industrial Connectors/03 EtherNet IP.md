---
title: "EtherNet/IP"
description: "Configure AnyLog as an EtherNet/IP client to pull data from industrial PLCs and controllers continuously."
layout: page
source_path: "03 EtherNet IP.md"
---

<!---
### 📜 Change Log
 **Date**   | **Name** | **Change**       | **Version** |
 |------------|--|------------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
--->


# EtherNet/IP

EtherNet/IP (Ethernet Industrial Protocol) is an industrial network protocol built on the Common Industrial Protocol (CIP) that enables communication between PLCs, sensors, actuators, and control systems over standard Ethernet. AnyLog can act as an EtherNet/IP client, pulling data from any EtherNet/IP device and streaming it into local databases.

## The EtherNet/IP Structure

EtherNet/IP organizes industrial automation data through a set of well-defined CIP (Common Industrial Protocol) objects, 
which represent device attributes, configurations, and runtime data. Unlike OPC UA's tree-based model, EtherNet/IP uses a flat, 
object-oriented structure where each device exposes standard or vendor-specific classes, instances, and attributes. 
These are accessed using CIP messaging over Ethernet.

Each class (such as Identity Object, Assembly Object, or Connection Object) may contain multiple instances, and each instance 
can expose multiple attributes, forming a structured view of the device's capabilities and status. 
While the structure is not hierarchical like OPC UA, it provides a standardized way to navigate and interact with device data.

The `get etherip struct` command explores the structure by querying supported classes and retrieving their instances and attributes. 
This provides insight into the connected PLC or device, including program tags and system-level data.

The EtherNet/IP structure is explored with the following command:


```anylog
get etherip struct where url = [connect string] and user = [username] and password = [password] and ...
```
This command enables users to query both system-level and user-defined tags, making it easier to explore and interact with a PLC’s data structure over EtherNet/IP.

### Command Variables

| Keyword     | Details    |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `url`       | The IP address of the target PLC or EtherNet/IP device.                                                                                |
| `slot`      | The slot number of the target controller (used in multi-slot chassis).                                                                 |
| `user`      | Username, if the PLC requires authentication.                                                                                          |
| `password`  | Password for authentication.                                                                                                           |
| `limit`     | Limit the number of tags or objects returned in the response.                                                                          |
| `prefix`    | Limit the tags to a path that satisfies the prefix string.                                                                             |
| `output`    | The target for the output stream (stdout or a file name).                                                                              |
| `format`    | The format of the output (see details below).                                                                                          |
| `target`    | The variables in the 'blockchain insert commands'. This option is used with 'format = policy' to generate 'blockchain insert' commands |
| `schema`    | A boolean value. If set to True, output includes, for each tag, the table's schema.                                                    |
| `frequency` | Specifying the reading frequency in Hz, with **format = run_client**.                                                                  |
| `name`      | Specifying a process name when with **format = run_client** option.                                                                    |

Format options:
* tree - the OPC-UA tree structure (default).
* policy - generating a policy representing the tag. If target is specified, output is "blockchain insert" command for every policy.
* get_value - generating a [get plc value](#the-get-plc-values-command) command with the tags visited in the **get plc struct** command.
* run_client - generating a [run plc client](#the-run-plc-client-command) command with the tags visited in the **get plc struct** command.

### Traversal examples

```anylog
# Browse all tags, show current values
get etherip struct where url = 127.0.0.1 and read = true

# Generate a get plc values command
get etherip struct where url = 127.0.0.1 and format = get_value

# Generate a run plc client command
get etherip struct where url = 127.0.0.1 and format = run_client and frequency = 1 and name = etherip_reads and dbms = my_dbms

# Generate blockchain insert commands for all tags (includes schema)
get etherip struct where url = 127.0.0.1 and format = policy and schema = true \
    and dbms = my_dbms and target = "local = true and master = !master_node" \
    and output = !tmp_dir/my_file.out
```

---

## Read tag values

```anylog
get plc values where type = etherip and url = [connect string] and node = [tag name]
```

Options:

| Option | Description |
|---|---|
| `node` | One or more tag names |
| `nodes` | Comma-separated list of tag names in square brackets |

Examples:
```anylog
get plc values where type = etherip and url = 127.0.0.1 \
    and node = CombinedChlorinatorAI.PV and node = STRUCT.Status

# List format
get plc values where type = etherip and url = 127.0.0.1 \
    and nodes = ["CombinedChlorinatorAI.PV", "STRUCT.Status"]
```

## The Run PLC Client Command

The command **run plc client*** pulls data from the PLC continuously and streams the data into a database on the local node:
```anylog
run plc client where type = etherip and name = [unique name] and url = [connect string] and frequency = [frequency] and dbms = [dbms name] and table = [table name] and node = [node id]]
```
 
The following tables summarizes the command variables:

| keyword   | Details                                                                                      |
|-----------|----------------------------------------------------------------------------------------------|
| name      | A unique connection name.                                                                    |
| url       | The url specifies the endpoint of the OPC UA server.                                         |
| user      | the username required by the OPC UA server for access.                                       |
| password  | the password associated with the username.                                                   |
| frequency | Read frequency in seconds or a fraction of seconds using hz (i.e.: 10 hz).                   |
| node      | ID of one or multiple nodes that their value is retrieved.                                   |
| nodes     | Providing a list of nodes, separated by comma, within square brackets.                       |
| policy    | If nodes are not specified on the CLI, the policy determines the nodes and the table to use. |
| dbms      | The database to host the data (if not specified in a policy).                                |
| table     | The table to host the data (if not specified in a policy).                                |
| topic     | If data is processed through the local broker.                                               |


Example 1 - listing individual tags:
```anylog
run plc client where type = etherip and name = etherip_reads and url = 127.0.0.1 and frequency = 1 and dbms = my_dbms and node = FreeChlorinatorAI.PV and node = CombinedChlorinatorAI.PV
```
Example 2 - providing a list of tags:
```anylog
<run plc client where type = etherip and name = etherip_reads and url = 127.0.0.1 and frequency = 1 and dbms = my_dbms and nodes =
["BOOL","SINT","INT","DINT","REAL","STRING","STRUCT.Temp","STRUCT.Status","ARRAY_INT","ARRAY_BOOL","ARRAY_STRING","TIMER.ACC"
,"TIMER.PRE","COUNTER.ACC","COUNTER.PRE","DATE_TIME","ATSNormalRdyDI","CombinedChlorinatorAI.PV","FreeChlorinatorAI.PV"]>
```

Notes: 
1. Multiple clients can be declared on the same node.
2. Each row is added with 2 columns:
   * Timestamp - representing the earliest source_timestamp of the values considered (if source_timestamp is missing, the server_timestamp is considered).
   * Duration - the number of milliseconds between the earliest timestamp and the latest timestamp that were considered in the values that were retrieved from the PLC.


---

## Policy-based tag management

For large EtherNet/IP deployments, generate policies for each tag and publish them to the blockchain. This lets AnyLog automatically map incoming data to the correct tables without specifying nodes inline.

### 1. Generate and publish policies

```anylog
# Generate policy file (includes schema if schema = true)
get etherip struct where url = 127.0.0.1 and format = policy and schema = true \
    and dbms = my_dbms and target = "local = true and master = !master_node" \
    and output = !tmp_dir/my_file.out

# Publish to blockchain
process !tmp_dir/my_file.out
```

The generated tag policy looks like:
```json
{"tag": {
    "protocol":  "etherip",
    "ns":        0,
    "dbms":      "my_dbms",
    "table":     "t101",
    "datatype":  "boolean",
    "node_sid":  "BOOL",
    "id":        "0e17856bdb914cdfe338eff3485ef366",
    "date":      "2025-05-04T18:07:54.695893Z",
    "ledger":    "local"
}}
```

If `schema = true`, the output also includes a `CREATE TABLE` statement for each tag.

### 2. Generate and run the data pull command

```anylog
# Generate run_client command file (table derived from policies — no table= needed)
get etherip struct where url = 127.0.0.1 and format = run_client \
    and frequency = 1 and name = etherip_reads and dbms = my_dbms \
    and output = !tmp_dir/my_run_cmd.out

# Execute
process !tmp_dir/my_run_cmd.out
```

This pulls data continuously and assigns each tag's values to the correct table based on the published policies.
