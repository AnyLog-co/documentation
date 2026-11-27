---
title: "AnyLog Quick Start"
description: "Quick command reference for configuring, joining, testing, and working with an AnyLog network."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**        | **Change**        | **Version** |
 |----------|-----------------|-------------------|-------------|
 | 2026-08-29 | Moshe Shadmon | created document  | 2026 |
--->
# AnyLog Quick Start

This page provides a quick command reference for working with a running AnyLog node and connecting it to an existing AnyLog network.

It is intended as a starting point for technical users. For detailed command options and configuration, follow the links to the corresponding documentation sections.

---

## CLI Help

The AnyLog CLI provides built-in help for commands and command groups.

List available commands:

~~~anylog
help
~~~

Search a command family:

~~~anylog
help blockchain
~~~

Get help for a specific command:

~~~anylog
help blockchain get
~~~

or:

~~~anylog
help blockchain insert
~~~

Commands can also be searched by category using the help index:

~~~anylog
help index
~~~

For example:

~~~anylog
help index streaming
~~~

The command help includes syntax, descriptions, examples, and links to the corresponding documentation.

---

## Check the Node

After starting an AnyLog node, verify that the expected services are running.

### View Active Processes

~~~anylog
get processes
~~~

This displays the background services currently running on the node.

### Test the Node

~~~anylog
test node
~~~

This tests the node's basic configuration and reports detected issues.

### Test the Network

~~~anylog
test network
~~~

This tests connectivity to network members known to the node.

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

Reference the value using `!`:

~~~anylog
get !data_dir
~~~

Dictionary variables can be used in other commands:

~~~anylog
set backup_dir = !data_dir/backup
~~~

To view the complete dictionary:

~~~anylog
get dictionary
~~~

To search the dictionary for keys containing a particular string:

~~~anylog
get dictionary _dir
~~~

This is useful when looking for configuration values such as directories without knowing the exact key name.

### Environment Variables

Environment variables are referenced using `$`.

For example:

~~~anylog
get $HOME
~~~

Environment variables can also be set directly from the AnyLog CLI:

~~~anylog
set $ANYLOG_SITE = plant_1
~~~

Retrieve the value using:

~~~anylog
get $ANYLOG_SITE
~~~

Both dictionary and environment variables can be used in AnyLog commands and configuration scripts.

---

## Find the Node Directories

AnyLog uses a set of working directories for data ingestion, processing, storage, distribution, security, and error handling.

A quick way to find the configured directories is:

~~~anylog
get dictionary _dir
~~~

Common directories include:

- `archive` — stores archived data files after they have been processed.
- `bkup` — stores backup copies of files.
- `blobs` — stores binary or large-object data managed separately from structured table data.
- `bwatch` — watch directory for incoming blob data.
- `dbms` — stores local database files when file-based databases such as SQLite are used.
- `distr` — stores files waiting to be distributed or replicated to other Operator nodes.
- `error` — stores files that could not be successfully processed.
- `pem` — stores certificates and keys used for secure communication and authentication.
- `prep` — stores data that has been prepared for the next stage of processing.
- `test` — workspace used for testing.
- `tmp` — stores temporary files created during processing.
- `watch` — watch directory for incoming data waiting to be processed.

When a node is initialized for the first time, create the configured AnyLog work directories using:
~~~anylog
create work directories
~~~
This command only needs to be run **once when the node is first initialized**. It creates the directory structure used by the node for data ingestion, processing, storage, distribution, backups, and other operations.

The directories can be reviewed using:

~~~anylog
get dictionary _dir
~~~
---

## Join an Existing Network

The `seed from` command provides a simple way to associate a node with an existing AnyLog network.

Instead of manually configuring all the information required to discover the network, a new node can contact an existing AnyLog node and use it as a **seed** for obtaining the network information.

For example:

~~~anylog
seed from 10.0.0.20:2048
~~~

The specified IP address and port identify an AnyLog node that is already a member of the target network.

The seed process allows the new node to obtain the information needed to connect to the network and its shared metadata.

Conceptually:

~~~text
             New AnyLog Node
                    │
                    │ seed from
                    ▼
          Existing AnyLog Node
                    │
                    │ network information
                    ▼
             New AnyLog Node
                    │
                    ▼
           Shared AnyLog Network
~~~

After the node is associated with the network, the node maintains its local metadata copy.

The seed node is therefore used to **discover and join the network**; it does not become a permanent dependency for normal node operation.

After seeding the node, verify the network and metadata:

~~~anylog
test network
~~~

---

## View Network Metadata

Each AnyLog node maintains a synchronized local copy of the network metadata.

View all metadata policies:

