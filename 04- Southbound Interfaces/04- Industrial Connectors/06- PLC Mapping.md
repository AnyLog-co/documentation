---
title: PLC Mapping Policies
description: Define what to read from an industrial device and how to store it, in one policy reusable across EtherNet/IP, OPC-UA, Modbus TCP, and DNP3.
layout: page
source_path: "06 PLC Mapping Policies.md"
---

<!---
### 📜 Change Log

| **Date**   | **Name** | **Change**       | **Version** |
|------------|--|------------------|----------|
| 2026-11-04 |  | Created document |  |
| 2026-11-05 | Ori Shadmon | based on AB-266/267 tentative document on the mapping policy | TBD |

--->

## Overview

Every industrial client in AnyLog uses the same `run plc client` command, whatever the protocol:
[EtherNet/IP](04-%20EtherIP.md), [OPC-UA](03-%20OPC-UA.md), [Modbus TCP](02-%20Modbus.md), or [DNP3](05-%20DNP3.md).
On each poll the client reads a set of tags or points and produces one flat JSON **reading**. The reading has one
key per point, plus two keys the client adds itself:

* `timestamp`: the earliest source timestamp among the values read.
* `duration`: the spread, in milliseconds, between the earliest and latest timestamps in that poll. It is `0` when
  the protocol doesn't timestamp individual values.

A **mapping policy** describes how that reading is turned into rows: the destination database and table, the table
schema, and how each value is placed. For `run msg client`, that is the whole policy. A PLC connection also needs
to know **what to read**, so a PLC mapping adds the read list: `nodes` and/or `map`. The `params` block then ties the
points that are read to rows in the table.


### Why one mapping can hold several read lists

The table describes the *equipment* (a power monitor, a pump, an I/O channel), not the protocol used to reach it.
The same equipment is often reachable in more than one way:

* **Multi-protocol devices.** Many I/O modules, meters, and gateways expose the same values over EtherNet/IP *and*
  Modbus TCP, or Modbus *and* DNP3.
* **Mixed fleets.** The same device model may be reached over EtherNet/IP at one site and over Modbus at another,
  depending on the network or which licenses are installed.
* **Migration.** Moving a site from one protocol to another, or from a gateway to direct device access, should not
  change the tables, queries, or dashboards built on top of them.

Keeping one mapping with one read list per protocol means `params` and `schema` are defined once. Whichever
protocol a client uses, it writes **identical rows into an identical table**. The client picks the read list that
matches its `type` and ignores the others.

---

## Policy structure

```json
{"mapping": {
    "id":        "<policy id>",
    "dbms":      "<database>",
    "table":     "<table>",
    "readings":  "",
    "nodes":     [ ... ],
    "map":       [ ... ],
    "params":    [ ... ],
    "schema":    { ... }
}}
```

| Key | Required | Purpose |
|---|---|---|
| `id` | Yes | Referenced by `policy = <id>` on the client. Also the default client name. |
| `dbms`, `table` | Yes | Destination of the rows. |
| `readings` | Yes | Path to the readings inside the incoming JSON. Always `""` for PLC clients, since the reading is the top-level object. |
| `nodes` | For EtherNet/IP and OPC-UA | Tags (EtherNet/IP) or node IDs (OPC-UA) to read. |
| `map` | For Modbus and DNP3 | Points to read, each with a `name` and an address. |
| `params` | Yes | Row definitions. **Each group produces one row per poll.** |
| `schema` | Yes | Output columns: type, default, and where each value comes from. |

AnyLog adds `date` and `ledger` when the policy is inserted.

### The read list: `nodes` or `map`

The client chooses the read list from the policy based on the connection `type`:

| `type` | Read list | Each entry is | Key it produces in the reading |
|---|---|---|---|
| `etherip` | `nodes` | A tag name, such as `BCT.RealPower` | The tag name |
| `opcua` | `nodes` | A node ID, such as `ns=3;i=1002` | The node's name, such as `random` |
| `modbus` | `map` | `{"name": ..., "register" \| "inputRegister" \| "coil" \| "input": <address>}` | `name` |
| `dnp3` | `map` | `{"name": ..., "type": ..., "index": ...}` or `group` + `variation` | `name` |

For one policy to work over several protocols, every read list must produce **the same reading keys**. For
example, name each `map` entry exactly like the corresponding EtherNet/IP tag.

EtherNet/IP and OPC-UA both use `nodes`, so one policy cannot hold read lists for both of them. For a device
reachable over both, use one policy per protocol with the same `params` and `schema`.

The read list is explicit, not derived from `params`, because `params` refers to **reading keys** and those don't
always identify what to read. On OPC-UA the key is a node name, not the node ID. On Modbus and DNP3 the key is a
label, and the address only exists in `map`.

### Rows: `params`

`params` is a list of **groups**. Each group becomes one row per poll. By convention:

