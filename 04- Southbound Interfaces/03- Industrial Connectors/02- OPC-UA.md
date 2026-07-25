---
title: OPC-UA
description: Configure AnyLog as an OPC-UA client to explore a server, read values, pull data continuously, apply aggregations, and manage tags with policies.
layout: page
source_path: "OPC UA Integration.md"
---
<!--
## Changelog
- 2026-04-17 | Created document (as opcua.md)
- 2026-07-14 | Merged the two overlapping OPC-UA docs (opcua.md and OPC UA Integration.md) into this single file.
              Backbone is OPC UA Integration.md — unlike the equivalent EtherNet/IP merge, it was the more
              complete of the two here, not the terser one. It covers two options opcua.md's table omitted
              entirely (`attributes`, `append`), explains the `validate` option's exact failure-handling
              behavior (absent from opcua.md), explains the address-space tree model itself (Objects/Types/Views
              folders), and has a fuller aggregations walkthrough (shows the actual query result, includes a
              `get aggregations config` step) and a richer, more concrete policy example. Nothing in opcua.md
              was found to be missing from this file, so nothing was folded forward from it — it's fully
              superseded rather than merged from. Kept as one file rather than split into an explainer +
              example (contrast with UNS/Authentication): the worked-example sections here (aggregations,
              policy-based tag management) are short, tightly-scoped walkthroughs proportional to the rest of
              the page, not a separate large scenario — same shape as DNP3.md and etherip.md, both of which
              keep their policy-management walkthrough inline.
- 2026-07-24 | `04 OPC UA Integration.md` resurfaced as a separate upload — checked it against this file line by
              line and confirmed it's the terser predecessor described above (shorter intro, missing `attributes`/
              `append` options, no validate-failure-behavior explanation, a 5-step aggregations walkthrough vs.
              this file's 7-step version with the actual query output shown). Nothing in it was missing here, so
              it's excluded rather than re-merged, consistent with the note above.
-->

OPC Unified Architecture (OPC UA) is a robust, platform-independent industrial communication protocol with built-in
security (encryption, authentication, and access control), widely used in industrial automation for secure and reliable
data exchange between devices, systems, and applications. Designed as an evolution of the OPC Classic standard, it
supports real-time data access, historical data retrieval, and event notifications, making it ideal for industrial IoT
and Industry 4.0 environments.

AnyLog can act as an OPC-UA client, pulling data from any OPC-UA server and streaming it into local databases.

---

## Explore the server

### Get namespaces

In OPC UA, namespaces organize and uniquely identify nodes in the address space of a server. Each namespace is assigned
a unique index (e.g. `ns=0`, `ns=1`, `ns=2`) used in Node IDs — for example `ns=1;s=TemperatureSensor`.

```anylog
get opcua namespace where url = [connect string] and user = [username] and password = [password]
```

Details:
* `url` — the endpoint of the OPC UA server.
* `user` — the username required by the OPC UA server for access.
* `password` — the password associated with the username.

Example:
```anylog
get opcua namespace where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer
```

### Traverse the address space tree

The OPC UA tree organizes the server's address space into a hierarchical model resembling a file system. At the root
level, predefined folders like **Objects**, **Types**, and **Views** provide entry points into the address space. The
**Objects** folder contains application-specific nodes (devices, sensors, systems), while the **Types** folder defines
the structure and behavior of nodes (ObjectTypes, VariableTypes, DataTypes). Each node can have child nodes, creating a
parent-child hierarchy.

The `get opcua struct` command navigates the tree and produces different outputs based on the command variables. The
traversal starts from the root, unless a node is specified to serve as the root.

```anylog
get opcua struct where url = [connect string] and [options]
```

| Option | Description |
|---|---|
| `url` | OPC UA server endpoint. |
| `user` / `password` | Credentials required by the server. |
| `node` | Override the root node by providing a node ID (e.g. `ns=6;s=MyObjectsFolder`). |
| `type` | Filter by node type: `Object`, `Variable`, etc. If not specified, all types are visited. |
| `attributes` | Attribute names to consider, or `*` for all. |
| `class` | Filter the traversal to nodes in the listed class. |
| `depth` | Limit traversal by depth. |
| `limit` | Limit traversal by number of nodes visited. |
| `output` | Target for the output stream (`stdout` or a file name). |
| `append` | If output is a file, a `true` value appends to it (default `false`). |
| `format` | Output format (see below). |
| `validate` | If `true`, reads each node's value to confirm it is readable (see below). |
| `schema` | If `true`, includes the table schema for each tag. |
| `dbms` / `table` | Used when generating `run_client` or `policy` output. |
| `frequency` | Used when generating `run_client` output. |
| `target` | Variables for the `blockchain insert` commands (used with `format = policy`). |

**Format options:**

