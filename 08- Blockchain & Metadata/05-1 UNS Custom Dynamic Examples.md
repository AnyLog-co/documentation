---
title: "Dynamic Ingestion with Custom UNS — Factory Floor Example"
description: "A production-style walkthrough tracing how dynamic=true auto-generation and personalized column/table mapping connect, plus how to design a namespace customers can navigate by their own naming"
layout: page
source_path: "UNS-dynamic-custom-example.md"
tags:
    - UNS
    - MCP
    - example
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon | Converted changelog to standard table format; flagged a mismatch between the example payloads (no `ts` field) and the `column.timestamp.timestamp = "bring [ts]"` mapping; filled in the missing `id` field on the intermediate `device`/`ac233fad6a3c`/`motor` JSON output blocks (values were already implied by the next query's `parent=`, just not shown at their own level); fixed a missing blank line that risked a paragraph being swallowed into the preceding bullet list | |
 | 2026-07-14 | Ori Shadmon | Created document — split out of UNS.md's "Ingesting Data with dynamic=true" section to stand alone as a worked production example (factory floor: PLCs, motors, blowers over REST) | |
 | 2026-07-14 | Ori Shadmon | Strengthened the dynamic/personalized connection: added PUT vs POST/MQTT context, the ISO 8601 timestamp-format caveat, and a full traced example (root policy down to leaf table via `blockchain get uns where parent=...`) showing exactly which tree levels come from the raw topic and which come from the personalized `table`-field mapping | |
 | 2026-07-14 | Ori Shadmon | Added "Building a namespace the customer can actually navigate" section: shaping the publish-side topic string to use the customer's own naming (e.g. association/tag names instead of raw MAC addresses), and where a purely topic-driven tree runs out (many-to-many relationships), with a hybrid pointer to hand-authored policies for that case | |
--->

> **AnyLog only.** `dynamic=true` UNS definitions are not available in EdgeLake.

# Dynamic Ingestion with Custom UNS — Factory Floor Example

The <a href="./05-%20Unitfied%20Namespace.md" target="_blank">Unified Namespace</a> page introduces `dynamic=true` using single-value, single-topic examples (one
scalar per MQTT topic). In production, data rarely arrives that cleanly — a single topic often carries multiple
JSON rows covering different measurements from different equipment. This page walks through that more realistic
case: a factory floor publishing PLC and device readings over REST, where `dynamic=true` still drives automatic
UNS generation, but the mapping and table-splitting need to be defined explicitly rather than left fully
automatic.

This sits between the two approaches described in <a href="./05-%20Unitfied%20Namespace.md#auto-generated-vs-user-defined" target="_blank">Unified Namespace</a>:
still auto-generated (no `blockchain insert` of hand-authored policies, as in
<a href="./05-2%20UNS%20Custom%20Examples.md" target="_blank">Custom UNS (data stream, ISA-95)</a>), but with enough explicit column mapping that the resulting
namespace and table layout is effectively **personalized** rather than purely derived from the raw topic string.

### Why this requires POST or MQTT, not PUT

AnyLog supports two broad ways to publish data. `PUT` stores the payload as-is — the destination database and
table are given in the request headers, with no mapping and no UNS involvement. `POST` and MQTT-based clients,
by contrast, support mapping logic between the incoming payload and how/where it's stored, and are the only
paths that can declare UNS policies on the blockchain as data arrives. Everything in this page — the column
mapping, the `dynamic=true` auto-generation, the per-row table splitting — depends on using `POST` or MQTT as
the ingestion path; it isn't available to `PUT`-based ingestion.

---

## The scenario

A factory floor publishes readings from PLCs and networked devices to a single AnyLog node over REST, under a
shared topic prefix (`factory-x/#`). Three source types are in play, each with its own sub-topic:

```json
{
    "factory-x/plc/192.168.78.10/RobotRead": [
        {"table": "Main Robot.RobotRead.j1.cur",  "tag": "RobotRead.j1.cur",  "plc": "192.168.78.10", "mac": "", "value": 482.7},
        {"table": "Main Robot.RobotRead.j1.torq", "tag": "RobotRead.j1.torq", "plc": "192.168.78.10", "mac": "", "value": 118.3}
    ],
    "factory-x/device/AC233FAD6A3C/motor": [
        {"table": "Infeed 3 / Scale Motor Temp", "tag": "mot_temp_AC233FAD6A3C", "plc": "", "mac": "AC233FAD6A3C", "value": 98.32},
        {"table": "Infeed 3 / Scale Motor Vibr",  "tag": "mot_vibr_AC233FAD6A3C", "plc": "", "mac": "AC233FAD6A3C", "value": 0.042}
    ],
    "factory-x/plc/192.168.78.10/Blower/VFD": [
        {"table": "Blower Info", "tag": "Blower.VFD.CurVoltsHMI", "plc": "192.168.78.10", "mac": "", "value": 281.45},
        {"table": "Blower Info", "tag": "Blower.VFD.CurAmpsHMI",  "plc": "192.168.78.10", "mac": "", "value": 22.47}
    ]
}
```
> Shown together above for readability, but these represent three separate messages arriving under three
> separate topics — not one combined payload on the wire.

Each row carries its own `table`, `tag`, `plc`/`mac` identifier, and `value` — this is full JSON, not a bare
scalar, and different rows under the same base topic represent different measurements. Neither of those two
facts rules out `dynamic=true` and auto-generated UNS; they just mean the client needs explicit column mapping
and a per-row table strategy.

---

## Message client: full JSON with explicit column mapping

A single client subscribes to the lowest common denominator of the topic tree — `factory-x/#` — and maps each field
out of the JSON payload using `column.[name].[type] = "bring [json-path]"`:

```anylog
<run msg client where
    broker = rest and
    user-agent = anylog and
    log = false and
    master_node = !ledger_conn and
    topic = (
        name = "factory-x/#" and
        dbms = !default_dbms and
        column.timestamp.timestamp = "bring [ts]" and
        column.tag.str = "bring [tag]" and
        column.plc.str = "bring [plc]" and
        column.mac.str = "bring [mac]" and
        column.value.float = "bring [value]" and
        dynamic = true
    )>
```
> **To verify:** none of the three example payloads above include a `ts` field — only `table`/`tag`/`plc`/`mac`/`value`.
> Either the sample payloads are missing a timestamp field that should be added, or this mapping should reference
> a field that's actually present (or fall back to a `default: "now()"`-style pattern, as used elsewhere in these
> docs when no source timestamp is available). Worth reconciling before this ships as a copy-pasteable example.

