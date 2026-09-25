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
- 2026-08-29 | Moshe Shadmon | Update Page content |
-->



# Getting Started

AnyLog is a distributed data platform designed to manage and provide unified access to operational data across edge environments.

An AnyLog network consists of nodes that provide different services. **Operator nodes host and process the operational data**, while a shared **metadata layer** describes the network, the data available across it, where that data is located, and how it can be accessed.

The fundamental design is:

> **The data remains distributed. The metadata describes the distributed environment. AnyLog uses the metadata to provide a unified view of the data.**

Applications and users do not need to know which node physically hosts the requested data. AnyLog uses the metadata to identify the relevant nodes, routes requests to those nodes, and returns a unified result.

This page introduces the main concepts needed to deploy and operate an AnyLog network.

---

## Architecture Overview

AnyLog decouples the **logical organization of data** from its **physical organization**.

```text
                   Users / Applications / AI
                             │
                    SQL / REST / APIs / UNS
                             │
                       AnyLog Network
                             │
                    Metadata determines
                    where data resides
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
         Operator A     Operator B     Operator C
          Local Data     Local Data     Local Data
            Site A         Site B         Site C
```

### Physical Data Organization

Operational data is distributed across AnyLog **Operator nodes**.

Data streamed to an Operator is managed locally by that node and does not need to be moved to a centralized database or cloud repository. Different Operators can use different local databases depending on the deployment requirements.

### Logical Data Organization

The **metadata layer** describes the distributed environment, including:

- nodes and the services they provide,
- clusters and relationships between nodes,
- tables supported by the network,
- where data is located,
- table schemas,
- data mappings,
- permissions and configuration,
- Unified Namespace (UNS) definitions,
- and other application or user-defined metadata.

This allows users, applications, and AI agents to access and understand the distributed data without needing to know its physical location.

---

## Node Roles

Every AnyLog node runs the same software. The services enabled in the node configuration determine its role in the network.

A node can provide one or more roles.

| Node Role | Purpose |
| --- | --- |
| **Operator** | Hosts operational data, processes data locally, and satisfies queries. |
| **Publisher** | Receives data from devices or applications and distributes it to Operators. |
| **Query** | Receives distributed queries, identifies the relevant Operators, and aggregates their results. |
| **Master** | Hosts the shared metadata ledger when a blockchain platform is not used. |

### Operator

The **Operator** is the node that hosts and processes operational data.

An Operator can:

- receive streamed data,
- map incoming data into the required structure,
- maintain the data in a local database,
- execute SQL queries locally,
- respond to distributed queries,
- and replicate data to other Operators when high availability is configured.

Operators are typically deployed close to the systems generating the data — for example at a plant, site, gateway, machine, or other edge location.

### Publisher

A **Publisher** receives data from devices, applications, brokers, or other data sources and distributes the data to the appropriate Operators.

The Publisher uses metadata to determine where the data should be delivered. This allows data sources to publish data without knowing which Operator physically manages it.

A Publisher is optional. Data can also be delivered directly to an Operator.

### Query Node

A **Query Node** is the entry point for a distributed query.

When a query is submitted, the Query Node:

1. Uses the metadata to determine which Operators host the requested data.
2. Sends the query to those Operators.
3. Each Operator processes the query against its local data.
4. The Query Node collects the replies.
5. The results are returned as a unified result.

```text
                         SQL Query
                            │
                            ▼
                       Query Node
                            │
                     Metadata Lookup
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Operator A     Operator B     Operator C
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                     Unified Result
```

The user or application does not need to identify the nodes that host the relevant data.

### Master Node

The **Master Node** hosts the shared metadata when a blockchain platform is not used.

The Master Node is a **blockchain emulator**. It supports the same AnyLog metadata APIs and policy model as a blockchain, allowing nodes and applications to operate in the same way regardless of which metadata backend is selected.

---

## Metadata

Metadata is the information shared by members of an AnyLog network that describes the network and its data.

The metadata is organized as JSON objects called **policies**.

For example:

```json
{
  "operator": {
    "name": "operator-1",
    "company": "AnyLog",
    "ip": "10.0.0.10",
    "port": 32148,
    "rest_port": 32149
  }
}
```

Different policy types describe different parts of the network, such as:

- Operators and other nodes,
- clusters,
- tables,
- mappings,
- configuration,
- permissions,
- UNS objects and relationships,
- and user-defined metadata.

The shared metadata can be maintained using either:

- an AnyLog **Master Node**, or
- a supported **blockchain platform**.

The AnyLog APIs and policy model are the same in both cases.

### Local Metadata

Each node periodically synchronizes the shared metadata and maintains a local copy.

```text
        Master Node / Blockchain
                  │
                  │ synchronization
                  ▼
           Local Metadata
                  │
                  ▼
            AnyLog Node
```

During normal operation, the node uses its local metadata. As a result, metadata lookups do not require continuous access to the Master Node or blockchain.

