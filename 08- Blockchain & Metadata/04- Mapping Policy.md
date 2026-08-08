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
--->

Mapping policies are a way to synchronize between the content coming in (i.e. data in JSON format) and the way it is stored.

In previous sections ([Message Broker](../04-%20Southbound%20Interfaces/02-%20Direct%20Connectors/02-%20Message%20Broker.md))
the idea of mapping was covered indirectly via `run msg client` and a quick explanation of mapping policies.

## Components of the Mapping Policy

Rather than writing the topic's mapping inline on every `run msg client` call, you can register the mapping once as
a **policy** on the blockchain, and reference it by name. This is useful when the same mapping is reused across
multiple subscriptions, or when you want the mapping managed centrally rather than duplicated in each command.

The following mapping policy is based on the data below. By the end of this data, the policy will have generated 3
tables on the `smart_city` logical database and 1 table on the `monitoring` logical database.

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
> The fourth reading (humidity, `value: 60.5`) omits `timestamp` on purpose — that's the case the schema's
> `"default": "now()"` below is for.

The associated mapping policy would be:
```json
{"mapping": {
    "id": "!policy_id",
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
}}
```
* `id` — the blockchain ID. Because this is used by a human when writing `run msg client`, it's one of the few
  cases where we recommend defining the ID yourself rather than letting AnyLog auto-generate a hash.
* `dbms` — the logical database where content is to be stored.
* `table` — the table within the logical database the content is stored under.
* `readings` — empty here because this payload is already flat (no nested array to unwrap); see
  [the `readings` key](#readings-key) below for when it's used.

As a `run msg client`:

```anylog
# using mapping policy
<run msg client where 
    broker=local and log=false and topic=(
        name=[topic name] and 
        policy=!policy_id
    )>

# or manually - what we've done before 
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

### `readings` key

You'll notice that there's a param called `readings` in the `mapping` policy. This is for when data is not as nicely
flat in the JSON.

For example, let's say the data looks something like this:

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

Instead of specifying the full nested path in every field's `bring` (e.g. `bring [data][][timestamp]`), set
`"readings": "[data]"` once in the policy, and each field's `bring` can then reference just `[timestamp]` relative
to each entry in that array.

## Timestamp

When running `run msg client` the default supported timestamp format is based on `%Y-%m-%d %H:%M:%S.%f`.
However, most devices use an epoch timestamp instead. To handle that, the mapping policy provides an `apply`
function that's able to translate a numeric epoch value into a timestamp.

```json
{"timestamp" : {
    "bring": "[origin]",
    "default" : "now()",
    "type" : "timestamp",
    "apply" :  "epoch_to_datetime"
}}
```
> `[origin]` here is just this example's source field name for the epoch value — it doesn't need to be called
> `origin`; `bring` points at whatever field in the incoming JSON actually holds it.

## Blob Data

Blob data is also unique because it requires mapping data that's ultimately stored in a
[NoSQL database](../99-%20INTERNAL%20%26%20DRAFT%20sections%20%28NOT%20publicly%20visible%29/C-%20Reference%20Materials/05-image%20mapping.md#image-mapping) to its associated SQL representation. For this, AnyLog supports
base64 encoding and OpenCV encoding.

```json
{
 "file": {
    "root": true,
    "blob": true,
    "bring": "[file_content]",
    "extension": "jpeg",
    "apply": "base64decoding",
    "hash": "md5",
    "type": "varchar"
  }
}
```

### Defining `apply` logic for a file

```anylog 
set policy new_policy [mapping][schema][file][apply] = "base64decoding"

# - OR - 

set policy new_policy [mapping][schema][file][apply] = "opencv"
```

## Unknown columns

There are cases, such as _Telegraf_ and _Litmus Edge_, where the engineer may not know the content, or content type
(i.e. data types for each key in the JSON), coming into the node. While AnyLog tries to validate those automatically
(for PUT) or via mapping (for `run msg client`) as data flows in, there are always cases where this isn't known ahead
of time.

To resolve that, there are 2 ways the mapping supports this:

* We don't know the data, but do know which keys we want to extract:
```json
{"*" : {
  "type": "*",
  "bring": ["success", "tagName", "value", "description"]
  }
}
```

* We don't know the keys or data types at all:
```json
{"*" : {
  "type": "*",
  "bring": ["*"]
  }
}
```

## A complete mapping policy with "all" options

Sample input (an EdgeX-Foundry-style payload):
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

The corresponding mapping policy:
```json
{
  "mapping": {
    "id": "full-policy",
    "dbms": "edgex_data",
    "table": "bring [deviceName]",
    "readings": "[readings]",
    "schema": {
      "timestamp": {
        "type": "timestamp",
        "default": "now()",
        "bring": "[timestamp]",
        "apply": "epoch_to_datetime"
      },
      "file": {
        "root": true,
        "blob": true,
        "bring": "[file_content]",
        "extension": "jpeg",
        "apply": "base64decoding",
        "hash": "md5",
        "type": "varchar"
      },
      "*": {
        "type": "*",
        "bring": ["deviceName", "resourceName", "profileName"]
      }
    }
  }
}
```
