---
title: "Nodes"
description: "AnyLog's node types (Master, Query, Operator, Publisher), Operator and Publisher configuration, high availability via data distributor/consumer, and data buffering."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-26 | Ori Shadmon | Added frontmatter/title; fixed `start_data`/`start_date` mismatch and reversed description; fixed invalid JSON (`True`/`False` → `true`/`false`); fixed empty cluster-policy link; removed stray angle brackets from code blocks; promoted Publisher to its own section | |
--->

# Nodes

AnyLog contains 4 major types of nodes:

* **Master or Metadata Manager** - responsible for maintaining a copy of the blockchain as an alternative to having an
actual blockchain.
* **Query** - Node dedicated to allow third-party applications to communicate with the network via REST; with a focus on
aggregating results from multiple operator nodes.
* **Operator** - Node dedicated to maintain a copy of the sensor and or devices data
* **Publisher** - A node that usually sits closer to the device and is able to distribute data across different operator
nodes seamlessly.

A detailed explanation of the (minimal) commands needed to run each type of AnyLog agent can be found under
<a href="../03-%20Training%20&%20Tutorials/06-%20Nodes.md" target="_blank">section 3 - Nodes</a>.

---

## Operator Services

The Operator monitors the watch directory, identifies or creates schemas, and ingests data into local databases.
An Operator must be associated with an <a href="{{ '/docs/Network-Services/policies-metadata/#operator-policy' | relative_url }}">Operator policy</a>
and a <a href="{{ '/docs/Network-Services/policies-metadata/#cluster-policy' | relative_url }}">Cluster policy</a>
published to the metadata layer.

### Cluster / Operator Relationship

A Cluster policy is a logical object within the metadata layer that's able to define a group of operators as a single unit.
In addition, it will contain sub or child policies (also named "cluster") that contain the logical database and tables shared
among the operator nodes.

From a technical point of view, the logic is that 1 cluster may have multiple operators, but an operator is only associated
to a single cluster.

**Sample Policies**: The following example shows a subset of a network, regarding smart cities, that has 2 operators
residing on the same cluster, sharing 2 tables defined on the cluster's child policies.
```json
{"cluster" : {"company" : "Smart City",
               "name" : "power-plant",
               "status" : "active",
               "id" : "2a5f83e1f2e63c16bbf5339988bf7489",
               "date" : "2026-07-19T19:35:01.842665Z",
               "ledger" : "global"}},
{"operator" : {"name" : "power-plant-operator1",
                "company" : "Smart City",
                "hostname" : "smart-city-operator2",
                "ip" : "172.105.6.90",
                "port" : 32148,
                "rest_port" : 32149,
                "broker_port" : 32150,
                "cluster" : "2a5f83e1f2e63c16bbf5339988bf7489",
                "main" : true,
                "loc" : "39.8958, 95.9922",
                "country" : "US",
                "state" : "KS",
                "city" : "Sabetha",
                "id" : "3d986f80eb86cf4b1529dd297e1e605f",
                "date" : "2026-07-19T19:35:06.927901Z",
                "member" : 157,
                "ledger" : "global"}},
 {"operator" : {"name" : "power-plant-operator1-bkup1-bkup",
                "company" : "Smart City",
                "hostname" : "smart-city-operator2-bkup1",
                "ip" : "172.105.13.202",
                "port" : 32148,
                "rest_port" : 32149,
                "broker_port" : 32150,
                "cluster" : "2a5f83e1f2e63c16bbf5339988bf7489",
                "main" : false,
                "loc" : "43.7064,-79.3986",
                "country" : "CA",
                "state" : "Ontario",
                "city" : "Toronto",
                "id" : "1811ee3672c201513644b7a43fb61bc9",
                "date" : "2026-07-19T19:56:21.702979Z",
                "member" : 165,
                "ledger" : "global"}},
{"cluster" : {"parent" : "2a5f83e1f2e63c16bbf5339988bf7489",
               "name" : "power-plant",
               "company" : "Smart City",
               "table" : [{"dbms" : "cos",
                           "name" : "pp_pm",
                           "status" : "active"}],
               "source" : "Node at 172.105.6.90:32148",
               "id" : "b1245decc1f1cf8def7bc599ee3e6f41",
               "date" : "2026-07-19T19:35:08.507752Z",
               "status" : "active",
               "ledger" : "global"}},
 {"cluster" : {"parent" : "2a5f83e1f2e63c16bbf5339988bf7489",
               "name" : "power-plant",
               "company" : "Smart City",
               "table" : [{"dbms" : "cos",
                           "name" : "pv",
                           "status" : "active"}],
               "source" : "Node at 172.105.6.90:32148",
               "id" : "aa3e66600da1daf0b8579e5175d33916",
               "date" : "2026-07-19T19:35:38.729163Z",
               "status" : "active",
               "ledger" : "global"}}
```

> **Note:** Both operator policies above use the hostname prefix `smart-city-operator2` even though the first is named
> `power-plant-operator1`. This looks like a copy-paste artifact in the sample data rather than intentional — worth
> confirming/correcting the hostnames before this ships.

### `run operator` command

