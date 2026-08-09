---
title: "Mapping Policy"
description: "How mapping policies translate incoming JSON data into table rows — the general model, plus epoch timestamps, blob data, and unknown/dynamic content."
layout: page
---

<!---
### 📜 Change Log
 | **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon    | Fixed invalid JSON throughout (inline `<-- comment -->` annotations aren't valid JSON; unquoted `!policy_id`; a missing closing brace in the epoch-timestamp example; a duplicated `readings` key in the "complete" example where the second occurrence should be `schema`); fixed the `run msg client` example that had copied the pre-fix `{user-agent=anylog}` bug and a `nama`/`name` typo from an earlier Message Broker draft; fixed `[device]`→`[deviceName]` and the `dbms` bring-vs-literal mismatch against the EdgeX sample payload; removed a duplicated line in the sample data; fixed a stray H1 mid-document; typo fixes | |
 | 2026-08-08 | Moshe Shadmon | moved from blockchain dir + added content | |
--->


# AnyLog Mapping Policies

## Overview

An **AnyLog Mapping Policy** defines how incoming JSON data is mapped to the logical database, table, and columns used by AnyLog.

Mapping policies synchronize the structure of incoming data with the structure used to store and query that data. They can:

- Select the destination logical database and table.
- Dynamically derive the database or table from the incoming message.
- Select a list of readings inside a larger JSON message.
- Map source attributes to destination columns.
- Define and normalize column data types.
- Supply default values when source attributes are missing.
- Read values from either an individual reading or the root message.
- Apply transformations to values.
- Create columns dynamically when the source schema is not known in advance.
- Generate multiple rows using parameter sets.
- Apply conditional mapping logic using scripts.
- Store blob or file content separately while maintaining a relational reference.

A mapping can be defined directly in a `run msg client` command or registered as a policy and referenced by its policy ID. A registered policy is useful when the same mapping is reused by multiple subscriptions or when the mapping should be managed centrally rather than duplicated in commands.

---

## 1. Basic Mapping Policy Structure

A mapping policy is represented by a root `mapping` object:

```json
{
  "mapping": {
    "id": "sensor-policy",
    "dbms": "smart_city",
    "table": "sensor_data",
    "readings": "",
    "schema": {
      "timestamp": {
        "type": "timestamp",
        "bring": "[timestamp]",
        "default": "now()"
      },
      "value": {
        "type": "float",
        "bring": "[value]",
        "default": null
      }
    }
  }
}
```

The two structural elements required by the mapping-policy validator are:

```text
mapping
 ├── id
 └── schema
```

The destination `dbms` and `table` must also be available when the mapping is executed. They can be supplied by the caller, defined literally in the policy, or derived from the incoming JSON.

---

## 2. Mapping Policy vs. Inline Mapping

Mapping can be specified directly as part of `run msg client`.

For example:

```text
<run msg client where
  broker=local and
  log=false and topic=(
    name=my-data and
    dbms="bring [dbms]" and
    table="bring [sensor]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.value.float="bring [value]"
)>
```

When the same mapping is reused, it can instead be registered as a policy and referenced by its ID:

```text
<run msg client where
  broker=local and
  log=false and topic=(
    name=[topic name] and
    policy=!policy_id
  )>
```

This separates the subscription from the mapping definition and avoids repeating the mapping on every client command.

---

## 3. A Dynamic Routing Example

Consider the following incoming messages:

```json
{"dbms": "smart_city", "sensor": "ping_sensor", "timestamp": "2026-07-27T10:00:00Z", "value": 12.4}
{"dbms": "smart_city", "sensor": "ping_sensor", "timestamp": "2026-07-27T10:05:00Z", "value": 13.1}
{"dbms": "smart_city", "sensor": "humidity", "timestamp": "2026-07-27T10:00:00Z", "value": 58.2}
{"dbms": "smart_city", "sensor": "humidity", "value": 60.5}
{"dbms": "smart_city", "sensor": "co2_level", "timestamp": "2026-07-27T09:55:00Z", "value": 412.7}
{"dbms": "smart_city", "sensor": "co2_level", "timestamp": "2026-07-27T10:10:00Z", "value": 418.3}
{"dbms": "monitoring", "sensor": "cpu_temp", "timestamp": "2026-07-27T10:00:00Z", "value": 62.8}
{"dbms": "monitoring", "sensor": "cpu_temp", "timestamp": "2026-07-27T10:15:00Z", "value": 65.0}
```

A single mapping policy can route these messages dynamically:

```json
{
  "mapping": {
    "id": "sensor-policy",
    "dbms": "bring [dbms]",
    "table": "bring [sensor]",
    "readings": "",
    "schema": {
      "timestamp": {
        "type": "timestamp",
        "default": "now()",
        "bring": "[timestamp]"
      },
      "value": {
        "type": "float",
        "default": null,
        "bring": "[value]"
      }
    }
  }
}
```

The policy creates data for:

```text
smart_city.ping_sensor
smart_city.humidity
smart_city.co2_level
monitoring.cpu_temp
```

This illustrates an important mapping-policy capability: **the database and table do not need to be fixed in the policy**. They can be derived from each incoming message.

The humidity message without a `timestamp` intentionally demonstrates the `default` mechanism. Because the source timestamp is missing, `"default": "now()"` supplies the current UTC time.

---

# Policy-Level Attributes

## 4. `id`

`id` identifies the mapping policy.

```json
"id": "sensor-policy"
```

The mapping-policy validator requires an ID.

When the policy is referenced by a human-readable variable from commands such as:

```text
policy=!policy_id
```

it is often useful to assign the policy ID explicitly rather than relying on an automatically generated identifier.

---

## 5. `dbms`

`dbms` identifies the destination logical database.

A fixed destination can be specified directly:

```json
"dbms": "industrial_data"
```

The database can also be derived from the incoming JSON:

```json
"dbms": "bring [dbms]"
```

Given:

```json
{
  "dbms": "factory_a"
}
```

the destination becomes:

```text
factory_a
```

This allows one mapping policy to route messages to different logical databases.

---

## 6. `table`

`table` identifies the destination table.

A fixed table can be specified directly:

```json
"table": "compressors"
```

The table can also be derived dynamically:

```json
"table": "bring [sensor]"
```

Given:

```json
{
  "sensor": "humidity"
}
```

the destination table becomes:

```text
humidity
```

The `dbms` and `table` values are resolved before the rows are generated.

---

## 7. `source`

`source` identifies the source of the incoming data, such as a device, gateway, application, or other producer.

Example:

```json
"source": {
  "bring": "[device]"
}
```

Given:

```json
{
  "device": "Pump Station 7"
}
```

the resolved source becomes:

```text
pump_station_7
```

The source string is normalized to lowercase and spaces are replaced with underscores.

---

## 8. `readings`

The `readings` attribute identifies the part of the incoming JSON that contains the individual records to map.

### Flat messages

When the incoming JSON object itself is the reading, `readings` can be empty:

```json
"readings": ""
```

For example:

```json
{
  "dbms": "smart_city",
  "sensor": "ping_sensor",
  "timestamp": "2026-07-27T10:00:00Z",
  "value": 12.4
}
```

The complete object is processed as one reading.

If `readings` is omitted, the mapping code likewise treats the complete JSON message as the reading. If the supplied input is already a list, each list entry is processed as a reading.

### Nested readings

Consider:

```json
{
  "dbms": "smart_city",
  "sensor": "ping_sensor",
  "data": [
    {
      "timestamp": "2026-07-27T10:00:00Z",
      "value": 12.4
    },
    {
      "timestamp": "2026-07-27T10:05:00Z",
      "value": 13.1
    }
  ]
}
```

The policy can specify:

```json
"readings": "data"
```

AnyLog then processes each object in `data` independently.

The `bring` expressions inside the schema are evaluated relative to each reading:

```json
"schema": {
  "timestamp": {
    "type": "timestamp",
    "bring": "[timestamp]"
  },
  "value": {
    "type": "float",
    "bring": "[value]"
  }
}
```

Conceptually:

```text
Incoming Message
       │
       ├── dbms
       ├── sensor
       │
       └── data
            │
            ├── Reading 1
            └── Reading 2
                   │
                   ▼
              Mapping Schema
                   │
                   ▼
                DB Rows
```

> `readings` is a key name, not a `bring` expression. For a JSON key named `data`, use `"readings": "data"`, not `"readings": "[data]"`.

---

# The Schema

## 9. `schema`

The `schema` defines the destination columns and the instructions used to obtain their values.

Example:

```json
"schema": {
  "timestamp": {
    "type": "timestamp",
    "bring": "[time]"
  },
  "temperature": {
    "type": "float",
    "bring": "[temp]"
  },
  "asset": {
    "type": "varchar",
    "bring": "[name]"
  }
}
```

Normally, each key in `schema` is the destination column name:

```text
schema
 │
 ├── timestamp
 │    ├── type
 │    └── bring
 │
 ├── temperature
 │    ├── type
 │    └── bring
 │
 └── asset
      ├── type
      └── bring
```

For each reading, AnyLog walks through the schema and constructs an output row.

---

## 10. `type`

`type` defines the destination column's data type.

Example:

```json
"temperature": {
  "type": "float",
  "bring": "[temperature]"
}
```

AnyLog normalizes multiple source or policy type names into a common set of data types.

### Data Type Normalization

| Input Type | Normalized Type |
|---|---|
| `str` | `varchar` |
| `string` | `varchar` |
| `char varying` | `varchar` |
| `varchar` | `varchar` |
| `bytestring` | `varchar` |
| `uuid` | `uuid` |
| `bigint` | `bigint` |
| `integer` | `int` |
| `int` | `int` |
| `int16` | `int` |
| `uint16` | `int` |
| `int32` | `int` |
| `uint32` | `int` |
| `sbyte` | `int` |
| `int64` | `bigint` |
| `uint64` | `bigint` |
| `float` | `float` |
| `float64` | `float` |
| `decimal` | `float` |
| `numeric` | `float` |
| `double` | `float` |
| `char` | `char` |
| `character` | `char` |
| `byte` | `char(1)` |
| `bool` | `bool` |
| `boolean` | `bool` |
| `timestamp` | `timestamp` |
| `datetime` | `timestamp` |
| `date` | `date` |
| `time` | `time` |
| `nonetype` | `nonetype` |

### OPC UA Types

The type normalizer also recognizes several OPC UA-oriented type names:

| Input Type | Normalized Type | Description |
|---|---|---|
| `nodeid` | `varchar` | OPC UA NodeId |
| `expandednodeid` | `varchar` | OPC UA ExpandedNodeId |
| `StatusCode` | `int` | OPC UA status code |
| `qualifiedmame` | `varchar` | OPC UA qualified-name value |
| `localizedtext` | `varchar` | OPC UA localized text |
| `variant` | `varchar` | Container for an arbitrary OPC UA data type |
| `datavalue` | `varchar` | Value with status and timestamp information |
| `diagnosticinfo` | `varchar` | Error or diagnostic information |

> The spelling `qualifiedmame` above reflects the currently supplied type-unifier key. If the implementation changes that key to `qualifiedname`, the documentation should be updated accordingly.

### Common normalized types

For most manually written mapping policies, the most common destination types are:

```text
varchar
uuid
int
bigint
float
char
bool
timestamp
date
time
nonetype
```

---

## 11. Default Mapping by Column Name

If a column does not specify `bring`, AnyLog attempts to retrieve a source attribute having the same name as the destination column.

For example:

```json
"schema": {
  "temperature": {
    "type": "float"
  }
}
```

with:

```json
{
  "temperature": 72.5
}
```

is effectively equivalent to:

```json
"temperature": {
  "type": "float",
  "bring": "[temperature]"
}
```

This allows simple mappings to remain concise.

---

## 12. `bring`

`bring` specifies where a column value should be retrieved from the source JSON.

Example:

```json
"temperature": {
  "type": "float",
  "bring": "[temp]"
}
```

Input:

```json
{
  "temp": 72.5
}
```

Output:

```json
{
  "temperature": 72.5
}
```

The destination column name and source attribute name do not need to match.

For example:

```json
"schema": {
  "asset_id": {
    "type": "varchar",
    "bring": "[device]"
  },
  "temperature": {
    "type": "float",
    "bring": "[measurements][temp]"
  }
}
```

Conceptually:

```text
Source JSON                         Destination

device --------------------------> asset_id

measurements
   └── temp ---------------------> temperature
```

AnyLog parses the `bring` instruction and, when possible, caches the compiled representation for reuse across subsequent rows.

---

## 13. `default`

`default` supplies a value when `bring` does not return data.

Example:

```json
"quality": {
  "type": "varchar",
  "bring": "[quality]",
  "default": "good"
}
```

If `quality` is absent, the mapped value becomes:

```json
{
  "quality": "good"
}
```

### Current time

A particularly useful default is:

```json
"default": "now()"
```

For example:

```json
"timestamp": {
  "type": "timestamp",
  "bring": "[timestamp]",
  "default": "now()"
}
```

When `timestamp` is missing, AnyLog uses the current UTC time.

A `null` default can also be specified:

```json
"value": {
  "type": "float",
  "bring": "[value]",
  "default": null
}
```

---

## 14. `root`

When `readings` selects a nested list, schema fields normally read from the current item in that list.

`root: true` changes the lookup context to the complete original JSON message.

Consider:

```json
{
  "site": "factory_a",
  "readings": [
    {
      "temperature": 71.2
    },
    {
      "temperature": 71.4
    }
  ]
}
```

Policy:

```json
{
  "mapping": {
    "id": "temperature-policy",
    "dbms": "factory",
    "table": "temperature",
    "readings": "readings",
    "schema": {
      "site": {
        "type": "varchar",
        "bring": "[site]",
        "root": true
      },
      "temperature": {
        "type": "float",
        "bring": "[temperature]"
      }
    }
  }
}
```

Output:

```json
{
  "site": "factory_a",
  "temperature": 71.2
}
```

and:

```json
{
  "site": "factory_a",
  "temperature": 71.4
}
```

Conceptually:

```text
Root Message
│
├── site -----------------------------┐
│                                     │ root=true
└── readings                          │
     │                                │
     ├── {temperature: 71.2} ---------┼----> Output Row 1
     │                                │
     └── {temperature: 71.4} ---------┼----> Output Row 2
                                      │
                     site copied -----┘
                     into each row
```

---

## 15. `value`

`value` can identify or derive the source attribute used by a mapping.

For example:

```json
"value": "bring [temperature]"
```

When `value` contains a `bring [...]` expression, the mapping logic extracts the referenced source attribute and uses it for value retrieval.

The same mechanism is also used in mapping flows that derive values from PLC attribute names or regular-expression matches.

---

## 16. `apply`

`apply` transforms a value before it is added to the destination row.

For regular mapped values, the supplied implementation supports:

- `epoch_to_datetime`
- `json_dump`

### `epoch_to_datetime`

```json
"timestamp": {
  "bring": "[origin]",
  "default": "now()",
  "type": "timestamp",
  "apply": "epoch_to_datetime"
}
```

This is useful when a device provides a numeric epoch value rather than a formatted timestamp.

The name `origin` is not special; it is simply the source field used in this example.

### `json_dump`

```json
"metadata": {
  "type": "varchar",
  "bring": "[metadata]",
  "apply": "json_dump"
}
```

If the source contains:

```json
{
  "metadata": {
    "manufacturer": "ABC",
    "model": "X7"
  }
}
```

the dictionary is serialized into a JSON-formatted string for storage.

---

## 17. Timestamp Handling

Timestamp columns receive special formatting and validation.

Example:

```json
"timestamp": {
  "type": "timestamp",
  "bring": "[timestamp]"
}
```

The mapping implementation handles timestamp values represented as:

- Date/time strings.
- ISO-formatted strings with timezone offsets.
- Integer values.
- Floating-point values.
- Numeric strings.

For sources that require an explicit epoch transformation, use:

```json
"timestamp": {
  "type": "timestamp",
  "bring": "[origin]",
  "default": "now()",
  "apply": "epoch_to_datetime"
}
```

---

# Advanced Schema Features

## 18. Multiple Mapping Alternatives for a Column

A schema column can contain a list of mapping definitions instead of one definition.

Example:

```json
"temperature": [
  {
    "dbms": "factory",
    "table": "compressors",
    "type": "float",
    "bring": "[compressor_temp]"
  },
  {
    "dbms": "factory",
    "table": "pumps",
    "type": "float",
    "bring": "[pump_temp]"
  }
]
```

AnyLog evaluates the alternatives in order and skips definitions whose `dbms` or `table` does not match the current destination.

Conceptually:

```text
temperature
    │
    ├── table = compressors
    │       └── bring [compressor_temp]
    │
    └── table = pumps
            └── bring [pump_temp]
```

This allows a schema to contain destination-specific alternatives.

---

## 19. Column-Level `dbms` and `table`

The `dbms` and `table` attributes inside a column definition restrict that particular mapping option.

Example:

```json
"value": [
  {
    "dbms": "factory_a",
    "table": "temperature",
    "type": "float",
    "bring": "[temp]"
  },
  {
    "dbms": "factory_a",
    "table": "pressure",
    "type": "float",
    "bring": "[pressure]"
  }
]
```

A definition that does not match the current database or table is ignored and the mapper continues to the next alternative.

---

## 20. Unknown and Dynamic Columns

Mapping policies can create columns dynamically when the complete source schema is not known ahead of time.

This is useful with sources such as Telegraf, Litmus Edge, and other systems that may provide changing sets of fields.

There are two common cases.

### Known keys, types determined dynamically

If the keys are known but their data types are not:

```json
"*": {
  "type": "*",
  "bring": [
    "success",
    "tagName",
    "value",
    "description"
  ]
}
```

AnyLog retrieves those keys and derives the column types from the source values.

### Unknown keys and unknown types

If neither the keys nor their types are known:

```json
"*": {
  "type": "*",
  "bring": ["*"]
}
```

Given:

```json
{
  "temperature": 72.5,
  "pressure": 101.3,
  "rpm": 1450
}
```

the mapper can create:

```text
temperature
pressure
rpm
```

and infer the corresponding data types.

---

## 21. Dynamic Columns from Subobjects

The `*` mapping can also pull fields from selected subobjects.

Example:

```json
"*": {
  "type": "*",
  "bring": [
    "fields",
    "tags"
  ]
}
```

Input:

```json
{
  "fields": {
    "temperature": 72.5,
    "pressure": 101.3
  },
  "tags": {
    "site": "A",
    "machine": "compressor_7"
  }
}
```

The generated column names include the parent key:

```text
fields_temperature
fields_pressure
tags_site
tags_machine
```

Conceptually:

```text
fields.temperature  ---> fields_temperature
fields.pressure     ---> fields_pressure

tags.site           ---> tags_site
tags.machine        ---> tags_machine
```

---

## 22. `params`

`params` allows the same schema to generate multiple logical output rows using different parameter sets.

Example:

```json
"params": [
  [
    "DelayTimer",
    "[DelayTimer.ACC]",
    "[DelayTimer.PRE]"
  ],
  [
    "CycleCounter",
    "[CycleCounter.ACC]",
    "[CycleCounter.PRE]"
  ]
]
```

The schema can reference each value using:

```text
params.0
params.1
params.2
```

Example:

```json
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
```

For the first parameter set:

```text
params.0 = DelayTimer
params.1 = [DelayTimer.ACC]
params.2 = [DelayTimer.PRE]
```

For the second:

```text
params.0 = CycleCounter
params.1 = [CycleCounter.ACC]
params.2 = [CycleCounter.PRE]
```

The policy is processed once for each parameter list.

```text
                     Mapping Schema
                          │
          ┌───────────────┴───────────────┐
          │                               │
      Params Set 1                    Params Set 2
          │                               │
     DelayTimer                      CycleCounter
          │                               │
          ▼                               ▼
      Output Row                       Output Row
```

`params.N` substitution is supported in `default`, `bring`, and `value`.

---

## 23. `script`

A schema entry can contain an AnyLog `script` that is executed before normal column mapping.

Example structure:

```json
"some_column": {
  "script": "<AnyLog script>",
  "type": "varchar",
  "bring": "[value]"
}
```

The script can affect mapping flow, including:

- Skipping the current attribute.
- Skipping the complete event.
- Exiting the script while allowing mapping to continue.
- Switching processing to another imported policy.

This provides conditional and procedural control over the mapping process.

---

## 24. Script-Only Schema Entries

Schema names beginning and ending with two underscores are treated as control entries and are not emitted as destination columns.

For example:

```json
"__start__": {
  "script": "..."
}
```

or:

```json
"__end__": {
  "script": "..."
}
```

Conceptually:

```text
schema
 │
 ├── __start__      script/control only
 │
 ├── timestamp      destination column
 │
 ├── temperature    destination column
 │
 └── __end__        script/control only
```

---

## 25. Changing Mapping Policy During Processing

Scripts can return a change-policy result.

When this occurs, the mapping logic can select another policy from an imported-policy dictionary and restart processing with that policy.

This provides a mechanism for selecting a mapping dynamically based on the content of the incoming event.

This is an advanced feature and is normally used only when a single incoming stream contains messages requiring substantially different mapping logic.

---

# Blob and File Data

## 26. Blob Columns

A schema column can identify source content as blob/file data.

Example:

```json
"file": {
  "root": true,
  "blob": true,
  "bring": "[file_content]",
  "extension": "jpeg",
  "apply": "base64decoding",
  "hash": "md5",
  "type": "varchar"
}
```

When:

```json
"blob": true
```

AnyLog writes the blob content to the configured blob directory.

The relational row contains the generated file identifier rather than the complete blob content.

The current implementation recognizes:

```json
"hash": "md5"
```

The hash is used to generate the file name.

An optional extension can be supplied:

```json
"extension": "jpeg"
```

---

## 27. Blob `apply` Operations

For blob processing, the supplied implementation supports:

```json
"apply": "base64decoding"
```

and:

```json
"apply": "opencv"
```

### Base64 example

```json
"file": {
  "root": true,
  "blob": true,
  "bring": "[file_content]",
  "extension": "jpeg",
  "apply": "base64decoding",
  "hash": "md5",
  "type": "varchar"
}
```

The Base64 value is decoded before being written to the blob directory.

### Updating blob `apply` logic

Examples of changing the policy:

```text
set policy new_policy [mapping][schema][file][apply] = "base64decoding"
```

or:

```text
set policy new_policy [mapping][schema][file][apply] = "opencv"
```

---

# Complete Examples

## 28. Complete Nested-Reading Example

Source message:

```json
{
  "site": "Plant_A",
  "gateway": "edge_17",
  "readings": [
    {
      "time": "2026-08-08T18:30:00Z",
      "asset": "compressor_1",
      "temp": 72.5,
      "pressure": 101.4
    },
    {
      "time": "2026-08-08T18:30:01Z",
      "asset": "compressor_2",
      "temp": 74.1,
      "pressure": 102.7
    }
  ]
}
```

Policy:

```json
{
  "mapping": {
    "id": "compressor_mapping",
    "dbms": "industrial",
    "table": "compressor_data",
    "source": {
      "bring": "[gateway]"
    },
    "readings": "readings",
    "schema": {
      "timestamp": {
        "type": "timestamp",
        "bring": "[time]",
        "default": "now()"
      },
      "site": {
        "type": "varchar",
        "bring": "[site]",
        "root": true
      },
      "asset": {
        "type": "varchar",
        "bring": "[asset]"
      },
      "temperature": {
        "type": "float",
        "bring": "[temp]"
      },
      "pressure": {
        "type": "float",
        "bring": "[pressure]"
      }
    }
  }
}
```

The first reading generates approximately:

```json
{
  "timestamp": "2026-08-08T18:30:00Z",
  "site": "Plant_A",
  "asset": "compressor_1",
  "temperature": 72.5,
  "pressure": 101.4
}
```

The second generates:

```json
{
  "timestamp": "2026-08-08T18:30:01Z",
  "site": "Plant_A",
  "asset": "compressor_2",
  "temperature": 74.1,
  "pressure": 102.7
}
```

`site` is read from the root message because it specifies:

```json
"root": true
```

while the other values are read from each individual item in `readings`.

---

## 29. EdgeX-Style Example

Sample EdgeX-style input:

```json
{
  "apiVersion": "v2",
  "id": "707564c4-6818-4746-9c54-219a0fd110c6",
  "deviceName": "ba-virtual",
  "profileName": "BuildingAutomationVirtualDevice",
  "sourceName": "AvgTemp",
  "origin": 1686087247849269800,
  "readings": [
    {
      "id": "42700bdd-4525-443f-88dd-22c488011b65",
      "origin": 1686087247849269800,
      "deviceName": "ba-virtual",
      "resourceName": "AvgTemp",
      "profileName": "BuildingAutomationVirtualDevice",
      "valueType": "Float32",
      "units": "°F",
      "value": "7.934139e+01"
    }
  ]
}
```

A corresponding mapping policy can be:

```json
{
  "mapping": {
    "id": "full-policy",
    "dbms": "edgex_data",
    "table": "bring [deviceName]",
    "readings": "readings",
    "schema": {
      "timestamp": {
        "type": "timestamp",
        "default": "now()",
        "bring": "[origin]",
        "apply": "epoch_to_datetime"
      },
      "*": {
        "type": "*",
        "bring": [
          "deviceName",
          "resourceName",
          "profileName",
          "valueType",
          "units",
          "value"
        ]
      }
    }
  }
}
```

In this example:

- `dbms` is fixed as `edgex_data`.
- `table` is dynamically derived from `deviceName`.
- `readings` selects the list under the `readings` key.
- `timestamp` is derived from the reading's `origin`.
- `epoch_to_datetime` converts the source epoch value.
- `*` dynamically creates the selected source columns and derives their types.

If file content exists at the root of the source message, a blob mapping can also be added:

```json
"file": {
  "root": true,
  "blob": true,
  "bring": "[file_content]",
  "extension": "jpeg",
  "apply": "base64decoding",
  "hash": "md5",
  "type": "varchar"
}
```

---

# Processing Model

## 30. Mapping Processing Flow

At a high level:

```text
                 Incoming JSON
                       │
                       ▼
               Determine Source
                       │
                       ▼
                Locate Readings
                       │
                       ▼
              Determine DBMS/Table
                       │
                       ▼
               For Each Param Set
                       │
                       ▼
               For Each Reading
                       │
                       ▼
                 Apply Schema
                       │
          ┌────────────┼────────────┐
          │            │            │
        bring        default       script
          │            │            │
          └────────────┼────────────┘
                       │
                     apply
                       │
                       ▼
                 Normalize Type
                       │
                       ▼
                  Output Row
                       │
                       ▼
               Destination Table
```

When no `params` are defined, the schema is processed once for each reading.

When `params` are defined, the mapping is repeated for each parameter set and each reading.

---

## 31. Column Processing Flow

For a normal schema column:

```text
1. Select applicable column definition
          │
          ▼
2. Apply params.N substitutions, if used
          │
          ▼
3. Execute script, if defined
          │
          ▼
4. Determine column type
          │
          ▼
5. Determine source attribute
          │
          ▼
6. Select reading or root JSON
          │
          ▼
7. Execute bring
          │
          ├── value found ───────────────┐
          │                              │
          └── no value                   │
                  │                      │
                  ▼                      │
               default                   │
                  │                      │
                  └──────────────────────┤
                                         ▼
                                   Apply function
                                         │
                                         ▼
                                   Normalize type
                                         │
                                         ▼
                                  Destination value
```

---

# Reference

## 32. Policy-Level Attributes

| Attribute | Purpose |
|---|---|
| `id` | Unique mapping-policy identifier |
| `dbms` | Destination logical database; can be literal or dynamically derived |
| `table` | Destination table; can be literal or dynamically derived |
| `source` | Identifies the data-producing source |
| `readings` | Identifies the key containing the readings to process |
| `params` | Repeats the schema using different parameter sets |
| `schema` | Defines destination columns and mapping instructions |

---

## 33. Schema-Column Attributes

| Attribute | Purpose |
|---|---|
| `type` | Defines the destination data type |
| `bring` | Retrieves a value from the source JSON |
| `default` | Supplies a value when source data is unavailable |
| `root` | Reads from the root JSON message instead of the current reading |
| `value` | Identifies or derives the source value used for mapping |
| `apply` | Applies a value transformation |
| `script` | Executes conditional or procedural mapping logic |
| `dbms` | Restricts a mapping alternative to a database |
| `table` | Restricts a mapping alternative to a table |
| `blob` | Identifies the value as file/blob data |
| `hash` | Defines the blob hash; the current implementation recognizes `md5` |
| `extension` | Adds an extension to a stored blob file |

---

## 34. Special Schema Constructs

| Construct | Purpose |
|---|---|
| `"*"` | Dynamically creates columns from source attributes |
| `"__name__"` | Defines a script/control entry that does not become a destination column |
| List of column definitions | Provides alternative mappings for the same destination column |
| `params.N` | Substitutes a value from the active parameter set |

---

## 35. Minimal Policy

When source attribute names already match the desired destination column names, the policy can be very small:

```json
{
  "mapping": {
    "id": "simple_mapping",
    "dbms": "factory",
    "table": "sensor_data",
    "schema": {
      "timestamp": {
        "type": "timestamp"
      },
      "asset": {
        "type": "varchar"
      },
      "temperature": {
        "type": "float"
      }
    }
  }
}
```

Input:

```json
{
  "timestamp": "2026-08-08T18:30:00Z",
  "asset": "compressor_7",
  "temperature": 72.5
}
```

Because `bring` is omitted, AnyLog uses the destination column names as the source attribute names:

```text
Source JSON attribute
        │
        │ same name
        ▼
Schema column
        │
        ▼
Destination table
```

More advanced attributes are only needed when the source structure, destination structure, routing, or processing logic requires them.
