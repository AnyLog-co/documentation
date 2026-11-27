---
title: "EtherNet/IP"
description: "Configure AnyLog as an EtherNet/IP client to pull data from industrial PLCs and controllers continuously."
layout: page
source_path: "03 EtherNet IP.md"
---

<!---
### 📜 Change Log
| **Date**   | **Name** | **Change**       | **Version** |
 |------------|--|------------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-11-27 | Massimiliano Pinto | Addition of UNS and examples | |
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
<get etherip struct where
    url = [connect string] and
    user = [username] and
    password = [password] and
    ...
>
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
<get etherip struct where
    url = 127.0.0.1:44818 and
    read = true
>
```

Output:

```text
Index Name                        Key                         Type Value             Error
-----|---------------------------|---------------------------|----|-----------------|-----|
    1|SystemReadyFlag            |SystemReadyFlag            |    |True             |     |
    2|WeatherReadings.temperature|WeatherReadings.temperature|    |            54.18|     |
    3|LargeRangeInt              |LargeRangeInt              |    |        766159627|     |
```

```anylog
# Generate a get plc values command
<get etherip struct where
    url = 127.0.0.1:44818 and
    format = get_value
>
```

Output:

```anylog
# The get plc values command for the same tags
<get plc values where
    type = etherip and
    url = 127.0.0.1:44818 and
    nodes = ["SystemReadyFlag",
             "WeatherReadings.temperature",
             "LargeRangeInt"]
>
```



```anylog
# Generate a get plc values command for all tags under a prefix
<get etherip struct where
    url = 127.0.0.1:44818 and
    prefix = WeatherReadings and
    format = get_value
>
```

Output:

```anylog
<get plc values where
    type = etherip and
    url = 127.0.0.1:44818 and
    nodes = ["WeatherReadings.temperature",
             "WeatherReadings.humidity",
             "WeatherReadings.pressure",
             "WeatherReadings.wind_speed",
             "WeatherReadings.wind_direction",
             "WeatherReadings.rain"]
>
```

```anylog

# Generate a run plc client command
<get etherip struct where
    url = 127.0.0.1:44818 and
    format = run_client and
    frequency = 1 and
    name = etherip_reads and
    dbms = my_dbms
>

```

Output:

```anylog
<run plc client where
    type = etherip and
    name = etherip_reads and
    url = 127.0.0.1:44818 and
    frequency = 1 and
    dbms = my_dbms and
    nodes = ["SystemReadyFlag",
             "WeatherReadings.temperature",
             "LargeRangeInt"]
>
```

```anylog
# Generate blockchain insert commands for all tags (includes schema)
<get etherip struct where
    url = 127.0.0.1:44818 and
    format = policy and
    schema = true and
    dbms = my_dbms and
    target = "local = true and master = !master_node" and
    output = !tmp_dir/my_file.out
>
```

Output:

generated policies for tags and tables

---

## Read specified tag values

```anylog
<get plc values where
    type = etherip and
    url = [connect string] and
    node = [tag name]
>
```

Options:

| Option | Description |
|---|---|
| `node` | One or more tag names |
| `nodes` | Comma-separated list of tag names in square brackets |

Examples:

```anylog
<get plc values where
    type = etherip and
    url = 127.0.0.1:44818 and
    node = WeatherReadings.temperature
>
```

Output:

```text
Ethernet/IP Nodes values
Index Name                        Key                         Type Value              Error 
-----|---------------------------|---------------------------|----|------------------|-----|
    1|WeatherReadings.temperature|WeatherReadings.temperature|    |54.15             |     |
```

List format:

```anylog
<get plc values where
    type = etherip and
    url = 127.0.0.1:44818 and
    nodes = ["WeatherReadings.temperature",
             "WeatherReadings.humidity",
             "WeatherReadings.pressure"]
