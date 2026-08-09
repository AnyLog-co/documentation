# AnyLog Mapping Policy

## Overview

An **AnyLog Mapping Policy** defines how incoming JSON data is transformed into rows that can be stored in an AnyLog-managed table.

A mapping policy determines:

- Which database and table receive the data.
- Which part of the incoming JSON represents the readings.
- How source attributes map to destination columns.
- The data type of each destination column.
- Default values when source data is missing.
- Transformations to apply to values.
- Conditional mapping rules.
- Whether values should be taken from the individual reading or from the root JSON message.
- How one incoming message can generate multiple output rows.
- How dynamic or unknown source attributes can automatically become columns.

At its simplest, a mapping policy looks like:

```json
{
  "mapping": {
    "id": "temperature_policy",
    "dbms": "factory",
    "table": "temperature",
    "schema": {
      "timestamp": {
        "type": "timestamp",
        "bring": "[timestamp]"
      },
      "value": {
        "type": "float",
        "bring": "[temperature]"
      }
    }
  }
}
```

For input such as:

```json
{
  "timestamp": "2026-08-08T18:30:00Z",
  "temperature": 72.4
}
```

the policy produces a row equivalent to:

```json
{
  "timestamp": "2026-08-08T18:30:00Z",
  "value": 72.4
}
```

---

## 1. Overall Policy Structure

The root object contains the `mapping` key:

```json
{
  "mapping": {
    ...
  }
}
```

The basic structure is:

```json
{
  "mapping": {
    "id": "<policy-id>",
    "dbms": "<database-name>",
    "table": "<table-name>",
    "source": ...,
    "readings": ...,
    "params": ...,
    "schema": {
      "<column-name>": {
        ...
      }
    }
  }
}
```

The required elements are:

```text
mapping
 ├── id
 └── schema
```

`dbms` and `table` must also ultimately be available when the policy is executed, either because they are supplied by the caller or because the policy derives or provides them.

---

## 2. `id`

The `id` uniquely identifies the mapping policy.

```json
"id": "compressor_readings"
```

Example:

```json
{
  "mapping": {
    "id": "compressor_readings"
  }
}
```

The policy validator requires an `id`.

The ID is also used in error and trace messages, making meaningful policy names useful for troubleshooting.

---

## 3. `dbms`

`dbms` identifies the destination database.

Example:

```json
"dbms": "industrial_data"
```

A database may also be derived dynamically from the incoming JSON using a `bring` expression.

For example:

```json
"dbms": "bring [database]"
```

Given:

```json
{
  "database": "factory_a"
}
```

the destination database becomes:

```text
factory_a
```

This allows the same policy structure to route different incoming messages to different databases.

---

## 4. `table`

`table` identifies the destination table.

Example:

```json
"table": "compressors"
```

Like `dbms`, the table can also be derived from the source message.

For example:

```json
"table": "bring [asset_type]"
```

Input:

```json
{
  "asset_type": "pump"
}
```

can therefore route the data to:

```text
pump
```

The database and table must be resolved before the row can be generated.

---

## 5. `source`

`source` identifies the source of the incoming data.

Conceptually this can represent a device, gateway, application, or other data-producing entity.

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

the source becomes:

```text
pump_station_7
```

Source names are normalized to lowercase and spaces are replaced with underscores.

The source information is used when organizing mapped data and associated files.

---

## 6. `readings`

A message often contains metadata at the root and a list of actual measurements under another key.

For example:

```json
{
  "site": "Factory_A",
  "device": "compressor_7",
  "readings": [
    {
      "timestamp": "2026-08-08T10:00:00Z",
      "temperature": 71.2
    },
    {
      "timestamp": "2026-08-08T10:00:01Z",
      "temperature": 71.4
    }
  ]
}
```

The policy can specify:

```json
"readings": "readings"
```

AnyLog then treats each entry in the `readings` list as an independent input record.

Conceptually:

```text
Incoming Message
       │
       ├── site
       ├── device
       │
       └── readings
            │
            ├── Reading 1
            ├── Reading 2
            └── Reading 3
                   │
                   ▼
              Mapping Schema
                   │
                   ▼
                DB Rows
```

If `readings` is not specified, the complete JSON object is treated as a reading.

If the supplied input itself is a list, each list entry becomes a reading.

---

## 7. `schema`

The `schema` is the core of the mapping policy.

It defines the destination columns and how their values are obtained.

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

Each key in `schema` is normally the **destination column name**:

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

For every reading, AnyLog iterates over the schema and builds one output row.

---

## 8. `type`

Every regular mapped column requires a data type.

Example:

```json
"temperature": {
  "type": "float"
}
```

Typical types include:

```text
varchar
int
float
timestamp
bool
uuid
```

The mapper normalizes the specified type before creating the output value.

Examples:

```json
"asset": {
  "type": "varchar"
}
```

```json
"count": {
  "type": "int"
}
```

```json
"value": {
  "type": "float"
}
```

```json
"timestamp": {
  "type": "timestamp"
}
```

---

## 9. Default Mapping by Column Name

If `bring` is omitted, AnyLog attempts to retrieve a source attribute with the same name as the destination column.

