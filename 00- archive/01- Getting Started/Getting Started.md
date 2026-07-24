---
title: Getting Started
description: Introduction to AnyLog and EdgeLake — architecture, node types, metadata, and core CLI operations.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document (legacy)
- 2026-04-25 | hyperlink fix (legacy)
- 2026-07-02 | Unified from: 01- Getting Started/Getting Started.md, 
                             ORPHANS/x anylog-docs/Getting-Started/getting-started.md, 
                             ORPHANS/x edgelake-docs/getting_started.md
               Hyperlinks re-pointed to numeric doc tree, however there are a few outstanding issues: 
                 1. **Master Node setup page has no numeric target.** The old link (`master node.md`) pointed to a 
                    dedicated setup guide that doesn't exist anywhere in the numbered tree. Needs either: (a) confirmation 
                    that this content lives inside `03- Installation & Deployment/A- Deployment Options/Node Configuration.md` 
                    or `Deploying a Node.md`, or (b) a new page created for it.
                 2. **"Using EdgeX" link is ambiguous.** Two candidate targets exist in the numbered tree — 
                    `03- Installation & Deployment/04- Cloud Support & Edge Deployments/EdgeX - complete example.md` and 
                    `07- Connectors & Integrations/B- Southbound Interfaces/Using MQTT (EdgeX).md` — and it's unclear 
                    which one the original link meant.
                 3. **"Starting an AnyLog Instance" has no numeric home.** This content only exists at 
                    `ORPHANS/x01-getting-started/starting an anylog instance.md`. Either merge it into 
                    `Quick Deployment Guide.md` or create a new numbered page for it.
                 4. **"Metadata Requests" link target is marked draft.** The old target 
                    (`99- Core Concepts/A- Agent Services/ZZZ metadata requests.md`) carries the `ZZZ` prefix used 
                    elsewhere in the repo to flag draft/deprecated content — needs a status check before it's safe to link.
                 5. **Sibling pages not yet reconciled.** This unified doc assumes `Overview.md`, `Prerequisite.md`, and 
                    `Quick Deployment Guide.md` (already in `01- Getting Started/`) stay separate and unchanged — I haven't 
                    verified those three don't already duplicate content now folded into this merged doc (e.g. install 
                    steps, directory structure).
                 6. **Original MODBUS.md / modbus.md duplicate** — still unresolved from earlier; two identical files with 
                    different casing (`MODBUS.md` vs `modbus.md`) sitting in the repo, one needs to be removed once you 
                    confirm which location/casing is canonical.
                 7. **southbound-overview.md / southbound overview.md title mismatch** — still unresolved; only difference 
                    is the frontmatter `title` (`A- Data Ingestion (Southbound)` vs `Data Ingestion (Southbound)`), and 
                    it's unclear which is meant to live where (subfolder vs. root-level file) — flagged but not yet 
                    checked against the actual repo copy.
-->

# Getting Started

Welcome to AnyLog! This guide introduces the platform's architecture, node types, and metadata model, then covers the 
core CLI operations you'll use to run and manage a node.

