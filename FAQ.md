# FAQ 

## General Questions 

1. **What is AnyLog?** 

AnyLog is a network of agents that lets you manage real-time and IoT data directly at the edge. Instead of relying on a 
centralized, cloud-based data lake, AnyLog transforms edge nodes into a distributed data lake with cloud-level 
capabilities. 

2. **What is EdgeLake?** 

EdgeLake is the open-source version of AnyLog. It provides the core components allowing users to manage their data at 
the edge, but does not include features like security and high-availability. 

3. Is **it possible to migrate from EdgeLake to AnyLog or AnyLog to EdgeLake?** 

Yes. Since AnyLog is built on top of EdgeLake switching from EdgeLake to AnyLog is done near seamlessly.  

Users simply need to update their desired docker image and get an [AnyLog license](https://anylog.network/download). 

4. **Where can AnyLog/EdgeLake run?** 

AnyLog / EdgeLake is predominantly deployed as a container-based solution, which allows it to run  locally on the user 
machine, on-premises, edge and cloud.

5. **Where can I find more information on EdgeLake?** 

EdgeLake is an open-source software that's part of the [Linux Foundation Edge Group](https://lfedge.org/projects/edgelake/). 
You can learn more about EdgeLake and try it on its [GitHub](https://github.com/EdgeLake)

6. **How can I try AnyLog?** 

Please visit our [Download Page](https://anylog.network/download) to download and try AnyLog

7. **How can I reach the AnyLog Team?**
   * Email us at [support@anylog.network](mailto:support@anylog.network)
   * Join [EdgeLake Slack](SLACK DOWN - NEED LINK)

## Architecture

8. **What are the types of AnyLog / EdgeLake nodes and what are they used for?** 

AnyLog has 4 major types of nodes:

| Node Type     | Role                                                                                      |
| ------------- | ----------------------------------------------------------------------------------------- |
| **Operator**  | Hosts the data and executes queries.                                                      |
| **Query**     | Orchestrates and manages the query process.                                               |
| **Master**    | Hosts metadata on a ledger and provides metadata services to peer nodes in the network.   |
| **Publisher** | Receives data from sources (e.g., devices, applications) and distributes it to Operators. |

Note: The Publisher node is only available in AnyLog and is not part of the EdgeLake deployment.

9. **Are the nodes different programs? Can a user run multiple nodes / agents on the same device?** 

The source code is the same for all node types, regardless of the configuration. AnyLog / EdgeLake follows a 
service-based architecture, which means multiple node types can run on the same machine—or even within the same container—
based on user-defined configurations.

The only exception is that Operator and Publisher services can run on the same machine but must be deployed in separate
containers.

10. **What does it mean "service-based"?** 

AnyLog uses a microservice based approach, where core functionalities, such as storage, query execution and transactions, 
are separated into independent services.

Instead of running a monolithic system, users interact only with the services they need. 

11. **What are the benefits of a service-based architecture in AnyLog?**  

AnyLog's service-based architecture allows for greater flexibility and scalability based on the needs of the user 
individual user and overall network. 

In addition, third-party applications can interact with the network via API calls without needing to know where the 
data resides. 


## High-Availability & Data Management

12. What's AnyLog's High Availability?

To achieve [highly availability](high_availability.md) (HA), AnyLog nodes are configured such that multiple _Operators_ 
maintain copies of the data. Using this setup, if an _Operator_ fails, the data is available on surviving Operator(s) 
and queries are directed to the surviving node. AnyLog's HA is done in a horizontal fashion, as opposed to a leaner, 
allowing limit-less number

13. **How does High-Availability work?**

AnyLog’s High Availability (HA) process has two key components:
* Cluster Policy logic for operator node connectivity 
* Data assertion to ensure replication without duplication

14. What are Clusters and why are they important? 

_Cluster_ are logical blockchain policies used to manage groups of operator nodes. 

An operator node must be associated with a cluster in order to for its service to be initiated. Each Cluster policy 
could have one or multiple Operator nodes associated with it, and based on the cluster ID operator nodes know who to 
share their data with.


15. What happens is an Operator node fails? 

There are 2 types of operator nodes - a node that's receiving the data from the device and a node that's just keeping a 
copy of the data. 

By default, if an Operator nodes fails, the system would automatically redirect queries to other operators in the same 
cluster.

That said... If the operator node that's receiving data from devices is the one that fails, then users would only be 
able to view historical data, until the data-generator is reconfigured to send data **or** the origianl operator comes 
back.

16. What happens if a full cluster group fails? 

In enterprise or edge-based deployments, network connectivity isn’t always guaranteed (e.g., in mining or remote 
operations). To address this, AnyLog’s cluster-based HA logic ensures data is replicated across multiple operator nodes.

To further mitigate potential network issues, we recommend that operator nodes within the same cluster reside on 
separate network segments. This way, if one segment experiences a failure, the other nodes remain accessible and 
maintain data availability.

17. How often does data get copied between operators? 

The operator sharing the data distributes new data across other operators in the cluster every few minutes. 
This guarantees close-to continuous data consistency across the operators in the cluster and strong eventual 
consistency.

18. How does AnyLog guarantee replication without duplication? 

Each operator node keeps a record of its own data and the data it had received from other operators.

This record is then used to guarantee removal of duplication  and that data has been transferred between nodes. 

19. What can I do with the replication metadata? 

Yes - The metadata information guaranteeing replication without duplication is accessible on a logical database called 
`almgm`. Users can utilize it to validate consensus between the data and the node, as well as across the nodes in the 
same clusters.

20. Are there any other details about High Availability I should know? 

Yes - A cluster (and its associated operator nodes(s)) may have 1 or more tables associated with it. Multiple cluster 
groups can share the same logical database.table, and in such a case queries executed on the network would return 
results from multiple sources (cluster groups) containing the relevant information.

## Security 

## Blockchain Layer 

