---
title: PLCs
description: How AnyLog connects to PLCs — supported protocols, the shared command pattern, and how to map incoming reads into tables.
layout: page
source_path: "01 PLC Overview.md"
---

<!---
### 📜 Change Log

| **Date**   | **Name** | **Change**       | **Version** |
|------------|--|------------------|----------|
| 2026-08-08 | Ori Shadmon | Created document | 2.1.XX |

--->

## How AnyLog Defines a PLC

A **PLC** (Programmable Logic Controller), is any industrial controller or field device that  exposes its data through 
one of AnyLog's supported client protocols. AnyLog does not care whether the source is a traditional PLC, an RTU, an 
outstation, or a sensor gateway — if it speaks **Modbus TCP**, **OPC-UA**, **EtherNet/IP**, or **DNP3**, AnyLog can act 
as a client against it.

Every PLC client, regardless of protocol, follows the same shape:

- AnyLog connects to the device over the network (`hostname`/`port` or `url`, depending on the protocol).
- Points on the device — coils, registers, tags, or DNP3 points — are read on a schedule (`frequency`).
- Each read is normalized into JSON and streamed into a local operator database table.

Because every protocol funnels into that same shape, the table structure, mapping logic, and command patterns
described below are shared across all four — only the connection keywords (Section 3) differ per protocol.

* <a href="./02-%20Modbus.md" target="_blank">Modbus TCP</a> - Reading coils, discrete inputs, and holding/input registers from Modbus TCP devices.
* <a href="./03-%20OPC-UA.md" target="_blank">OPC-UA</a> | Traversing an OPC-UA server's node tree and reading tag values.
* <a href="./04-%20EtherIP.md" target="_blank">EtherNet/IP</a> | Reading CIP object tags from PLCs and controllers over EtherNet/IP.
* <a href="./05-%20DNP3.md" target="_blank">DNP3</a> | Acting as a DNP3 master against outstations over TCP or TLS. |

## Standard Command Format:

Keywords common to every protocol:

| Keyword | Details |
|---|---|
| `type` | Selects the protocol: `modbus`, `opcua`, `etherip`, or `dnp3`. |
| `name` | A unique client name — also used to derive table names under dynamic ingest. |
| `frequency` | Poll interval (seconds, or a fraction of a second expressed in Hz). |
| `dbms` | Target database for the ingested rows. |
| `table` | Wide-table ingest; omit when using `dynamic = true`. |
| `dynamic` | `true` writes each mapped point to its own table instead of one wide table. |
| `map` / `nodes` | The points to read — a JSON array of point definitions, or a list of tag names depending on protocol. |
| `namespace`, `master_node` | Optional Unified Namespace registration (Modbus and DNP3; requires `dynamic = true`). |

The connection keywords themselves are protocol-specific — for example, Modbus and DNP3 use `hostname`/`port`,
while OPC-UA and EtherNet/IP use `url`; DNP3 adds `master_id`/`outstation_id`, Modbus adds `device_id`. See each
protocol's page for its full keyword table.

<<<<<<< HEAD
* View the data that's accessible via the PLC 
=======
* View the data that's accessible via the PLC
>>>>>>> origin/os-dev

```anylog
get <plc type - opcua | etherip> struct where url = opc.tcp://10.0.0.111:53530/OPCUA/SimulationServer
```

* View current value based on the _map_ of _node_

```anylog
<get plc values where type = <plc type - opcua | etherip | modbus | dnp3> and
    hostname = 192.168.1.72 and
    port = 1502 and
    device_id = 1 and
    map|nodes = [{"name":"sensor_1","register":0}]>
```

* (Continuously) pull content and store into table
```anylog
<run plc client where
    type = opcua and name = <plc type - opcua | etherip | modbus | dnp3> and
    url = [connect string] and
    frequency = [seconds] and
    dbms = [dbms] and
    node = [node id]>
```

## Generic Command Pattern

`run plc client` service, by default converts the _tags_ into column names of the table.
Alternatively, the metadata can be converted into mapping, so data can be store in  a more consistent format.

**Example I**:

1. A _PLC_ publishes data with tags: `timestamp`, `duration`, `DelayTimer.ACC`, `DelayTimer.PRE`,
`CycleCounter.ACC` and `CycleCounter.PRE`, with data looking like:

