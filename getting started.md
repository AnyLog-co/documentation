# Getting Started
This document explains how to install and run AnyLog instances.  

## About AnyLog

AnyLog is a decentralized network to manage IoT data. Nodes in the network are compute instances that execute the AnyLog Software.    
Joining a network requires the following steps:  
1) Install the AnyLog Software on a compute instance.
2) Configure the node such that it can join an exiting network (or create a new network).

## Type of instances
A node in the network is assigned with one or more roles. The optional roles are the following:  

| Node Type     | Role  |
| ----------- | ------------| 
| Publisher   | a node that receives data from a data source (i.e. devices) and distribute the data to Operators. | 
| Operator   | a node that hosts the data and satisfy queries. |
| Query  | a node that orchestrates a query processe. |
| Master | a node that maintains a complete copy of the metadata and receives updates when the metadata is updated. |

## Managing the MetaData
The metadata is the network related information that is shared by members of the network.
The metadata includes information about the network members, their permissions, the logical representation of the data and how the data is distributed.  
The metadata is stored in a repository which is accessible to all the nodes in the network. The repository can be a blockchain or a master node.  
The interaction with the metadata is not dependent on the repository. When a member node operates, it is configured to use a particular metadata repository and
there are no operational differences which are dependent on the type of metadata repository.  
***Note that the documentation (and the nodes processes) reference the blockchain for metadata operations regardless if the metadata is maintained in a blockchain platform or in a master node.***   
Nodes in the network are configured to pull the metadata periodically (if it was changed) and the processing in a node considers the 
local copy of the blockchain. Therefore, if connection to the blockchain platform is lost, the node continues to operate based on the latest copy of the metadata that is maintained locally on the node.  
Synchronizing the local copy of the blockchain data is explained in the following section: [Blockchain Synchronizer](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#blockchain-synchronizer).  

## Managing the Data
The users data is distributed in local databases on the Operators Node. Operators can use different databases for different sets of data.  
Currently AnyLog Operators can use the following databases:
[PostgreSQL](https://www.postgresql.org/) - recommended for larger nodes and deployments of large data sets.  
[SQLite](https://www.sqlite.org/index.html) - recommended for gateways, smaller nodes and deployments of small or in-memory data sets.    
The data managed by the network is distributed to many nodes but the network protocol provides a unified view over the distributed data -
 the query process for user data does not need to identify the nodes that host the relevant data.  
For each query, the network protocol resolves the location of the relevant data and returns a reply as if the data is organized in a single database.  

## AnyLog Install

AnyLog can be installed from Docker or by downloading the codebase from github and calling an install script.
Docker install is detailed in the section: [AnyLog Docker Install](https://github.com/AnyLog-co/documentation/blob/master/anylog%20docker%20install.md)

## Local directory structure

AnyLog directory setup is configurable. The default setup is detailed below: 

<pre>
Directory Structure   Explabnation
-------------------   -----------------------------------------
--> AnyLog-Network    [AnyLog Root]
    -->anylog         [Directory containing authentication keys and passwords]
    -->blockchain     [A JSON file representing the metadata relevant to the node]
    -->data           [Users data and intermediate data processed by this node]
       -->archive     [The root directory of and archival for data processed successfully]
       -->bkup        [Optional location for backup of user data]
       -->dbms        [Optional location for persistent database data. If using SQLite, used for persistent SQLIte data]
       -->distr       [Directory maintaining JSON files that triggered failures when processed]
       -->error       [JSON files placed on this directory are processed by the node]
       -->pem         [Directory containing network Certificates]
       -->prep        [Directory for system intermediate data]
       -->watch       [Directory monitored by the system, data files placed in the directory are being processed] 
    -->source         [The root directory for source or executable files]
    -->scripts        [Script files that install and configure the AnyLog instance role]
       -->install     [Installation scripts]
       -->anylog      [AnyLog scripts, configure the AnyLog instance]
</pre>

## Basic operations

### Starting AnyLog from the Linux CLI

From the AnyLog-Network directory issue the following command:
<pre>
python3 source/cmd/user_cmd.py [command line arguments]
</pre>
The command line arguments are optional and can include a list of AnyLog commands separated by the ***and*** keyword.  
The commands specified in the command line are executed upon initialization of the node and can include configuration and setup instructions.

If the initialization commands are organized in a script file, call the command ***process*** followed by the path to the script. 

### AnyLog Command Line Interface
When a node starts, it provides the ***AnyLog Command Line Interface*** (CLI).  
The command line prompt appear as ***AL >*** and it can be changed by issuing the following command on the CLI:
<pre>
node_name = my_node_name
</pre>

Using the CLI, user can interact with the node or peers nodes in the network.  
The supported commands allow to retrieve and modify configuration, state of different processes 
and issue SQL queries to data stored locally and data that is stored by other members of the network.  

Exiting and terminating an AnyLog node is by issueing the command ***exit*** on the CLI.

### The help command
The list of commands is available by executing the ***help command*** on the CLI:
<pre>
help
</pre>

Users can apply the ***help command*** to detail specific options and examples of usage. Below are some examples:
<pre>
help get 
help get mqtt clients
help set
help set echo queue
help blockchain
help blockchain push
</pre>

### The node dictionary

Every node contains a dictionary. The dictionary maps keys to values and when users or applications interact with a node,
they can use the keys names prefixed with exclamation point (!) rather than the values.  
All the keys and values are organized in a dictionary and can be processed using the following command:

* Assigning a value to a key:
 <pre>
 key = value
 </pre>
 Example:
 <pre>
 master_node = 126.32.47.29:2048
 </pre>
 
If the value string is identical to a command name, setting a value returns an error and the user can enforce the value using the command ***set***.    
Example:
<pre>
set dbms_name = test
</pre>
 
* Retrieve a value assigned to a key is by executing ***!key***. For example:
<pre>
!dbms_name
</pre>

* Retrieve all the assigned values:
<pre>
get dictionary
</pre>

### Get info on active background processes

An active node may be configured such that some background processes are enabled.
To view the list of active processes issue the following command:
<pre>
get processes
</pre>
More information on the background processes is available the [background processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md) section.

### The dynamic logs
Every node maintains 4 dynamic logs that capture different types of events:
* The event log - registers the executed commands
* The error log - registers the commands that failed to execute.
* The query log - registers the executed SQL queries. This log needs to be enabled and configured as needed.

To view the content of the logs issue the following commands:
<pre>
get event log
get error log
get query log
</pre>

The content of the logs can be reset using the following commands:
<pre>
reset event log
reset error log
reset query log
</pre>

## Making a node a member of the network

Connecting a node to the network is explained in [network configuration](https://github.com/AnyLog-co/documentation/blob/master/network%20configuration.md)

