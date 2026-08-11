---
title: Introduction to AnyLog
description: Introduction to AnyLog and the Edge Data Fabric — what it is, core terminology, node types, and high-level architecture.
layout: page
---
<!--
## Changelog
-
- 2026-08-07 | Eric Aquaronne | change log format adding ref version | 2.0.2606 
2026-04-17 | Created document (legacy)
- 2026-04-25 | hyperlink fix (legacy)
- 2026-07-02 | Unified from: 01- Getting Started/Getting Started.md,
                             ORPHANS/x anylog-docs/Getting-Started/getting-started.md,
                             ORPHANS/x edgelake-docs/getting_started.md
- 2026-07-22 | Rescoped from the unified "Getting Started" merge into a pure conceptual intro page.
               Removed: CLI operations, node dictionary, local directory structure, install pointers,
               blockchain/REST commands, HA, and network security — these belong in their own target
               docs (install.md / full-deployment.md / a CLI or core-concepts reference), not here.
               Renamed "Master Node" to "Metadata Manager" throughout, per clarified terminology.
               Replaced the separate "How Data is Collected" / "How Querying Works" reference tables
               with a single conceptual data-lifecycle walkthrough (PLC → southbound → table → insert →
               query), per the outline. A deeper, protocol-by-protocol version belongs under
               12- Examples & Use Cases/, not here.
               Open item carried over from the prior merge, still unresolved: whether `01- Getting
               Started/01 Getting Started.md` (the numbered duplicate) is now fully superseded by this
               file or still holds content that needs reconciling — not confirmed.
-->

Welcome to AnyLog! This guide introduces the platform's architecture, terminology, node types, and the
lifecycle of data as it moves through the network.

## What is AnyLog?

**AnyLog** is a **decentralized** network for managing **IoT and time-series data**: rather than centralizing data in
the cloud, it stays at the edge, close to where it's generated. Across that edge footprint, data is also
**distributed** — spread across many Operator nodes, each holding its own localized data lake — and coordinated
through shared metadata and protocols.

