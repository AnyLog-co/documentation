---
title: Troubleshooting
description: Commands to validate node accessibility, active services, network connectivity, and blockchain consistency.
layout: page
---
<!--
## Changelog
- 2026-04-25 | Created document
--> 

Use these commands from the AnyLog CLI or via REST to diagnose connectivity and confirm your node and network are 
operating correctly.

| Step | Command | Confirms |
|---|---|---|
| 1 | `get processes` | Services are running |
| 2 | `test node` | Local TCP/REST accessibility |
| 3 | `test network` | Peer connectivity |
| 4 | `blockchain test` | Local blockchain is intact |
| 5 | `get metadata version` | Metadata is in sync with peers |
| 6 | `test cluster` | Cluster config — operator nodes only |

---

## `get processes`

Shows which AnyLog services are currently running on the node. This is the quickest first check — run it any time a node 
is misbehaving or a service is suspected to be down.

```anylog
get processes
```

Services are listed with their status. Any service shown as `Not declared` or absent is not running. 
Common services to verify:

```
Process         Status        Details
----------------|-------------|--------------------------------------------------------------------
TCP             | Running     | Listening on: 10.0.1.5:32148, Threads Pool: 6
REST            | Running     | Listening on: 10.0.1.5:32149, Threads Pool: 6, Timeout: 20, SSL: False
MCP             | Not declared|
Operator        | Running     | Cluster Member: True, Using Master: 10.0.0.1:32048, Threads Pool: 3
Blockchain Sync | Running     | Sync every 120 seconds with master using: 10.0.0.1:32048
Scheduler       | Running     | Schedulers IDs in use: [0 (system)] [1 (user)]
Blobs Archiver  | Running     | Flags: dbms = False, folder = True, compress = True, reuse_blobs = True
MQTT            | Running     |
MSG Client Pool | Not declared|
MSG Broker      | Running     | Listening on: 10.0.1.5:32150, Threads Pool: 6
SMTP            | Not declared|
Streamer        | Running     | Default streaming thresholds are 60 seconds and 10,240 bytes
UNS Streamer    | Not declared|
Query Pool      | Running     | Threads Pool: 3
Kafka Consumer  | Not declared|
gRPC            | Not declared|
PLC Client      | Not declared|
Pull Processes  | Not declared|
Video Processes | Not declared|
Publisher       | Not declared|
Distributor     | Not declared|
Consumer        | Not declared|
```

---

## `test node`

Validates that the node is self-accessible — checks that the TCP service, REST service, and local blockchain 
copy are all reachable and consistent.

```anylog
test node
```

A passing result confirms:
- TCP port is bound and accepting connections
- REST port is bound and responding
- Local blockchain file is readable and valid

Run this first when a node appears unreachable from the network — if `test node` fails, the issue is local to the node 
itself rather than a network path problem.

```
Test TCP
[************************************************************]

Test REST
[************************************************************]

Test                                        Status
--------------------------------------------|----------------------------------------------------
Metadata Version                            | a3f9c2e1d84b7a6f2c1e0d95b83a417
Metadata Test                               | Pass
TCP test using 10.0.1.5:32148               | [From Node 10.0.1.5:32148] NODE-01@10.0.1.5:32148 running
REST test using http://10.0.1.5:32149       | NODE-01@10.0.1.5:32148 running
```

---

## `test network`

Validates that the node can communicate with the rest of the network — sends a test message to all peer nodes and 
reports which ones respond.

```anylog
test network
```

A failure here (while `test node` passes) points to a network path issue between nodes rather than a local 
configuration problem.

**Common causes of `test network` failure:**

- Nodes on the same DNS network — bind IP addresses to shared local IPs rather than the external router-assigned IP
- Nodes on different DNS networks — confirm that AnyLog ports are accessible externally; this can be a machine-level firewall issue or a DNS/modem port-forwarding issue

Expected output — a `+` means the node replied; no `+` means it failed to respond:

