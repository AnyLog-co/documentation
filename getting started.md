# Getting Started
This document explains how to install, configure and run AnyLog instances.  

## About AnyLog

AnyLog is a decentralized network to manage IoT data. Nodes in the network are compute instances that execute the AnyLog Software.    
Joining a network requires the following steps:  
1) Install the AnyLog Software on a compute instance.
2) Configure the node such that it can join an exiting network (or create a new network).

## Type of instances
A node in the network is assigned with one or more roles. The optional roles are the following:  

| Node Type     | Role  |
| ----------- | ------------| 
| Publisher   | A node that receives data from a data source (i.e. devices) and distribute the data to Operators. | 
| Operator   | A node that hosts the data and satisfies queries. |
| Query  | A node that orchestrates a query process. |
| Master | A node that maintains a complete copy of the metadata and receives updates when the metadata is updated. |

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
The users data is distributed in local databases on the Operators Nodes. Operators can use different databases for different sets of data.  
Currently AnyLog Operators can use the following databases:  
[PostgreSQL](https://www.postgresql.org/) - recommended for larger nodes and deployments of large data sets.    
[SQLite](https://www.sqlite.org/index.html) - recommended for gateways, smaller nodes and deployments of small or in-memory data sets.      

The data managed by the network is distributed to many nodes but the network protocol provides a unified view over the distributed data -
 the query process for user data does not need to identify the nodes that host the relevant data.  
For each query, the network protocol resolves the location of the relevant data and returns a reply as if the data is organized in a single database.  

The section [Data Distribution and Configuration](https://github.com/AnyLog-co/documentation/blob/master/data%20distribution%20and%20configuration.md)
details how the user data is organized in the network.    
The section [Managing Data files](https://github.com/AnyLog-co/documentation/blob/master/managing%20data%20files%20status.md)
details how new file added to an Opertor node is registered and treated.

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

Using the CLI, a user can interact with the node or peer nodes in the network.  
The supported commands allow to retrieve and modify configuration, state of different processes, query and update the blockchain data and
issue SQL queries to data stored locally and data that is stored by other members of the network.    

Exiting and terminating an AnyLog node is by issuing the command ***exit*** on the CLI.

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
help connect dbms
help sql
</pre>

### The node dictionary

Every node contains a dictionary. The dictionary maps keys to values and when users or applications interact with a node,
they can use the key names prefixed with exclamation point (!) rather than the values.  
All the keys and values are organized in a dictionary and can be processed using the following commands:

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

### Retrieving environment variables

By adding the $ sign to a variable name, users can retrieve the values assigned to an environment variable.
For example: $HOME retrieves the assigned value to HOME and $PATH retrieves the assigned value to PATH.

### Get info on active background processes

An active node is configured such that some background processes are enabled.
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
Additional information is available at [Profiling and Monitoring Queries](https://github.com/AnyLog-co/documentation/blob/master/profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries)

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

Connecting a node to the network is explained in [network configuration](https://github.com/AnyLog-co/documentation/blob/master/network%20configuration.md).

Users can associate a node to different networks or configurations. This is a useful functionality for testing when users
deploy multiple networks or they switch between a main-net and a testnet.

### Switching between different setups

Users may have multiple [directories setups](https://github.com/AnyLog-co/documentation/blob/master/getting%20started.md#local-directory-structure)
on the same node. Using the following command, users can associate a node to a different setup location:
<pre>
set anylog home [path to AnyLog root]
</pre>
AnyLog root is the ***AnyLog-Network*** directory.

### Switching between different master nodes

Users may need to switch between different master nodes.
The following command makes the [blockchain synchronizer process](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#blockchain-synchronizer)
 connect to a different master node:
<pre>
blockchain switch network where master = [IP:Port]
</pre>
 
## Communicating between peers in the network

Nodes in the network can send messages to peers in the network. Each message includes a command and sometimes additional data.      
When a meesage is received at a node, the node retrieves the command and the data from the message and executes the command.    
Depending on the command in the message, some messages trigger a reply (for example, a command to derive a status, or a SQL query)
and some types of commands are only executed on the node (for example, a command to change a state or a commmad to display a message).    
If authentication is disabled, a node will execute all the commands in the incoming messages.   
If authentication in enabled, the node will validate that the sender is authorized for the messaged command.
If validation fails, the node will discard the incoming message.  

The format to send a command is the following:
<pre>
run client (destination) command
</pre>
#### The message sections:  
***run client*** - Making the current node a client of a member node (or nodes). The command is organized in a message
 delivered to one or more destination nodes and is executed on the destination nodes.    
***(destination)*** - the destination nodes identified by the IP and Port assigned to their
[TCP Server configuration](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#the-tcp-server-process).
Destination can be represented in any of the following ways:
* As a comma seperated list of IP-Ports pairs. The IP and Port are seperated by space. For example: ```139.162.126.241 2048, 172.105.13.202 2048)```    
* For a single destination node - as an IP-Port string. For example:  ```10.0.0.78:20348```  
* As variables. For example: ```!dest_ip !dest_port```
* If more than a single destination is specified, the destinations are contained in parentheses.  
  
***command*** - any of the AnyLog commands.  

Examples:

<pre>
run client 10.0.0.78:20348 get status
run client (!operator1_ip !operator1_port, !operator2_ip operator2_port) get operator
</pre>

Queries are not required to specify destinations. If destination is specified, only the destination nodes participate in the query.    
If destination is not specified, the network protocol identifies the destination.
When destination is not specified, the parentheses are left empty.  
For example:
<pre>
run client () sql my_dbms "select count(*) from my_table"
</pre>
More information is available at [Queries and info requests to the AnyLog Network](https://github.com/AnyLog-co/documentation/blob/master/queries%20and%20info%20requests.md).

# Network security

Several mechanisms secure the data managed by the network:
* Nodes authentication - each node is assigned with a private and public key.
The public key servers as the identification of the node and the private key is used to sign messages send by the node.
When a node sends a message, the message data includes the public key of the sender and a signature done with the private key of the sender.
Using the signature, the node that received the message is able to authenticate the sender. Then the node evaluates the permissions
provided to the sender and determines if the sender is authorized as needed.
* User authentication - users can be assigned with private and public keys and consider as a node with the process described above.  
* Basic authentication - Nodes can be updated with a list of user names and passoword and satisfy commands from users providing the registered passwords.
* Certificate - The network can provide certificates to Clients and Servers and configured such that connection to clients use SSL with client and server Certificate authentication.
* Encryption - message send between nodes in the network can be encrypted.
More information is available at [User Authentication](https://github.com/AnyLog-co/documentation/blob/master/authentication.md).

  


