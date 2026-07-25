---
title: EtherNet/IP
description: Configure AnyLog as an EtherNet/IP client to pull data from industrial PLCs and controllers continuously.
layout: page
source_path: "EtherNet IP.md"
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-07-14 | Merged the two overlapping EtherNet/IP docs (etherip.md and EtherNet IP.md) into this single file.
              Backbone is etherip.md (the current, house-style version). Folded in two genuine additions from
              EtherNet IP.md: the CIP object-model explanation (Identity/Assembly/Connection Object examples,
              class→instance→attribute hierarchy) and a concrete example of the CREATE TABLE output produced
              by `schema = true`. Left out, not "fixed": EtherNet IP.md's format-options table incorrectly
              described `tree` as "the OPC-UA tree structure" (contradicting its own earlier statement that
              EtherNet/IP is explicitly not tree-structured like OPC-UA), and its Get/Run PLC Values sections
              described `url`/`user`/`password` as OPC-UA server parameters in an EtherNet/IP document — both
              look like leftover artifacts from an OPC-UA doc this one was templated from, not real content.
-->

EtherNet/IP (Ethernet Industrial Protocol) is an industrial network protocol built on the Common Industrial Protocol (CIP) that enables communication between PLCs, sensors, actuators, and control systems over standard Ethernet. AnyLog can act as an EtherNet/IP client, pulling data from any EtherNet/IP device and streaming it into local databases.

---

## The EtherNet/IP structure

EtherNet/IP organizes industrial automation data through a set of well-defined CIP objects, which represent device attributes, configurations, and runtime data. Unlike OPC-UA's tree-based address space, EtherNet/IP uses a flat, object-oriented structure where each device exposes standard or vendor-specific CIP classes, instances, and attributes — accessed via CIP messaging over Ethernet.

Each class (for example, an Identity Object, Assembly Object, or Connection Object) may contain multiple instances, and each instance can expose multiple attributes, forming a structured view of the device's capabilities and status. The structure isn't hierarchical like OPC-UA's, but it provides a standardized way to navigate and interact with device data.

## Explore the device

### Traverse the tag structure

The `get etherip struct` command queries the device to discover supported tags, program tags, and system-level data — both system-level and user-defined.

```anylog
get etherip struct where url = [connect string] and [options]
```

Key options:

| Option | Description |
|---|---|
| `url` | IP address of the target PLC or EtherNet/IP device |
| `slot` | Slot number of the target controller (multi-slot chassis) |
| `user` / `password` | Credentials if the device requires authentication |
| `limit` | Limit the number of tags or objects returned |
| `prefix` | Filter tags to those matching the given path prefix |
| `format` | Output format (see below) |
| `output` | Write output to a file instead of stdout |
| `schema` | If `true`, includes the table schema for each tag |
| `dbms` / `table` | Used when generating `run_client` or `policy` output |
| `frequency` | Used when generating `run_client` output (in Hz) |
| `name` | Process name when using `format = run_client` |
| `target` | Variables for `blockchain insert` commands (used with `format = policy`) |

**Format options:**

| Format | Output |
|---|---|
| `tree` | EtherNet/IP tag structure (default) |
| `get_value` | Generates `get plc values` commands for visited tags |
| `run_client` | Generates `run plc client` commands for visited tags |
| `policy` | Generates a policy per tag; combine with `target` for `blockchain insert` commands |

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

---

## Continuous data pull

Stream data from an EtherNet/IP device into the local database continuously:

```anylog
run plc client where type = etherip and name = [unique name] and url = [connect string] and frequency = [seconds] and dbms = [dbms] and table = [table] and node = [tag name]
```

| Option | Description |
|---|---|
| `name` | Unique client name |
| `frequency` | Read frequency in seconds, or in Hz (e.g. `10 hz`) |
| `node` / `nodes` | One or more tag names |
| `policy` | Use a policy to determine tags and table (alternative to specifying nodes inline) |
| `topic` | Route data through the local broker |

Each row is stored with two columns added automatically:
- `timestamp` — earliest source timestamp of the values in this read (falls back to the server timestamp if the source timestamp is missing)
- `duration` — milliseconds between the earliest and latest timestamp in this read

Examples:
```anylog
# Individual tags
run plc client where type = etherip and name = etherip_reads and url = 127.0.0.1 \
    and frequency = 1 and dbms = my_dbms \
    and node = FreeChlorinatorAI.PV and node = CombinedChlorinatorAI.PV

# Tag list
<run plc client where type = etherip and name = etherip_reads and url = 127.0.0.1 \
    and frequency = 1 and dbms = my_dbms \
    and nodes = ["BOOL","SINT","INT","DINT","REAL","STRING","STRUCT.Temp","STRUCT.Status",
                 "ARRAY_INT","ARRAY_BOOL","ARRAY_STRING","TIMER.ACC","TIMER.PRE",
                 "COUNTER.ACC","COUNTER.PRE","DATE_TIME","ATSNormalRdyDI",
                 "CombinedChlorinatorAI.PV","FreeChlorinatorAI.PV"]>
```

Multiple EtherNet/IP clients can run on the same node simultaneously.

### Check client status
```anylog
get plc client
```

### Stop a client
```anylog
exit plc client [client name]
exit plc all
```

---

## Policy-based tag management

For large EtherNet/IP deployments, generate policies for each tag and publish them to the blockchain. This lets AnyLog automatically map incoming data to the correct tables without specifying nodes inline — the policies serve as a mapping between table names and tag information (and vice versa), so incoming data can be interpreted and organized automatically, in line with the defined structure, for querying, validation, and distribution across the network.

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

If `schema = true`, the output also includes, for every tag, a `table` policy with the `CREATE TABLE` statement for that tag's table:

```json
{"table": {"name": "t109",
           "dbms": "my_dbms",
           "create": "CREATE TABLE IF NOT EXISTS t109(row_id SERIAL PRIMARY KEY, insert_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
           tsd_name CHAR(3), tsd_id INT, timestamp timestamp not null default now(), value varchar );
           CREATE INDEX t109_timestamp_index ON t109(timestamp); CREATE INDEX t109_insert_timestamp_index ON t109(insert_timestamp);",
           "source": "ETHERIP Interface"}}
```

### 2. Generate and run the data pull command

```anylog
# Generate run_client command file (table derived from policies — no table= needed)
get etherip struct where url = 127.0.0.1 and format = run_client \
    and frequency = 1 and name = etherip_reads and dbms = my_dbms \
    and output = !tmp_dir/my_run_cmd.out

# Execute
process !tmp_dir/my_run_cmd.out
```

This pulls data continuously and assigns each tag's values to the correct table based on the published policies — the table name is derived from the policies (namespace and node ID) rather than needing to be specified on the command line.