Every node runs the same AnyLog software, though which services are active differs by node type (see
[Node Types](#node-types) below). Queries travel **peer-to-peer**: a query sent by a user goes directly to the
relevant Operator node(s), and results come directly back — there's no central broker or hop in between routing the
traffic.

The architecture consists of two complementary layers:
* **Physical layer** — the Operator nodes where data actually resides, both as structured tables and as the original
  raw files.
* **Virtual layer** — the Edge Data Fabric (EDF) connecting those nodes, providing unified, single-point access to
  data that's physically spread across all of them.

Together, these layers create a cloud-like architecture for distributed edge and IoT data — enabling real-time access
without moving data and without locking organizations into a specific cloud, application, or hardware vendor.

## What is Edge Data Fabric (EDF)?

AnyLog is built around keeping data at the edge — in localized data lakes close to where it's generated — while still
letting users query across all of them from a single point. The Edge Data Fabric (EDF) is what makes this possible: the
distributed layer that connects those data lakes together without centralizing the actual data. Rather than moving
operational information to one place before it can be analyzed, EDF shares metadata instead — a lightweight index of
what data exists and where it lives.

In practical terms, this metadata layer tells query nodes where to find the data they need and tells publisher nodes
where to store it. Every node stays autonomous and keeps ownership of its own data, but because they all share the same
metadata, the whole network behaves like one logical system to anyone querying it.

## EdgeLake vs AnyLog

<a href="https://github.com/EdgeLake/EdgeLake" target="_blank">EdgeLake</a> is the **open-source, free** version of AnyLog,
distributed by the Linux Foundation. It provides a managed, zero-maintenance experience — most, but not all, of AnyLog's
functionality — and is ideal for teams that want the benefits of edge computing and decentralized data control without
managing infrastructure.

**EdgeLake offers:**
* Turnkey node deployment at the edge or in the cloud
* Zero-maintenance operation (automatic updates, monitoring, configuration)
* Scalable pricing — starting at **$1 per device/month**
* Real-time SQL and REST API access from any node
* Built-in dashboards and analytics

| Feature                                    | EdgeLake           | AnyLog       |
|--------------------------------------------|--------------------|--------------|
| Cost                                       | Free / Open-Source | Subscription |
| Virtual edge layer                         | ✅                  | ✅            |
| Rule engine                                | ✅                  | ✅            |
| Policy-based data management               | ✅                  | ✅            |
| Node management                            | ✅                  | ✅            |
| Unified APIs, CLIs, Admin UI               | ✅                  | ✅            |
| Supported IoT connectors                   | ✅                  | ✅            |
| Blockchain abstraction                     | ✅                  | ✅            |
| MCP Integration                            | limited            | ✅            |
| Aggregations                               | ❌                  | ✅            |
| Automated Unified Namespace (UNS)          | ❌                  | ✅            |
| Security protocol & High Availability (HA) | ❌                  | ✅            |
| Publisher node role                        | ❌                  | ✅            |

**AnyLog (Enterprise)** includes everything in EdgeLake plus: advanced security and authentication, federated data
aggregation and model training, and real-time support with SLA options.

## Terminology

| Term               | Definition                                                                                                                                                                                                                                                                                                 |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Southbound**     | Data flowing *in* from devices and sensors, stored into AnyLog/EDF                                                                                                                                                                                                                                         |
| **Northbound**     | Queries and results flowing *out* to applications                                                                                                                                                                                                                                                          |
| **Metadata**       | Descriptive information about the data and nodes in the network — not the data itself                                                                                                                                                                                                                      |
| **Blockchain**     | The mechanism used to store and distribute policies across the network in a consistent, tamper-resistant way. When a blockchain platform isn't in use, the Metadata Manager's local database serves the same role — both documentation and system refer to this repository as "the blockchain" either way. |
| **Policy**         | A JSON-structured record stored in the network's metadata, describing things like node configuration, network connectivity, or cluster membership                                                                                                                                                          |
| **Services**       | Components of AnyLog/EDF that can be started and stopped independently                                                                                                                                                                                                                                     |
| **Nodes / Agents** | Running AnyLog/EDF instances                                                                                                                                                                                                                                                                               |
| **Containers**     | Docker instances running AnyLog/EDF                                                                                                                                                                                                                                                                        |

## Node Types

AnyLog/EDF uses a single codebase across all node types. Except for Operator and Publisher — which are
mutually exclusive on the same node — any node can run any combination of services simultaneously.

| Node type            | Role                             | Key characteristic                                                                                                                                                                                                                               |
|----------------------|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Metadata Manager** | Hosts the network's metadata     | Also called the Master Node. Optional — only needed when not using a blockchain platform. One per network (or HA pair).                                                                                                                          |
| **Operator**         | Stores and serves data           | Hosts local databases, answers queries, and receives data from southbound connectors or Publishers.                                                                                                                                              |
| **Publisher**        | Routes data to Operators         | Receives data from devices or connectors, resolves the target Operator from the metadata layer, and forwards the data. Does not store data locally. Cannot run on the same node as an Operator. AnyLog/EDF-specific — not available in EdgeLake. |
| **Query**            | Orchestrates distributed queries | Receives SQL from applications, fans the query out to relevant Operators, and returns aggregated results. Any node can serve as a Query node — it's a role, not a dedicated machine.                                                             |

### Metadata Manager

Also called the **Master Node**. Hosts the network's metadata: node configurations, policies (including network
connectivity details), which cluster/operator a given dataset lives on, Unified Namespace (UNS) definitions, and
scheduler information — everything about the network *except* the data itself.

The actual data — both the logical database records and the original raw files (e.g. JSON) as they arrived — lives on
the Operator node(s), not the Metadata Manager.

- **When to use:** Any deployment that does not use a blockchain platform (Optimism, Ethereum, etc.) needs a Metadata
  Manager. Using a blockchain instead is optional but removes the single point of failure.
- **Access:** Must be continuously reachable by all nodes in the network.
- **Location:** Cloud or office machine with stable, consistent connectivity.

### Operator Node

The data layer of the network. Operator nodes host the actual databases — SQL or NoSQL — where time-series and event
data is stored and indexed, alongside the original raw data as it arrived. They respond directly to queries fanned out
by Query Nodes.

- **Access:** Must communicate bi-directionally with the Metadata Manager, Query Nodes, and peer Operators within the
  same cluster.
- **Location:** Typically at the edge, close to data sources. HA deployments add a cloud-hosted replica in the same
  cluster.

### Publisher Node

An optional ingestion router. A Publisher accepts data from multiple sensors or devices, looks up the appropriate
Operator for each dataset using the metadata layer, and forwards it. It never writes data to a local database.

Use a Publisher when a single ingestion point needs to distribute data across multiple clusters, or when you want to
decouple data sources from storage topology.

> A node cannot run both Operator and Publisher services. Choose one per node.

- **Access:** Must be able to reach the target Operator node(s).
- **Location:** At the edge, alongside or near the data sources.

### Query Node

Accepts SQL queries from external applications — typically via REST — and coordinates execution across the network. It
uses cluster metadata to identify which Operators hold the relevant data, fans the query out in parallel, collects
partial results, and returns a unified response.

Any node can serve as a Query Node by enabling the REST service and the query thread pool. A dedicated Query Node is
recommended for production workloads handling high query volumes.

- **Access:** Must have network access to all Operator nodes it may query.
- **Location:** Same network considerations as the Metadata Manager — cloud or office with reliable connectivity.

### The Cluster

A **cluster** is a policy on the blockchain, not a running process. It declares that one or more Operator nodes are
collectively responsible for a specific set of tables. Every table in the network belongs to a cluster. This
membership drives:

- **Query routing** — the Query Node uses the cluster to find which Operators hold the data for a given table, then
  sends the query there.
- **HA replication** — when multiple Operators share a cluster, data written to any one of them is automatically
  replicated to the others.

## High-Level Architecture

### Data Flow Overview

```
  [ Sensor / Device ]
         │
         ▼
  [ Publisher Node ]  (optional — distributes data across operators)
         │
    ┌────┴────┐
    ▼         ▼
[ Operator ] [ Operator ]   ←──── [ Metadata Manager / Blockchain ]
    ▲         ▲                         (metadata sync, dotted lines)
    └────┬────┘
         │
  [ Query Node ]
         │
         ▼
  [ User Application ]
```

**Roles at a glance:**
- The **Metadata Manager** holds metadata for the entire network. Metadata is auto-generated as data arrives (node
  policies, table definitions, cluster mappings).
- The **Publisher Node** (optional) accepts raw sensor data and routes it to the correct Operator nodes.
- **Operator Nodes** store the actual data. Together they form a virtual data lake.
- The **Query Node** receives requests from applications, uses metadata from the blockchain to locate the data, and
  assembles the final result.

### Traditional vs. AnyLog/EDF Approach

**Traditional approach:** Data travels from sensors → edge hardware → cloud before it's accessible to applications.
"Real-time" dashboards often carry a significant hidden delay, and accessing edge data typically requires proprietary
software tightly coupled to specific devices.

**With AnyLog/EDF:** Each edge data server becomes an Operator node, directly part of the queryable network. Multiple
Operator nodes together form a virtual data lake. Applications connect to a single Query node — not to each data
source individually — and AnyLog/EDF handles locating and retrieving the data using blockchain metadata. This removes
the complexity of managing multiple connections, eliminates the need to know where data physically resides, and
dramatically reduces latency.

### Application-Facing Architecture

```
  [ Customer Application ]
           │
           ▼
    [ Query Node ]
     /     |      \
    ▼      ▼       ▼
[Edge  ] [Edge  ] [Cloud /
 Op. I]  Op. II]  Historical Op.]
```

The application connects only to the Query node. AnyLog/EDF routes each request to the appropriate operator(s)
automatically, returning a unified result regardless of how many nodes or locations are involved.

## The Data Lifecycle

This is the conceptual version of how data moves through AnyLog, from generation to query. A deeper, protocol-by-
protocol walkthrough belongs under **11- Examples & Use Cases/**, not here.

```
  [ PLC / Sensor ]
         │   (MQTT, DNP3, ...)
         ▼
  [ Southbound Connector ]   (direct — or via a 3rd-party bridge, e.g. Node-RED)
         │
         ▼
  [ Operator Node ]
         │   generates table (if new) + publishes metadata/policy
         ▼
  [ Local Table ] + [ Raw File ]
         │
         ▼
    [ Query Node ]
         │
         ▼
  [ User / Application ]
```

A PLC or other device/sensor generates data and sends it out using one of several protocols — some natively supported
by AnyLog (e.g. MQTT, DNP3), others not (e.g. BACnet). That data reaches AnyLog either directly, through an existing
southbound connector, or indirectly, through a third-party bridge like Node-RED.

The receiving Operator node ingests the data, converting it from its original format (e.g. JSON) into a SQL table. If
no table definition exists yet for this data, one is generated automatically as part of ingestion — along with any
metadata/policies other nodes need in order to know this data now lives on this cluster.
The data is then stored — both as structured table rows and as the original raw file — and becomes queryable.
The only real "wait" in this pipeline isn't processing delay — it's the Operator's data buffer, which flushes on a
configurable threshold (default: 100MB or 60 seconds, whichever comes first).

## High Availability (HA)

AnyLog's availability model is **horizontal**, not vertical: resilience comes from adding more Operator nodes to a
cluster, not from making any single node more redundant on its own.

Backing up operators is designed to scale with this architecture. You can add as many Operator nodes as needed, the 
system will automatically perform hot backups across the cluster. If the primary Operator receiving live data becomes
unavailable, one or more HA Operator nodes — already holding the replicated historical data — can immediately take
over serving it, providing both scalability and resilience.

Users can also layer on database-level redundancy for **vertical** scaling or additional replication — for example,
PostgreSQL's built-in backup/replication features, or an orchestration layer like Kubernetes. These are supported at
the user's own discretion: they sit outside AnyLog's own HA guarantees unless described in the relevant chapter(s)
covering that specific integration.