* Element 0 is a literal identifier for the row, such as `"BCT"` or `"feeder_a"`.
* The remaining elements are `[key]` references into the reading.

```json
"params": [
    ["BCT", "[BCT.Frequency]", "[BCT.RealPower]"],
    ["BF1", "[BF1.Frequency]", "[BF1.RealPower]"]
]
```

Every group must have the same shape, because the same `schema` is applied to each one.

### Columns: `schema`

Each column has a `type`, a `default`, and optionally a `bring`:

| Expression | Resolves to | Example |
|---|---|---|
| `"bring": "[timestamp]"` | The key `timestamp` in the reading | The poll's timestamp |
| `"bring": "params.2"` | Position 2 of the current group (`"[BCT.RealPower]"`), which is then looked up in the reading | `412.7` |
| `"default": "params.0"` | Position 0 of the current group, used **as is** | `"BCT"` |
| `"default": null` | Used when the `bring` lookup finds nothing | `NULL` |

Identifier columns use `default` instead of `bring` because element 0 is a literal and there is nothing to look up.

Supported types: `timestamp`, `str`, `int`, `float`, `bool`.


## Designing a mapping

1. **Find the repeating unit.** This could be a monitor, a pump, a feeder, or an I/O channel. Each unit becomes one
   group in `params` and one row per poll.
2. **List the measurements per unit.** These become the `schema` columns and positions 1..N in each group.
3. **Pick an identifier column.** Position 0 of each group, read with `"default": "params.0"`.
4. **Match types to the device.** Check the controller's data types (BOOL, INT, DINT, REAL/Float32). Declaring a
   REAL as `int` truncates it; a power factor of 0.94 becomes 0.
5. **Build the read lists.** List every point referenced in `params` in `nodes`, `map`, or both, depending on which
   protocols the device supports. Name `map` entries the same as the `nodes` tags.
6. **Publish, start, verify.** Insert the policy, start the client with `type`, the connection keywords, and
   `policy`, then query the table.

### Sample: one mapping, two protocols

An I/O module exposes three analog inputs over both EtherNet/IP and Modbus TCP. The `nodes` tags and the `map`
names are identical, so `params` and `schema` don't care which protocol produced the reading.

```anylog
<new_policy = {"mapping": {
    "id": "edge_io",
    "dbms": "mydb",
    "table": "edge_io",
    "readings": "",
    "nodes": ["AI1.Value", "AI2.Value", "AI3.Value"],
    "map": [
        {"name": "AI1.Value", "inputRegister": [0, 1], "datatype": "float32"},
        {"name": "AI2.Value", "inputRegister": [2, 3], "datatype": "float32"},
        {"name": "AI3.Value", "inputRegister": [4, 5], "datatype": "float32"}
    ],
    "params": [
        ["AI1", "[AI1.Value]"],
        ["AI2", "[AI2.Value]"],
        ["AI3", "[AI3.Value]"]
    ],
    "schema": {
        "timestamp":  {"type": "timestamp", "default": "now()", "bring": "[timestamp]"},
        "channel_id": {"type": "str",   "default": "params.0"},
        "value":      {"type": "float", "default": null, "bring": "params.1"}
    }
}}>

blockchain insert where policy = !new_policy and local = true and master = !ledger_conn
```

Tag names and register addresses are illustrative. Use the device's own tag list and register map. A Float32 spans
two Modbus registers, and `"datatype": "float32"` tells the client to combine them.

### Reusing the mapping: change only the connection

Only `type` and the connection keywords change between commands. The policy stays the same:

```anylog
# EtherNet/IP: the client reads "nodes"
<run plc client where type = etherip and url = 10.10.1.50 and
   name = edge-io-eip and frequency = 5 and policy = edge_io>

# Modbus TCP: the client reads "map"
<run plc client where type = modbus and hostname = 10.10.1.50 and port = 502 and device_id = 1 and
   name = edge-io-mb and frequency = 5 and policy = edge_io>
```

Both write the same rows into `mydb.edge_io`:

| timestamp | channel_id | value |
|---|---|---|
| 2026-11-05T17:00:00Z | AI1 | 23.4 |
| 2026-11-05T17:00:00Z | AI2 | 4.12 |
| 2026-11-05T17:00:00Z | AI3 | 101.7 |

Run one client per device, not both. Two clients against the same device write every value twice. If the device
sends a scaled integer over Modbus (234) but engineering units over EtherNet/IP (23.4), the two protocols won't
produce the same numbers. Check this before switching protocols.

---

## Example: power plant power monitors

A Rockwell ControlLogix controller (`10.10.1.19`) collects readings from the plant's power monitors. Each monitor
(`BCT`, `BF1`, `BF2`, ...) exposes the same 12 tags, and the measurements are Float32. The goal is one table,
`cos.pp_pm`, with one row per monitor per poll.

1. Define and publish the mapping