| Format | Output |
|---|---|
| `tree` | OPC-UA tree structure (default). |
| `path` | Full path strings for each node. |
| `stats` | Count of entries per class. |
| `get_value` | Generates [get opcua value](#read-node-values) commands for the visited nodes. |
| `run_client` | Generates [run opcua client](#continuous-data-pull) commands for the visited nodes. |
| `policy` | Generates a policy per tag; combine with `target` for `blockchain insert` commands. |

**The validate option:**
* The default value is `false`.
* If set to `true`, the value of each considered node is read during traversal.
* If the read fails:
  * When `format` is `get_value` or `run_client`, the node is not included.
  * In other cases, the output includes a `validate` attribute assigned `success` or `failure`.
  * The summary chart includes a counter for the number of nodes that failed to generate a value.

**Traversal examples:**

```anylog
# Browse from root, limit 10 nodes
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and limit = 10

# Direct the output to a file
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = !prep_dir/opcua_tree.txt and limit = 10

# Browse from root, limit by depth
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and depth = 4

# Browse from a specific node
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and node="ns=6;s=MyObjectsFolder"

# Browse from a specific node, including attribute info
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and node="ns=6;s=MyObjectsFolder" and attributes = *

# Limit by depth and filter by classes "variable" and "object"
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and output = stdout and depth = 4 and class = variable and class = object

# Variables only, generate a get opcua value command
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and node="ns=6;s=MyObjectsFolder" and class = variable and format = get_value

# Variables only, generate a run opcua client command
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and node="ns=6;s=MyObjectsFolder" and class = variable and format = run_client and name = opcua_nov and dbms = nov and table = sensor and frequency = 10 and limit = 10

# Variables only, output the path of each node
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and format = path and node = "ns=2;s=DeviceSet" and class = variable and dbms = my_dbms

# Variables only, generate a policy per node
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and format = policy and limit = 100 and node = "ns=2;s=DeviceSet" and class = variable and dbms = my_dbms

# Variables only, generate blockchain insert commands for each policy, written to a file
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and format = policy and limit = 100 and node = "ns=2;s=DeviceSet" and class = variable and dbms = my_dbms and target = "local = true and master = !master_node" and output = !tmp_dir/my_file.out
```

---

## Read node values

Node values are retrieved with the `get plc values` command:

```anylog
get plc values where type = opcua and url = [connect string] and user = [username] and password = [password] and node = [node id]
```

| Option | Description |
|---|---|
| `url` | OPC UA server endpoint. |
| `user` / `password` | Credentials required by the server. |
| `node` | One or more node IDs. |
| `nodes` | A comma-separated list of nodes within square brackets. |
| `include` | Additional attributes returned with the value: `id`, `name`, `source_timestamp`, `server_timestamp`, `status_code`, or `all`. |
| `method` | `collection` (default, a single read pulls all listed nodes) or `individual` (one read per node, used to identify the node causing failures). |
| `failures` | Requires `method = individual`. `false` (default) collects successful and failed reads; `true` collects only failed reads. |

The `include` attributes:
* `id` — the id of the attribute.
* `name` — the attribute name.
* `source_timestamp` — the timestamp of the value as determined by the data source (e.g. a sensor or device).
* `server_timestamp` — the timestamp assigned by the OPC UA server when the value was received or processed.
* `status_code` — the status of the value (e.g. Good, Bad, Uncertain).

> Note: if `include` is assigned the keyword `all`, all attributes are included in the output.

Examples:
```anylog
get plc values where type = opcua and url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and node = "ns=0;i=2257" and node = "ns=0;i=2258" and include = all

# List format
get plc values where type = opcua and url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and nodes = ["ns=4;s=AirConditioner_1.StateCondition.EventType","ns=4;s=AirConditioner_1.StateCondition.SourceNode"]
```

---

## Continuous data pull

Stream data from OPC-UA into the local database continuously:

```anylog
run plc client where type = opcua and name = [unique name] and url = [connect string] and frequency = [seconds] and dbms = [dbms] and node = [node id]
```

| Option | Description |
|---|---|
| `name` | Unique client name. |
| `frequency` | Read frequency in seconds, or in hz (e.g. `10 hz`). |
| `node` / `nodes` | One or more node IDs. |
| `policy` | Use a policy to determine nodes and table (alternative to specifying nodes inline). |
| `table` | The table to host the data (if not specified in a policy). |
| `topic` | Route data through the local broker. |

Each row is stored with two columns added automatically:
- `timestamp` — the earliest source timestamp of the values considered (if `source_timestamp` is missing, the `server_timestamp` is used).
- `duration` — the number of milliseconds between the earliest and latest timestamp considered in this read.

Examples:
```anylog
# Individual nodes
run plc client where type = opcua and name = myopcua and url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and frequency = 10 and dbms = nov and table = sensor and node = "ns=0;i=2257" and node = "ns=0;i=2258"

# Using a node list
run plc client where type = opcua and name = myopcua and url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and frequency = 10 and dbms = nov and table = sensor and nodes = ["ns=0;i=2257","ns=0;i=2258"]
```

> Multiple OPC-UA clients can run on the same node simultaneously.

### Check client status

```anylog
get plc client
```

### Stop a client

```anylog
exit plc client [client name]
```

The client name is the policy ID or `[dbms name].[table name]`. If the client name is `all`, all clients are terminated.

```anylog
exit plc all
exit plc nov.rig8
```

---

## OPC-UA with aggregations

Aggregation functions summarize streaming data over a time interval, enabling real-time analytics without storing raw
data. See details in the [Aggregations](../../06-%20Data%20Management/B-%20Query%20&%20Aggregations/Aggregations.md) section.

### 1. Identify the time and value column names

To apply aggregation, identify the names of the time attribute and the value attribute retrieved from the OPC UA
connector. If the AnyLog OPC UA service is used, the time attribute name is `timestamp`, and the value attribute name can
be retrieved with `get plc values` using `include = all` or `include = name`.

```anylog
get plc values where type = opcua and url = opc.tcp://uademo.prosysopc.com:53530/OPCUA/SimulationServer and node = "ns=3;i=1002" and include = name
```

```text
OPCUA Nodes values
name   value
------|----------|
random|-0.5909728|
```

The call above shows that the column name for `ns=3;i=1002` is `random`.

### 2. Declare the aggregation

```anylog
set aggregations where dbms = nov and table = table_2 and time_column = timestamp and value_column = random
```

### 3. (Optional) Replace raw data with aggregated data

```anylog
set aggregations encoding where dbms = nov and table = table_2 and encoding = bounds
```

### 4. Validate the aggregation declarations

```anylog
get aggregations
get aggregations config
```

### 5. Start the OPC-UA client

```anylog
<run plc client where
   type = opcua and
   name = opcua_connect1 and
   url = opc.tcp://uademo.prosysopc.com:53530/OPCUA/SimulationServer and
   node = "ns=3;i=1002" and
   frequency = 25 and
   dbms = nov and
   table = table_2>
```

### 6. Validate processing

```anylog
get plc client
get aggregations
get aggregations where dbms = nov and table = table_2
get streaming
get operator
```

### 7. Query aggregated results

```anylog
run client () sql nov format = table select timestamp::ljust(19), end_interval::ljust(19), min_val, max_val, avg_val, events from bounds_table_2 order by timestamp desc limit 10
```

> **Worth verifying:** unlike every other SQL query example across this doc set, the query text above isn't wrapped
> in quotes (`"select ..."`). This is consistent in both source files, so it isn't something either merge
> introduced — but it's worth confirming this is genuinely valid syntax for `run client () sql` rather than a
> pre-existing typo that was carried through both docs.

---

## Policy-based tag management

For large OPC-UA deployments, generate a policy for each tag and store it on the blockchain. Policies define the
structure and semantics of the tags (names, data types, relationships) and serve as a mapping between table names and tag
information. This lets AnyLog automatically interpret and organize incoming data, aligning it with the defined structure
for querying, validation, and distribution across the network.

### Generate the policies

```anylog
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and format = policy and schema = true and node = "ns=2;s=DeviceSet" and class = variable and dbms = my_dbms and target = "local = true and master = !master_node" and output = !tmp_dir/my_file.out
```

The tag policies are stored in the file `!tmp_dir/my_file.out`, in a format like:

```json
{"tag": {"class": "variable",
         "datatype": "Boolean",
         "dbms": "my_dbms",
         "nodeid": "LS1002H_AlarmSetpoint",
         "ns": 2,
         "parent": "ALARM_TAGS",
         "path": "Root/Objects/DeviceSet/WAGO 750-8210 PFC200 G2 4ETH XTR/Resources/Application/GlobalVars/ALARM_TAGS/LS1002H_AlarmSetpoint",
         "table": "t39"}}
```

If `schema` is set to `true`, the output includes, for every tag, the table schema associated with the tag:

```json
{"table": {"name": "t39",
           "dbms": "nov",
           "create": "CREATE TABLE IF NOT EXISTS t39(row_id SERIAL PRIMARY KEY, insert_timestamp TIMESTAMP NOT NULL DEFAULT NOW(), tsd_name CHAR(3), tsd_id INT, timestamp timestamp not null default now(), value bool ); CREATE INDEX t39_timestamp_index ON t39(timestamp); CREATE INDEX t39_insert_timestamp_index ON t39(insert_timestamp);",
           "source": "OPCUA Interface",
           "id": "040197b7eed831dddb1b3fd910d86deb",
           "date": "2025-04-09T00:09:53.406292Z",
           "ledger": "local"}}
```

### Load the policies to the metadata

```anylog
process !tmp_dir/my_file.out
```

### Generate the command to read the tag data

```anylog
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and format = run_client and node = "ns=2;s=DeviceSet" and class = variable and output = !tmp_dir/my_run_cmd.out and dbms = my_dbms and frequency = 3 and name = opcua_nov
```

Notes:
* The [run opcua client](#continuous-data-pull) command is stored in the file `!tmp_dir/my_run_cmd.out`.
* The `table` name is not specified, as it is derived from the policies (based on the namespace and node id).

### Execute the command

```anylog
process !tmp_dir/my_run_cmd.out
```

This pulls the data using OPC-UA and assigns it to the tables according to the info in the policies.