If access to the shared metadata is temporarily unavailable, the node can continue operating using its most recently synchronized metadata.

> Only metadata is synchronized through this process. Operational data remains distributed across the Operator nodes.

See [Blockchain & Metadata](/docs/08-blockchain-and-metadata/) for details on policies, metadata synchronization, Master Node configuration, and metadata commands.

---

## Clusters

A **cluster** represents a logical partition of the data in the AnyLog network, while Operator nodes host and manage the physical data associated with that partition.

A logical table can span multiple clusters, with each cluster representing a different partition of the table's data. One or more Operator nodes are assigned to each cluster and physically maintain that cluster's data.

Without High Availability (HA), a cluster is assigned to a single Operator. With HA enabled, multiple Operators are assigned to the same cluster and replicate the cluster's data so that they eventually maintain the same physical data.

A logical table can exist across **multiple clusters**. Each cluster may contain different rows of that table, allowing the table's data to be distributed across locations, sites, or other partitions of the network.

For example, without High Availability (HA), each cluster is assigned to a single Operator:

~~~text
                         Table A
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
             Cluster 1               Cluster 2
          Data Partition 1         Data Partition 2
                │                       │
                ▼                       ▼
           Operator 1              Operator 2
~~~

In this example, `Table A` exists in both clusters, but the data maintained by `Cluster 1` is different from the data maintained by `Cluster 2`. Together, the clusters provide the distributed data associated with the logical table.

### High Availability

By default, without High Availability (HA), **each cluster is assigned to a single Operator**. That Operator maintains the data partition associated with the cluster.

When HA is enabled, **multiple Operators are assigned to the same cluster**. When data is received by any Operator in the cluster, it is replicated to the other Operators assigned to that cluster.

For example:

~~~text
                         Table A
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
             Cluster 1               Cluster 2
          Data Partition 1         Data Partition 2
                │                       │
          ┌─────┼─────┐             ┌───┴───┐
          ▼     ▼     ▼             ▼       ▼
        Op 1  Op 2  Op 3          Op 4    Op 5
~~~

Within `Cluster 1`, Operators 1, 2, and 3 maintain replicas of Data Partition 1. Within `Cluster 2`, Operators 4 and 5 maintain replicas of Data Partition 2.

Replication is asynchronous, so Operators assigned to the same cluster may not contain identical data at every instant. However, **the Operators within a cluster eventually maintain the same data**.

The distinction between clusters and Operators is therefore important:

- **Across clusters, data is partitioned** — different clusters can maintain different portions of the same logical table.
- **Within a cluster, data is replicated when HA is enabled** — Operators assigned to the same cluster eventually maintain the same data.
- **Without HA, a cluster has one Operator** — that Operator maintains the cluster's data partition.

When a distributed query references a table, AnyLog uses the metadata to identify the clusters that maintain that table and the Operators assigned to those clusters. The query is processed against the distributed data partitions, and the results are combined into a unified result.

This allows a single logical table to span distributed locations while optionally providing redundancy and high availability within each cluster.

## Distributed Queries

Data can be distributed across many Operator nodes while applications query it as a single logical data environment.

Distributed SQL queries are issued using the `run client` command. The query identifies the logical database and table, while AnyLog uses the metadata to determine which clusters and Operator nodes maintain the requested data.

For example:

~~~anylog
run client () sql plant_data format = table and stat = select timestamp, temperature from sensors where timestamp >= NOW() - INTERVAL '10 minutes'
~~~

The application does not need to specify which Operator nodes host the data.

AnyLog uses the metadata to identify the clusters that maintain the requested table and the Operators assigned to those clusters. The query is distributed to the relevant Operators, processed against their local data, and the results are aggregated into a unified result.

Conceptually:

~~~text
             Logical SQL Query
                    │
                    ▼
            Metadata Resolution
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
     Cluster 1  Cluster 2  Cluster 3
         │          │          │
         ▼          ▼          ▼
     Operator    Operator    Operator
         │          │          │
         └──────────┼──────────┘
                    ▼
               Unified Result
~~~

The physical distribution of the data is therefore decoupled from the logical SQL interface presented to users and applications.

See [SQL Commands](/docs/07-cli/04-sql/) for the complete AnyLog SQL syntax, distributed query options, output formats, and examples.

## Unified Namespace

The **Unified Namespace (UNS)** provides a logical hierarchy over the distributed operational data.

For example:

```text
Enterprise
└── Site
    └── Production Line
        └── Machine
            └── Sensor
```

The hierarchy is described in metadata. The underlying operational data does not need to be reorganized or moved.

AnyLog supports multiple ways to create a UNS:

- users can explicitly define the hierarchy,
- existing structures such as OPC-UA hierarchies or MQTT topics can be used to generate it,
- and AI can generate or extend the hierarchy from available metadata and data structures.

SQL and UNS provide complementary ways to access the same distributed data:

- **SQL** provides direct analytical access.
- **UNS** provides contextual navigation through logical objects and relationships.

See [Unified Namespace](/docs/08-blockchain-and-metadata/04-unified-namespace/) for details.

---

## Installing AnyLog

AnyLog can be deployed using:

- **Docker**
- **Kubernetes**
- a direct installation from the AnyLog source distribution

The deployment and configuration determine which services the node provides.

See the installation and deployment documentation for the supported deployment options and configuration examples.

---

## The AnyLog Command Line

When an AnyLog node starts, it provides the AnyLog Command Line Interface (CLI).

The default prompt is:

```text
AL >
```

The CLI can be used to inspect the node, configure services, manage metadata, communicate with peer nodes, and query data.

### Help

Use:

```anylog
help
```

to list available commands.

Commands can also be searched by prefix:

```anylog
help get
help set
help blockchain
```

To retrieve usage and examples for a specific command:

```anylog
help blockchain get
```

or:

```anylog
help blockchain insert
```

The command help provides the command syntax, explanation, examples, and a link to the relevant documentation.

---

## The Node Dictionary and Environment Variables

AnyLog provides two types of variables that can be referenced from CLI commands:

- **Dictionary variables** — maintained by AnyLog and referenced using `!`.
- **Environment variables** — maintained in the process environment and referenced using `$`.

### Dictionary Variables

Use `set` to assign a value to the AnyLog dictionary.

For example:

~~~anylog
set data_dir = /app/AnyLog-Network/data
~~~

The value can then be referenced using `!data_dir`:

~~~anylog
get !data_dir
~~~

or used as part of another command:

~~~anylog
set backup_dir = !data_dir/backup
~~~

To view the complete dictionary:

~~~anylog
get dictionary
~~~

To search the dictionary for keys containing a particular string, specify the search string:

~~~anylog
get dictionary _dir
~~~

This returns dictionary entries whose keys contain `_dir`, making it useful for locating configuration values such as `data_dir`, `backup_dir`, or other directory settings.

### Environment Variables

Environment variables are referenced using `$`.

For example:

~~~anylog
get $HOME
~~~

Environment variables can also be created or changed directly from the AnyLog CLI using `set`:

~~~anylog
set $ANYLOG_SITE = plant_1
~~~

The value can then be referenced from AnyLog commands:

~~~anylog
get $ANYLOG_SITE
~~~

Both dictionary and environment variables can therefore be configured and used directly from the AnyLog CLI:

~~~anylog
set company_name = AnyLog
set $ANYLOG_SITE = plant_1

get !company_name
get $ANYLOG_SITE
~~~

Dictionary variables are commonly used by AnyLog configuration and deployment scripts, while environment variables provide access to values maintained in the process environment.

---

## Check a Running Node

A few commands are particularly useful after starting a node.

### View Active Processes

```anylog
get processes
```

This displays the background services currently running on the node.

### Test the Node

```anylog
test node
```

This tests the basic node configuration.

### Test the Network

```anylog
test network
```

This tests the availability of network members known to the node.

---

## Basic Deployment Flow

At a high level, deploying an AnyLog network consists of the following steps:

1. **Install AnyLog** on the physical machines, virtual machines, gateways, or containers that will participate in the network.
2. **Configure the metadata layer** using a Master Node or blockchain platform.
3. **Configure each node** with the services it will provide, such as Operator, Publisher, or Query services.
4. **Connect the nodes to the shared metadata** so they can discover the network and synchronize their local metadata.
5. **Configure data ingestion** from the required devices, brokers, databases, or applications.
6. **Verify the nodes and network** using `get processes`, `test node`, `test network`, and `blockchain get *`.
7. **Query the distributed data** using SQL, REST, or another supported interface.
8. **Add logical context** using mappings, UNS definitions, permissions, and other metadata as required.

The same architecture can be used for a small deployment on a single machine or a distributed network spanning many edge locations.

---

## Next Steps

After understanding the concepts on this page, continue with the documentation based on what you want to configure:

| Topic | What it covers |
| --- | --- |
| **Installation & Deployment** | Installing and starting AnyLog nodes. |
| **Node Configuration** | Configuring node services, networking, databases, and directories. |
| **Data Ingestion & Mapping** | Connecting data sources and transforming incoming data. |
| **Queries** | Querying local and distributed operational data. |
| **Blockchain & Metadata** | Policies, metadata synchronization, Master Node configuration, and metadata commands. |
| **Unified Namespace** | Creating logical asset hierarchies over distributed operational data. |
| **Networking & Security** | Network connectivity, authentication, permissions, and secure communication. |
| **High Availability** | Replication and failover across Operator nodes. |

The key model to keep in mind throughout the documentation is:

```text
Distributed Operational Data
            +
Shared Metadata and Context
            +
Distributed Query and Routing
            =
Unified Access Without Centralizing the Data
```


<!--
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

-->