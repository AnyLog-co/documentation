---
title: "Blockchain"
description: "Metadata Overview"
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon    | created document | 2025 |
 | 2026-08-29 | Moshe Shadmon    | updated document | 2025 |
--->

# Blockchain & Metadata

AnyLog uses a **shared metadata layer** to describe and coordinate the distributed network. This metadata defines what exists across the network and how it operates — including nodes, clusters, data locations and schemas, permissions, services, Unified Namespace (UNS) definitions, and other configuration information.

The metadata is organized as **policies**. A policy is a JSON document representing a specific metadata object or configuration. Different policy types describe different aspects of the network, such as an operator, cluster, data source, table, permission, or UNS object.

AnyLog provides a common API for managing this metadata. Applications and AnyLog nodes can **add, update, and delete policies**, as well as use a rich set of **query commands** to discover and retrieve policies based on their type, attributes, relationships, and other conditions. This allows the metadata layer to operate as a distributed directory describing the resources and capabilities available across the network.

## Blockchain and the Master Node

The metadata can be maintained using either a **blockchain** or an AnyLog **Master Node (blockchain emulator)**.

A blockchain provides a decentralized and immutable mechanism for maintaining metadata across organizations that may not fully trust one another. Participants can share a common view of the network configuration while retaining control over their individual data and systems.

However, many deployments do not require the complexity of a blockchain. For these environments, AnyLog provides the **Master Node**, which operates as a blockchain emulator. The Master Node maintains and distributes the same policy-based metadata while providing a simpler deployment model.

From the perspective of AnyLog nodes and applications, the two approaches are interchangeable. **The blockchain and Master Node expose the same AnyLog metadata APIs and policy model.** A deployment can therefore use a Master Node and later switch to a blockchain, or move from a blockchain to a Master Node, without changing the applications, policies, or commands used to manage and query the metadata.

Importantly, **the blockchain or Master Node does not store the operational data itself**. Sensor, device, historian, database, and application data remains distributed across the nodes and systems where it is managed. The metadata layer describes that distributed environment and allows AnyLog to determine where data and services are located, how they are organized, and how they can be accessed.

## Metadata Policies

Policies provide a consistent representation for all metadata maintained by AnyLog. Each policy is a JSON object with a single root key identifying the policy type and attributes describing that object.

Through the AnyLog metadata API, users and applications can:

- **Add policies** to register new metadata and resources.
- **Update policies** as network configuration or definitions change.
- **Delete policies** that are no longer applicable.
- **Query policies** using a rich set of commands and conditions to discover resources, retrieve configuration, traverse relationships, and identify where data or services are available.

Because the same policy model and APIs are supported by both the blockchain and the Master Node, the rest of AnyLog operates independently of which metadata backend is selected.

## Terminology

- **blockchain**: A decentralized and distributed ledger that can be used by AnyLog to maintain shared, immutable network metadata.
- **ledger**: The collection of metadata policies maintained by the blockchain or Master Node.
- **metadata**: Policies describing the structure, resources, configuration, data, services, permissions, and logical organization of an AnyLog network.
- **policy**: A JSON object with a single root key identifying the policy type and containing the attributes describing a metadata object or configuration.
- **Master Node / Metadata Node**: AnyLog's blockchain emulator. It maintains and distributes the same policy-based metadata and supports the same APIs as a blockchain, allowing deployments to switch between the two without changing how AnyLog nodes and applications interact with the metadata.