```
Address               Node Type  Node Name                    Status
----------------------|----------|----------------------------|------
10.0.0.1:32048        | master   | anylog-master               |  +
10.0.1.1:32148        | operator | wind-turbine1               |  +
10.0.1.2:32148        | operator | wind-turbine2               |  +
10.0.1.3:32148        | operator | wind-turbine3               |  +
10.0.1.4:32148        | operator | wind-turbine5               |  +
10.0.2.1:32148        | operator | water-plant-operator1       |  +
10.0.2.2:32148        | operator | power-plant-operator1       |  +
10.0.2.3:32148        | operator | waste-water-plant-operator1 |  +
10.0.2.4:32148        | operator | water-plant-operator1-bkup1 |  +
10.0.2.5:32148        | operator | power-plant-operator1-bkup1 |  +
10.0.3.1:32348        | query    | anylog-ucsc-query           |      ← no + means failed to return a reply
10.0.3.2:32348        | query    | anylog-remote-query         |  +
10.0.1.6:32148        | operator | RIG-TX-001                  |  +
10.0.1.7:32148        | operator | RIG-TX-007                  |  +
10.0.1.8:32148        | operator | RIG-GOM-023                 |  +
10.0.3.3:32348        | query    | mark-query                  |  +
10.0.3.4:32348        | query    | bachelor-query              |  +
10.0.1.5:32148        | operator | RIG-ND-012                  |  +
10.0.1.9:32148        | operator | vessel-operator-dlt         |  +
```

> During `test network` you may see blockchain sync warnings such as `Policy #NNNN is not recognized` or
> `Terminating blockchain sync process — unrecognized file format`. These indicate a blockchain consistency issue
> between nodes — proceed to the [blockchain validation](#blockchain-validation) steps below.

If no error appears on screen, check the error log:

```anylog
get error log
```

Once the issue is resolved, clear the log to confirm no new errors appear:

```anylog
reset error log
```

---

## Blockchain validation

The blockchain is AnyLog's metadata layer — it holds node policies, cluster assignments, and network topology. If nodes 
can reach each other (TCP/REST pass) but queries fail or nodes aren't routing data correctly, a blockchain mismatch is 
the likely cause.

### `blockchain test`

**When:** `test network` passes but nodes still aren't finding each other or routing queries correctly.

**Why:** Confirms the local copy of the blockchain file is intact. A corrupted or missing local copy means the node has 
no metadata to work from.

```anylog
blockchain test
```

### `get metadata version`

**When:** Nodes are communicating but behaving inconsistently — one node sees a policy another doesn't.

**Why:** Every node should be running the same metadata version. A mismatch means one or more nodes have a stale local 
copy and need to re-sync from the master.

```anylog
get metadata version
```

Run on the problem node, then on the master or a known-good node and compare the returned ID — they must match.

```anylog
run client (IP:Port) get metadata version
```

### `test cluster`

**When:** Operator nodes are running and network connectivity is confirmed, but data is not being shared or replicated
within the cluster.

**Why:** `test cluster` alone is a top-level check — use the subcommands below to isolate exactly where the cluster
divergence is. A node can be reachable on the network but still misconfigured at the cluster level — wrong cluster ID,
missing operator assignment, database/partition mismatch, or stale policy that hasn't synced.

Run all four on each operator node in the cluster, in order:

#### `test cluster setup`

Validates the node's configuration supports HA — confirms the operator is correctly assigned to a cluster and
the local setup is consistent with what the blockchain policy describes.

```anylog
test cluster setup
```

Start here. If this fails, the remaining tests are not meaningful — fix the configuration first.

#### `test cluster databases`

Compares the databases defined on each member of the cluster — all operators in the same cluster should have
the same logical databases.

```anylog
test cluster databases
```

A mismatch here means one or more operators are missing a database that peers have, or have an extra one.

#### `test cluster partitions`

Compares the partition scheme defined on each member — operators in the same cluster must partition data
identically or queries will return inconsistent results.

```anylog
test cluster partitions
```

#### `test cluster data`

Compares the actual TSD (time-series data) tables across cluster members to confirm data is being replicated
consistently. Optionally scope to a recent window:

```anylog
test cluster data
test cluster data where start_date = -7d
```

A divergence here (after setup, databases, and partitions all pass) means replication is failing at the data
level — check the Operator and Streamer services are running on all members (`get processes`) and that the
cluster policy on the blockchain is consistent across nodes.