```json
{
   "timestamp": "'2026-08-08T18:23:34.709272Z'",
   "duration": 0,
   "DelayTimer.ACC": 140,
   "DelayTimer.PRE": 2105,
   "CycleCounter.ACC": 949,
   "CycleCounter.PRE": 2341
}
```

2. Initiate a `run plc client`

```anylog
<run plc client where
    type = etherip and
    name = device1 and
    url = 10.10.1.19,1,0 and
    frequency = 10 and
    dbms = my_db and
    table = my_data and
    nodes = ["DelayTimer.ACC", "DelayTimer.ACC", "CycleCounter.ACC", "CycleCounter.PRE"]]>
```

3. Data would be stored in logical database `my_db` and table `my_data`
```sql
CREATE TABLE my_data (
   row_id SERIAL PRIMARY KEY,
   insert_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   tsd_name character(3),
   tsd_id integer,
   timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
   DelayTimer_ACC INT,
   DelayTimer_PRE INT,
   CycleCounter_ACC INT,
   CycleCounter_PRE INT
);

# Row
| row_id | insert_timestamp            | tsd_name | tsd_id | timestamp                   | DelayTimer_ACC | DelayTimer_PRE | CycleCounter_ACC | CycleCounter_PRE |
|      1 | 2026-08-08T18:23:35.709272Z |        0 |      0 | 2026-08-08T18:23:34.709272Z |            140 |           2105 |              494 |             2341 |
```

That works, but it doesn't scale: every new tag on the device means a new column, and structurally identical
tags (`DelayTimer` and `CycleCounter` are both "a monitor with an ACC and a PRE value") end up as unrelated
columns instead of related rows.

**Example 2**: A **mapping policy** reshapes the same read into a narrower, repeating structure — one row per monitor instead
of one row per poll:

1. Define a mapping policy

```anylog
<new_policy = {"mapping": {
    "id": "123",
    "dbms": "my_dbms",
    "table": "my_table",
    "readings": "",
    "params" : [
		["DelayTimer", "[DelayTimer.ACC]", "[DelayTimer.PRE]"],
		["CycleCounter", "[CycleCounter.ACC]", "[CycleCounter.PRE]"]
		],

    "schema": {
        "timestamp": {
            "type": "timestamp",
            "default": "now()",
            "bring": "[timestamp]"
        },
        "Monitor_ID": {
          "type": "str",
          "default": "params.0"
        },
	"ACC": {
          "type": "int",
          "default": null,
          "bring": "params.1"
        },
	"PRE": {
          "type": "int",
          "default": null,
          "bring": "params.2"
        }

    }
}}>

blockchain insert where policy=!policy_id and local=true and master=!ledger_conn
```
> The policy's `params` list defines each output row as a group of source fields — here, each group is
> `[monitor_id, ACC field, PRE field]`. The `schema` block then defines the table's columns and, for each
> column, where its value comes from: either lifted straight from the reading (`bring`) or taken positionally
> from `params` (`params.0`, `params.1`, ...).

<<<<<<< HEAD
2. Initiate a `run plc client` - Once the policy is published, reference it by ID on `run plc client` instead of (or 
=======
2. Initiate a `run plc client` - Once the policy is published, reference it by ID on `run plc client` instead of (or
>>>>>>> origin/os-dev
alongside) an inline `map`:

```anylog
run plc client where type = <protocol> and <connection keywords> and
    frequency = <interval> and
    name = <unique client name> and
    dbms = <target dbms> and
    nodes= ["DelayTimer.ACC", "DelayTimer.PRE", "CycleCounter.ACC", "CycleCounter.PRE"]
    policy = 123
```

3. Data would be stored in logical database `my_db` and table `my_data`

```sql
CREATE TABLE <table_name> (
   timestamp DATETIME,
   monitor_id VARCHAR,
   ACC        INT,
   PRE        INT
);

# Row
| row_id | insert_timestamp            | tsd_name | tsd_id | timestamp                   | monitor_id   | ACC | PRE  |
|      1 | 2026-08-08T18:23:35.709272Z |        0 |      0 | 2026-08-08T18:23:34.709272Z | DelayTimer   | 140 | 2105 |
|      2 | 2026-08-08T18:23:35.709272Z |        0 |      0 | 2026-08-08T18:23:34.709272Z | CycleCounter | 494 | 2341 |
```