For example:

```json
"schema": {
  "temperature": {
    "type": "float"
  }
}
```

with input:

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

This makes simple mappings very concise.

---

## 10. `bring`

`bring` specifies where the value should be retrieved from the input JSON.

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

`bring` is especially useful when the source attribute name differs from the destination column name.

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

The `bring` instruction is parsed and reused while processing subsequent rows.

---

## 11. `default`

`default` defines the value to use when `bring` does not return data.

Example:

```json
"quality": {
  "type": "varchar",
  "bring": "[quality]",
  "default": "good"
}
```

If the incoming reading is:

```json
{
  "temperature": 72.5
}
```

the mapped output can contain:

```json
{
  "quality": "good"
}
```

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

If the source does not provide a timestamp, AnyLog inserts the current UTC time.

---

## 12. `root`

Normally, a schema column retrieves its value from the current object being processed from the `readings` list.

Sometimes a value belongs to the root message instead.

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

The schema can retrieve `site` from the root object:

```json
"site": {
  "type": "varchar",
  "bring": "[site]",
  "root": true
}
```

while reading `temperature` from the individual reading:

```json
"temperature": {
  "type": "float",
  "bring": "[temperature]"
}
```

This produces:

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

## 13. `value`

`value` can be used to identify the source attribute that should be used when determining the mapping.

For example:

```json
"value": "bring [temperature]"
```

The mapping implementation recognizes a `bring [...]` expression in `value` and uses the referenced source attribute when retrieving the value.

This is also used by mappings that derive information from PLC attribute names or regular-expression matches.

---

## 14. `apply`

`apply` transforms a source value before placing it in the destination row.

The provided implementation supports the following regular mapping transformations.

### `epoch_to_datetime`

```json
"timestamp": {
  "type": "timestamp",
  "bring": "[time]",
  "apply": "epoch_to_datetime"
}
```

This converts an epoch value into a datetime representation.

### `json_dump`

```json
"metadata": {
  "type": "varchar",
  "bring": "[metadata]",
  "apply": "json_dump"
}
```

If `metadata` is an object:

```json
{
  "manufacturer": "ABC",
  "model": "X7"
}
```

`json_dump` serializes the object into a JSON-formatted string suitable for storage in a character column.

---

## 15. Multiple Mapping Alternatives for One Column

A schema column does not have to contain only one mapping definition.

It can contain a **list of definitions**:

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

AnyLog evaluates the alternatives and applies the one matching the current database and table.

This allows a single policy schema to contain table-specific or database-specific mapping definitions.

Conceptually:

```text
temperature
    │
    ├── if table = compressors
    │       bring [compressor_temp]
    │
    └── if table = pumps
            bring [pump_temp]
```

---

## 16. Column-Level `dbms` and `table`

Inside a column definition, `dbms` and `table` restrict that mapping definition to a particular destination.

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

A definition whose `dbms` or `table` does not match the current destination is skipped.

---

## 17. Dynamic Columns with `*`

A special schema entry named `*` can be used when the source contains attributes that should automatically become relational columns.

Example:

```json
"schema": {
  "*": {
    "type": "*",
    "bring": ["*"]
  }
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

AnyLog can generate columns corresponding to the source attributes:

```text
temperature
pressure
rpm
```

This is useful when the incoming data structure is dynamic or when enumerating every source attribute in the policy is undesirable.

---

## 18. Bringing Dynamic Columns from Subobjects

The `*` mechanism can also retrieve dictionaries under selected source keys.

For example:

```json
"schema": {
  "*": {
    "type": "*",
    "bring": [
      "fields",
      "tags"
    ]
  }
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

The generated column names are prefixed by the parent key:

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

## 19. `params`

`params` allows the same schema to be repeated with different parameter values.

Each element of `params` represents another output-row configuration.

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

The schema can reference these values with:

```text
params.0
params.1
params.2
```

For example:

```json
"schema": {
  "timestamp": {
    "type": "timestamp",
    "default": "now()"
  },

  "Monitor_ID": {
    "type": "varchar",
    "default": "params.0"
  },

  "ACC": {
    "type": "int",
    "bring": "params.1"
  },

  "PRE": {
    "type": "int",
    "bring": "params.2"
  }
}
```

For the first parameter list:

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

The policy is therefore effectively executed once for each parameter set.

---

## 20. `script`

A column definition can include a `script` that is executed before the normal column mapping.

Example structure:

```json
"some_column": {
  "script": "<AnyLog script>",
  "type": "varchar",
  "bring": "[value]"
}
```

A script can influence the mapping flow.

The implementation recognizes outcomes that can:

- Skip the current attribute.
- Skip the complete event.
- Exit the script but continue processing.
- Change to another mapping policy.

This makes scripts useful for conditional processing and more complex mapping decisions.

---

## 21. Script-Only Schema Entries

Schema names beginning and ending with two underscores are treated specially.

Examples:

```json
"__start__": {
  "script": "..."
}
```

```json
"__end__": {
  "script": "..."
}
```

These entries can execute mapping logic without creating a destination table column.

Conceptually:

```text
schema
 │
 ├── __start__      script only
 │
 ├── timestamp      destination column
 │
 ├── temperature    destination column
 │
 └── __end__        script only
```

---

## 22. Blob Columns

A column can be identified as blob/file data:

```json
"image": {
  "type": "varchar",
  "bring": "[image]",
  "blob": true,
  "hash": "md5",
  "extension": "jpg"
}
```

When `blob` is `true`, AnyLog writes the blob to the configured blob directory rather than keeping the complete binary content in the relational row.

The implementation currently expects:

```json
"hash": "md5"
```

The generated hash identifies the stored file.

An extension can optionally be added:

```json
"extension": "jpg"
```

The result stored in the row references the generated blob file.

---

## 23. Blob Transformations

Blob mappings can also specify an `apply` operation.

The supplied implementation supports blob processing including:

```json
"apply": "base64decoding"
```

and:

```json
"apply": "opencv"
```

For example:

```json
"image": {
  "type": "varchar",
  "bring": "[image]",
  "blob": true,
  "hash": "md5",
  "extension": "jpg",
  "apply": "base64decoding"
}
```

This can decode a Base64 source value before writing the file.

---

## 24. Timestamp Handling

Timestamp columns receive special processing.

Example:

```json
"timestamp": {
  "type": "timestamp",
  "bring": "[timestamp]"
}
```

The mapping code accepts several forms of timestamp input, including:

- Date/time strings.
- ISO-formatted timestamps with timezone offsets.
- Integer timestamps.
- Floating-point timestamps.
- Numeric strings.

Numeric timestamps are interpreted by the timestamp mapping logic and converted into the datetime representation used by AnyLog.

A common pattern is:

```json
"timestamp": {
  "type": "timestamp",
  "bring": "[timestamp]",
  "default": "now()"
}
```

---

## 25. Complete Example

Consider the following source message:

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

The corresponding mapping policy could be:

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

The first reading produces approximately:

```json
{
  "timestamp": "2026-08-08T18:30:00Z",
  "site": "Plant_A",
  "asset": "compressor_1",
  "temperature": 72.5,
  "pressure": 101.4
}
```

The second produces:

```json
{
  "timestamp": "2026-08-08T18:30:01Z",
  "site": "Plant_A",
  "asset": "compressor_2",
  "temperature": 74.1,
  "pressure": 102.7
}
```

Notice that `site` comes from the root message because:

```json
"root": true
```

while `asset`, `temperature`, `pressure`, and `timestamp` come from each individual reading.

---

## 26. Mapping Processing Model

At a high level, AnyLog processes a mapping policy as follows:

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
               For Each Reading
                       │
                       ▼
                 For Each Param
                (when specified)
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
                 Convert Type
                       │
                       ▼
                  Output Row
                       │
                       ▼
               Destination Table
```

---

## 27. Column Mapping Logic

For a normal schema column, the conceptual processing sequence is:

```text
1. Select the applicable column definition
          │
          ▼
2. Execute script, if defined
          │
          ▼
3. Determine column type
          │
          ▼
4. Determine source attribute
          │
          ▼
5. Select current reading or root JSON
          │
          ▼
6. Execute bring
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
                                   Convert type
                                         │
                                         ▼
                                  Destination value
```

---

## 28. Mapping Policy Reference

The principal policy-level attributes are:

| Attribute | Purpose |
|---|---|
| `id` | Unique policy identifier |
| `dbms` | Destination database |
| `table` | Destination table |
| `source` | Identifies the incoming data source |
| `readings` | Identifies the portion of the message containing readings |
| `params` | Repeats mapping using different parameter sets |
| `schema` | Defines the destination columns and mapping rules |

The principal schema-column attributes are:

| Attribute | Purpose |
|---|---|
| `type` | Destination data type |
| `bring` | Retrieves a value from the source JSON |
| `default` | Value used when the source value is unavailable |
| `root` | Retrieves the value from the root message instead of the current reading |
| `value` | Identifies or derives the source value used for mapping |
| `apply` | Applies a transformation to the value |
| `script` | Executes conditional or procedural mapping logic |
| `dbms` | Restricts a mapping option to a database |
| `table` | Restricts a mapping option to a table |
| `blob` | Treats the source value as file/blob data |
| `hash` | Defines the blob hash mechanism; current implementation recognizes `md5` |
| `extension` | Adds a file extension to a stored blob |

Special schema constructs include:

| Construct | Purpose |
|---|---|
| `"*"` | Dynamically creates columns from source attributes |
| `"__name__"` | Script/control entry that does not create a table column |
| List of column definitions | Provides alternative mappings for the same output column |
| `params.N` | Substitutes values from a policy parameter set |

---

## 29. Minimal Mapping Policy

For source data whose names already match the table column names, the policy can be very simple:

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

Given:

```json
{
  "timestamp": "2026-08-08T18:30:00Z",
  "asset": "compressor_7",
  "temperature": 72.5
}
```

the column names themselves are used to retrieve the source attributes.

This is the simplest form of an AnyLog Mapping Policy:

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

The additional mapping attributes are needed only when the source structure, destination structure, or required processing is more complex.