`dynamic=true` combined with `master_node` in the client config is what drives both the automated table naming
and the `uns` policy declarations published to the blockchain. The explicit `column.*` mappings don't turn this
into policy-mapped ingestion — they only control how each field is typed and extracted from the JSON; the UNS
hierarchy is still derived automatically from the topic.

---
## Splitting one topic into multiple tables

A mapping logic can either store data dynamically (i.e. `dynamic=true`), and then its (sub) topic resides in its
own table — or a table that's either hardcoded into the command or is part of the payload coming in.

Left on the first option alone, every row published under a shared base topic — for example everything under
`factory-x/device/AC233FAD6A3C/motor` — would collapse into a single table, regardless of whether it represents
a temperature reading or a vibration reading.
The way out is the second option: extract a per-row `table` field from the payload and treat it as the final segment of
that row's effective topic, so each row's `table` value becomes the differentiator —

- `factory-x/device/AC233FAD6A3C/motor` rows with `"table": "Infeed 3 / Scale Motor Temp"` resolve to their own
  table (`infeed_3_scale_motor_temp`)
- rows with `"table": "Infeed 3 / Scale Motor Vibr"` resolve to a separate table (`infeed_3_scale_motor_vibr`)

Both tables live side by side under the same `motor` namespace node in the resulting UNS tree, rather than
merging into one. The same logic applies to the `RobotRead` and `Blower/VFD` topics above — each distinct
`table` value under a shared sub-topic becomes its own leaf.

---

## The connection: how personalized mapping shapes the dynamic tree

`dynamic=true` alone only knows how to do one thing: walk a topic string segment by segment and turn each
segment into a parent-linked `uns` policy. Left on its own, it can't distinguish two different measurements
published under the same topic, and it has no way to enrich each level with typed columns. That's exactly the
gap the personalization from the previous two sections fills — the `column.*` mapping and the per-row `table`
append are not a separate mechanism running alongside `dynamic=true`; they are the inputs that `dynamic=true`
walks.

