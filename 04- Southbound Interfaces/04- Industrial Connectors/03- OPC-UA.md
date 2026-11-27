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
- 2026-11-26 | Addition of UNS
- 2026-11-27 | Multiple weather stations UNS example
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
| `auto_uns` | Used with `format = run_client`. `true` copies it onto the generated `run plc client` command so the data is registered in the UNS. Requires `master_node`. |
| `master_node` | Used with `format = run_client`. The master node (`ip:port`) that holds the UNS policies. Required when `auto_uns = true`. |
| `group_by_attributes` | Used with `format = run_client` and `auto_uns = true`. Copied onto the generated `run plc client` command. |

**Format options:**

| Format       | Output                                                                              |
| ------------ | ----------------------------------------------------------------------------------- |
| `tree`       | OPC-UA tree structure (default).                                                    |
| `path`       | Full path strings for each node.                                                    |
| `stats`      | Count of entries per class.                                                         |
| `get_value`  | Generates [get opcua value](#read-node-values) commands for the visited nodes.      |
| `run_client` | Generates [run opcua client](#continuous-data-pull) commands for the visited nodes. |
| `policy`     | Generates a policy per tag; combine with `target` for `blockchain insert` commands. |

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
| `auto_uns` | `true` to register the ingested data in the Unified Namespace (UNS). Requires `master_node`. The default is `true` on AnyLog Enterprise and `false` on EdgeDataLake. |
| `master_node` | Master node (`ip:port`) that holds the UNS policies. Required when `auto_uns = true`. |
| `uns_prefix` | Optional UNS path prefix for the leaves, for example `opc_stations_uns3`. Used with `auto_uns = true`. |
| `group_by_attributes` | Optional list of constant names stored as a `where` clause on each UNS object. |
| `constants` | Optional JSON object of constant values copied onto each row and each UNS object. |

See [Mapping policy, constants, and UNS](#mapping-policy-constants-and-uns) for examples.

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

### UNS leaves

With `auto_uns = true`, the client creates one UNS leaf for each node in `nodes`, and an object policy for it. The namespace of each leaf is `uns_prefix` (if set) followed by the path of the variable, without `Root`:

```text
namespace = uns_prefix + "/" + path of the variable
```

The leaf is built from these parts:

| Part              | Where it comes from                                                                                                                                  |
|-------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| Namespace         | `uns_prefix` (if set), followed by the path of the variable on the OPC-UA server, without `Root`, in lower case, with `-` replaced by `_`. The variable `Root/Objects/WS-001/temperature` with `uns_prefix = opcua_ws_stations` gets the namespace `opcua_ws_stations/objects/ws_001/temperature`. If `uns_prefix` is not set, the namespace is only the path. |
| Object attributes | `column`, `table`, and `dbms` come from the mapping policy. The constants (`device`, `model`, `station_id`) are copied to the object.                |
| `where`           | Built from `group_by_attributes`, see below.                                                                                                         |

Example. The server has these nodes, with `ns=X;i=Y` as the node id of each:

```text
Paths for ns=X;i=Y
Root/Objects/Data/Temp
Root/Objects/Data/Name
Root/Objects/Data/Torque
```

With `uns_prefix = plant1`, the UNS leaves are:

```text
plant1
└── objects
    └── data
        ├── temp
        ├── name
        └── torque
```

For an example with several weather stations, see [Use case with multiple weather stations](#use-case-with-multiple-weather-stations-with-multiple-operators).

#### `group_by_attributes` and the `where`

The `where` of each object is built once, from the values of the `group_by_attributes` names, using the constants of the command and the first read:

* One attribute, `"group_by_attributes": ["station_id"]`: `where = station_id = 'WS-001'`.
* Two attributes, `"group_by_attributes": ["station_id", "device"]`: the comparisons are joined with `and`, `where = station_id = 'WS-001' and device = 'opc1-dev1'`. If one of the attributes has no value, the object gets no `where`.

The attributes only set the `where`. They do not change the path of the leaf.

Each leaf has a UNS policy and an object policy. The object names the table, the column, and the `where` that selects the station. Example, the `pressure` leaf of WS-001:

```json
{
  "uns": {
    "name": "pressure",
    "namespace": "opcua_ws_stations/objects/ws_001/pressure",
    "object_id": "8f51cfed95f6662c98ff5e2f2ed4f630",
    "parent": "f4b625e659b0423109e912ee0cb784ae",
    "id": "ff0fbcb0bc3f1fb810963ed491fea50a",
    "date": "2026-11-27T08:58:00.616328Z",
    "ledger": "global"
  },
  "object": {
    "device": "opc1-dev1",
    "model": "MX1234D1",
    "station_id": "WS-001",
    "opcua": {
      "ns": "ns=2;i=21",
      "class": "variable",
      "node_sid": "mud_weight_out",
      "datatype": "String",
      "parent": "rig-1",
      "path": "Root/Objects/rig-data/rig-1/mud_weight_out"
    },
    "column": "pressure",
    "dbms": "env_sensor",
    "table": "weather_stations_opcua",
    "where": "station_id = 'WS-001'",
    "id": "8f51cfed95f6662c98ff5e2f2ed4f630",
    "date": "2026-11-27T08:58:00.611856Z",
    "ledger": "global"
  }
}
```

The constants `device`, `model`, and `station_id` are stored on the object, and `station_id` is also in `where`. The `column` is the column of the table that holds the leaf's value.

To list the leaves:

```anylog
blockchain get uns where name = pressure
```

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
data. See details in the [Aggregations](../../09-%20Data%20Management/02-2%20Data%20Aggregations.md) section.

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
<get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and
    format = run_client and
    node = "ns=2;s=DeviceSet" and
    class = variable and
    output = !tmp_dir/my_run_cmd.out and
    dbms = my_dbms and
    frequency = 3 and
    name = opcua_nov
>
```

Notes:

* The [run opcua client](#continuous-data-pull) command is stored in the file `!tmp_dir/my_run_cmd.out`.
* The `table` name is not specified, as it is derived from the policies (based on the namespace and node id).

To register the data in the UNS, add `auto_uns`, `master_node` and, optionally, `group_by_attributes`. They are copied onto the generated `run plc client` command:

```anylog
<get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server and
    format = run_client and
    node = "ns=2;s=DeviceSet" and
    class = variable and
    dbms = my_dbms and
    frequency = 3 and
    name = opcua-client1 and
    auto_uns = true and
    master_node = !ledger_conn and
    group_by_attributes = ["XYZ"] and
    output = !tmp_dir/my_run_cmd_uns.out
>
```

Notes:

* The `run plc client` command is stored in the file `!tmp_dir/my_run_cmd_uns.out`.
* `auto_uns` is accepted only with `format = run_client`, and it requires `master_node`.
* `group_by_attributes` is accepted only with `format = run_client` and `auto_uns = true`.
* `get opcua struct` does not accept `constants`. Add `constants` to the generated `run plc client` command.

### Execute the command

```anylog
process !tmp_dir/my_run_cmd.out
process !tmp_dir/my_run_cmd_uns.out
```

Each file holds one of the two commands above. `my_run_cmd.out` is for the run without UNS. `my_run_cmd_uns.out` is for the run with UNS. Process only the file you need, because both commands read the same node.

This pulls the data using OPC-UA and assigns it to the tables according to the info in the policies.

### Constants and `group_by_attributes`

Both are optional on `run plc client`. `get opcua struct` with `format = run_client` copies `group_by_attributes` onto the generated command. It does not accept `constants`, so that keyword is added on the `run plc client` command.

```anylog
constants = {"station_id":"RIG-1", "site":"WEST"} and
group_by_attributes = ["rig_name"]
```

* `constants` copies each key onto the stored row. A value is a string, a number, or a bool. The row keeps the value when the table has a column for it: a fixed table, or a mapping schema that names the column.  
Tag tables from `get plc struct` and `schema = true` have `timestamp` and `value` only, so a constant has no column there.
* With `auto_uns = true`, each constant is also a key on the UNS object. A key already set on the object stays. With `auto_uns = false`, no UNS objects are written.
* `group_by_attributes` sets the `where` on each UNS object, for example `rig_name = 'Permian Star'`. It applies when `auto_uns = true` and a table is named, on the command or in a mapping policy.

---

### Mapping policy, constants, and UNS

The two examples below use the same policy, `b06e3717bc7ea3e237111c89fe4e3064`, and write to the same table `opcua_stations`. The table does not record which client wrote each row. The policy is stored on the blockchain as follows.

```json
{
  "mapping": {
    "name": "opcua_stations",
    "dbms": "env_sensor",
    "table": "opcua_stations",
    "readings": "",
    "params": [
      ["Permian Star", "[rop]", "[wob]", "[torque]"]
    ],
    "group_by_attributes": ["rig_name", "station_id"],
    "schema": {
      "timestamp": {"type": "timestamp", "default": "now()", "bring": "[timestamp]"},
      "rig_name": {"type": "str", "default": "params.0"},
      "station_id": {"type": "str", "default": null, "bring": "[station_id]"},
      "drill_rate": {"type": "float", "default": null, "bring": "params.1"},
      "bit_weight": {"type": "float", "default": null, "bring": "params.2"},
      "rotary_torque": {"type": "float", "default": null, "bring": "params.3"}
    },
    "id": "b06e3717bc7ea3e237111c89fe4e3064",
    "date": "2026-11-26T15:39:09.565783Z",
    "ledger": "global"
  }
}
```

The command and the policy can also set constants, such as `modeid` and `serialno`:

```anylog
constants = {"station_id":"RIG-1", "modeid":"MODEL-X1", "serialno":"SN-0042"}
```

These keys are copied onto a row only when the table has a column for them, as described in [Constants and `group_by_attributes](#constants-and-group_by_attributes)`.

#### Named table, no UNS

A mapping policy sets the table and the column for each node. `auto_uns = false`, so this run writes no UNS entries.

A table can be either in policy or in the command. If neither names a table, the run fails with "mapping policy requires table (in policy or on the command)".  

The following example uses table `opcua_stations`, set in the policy.  
The policy has a `station_id` column, which is filled from the constant `constants = {"station_id":"RIG-1"}` on the command.  
The rows have `station_id = RIG-1`, `rig_name = Permian Star`, and the three measurements.

```anylog
<run plc client where type = opcua and
    name = opc-test-const and
    url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and
    frequency = 10 and
    dbms = env_sensor and
    policy = b06e3717bc7ea3e237111c89fe4e3064 and
    auto_uns = false and
    constants = {"station_id":"RIG-1"} and
    nodes = ["ns=2;i=5",
           "ns=2;i=10",
           "ns=2;i=11",
           "ns=2;i=13"]
>
```

Tables:

* `opcua_stations`

The mapping sets the columns:  

- `station_id` comes from the constant `RIG-1`  
- `rop` goes to `drill_rate`  
- `wob` to `bit_weight`  
- `torque` to `rotary_torque`.

```
Schema for DBMS: 'env_sensor' and Table: 'opcua_stations'
Column Name      Column Type                 
----------------|---------------------------|
row_id          |integer                    |
insert_timestamp|timestamp without time zone|
tsd_name        |char(3)                    |
tsd_id          |int                        |
timestamp       |timestamp without time zone|
rig_name        |varchar                    |
station_id      |varchar                    |
drill_rate      |float                      |
bit_weight      |float                      |
rotary_torque   |float                      |
```

---

#### Named table with UNS

Uses the same policy as the named-table example (`b06e3717bc7ea3e237111c89fe4e3064`), with `auto_uns = true` and UNS prefix `opc_stations_uns3`.  
The constant `station_id = RIG-1` is set on the command.

The policy has `group_by_attributes = ["rig_name", "station_id"]`, so the `where` on each UNS object is built from the row values, including the constant. Use this form when a field's value comes from the row or the constant.

**Limitation:** if `group_by_attributes` is on the command instead of the policy, a field is used in the `where` only when its schema has a literal default, such as `rig_name` with `params.0`. A `station_id` with `bring`, `null` or `""` as its default gives no value, so the whole `where` is dropped.

```anylog
<run plc client where type = opcua and
    name = opc-stations-uns3 and
    url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and
    frequency = 10 and
    dbms = env_sensor and
    policy = b06e3717bc7ea3e237111c89fe4e3064 and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    uns_prefix = opc_stations_uns3 and
    constants = {"station_id":"RIG-1"} and
    nodes = ["ns=2;i=5",
           "ns=2;i=10",
           "ns=2;i=11",
           "ns=2;i=13"]
>
```

Tables:

* `opcua_stations`

Namespace (one leaf per node, each with `where rig_name = 'Permian Star' and station_id = 'RIG-1'`):

* `opc_stations_uns3/objects/rig_data/rig_1/rig_name`, column `rig_name`
* `opc_stations_uns3/objects/rig_data/rig_1/rop`, column `drill_rate`
* `opc_stations_uns3/objects/rig_data/rig_1/wob`, column `bit_weight`
* `opc_stations_uns3/objects/rig_data/rig_1/torque`, column `rotary_torque`

```anylog
blockchain get uns where name = rop bring.extend
```

```json
[
  {
    "uns": {
      "name": "rop",
      "namespace": "opc_stations_uns3/objects/rig_data/rig_1/rop",
      "object_id": "f89d72ab3e050ddc8b9c8ccf2c284f49",
      "parent": "0693034e466b3be2361c05c186082081",
      "id": "5138c590048a8a5825535a0382e7fc2f",
      "date": "2026-11-26T15:41:18.903177Z",
      "ledger": "global"
    },
    "object": {
      "station_id": "RIG-1",
      "opcua": {
        "ns": "ns=2;i=10",
        "class": "variable",
        "node_sid": "rop",
        "datatype": "Double",
        "parent": "rig-1",
        "path": "Root/Objects/rig-data/rig-1/rop",
        "url": "opc.tcp://127.0.0.1:4840/freeopcua/data-generator"
      },
      "column": "drill_rate",
      "dbms": "env_sensor",
      "table": "opcua_stations",
      "where": "rig_name = 'Permian Star' and station_id = 'RIG-1'",
      "id": "f89d72ab3e050ddc8b9c8ccf2c284f49",
      "date": "2026-11-26T15:41:18.898774Z",
      "ledger": "global"
    }
  }
]
```

---

### One table per tag, no UNS

These two examples share the tag tables `t28` through `t31`. The table does not record which client wrote each row.

No `table` and no `policy`. Each node writes to its own table, which is created from a tag policy. Create the tag policies first, one node at a time, with `get plc struct` and `process`.  
The example below is for `ns=2;i=5`. Repeat it for `ns=2;i=10`, `ns=2;i=11`, and `ns=2;i=13`.

```anylog
<get plc struct where type = opcua and
    format = policy and
    schema = true and
    url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and
    dbms = env_sensor and
    node = "ns=2;i=5" and
    output = !struct_file and
    target = "local = true"
>

<process !struct_file>
```

```anylog
<run plc client where type = opcua and
    name = opc-tag-test and
    url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and
    frequency = 10 and
    dbms = env_sensor and
    auto_uns = false and
    nodes = ["ns=2;i=5",
           "ns=2;i=10",
           "ns=2;i=11",
           "ns=2;i=13"]
>
```

Tables:

* `t28` for `rig_name`
* `t29` for `rop`
* `t30` for `wob`
* `t31` for `torque`

Columns:

* `t28`: `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`, `timestamp`, `value` (`varchar`)
* `t29`: `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`, `timestamp`, `value` (`float`)
* `t30`: `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`, `timestamp`, `value` (`float`)
* `t31`: `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`, `timestamp`, `value` (`float`)

Schema for `t29`:

```
Schema for DBMS: 'env_sensor' and Table: 't29'
Column Name      Column Type                 
----------------|---------------------------|
row_id          |integer                    |
insert_timestamp|timestamp without time zone|
tsd_name        |char(3)                    |
tsd_id          |int                        |
timestamp       |timestamp without time zone|
value           |float                      |
```

### One table per tag with UNS

Same tag tables as the example above. The UNS prefix is `opc_tag_uns`.

```anylog
<run plc client where type = opcua and
    name = opc-tag-uns and
    url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and
    frequency = 10 and
    dbms = env_sensor and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    uns_prefix = opc_tag_uns and
    nodes = ["ns=2;i=5",
           "ns=2;i=10",
           "ns=2;i=11",
           "ns=2;i=13"]
>
```

Tables:

* `t28`, `t29`, `t30`, `t31` (shared with run 3, no new tables)

Columns (same as the example above):

* `t28`: `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`, `timestamp`, `value` (`varchar`)
* `t29`: `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`, `timestamp`, `value` (`float`)
* `t30`: `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`, `timestamp`, `value` (`float`)
* `t31`: `row_id`, `insert_timestamp`, `tsd_name`, `tsd_id`, `timestamp`, `value` (`float`)

Namespace (one leaf per node). Each leaf has no `column` and no `where`, because each table holds one tag:

* `opc_tag_uns/objects/rig_data/rig_1/rig_name`, table `t28`
* `opc_tag_uns/objects/rig_data/rig_1/rop`, table `t29`
* `opc_tag_uns/objects/rig_data/rig_1/wob`, table `t30`
* `opc_tag_uns/objects/rig_data/rig_1/torque`, table `t31`

```anylog
blockchain get uns where name = rig_name bring.extend
```

```json
[
  {
    "uns": {
      "name": "rig_name",
      "namespace": "opc_tag_uns/objects/rig_data/rig_1/rig_name",
      "object_id": "98dd553100b5551178ea7f5450bfec46",
      "parent": "c40d26f1fd32f7402110cc3f3e500b06",
      "id": "a6eee1606069c0e85d0a6736ee2bc2cc",
      "date": "2026-11-26T11:54:29.328379Z",
      "ledger": "global"
    },
    "object": {
      "opcua": {
        "ns": "ns=2;i=5",
        "class": "variable",
        "node_sid": "rig_name",
        "datatype": "String",
        "parent": "rig-1",
        "path": "Root/Objects/rig-data/rig-1/rig_name",
        "url": "opc.tcp://127.0.0.1:4840/freeopcua/data-generator"
      },
      "dbms": "env_sensor",
      "table": "t28",
      "id": "98dd553100b5551178ea7f5450bfec46",
      "date": "2026-11-26T11:54:29.323752Z",
      "ledger": "global"
    }
  }
]
```

---

### Use case with multiple weather stations with multiple operators

Each operator runs one client into the same fixed table `weather_stations_opcua`, with `auto_uns = true`.  
The mapping policy below sets the table and the columns for the weather readings and for the constants. The policy, the nodes, the UNS prefix `opcua_ws_stations`, and the constant names are the same on every operator.  

#### Browse the station object

To see the whole address space of the weather server, start the browse at the root:

```anylog
get opcua struct where url = opc.tcp://127.0.0.1:4844/freeopcua/weather and depth = 4
```

The browse at `depth = 4` returns 65 nodes. The block below keeps only the path from `Root` to the station object and its 14 variables. The other nodes, such as `Server`, `Aliases`, `Types`, and `Views`, are left out:

```text
Root
  [object], (ns=0;i=85, name=Objects, datatype=None)
    [object], (ns=2;i=1, name=WeatherStation1, datatype=None)
      [variable], (ns=2;i=10, name=station_id, datatype=VariantType.String)
      [variable], (ns=2;i=11, name=location, datatype=VariantType.String)
      [variable], (ns=2;i=20, name=temperature, datatype=VariantType.Double)
      [variable], (ns=2;i=30, name=temperature_unit, datatype=VariantType.String)
      [variable], (ns=2;i=21, name=pressure, datatype=VariantType.Double)
      [variable], (ns=2;i=31, name=pressure_unit, datatype=VariantType.String)
      [variable], (ns=2;i=22, name=humidity, datatype=VariantType.Double)
      [variable], (ns=2;i=32, name=humidity_unit, datatype=VariantType.String)
      [variable], (ns=2;i=23, name=wind_speed, datatype=VariantType.Double)
      [variable], (ns=2;i=33, name=wind_speed_unit, datatype=VariantType.String)
      [variable], (ns=2;i=24, name=wind_direction, datatype=VariantType.Double)
      [variable], (ns=2;i=34, name=wind_direction_unit, datatype=VariantType.String)
      [variable], (ns=2;i=25, name=rain, datatype=VariantType.Double)
      [variable], (ns=2;i=35, name=rain_unit, datatype=VariantType.String)
```

Each line is one node. The indentation shows its depth. `Root` is at depth 0, `Objects` at depth 1, and the station object at depth 2. In the output it is named `WeatherStation1`, and its browse name is `WS-001`. Its variables are one level below it, so they appear at `depth = 4`.

Each line has the same parts, which the node printer builds in `print_info` in `struct_tree.py`:

* `[object]`: the node class, from `get_node_class`. Other classes are `[variable]`, `[method]`, and so on.
* `ns=2;i=1`: the namespace index, then the node id. The id type is `i` for numeric ids and `s` for string ids. Root shows `?` because its id type is not in the lookup table.
* `name=WeatherStation1`: the display name of the node. `get opcua struct` prints this name.
* `datatype=None`: the value type. Objects have no value, so it is `None`. A variable shows its type, such as `VariantType.Double`.

Each node also has a browse name. It is the name the UNS path is built from. The tree output above does not show it. To see the browse names, use `format = path`. The output is the browse path of each variable under `WS-001`, built from the browse names:

```anylog
get opcua struct where url = opc.tcp://127.0.0.1:4844/freeopcua/weather and node = "ns=2;i=1" and format = path and output = /tmp/anylog_test/path_ws001.out
```

```text
Root/Objects/WS-001/station_id
Root/Objects/WS-001/location
Root/Objects/WS-001/temperature
Root/Objects/WS-001/temperature_unit
Root/Objects/WS-001/pressure
Root/Objects/WS-001/pressure_unit
Root/Objects/WS-001/humidity
Root/Objects/WS-001/humidity_unit
Root/Objects/WS-001/wind_speed
Root/Objects/WS-001/wind_speed_unit
Root/Objects/WS-001/wind_direction
Root/Objects/WS-001/wind_direction_unit
Root/Objects/WS-001/rain
Root/Objects/WS-001/rain_unit
```

On this server the browse name of the station object is `WS-001`, and its display name is `WeatherStation1`. The UNS folder `ws_001` is the browse name in lowercase, with `-` replaced by `_`. The display name does not change the UNS path.

```anylog
get opcua struct where url = opc.tcp://127.0.0.1:4844/freeopcua/weather and node = "ns=2;i=1"
```

```text
[object], (ns=2;i=1, name=WeatherStation1, datatype=None)
  [variable], (ns=2;i=10, name=station_id, datatype=VariantType.String)
  [variable], (ns=2;i=11, name=location, datatype=VariantType.String)
  [variable], (ns=2;i=20, name=temperature, datatype=VariantType.Double)
  [variable], (ns=2;i=30, name=temperature_unit, datatype=VariantType.String)
  [variable], (ns=2;i=21, name=pressure, datatype=VariantType.Double)
  [variable], (ns=2;i=31, name=pressure_unit, datatype=VariantType.String)
  [variable], (ns=2;i=22, name=humidity, datatype=VariantType.Double)
  [variable], (ns=2;i=32, name=humidity_unit, datatype=VariantType.String)
  [variable], (ns=2;i=23, name=wind_speed, datatype=VariantType.Double)
  [variable], (ns=2;i=33, name=wind_speed_unit, datatype=VariantType.String)
  [variable], (ns=2;i=24, name=wind_direction, datatype=VariantType.Double)
  [variable], (ns=2;i=34, name=wind_direction_unit, datatype=VariantType.String)
  [variable], (ns=2;i=25, name=rain, datatype=VariantType.Double)
  [variable], (ns=2;i=35, name=rain_unit, datatype=VariantType.String)
```

The command ends with a summary of the nodes it considered:

```text
PLC Nodes Considered
Type          Counter 
-------------|-------|
total        |     15|
object       |      1|
variable     |     14|
method       |      0|
objecttype   |      0|
variabletype |      0|
referencetype|      0|
datatype     |      0|
view         |      0|
read_failure |      0|
unknown      |      0|
```

How these object names become the UNS folders is described in [UNS leaves](#uns-leaves).

The weather server used in this section has only the `WS-001` object (`ns=2;i=1`). A `WS-002` object is not on the server yet, so browsing `ns=2;i=N` for WS-002 returns nothing until the station is added to the server.

Read the station first.  
One `get plc values` returns every measurement and its unit, node list is the same on every station.  
Only the `url` is the parameter to change.

**Station WS-001**

```anylog
<get plc values where type = opcua and
    url = opc.tcp://127.0.0.1:4844/freeopcua/weather and
    nodes = ["ns=2;i=20","ns=2;i=30",
             "ns=2;i=21","ns=2;i=31",
             "ns=2;i=22","ns=2;i=32",
             "ns=2;i=23","ns=2;i=33",
             "ns=2;i=24","ns=2;i=34",
             "ns=2;i=25","ns=2;i=35"] and
    include = name
>
```

One read of that server:

```text
OPCUA Nodes values
name              value
------------------|--------|
temperature       |63.2    |
temperature_unit  |degF    |
pressure          |1007.41 |
pressure_unit     |hPa     |
humidity          |45.33   |
humidity_unit     |%       |
wind_speed        |2.45    |
wind_speed_unit   |m/s     |
wind_direction    |205.76  |
wind_direction_unit|deg    |
rain              |0.0     |
rain_unit         |mm      |
```

If the server has `station_id` and `location` as nodes, read them too, for example `ns=2;i=10` for `station_id` and `ns=2;i=11` for `location`.  
If not, set them as constants on the `run plc client` command, for example `constants = {"station_id":"WS-001","location":"Fresno, CA"}`.

WS-002 is the same command with a different client name and constants.

The policy has one column per node, values and units, plus `device`, `model`, and `station_id` filled from the constants.  
Each entry in `params` is the browse name of an OPC-UA node, written in square brackets, for example `"[temperature]"`. The names must match the browse names returned by `get plc values ... include = name`, and they must be in the same order as the `nodes` list of the `run plc client` command. The schema picks each value by its position, `params.0`, `params.1`, and so on.  
The node ids `ns=2;i=20` to `ns=2;i=35` are the nodes of the weather server used above. Replace them with the nodes of your server before you run the commands:

```json
{
  "mapping": {
    "name": "weather_stations_opcua",
    "dbms": "env_sensor",
    "table": "weather_stations_opcua",
    "readings": "",
    "params": [
      ["[temperature]", "[temperature_unit]",
       "[pressure]", "[pressure_unit]",
       "[humidity]", "[humidity_unit]",
       "[wind_speed]", "[wind_speed_unit]",
       "[wind_direction]", "[wind_direction_unit]",
       "[rain]", "[rain_unit]"]
    ],
    "group_by_attributes": ["station_id"],
    "schema": {
      "timestamp": {"type": "timestamp", "default": "now()", "bring": "[timestamp]"},
      "device": {"type": "str", "default": null, "bring": "[device]"},
      "model": {"type": "str", "default": null, "bring": "[model]"},
      "station_id": {"type": "str", "default": null, "bring": "[station_id]"},
      "temperature": {"type": "float", "default": null, "bring": "params.0"},
      "temperature_unit": {"type": "str", "default": null, "bring": "params.1"},
      "pressure": {"type": "float", "default": null, "bring": "params.2"},
      "pressure_unit": {"type": "str", "default": null, "bring": "params.3"},
      "humidity": {"type": "float", "default": null, "bring": "params.4"},
      "humidity_unit": {"type": "str", "default": null, "bring": "params.5"},
      "wind_speed": {"type": "float", "default": null, "bring": "params.6"},
      "wind_speed_unit": {"type": "str", "default": null, "bring": "params.7"},
      "wind_direction": {"type": "float", "default": null, "bring": "params.8"},
      "wind_direction_unit": {"type": "str", "default": null, "bring": "params.9"},
      "rain": {"type": "float", "default": null, "bring": "params.10"},
      "rain_unit": {"type": "str", "default": null, "bring": "params.11"}
    },
    "id": "7e0c1a9f4b2d4c58a3b6d1f90e2a5c73",
    "date": "2026-11-26T20:30:00.000000Z",
    "ledger": "global"
  }
}
```

**Operator 1 — station WS-001**

```anylog
<run plc client where type = opcua and
    name = opc-1 and
    url = opc.tcp://127.0.0.1:4840/freeopcua/data-generator and
    frequency = 10 and
    dbms = env_sensor and
    policy = 7e0c1a9f4b2d4c58a3b6d1f90e2a5c73 and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    uns_prefix = opcua_ws_stations and
    constants = {"device":"opc1-dev1","model":"MX1234D1","station_id":"WS-001"} and
    nodes = ["ns=2;i=20","ns=2;i=30",
             "ns=2;i=21","ns=2;i=31",
             "ns=2;i=22","ns=2;i=32",
             "ns=2;i=23","ns=2;i=33",
             "ns=2;i=24","ns=2;i=34",
             "ns=2;i=25","ns=2;i=35"]
>
```

**Operator 2 — station WS-002**

```anylog
<run plc client where type = opcua and
    name = opc-2 and
    url = opc.tcp://127.0.0.2:4840/freeopcua/data-generator and
    frequency = 10 and
    dbms = env_sensor and
    policy = 7e0c1a9f4b2d4c58a3b6d1f90e2a5c73 and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    uns_prefix = opcua_ws_stations and
    constants = {"device":"opc2-dev2","model":"FX1234D9","station_id":"WS-002"} and
    nodes = ["ns=2;i=20","ns=2;i=30",
             "ns=2;i=21","ns=2;i=31",
             "ns=2;i=22","ns=2;i=32",
             "ns=2;i=23","ns=2;i=33",
             "ns=2;i=24","ns=2;i=34",
             "ns=2;i=25","ns=2;i=35"]
>
```

Tables:

* `weather_stations_opcua`

Both operators write to the same table, and the `station_id` column keeps their rows apart.

The two OPC-UA servers have different browse names, `WS-001` and `WS-002`, so their UNS leaves are separate: `opcua_ws_stations/objects/ws_001/` and `opcua_ws_stations/objects/ws_002/`. The display name does not change the UNS path, so if both servers have the same display name, that is not an issue. How the UNS leaves are created is described in [UNS leaves](#uns-leaves).

The `ws_002` branch is created when the `WS-002` client starts. Each station gets its own branch, under the same `opcua_ws_stations` prefix.

Each station is one object directly under `Objects`. The browse path of the object is `Root/Objects/` followed by its browse name. The display name is not used. Each station has its own server, so the node id `ns=2;i=1` is the same on each one:

```text
Root/Objects/WS-001    [object], (ns=2;i=1, name=WeatherStation1, datatype=None)    server 1, opc.tcp://127.0.0.1:4844
Root/Objects/WS-002    [object], (ns=2;i=1, name=WeatherStation2, datatype=None)    server 2, opc.tcp://127.0.0.1:4845
Root/Objects/WS-00N    [object], (ns=2;i=1, name=..., datatype=None)                server N
```

The variables of each station are one level below its object, for example `Root/Objects/WS-001/temperature`. The browse name of the object becomes the folder under `objects` after the name is normalized: `WS-001` creates `opcua_ws_stations/objects/ws_001/`, `WS-002` creates `opcua_ws_stations/objects/ws_002/`, and `WS-00N` creates `opcua_ws_stations/objects/ws_00n/`. The leaves are:

```text
opcua_ws_stations
└── objects
    ├── ws_001
    │   ├── temperature
    │   ├── temperature_unit
    │   ├── pressure
    │   ├── pressure_unit
    │   └── ...
    └── ws_002
        ├── temperature
        ├── temperature_unit
        ├── pressure
        ├── pressure_unit
        └── ...
```

#### If the servers are identical

**Warning:** if the servers are identical, with the same browse names (`WeatherData`) and the same display name (`Weather`), the two clients write to the same leaves. **Each client must have its own `uns_prefix`.**

```text
client1: uns_prefix = testmulti/WS-01
client2: uns_prefix = testmulti/WS-02
```

All other options are the same as in `Operator 1` and `Operator 2` above.

Example. Each clone is the same server, with the same node ids and the same layout. Only the URL changes:

* Browse name: `WeatherData`. The UNS path uses it, so both clones create the folder `weatherdata`.
* Display name: `Weather`. `get opcua struct` prints it, and the UNS path does not use it.
* Station object: `ns=2;i=1`. Values: `ns=2;i=20` to `25`. Units: `ns=2;i=30` to `35`.

Browse one clone to check its names:

```anylog
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/weather and node = "ns=2;i=1"
```

```text
[object], (ns=2;i=1, name=Weather, datatype=None)
  [variable], (ns=2;i=20, name=temperature, datatype=VariantType.Double)
  [variable], (ns=2;i=30, name=temperature_unit, datatype=VariantType.String)
  ...
```

The browse paths of the clone are `Root/Objects/WeatherData/<name>`.

Each operator runs one `run plc client` command. The two commands are the same except for the client name, the URL, `uns_prefix`, and `constants`.

**Operator 1 — Station 1**

```anylog
run plc client where type = opcua and
    name = opc-mw-1 and
    url = opc.tcp://127.0.0.1:4840/freeopcua/weather and
    frequency = 10 and
    dbms = env_sensor and
    policy = 5b2f7c1e9a3d4e60b8c4f1a27d9e3a15 and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    uns_prefix = multiweather/WS-001 and
    constants = {"device":"mw-dev1","model":"MW1234","station_id":"WS-001"} and
    nodes = ["ns=2;i=20","ns=2;i=30",
             "ns=2;i=21","ns=2;i=31",
             "ns=2;i=22","ns=2;i=32",
             "ns=2;i=23","ns=2;i=33",
             "ns=2;i=24","ns=2;i=34",
             "ns=2;i=25","ns=2;i=35"]
```

**Operator 2 — Station 2**

```anylog
run plc client where type = opcua and
    name = opc-mw-2 and
    url = opc.tcp://127.0.0.2:4840/freeopcua/weather and
    frequency = 10 and
    dbms = env_sensor and
    policy = 5b2f7c1e9a3d4e60b8c4f1a27d9e3a15 and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    uns_prefix = multiweather/WS-002 and
    constants = {"device":"mw-dev2","model":"MW1234","station_id":"WS-002"} and
    nodes = ["ns=2;i=20","ns=2;i=30",
             "ns=2;i=21","ns=2;i=31",
             "ns=2;i=22","ns=2;i=32",
             "ns=2;i=23","ns=2;i=33",
             "ns=2;i=24","ns=2;i=34",
             "ns=2;i=25","ns=2;i=35"]
```

The `uns_prefix` is lower case in the leaves, so the two clients create these branches:

The squeezed list of the leaves under each station:

```text
multiweather
├── ws_001
│   └── objects/weatherdata/
│       ├── humidity
│       ├── humidity_unit
│       ├── pressure
│       ├── pressure_unit
│       └── ...
└── ws_002
    └── objects/weatherdata/
        ├── humidity
        ├── humidity_unit
        ├── pressure
        ├── pressure_unit
        └── ...
```

The two clones are separate servers, so each client reads its own clone. Both clients write to `weather_stations_opcua_full`, and the `station_id` column keeps their rows apart.

#### Table columns

The columns of `weather_stations_opcua`, from `get columns where dbms = env_sensor and table = weather_stations_opcua`:

| Column                | Type                        | Source                            |
|-----------------------|-----------------------------|-----------------------------------|
| `row_id`              | integer                     | Added by the node                 |
| `insert_timestamp`    | timestamp without time zone | Added by the node                 |
| `tsd_name`            | char(3)                     | Added by the node                 |
| `tsd_id`              | int                         | Added by the node                 |
| `timestamp`           | timestamp without time zone | Policy, `[timestamp]`             |
| `device`              | character varying           | Constant `device`                 |
| `model`               | character varying           | Constant `model`                  |
| `station_id`          | character varying           | Constant `station_id`             |
| `temperature`         | float                       | Node `ns=2;i=20`, `params.0`      |
| `temperature_unit`    | character varying           | Node `ns=2;i=30`, `params.1`      |
| `pressure`            | float                       | Node `ns=2;i=21`, `params.2`      |
| `pressure_unit`       | character varying           | Node `ns=2;i=31`, `params.3`      |
| `humidity`            | float                       | Node `ns=2;i=22`, `params.4`      |
| `humidity_unit`       | character varying           | Node `ns=2;i=32`, `params.5`      |
| `wind_speed`          | float                       | Node `ns=2;i=23`, `params.6`      |
| `wind_speed_unit`     | character varying           | Node `ns=2;i=33`, `params.7`      |
| `wind_direction`      | float                       | Node `ns=2;i=24`, `params.8`      |
| `wind_direction_unit` | character varying           | Node `ns=2;i=34`, `params.9`      |
| `rain`                | float                       | Node `ns=2;i=25`, `params.10`     |
| `rain_unit`           | character varying           | Node `ns=2;i=35`, `params.11`     |
