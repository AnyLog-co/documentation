---
title: "Blockchain & Metadata"
description: "Why AnyLog uses a blockchain/ledger for metadata, core terminology, and where to find policy structure, commands, and connectivity setup."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon    | Split into 4 docs: this intro (concept only), Blockchain Policy, Blockchain Commands, and a new standalone Blockchain Connectivity doc. Removed duplicate content that had been pasted in twice. Fixed the "blockchain as a service" dead link to point at the new standalone doc. | |
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-04-25 |                | Created document | |
--->

# Blockchain & Metadata

The idea of the _blockchain_ is probably one of the most innovative things in modern technology due to its immutability
mechanism. At the core, AnyLog is a series of nodes that share data — from sensors and devices — among themselves in order
to remove the need for centralization and provide real-time insight.

The reason we use the blockchain is simply because it's able to provide a way for untrusting groups
(e.g. a factory-line component manufacturer and the factory owner) to see the same data without needing to move it around,
with the blockchain acting as a guarantee of what each can actually see, and that it has not been manipulated or 
tampered with.

Additionally, when growing the network out to the idea of blockchain as a service individuals can become "personalized" 
cloud providers, while the data owners can still offload their data to untrusted machine(s) - think of _Storj_ or 
_Filecoin_.

Finally, AnyLog agents of the network are aware they are a part of the network based on the `LEDGER_CONN` (`!ledger_conn`)
configuration and the metadata (i.e. `blockchain get`) they see.

Note that while nodes are able to see every other members in their shared network, via the blockchain, they may
not be granted access to all those nodes, as described in [security and permissions](../06-%20Networking%20&%20Security).

* [Blockchain Policy](./02-%20Policy%20&%20Metadata.md) — what a policy is, the core policy types, and how to structure one
* [Blockchain Commands](./03-%20Blockchain%20Commands.md) — full command reference for adding, querying, updating, and deleting policies
* [Blockchain Connectivity](./03-1%20Blockchain%20Full%20Circle.md) — setting up a Master/Metadata node or connecting to a real blockchain platform
* [Unified Namespace](05-%20Unitfied%20Namespace.md)

## Terminology

* **blockchain**: A decentralized, distributed ledger technology that securely records transactions across multiple
computers. It is designed to be immutable, meaning that once data is recorded, it cannot be altered without altering all
subsequent blocks, ensuring data integrity and security.
* **ledger**: The list of records residing on the blockchain.
* **metadata**: The policies stored on the blockchain (master, operator, cluster, and table definitions, among others)
that describe the structure and configuration of the network.
* **policy**: A JSON object with a single root key — the policy type — that represents one metadata record (a node,
a cluster, a table schema, a scheduled task, etc.). See [Blockchain Policy](02-%20Policy%20&%20Metadata.md) for the full
structure.
* **ledger_conn**: AnyLog's configuration variable specifying which ledger the node syncs against.
* **master node** or **metadata node**: a proprietary alternative to an actual blockchain, that acts as a blockchain
emulator to store the metadata. See [Blockchain Connectivity](04-%20Mapping%20Policy.md) for setup.