* [What is AnyLog](#what-is-anylog)
* [EdgeLake vs AnyLog](#edgelake-vs-anylog)
* [Key Terminology](#key-terminology)
* [Node Types](#node-types)
* [Network Architecture](#network-architecture)
* [The Network Metadata](#the-network-metadata)
* [The Data](#the-data)
* [Install](#install)
* [Local Directory Structure](#local-directory-structure)
* [Basic Operations](#basic-operations)
* [Making a Node a Member of the Network](#making-a-node-a-member-of-the-network)
* [The Seed Command](#the-seed-command)
* [Using the REST API](#using-the-rest-api-to-issue-anylog-commands)
* [Sending Messages to Peers](#sending-messages-to-peers-in-the-network)
* [Querying and Updating Metadata](#querying-and-updating-metadata-in-the-blockchain)
* [High Availability](#high-availability-ha)
* [Network Security](#network-security)

---

## What is AnyLog

**AnyLog** is a decentralized network for managing **IoT and time-series data** across distributed environments. It 
enables real-time data ingestion, storage, and querying by connecting independent compute nodes — each running the 
AnyLog software — that coordinate through shared metadata and protocols.

When deployed on edge nodes, AnyLog forms a peer-to-peer (P2P) network in which each node contributes data and compute 
resources. Applications access distributed IoT data through a **single query point**, as if the data were stored on one 
system.

The architecture consists of two complementary layers:
* **Physical layer** — manages and processes data locally on edge nodes.
* **Virtualized data layer** — provides unified access to distributed datasets across the network.

Together, these layers create a cloud-like architecture for distributed edge and IoT data — enabling real-time access 
without moving data and without locking organizations into a specific cloud, application, or hardware vendor.

## What is Edge Data Fabric (EDF)?

The __Edge Data Fabric (EDF)

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

| Feature | EdgeLake          | AnyLog |
|---|-------------------|---|
| Cost | Free / Open-Source | Subscription |
| Virtual edge layer | ✅                 | ✅ |
| Rule engine | ✅                 | ✅ |
| Policy-based data management | ✅                 | ✅ |
| Node management | ✅                 | ✅ |
| Unified APIs, CLIs, Admin UI | ✅                 | ✅ |
| Supported IoT connectors | ✅                 | ✅ |
| Blockchain abstraction | ✅                 | ✅ |
| MCP Integration | limited           | ✅ |
| Aggregations | ❌                 | ✅ |
| Automated Unified Namespace (UNS) | ❌                 | ✅ |
| Security protocol & High Availability (HA) | ❌                 | ✅ |
| Publisher node role | ❌                 | ✅ |

**AnyLog (Enterprise)** includes everything in EdgeLake plus: advanced security and authentication, federated data 
aggregation and model training, and real-time support with SLA options.

Note: EdgeLake supports **MongoDB** as an additional Operator database option (for unstructured data) alongside 
PostgreSQL and SQLite — see [The Data](#the-data).

---

## Key Terminology

| Term | Definition |
|---|---|
| **Southbound** | Data flowing *in* from devices and sensors, stored into AnyLog |
| **Northbound** | Queries and results flowing *out* to applications |
| **Blockchain** | The metadata layer — tracks nodes, datasets, and configurations across the network |
| **Metadata** | Descriptive information about the data and nodes in the network (not the data itself) |
| **Services** | Components of AnyLog / EdgeLake that can be started and stopped independently |
| **Nodes / Agents** | Running AnyLog instances |
| **Containers** | Docker instances running AnyLog |

---

## Node Types

AnyLog uses a single codebase across all node types. With the exception of Operator and Publisher — which are mutually 
exclusive on the same node — any node can run any combination of services simultaneously.

| Node type | Role | Key characteristic |
|---|---|---|
| **Master** | Hosts the metadata ledger | Optional — only needed when not using a blockchain platform. One per network (or HA pair). |
| **Operator** | Stores and serves data | Hosts local databases, answers queries, and receives data from southbound connectors or Publishers. |
| **Publisher** | Routes data to Operators | Receives data from devices or connectors, resolves the target Operator from the metadata layer, and forwards the data. Does not store data locally. Cannot run on the same node as an Operator. AnyLog-specific — not available in EdgeLake. |
| **Query** | Orchestrates distributed queries | Receives SQL from applications, fans the query out to relevant Operators, and returns aggregated results. Any node can serve as a Query node — it's a role, not a dedicated machine. |

### The Cluster

A **cluster** is a policy on the blockchain, not a running process. It declares that one or more Operator nodes are collectively responsible for a specific set of tables. Every table in the network belongs to a cluster. This membership drives:

- **Query routing** — the Query Node uses the cluster to find which Operators hold the data for a given table, then sends the query there.
- **HA replication** — when multiple Operators share a cluster, data written to any one of them is automatically replicated to the others. See [High Availability](../04- Core Concepts/High Availability.md).

### Master Node

Stores the network's metadata in a local database, making it available to all peer nodes on demand. Acts as a centralized metadata ledger when a blockchain platform is not in use.

- **When to use:** Any deployment that does not use a blockchain platform (Optimism, Ethereum, etc.) needs a master node. Using a blockchain is optional but removes the single point of failure.
- **Access:** Must be continuously reachable by all nodes in the network.
- **Location:** Cloud or office machine with stable, consistent connectivity.

<!-- LINK NEEDS TARGET: legacy docs reference a dedicated "Using a Master Node" page (old path: master node.md). No equivalent file currently exists under the numeric tree. Closest candidates: ../03- Installation & Deployment/A- Deployment Options/Node Configuration.md or Deploying a Node.md — confirm which (or create a new page) before publishing. -->

### Operator Node

The data layer of the network. Operator nodes host the actual databases — SQL or NoSQL — where time-series and event data is stored and indexed. They respond directly to queries fanned out by Query Nodes.

- **Access:** Must communicate bi-directionally with the Master Node, Query Nodes, and peer Operators within the same cluster.
- **Location:** Typically at the edge, close to data sources. HA deployments add a cloud-hosted replica in the same cluster.

See [Operator](../04- Core Concepts/A- Agent Services/Operator.md).

### Publisher Node

An optional ingestion router. A Publisher accepts data from multiple sensors or devices, looks up the appropriate Operator for each dataset using the blockchain metadata, and forwards it. It never writes data to a local database.

Use a Publisher when a single ingestion point needs to distribute data across multiple clusters, or when you want to decouple data sources from storage topology.

> A node cannot run both Operator and Publisher services. Choose one per node.

- **Access:** Must be able to reach the target Operator node(s).
- **Location:** At the edge, alongside or near the data sources.

See [Publisher](../04- Core Concepts/A- Agent Services/Publisher.md).

### Query Node

Accepts SQL queries from external applications — typically via REST — and coordinates execution across the network. It uses the cluster metadata to identify which Operators hold the relevant data, fans the query out in parallel, collects partial results, and returns a unified response.

Any node can serve as a Query Node by enabling the REST service and the query thread pool. A dedicated Query Node is recommended for production workloads handling high query volumes.

- **Access:** Must have network access to all Operator nodes it may query.
- **Location:** Same network considerations as the Master Node — cloud or office with reliable connectivity.

See [Query](../04- Core Concepts/A- Agent Services/Query.md).

---

## Network Architecture

### Data Flow Overview

```
  [ Sensor / Device ]
         │
         ▼
  [ Publisher Node ]  (optional — distributes data across operators)
         │
    ┌────┴────┐
    ▼         ▼
[ Operator ] [ Operator ]   ←──── [ Master Node / Blockchain ]
    ▲         ▲                         (metadata sync, dotted lines)
    └────┬────┘
         │
  [ Query Node ]
         │
         ▼
  [ User Application ]
```

**Roles at a glance:**
- The **Master Node** holds metadata for the entire network. Metadata is auto-generated as data arrives (node policies, table definitions, cluster mappings).
- The **Publisher Node** (optional) accepts raw sensor data and routes it to the correct operator nodes.
- **Operator Nodes** store the actual data. Together they form a virtual data lake.
- The **Query Node** receives requests from applications, uses metadata from the blockchain to locate the data, and assembles the final result.

### Traditional vs. AnyLog Approach

**Traditional approach:** Data travels from sensors → edge hardware → cloud before it's accessible to applications. 
"Real-time" dashboards often carry a significant hidden delay, and accessing edge data typically requires proprietary 
software tightly coupled to specific devices.

**With AnyLog / EdgeLake:** Each edge data server becomes an operator node, directly part of the queryable network. 
Multiple operator nodes together form a virtual data lake. Applications connect to a single query node — not to each data 
source individually — and AnyLog handles locating and retrieving the data using blockchain metadata. This removes the 
complexity of managing multiple connections, eliminates the need to know where data physically resides, and dramatically 
reduces latency.

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

The application connects only to the query node. AnyLog routes each request to the appropriate operator(s) automatically, 
returning a unified result regardless of how many nodes or locations are involved.

---

## The Network Metadata

The metadata is the network-related information shared among members of the network. This includes:
* Details about network members
* Permissions and access control
* Logical representation of data
* Information on how data is distributed

The metadata is stored in a repository accessible to all nodes — either a **blockchain** (e.g., Ethereum) or a 
**Master node** — as specified in the node's configuration. Interaction with the metadata is identical regardless of 
repository type, which lets you switch between a Master node and a blockchain without changing logic or process. For 
consistency, both the documentation and the system refer to the metadata repository as "the blockchain," even when a 
Master node is used.

**Data is not stored on the blockchain.** Raw data lives on operator nodes. The blockchain stores only metadata — node 
policies, table definitions, cluster assignments, and similar configuration records. Because the ledger is non-mutable, 
it ensures trust and consistency among all participants without a single point of failure. Operator, Query, and Publisher 
nodes synchronize their configurations via the blockchain, so the network self-organizes as nodes join or leave.

The metadata is organized as **policies** — each a JSON structure associated with a type (e.g. security, member, 
distribution). Policies are updated dynamically by the network protocol (for example, when a node joins) or by users 
through APIs or the CLI.

### Metadata Synchronization

Each node maintains a local copy of the metadata. A background process periodically checks the configured repository for 
updates and pulls changes if necessary. During operation, the node uses its local copy, which ensures:
* Node behavior is independent of the metadata source (blockchain or Master node)
* Nodes continue operating even if the connection to the metadata repository is temporarily lost

For more details, see: [Blockchain Synchronizer](../04- Core Concepts/Background Processes.md#blockchain-synchronizer)

**Related documentation:**

| Section | Information provided |
|---|---|
| [Metadata Management](../04- Core Concepts/Metadata Management.md#managing-metadata) | Details on the network metadata and related processes. |
| [Using Ethereum](../17- Appendices/B- Blockchain Integration/Using Ethereum.md#using-ethereum-as-a-global-metadata-platform) | Using Ethereum as a global metadata platform. |

<!-- LINK REMOVED: legacy "Metadata Requests" link pointed to 99- Core Concepts/A- Agent Services/ZZZ metadata requests.md. The "ZZZ" prefix elsewhere in this repo marks draft/deprecated content — confirm whether this file is publish-ready before re-adding the link. -->

---

## The Data

Users' data is distributed across local databases on Operator nodes. Different Operators can use different databases for different data sets. Supported databases:
* [PostgreSQL](https://www.postgresql.org/) — recommended for larger nodes and large data sets.
* [SQLite](https://www.sqlite.org/index.html) — recommended for gateways, smaller nodes, and small or in-memory data sets.
* [MongoDB](https://www.mongodb.com/) — recommended for unstructured data (EdgeLake Operators).

The network protocol provides a unified view over this distributed data — users and applications don't need to identify which nodes host relevant data. Each query starts at a **Query Node**, which determines which Operators host the relevant data (via cluster metadata), delivers the query to them, and aggregates their results into a single unified response.

### How Data is Collected (Southbound)

| Method | Description |
|---|---|
| **REST PUT** | AnyLog maps the request to a DB, table, and key/value pairs |
| **REST POST** | AnyLog consumes messages and applies mapping to DB tables |
| **Remote Message Broker** | Kafka / MQTT — AnyLog subscribes and applies mapping to DB tables |
| **Local Message Broker** | AnyLog itself acts as the MQTT broker |
| **OPC-UA / EtherNet-IP / Modbus** | Values stored in timestamp/value format for time-series data |
| **gRPC** | Used for KubeArmor, monitoring tools, and video/inference streaming |

The mapping layer translates incoming messages or streams into the correct database structure so data is immediately queryable. AnyLog supports a **Unified Namespace (UNS)** — built-in or customer-defined — providing consistent variable names across all nodes. EdgeLake does not include a built-in UNS.

### How Querying Works

**Part 1 — Metadata sync:** a background process continuously synchronizes metadata between the blockchain and each node in the network, particularly Query nodes, keeping routing information current.

**Part 2 — Query execution:**
1. A user sends a `SELECT` request to the Query Node (typically via REST).
2. The Query Node uses its local metadata copy to identify which Operator node(s) hold the relevant data.
3. The Query Node distributes the request. For aggregate queries (e.g. `SELECT avg(...)`), each Operator computes partial results (`sum`, `count`) and returns them; the Query Node assembles the final answer.
4. The result is returned to the application.

Applications never need to know where data is physically stored — the AnyLog network handles that.

**Related documentation:**

| Section | Information provided |
|---|---|
| [Adding Data to Nodes in the Network](../06- Data Management/A- Data Ingestion/Adding Data.md) | Delivering data to Operators in the network. |
| [Mapping Data](../06- Data Management/A- Data Ingestion/Mapping Data to Tables.md) | Transformation of source data to the destination format. |
| [Using a Message Broker](../07- Connectors & Integrations/C- Messages Brokers/Message Broker Setup.md#using-a-message-broker) | Delivering data to Operators using an MQTT broker. |
| [Managing Data Files](../06- Data Management/D- Monitoring & Alerts/Managing Data Files Status.md) | Monitoring data managed by Operator nodes. |
| [Queries to Data](../06- Data Management/B- Query & Aggregations/Queries.md#query-nodes-in-the-network) | Queries to data hosted by nodes in the network. |
| [Profiling and Monitoring Queries](../06- Data Management/B- Query & Aggregations/Profiling & Monitoring Queries.md) | Identifying and profiling slow queries. |
| [Using Grafana](../07- Connectors & Integrations/A- Northbound Connectors/Using Grafana.md#using-grafana) | Integrating Grafana to visualize data. |

<!-- LINK NEEDS TARGET: legacy "Using EdgeX" link is ambiguous between ../03- Installation & Deployment/04- Cloud Support & Edge Deployments/EdgeX - complete example.md and ../07- Connectors & Integrations/B- Southbound Interfaces/Using MQTT (EdgeX).md. Pick one (or link both) before publishing. -->

---

## Install

AnyLog can be installed via Docker, Kubernetes, or by downloading the codebase from GitHub and running an installation 
script.

* Deployment options: [Deployment Options](../03- Installation & Deployment/A- Deployment Options/Deploying a Node.md)
* Prerequisites: [Prerequisite](Prerequisite.md)
* A guided walkthrough: [Quick Deployment Guide](Quick Deployment Guide.md)

<!-- LINK NEEDS TARGET: legacy doc also references a dedicated "Starting an AnyLog Instance" page (old path: ORPHANS/x01-getting-started/starting an anylog instance.md). This content has no numeric home yet — either fold its content into Quick Deployment Guide.md or create a new numbered page for it. -->

---

## Local Directory Structure

AnyLog's directory setup is configurable. The default setup is detailed below:

```anylog
Directory Structure   Explanation
-------------------   -----------------------------------------
--> AnyLog-Network    [AnyLog Root]
    -->anylog         [Directory containing authentication keys and passwords]
    -->blockchain     [A JSON file representing the metadata relevant to the node]
    -->data           [Users data and intermediate data processed by this node]
       -->archive     [The root directory of an archival directory]
       -->bkup        [Optional location for backup of user data]
       -->blobs       [Directory containing unstructured data]
       -->dbms        [Optional location for persistent database data (SQLite)]
       -->distr       [Directory used in the High Availability processes]
       -->error       [Storage location for new data that failed database storage]
       -->pem         [Directory containing keys and certificates]
       -->prep        [Directory for system intermediate data]
       -->test        [Directory for output data of test queries]
       -->watch       [Monitored directory — files placed here are processed]
       -->bwatch      [Monitored directory for unstructured data]
    -->source         [Root directory for source or executable files]
    -->scripts        [System scripts to install and configure the node]
       -->install     [Installation scripts]
       -->anylog      [Configuration scripts]
    -->local_scripts  [User scripts]
```

> **EdgeLake note:** the default Docker layout nests everything under `/app`, with node data under `/app/EdgeLake/` and 
> deployment scripts under `/app/deployment-scripts/`. The subfolder names and purpose (`archive`, `bkup`, `blobs`, `dbms`, 
> `distr`, `error`, `pem`, `prep`, `test`, `watch`, `bwatch`) are identical to the AnyLog layout above.

**Notes:**
* Create the work folders (only needs to be run once per machine):
    ```anylog
    create work directories
    ```
* List the directories on a node:
    ```anylog
    get dictionary _dir
    ```

---

## Basic Operations

### Initiating and Configuring AnyLog Instances

AnyLog is deployed and initiated using Docker or Kubernetes. It can be configured in several ways:
* Command-line arguments at launch — a list of AnyLog commands separated by `and`.
* Configuration commands issued directly on the CLI.
* A script file listing configuration commands (run via `process [path to script]`).
* A configuration file hosted in a database.
* A Configuration Policy associated with the node.

**Related documentation:**

| Section | Information provided |
|---|---|
| [Node Configuration](../03- Installation & Deployment/A- Deployment Options/Node Configuration.md#node-configuration) | Details on the configuration process. |
| [Deploying a Node](../03- Installation & Deployment/A- Deployment Options/Deploying a Node.md#deploying-a-node) | Basic deployment using Docker or Kubernetes. |
| [Network Setup](../02- Training & Tutorials/B- Advanced Topics/Network Setup.md) | A step-by-step example of a network deployment. |
| [Configuration Policies](../04- Core Concepts/Policies.md#configuration-policies) | Policy-based configuration. |

### The AnyLog Command Line Interface

When a node starts, it provides the **AnyLog CLI**. The prompt appears as `AL >` and can be changed with:
```anylog
set node name [node name]
```
Use the CLI to interact with the current node or peer nodes — retrieving/modifying configuration and process state, 
querying/updating the blockchain, and issuing SQL queries to local or network-wide data. Exit with `exit node`.

See: [The AnyLog CLI](../12- Commands & CLI/CLI.md).

### The help Command

The `help` command provides dynamic information on AnyLog commands.

* List all commands:
  ```anylog
  help
  ```
* List commands sharing a prefix (e.g. `get`):
  ```anylog
  help get
  help set
  help reset
  help blockchain
  ```
* Show usage, examples, and a doc link for a specific command:
  ```anylog
  help connect dbms
  help blockchain insert
  help get msg client
  ```
  Example output:
  ```anylog
  help blockchain get

  Usage:
          blockchain get [policy type] [where] [attribute name value pairs] [bring] [bring command variables]

  Explanation:
          Get the policies or information from the policies that satisfy the search criteria.

  Examples:
          blockchain get *
          blockchain get operator where dbms = lsl_demo
          blockchain get cluster where table[dbms] = purpleair and table[name] = air_data bring [cluster][id] separator = ,
          blockchain get operator bring.table [*] [*][name] [*][ip] [*][port]
          blockchain get * bring.table.unique [*]

  Index:
          ['blockchain']
  ```
* List the command index:
  ```anylog
  help index
  ```
* List commands under an index key (e.g. all commands under `s`):
  ```anylog
  help index s
  ```
  Returns commands such as `script`, `secure network`, `streaming`.

### The Node Dictionary

Every node maintains a dictionary mapping keys to values. Reference a key with a leading `!` instead of specifying its 
value directly.

* Assign a value:
  ```anylog
  key = value
  ```
  Example:
  ```anylog
  master_node = 126.32.47.29:2048
  ```
  If the value string matches a command name, assignment fails — use `set` to force it:
  ```anylog
  set dbms_name = test
  ```
* Retrieve a value:
  ```anylog
  !dbms_name
  ```
  or
  ```anylog
  get !dbms_name
  ```
* Retrieve all assigned values:
  ```anylog
  get dictionary
  ```

See: [The Local Dictionary](../17- Appendices/C- Reference Materials/dictionary.md#the-local-dictionary).

### Retrieving Environment Variables

Prefix a variable name with `$` to retrieve its value — e.g. `$HOME`, `$PATH`.

### Retrieving Active Background Processes

```anylog
get processes
```
See: [Background Processes](../04- Core Concepts/Background Processes.md).

### The Dynamic Logs

Every node maintains logs for different event types:
* **Event log** — executed commands
* **Error log** — commands that failed to execute
* **Query log** — executed SQL queries (must be enabled and configured)

See: [Profiling and Monitoring Queries](../06- Data Management/B- Query & Aggregations/Profiling & Monitoring Queries.md#profiling-and-monitoring-queries).

View logs:
```anylog
get event log
get error log
get query log
```
Reset logs:
```anylog
reset event log
reset error log
reset query log
```

---

## Making a Node a Member of the Network

Connecting a node to the network is explained in [Network Configuration](../03- Installation & Deployment/D- Networking & Security/Network Configuration.md).

Basic node configuration test:
```anylog
test node
```
Test availability of network members:
```anylog
test network
```

Users can associate a node with different networks or configurations — useful when testing multiple networks or switching between a main-net and a test-net.

### Switching Between Different Setups

You may have multiple [directory setups](#local-directory-structure) on the same node. Associate the node with a different setup location:
```anylog
set anylog home [path to AnyLog root]
```
`AnyLog root` is the `AnyLog-Network` directory. If assigned to a new root, recreate subdirectories with `create work directories` 
(see [Local Directory Structure](#local-directory-structure)).

---

## The Seed Command

When a new node starts, or you want to connect to a new network on the same root directory, retrieve and assign metadata with:
```anylog
seed from [ip:port]
```
`[ip:port]` is a member of the target network. See [Blockchain Commands](../12- Commands & CLI/A- Command Categories/Blockchain Commands.md#retrieving-the-metadata-from-a-source-node).

### Switching Between Different Master Nodes

Make the [blockchain synchronizer process](../04- Core Concepts/Background Processes.md#blockchain-synchronizer) 
connect to a different master node:
```anylog
blockchain switch network where master = [IP:Port]
```

---

## Using the REST API to Issue AnyLog Commands

Commands can be executed by sending them via REST to a node in the network — a node interprets and executes commands 
identically whether issued via CLI or REST.

See: [Using REST](../07- Connectors & Integrations/B- Southbound Interfaces/Using REST.md#using-rest).

---

## Sending Messages to Peers in the Network

Nodes can send messages — each including a command and, sometimes, data — to peers. Depending on the command, some 
messages trigger a reply (e.g. status request, SQL query); others execute only on the destination (e.g. change state, 
display message). If authentication is enabled, the receiving node validates the sender is authorized for the command 
before executing; unauthorized messages are discarded.

Format:
```anylog
run client (destination) command
```

**Message sections:**
- **`run client`** — makes the current node a client of one or more peer nodes; the command executes on the destination(s).
- **`(destination)`** — identified by IP:Port from the target's [TCP Server configuration](../04- Core Concepts/Background Processes.md). Can be:
  - A comma/space-separated list in parentheses: `(139.162.126.241 2048, 172.105.13.202 2048)`
  - A single IP:Port (no parentheses needed): `10.0.0.78:20348`
  - Variables: `!dest_ip !dest_port`
  - A metadata query returning a list of IP:Port pairs
- **`command`** — any AnyLog command.

**Examples:**
```anylog
run client 10.0.0.78:20348 get status
run client (139.162.126.241:2048, 172.105.13.202:2048) get processes
run client (!operator1_ip !operator1_port, !operator2_ip !operator2_port) get operator
```

Queries don't require an explicit destination — the network protocol resolves it:
```anylog
run client () sql my_dbms "select count(*) from my_table"
```

Destination can also be a metadata query, e.g. returning CPU usage from all US-based Operators:
```anylog
run client (blockchain get operator where [country] contains US bring [operator][ip] : [operator][port] separator = ,) get cpu usage
```

See: [Queries and Info Requests to the AnyLog Network](../06- Data Management/B- Query & Aggregations/Queries.md#query-nodes-in-the-network).

---

## Querying and Updating Metadata in the Blockchain

The network's global metadata — stored in a blockchain or a Master Node — can be queried and updated (regardless of 
platform) using the **blockchain commands**.

See: [Blockchain Commands](../12- Commands & CLI/A- Command Categories/Blockchain Commands.md).

---

## High Availability (HA)

Nodes can be configured to dynamically and transparently replicate hosted data across multiple copies. If a node fails, 
queries are redirected to a surviving node, and a replacement node can be assigned.

See: [High Availability](../04- Core Concepts/High Availability.md#high-availability-ha).

---

## Network Security

Several mechanisms secure network data:
* **Node authentication** — each node has a private/public key pair; the public key identifies the node, the private key signs outgoing messages, letting receivers authenticate the sender and evaluate permissions.
* **User authentication** — users can be assigned private/public keys and treated like a node for authentication purposes.
* **Basic authentication** — nodes maintain a username/password list and validate incoming commands against it.
* **Certificates** — the network can issue certificates to clients and servers, enabling SSL with client/server certificate authentication.
* **Encryption** — messages between nodes can be encrypted.

See: [User Authentication](../05- Networking & Security/Authentication.md).

---

## Open Items — Link Audit

The following references from the source documents don't yet have a confirmed home in the numbered doc tree. Resolve 
before treating this page as final:

1. **Master Node setup page** — no dedicated numeric doc found. Candidates: `03- Installation & Deployment/A- Deployment Options/Node Configuration.md` or `Deploying a Node.md`.
2. **"Using EdgeX" link** — ambiguous between `03- Installation & Deployment/C- Cloud & Edge Deployments/EdgeX Foundry Integration.md` and `07- Connectors & Integrations/B- Southbound Interfaces/Using MQTT (EdgeX).md`.
3. **"Starting an AnyLog Instance"** — content only exists in `ORPHANS/x01-getting-started/starting an anylog instance.md`; no numeric equivalent. Either merge into `Quick Deployment Guide.md` or create a new numbered page.
4. **"Metadata Requests" link** — old target (`04- Core Concepts/A- Agent Services/ZZZ metadata requests.md`) carries a `ZZZ` prefix, which elsewhere in this repo marks draft/deprecated content. Confirm status before linking.