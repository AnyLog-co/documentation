---
title: Modbus TCP
description: Pull coils, discrete inputs, and holding/input registers from Modbus TCP devices into AnyLog using run plc client.
layout: page
---
<!--
## Changelog
- 2026-05-08 | Created document
-->

AnyLog can act as a **Modbus TCP client** (over **hostname** and **port**, typically port **502**). Data is read on a schedule and streamed into your local operator database as JSON, using the same **`run plc client`** pattern as [OPC-UA](/docs/managing-data-southbound/opcua/) and [EtherNet/IP](/docs/managing-data-southbound/etherip/).

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **`pymodbus`** | Must be installed in the AnyLog runtime environment. |

Declare the target DBMS before streaming, for example:

```anylog
connect dbms new_company where type = sqlite
```

---

## Connection and map

Modbus uses **`hostname`** and **`port`** (not `url`). **`device_id`** is the **Modbus PDU unit id** (often `0` or `1` on TCP). **`map`** is a **JSON array** of points; each object must include a **`name`** (column / logical label) and exactly one address field:

| Key | Meaning |
|---|---|
| `coil` | Coil (0-based address) |
| `input` | Discrete input |
| `inputRegister` | Input register (single address or list for blocks) |
| `register` | Holding register (single address or list for blocks) |

**`topic`** is **not** supported on Modbus `run plc client` commands.

---

## One-shot read

```anylog
<get plc values where type = modbus and
    hostname = 192.168.1.72 and
    port = 1502 and
    device_id = 1 and
    map = [{"name":"sensor_1","register":0}]
>
```

Alias: **`get modbus values`** (same keywords).

---

## Continuous ingest — wide table (default)

With **`table = ...`** and **`dbms`**, all points from **`map`** land in **one table**. Each poll inserts **one row**; every object in **`map`** is **one column**: the map **`name`** is the **column name**, and that column stores the **value** read for that point.

```anylog
<run plc client where type = modbus and
    hostname = 192.168.1.72 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = my_mb and
    dbms = new_company and
    table = sensors and
    map = [{"name":"temperature","register":0}]
>
```

---

## Continuous ingest — dynamic tables (`dynamic = true`)

Omit **`table`** and omit **`namespace`** for plain dynamic ingest. Each object in **`map`** is written to its **own table**. The table name is derived from the client **`name`** and the map **`name`** (for example, **`fdev10_outside_temperature`** when **`name = fdev10`** and the map entry’s **`name`** is **`outside_temperature`**). Each row includes **`timestamp`**, **`tag`**, and **`value`**.

```anylog
<run plc client where type = modbus and
    hostname = 192.168.1.72 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = fdev10 and
    dbms = new_company and
    dynamic = true and
    map = [{"name":"outside_temperature","inputRegister":1}]
>
```

---

## Dynamic ingest with UNS (`namespace` + `master_node`)

With **`dynamic = true`**, you can add a **Unified Namespace** path and a **master node** so Modbus ingest is registered in the UNS alongside your policies and DBMS. **`namespace`** requires **`master_node = [ip:port]`** for policy updates.

Example (abbreviated):

```anylog
run plc client where type = modbus and
    hostname = 192.168.1.72 and
    port = 1502 and
    device_id = 1 and
    frequency = 5 and
    name = fdev11 and
    dbms = new_company and
    dynamic = true and
    master_node = 192.168.1.88:32048 and
    namespace = FA9/MID9/DEVICE9 and
    map = [{"name":"desk_lamp","coil":0}]
```

**Table names** follow the **same pattern** as plain **`dynamic = true`** (client **`name`** plus map **`name`**, e.g. **`fdev11_desk_lamp`** for the example above). Under UNS, the **read value** is usually stored in a **column named like the tag**—the map **`name`** (here **`desk_lamp`**), not a generic **`value`** column.

With **`namespace`**, table and column layout follow **UNS policies**. **`namespace`** and **`master_node`** drive how tables are registered in the UNS. See [Unified Namespace](/docs/managing-data-southbound/UNS/) for background.

---

## Command keywords (summary)

| Keyword | Required / notes |
|---|---|
| `type` | `modbus` |
| `hostname`, `port` | Modbus TCP target |
| `device_id` | PDU unit id |
| `frequency` | Poll interval |
| `name` | Unique client name |
| `dbms` | Target DBMS |
| `table` | Wide-table ingest; omit with **`dynamic = true`** |
| `dynamic` | `true` for per-map tables or UNS |
| `map` | JSON array of points |
| `namespace` | UNS path (Modbus + **`dynamic = true`** only) |
| `master_node` | Required when **`namespace`** is set |

---

## Related

- [Data Ingestion (Southbound)](/docs/managing-data-southbound/southbound-overview/)
- [Unified Namespace](/docs/managing-data-southbound/UNS/)
- [OPC-UA](/docs/managing-data-southbound/opcua/)
- [EtherNet/IP](/docs/managing-data-southbound/etherip/)
