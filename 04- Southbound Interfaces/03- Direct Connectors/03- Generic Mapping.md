---
title: "Generic Mapping"
description: Ingest data from devices and sensors via MQTT or REST POST without writing a mapping first — AnyLog derives the table, columns, and UNS from the topic and payload.
layout: page
source_path: "03- Generic Mapping.md"
tags:
    - UNS
    - MQTT
    - REST
---

<!---
### 📜 Change Log

| **Date** | **Name** | **Change** |
|---|---|---|
| 2026-09-25 | Ori Shadmon | Created document |
--->

> **AnyLog only.** `dynamic=true` UNS generation is not available in EdgeLake.

A common first question from new users is *"can I just publish my data over MQTT or POST?"* The answer is yes — but
the usual path requires knowing the payload structure up front, so the topic can be mapped to a table and each field
to a typed column [Message Broker](02-%20Message%20Broker.md) and [REST POST](01-%20REST.md#publishing-data-via-post)). 
That means reverse-engineering what the device emits, and deciding what the end result should look like, before a single 
row is stored. On a new deployment with dozens of device types, that step is usually the bottleneck.

Configuring a message client, either with AnyLog or third-party message broker, **Generic mapping** removes it. The 
message client is given only a topic and a database, with `dynamic=true` and no `column.*` mapping. AnyLog then:

1. derives the **table name** from the topic,
2. derives the **columns and their types** from the JSON keys and values in the payload
3. publishes a **UNS hierarchy** for the data to the blockchain, based on the topic path — see [Unified Namespace](../../08-%20Blockchain%20&%20Metadata/04-%20Unified%20Namespace.md)

The data is accepted as-is on day one. Explicit mapping can still be added later for the topics where it matters.

---

## Generic vs. Explicit Mapping

Generic mapping is the fastest way to get data in. Explicit mapping is the right choice once you know which fields
matter, need specific types or names, or need to split one topic into several tables (see [Dynamic Ingestion with 
Custom UNS](../../08-%20Blockchain%20&%20Metadata/04-1%20UNS%20Custom%20Dynamic%20Examples.md)).

Two independent settings control how a topic is ingested. **Mapping** decides how JSON keys become columns, and
**`dynamic`** decides whether a UNS is created and where the table name comes from. They can be combined in any way.

**Mapping**: how JSON keys become columns

| | Explicit mapping (default) | Generic mapping |
|---|:---:|:---:|
| How it's set | `column.*` (inline) or a mapping policy | No `column.*` |
| JSON keys → column names & types | Matched by you | Derived from the payload |
| Need to know the payload up front | Yes | No |

**`dynamic`**: UNS and table name

| | `dynamic=false` (default) | `dynamic=true` |
|---|:---:|:---:|
| UNS generated | No | Yes |
| `master_node` required | No | Yes (UNS policies are published to it) |
| Table name | Set by you (`table=...`) | `table=...` if provided, otherwise derived from the topic |
---

## Example 1: A Single JSON Object over MQTT

### The data

A vessel publishes one JSON object per reading, with the measurement name as the last topic segment.

Topic: `vessel-data2/batteryStateOfChargePercent`

```json
{
  "component": "batteryStateOfChargePercent",
  "IP": null,
  "ID": null,
  "side": "B",
  "boat": "Helios",
  "end_ts":     "2026-11-06T21:44:46.863435Z",
  "start_ts":   "2026-09-25T21:44:46.863435Z",
  "timestamp":  "2026-09-25T21:44:46.863435Z",
  "value": 99
}
```

### The message client

The client subscribes to everything under `vessel-data2/` and provides only the database. There is no `table` and
no `column.*` mapping. Because `dynamic=true` publishes new UNS policies, `master_node` identifies the Master Node they
are published to.

```anylog
<run msg client where
    broker=172.104.228.251 and port=1883 and
    user=anyloguser and password=mqtt4AnyLog! and
    log=false and
    master_node=!ledger_conn and
    topic=(
        name=vessel-data2/# and
        dbms=!default_dbms and
        dynamic=true
    )>
```


### The result

1. **A table, created automatically.** The last topic segment becomes the table name, lowercased and suffixed
(`batterystateofchargepercent_1`). Each JSON key becomes a column, lowercased (`IP` → `ip`, `ID` → `id`), and the
ISO 8601 strings are stored as timestamps.

```anylog
run client () sql mydb format=table "select * from batterystateofchargepercent_1"
```

```anylog
row_id insert_timestamp           tsd_name tsd_id component                   ip   id   side boat   end_ts                     start_ts                   timestamp                  value
------ -------------------------- -------- ------ --------------------------- ---- ---- ---- ------ -------------------------- -------------------------- -------------------------- -----
     1 2026-09-25 21:45:08.809978      136     55 batteryStateOfChargePercent None None B    Helios 2026-11-06 21:44:46.863435 2026-09-25 21:44:46.863435 2026-09-25 21:44:46.863435    99

{"Statistics":[{"Count": 1,
                "Time":"00:00:00",
                "Nodes": 1}]}
```

`row_id`, `insert_timestamp`, `tsd_name` and `tsd_id` are added by AnyLog; the rest comes from the payload.

2. **A UNS hierarchy, published to the blockchain.** Each topic segment becomes a `UNS` policy, linked to its
parent by `id`. Segment names are normalized (`vessel-data2` → `vessel_data2`). Each `UNS` policy is paired with an
`object` policy; for the leaf, the object carries the `dbms` and `table` where the data lives.

```anylog
blockchain get uns bring.extend
```

```json
[{"uns" : {"name" : "vessel_data2",
           "namespace" : "vessel_data2",
           "source_node" : "81afcd01d803-acme-operator-7559@172.27.0.2:32148",
           "object_id" : "f24f7b124395050747a1c42bc316b44e",
           "id" : "2d2cf966293923e935562f208d0cff0f",
           "date" : "2026-09-25T21:36:56.356188Z",
           "ledger" : "global"},
  "object" : {"name" : "vessel_data2",
              "description" : "object for MQTT vessel_data2",
              "id" : "f24f7b124395050747a1c42bc316b44e",
              "date" : "2026-09-25T21:36:56.341369Z",
              "ledger" : "global"}},
 {"uns" : {"name" : "batterystateofchargepercent",
           "namespace" : "vessel_data2/batterystateofchargepercent",
           "source_node" : "81afcd01d803-acme-operator-7559@172.27.0.2:32148",
           "parent" : "2d2cf966293923e935562f208d0cff0f",
           "object_id" : "c259e45495acc903a876aa4345ce04d8",
           "id" : "5b6757eff0f9142408f9e5bf3885e546",
           "date" : "2026-09-25T21:44:52.042883Z",
           "ledger" : "global"},
  "object" : {"name" : "batterystateofchargepercent_1",
              "description" : "object for MQTT batterystateofchargepercent_1",
              "dbms" : "mydb",
              "table" : "batterystateofchargepercent_1",
              "id" : "c259e45495acc903a876aa4345ce04d8",
              "date" : "2026-09-25T21:44:52.025471Z",
              "ledger" : "global"}}]
```

Other topics published under `vessel-data2/` on the same stream (for example `ach65`, `bcl25`, `bmwix`, `gd`)
appear as siblings of `batterystateofchargepercent`, each with its own table — no additional configuration needed.

> **To verify:** the query above is a reconstruction — the original capture listed the full tree without the
> command. Also note that the uns/object split shown here differs from older examples (UNS page, factory-floor
> example) where `dbms`/`table` sit directly on the `uns` policy; worth aligning those docs.

**3. A subscription you can monitor.**

```anylog
get msg client
```

Lists the subscription, message and error counters, and each topic that `dynamic=true` has materialized into a
table.

> **To verify:** the draft said "3 components" but only showed two. Replace this third item with whatever was
> intended if it wasn't the subscription view.

---

## Example 2: The Same Data over REST (POST)

The REST version is the same client with `broker=rest` instead of an MQTT broker address.

1. Start the message client (once), either on the node's CLI or via POST:

```anylog
<run msg client where
    broker=rest and user-agent=anylog and
    log=false and
    master_node=!ledger_conn and
    topic=(
        name=vessel-data2/# and
        dbms=!default_dbms and
        dynamic=true
    )>
```

2. Publish data, with the full topic path in the `topic` header:

```shell
curl -X POST http://[Operator IP]:[Operator Port] \
  -H "command: data" \
  -H "topic: vessel-data2/batteryStateOfChargePercent" \
  -H "AnyLog-Agent: AnyLog/1.23" \
  -H "Content-Type: application/json" \
  -d '{"component": "batteryStateOfChargePercent", "IP": null, "ID": null, "side": "B", "boat": "Helios",
       "end_ts": "2026-11-06T21:44:46.863435Z", "start_ts": "2026-09-25T21:44:46.863435Z",
       "timestamp": "2026-09-25T21:44:46.863435Z", "value": 99}'
```

The resulting table and UNS are the same as in Example 1.

> **To verify:** this example hasn't been run. Confirm that (a) the `#` wildcard matches a full topic path passed
> in the `topic` header with `broker=rest` (the factory-floor example suggests it does), and (b) a single JSON
> object is accepted in the body, not only a JSON array.

`PUT` is not an option here: it stores data into the database/table given in the headers, with no mapping and no
UNS generation.

---

## Things to Know

* **Naming is normalized.** Topic segments and JSON keys are lowercased, and characters such as `-` become `_`.
  Table names get a numeric suffix (`_1`). Query using the normalized names.
* **The topic defines the tree.** The UNS is only as readable as the topic. If devices publish raw MAC addresses
  or IPs as segments, that's what users will click through. Shaping the topic on the publisher side is the fix —
  see <a href="../../08-%20Blockchain%20&%20Metadata/04-1%20UNS%20Custom%20Dynamic%20Examples.md#building-a-namespace-the-customer-can-actually-navigate" target="_blank">Building a namespace the customer can actually navigate</a>.
* **One topic, one table.** Every message on a given topic lands in the same table. If one topic carries several
  different measurements, use `dynamic=true` with explicit mapping and a per-row `table` field instead.

> **To verify before publishing:**
> * **Type inference from nulls** — in the example, `IP` and `ID` are `null` on the first message. What type do
>   those columns get, and what happens when a later message sends a string or number?
> * **Schema drift** — if a later message on the same topic adds a new key, is a column added, is the key
>   dropped, or does the message fail?
> * **Time column** — the payload has three timestamps (`timestamp`, `start_ts`, `end_ts`). Which one, if any, is
>   used as the table's time column, and does AnyLog fall back to `insert_timestamp` when none is present?
> * **Other payload shapes** — the heading "Example 1" implies more cases. Worth adding a JSON array (several rows
>   per message) and a nested JSON object once their behavior is confirmed.

---

## Moving to Explicit Mapping Later

Generic mapping and explicit mapping aren't exclusive. A common pattern is to start generic to see what devices
actually send, then tighten the topics that matter:

* add `column.*` mapping to a topic while keeping `dynamic=true` (the UNS is still generated), or
* register a reusable mapping policy — see
  <a href="02-%20Message%20Broker.md#registering-a-mapping-policy" target="_blank">Registering a Mapping Policy</a>.

---

## See Also

* <a href="01-%20REST.md" target="_blank">Publishing data via REST</a> — PUT vs POST and support commands
* <a href="02-%20Message%20Broker.md" target="_blank">Message Broker</a> — MQTT/Kafka clients and mapping policies
* <a href="../../08-%20Blockchain%20&%20Metadata/04-%20Unified%20Namespace.md" target="_blank">Unified Namespace</a> — the UNS model and `dynamic=true`
* <a href="../../08-%20Blockchain%20&%20Metadata/04-1%20UNS%20Custom%20Dynamic%20Examples.md" target="_blank">Dynamic Ingestion with Custom UNS</a> — splitting one topic into several tables