~~~anylog
blockchain get *
~~~

View Operator policies:

~~~anylog
blockchain get operator
~~~

View cluster policies:

~~~anylog
blockchain get cluster
~~~

View table policies:

~~~anylog
blockchain get table
~~~

Policies can be filtered by their attributes.

For example:

~~~anylog
blockchain get operator where company = AnyLog
~~~

AnyLog provides a rich set of options for querying policies, including filtering, selecting attributes, and traversing relationships.

See [Blockchain Commands](/docs/08-blockchain-and-metadata/03-blockchain-commands/) for the complete metadata command reference.

---

## Check the Logs

AnyLog maintains dynamic logs that can be inspected from the CLI.

View the event log:

~~~anylog
get event log
~~~

View errors:

~~~anylog
get error log
~~~

View SQL query activity:

~~~anylog
get query log
~~~

Logs can also be reset:

~~~anylog
reset event log
reset error log
reset query log
~~~

These commands are useful when validating configuration, ingestion, network communication, and queries.

---

## Run Commands as a Client to the Network

The `run client` command executes a request with the current AnyLog node acting as a **client to the AnyLog network**.

The destination determines how the request is routed. A client request can be directed to a specific AnyLog node, to multiple nodes, or — for commands such as distributed SQL — resolved dynamically using the network metadata.

To run a command on a specific node:

~~~anylog
run client 10.0.0.78:20348 get processes
~~~

To run the same command on multiple nodes:

~~~anylog
run client (10.0.0.78:20348, 10.0.0.79:20348) get processes
~~~

For distributed SQL, the destination can be left empty:

~~~anylog
run client () sql plant_data format = table and stat = select timestamp, temperature from sensors
~~~

In this case, AnyLog uses the metadata to determine which nodes in the network should process the request.

## Query Distributed Data

Distributed SQL queries are also issued using `run client`.

In this case, the destination can be left empty:

~~~anylog
run client () sql plant_data format = table and stat = select timestamp, temperature from sensors
~~~

The empty destination `()` instructs AnyLog to use the metadata to determine where the requested data resides.

AnyLog:

1. Identifies the clusters that maintain the requested table.
2. Identifies the Operators assigned to those clusters.
3. Routes the query to the appropriate Operators.
4. Executes the query against the local data on those Operators.
5. Aggregates the replies.
6. Returns a unified result.

The user therefore queries the logical table without needing to know where its physical data is located.

See [SQL Commands](/docs/07-cli/04-sql/) for SQL syntax, distributed query options, output formats, and examples.

---

## Switch Metadata Networks

A running node can change the Master Node used for metadata synchronization.

For example:

~~~anylog
blockchain switch network where master = 10.0.0.21:2048
~~~

This changes the metadata source used by the node's synchronization process.

This is different from `seed from`:

- `seed from` is used to **discover and associate a node with an existing network**.
- `blockchain switch network` changes the **metadata network used by an already configured node**.

---

## Useful First Commands

The following commands provide a quick overview of a running node and its network:

~~~anylog
get processes
test node
test network
get dictionary
get dictionary _dir
blockchain get *
get event log
get error log
~~~

For a node that needs to join an existing network:

~~~anylog
seed from <ip>:<port>
~~~

To run a command remotely:

~~~anylog
run client <ip>:<port> <command>
~~~

To execute a distributed SQL query:

~~~anylog
run client () sql <dbms> format = table and stat = <SQL statement>
~~~

---

## Exit the Node

To stop and exit the AnyLog node:

~~~anylog
exit node
~~~

---

## Where to Go Next

After becoming familiar with the basic CLI and network commands, use the detailed documentation for the area you are configuring:

| Topic | What it covers |
| --- | --- |
| **Installation & Deployment** | Installing and starting AnyLog nodes. |
| **Node Configuration** | Configuring services, networking, databases, directories, and node roles. |
| **Data Ingestion & Mapping** | Connecting operational data sources and mapping incoming data. |
| **SQL Commands** | Local and distributed SQL queries. |
| **Blockchain & Metadata** | Policies, metadata synchronization, Master Node configuration, and metadata commands. |
| **Unified Namespace** | Logical asset hierarchies over distributed operational data. |
| **Networking & Security** | Node communication, authentication, permissions, and secure connectivity. |
| **High Availability** | Clusters, Operator replication, and failover. |

For most technical users, the initial workflow is:

~~~text
Start Node
    │
    ▼
Check Processes and Configuration
    │
    ▼
Seed / Join the Network
    │
    ▼
Synchronize and Inspect Metadata
    │
    ▼
Test Network Connectivity
    │
    ▼
Ingest Data
    │
    ▼
Run Distributed Queries
~~~