---
title: "Policy & Metadata"
description: "Explain policies"
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**       | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-27 | Ori Shadmon    | created document | 2025 |
 | 2026-08-29 | Moshe Shadmon    | updated document | 2025 |
--->

# Metadata

AnyLog metadata describes the resources, configuration, data organization, services, and relationships that make up an AnyLog network. Examples include node definitions, clusters, tables supported by the network, mapping rules, permissions, configuration settings, and Unified Namespace (UNS) definitions.

The metadata is maintained in a **ledger**, which can be managed by either a blockchain or an AnyLog Master Node (blockchain emulator). Regardless of which backend is used, AnyLog uses the same APIs and metadata model.

Metadata is organized as a collection of JSON objects called **policies**. Policies usually have a single attribute at the root. **The root attribute determines the Policy Type.**

For example:

~~~json
{
  "cluster": {
    "company": "Bachelor Controls 2.0",
    "name": "cluster1",
    "id": "06f093559c851c6d4c3e950ebc9c5499",
    "status": "active",
    "ledger": "global"
  }
}
~~~

In this example, `cluster` is the root attribute and therefore identifies this as a `cluster` policy. The object associated with `cluster` contains the attributes describing that cluster.

AnyLog provides APIs to **add, update, and delete policies**, together with a rich set of query commands for retrieving and discovering policies based on their types, attributes, values, and relationships.

This makes the metadata more than configuration storage. It acts as a directory describing the distributed environment — what resources exist, how they relate to one another, and where data and services can be found.

## Policy vs. Metadata

**Metadata** and **policy** describe the same information at different levels.

- **Metadata** refers collectively to the information AnyLog maintains about the network.
- A **policy** is an individual JSON record representing one piece of that metadata.

For example, a `cluster` policy may define a logical group of operator nodes, while an `operator` policy identifies a particular node and references the cluster to which it belongs:

~~~json
{
  "cluster": {
    "company": "Bachelor Controls 2.0",
    "name": "cluster1",
    "id": "06f093559c851c6d4c3e950ebc9c5499",
    "date": "2026-07-20T18:40:12.114402Z",
    "status": "active",
    "ledger": "global"
  }
},
{
  "operator": {
    "name": "bachelor-operator1",
    "company": "Bachelor Controls 2.0",
    "hostname": "node3",
    "ip": "172.233.208.212",
    "port": 32148,
    "rest_port": 32149,
    "broker_port": 32150,
    "loc": "41.8500,-87.6500",
    "country": "US",
    "state": "Illinois",
    "city": "Chicago",
    "cluster": "06f093559c851c6d4c3e950ebc9c5499",
    "id": "c7df327826839d64ff23f5f9b52ebf1b",
    "date": "2026-07-20T18:38:31.925781Z",
    "ledger": "global"
  }
}
~~~

Each JSON object is an individual policy (`cluster` and `operator`). The `cluster` attribute in the `operator` policy references the `id` of the cluster policy, creating a relationship between the two objects.

Together with the other policies known to the node — tables, mappings, configurations, permissions, UNS definitions, and others — these policies collectively represent the network's metadata.

There is no separate metadata representation into which policies are converted. **Policies are the metadata records themselves.**

## Metadata Storage

When a blockchain is used, the shared metadata is **hosted on the blockchain**. Each AnyLog node synchronizes the metadata from the blockchain and maintains a **local copy in a file**. This allows each node to access and query the network metadata locally while the blockchain provides the authoritative shared version.

When a **Master Node** is used instead of a blockchain, the Master Node acts as the blockchain emulator and hosts the authoritative metadata in a **local database**. Other AnyLog nodes synchronize the metadata from the Master Node in the same way they would synchronize it from a blockchain and maintain their local metadata copy in a file.

Therefore, from the perspective of an AnyLog node, the synchronization model is the same:

**Blockchain or Master Node → metadata synchronization → local metadata file on each node**

Because the blockchain and Master Node support the same metadata APIs and policy model, nodes can operate with either backend without changing how they manage or query metadata.

> **Note:** Only metadata is synchronized in this way. Operational data — including sensor, device, historian, database, and application data — remains distributed across the systems and AnyLog nodes where it is managed.

## Policy Types

AnyLog generates a set of standard policy types required to support network operations. These policies describe the resources and configuration that allow the distributed network to operate and make its data discoverable.

Common policy types include:

- `config` — defines how a node is configured and which services it should run.
- `cluster` — defines logical groups of operator nodes and helps identify where distributed data resides.
- **Node policies**, such as `operator` — describe nodes, the services they provide, and how they can be reached.
- `table` — describes the **tables supported by the network**, including the logical database, table name, and table schema. Table policies allow nodes to discover which tables are available and provide a common definition for accessing distributed data using the same logical table across multiple nodes.
- **Mapping policies** — define how incoming data is transformed and mapped into the target data structure.
- **UNS policies** — define logical Unified Namespace hierarchies over distributed operational data.
- **Permission and security policies** — define access and authorization information used by the network.

Some of these policies are created automatically by AnyLog as nodes, tables, and other resources are introduced into the network. Others are explicitly created by users or administrators.

### User-Defined Policies

Users are not limited to the policy types generated and used internally by AnyLog. **Users can define and publish their own policy types** to represent metadata that is relevant to their applications and operational environment.

For example, user-defined policies can describe equipment, sensors, processes, applications, organizational structures, asset relationships, or other domain-specific information.

Once a policy is published to the shared metadata, it becomes available to the members of the AnyLog network and is synchronized across the participating edge nodes.

In this sense, the metadata layer serves two complementary purposes:

- **A single source of truth for shared metadata** — providing a common and consistent view of the network, its resources, supported tables, and user-defined information.
- **A metadata synchronization mechanism** — distributing policies across the network so that participating edge nodes maintain a consistent local view of the metadata.

The operational data itself remains distributed. It is the **metadata describing the data, resources, relationships, and network configuration that is synchronized across the network**.