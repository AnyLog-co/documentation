---
title: Custom UNS (data stream, ISA-95)
description: Example of hand-authored UNS policies for a data_stream_isa95 hierarchy with ISA-95 metadata, inserts, and blockchain queries
layout: page
---

<!--
## Changelog
- 2026-04-22 | Initial UNS_custom example (data_stream_isa95 root, stream1, d1/d2 devices)
-->

This page records an end-to-end pattern: define **`uns`** policy dictionaries, insert them on the blockchain with **`blockchain insert`**, then verify with **`blockchain get uns`**. Parent IDs from earlier inserts are reused for child policies.

For the broader UNS model (including auto-generated MQTT with **`dynamic=true`**), see <a href="{{ '/docs/Managing-Data-Southbound/UNS/' | relative_url }}">Unified Namespace</a>.

---

## Root (enterprise tier)

```anylog
<uns_data_stream_isa95_root = {"uns": {
    "name": "data_stream_isa95",
    "namespace": "data_stream_isa95",
    "company": "MyCompany",
    "description": "ISA-95 data stream root (enterprise tier).",
    "uns_level": "enterprise",
    "isa95": {
        "level": "L4",
        "entity": "Enterprise",
        "standard": "ISA-95"
    }
}}>
```

```anylog
blockchain insert where policy = !uns_data_stream_isa95_root and local = true and master = !ledger_conn
```

```anylog
blockchain get uns where name = data_stream_isa95
```

```json
[{"uns" : {"name" : "data_stream_isa95",
           "namespace" : "data_stream_isa95",
           "company" : "MyCompany",
           "description" : "ISA-95 data stream root (enterprise tier).",
           "uns_level" : "enterprise",
           "isa95" : {"level" : "L4",
                      "entity" : "Enterprise",
                      "standard" : "ISA-95"},
           "id" : "70f1b1a895f1d71b37ba12166514dc9d",
           "date" : "2026-04-21T11:59:15.688934Z"}}]
```

**Intermediate:** use **`parent = 70f1b1a895f1d71b37ba12166514dc9d`** for the next level.

---

## `stream1` (site / stream branch, L3)

```anylog
<uns_data_stream_isa95_stream1 = {"uns": {
    "name": "stream1",
    "namespace": "data_stream_isa95/stream1",
    "parent": "70f1b1a895f1d71b37ba12166514dc9d",
    "company": "MyCompany",
    "description": "Site / stream branch (L3) under data_stream_isa95.",
    "uns_level": "factory",
    "isa95": {
        "level": "L3",
        "entity": "Site",
        "standard": "ISA-95"
    }
}}>
```

```anylog
blockchain insert where policy = !uns_data_stream_isa95_stream1 and local = true and master = !ledger_conn
```

```anylog
AL op1 +> blockchain get uns where name = stream1
```

```json
[{"uns" : {"name" : "stream1",
           "namespace" : "data_stream_isa95/stream1",
           "parent" : "70f1b1a895f1d71b37ba12166514dc9d",
           "company" : "MyCompany",
           "description" : "Site / stream branch (L3) under data_stream_isa95.",
           "uns_level" : "factory",
           "isa95" : {"level" : "L3",
                      "entity" : "Site",
                      "standard" : "ISA-95"},
           "id" : "f31ef430f33d406658f2d241e2d065fb",
           "date" : "2026-04-21T12:02:13.498713Z"}}]
```

**D1 / D2:** use **`parent = f31ef430f33d406658f2d241e2d065fb`** for device-level nodes under **`stream1`**.

---

## `d1` (device stream, L1)

```anylog
<uns_data_stream_isa95_d1 = {"uns": {
    "name": "d1",
    "namespace": "data_stream_isa95/stream1/d1",
    "parent": "f31ef430f33d406658f2d241e2d065fb",
    "company": "MyCompany",
    "description": "Device stream d1 (L1); table data_stream_isa95_d1.",
    "uns_level": "device",
    "isa95": {
        "level": "L1",
        "entity": "Work Unit",
        "standard": "ISA-95"
    },
    "dbms": "new_company",
    "table": "data_stream_isa95_d1"
}}>
```

```anylog
blockchain insert where policy = !uns_data_stream_isa95_d1 and local = true and master = !ledger_conn
```

---

## `d2` (device stream, L1)

```anylog
<uns_data_stream_isa95_d2 = {"uns": {
    "name": "d2",
    "namespace": "data_stream_isa95/stream1/d2",
    "parent": "f31ef430f33d406658f2d241e2d065fb",
    "company": "MyCompany",
    "description": "Device stream d2 (L1); table data_stream_isa95_d2.",
    "uns_level": "device",
    "isa95": {
        "level": "L1",
        "entity": "Work Unit",
        "standard": "ISA-95"
    },
    "dbms": "new_company",
    "table": "data_stream_isa95_d2"
}}>
```

```anylog
blockchain insert where policy = !uns_data_stream_isa95_d2 and local = true and master = !ledger_conn
```