>
```

Output:

```text
Ethernet/IP Nodes values
Index Name                        Key                         Type Value              Error 
-----|---------------------------|---------------------------|----|------------------|-----|
    1|WeatherReadings.temperature|WeatherReadings.temperature|    |54.77             |     |
    2|WeatherReadings.humidity   |WeatherReadings.humidity   |    |80.13             |     |
    3|WeatherReadings.pressure   |WeatherReadings.pressure   |    |1006.25           |     |
```

## The Run PLC Client Command

The command **run plc client*** pulls data from the PLC continuously and streams the data into a database on the local node:

```anylog
<run plc client where
    type = etherip and
    name = [unique name] and
    url = [connect string] and
    frequency = [frequency] and
    dbms = [dbms name] and
    table = [table name] and
    node = [node id]
>
```

The following table summarizes the command variables:

| keyword             | Details                                                                                                                                             |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| name                | A unique connection name.                                                                                                                           |
| url                 | The url specifies the endpoint of the OPC UA server.                                                                                                |
| user                | the username required by the OPC UA server for access.                                                                                              |
| password            | the password associated with the username.                                                                                                          |
| frequency           | Read frequency in seconds or a fraction of seconds using hz (i.e.: 10 hz).                                                                          |
| node                | ID of one or multiple nodes that their value is retrieved.                                                                                          |
| nodes               | Providing a list of nodes, separated by comma, within square brackets.                                                                              |
| policy              | If nodes are not specified on the CLI, the policy determines the nodes and the table to use.                                                        |
| dbms                | The database to host the data (if not specified in a policy).                                                                                       |
| table               | The table to host the data (if not specified in a policy).                                                                                          |
| topic               | If data is processed through the local broker.                                                                                                      |
| auto_uns            | Set `true` to register the tags in the UNS. Requires `master_node`, and a `table` or a tag policy for each tag.                                     |
| master_node         | Required with `auto_uns` (`ip:port`).                                                                                                               |
| uns_prefix          | Optional path in front of each UNS leaf, for example `plant1`. Requires `auto_uns = true`.                                                          |
| group_by_attributes | Optional list of names; stored on each UNS object as `where`. Requires `auto_uns = true`.                                                           |
| constants           | Optional JSON object, for example `{"station_id":"WS-001"}`. Its values are copied onto each stored row when the table has a column with that name. |

Example 1 - listing individual tags:

```anylog
<run plc client where
    type = etherip and
    name = etherip_reads and
    url = 127.0.0.1:44818 and
    frequency = 1 and
    dbms = my_dbms and
    node = FreeChlorinatorAI.PV and
    node = CombinedChlorinatorAI.PV
>
```

Example 2 - providing a list of tags:

```anylog
<run plc client where
    type = etherip and
    name = etherip_reads and
    url = 127.0.0.1:44818 and
    frequency = 1 and
    dbms = my_dbms and
    nodes = ["CombinedChlorinatorAI.PV",
             "FreeChlorinatorAI.PV"]
>
```

Example 3 - fixed table and list of tags:

```anylog
<run plc client where
    type = etherip and
    name = etherip_reads and
    url = 127.0.0.1:44818 and
    frequency = 1 and
    dbms = env_sensor and
    table = eip_weather and
    nodes = ["WeatherReadings.temperature",
             "WeatherReadings.humidity"]
>
```

The table `eip_weather` gets one row per read. Its columns are:

- `timestamp`
- `weatherreadings_temperature`
- `weatherreadings_humidity`

The table also has the standard `row_id`, `insert_timestamp`, `tsd_name`, and `tsd_id` columns.

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
<get etherip struct where
    url = 127.0.0.1:44818 and
    format = policy and
    schema = true and
    dbms = my_dbms and
    target = "local = true and master = !master_node" and
    output = !tmp_dir/my_file.out
>

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
<get etherip struct where
    url = 127.0.0.1:44818 and
    format = run_client and
    frequency = 1 and
    name = etherip_reads and
    dbms = my_dbms and
    output = !tmp_dir/my_run_cmd.out
>

# Execute
process !tmp_dir/my_run_cmd.out
```

This pulls data continuously and assigns each tag's values to the correct table based on the published policies.

