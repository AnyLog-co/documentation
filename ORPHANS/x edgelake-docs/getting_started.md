---
layout: default
title: Getting Started
nav_order: 2
---

# Getting Started
  
This document provides the following:

* A high-level summary of the main functionalities supported by the EdgeLake Network.
* Install, configure, and deploy instructions.

Note: The EdgeLake software is derived from AnyLog. To provide additional info, some links reference the AnyLog documentation. 

## Table of Contents
- [The Member Nodes](#the-member-nodes)
- [The Network Metadata](#the-network-metadata)
- [The Users Data](#the-users-data)
- [EdgeLake Install](#edgelake-install)
- [Node's Directory Structure](#nodes-directory-structure)
- [Basic Operations](#basic-operations)
  - [Initiating and Configuring EdgeLake Instances](#initiating-and-configuring-edgelake-instances)
  - [The EdgeLake CLI](#the-edgelake-command-line-interface)
  - [The help Command](#the-help-command)
  - [The Local Dictionary](#the-local-dictionary)
  - [Retrieving Environment Variables](#retrieving-environment-variables)
  - [Retrieving the Services Status](#retrieving-the-services-status)
  - [The Dynamic Logs](#the-dynamic-logs)
- [Making a Node a Member of the Network](#making-a-node-a-member-of-the-network)
- [The Seed Command](#the-seed-command)
- [Dynamically Connecting to a Master Node](#dynamically-connecting-to-a-master-node)
- [Using the REST API to Issue EdgeLake Commands](#using-the-rest-api-to-issue-edgelake-commands)
- [Sending Messages to Peers in the Network](#sending-messages-to-peers-in-the-network)
- [Querying and Updating Metadata](#querying-and-updating-metadata-in-the-blockchain)


## About EdgeLake

EdgeLake is a decentralized network to manage IoT data. Nodes in the network are compute instances that execute the EdgeLake Software.    
Joining a network requires the following steps:  
1. Install the EdgeLake Software on a computer instance.
2. Configure the node to either join an existing network or create a new network, and enable the services provided by the node.

The EdgeLake Software is a stack of services to manage data and resources on each node. When a node starts, it enables
selected services. These services manage data ingestion, data storage, southbound and northbound connectors, queries, resource status and more.  

Some nodes are configured to host data. The database used is determined by the users.  
All the nodes share a metadata layer. for the metadata, users can choose between a blockchain platform or a master node. 

## The member nodes
A node in the network is assigned with one or more roles (summarized in the chart below):  

| Node Type     | Comment | Role  |
| ----------- | ------------|  -------------- | 
| Operator   | | A node that hosts the data and satisfies queries. |
| Query  | | A node that orchestrates a query process. |
| Master | Optional | A node that hosts the metadata and serves the metadata to the nodes in the network. |

Using a Master node is optional. A master node is used to maintain the global metadata when users do not enable the blockchain functionality.  
If the nodes in the network are associated with a blockchain (see more details below), the master node in not needed, and the network remains fully decentralized.  
Enabling the blockchain functionality using the Ethereum blockchain is explained in the 
[Using Ethereum as a Global Metadata Platform](https://github.com/AnyLog-co/documentation/blob/master/using%20ethereum.md) section.
Additional information on a Master Node configuration is available at the section: [Using a Master Node](https://github.com/AnyLog-co/documentation/blob/master/master%20node.md).

## The Network MetaData
The metadata is the network related information that is shared by members of the network.
The metadata includes information about the network members, their permissions, the logical representation of the data and how the data is distributed.  
The metadata is stored in a repository which is accessible to all the nodes in the network. The repository can be a blockchain or a master node and the type to use is determined in the configuration.  
The interaction with the metadata is not dependent on the repository used. When a member node operates, it is configured to use a particular metadata repository and
there are no operational differences which are dependent on the repository used.

**Note that the documentation (and the nodes processes) reference the blockchain for metadata operations regardless if 
the metadata is maintained in a blockchain platform or in a master node.**

It allows users to leverage one type of repository, and change to a different type without the need to make changes to their processes and logic.

The nodes in the network are configured to pull the metadata (from the blockchain platform, or the master node) periodically (using a backround service and if the metadata was changed) and update a local copy of the metadata on the node.  
When a node operates, it considers the local copy of the metadata and therefore, nodes processes are agnostic to the metadata platform used. If a connection 
to the metadata platform is lost, the node continues to operate based on the latest copy of the metadata that is maintained locally on the node.      
Synchronizing the local copy of the metadata is explained in the following section: [Blockchain Synchronizer](commands/backgound_services.md#enable-the-blockchain-synchronization-service).  

The metadata is organized as **policies**. Each policy is a JSON structure that is associated to a type (i.e. security, member, distribution).
The policies are updated in 2 ways:
* Dynamically, by the network protocol, for example, when a node joins the network.
* By users through APIs or with the EdgeLake CLI.
  
Applications and users can query the metadata. The metadata commands are detailed in the [metadata section](commands/metadata.md).

The metadata is shared by all the nodes of the network, and includes the following:
* Information utilized by the Network Members. 
* Data leveraged in conjunction with node services. For instance, 
  users can issue SQL queries to member nodes based on geographical location or request disk usage from nodes processing data from specific sensor types.
* Users can utilize metadata as a centralized repository for declaring policies to satisfy proprietry logic. As all nodes share this metadata, 
  EdgeLake instances ensure necessary metadata availability by distributing local policies across member nodes.  
  For example, users can leverage the metadata to represent **Device Shadow** (a virtual representation of the physical Sensor or Device).

## The Users Data
The users' data is distributed in local databases on the Operators Nodes. Operators can use different databases for different sets of data.  
Currently EdgeLake Operators can use the following databases:  
* [PostgresSQL](https://www.postgresql.org/) - recommended for larger nodes and deployments of large data sets.    
* [SQLite](https://www.sqlite.org/index.html) - recommended for gateways, smaller nodes and deployments of small or in-memory data sets.      
* [MongoDB](https://www.mongodb.com/) - recommended for unstructured data.

The data managed by the network is distributed to many nodes, but the network protocol provides a unified view over the distributed data -
the users or applications issuing the queries do not need to identify the nodes that host the relevant data - for each query, the network protocol 
resolves the location of the relevant data.   
Each query process starts with a node that receives a query from a user or application. This node is called the Query Node.
The Query Node determines which are the Operators that host the data that needs to be evaluated to satisfy the query, and delivers the query to these Operators.
These Operators process the query locally and retrurn a result set the Query Node. 
The Query Node aggregates all the results and returns a unified result to the user or application that issued the query.  

Related documentation:

| Section       | Information provided  |
| ------------- | ------------| 
| [Adding Data to Nodes in the Network](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#adding-data-to-nodes-in-the-network) | Delivering data to Operators in the network. |
| [Mapping Data](https://github.com/AnyLog-co/documentation/blob/master/mapping%20data%20to%20t) | Transformation of the source data to the destination format. |
| [Using a Message Broker](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#using-a-message-broker) | Delivering data to Operators using a MQTT broker. |
| [Queries to data](https://github.com/AnyLog-co/documentation/blob/master/queries.md#query-nodes-in-the-network) | Queries to data hosted by nodes in the network. |
| [Profiling and Monitoring Queries](https://github.com/AnyLog-co/documentation/blob/master/profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries) | Identifying and profiling slow queries. |
| [Using Grafana](https://github.com/AnyLog-co/documentation/blob/master/northbound%20connectors/using%20grafana.md#using-grafana) | Integrating Grafana to visualize data. |
| [Using Edgex](https://github.com/AnyLog-co/documentation/blob/master/using%20edgex.md#using-edgex) | Integrating with Edgex as a southbound connector. |
 
## EdgeLake Install

EdgeLake can be installed from Docker, Kubernetes or by downloading the codebase from GitHub and calling an installation script. 
Directions for deployment can be found [here](https://github.com/EdgeLake/docker-compose). 

An installation training session is available with the [Training Session Link](https://github.com/AnyLog-co/documentation/blob/master/training/Overview.md) 

## Node's directory structure

The EdgeLake directory setup is configurable. The default setup (used on docker deployment) is detailed below: 

<pre style="border: 2px ; border: none; overflow-x: auto;padding: 10px;"><code style="textcolor: black;">
<b>Directory Structure                 Explanation</b>
-------------------                 -----------------------------------------
/app                                [EdgeLake Root]
├── EdgeLake                        [Directory containing authentication keys and passwords]
│   ├── blockchain                  [A JSON file representing the metadata relevant to the node]
│   └── data                        [Users data and intermediate data processed by this node]
│       ├── archive                 [The root directory of and archival directory]
│       ├── bkup                    [Optional location for backup of user data]
│       ├── blobs                   [Directory containing unstructured data]
│       ├── dbms                    [Optional location for persistent database data. If using SQLite, used for persistent SQLIte data]
│       ├── distr                   [Directory used in the High Availability processes]
│       ├── error                   [The storage location for new data that failed database storage]
│       ├── pem                     [Directory containing keys and certificates]
│       ├── prep                    [Directory for system intermediate data]
│       ├── test                    [Directory location for output data of test queries]
│       ├── watch                   [Directory monitored by the system, data files placed in the directory are being processed]
│       └── bwatch                  [Directory monitored by the system, managing unstructured data]
├── deployment-scripts              [Directory consisting of scripts used to deploy & test EdgeLake]
│   ├── demo-scripts                [Directory consisting of examples for running different processes / services]
│   ├── grpc                        [Directory consisting of examples for compiling <i>gRPC</i> proto file and accepting data from KubeArmor]
│   ├── node-deployment             [Directory consisting of scripts that utilize user-defined configurations in order to deploy different node types]
│   │   ├── database                [Directory consisting of scripts to deploy database(s) based on configurations and node type]
│   │   └── policies                [Directory consisting of different policy definitions for both configurations and cluster / node policies]
│   ├── test-network-local-scripts  [Directory consisting of scripts used by AnyLog's demo / test network setup]
│   └── tests                       [Directory consisting of using test cases]
└── edgelake_v0.0.0_x86_64          [Compiled code of either EdgeLake or AnyLog. Namimg slightly changes based on version / CPU architecture]
</code></pre>

Notes: 
* The following command creates the work folders if they do not exist:
    <pre class="code-frame"><code class="language-anylog">create work directories</code></pre>
    
    The command needs to be issued only once on the physical or virtual machine.
    
* The following command list the directories on an EdgeLake node:
     <pre class="code-frame"><code class="language-anylog">get dictionary _dir</code></pre>

## Basic operations

### Initiating and Configuring EdgeLake Instances

EdgeLake can be deployed and initiated using Docker or Kubernetes or as a background process. The way the node operates depends on the configuration.  
EdgeLake can be configured in 4 ways:
* Using command line arguments when EdgeLake is called on the Operating System CLI (as a list of EdgeLake commands separated by the _and_ keyword).
* By issuing configuration commands on the CLI of an EdgeLake node.
* By calling a script file that lists the EdgeLake configuration commands (calling the command _process_ followed by the path to the script).
* By associating a Configuration Policy with the node. Configuration policies are hosted on the shared metadata layer. 


### The EdgeLake Command Line Interface

When a node starts, it provides the **EdgeLake Command Line Interface (CLI)**.    
The command line prompt appear as **EL >**, and it can be updated by issuing the following command on the CLI:
<pre class="code-frame"><code class="language-anylog">set node name [node name]</code></pre>

Using the CLI, a user can interact with the node or peer nodes in the network.  
A more detailed description of the EdgeLake CLI is available at [The EdgeLake CLI](https://github.com/AnyLog-co/documentation/blob/master/cli.md#the-anylog-cli) section. 

Users issue commands to retrieve and modify configuration, state of different processes, query and update the metadata and
issue SQL queries to data stored locally and data that is stored on other members of the network.    

Exiting and terminating an EdgeLake node is by issuing the command `exit node` on the CLI.

### The help command
The ***help*** command provides dynamic information on EdgeLake commands.  
The help command is issued on the CLI and can be used in multiple ways:

* List the commands by typing ***help*** on the CLI.
<pre class="code-frame"><code class="language-anylog">help</code></pre>
* List all commands that are assigned to a group. For example: the keyword ***get*** groups commands that retrieve information.
  These commands can be listed by typing ***help get***.   
  
Additional Examples:
 <pre class="code-frame"><code class="language-anylog">help get 
help set
help reset
help blockchain</code></pre>
* List command usage and examples - type ***help*** followed by the command text.  
  Examples:
<pre class="code-frame"><code class="language-anylog">help connect dbms
help blockchain insert
help get msg client
</code></pre>
The help provides the usage, examples, explanation and a link to the relevant documentation.  
For example:
<pre class="code-frame"><code class="language-anylog">help blockchain get

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

Link: https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#query-policies

Link: https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md
</code></pre>

* List an index that classifies the commands.
<pre class="code-frame"><code class="language-anylog">help index</code></pre>
* List commands associated with an index key.
<pre class="code-frame"><code class="language-anylog">help index index-key</code></pre>
Note: **help index** followed by a key prefix, returns all the EdgeLake commands associated with the key prefix.   
For example:
<pre class="code-frame"><code class="language-anylog">help index s</code></pre>
Returns all commands associated with **_s_** in the index key prefix:
* <code class="language-anylog">script</code> 
* <code class="language-anylog">secure network</code> 
* <code class="language-anylog">streaming</code>


### The local dictionary

Every node contains a dictionary. The dictionary maps keys to values. When users or applications interact with a node,
they can use the key names prefixed with an exclamation point (!) rather than specifying the values.  
The keys and values are organized in a dictionary and can be processed using the following commands:

* Assigning a value to a key:
<pre class="code-frame"><code class="language-anylog"> key = value</code></pre>
 Example:
<pre class="code-frame"><code class="language-anylog"> master_node = 126.32.47.29:2048</code></pre>
 
If the value string is identical to a command name, setting a value returns an error, and the user can enforce the value using the command ***set***.    
Example:
<pre class="code-frame"><code class="language-anylog">set dbms_name = test</code></pre>
 
* Retrieve a value assigned to a key is by executing ***!key***. For example:
<pre class="code-frame"><code class="language-anylog">!dbms_name</code></pre>
or using the get command:
<pre class="code-frame"><code class="language-anylog">get !dbms_name</code></pre>

* Retrieve all the assigned values:
<pre class="code-frame"><code class="language-anylog">get dictionary</code></pre>

The node dictionary is detailed in the [local dictionary](https://github.com/AnyLog-co/documentation/blob/master/dictionary.md#the-local-dictionary) section.

### Retrieving environment variables

By adding the $ sign to a variable name, users can retrieve the values assigned to an environment variable.
For example: **$HOME** retrieves the assigned value to HOME and **$PATH** retrieves the assigned value to PATH.

### Retrieving the services status

An active node is configured such that some services are enabled.
To view the list of services and their status issue the following command:
<pre class="code-frame"><code class="language-anylog">get processes</code></pre>
More information on the background processes is available the [background services](commands/backgound_services.md) section.

### The dynamic logs
Every node maintains 3 dynamic logs that capture different types of events:
* <code class="language-anylog">The event log</code> - registers the executed commands
* <code class="language-anylog">The error log</code> - registers the commands that failed to execute.
* <code class="language-anylog">The query log</code> - registers the executed SQL queries. This log needs to be enabled and configured as needed.
Additional information is available at [Profiling and Monitoring Queries](https://github.com/AnyLog-co/documentation/blob/master/profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries)

To view the content of the logs issue the following commands:
<pre class="code-frame"><code class="language-anylog">get event log
get error log
get query log</code></pre>

The content of the logs can be reset using the following commands:
<pre class="code-frame"><code class="language-anylog">reset event log
reset error log
reset query log</code></pre>

## Making a node a member of the network

Connecting a node to the network is explained in [network configuration](https://github.com/AnyLog-co/documentation/blob/master/network%20configuration.md#network-configuration).

The basic configuration of a node can be tested using the command:
<pre class="code-frame"><code class="language-anylog">test node</code></pre>
The following command tests the availability of the network members:
<pre class="code-frame"><code class="language-anylog">test network</code></pre>

## The Seed command
When a new node starts, or when a user wants to connect to a new network on the same root directory, user can retrieve 
and assign a node to a metadata using the following command:
<pre class="code-frame"><code class="language-anylog">seed from [ip:port]</code></pre>

Note: IP:Port is the IP and Port of a member of the network.    
More details are in the [Metadata](commands/metadata.md) section.

## Dynamically connecting to a master node

Users may need to switch between different master nodes.
The following command makes the [blockchain synchronizer process](commands/backgound_services.md)
 connect to a different master node:
<pre class="code-frame"><code class="language-anylog">blockchain switch network where master = [IP:Port]</code></pre>
Note: IP:Port is the IP and Port of the Master node.

## Using the REST API to issue EdgeLake commands

Users can execute the EdgeLake commands by sending the commands via REST to a node in the network.  
A node receiving REST requests interprets and executes the command regardless if the command is issued on the CLI or via REST.   
Additional information on the REST API to EdgeLake is available at the following section: [Using REST](https://github.com/AnyLog-co/documentation/blob/master/using%20rest.md#using-rest).

 
## Sending messages to peers in the network

Nodes in the network can send messages to peers in the network. Each message includes a command and sometimes additional data.      
When a message is received at a node, the node retrieves the command and the data from the message and executes the command.    
Depending on the command in the message, some messages trigger a reply (for example, a command to derive a status, or a SQL query)
and some types of commands are only executed on the destination node (for example, a command to change a state, or a command to display a message).    

The format for sending a command from the node's CLI is as follows:
<pre class="code-frame"><code class="language-anylog">run client (destination) command</code></pre>
### The message sections:
**run client** - Making the current node a client of a peer node (or nodes). The command is organized in a message
 delivered to one or more destination nodes and is executed on the destination nodes.    

**(destination)** - the destination nodes identified by the IP and Port assigned to their
[TCP Server configuration](commands/backgound_services.md#enable-the-tcp-service).
Destination can be represented in any of the following ways:
* As a comma (or space) separated list of IP-Ports pairs within parenthesis. For example: <code class="language-anylog">(139.162.126.241 2048, 172.105.13.202 2048)</code>    
* For a single destination node - as an IP-Port string (a single destination does not require the parenthesis). For example:  <code class="language-anylog">10.0.0.78:20348</code>  
* As variables. For example: <code class="language-anylog">!dest_ip !dest_port</code>
* As a query to the metadata that returns a list of comma separated IPs and Ports.

Note: If more than a single destination is specified, the destinations are contained in parentheses.   
  
**command** - any of the EdgeLake commands.  

### Examples:

<pre class="code-frame"><code class="language-anylog">run client 10.0.0.78:20348 get status
run client (139.162.126.241:2048, 172.105.13.202:2048) get processes   
run client (!operator1_ip !operator1_port, !operator2_ip operator2_port) get operator</code></pre>
Queries are not required to specify destinations (and the parentheses are left empty).  
If destination is not specified, the network protocol identifies the destination nodes.  
For example:
<pre class="code-frame"><code class="language-anylog">run client () sql my_dbms "select count(*) from my_table"</code></pre>
Destination can be a query to the metadata that generates a list of IPs and Ports.  
The example below returns the CPU usage from all the Operator nodes in the US: 
<pre class="code-frame"><code class="language-anylog">run client (blockchain get operator where [country] contains US bring [operator][ip] : [operator][port]  separator = ,) get cpu usage</code></pre>

Additional information is available at [Queries and info requests to the Network](https://github.com/AnyLog-co/documentation/blob/master/queries.md).

## Querying and updating metadata

The network maintains a global metadata that is stored in a blockchain or in a Master Node.  
Users are able to query and update the metadata (regardless of the platform used to store the metadata) using the ***blockchain commands***.    
Additional information on the blockchain commands is available in the [Metadata](commands/metadata.md) section.



