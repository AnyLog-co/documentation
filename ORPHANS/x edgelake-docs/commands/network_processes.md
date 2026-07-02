---
layout: default
title: Northbound Services
parent: Commands
nav_order: 5
---
# Interacting with the network

## Querying and issuing commands

Users and applications connect to the network by issuing queries and commands to a single node in the network. This node serves as a
gateway to the network.  
In the context of data query, the node that serves as a gateway is called a **Query Node**. 
Users and applications interacts with the node that serves as a gateway using the EdgeLake CLI or via REST.
* Every member node can serve as a gateway to the network.
* The EdgeLake CLI is available by default on each EdgeLake instance. Using the CLI, users can interact with the local node, 
a peer node or a group of nodes which are members of the network.
* To support calls from the Node's CLI, the TCP service needs to be enabled. Details are available [here](backgound_services.md#run-tcp-server).  
* A REST API can be enabled on each participating node by enabling the REST service. Details are available [here](backgound_services.md#enable-the-rest-service).
* Examples of REST calls to a network from Python, Postman, Grafana, Power BI, and Google tools are available
      [here](https://github.com/AnyLog-co/documentation/tree/master/northbound%20connectors).
* EdgeLake offers a Remote CLI application. This is a graphical web based interactive tool to issue queries and commands.
Details are available [here](../../northbound/remote_cli)
     
## Streaming data to the nodes in the network.

Some nodes in the network serve to host data. These nodes are called **Operator Nodes**.
Data is streamed to nodes in the network using a variety of methods summarized below ([Southbound Connectors](#southbound-connectors)).

# Query data and issue commands

Queries and commands issued to a node can be processed locally, or by peers (target nodes) in the network.  
When a SQL query is issued, the target nodes are determined dynamically and transparently by the database referenced 
in the query info and the table name in the SQL command. Alternatively users can specify the target nodes.  

The target nodes for commands (which are not SQL) are specified by the users and applications that issue the commands.     

Specifying the target nodes can be done by listing their IPs and Ports, or by a query to the metadata.  
Queries to the metadata can leverage domain info represented in the metadata policies. 
Example are: all nodes deployed in a region, and all nodes supporting machines from a specified vendor.    
Note that users can represent their domain knowledge in the metadata policies and leverage this info to identify target nodes.  
The EdgeLake Metadata APIs are open allowing to update and query metadata information as needed, and the metadata can be used to identify target nodes.

# Streaming data to the EdgeLake Network

Users stream their data into Operator Nodes. These nodes are configured to host the data and operate as follows:
* Data streams are identified by their source and their assigned logical database and table.
* The logical database identifies the physical database that hosts the table's data. 
  See details [here](data_management.md#associate-a-physical-database-to-a-logical-database).
* If the table exists (published as a policy on the shared metadata), the data will be hosted in the table.
* If the table doesn't exist, a schema is created based on the streaming data and published on the metadata.
* Optionally, users defile a **Mapping Policy** to instruct a schema and the mapping rules.
* Additional logic on the streaming data can be added by rules in one of the following manners:
    * Specifying rules in the **Mapping Policy**.
      Details are available in the [Mapping Data](https://github.com/AnyLog-co/documentation/blob/master/mapping%20data%20to%20tables.md#mapping-data) section.
    * Specifying rules with the node's **Rule Engine**.
      Details are available in the [Alerts and Monitoring](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring) section.
    

## Southbound connectors

A detailed description on how data is added to nodes in the network is available [here](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md).

Users can transfer data to nodes in the network using one of the following methods:

* [Using REST](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#data-transfer-using-a-rest-api)
* [Subscribing to a Nessaage Broker](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#subscribing-to-a-third-party-message-broker)
* [Configuring the EdgeLake node as a Message Broker](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#configuring-the-anylog-node-as-a-message-broker)
* [Using Kafka](https://github.com/AnyLog-co/documentation/blob/master/using%20kafka.md)
* [Using Syslog](https://github.com/AnyLog-co/documentation/blob/master/using%20syslog.md).
* [Using gRPC](https://github.com/AnyLog-co/documentation/blob/master/using%20grpc.md).
* [Using Node-Red](https://github.com/AnyLog-co/documentation/blob/master/node_red.md).