### How UNS leaves are created

The UNS path of a tag comes from its name:

1. A dot in the tag name starts a new path level. `Line1.Temp` becomes `Line1/Temp`.
2. If the command has `uns_prefix`, it goes in front of the path, for example `uns_prefix = plant1` gives `plant1/Line1/Temp`.
3. Each part is cleaned the same way as in OPC-UA: it is lowercased, and `-` is replaced by `_`. The example becomes `plant1/line1/temp`.
4. Each level gets one object and one UNS entry. Each entry points to its parent, so the chain runs from the first level to the leaf.
5. The leaf holds the table, the `column` when the table has several columns, and the tag's `node_sid` and `datatype`. If `group_by_attributes` is set, the leaf also holds its `where`.

Stored column names follow the tag name in lower case, with `.` replaced by `_`. `CombinedChlorinatorAI.PV` is stored as `combinedchlorinatorai_pv`. The leaf object name is the UNS path with `/` replaced by `_`, which gives `combinedchlorinatorai_pv` for the same tag. A bool is stored as `0` or `1`.

See [Unified Namespace](../../08-%20Blockchain%20&%20Metadata/04-%20Unified%20Namespace.md) for background.

### Constants and `group_by_attributes`

Both are optional on `run plc client`. Add them to the command with `constants = {...}` and `group_by_attributes = [...]`:

```anylog
constants = {"plc_id":"PLC-1"} and
group_by_attributes = ["plc_id"]
```

* `constants` on the command copies each key onto the stored row when the table has that column, and onto the UNS object when `auto_uns = true`. A value is a string, a number, or a bool. A key already set on the object stays. Tag tables from per-tag policies have `timestamp` and `value` only, so a constant has no column there.
* A constant can also sit in the mapping, as a schema `default` that is not `params.N` and not a `bring`. That value is stored in the column. It is not added as its own key on the UNS object.
* `group_by_attributes` can sit in the mapping or on the command. It requires `auto_uns = true`, and the table has to be named. In the mapping, the `where` is taken from the first row, so a command constant is included, for example `plc_id = 'PLC-1'`. On the command, the `where` is taken only from a literal default, such as `params.0` or a fixed default. A `bring` value is not used, and then the leaf has no `where`.

**Limitation:** without a mapping policy, `group_by_attributes` on the command gets its value only from a PLC tag read in the same command. A value from `constants` is not used in the `where`. If any group field has no value, no leaf gets a `where`. To use a constant in the `where`, put `group_by_attributes` in a mapping policy.

---

## Ingest with UNS (`auto_uns` + `master_node`)

