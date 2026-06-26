---
title: OPC-UA
description: Configure AnyLog as an OPC-UA client to pull data from industrial devices continuously.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

OPC Unified Architecture (OPC UA) is a platform-independent industrial communication protocol with built-in security (encryption, authentication, access control). AnyLog can act as an OPC-UA client, pulling data from any OPC-UA server and streaming it into local databases.

---

## Explore the server

### Get namespaces

Each namespace in an OPC UA server is assigned a unique index used in Node IDs (e.g. `ns=1;s=TemperatureSensor`):

```anylog
get opcua namespace where url = [connect string] and user = [username] and password = [password]
```

Example:
```anylog
get opcua namespace where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer
```

### Traverse the address space tree

```anylog
get opcua struct where url = [connect string] and [options]
```

Key options:

| Option | Description |
|---|---|
| `url` | OPC UA server endpoint |
| `user` / `password` | Credentials |
| `node` | Override the root node (e.g. `ns=6;s=MyObjectsFolder`) |
| `type` | Filter by node type: `Object`, `Variable`, etc. |
| `class` | Filter by class |
| `depth` | Limit traversal depth |
| `limit` | Limit number of nodes visited |
| `format` | Output format (see below) |
| `output` | Write output to file instead of stdout |
| `validate` | If `true`, reads each node's value to confirm it is readable |
| `schema` | If `true`, includes table schema for each tag |
| `dbms` / `table` | Used when generating `run_client` or `policy` output |
| `frequency` | Used when generating `run_client` output |
| `target` | Variables for `blockchain insert` commands (used with `format = policy`) |

**Format options:**

| Format | Output |
|---|---|
| `tree` | OPC-UA tree structure (default) |
| `path` | Full path strings for each node |
| `stats` | Count of entries per class |
| `get_value` | Generates `get opcua value` commands for visited nodes |
| `run_client` | Generates `run opcua client` commands for visited nodes |
| `policy` | Generates a policy per tag; combine with `target` for `blockchain insert` commands |

### Traversal examples

```anylog
# Browse from root, limit 10 nodes
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and limit = 10

# Browse from a specific node, depth limit
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer and node="ns=6;s=MyObjectsFolder" and depth = 4

# Filter to variable nodes only, generate run_client command
get opcua struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer \
    and node="ns=6;s=MyObjectsFolder" and class = variable \
    and format = run_client and dbms = nov and table = sensor and frequency = 10

# Generate blockchain insert commands for all variable tags
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server \
    and format = policy and node = "ns=2;s=DeviceSet" and class = variable \
    and dbms = my_dbms and target = "local = true and master = !master_node" \
    and output = !tmp_dir/my_file.out
```

---

## Read node values

```anylog
get plc values where type = opcua and url = [connect string] and node = [node id]
```

Options:

| Option | Description |
|---|---|
| `node` | One or more node IDs |
| `nodes` | Comma-separated list in square brackets |
| `include` | `id`, `name`, `source_timestamp`, `server_timestamp`, `status_code`, or `all` |
| `method` | `collection` (default, single read for all nodes) or `individual` (one read per node, for debugging) |
| `failures` | `true` — return only failed reads (requires `method = individual`) |

Examples:
```anylog
get plc values where type = opcua and url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer \
    and node = "ns=0;i=2257" and node = "ns=0;i=2258" and include = all

# List format
get plc values where type = opcua and url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer \
    and nodes = ["ns=4;s=AirConditioner_1.StateCondition.EventType","ns=4;s=AirConditioner_1.StateCondition.SourceNode"]
```

---

## Continuous data pull

Stream data from OPC-UA into the local database continuously:

```anylog
run plc client where type = opcua and name = [unique name] and url = [connect string] and frequency = [seconds] and dbms = [dbms] and table = [table] and node = [node id]
```

| Option | Description |
|---|---|
| `name` | Unique client name |
| `frequency` | Read frequency in seconds, or in hz (e.g. `10 hz`) |
| `node` / `nodes` | One or more node IDs |
| `policy` | Use a policy to determine nodes and table (alternative to specifying nodes inline) |
| `topic` | Route data through the local broker |

Each row is stored with two columns added automatically:
- `timestamp` — earliest source timestamp of the values in this read
- `duration` — milliseconds between the earliest and latest timestamp in this read

Examples:
```anylog
run plc client where type = opcua and name = myopcua \
    and url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer \
    and frequency = 10 and dbms = nov and table = sensor \
    and node = "ns=0;i=2257" and node = "ns=0;i=2258"

# Using a node list
run plc client where type = opcua and name = myopcua \
    and url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer \
    and frequency = 10 and dbms = nov and table = sensor \
    and nodes = ["ns=0;i=2257","ns=0;i=2258"]
```

Multiple OPC-UA clients can run on the same node simultaneously.

### Check client status
```anylog
get plc client
```

### Stop a client
```anylog
exit plc client [client name]    # by policy ID or dbms.table
exit plc all                      # stop all clients
exit plc nov.rig8
```

---

## OPC-UA with aggregations

Combine OPC-UA with rolling aggregations for real-time analytics without storing raw data.

### 1. Identify the value column name

```anylog
get plc values where type = opcua and url = opc.tcp://uademo.prosysopc.com:53530/OPCUA/SimulationServer \
    and node = "ns=3;i=1002" and include = name
```

### 2. Declare the aggregation

```anylog
set aggregations where dbms = nov and table = table_2 and time_column = timestamp and value_column = random
```

### 3. (Optional) Replace raw data with aggregated data

```anylog
set aggregations encoding where dbms = nov and table = table_2 and encoding = bounds
```

### 4. Start the OPC-UA client

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

### 5. Validate

```anylog
get plc client
get aggregations
get aggregations where dbms = nov and table = table_2
get streaming
get operator
```

### 6. Query aggregated results

```anylog
run client () sql nov format = table \
    select timestamp::ljust(19), end_interval::ljust(19), min_val, max_val, avg_val, events \
    from bounds_table_2 order by timestamp desc limit 10
```

---

## Policy-based tag management

For large OPC-UA deployments, generate policies for each tag and store them on the blockchain. This lets AnyLog automatically map incoming data to the correct tables.

### Generate and publish policies

```anylog
# Generate policy file (includes schema if schema = true)
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server \
    and format = policy and schema = true \
    and node = "ns=2;s=DeviceSet" and class = variable \
    and dbms = my_dbms \
    and target = "local = true and master = !master_node" \
    and output = !tmp_dir/my_file.out

# Publish to blockchain
process !tmp_dir/my_file.out
```

### Generate and run the data pull command

```anylog
# Generate run_client command file (table derived from policies)
get opcua struct where url = opc.tcp://127.0.0.1:4840/freeopcua/server \
    and format = run_client \
    and node = "ns=2;s=DeviceSet" and class = variable \
    and output = !tmp_dir/my_run_cmd.out \
    and dbms = my_dbms and frequency = 3 and name = opcua_nov

# Execute
process !tmp_dir/my_run_cmd.out
```