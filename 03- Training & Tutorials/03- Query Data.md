---
title: "Querying the Data"
description: "A quick run through for querying the data"
layout: page
source_path: "training/03- Query Data.md"
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**            |
 |------------|----------------|------------------|
 | 2026-07-24 | Ori Shadmon    | create file      |
--->

# Querying the Data

Once the network is running, there are two types of data sets of interest to the user:

* **Metadata** — the content stored in the blockchain: information about the agents in the network and their role,
  which tables and databases are part of the network, and where that data resides.
* **The actual data** — retrieved by "connecting" from a query node to the node(s) that hold the data, using a SQL
  command.

## Metadata Commands

**`get data nodes`** — shows a clean view of what data exists and where it resides.

```anylog
get data nodes
```

> **Note:** the example below uses anonymized company/node names and placeholder IPs; a real network's output will
> look the same in structure, just with your own deployment's values.

```
Company    DBMS          Table            Cluster ID                        Cluster Status  Node Name          Member ID  External IP/Port     Local IP/Port  Main  Node Status
---------  ------------  ---------------  --------------------------------  --------------  -----------------  ---------  -------------------  -------------  ----  -----------
Acme Co    monitoring     syslog          a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4  active          site-operator-1    101        10.0.1.11:32148                     +     active
                                          f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3  active          site-operator-2    102        10.0.1.12:32148                     +     active
Acme Co    telemetry      device_logs     a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4  active          site-operator-1    101        10.0.1.11:32148                     +     active
                                          f6e5d4c3b2a1f6e5d4c3b2a1f6e5d4c3  active          site-operator-2    102        10.0.1.12:32148                     +     active
Contoso    monitoring     syslog          9a8b7c6d5e4f9a8b7c6d5e4f9a8b7c6d  active          plant-operator-1   201        10.0.2.21:32148                     +     active
                                          (backup)                          active          plant-operator-1-bkup  202    10.0.2.22:32148                     -     active
Contoso    process_data   turbine_pitch   9a8b7c6d5e4f9a8b7c6d5e4f9a8b7c6d  active          plant-operator-1   201        10.0.2.21:32148                     +     active
...
```

* **`blockchain get *`** — view all metadata on the blockchain.
* **`blockchain get [policy type]`** — list all metadata of a given policy type (e.g. `operator`, `cluster`, `table`).

A more thorough set of documentation regarding querying the Blockchain / Metadata can be found [here](../08-%20Blockchain%20&%20Metadata).

---

## Query

Since data is distributed across the network, prefix the SQL command with `run client ()` so the node knows to send
the request against the network rather than run it locally. The network automatically determines where the data
resides and extracts the results. (The parentheses in `run client ()` are reserved for optionally targeting specific
nodes/clusters — leave them empty to query the whole network.)

**Supported functionality:**

| Function | Description |
|---|---|
| raw | Specific column(s), or all columns via `*` |
| `min` | Minimum value of a column |
| `max` | Maximum value of a column |
| `avg` | Average value of a column |
| `count` | Row count |
| `WHERE` | Filter rows by condition |
| `ORDER BY` | Sort results |

### Examples

**Raw select:**

```anylog
run client () sql my_dbms "SELECT timestmap, device_id, temperature, humidity FROM sensor_data"
```

```
timestamp            device_id   temperature   humidity
--------------------  ----------  ------------  --------
2026-07-24 09:00:01   sensor-01   21.4          48.2
2026-07-24 09:00:01   sensor-02   22.1          46.9
2026-07-24 09:00:02   sensor-01   21.5          48.0
```

**Aggregates + `WHERE` + `ORDER BY`:**

```anylog
run client () sql my_dbms "SELECT device_id, min(temperature), max(temperature), avg(temperature), count(*) 
FROM sensor_data WHERE device_id = 'sensor-01' ORDER BY device_id"
```

```
device_id   min(temperature)   max(temperature)   avg(temperature)   count(*)
----------  -----------------  -----------------  -----------------  --------
sensor-01   19.8               23.6               21.42              1440
```

### Via REST

```shell
# cURL GET — note `destination: network` replaces `run client ()`
curl -X GET http://[Node ip]:[Node port] \
  -H 'command: sql my_dbms "SELECT * FROM sensor_data"' \
  -H "AnyLog-Agent: AnyLog/1.23" \
  -H "destination: network"

# cURL POST
curl -X POST http://[Node ip]:[Node port] \
  -H "Content-Type: application/json" \
  -H "AnyLog-Agent: AnyLog/1.23" \
  -H "destination: network" \
  -d '{"command": "sql my_dbms \"SELECT * FROM sensor_data\""}'
```

A more thorough set of documentation regarding querying the SQL can be found [here](../05-%20Northbound%20Connectors/01-%20Northbound%20Connectors.md).