Querying the blockchain after ingestion shows this directly. Starting from the root and following `parent` down
one level at a time:

```bash
# Root policy — the base topic segment
curl -X GET http://192.168.86.29:32149 -H "command: blockchain get root policies exclude cluster" -H "User-Agent: AnyLog/1.23" | jq
```
```json
[{"uns": {"name": "factory-x", "namespace": "factory-x", "dbms": "mydb", "table": "factory-x_1",
          "id": "c7e14e59ed39a83555b044d9bdf5174b", "ledger": "global"}}]
```

```bash
# Child of factory-x — the next raw topic segment
curl -X GET http://192.168.86.29:32149 -H "command: blockchain get uns where parent=c7e14e59ed39a83555b044d9bdf5174b bring.first" -H "User-Agent: AnyLog/1.23" | jq
```
```json
[{"uns": {"name": "device", "namespace": "factory-x/device", "dbms": "mydb", "table": "device_1",
          "id": "9c4be8d724b2472146cd9bdef8a721c9", "parent": "c7e14e59ed39a83555b044d9bdf5174b", "ledger": "global"}}]
```

```bash
# Child of device — still a raw topic segment (the device MAC)
curl -X GET http://192.168.86.29:32149 -H "command: blockchain get uns where parent=9c4be8d724b2472146cd9bdef8a721c9 bring.first" -H "User-Agent: AnyLog/1.23" | jq
```
```json
[{"uns": {"name": "ac233fad6a3c", "namespace": "factory-x/device/ac233fad6a3c", "dbms": "mydb",
          "table": "ac233fad6a3c_1", "id": "ee56a809e7a51af6d64660e6aab34ad7", "parent": "9c4be8d724b2472146cd9bdef8a721c9", "ledger": "global"}}]
```

```bash
# Child of ac233fad6a3c — still a raw topic segment
curl -X GET http://192.168.86.29:32149 -H "command: blockchain get uns where parent=ee56a809e7a51af6d64660e6aab34ad7 bring.first" -H "User-Agent: AnyLog/1.23" | jq
```
```json
[{"uns": {"name": "motor", "namespace": "factory-x/device/ac233fad6a3c/motor", "dbms": "mydb",
          "table": "motor_1", "id": "9d4cad129914aeb92edda8c18cacbafe", "parent": "ee56a809e7a51af6d64660e6aab34ad7", "ledger": "global"}}]
```

```bash
# Child of motor — this is where the raw topic runs out, and the personalized `table` field takes over
curl -X GET http://192.168.86.29:32149 -H "command: blockchain get uns where parent=9d4cad129914aeb92edda8c18cacbafe bring.first" -H "User-Agent: AnyLog/1.23" | jq
```
```json
[{"uns": {"name": "infeed_3_scale_motor_vibr", "namespace": "factory-x/device/ac233fad6a3c/motor/infeed_3_scale_motor_vibr",
          "dbms": "mydb", "table": "infeed_3_scale_motor_vibr_1", "parent": "9d4cad129914aeb92edda8c18cacbafe", "ledger": "global"}}]
```

The first four levels (`factory-x` → `device` → `ac233fad6a3c` → `motor`) are the raw topic path,
`factory-x/device/AC233FAD6A3C/motor`, walked one segment at a time — this part is exactly what `dynamic=true` would
do on its own, with no personalization involved. The fifth level, `infeed_3_scale_motor_vibr`, doesn't come from
the topic at all — the raw topic ends at `motor`. It comes from the per-row `table` field described above, which
the client's personalized mapping appends as one more segment. That's the concrete connection between the two
halves of this pattern: **dynamic auto-generation supplies the walk-the-topic mechanism, and personalized
mapping supplies the extra segment (and the typed columns at every level) that the raw topic alone couldn't
provide.** Remove the personalization and every row under `factory-x/device/AC233FAD6A3C/motor` — temperature and
vibration alike — would land in one `motor_1` table with no way to tell them apart; remove `dynamic=true` and
none of this tree gets built at all, personalized or not.