With `auto_uns = true` and `master_node`, the EtherNet/IP ingest is registered in the UNS (object policies on the blockchain). The option is used with `format = run_client`: the generated `run plc client` command copies `auto_uns`, `master_node`, and `group_by_attributes` onto the client. `get etherip struct` accepts these three options only with `format = run_client`. `auto_uns` requires `master_node`, and `group_by_attributes` requires `auto_uns = true`. The options are described in [The Run PLC Client Command](#the-run-plc-client-command).

```anylog
<get etherip struct where
    url = 127.0.0.1:44818 and
    format = run_client and
    frequency = 1 and
    name = etherip_reads and
    dbms = my_dbms and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    output = !tmp_dir/my_run_cmd.out
>
```

### Examples

The examples below were run against a simulator at `url = 127.0.0.1:44818` with `frequency = 2`, `dbms = env_sensor`, and `master_node = 192.168.1.62:32148`. Tag values change on every read. The `BF1` and `BF2` examples use `url = 127.0.0.1:44820`.

**One table, UNS on.** Each node is one column, and each tag is one UNS leaf:

```anylog
<run plc client where
    name = eip_on and
    table = etherip_weather and
    auto_uns = true and
    type = etherip and
    url = 127.0.0.1:44818 and
    frequency = 2 and
    dbms = env_sensor and
    master_node = 192.168.1.62:32148 and
    nodes = ["WeatherReadings.temperature",
             "WeatherReadings.humidity",
             "WeatherReadings.pressure",
             "WeatherReadings.wind_speed",
             "WeatherReadings.wind_direction",
             "WeatherReadings.rain"]
>
```

The table `etherip_weather` gets one row per read. Its columns are:

- `timestamp`
- `weatherreadings_temperature`
- `weatherreadings_humidity`
- `weatherreadings_pressure`
- `weatherreadings_wind_speed`
- `weatherreadings_wind_direction`
- `weatherreadings_rain`

The table also has the standard `row_id`, `insert_timestamp`, `tsd_name`, and `tsd_id` columns.

The UNS leaves are:

```text
UNS
└── weatherreadings
    ├── temperature
    ├── humidity
    ├── pressure
    ├── wind_speed
    ├── wind_direction
    └── rain
```

The leaves have no `where`, because this run has no `group_by_attributes`.

This run has no `uns_prefix`, so the leaves sit at the top level of the UNS.  
With `uns_prefix = plant1`, the same tags are stored under it:

```text
plant1
└── weatherreadings
    ├── temperature
    ├── humidity
    ├── pressure
    ├── wind_speed
    ├── wind_direction
    └── rain
```

A UNS entry and its object, for one tag (`WeatherReadings.pressure`) in the `etherip_weather_pre` table. The `uns` part gives the path, and the `object` part holds the tag.

```json
{
  "uns": {
    "name": "pressure",
    "namespace": "plant1/weatherreadings/pressure",
    "object_id": "748d7a7bdb7fd2ac5b9225cbb4d77e30",
    "parent": "9d44bb1810326d39a6890b4eff2a1554",
    "id": "a90ce33b541ff130a862578a6cd73781",
    "date": "2026-11-27T17:23:52.090737Z",
    "ledger": "global"
  },
  "object": {
    "name": "weatherreadings_pressure",
    "etherip": {
      "node_sid": "WeatherReadings.pressure"
    },
    "column": "weatherreadings_pressure",
    "dbms": "env_sensor",
    "table": "etherip_weather_pre",
    "id": "748d7a7bdb7fd2ac5b9225cbb4d77e30",
    "date": "2026-11-27T17:23:52.086789Z",
    "ledger": "global"
  }
}
```

**UNS, Group by monitor_id, weather nodes, one table.** `group_by_attributes` puts a `where` on each leaf, taken from the first read. `monitor_id` is read as a PLC tag, so it is also in `nodes`:

```anylog
<run plc client where
    name = eip_grp and
    table = eip_grp and
    auto_uns = true and
    uns_prefix = weather_grp and
    group_by_attributes = ["monitor_id"] and
    type = etherip and
    url = 127.0.0.1:44818 and
    frequency = 2 and
    dbms = env_sensor and
    master_node = 192.168.1.62:32148 and
    nodes = ["monitor_id",
             "WeatherReadings.temperature",
             "WeatherReadings.humidity",
             "WeatherReadings.pressure",
             "WeatherReadings.wind_speed",
             "WeatherReadings.wind_direction",
             "WeatherReadings.rain"]
>
```

The table `eip_grp` gets one row per read. Its columns are:

- `timestamp`
- `monitor_id`
- `weatherreadings_temperature`
- `weatherreadings_humidity`
- `weatherreadings_pressure`
- `weatherreadings_wind_speed`
- `weatherreadings_wind_direction`
- `weatherreadings_rain`

The UNS leaves sit under `weather_grp`, the `uns_prefix`:

```text
weather_grp
├── monitor_id
└── weatherreadings
    ├── temperature
    ├── humidity
    ├── pressure
    ├── wind_speed
    ├── wind_direction
    └── rain
```

A UNS entry and its object, for one tag (`WeatherReadings.temperature`) in the `eip_grp` table. The `where` comes from `monitor_id`:

```json
{
  "uns": {
    "name": "temperature",
    "namespace": "weather_grp/weatherreadings/temperature",
    "object_id": "cc6e5b21428e19b03c92611f1c9cef14",
    "parent": "5d5f6db424cb0f81d64443647f58a163",
    "id": "57be1e1e85b49759501bd906207b51bb",
    "date": "2026-11-27T17:37:39.649876Z",
    "ledger": "global"
  },
  "object": {
    "name": "weatherreadings_temperature",
    "etherip": {
      "node_sid": "WeatherReadings.temperature"
    },
    "column": "weatherreadings_temperature",
    "dbms": "env_sensor",
    "table": "eip_grp",
    "where": "monitor_id = 19",
    "id": "cc6e5b21428e19b03c92611f1c9cef14",
    "date": "2026-11-27T17:37:39.646435Z",
    "ledger": "global"
  }
}
```

**One table per tag.** Insert one tag policy per tag, then run the client without `table`:

```json
{
  "tag": {
    "protocol": "etherip",
    "ns": 0,
    "dbms": "env_sensor",
    "table": "eip_sint",
    "datatype": "dint",
    "node_sid": "BF1.SmallRangeInt"
  }
}
```

```json
{
  "tag": {
    "protocol": "etherip",
    "ns": 0,
    "dbms": "env_sensor",
    "table": "eip_int",
    "datatype": "dint",
    "node_sid": "BF2.MediumRangeInt"
  }
}
```

```anylog
blockchain insert where policy = <policy> and local = true and master = 192.168.1.62:32148
```

```anylog
<run plc client where
    name = eip_per and
    auto_uns = true and
    type = etherip and
    url = 127.0.0.1:44818 and
    frequency = 2 and
    dbms = env_sensor and
    master_node = 192.168.1.62:32148 and
    nodes = ["BF1.SmallRangeInt",
             "BF2.MediumRangeInt"]
>
```

Each tag writes to its own table. The tables are:

- `eip_sint`
- `eip_int`

Each table has the columns:

- `timestamp`
- `value`

The UNS leaves are:

```text
UNS
├── bf1
│   └── smallrangeint
└── bf2
    └── mediumrangeint
```

A UNS entry and its object for the leaf `BF1.SmallRangeInt`. The `uns` part gives the path, and the `object` part holds the tag with its `dbms` and `table` from the tag policy. The `object_id`, `parent`, `id`, `date`, and `ledger` fields are not shown. There is no `where`. A leaf gets a `where` only when the command or a mapping policy sets the table. Here the table comes from a tag policy, so the leaf has no `where`, even if `group_by_attributes` is set.

```json
{
  "uns": {
    "name": "smallrangeint",
    "namespace": "bf1/smallrangeint"
  },
  "object": {
    "name": "bf1_smallrangeint",
    "etherip": {
      "node_sid": "BF1.SmallRangeInt",
      "datatype": "dint"
    },
    "dbms": "env_sensor",
    "table": "eip_sint"
  }
}
```

**Mapping policy with** `group_by_attributes`**.** A mapping policy names the table, the columns, and the `group_by_attributes`. The tag `plc_id` is not a PLC tag. It is a constant passed on the command. Insert the policy:

```json
{
  "mapping": {
    "name": "ether_plc_weather",
    "dbms": "env_sensor",
    "table": "ether_plc_weather",
    "group_by_attributes": ["plc_id"],
    "schema": {
      "timestamp": {
        "type": "timestamp",
        "bring": "[timestamp]"
      },
      "weatherreadings_temperature": {
        "type": "float",
        "bring": "[WeatherReadings.temperature]"
      },
      "weatherreadings_humidity": {
        "type": "float",
        "bring": "[WeatherReadings.humidity]"
      },
      "weatherreadings_pressure": {
        "type": "float",
        "bring": "[WeatherReadings.pressure]"
      },
      "weatherreadings_wind_speed": {
        "type": "float",
        "bring": "[WeatherReadings.wind_speed]"
      },
      "weatherreadings_wind_direction": {
        "type": "float",
        "bring": "[WeatherReadings.wind_direction]"
      },
      "weatherreadings_rain": {
        "type": "float",
        "bring": "[WeatherReadings.rain]"
      },
      "plc_id": {
        "type": "string",
        "bring": "[plc_id]"
      }
    },
    "id": "7ea6571da1bf7b3dc6e921cb559cfbe1",
    "date": "2026-11-11T09:59:44.052872Z",
    "ledger": "global"
  }
}
```

```anylog
blockchain insert where policy = <policy> and local = true and master = 192.168.1.62:32148
```

Run the client with the policy id. The command has no `table`, because the policy names it:

```anylog
<run plc client where
    name = eip_map and
    type = etherip and
    url = 127.0.0.1:44818 and
    frequency = 2 and
    dbms = env_sensor and
    policy = 7ea6571da1bf7b3dc6e921cb559cfbe1 and
    auto_uns = true and
    uns_prefix = weather_map_const and
    master_node = 192.168.1.62:32148 and
    constants = {"plc_id":"PLC-1"} and
    nodes = ["WeatherReadings.temperature",
             "WeatherReadings.humidity",
             "WeatherReadings.pressure",
             "WeatherReadings.wind_speed",
             "WeatherReadings.wind_direction",
             "WeatherReadings.rain"]
>
```

Table:

- `ether_plc_weather_wr`

Columns:

- `timestamp`
- `weatherreadings_temperature`
- `weatherreadings_humidity`
- `weatherreadings_pressure`
- `weatherreadings_wind_speed`
- `weatherreadings_wind_direction`
- `weatherreadings_rain`
- `plc_id` (it comes from the constant)

UNS tree:

```text
weather_map_const
└── weatherreadings
    ├── temperature
    ├── humidity
    ├── pressure
    ├── wind_speed
    ├── wind_direction
    └── rain
```

This example proves we do not need to declare new tags in the PLC for `plc_id`, `monitor_id`, or `station_id`: they come from `constants` on the command, and the policy stores them through `bring`. `plc_id` still has to be in `constants`, because the `where` is built from it.

UNS result:

```json
{
  "uns": {
    "name": "temperature",
    "namespace": "weather_map_const/weatherreadings/temperature",
    "object_id": "4187565db0546c9cc334293b705576ae",
    "parent": "bf2d3d390b489fd520495d5f64d2f8c8",
    "id": "519ef2e4818261b849b330331cf95356",
    "date": "2026-11-27T17:59:24.145879Z",
    "ledger": "global"
  },
  "object": {
    "plc_id": "PLC-1",
    "name": "weatherreadings_temperature",
    "etherip": {
      "node_sid": "WeatherReadings.temperature"
    },
    "column": "weatherreadings_temperature",
    "dbms": "env_sensor",
    "table": "ether_plc_weather_wr",
    "where": "plc_id = 'PLC-1'",
    "id": "4187565db0546c9cc334293b705576ae",
    "date": "2026-11-27T17:59:24.142507Z",
    "ledger": "global"
  }
}
```

**Mapping policy with** `params`**, two devices.** One policy names the table and the columns for two devices, `BF1` and `BF2`. Each `params` row is one device. The first value of a row is a literal (`BF2` or `BF1`), and the others are tags. In the schema, `params.0` is the `monitor_id` column, and `params.1` to `params.12` are the tag columns. A BF1 tag and a BF2 tag at the same position go to the same column. The policy has no `group_by_attributes`, so the command adds it. Insert the policy:

```json
{
  "mapping": {
    "name": "eip_uns_v3",
    "dbms": "env_sensor",
    "table": "eip_uns_v2",
    "readings": "",
    "params": [
      ["BF2", "[BF2.CommsStatus]", "[BF2.RealEnergy]", "[BF2.Frequency]",
              "[BF2.PowerFactor]", "[BF2.ReactivePower]", "[BF2.RealPower]",
              "[BF2.CurrentA]", "[BF2.VoltageAN]", "[BF2.CurrentB]",
              "[BF2.VoltageBN]", "[BF2.CurrentC]", "[BF2.VoltageCN]"],
      ["BF1", "[BF1.Running]", "[BF1.ElapsedRunTime]", "[BF1.OutputFreq]",
              "[BF1.OutputPower]", "[BF1.OutputCurrent]", "[BF1.OutputVoltage]",
              "[BF1.CommandedFreq]", "[BF1.DCBusVoltage]", "[BF1.DriveTemp]",
              "[BF1.OutputRPM]", "[BF1.ElapsedkWh]", "[BF1.FaultCode]"]
    ],
    "schema": {
      "timestamp": {"type": "timestamp", "default": "now()", "bring": "[timestamp]"},
      "monitor_id": {"type": "str", "default": "params.0"},
      "commsstatus": {"type": "bool", "default": null, "bring": "params.1"},
      "energymultiplier": {"type": "int", "default": null, "bring": "params.2"},
      "frequency": {"type": "int", "default": null, "bring": "params.3"},
      "powerfactor": {"type": "int", "default": null, "bring": "params.4"},
      "reactivepower": {"type": "int", "default": null, "bring": "params.5"},
      "realpower": {"type": "int", "default": null, "bring": "params.6"},
      "a_current": {"type": "int", "default": null, "bring": "params.7"},
      "a_n_voltage": {"type": "int", "default": null, "bring": "params.8"},
      "b_current": {"type": "int", "default": null, "bring": "params.9"},
      "b_n_voltage": {"type": "int", "default": null, "bring": "params.10"},
      "c_current": {"type": "int", "default": null, "bring": "params.11"},
      "c_n_voltage": {"type": "int", "default": null, "bring": "params.12"}
    },
    "id": "1774da49fabc42e0d5a149a6c5148804",
    "date": "2026-11-13T10:29:17.246086Z",
    "ledger": "global"
  }
}
```

```anylog
blockchain insert where policy = <policy> and local = true and master = 192.168.1.62:32148
```

Run the client with the policy id. The command has no `table`, because the policy names it. `monitor_id` is not a PLC tag, so `group_by_attributes = ["monitor_id"]` takes its value from the `params` row:

```anylog
<run plc client where
    name = eip_dev and
    type = etherip and
    url = 127.0.0.1:44820 and
    frequency = 2 and
    dbms = env_sensor and
    policy = 1774da49fabc42e0d5a149a6c5148804 and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    uns_prefix = plant1 and
    group_by_attributes = ["monitor_id"] and
    nodes = ["BF2.CommsStatus",
             "BF2.RealEnergy",
             "BF2.Frequency",
             "BF2.PowerFactor",
             "BF2.ReactivePower",
             "BF2.RealPower",
             "BF2.CurrentA",
             "BF2.VoltageAN",
             "BF2.CurrentB",
             "BF2.VoltageBN",
             "BF2.CurrentC",
             "BF2.VoltageCN",
             "BF1.Running",
             "BF1.ElapsedRunTime",
             "BF1.OutputFreq",
             "BF1.OutputPower",
             "BF1.OutputCurrent",
             "BF1.OutputVoltage",
             "BF1.CommandedFreq",
             "BF1.DCBusVoltage",
             "BF1.DriveTemp",
             "BF1.OutputRPM",
             "BF1.ElapsedkWh",
             "BF1.FaultCode"]
>
```

The table `eip_uns_v2` gets one row per device on every read. Its columns are:

- `timestamp`
- `monitor_id`
- `commsstatus`
- `energymultiplier`
- `frequency`
- `powerfactor`
- `reactivepower`
- `realpower`
- `a_current`
- `a_n_voltage`
- `b_current`
- `b_n_voltage`
- `c_current`
- `c_n_voltage`

The UNS has one leaf per tag, 12 for each device. `monitor_id` has no leaf, because it is not a PLC tag:

```text
plant1
├── bf1
│   ├── running
│   ├── elapsedruntime
│   ├── ...
│   └── faultcode
└── bf2
    ├── commsstatus
    ├── realenergy
    ├── ...
    └── voltagecn
```

A UNS entry and its object for the leaf `BF1.DCBusVoltage`. The `column` is the one at the tag's position in the `params` row, and the `where` separates BF1 from BF2, because both devices share the columns. The `object_id`, `parent`, `id`, `date`, and `ledger` fields are not shown.

```json
{
  "uns": {
    "name": "dcbusvoltage",
    "namespace": "plant1/bf1/dcbusvoltage"
  },
  "object": {
    "name": "bf1_dcbusvoltage",
    "etherip": {
      "node_sid": "BF1.DCBusVoltage"
    },
    "column": "a_n_voltage",
    "dbms": "env_sensor",
    "table": "eip_uns_v2",
    "where": "monitor_id = 'BF1'"
  }
}
```

**Mapping policy without** `params`**, with** `monitor_id` **from a constant.** This policy reads each tag directly with `bring`, as in the `ether_plc_weather` example. `monitor_id` has no tag, so it is a generic column: `bring` is `[monitor_id]`, and the value comes from `constants` on the command. The same policy can be used by more than one client, each with its own `monitor_id`. Insert the policy:

```json
{
  "mapping": {
    "name": "eip_direct",
    "dbms": "env_sensor",
    "table": "eip_direct",
    "schema": {
      "timestamp": {"type": "timestamp", "bring": "[timestamp]"},
      "monitor_id": {"type": "string", "bring": "[monitor_id]"},
      "bf1_running": {"type": "bool", "bring": "[BF1.Running]"},
      "bf1_outputfreq": {"type": "float", "bring": "[BF1.OutputFreq]"},
      "bf2_commsstatus": {"type": "bool", "bring": "[BF2.CommsStatus]"},
      "bf2_realpower": {"type": "float", "bring": "[BF2.RealPower]"}
    }
  }
}
```

```anylog
blockchain insert where policy = <policy> and local = true and master = 192.168.1.62:32148
```

Run the client with the policy id. The command has no `table`, because the policy names it. `group_by_attributes` and `constants` are on the command. `monitor_id` is not a PLC tag. The constant is stored in the column and on the object. The leaf has no `where`: `group_by_attributes` is on the command, and `monitor_id` is a `bring`, not a literal default.

```anylog
<run plc client where
    name = eip_direct_run and
    type = etherip and
    url = 127.0.0.1:44820 and
    frequency = 2 and
    dbms = env_sensor and
    policy = 618061bea70aa75869892f09e9b978e2 and
    auto_uns = true and
    master_node = 192.168.1.62:32148 and
    group_by_attributes = ["monitor_id"] and
    constants = {"monitor_id":"BF1"} and
    nodes = ["BF1.Running",
             "BF1.OutputFreq",
             "BF2.CommsStatus",
             "BF2.RealPower"]
>
```

The table `eip_direct` gets one row per read. Its columns are:

- `timestamp`
- `monitor_id`
- `bf1_running`
- `bf1_outputfreq`
- `bf2_commsstatus`
- `bf2_realpower`

`monitor_id` is `BF1` for every row of this run.

The UNS leaves are:

```text
UNS
├── bf1
│   ├── running
│   └── outputfreq
└── bf2
    ├── commsstatus
    └── realpower
```

The four tags come from both devices, so a row labeled `BF1` also holds `BF2` values. To keep one device per row, list only that device's tags in `nodes` and in the schema.

A UNS entry and its object for `BF1.Running`. The constant is a key on the object. There is no `where`. The `object_id`, `parent`, `id`, `date`, and `ledger` fields are not shown.

```json
{
  "uns": {
    "name": "running",
    "namespace": "bf1/running"
  },
  "object": {
    "monitor_id": "BF1",
    "name": "bf1_running",
    "etherip": {
      "node_sid": "BF1.Running",
      "datatype": "boolean"
    },
    "column": "bf1_running",
    "dbms": "env_sensor",
    "table": "eip_direct"
  }
}
```