The example shows two monitors. Each additional monitor adds 12 entries to `nodes` and one group to `params`.

```anylog
<new_policy = {"mapping": {
    "id": "power_monitors",
    "dbms": "cos",
    "table": "pp_pm",
    "readings": "",
    "nodes": [
        "BCT.CommsStatus", "BCT.EnergyMultiplier", "BCT.Frequency", "BCT.PowerFactor",
        "BCT.ReactivePower", "BCT.RealPower", "BCT.A_Current", "BCT.A_N_Voltage",
        "BCT.B_Current", "BCT.B_N_Voltage", "BCT.C_Current", "BCT.C_N_Voltage",
        "BF1.CommsStatus", "BF1.EnergyMultiplier", "BF1.Frequency", "BF1.PowerFactor",
        "BF1.ReactivePower", "BF1.RealPower", "BF1.A_Current", "BF1.A_N_Voltage",
        "BF1.B_Current", "BF1.B_N_Voltage", "BF1.C_Current", "BF1.C_N_Voltage"
    ],
    "params": [
        ["BCT", "[BCT.CommsStatus]", "[BCT.EnergyMultiplier]", "[BCT.Frequency]", "[BCT.PowerFactor]",
                "[BCT.ReactivePower]", "[BCT.RealPower]", "[BCT.A_Current]", "[BCT.A_N_Voltage]",
                "[BCT.B_Current]", "[BCT.B_N_Voltage]", "[BCT.C_Current]", "[BCT.C_N_Voltage]"],
        ["BF1", "[BF1.CommsStatus]", "[BF1.EnergyMultiplier]", "[BF1.Frequency]", "[BF1.PowerFactor]",
                "[BF1.ReactivePower]", "[BF1.RealPower]", "[BF1.A_Current]", "[BF1.A_N_Voltage]",
                "[BF1.B_Current]", "[BF1.B_N_Voltage]", "[BF1.C_Current]", "[BF1.C_N_Voltage]"]
    ],
    "schema": {
        "timestamp":        {"type": "timestamp", "default": "now()", "bring": "[timestamp]"},
        "monitor_id":       {"type": "str",   "default": "params.0"},
        "commsstatus":      {"type": "bool",  "default": null, "bring": "params.1"},
        "energymultiplier": {"type": "int",   "default": null, "bring": "params.2"},
        "frequency":        {"type": "float", "default": null, "bring": "params.3"},
        "powerfactor":      {"type": "float", "default": null, "bring": "params.4"},
        "reactivepower":    {"type": "float", "default": null, "bring": "params.5"},
        "realpower":        {"type": "float", "default": null, "bring": "params.6"},
        "a_current":        {"type": "float", "default": null, "bring": "params.7"},
        "a_n_voltage":      {"type": "float", "default": null, "bring": "params.8"},
        "b_current":        {"type": "float", "default": null, "bring": "params.9"},
        "b_n_voltage":      {"type": "float", "default": null, "bring": "params.10"},
        "c_current":        {"type": "float", "default": null, "bring": "params.11"},
        "c_n_voltage":      {"type": "float", "default": null, "bring": "params.12"}
    }
}}>

blockchain insert where policy = !new_policy and local = true and master = !ledger_conn
```

> **Tip:** to build `nodes` for a large controller, list its tags with
> `get etherip struct where url = 10.10.1.19 and format = get_value` and copy the relevant names.

2. Start the client

The customer chose EtherNet/IP because the AnyLog agent and the PLC sit on the same network, so the agent can read
the controller's tags directly. If the agent had been on a different network, for example an IT network or a
remote site, OPC-UA would have been the better fit, since it adds encryption and authentication on the connection.

```anylog
# etherIP 
<run plc client where type = etherip and url = 10.10.1.19 and
   name = pp-pm and frequency = 10 and policy = power_monitors>
 
# OPC-UA    
<run plc client where type = opcua and url = opc.tcp://10.10.1.19:4840 and
  name = pp-pm and frequency = 10 and policy = power_monitors_opcua>
```

3. Verify

```anylog
get plc client
get streaming
get operator
run client () sql cos format = table "select * from pp_pm order by timestamp desc limit 4"
```

Each poll writes one row per monitor, all sharing the poll's timestamp:

| timestamp | monitor_id | commsstatus | frequency | powerfactor | realpower | a_current | ... |
|---|---|---|---|---|---|---|---|
| 2026-11-05T17:00:10Z | BCT | true | 59.98 | 0.94 | 412.7 | 88.2 | ... |
| 2026-11-05T17:00:10Z | BF1 | true | 59.99 | 0.91 | 390.2 | 81.0 | ... |
| 2026-11-05T17:00:00Z | BCT | true | 59.98 | 0.94 | 411.9 | 88.0 | ... |
| 2026-11-05T17:00:00Z | BF1 | true | 60.00 | 0.91 | 389.6 | 80.8 | ... |


