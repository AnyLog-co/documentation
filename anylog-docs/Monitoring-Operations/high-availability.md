---
title: High Availability (HA)
description: Configure multiple operator nodes to maintain copies of data so queries survive individual node failures.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

> **AnyLog only.** High Availability is not available in EdgeLake.

HA is achieved by assigning multiple Operator nodes to the same **cluster**. Each operator in a cluster maintains an identical copy of the cluster's data. If one operator fails, surviving operators continue to serve queries without interruption.

---

## How it works

### Data organisation

- Data is stored in **tables** within logical **databases**
- Each table's data is partitioned into one or more **clusters**
- Each cluster is supported by multiple **Operators**, all holding identical data
- The number of operators per cluster = number of copies of that data

### Example layout

```
Database
└── Tables 1–4
    ├── Cluster 1 ──► Operator 1
    │              ──► Operator 2
    │              ──► Operator 3
    └── Cluster 2 ──► Operator 4
                   ──► Operator 5
                   ──► Operator 6
```

### Data replication flow

When an operator receives data, it stores it locally and **pushes** it to all peer operators in the same cluster. Each operator also continuously **pulls** any data it is missing from its peers. This push/pull sync keeps all cluster members in sync automatically.

---

## Prerequisites

1. Operator nodes deployed and running
2. A **Cluster policy** for each cluster
3. An **Operator policy** for each operator, referencing its cluster ID
4. Three background services enabled on each operator:
   - `run operator` — ingests data to the local database
   - `run data distributor` — pushes new data to peer operators
   - `run data consumer` — pulls missing data from peers
5. TSD tables created (see [TSD tables](#tsd-management-tables) below)

> At least 2 operators must be assigned to each cluster for HA.

---

## Cluster policy

```json
{"cluster": {
  "company": "Lit San Leandro",
  "name": "lsl-cluster2",
  "status": "active"
}}
```

When published, the network adds a unique `id` and `date`:

```json
{"cluster": {
  "company": "Lit San Leandro",
  "name": "lsl-cluster2",
  "status": "active",
  "id": "7a00b26006a6ab7b8af4c400a5c47f2a",
  "date": "2022-12-23T01:48:33Z",
  "ledger": "global"
}}
```

---

## Operator policy

Operators are assigned to a cluster via the `cluster` key (the cluster policy ID):

```json
{"operator": {
  "cluster": "7a00b26006a6ab7b8af4c400a5c47f2a",
  "ip": "24.23.250.144",
  "local_ip": "10.0.0.78",
  "port": 7848,
  "member": 145
}}
```

---

## Configuring an operator node for HA

```anylog
run operator where policy = [operator-policy-id] and create_table = true and update_tsd_info = true and archive = true and distributor = true and master_node = !master_node
run data distributor
run data consumer where start_date = -30d
```

With this configuration, each operator that receives data shares it with all peers, and continuously syncs with peers to fill any gaps.

---

## Monitoring and diagnostics

### Validate HA setup on this node

```anylog
test cluster setup
```

Returns the expected status for each HA component:

| Check | Expected |
|---|---|
| Operator | Running with `distributor = true` |
| Distributor | Running |
| Consumer | Running |
| Cluster ID | Valid |
| Member ID | Valid |
| `almgm.tsd_info` | Table defined |

### View data distribution

```anylog
# Table format
get data nodes
get data nodes where table = ping_sensor
get data nodes where sort = (1,2)

# Detailed format with cluster membership
blockchain query metadata
```

### View cluster membership on this operator

```anylog
get cluster info
```

### Test cluster health

```anylog
blockchain test cluster           # Validate cluster policy structure
test cluster databases            # Compare databases defined across cluster members
test cluster data                 # Compare row/file counts across cluster members
test cluster data where start_date = -7d
```

### HA command reference

| Command | Description |
|---|---|
| `get data nodes` | Tables and the physical nodes managing each |
| `get metadata version` | Metadata version ID on this node |
| `blockchain query metadata` | Same as `get data nodes`, different format |
| `blockchain test cluster` | Validate cluster policy structure |
| `get tsd list` | List TSD tables on this node |
| `get tsd details` | Query TSD table entries |
| `get tsd summary` | Summary of TSD tables |
| `get tsd errors` | TSD entries with ingestion errors |
| `get tsd sync status` | Sync status with peer members |
| `test cluster setup` | HA configuration check for this node |
| `test cluster data` | Row/file sync status across cluster members |
| `test network metadata` | Metadata version on each participating node |

---

## TSD management tables

TSD (Time Series Data) tables track the sync state between cluster members:

- `tsd_info` — data received directly from data sources
- `tsd_[member_id]` — data received from a specific peer member

Create the info table:
```anylog
create table tsd_info where dbms = almgm
```

### Query TSD tables

```anylog
# List all TSD tables on this node
get tsd list

# Details (last 100 entries by default)
get tsd details
get tsd details where table = *
get tsd details where start_date = -3d and end_date = -2d

# Summary
get tsd summary
get tsd summary where table = *
get tsd summary where start_date = -3d

# Errors only
get tsd errors

# Sync status
get tsd sync status
get tsd sync status where table = tsd_128
```

### Drop and manage TSD tables

```anylog
drop table tsd_info where dbms = almgm
time file drop tsd_123
time file drop all

# Delete a single row
time file delete 16 from tsd_info
```

---

## Adding operators to a cluster

New operators can be added to a running cluster at any time — to replace a failed node or increase redundancy. The new operator automatically syncs with existing cluster members to build a complete local copy of the data.

Steps:
1. Deploy and configure the new operator node
2. Publish an operator policy associating it with the target cluster ID
3. Start `run operator`, `run data distributor`, and `run data consumer`

The consumer process handles the initial data sync automatically.

---

## Query behaviour in HA mode

Queries are routed to an active operator in the relevant cluster. If an operator fails to respond, it is flagged as non-active and excluded from future query routing automatically.

Monitor in-flight queries:
```anylog
query status
```

Query options relevant to HA:

| Option | Default | Description |
|---|---|---|
| `nodes` | `main` | `main`: query designated main operators only; `all`: round-robin across all operators |
| `committed` | `false` | `true`: only return data confirmed synced across cluster nodes |