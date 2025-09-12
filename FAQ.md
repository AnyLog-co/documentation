# FAQ 

## General Questions 

* **What is AnyLog?** 

AnyLog is a network of agents that lets you manage real-time and IoT data directly at the edge. Instead of relying on a 
centralized, cloud-based data lake, AnyLog transforms edge nodes into a distributed data lake with cloud-level 
capabilities. 

* **What is EdgeLake?** 

EdgeLake is the open-source version of AnyLog. It provides the core components allowing users to manage their data at 
the edge, but does not include features like security and high-availability. 

* Is **it possible to migrate from EdgeLake to AnyLog or AnyLog to EdgeLake?** 

Yes. Since AnyLog is built on top of EdgeLake switching from EdgeLake to AnyLog is done near seamlessly.  

Users simply need to update their desired docker image and get an [AnyLog license](https://anylog.network/download). 

* Is AnyLog/EdgeLake open-source?

EdgeLake is 100% free and open-source, while AnyLog is a license-based program. 

Users can get a 90-day trail of [AnyLog license](https://anylog.network/download) to try. 


* **Where can AnyLog/EdgeLake run?** 

AnyLog / EdgeLake is predominantly deployed as a container-based solution, which allows it to run  locally on the user 
machine, on-premises, edge and cloud.

* **Where can I find more information on EdgeLake?** 

EdgeLake is an open-source software that's part of the [Linux Foundation Edge Group](https://lfedge.org/projects/edgelake/). 
You can learn more about EdgeLake and try it on its [GitHub](https://github.com/EdgeLake)

* What are the system requirements for AnyLog/EdgeLake?

In general, AnyLog / EdgeLake image has a footprint of about 100MB and supported on both arm and am64. 
However, a dockorized image is about 700MB due to the associated requirements. Please viti [Prerequisite](prerequisite.md) to get 
for farther details 



* **How can I try AnyLog?** 

Please visit our [Download Page](https://anylog.network/download) to download and try AnyLog

* **How can I reach the AnyLog Team?**
   * Email us at [support@anylog.network](mailto:support@anylog.network)
   * Join [EdgeLake Slack](SLACK DOWN - NEED LINK)

## Architecture

* **What are the types of AnyLog / EdgeLake nodes and what are they used for?** 

AnyLog has 4 major types of nodes:

| Node Type     | Role                                                                                      |
| ------------- | ----------------------------------------------------------------------------------------- |
| **Operator**  | Hosts the data and executes queries.                                                      |
| **Query**     | Orchestrates and manages the query process.                                               |
| **Master**    | Hosts metadata on a ledger and provides metadata services to peer nodes in the network.   |
| **Publisher** | Receives data from sources (e.g., devices, applications) and distributes it to Operators. |

Note: The Publisher node is only available in AnyLog and is not part of the EdgeLake deployment.

* What are the differences between different node types? 

A node type is defined by 2 things: 
* the services enabled
* the logical database connected 

| Node Type |                  Services                  | Database | 
| :---: |:------------------------------------------:| :---: | 
| Master |                                            | blockchain logical database + ledger table | 
| Query |                                            | system_query logical database | 
| Operator | Consumer, Distributor and Operator Service | user-defined database and almgm | 
| Publisher | Distributor and Publisher service | | 


* **Are the nodes different programs? Can a user run multiple nodes / agents on the same device?** 

The source code is the same for all node types, regardless of the configuration. AnyLog / EdgeLake follows a 
service-based architecture, which means multiple node types can run on the same machine—or even within the same container—
based on user-defined configurations.

The only exception is that Operator and Publisher services can run on the same machine but must be deployed in separate
containers.

* Can multiple node types run on the same machine?

Yes. AnyLog / EdgeLake multiple agents can can run on the same machine. 

In fact, since AnyLog/EdgeLake is a service based, users can enable multiple databases and services on the same agent 
creating a single container that can act as multiple node types.

* Can nodes be dynamically reconfigured?

Yes. Because AnyLog is service-based, a node’s services can be enabled or disabled as needed.

Caveat: For Operator nodes that are part of a cluster, data (files) and query requests will continue to flow according 
to the cluster’s policies. This means that while you can reconfigure services, the node’s role within the cluster will 
still affect how it handles data and queries.

* Can nodes be moved to another machine or network location?

Yes, but with some considerations.

Data can be migrated from one machine to another using high-availability or tvia REST calls. 

One of our key requirements is a static IP address, and that's required in the blockchain policy. 
If the IP cannot be static, we highly recommend using something like Nebula (built-in) or another VPN tool to assert 
consistent connection information (we also support nic types). If the IP does change, then the associated blockchain 
policy must be updated.

* **What does it mean "service-based"?** 

AnyLog uses a microservice based approach, where core functionalities, such as storage, query execution and transactions, 
are separated into independent services.

Instead of running a monolithic system, users interact only with the services they need. 

* **What are the benefits of a service-based architecture in AnyLog?**  

AnyLog's service-based architecture allows for greater flexibility and scalability based on the needs of the user 
individual user and overall network. 

In addition, third-party applications can interact with the network via API calls without needing to know where the 
data resides. 

* Which programming languages or APIs are supported?

AnyLog and EdgeLake provide a REST-based API, allowing users to interact with nodes, execute queries, and integrate 
with third-party applications. No special programming language is required—any language that can make HTTP requests can 
communicate with the API.

* What is the ideal network setup? Why? 

Our base network setup consists of 2 operator nodes each residing on a different cluster, associated with it are a 
query node and master node if you do not want to use a blockchain. 

Each operator should reside on its own machine, and the master and query could reside on either their own machine or 
with one of the other operator node(s). 

This basic setup allows users to easily see AnyLog's distributed system using a relatively small network. This network 
can then easily be grown horizontally via more operators against same cluster or vertical, with more operators on
different clusters. 

## High-Availability & Data Management

* What's AnyLog's High Availability?

To achieve [highly availability](high_availability.md) (HA), AnyLog nodes are configured such that multiple _Operators_ 
maintain copies of the data. Using this setup, if an _Operator_ fails, the data is available on surviving Operator(s) 
and queries are directed to the surviving node. AnyLog's HA is done in a horizontal fashion, as opposed to a leaner, 
allowing limit-less number

* **How does High-Availability work?**

AnyLog’s High Availability (HA) process has two key components:
* Cluster Policy logic for operator node connectivity 
* Data assertion to ensure replication without duplication

* What are Clusters and why are they important? 

Cluster_ are logical blockchain policies used to manage groups of operator nodes. 

An operator node must be associated with a cluster in order to for its service to be initiated. Each Cluster policy 
could have one or multiple Operator nodes associated with it, and based on the cluster ID operator nodes know who to 
share their data with.


* What happens is an Operator node fails? 

There are 2 types of operator nodes - a node that's receiving the data from the device and a node that's just keeping a 
copy of the data. 

By default, if an Operator nodes fails, the system would automatically redirect queries to other operators in the same 
cluster.

That said... If the operator node that's receiving data from devices is the one that fails, then users would only be 
able to view historical data, until the data-generator is reconfigured to send data **or** the origianl operator comes 
back.

* What happens if a full cluster group fails? 

In enterprise or edge-based deployments, network connectivity isn’t always guaranteed (e.g., in mining or remote 
operations). To address this, AnyLog’s cluster-based HA logic ensures data is replicated across multiple operator nodes.

To further mitigate potential network issues, we recommend that operator nodes within the same cluster reside on 
separate network segments. This way, if one segment experiences a failure, the other nodes remain accessible and 
maintain data availability.

* How does AnyLog handle network partitions or split-brain scenarios?

**Bidirectional Operators** – All Operators can send and receive data, so replication and query handling continue even 
if some nodes are disconnected.

**Leader failover** – If the main Operator fails, a new main is automatically selected from the remaining Operators, 
based on a cluster's internal rules. This ensures continuous operation and prevents split-brain issues.


* How often does data get copied between operators? 

The operator sharing the data distributes new data across other operators in the cluster every few minutes. 
This guarantees close-to continuous data consistency across the operators in the cluster and strong eventual 
consistency.

* Can I manually trigger replication or resync between nodes?

Currently the answer is no, but it is something we plean to implement in the near future. 


* How does AnyLog guarantee replication without duplication? 

Each operator node keeps a record of its own data and the data it had received from other operators.

This record is then used to guarantee removal of duplication  and that data has been transferred between nodes. 

* What can I do with the replication metadata? 

Yes - The metadata information guaranteeing replication without duplication is accessible on a logical database called 
`almgm`. Users can utilize it to validate consensus between the data and the node, as well as across the nodes in the 
same clusters.

* What is the consistency model?


* Are there any other details about High Availability I should know? 

Yes. A cluster (and its associated operator nodes(s)) may have 1 or more tables associated with it. Multiple cluster 
groups can share the same logical database.table, and in such a case queries executed on the network would return 
results from multiple sources (cluster groups) containing the relevant information.

## Security 

* How is data encrypted at rest and in transit?

* How are user permissions managed?

* Is there audit logging for node activity?

* Can third-party applications access data securely?
Yes.  

## Blockchain Layer 
* What's the difference between metadata and blockchain? 

The blockchain is a platform to manage immutable data, ie data that cannot be changed. 
 
Metadata (policies) is the data residing on the blockchain. In the case of AnyLog, that would be things like cluster and 
node information, model locations and inferences (for Federated Learning) and other infrastructure information the uses 
deems fit for the blockchain.

* What role does blockchain play in AnyLog?


* Which consensus mechanism is used?

* Can blockchain be disabled for private deployments?

Yes. If a user does not want to use a public blockchain he has 2 options. He can either use the master node, which is 
recommended for POCs and we plan to have a private blockchain option as well to use in the future.