Unlike other AnyLog agents, an operator node **must** be represented by a self-defined node policy associated with the
cluster, in order to leverage the blockchain both as a record of the data (specifically, tables associated with the
cluster) and as metadata (the table's `CREATE` statement).

```anylog
run operator where [option] = [value] and ...
```

| Option | Description | Default |
|---|---|---|
| `policy` | ID of the Operator policy | |
| `create_table` | Auto-create tables if they don't exist | `true` |
| `update_tsd_info` | Update the `tsd_info` summary table (used for HA sync) | |
| `archive_json` | Archive JSON files after processing | `true` |
| `archive_sql` | Archive SQL files after processing | `false` |
| `compress_json` | Compress JSON files after processing | `true` |
| `compress_sql` | Compress SQL files after processing | `true` |
| `limit_tables` | Comma-separated list of table names to process | |
| `master_node` | IP:Port of the master node | |
| `distributor` | Enable HA data distribution to peer Operators | |
| `threads` | Worker thread count | |

**Example**:
```anylog
<run operator where
    create_table = true and
    update_tsd_info = true and
    archive_json = true and
    distributor = true and
    master_node = !master_node and
    policy = !operator_policy and
    threads = 3>
```

> **Note:** The Operator and Publisher services cannot run on the same node. A node acts as either an Operator
> (stores data) or a Publisher (routes data to Operators), not both.

### High Availability & Data Consumer

The utilization of <a href="{{ '/docs/Network-Services/policies-metadata/#cluster-policy' | relative_url }}">cluster policies</a> allows for both high availability and data resilience up to the point of the last automated
(hot) backup.
That means when a user adds secondary operator nodes to the cluster, the agent is smart enough to automatically forward the
data to other members of the network, allowing for an active backup or data resilience even when the edge, or primary,
operator node goes down.
Similarly, the Query node is intelligent enough to know that the primary is down, and on a second attempt of querying data
will automatically try a different operator associated with the cluster, thus creating the idea of high availability.

To accomplish this we have 2 main commands:

1. `run data distributor` - allows the operator to distribute its data to other operators that reside under the same cluster
```anylog
<run data distributor where
    cluster_id = 87bd559697640dad9bdd4c356a4f7421 and
    distr_dir = !distr_dir>
```

2. `run data consumer` - allows the operator to consume (pull in) data from other operators that reside under the same cluster, to fill in anything missing locally
```anylog
run data consumer where start_date=-30d and mode=active
```

| Param | Description | Input |
|:---:|---|:---:|
| `start_date` | How far back to look for missing data to pull in from peer operators in the cluster | A specific date `YY-MM-DD HH:MM:SS`, or number of days back (e.g. `-30d`) |
| `end_date` | (optional) Limits the range of time (i.e. between start and end date) for the data being pulled in | |
| `mode` | Whether to enable / disable HA | `active` or `suspend` |

### Operator Monitoring

* Get data flowing in:
```anylog
get streaming
```

* View data specifically processed by `run operator`:
```anylog
get operator
get operator inserts
get operator summary
get operator config
get operator summary where format = json
```

* View data consumption:
```anylog
get consumer
```

* Validate cluster data - Compare the TSD tables of the nodes supporting the cluster:
```anylog
test cluster data
```

## Publisher Service

The Publisher monitors the watch directory and distributes data files to the appropriate Operator nodes based on
metadata policies. It does not store data locally.

> **Note:** The Publisher and Operator services cannot run on the same node. A node acts as either a Publisher
> (routes data) or an Operator (stores data), not both.

```anylog
run publisher where [option] = [value] and ...
```

| Option | Description | Default |
|---|---|---|
| `watch_dir` | Directory monitored for new files | `!watch_dir` |
| `bkup_dir` | Directory for successfully processed files | `!bkup_dir` |
| `error_dir` | Directory for files that failed processing | `!error_dir` |
| `delete_json` | Delete JSON file after successful processing | `false` |
| `delete_sql` | Delete SQL file after successful processing | `false` |
| `compress_json` | Compress JSON file after processing | `false` |
| `compress_sql` | Compress SQL file after processing | `false` |
| `company` | Company name associated with the data | Derived from database name |
| `master_node` | IP:Port of the master node | |

Examples:
```anylog
run publisher where delete_json = true and delete_sql = true

run publisher where company = anylog and delete_json = true and delete_sql = true
```

**Monitor the Publisher**:
```anylog
get publisher
```

## Data Buffering

In order to better manage data flow, AnyLog has built-in buffering logic that helps combine data intended for the
same logical database/table into a single packet for insertion. This logic is used with both **operator** and
**publisher** nodes.

* `set buffer threshold` - Configure time and volume thresholds for buffered streaming data. The condition can be just
a buffer threshold size (in terms of time and/or volume), or scoped to a specific database (and table).

```anylog
<set buffer threshold where
    dbms = al_demo and
    table = ping_sensor and
    time = 2 minutes and volume = 1MB>
```

* `run streamer` - Writes streaming data to files

```anylog
run streamer where prep_dir = !prep_dir and watch_dir = !watch_dir and err_dir = !err_dir
```

If directories are not specified, the default paths from the AnyLog dictionary are used (`get dictionary` to view them).

* `get streaming` - Monitor streaming buffer status

```anylog
get streaming
```

> Notice: these steps are built into the default configuration policies being automatically executed at start up.