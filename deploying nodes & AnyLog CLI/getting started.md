# Getting Started
 
This document provides the following:
* A high level summary of the main functionalities supported by the AnyLog Network.   
* Explanations on how to install, configure and run AnyLog instances. 

## About AnyLog

AnyLog is a decentralized network to manage IoT data. Nodes in the network are compute instances that execute the AnyLog Software.    
Joining a network requires the following steps:  
1) Install the AnyLog Software on computer instance
2) Configure a node such that it can join an exiting network (or create a new network).

## Type of instances
A node in the network is assigned with one or more roles. The optional roles are the following:  

| Node Type     | Role  |
| ----------- | ------------| 
| Publisher   | A node that receives data from a data source (i.e. devices, applications) and distributes the data to Operators. | 
| Operator   | A node that hosts the data and satisfies queries. |
| Query  | A node that orchestrates a query process. |
| Master | A node that maintains a complete copy of the metadata and receives updates when the metadata is updated. |

Using a Master node is optional. A master node is used to maintain the global metadata when users do not enable the blockchain functionality.   
Enabling the blockchain functionality using the Ethereum blockchain is explained in the [Using Ethereum as a Global Metadata Platform](../blockchain/using%20ethereum.md#using-ethereum-as-a-global-metadata-platform) section.
If a blockchain platform is used, there is no need in a Master node as the metadata is registered on (and is available from) the blockchain.  
Additional information on a Master Node configuration is available at the section: [Using a Master Node](../blockchain/using%20ethereum.md#using-ethereum-as-a-global-metadata-platform).

## The Network MetaData
The metadata is the network related information that is shared by members of the network.
The metadata includes information about the network members, their permissions, the logical representation of the data and how the data is distributed.  
The metadata is stored in a repository which is accessible to all the nodes in the network. The repository can be a blockchain or a master node.  
The interaction with the metadata is not dependent on the repository. When a member node operates, it is configured to use a particular metadata repository and
there are no operational differences which are dependent on the type of the metadata repository used.

**Note that the documentation (and the nodes processes) reference the blockchain for metadata operations regardless if the metadata is maintained in a blockchain platform or in a master node.**

The nodes in the network are configured to pull the metadata (from the blockchain platform or the master node) periodically (if it was changed) and update a local copy of the metadata on the node.  
The processing in a node considers the local copy of the metadata and therefore, nodes processes are agnostic to the metadata platform and if a connection 
to the metadata platform is lost, the node continues to operate based on the latest copy of the metadata that is maintained locally on the node.      
Synchronizing the local copy of the metadata is explained in the following section: [Blockchain Synchronizer](../deploying%20nodes%20&%20AnyLog%20CLI/background%20processes.md#blockchain-synchronizer).  


Related documentation:

| Section                                                                                | Information provided  |
|----------------------------------------------------------------------------------------| ------------| 
| [Metadata Management](../data%20management/metadata%20management.md#managing-metadata) | Details on the network metadata and related processes. | 
| [Metadata Requests](metadata%20requests.md)                                            | Details on how the metadata can be queried. |
| [Using Ethereum](../blockchain/using%20ethereum.md#using-ethereum-as-a-global-metadata-platform)                                                       | Using Ethereum as a global metadata platform. |

## The Data
The users data is distributed in local databases on the Operators Nodes. Operators can use different databases for different sets of data.  
Currently AnyLog Operators can use the following databases:  
[PostgresSQL](https://www.postgresql.org/) - recommended for larger nodes and deployments of large data sets.    
[SQLite](https://www.sqlite.org/index.html) - recommended for gateways, smaller nodes and deployments of small or in-memory data sets.      

The data managed by the network is distributed to many nodes but the network protocol provides a unified view over the distributed data -
the users or applications issuing the queries do not need to identify the nodes that host the relevant data - for each query, the network protocol 
resolves the location of the relevant data.   
Each query process starts with a node that receives a query from a user or application. This node is called the Query Node.
The Query Node determines which are the [Operators](#type-of-instances) 
that host the data that needs to be evaluated to satisfy the query, and delivers the query to these Operators.
Each of the Operators process the query locally and replies to the Query Node with a result. The Query Node aggregates all the results and returns a unified result to the user or application that issued the query.  

Related documentation:

| Section       | Information provided  |
| ------------- | ------------| 
| [Data Distribution and Configuration](data%20distribution%20and%20configuration.md) | The organization of the user data in the network. | 
| [Adding Data to Nodes in the Network](adding%20data.md) | Delivering data to Operators in the network. |
| [Using MQTT Broker](mqtt.md) | Delivering data to Operators using a MQTT broker. |
| [Managing Data files](../managing%20data%20files%20status.md) | Monitoring data managed by Operator nodes. |
| [Queries and info requests](queries%20and%20info%20requests.md) | Queries to data hosted by nodes in the network. |
| [Profiling and Monitoring Queries](../profiling%20and%20monitoring%20queries.md) | Identifying and profiling slow queries. |
| [Using Grafana](../northbound%20connectors/using%20grafana.md) | Integrating Grafana to visualize data. |
 
## AnyLog Install

AnyLog can be installed from [Docker](../deployments/Docker), [Kubernetes](../deployments/Kubernetes) or by downloading the codebase from GitHub and calling an installation script.
Starting AnyLog from the command line is demonstrated in the section: [Starting an AnyLog Instance](starting%20an%20anylog%20instance.md).

## Local directory structure

AnyLog directory setup is configurable. The default setup is detailed below: 

```anylog
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
       -->test        [Directory location for output data of test queries] 
       -->watch       [Directory monitored by the system, data files placed in the directory are being processed] 
    -->source         [The root directory for source or executable files]
    -->scripts        [System scripts to install and configure the AnyLog node]
       -->install     [Installation scripts]
       -->anylog      [Configuration Scripts]
    -->local_scripts  [Users scripts]
```

Note: The following command creates the work folders if they do not exist:
```anylog
create work directories
```
The command needs to be issued only once on the physical or virtual machine.

  
## Basic operations

### Starting AnyLog from the Linux CLI

From the AnyLog-Network directory issue the following command:
```anylog
python3 source/cmd/user_cmd.py [command line arguments]
```
The command line arguments are optional and can include a list of AnyLog commands separated by the _and_ keyword.  
The commands specified in the command line are executed upon initialization of the node and can include configuration and setup instructions.

If the initialization commands are organized in a script file, call the command _process_ followed by the path to the script. 

### AnyLog Command Line Interface
When a node starts, it provides the **AnyLog Command Line Interface** (AnyLog CLI).  
The command line prompt appear as `AL >` and it can be changed by issuing the following command on the CLI:
```anylog
node_name = my_node_name
```

Using the CLI, a user can interact with the node or peer nodes in the network.  
The supported commands allow to retrieve and modify configuration, state of different processes, query and update the blockchain data and
issue SQL queries to data stored locally and data that is stored by other members of the network.    

Exiting and terminating an AnyLog node is by issuing the command `exit node` on the CLI.
```anylog
AL anylog-node +> help exit 
Usage:
        exit [process type|reset]
        
Explanation:
        exit node - terminate all process and shutdown
        exit tcp - terminate the TCP listner thread
        exit rest - terminate the REST listner thread
        exit scripts - terminate the running scripts
        exit scheduler - terminate the scheduler process
        exit workers - terminate the query threads

Examples:
        exit node
        exit tcp
        exit rest
        exit scripts
        exit scheduler
        exit synchronizer
        exit mqtt
        exit kafka
        exit smtp
        exit workers
```

### The help command
The list of commands is available by executing the ***help*** command on the CLI:
```anylog
help
```

Users can apply the ***help*** command to detail specific options and examples of usage. Below are some examples:
```anylog
help get 
help get mqtt clients
help set
help set echo queue
help blockchain
help blockchain push
help connect dbms
help sql
```

### The node dictionary

Every node contains a dictionary. The dictionary maps keys to values and when users or applications interact with a node,
they can use the key names prefixed with an exclamation point (!) rather than specifying the values.  
The keys and values are organized in a dictionary and can be processed using the following commands:

* Assigning a value to a key:
```anylog
 key = value
```
 Example:
```anylog
 master_node = 126.32.47.29:2048
```
 
If the value string is identical to a command name, setting a value returns an error, and the user can enforce the value using the command ***set***.    
Example:
```anylog
set dbms_name = test
```
 
* Retrieve a value assigned to a key is by executing ***!key***. For example:
```anylog
!dbms_name
```
or using the get command:
```anylog
get !dbms_name
```

* Retrieve all the assigned values:
```anylog
get dictionary
```

The values assigned to key can be tested using an ***if statement*** to trigger conditional execution of ANyLog commands.  
Details are available in thr [Conditional Execution](anylog%20commands.md#conditional-execution) section. 


### Retrieving environment variables

By adding the $ sign to a variable name, users can retrieve the values assigned to an environment variable.
For example: $HOME retrieves the assigned value to HOME and $PATH retrieves the assigned value to PATH.

### Retrieving info on active background processes

An active node is configured such that some background processes are enabled.
To view the list of active processes issue the following command:
```anylog
get processes
```
More information on the background processes is available the [background processes](background%20processes.md) section.

### The dynamic logs
Every node maintains 4 dynamic logs that capture different types of events:
* The event log - registers the executed commands
* The error log - registers the commands that failed to execute.
* The query log - registers the executed SQL queries. This log needs to be enabled and configured as needed.
Additional information is available at [Profiling and Monitoring Queries](../query%20data/profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries)

To view the content of the logs issue the following commands:
```anylog
get event log
get error log
get query log
```

The content of the logs can be reset using the following commands:
```anylog
reset event log
reset error log
reset query log
```

## Making a node a member of the network

Connecting a node to the network is explained in [network configuration](network%20configuration.md).

Users can associate a node to different networks or configurations. This is a useful functionality for testing when users
deploy multiple networks, or they switch between a main-net and a testnet.

### Switching between different setups

Users may have multiple [directories setups](#local-directory-structure)
on the same node. Using the following command, users can associate a node to a different setup location:
```anylog
set anylog home [path to AnyLog root]
```
AnyLog root is the ***AnyLog-Network*** directory.

### Switching between different master nodes

Users may need to switch between different master nodes.
The following command makes the [blockchain synchronizer process](background%20processes.md#blockchain-synchronizer)
 connect to a different master node:
```anylog
blockchain switch network where master = [IP:Port]
```

## Using the REST API to issue AnyLog commands

Users can execute the AnyLog commands by sending the commands via REST to a node in the network.  
A node receiving REST requests interprets and executes the command regardless if the command is issued on the CLI or via REST.   
Additional information on the REST API to AnyLOg is available at the following section: [Using REST](using%20rest.md).

 
## Sending messages to peers in the network

Nodes in the network can send messages to peers in the network. Each message includes a command and sometimes additional data.      
When a message is received at a node, the node retrieves the command and the data from the message and executes the command.    
Depending on the command in the message, some messages trigger a reply (for example, a command to derive a status, or a SQL query)
and some types of commands are only executed on the node (for example, a command to change a state or a command to display a message).    
If authentication is disabled, a node will execute all the commands in the incoming messages.   
If authentication in enabled, the node will validate that the sender is authorized for the messaged command.
If validation fails, the node will discard the incoming message.  

The format to send a command is the following:
```anylog
run client (destination) command
```
#### The message sections:  
***run client*** - Making the current node a client of a member node (or nodes). The command is organized in a message
 delivered to one or more destination nodes and is executed on the destination nodes.    
***(destination)*** - the destination nodes identified by the IP and Port assigned to their
[TCP Server configuration](background%20processes.md#the-tcp-server-process).
Destination can be represented in any of the following ways:
* As a comma separate list of IP-Ports pairs. The IP and Port are separated by space. For example: `139.162.126.241 2048, 172.105.13.202 2048)`    
* For a single destination node - as an IP-Port string. For example:  `10.0.0.78:20348`  
* As variables. For example: `!dest_ip !dest_port`
* If more than a single destination is specified, the destinations are contained in parentheses.  
  
***command*** - any of the AnyLog commands.  

Examples:

```anylog
run client 10.0.0.78:20348 get status
run client (!operator1_ip !operator1_port, !operator2_ip operator2_port) get operator
```

Queries are not required to specify destinations. If destination is specified, only the destination nodes participate in the query.    
If destination is not specified, the network protocol identifies the destination.
When destination is not specified, the parentheses are left empty.  
For example:
```anylog
run client () sql my_dbms "select count(*) from my_table"
```
Additional information is available at [Queries and info requests to the AnyLog Network](../query%20data/queries.md#query-nodes-in-the-network).

## Querying and updating metadata in the blockchain

The network maintains a global metadata that is stored in a blockchain or in a Master Node.  
Users are able to query and update the metadata (regardless of the platform used to store the metadata) using the ***blockchain commands***.    
Additional information on the blockchain commands is available in the [Blockchain commands](../blockchain/blockchain%20commands.md) section.

## High Availability (HA)

Users can configure nodes in the network to dynamically and transparently replicate hosted data to maintain multiple copies of the data.    
Using this approach, if a node fails, queries are directed to a surviving node and a new node can be assigned to replace the failed node.  
Additional information on the HA processes is available in the [High Availability](../high-availability/high-availability.md#high-availability--ha-) section.

## Network security

Several mechanisms secure the data managed by the network:
* Nodes authentication - Each node is assigned with a private and a public key.
The public key servers as the identification of the node and the private key is used to sign messages send by the node.
When a node sends a message, the message data includes the public key and a signature over key information.
Using the signature and the signed information, the node that received the message is able to authenticate the sender. Then the node evaluates the permissions
provided to the sender and determines if the sender is authorized as needed.
* User authentication - Users can be assigned with private and public keys and consider as a node with the process described above.  
* Basic authentication - Nodes can be updated with a list of usernames and password and satisfy commands from users providing the registered passwords.
* Certificate - The network can provide certificates to Clients and Servers and configured such that connection to clients use SSL with client and server Certificate Authentication.
* Encryption - Message send between nodes in the network can be encrypted.  

Additional information is available in the [User Authentication](../security%20&%20authentication/authentication.md) section.


  