Each level's `id` becomes the next level's `parent`, and the `namespace` grows by exactly one segment at each
step — so the tree is fully traversable and the namespace path stays human-readable all the way to the leaf.

---

## Why this counts as "personalized" UNS

This pattern sits deliberately between the two poles described in <a href="./05-%20Unitfied%20Namespace.md" target="_blank">Unified Namespace</a>, and the tree
traced above is the product of exactly that middle position:

| | Fully auto-generated | This pattern | Fully user-defined |
|---|:---:|:---:|:---:|
| UNS hierarchy source | Raw topic path | Topic path + per-row `table` field | Hand-authored policy JSON |
| Schema required | No | No (mapped, not declared) | Yes |
| Column typing | Inferred | Explicit (`column.*.type`) | Explicit (in the policy) |
| Multiple tables per topic | No (one topic = one table) | Yes (via `table` field) | Yes (by design) |

The hierarchy is still generated automatically and still requires no `blockchain insert` of hand-authored
policies — but because the mapping and table-splitting are explicit rather than inferred, the resulting
namespace reflects a deliberate design (which fields become columns, which rows become distinct tables) rather
than a literal mirror of whatever the topic string happens to look like.

---

## Building a namespace the customer can actually navigate

The traced tree above works, but look at what a person browsing it actually sees:
`factory-x/device/ac233fad6a3c/motor/infeed_3_scale_motor_vibr`. The middle segment is a raw MAC address — accurate,
but meaningless to someone drilling down who doesn't already have a lookup table mapping MACs to physical
equipment. A customer who wants to browse their own data usually already has a naming scheme they think in —
for example, a set of named **tags** grouped into named **associations** (with the underlying time-series values
tracked separately) — and wants the UNS tree to read in those terms, not in device-identifier terms.

**The fix is upstream of AnyLog, not a different AnyLog feature.** Because `dynamic=true` does nothing more than
walk whatever segments the topic string contains, the namespace is only ever as readable as the topic itself.
To get `factory-x/<association_name>/<tag_name>` instead of `factory-x/device/<mac>/<subsystem>`, the publisher needs to
construct that topic string — using the customer's own association and tag names — before the data is ever
posted to AnyLog. Nothing about the message client changes; the `column.*` mapping and `dynamic=true` config
stay the same. Only the topic the publisher constructs changes, and the auto-generated tree follows it exactly.

This is a natural extension of the per-row `table`-field technique already used above (renaming
`AC233FAD6A3C/motor` readings to `Infeed 3 / Scale Motor Temp`/`Vibr` at the leaf) — it's the same idea applied
one or two levels higher, to the segments a human actually has to click through to get there, not just the final
leaf name.

### Where this approach runs out: many-to-many relationships

A purely topic-driven tree is still a strict single-parent hierarchy — each `uns` policy has exactly one
`parent`. That's a good match for a naming scheme where every tag belongs to exactly one association. It breaks
down if the customer's own model allows a tag to belong to **more than one** association at once (a many-to-many
relationship tracked by ID in their own database, for example) — the auto-generated tree has no way to attach
one leaf under two different parents.

AnyLog's blockchain policies also don't currently enforce foreign-key-style referential integrity — a tag
"belonging" to an association here is a naming and hierarchy convention, not a database-level constraint. If the
many-to-many case matters, the practical options are either to publish the same reading under more than one
topic (accepting some duplication) or to hand-author the association/tag layer as explicit policies — the
approach in <a href="./05-2%20UNS%20Custom%20Examples.md" target="_blank">Custom UNS (data stream, ISA-95)</a> — while still using `dynamic=true` for the raw
sensor stream underneath it. That's a hybrid: a manually curated, meaningful structure at the levels the customer
actually browses, with fully automated ingestion still doing the work at the leaves.

---

## See also

- <a href="./05-%20Unitfied%20Namespace.md" target="_blank">Unified Namespace</a> — the base `dynamic=true` model (scalar values, MQTT/OPC-UA)
- <a href="./05-2%20UNS%20Custom%20Examples.md" target="_blank">Custom UNS (data stream, ISA-95)</a> — the fully hand-authored, policy-based approach