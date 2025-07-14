## AnyLog Install

AnyLog can be installed from Docker, Kubernetes or by downloading the codebase from GitHub and calling an installation script. 
Directions for deployment can be found [here](deployments). 

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
       -->archive     [The root directory of and archival directory]
       -->bkup        [Optional location for backup of user data]
       -->blobs       [Directory containing unstructured data]
       -->dbms        [Optional location for persistent database data. If using SQLite, used for persistent SQLIte data]
       -->distr       [Directory used in the High Availability processes]
       -->error       [The storage location for new data that failed database storage]
       -->pem         [Directory containing keys and certificates]
       -->prep        [Directory for system intermediate data]
       -->test        [Directory location for output data of test queries] 
       -->watch       [Directory monitored by the system, data files placed in the directory are being processed] 
       -->bwatch      [Directory monitored by the system, managing unstructured data]
    -->source         [The root directory for source or executable files]
    -->scripts        [System scripts to install and configure the AnyLog node]
       -->install     [Installation scripts]
       -->anylog      [Configuration Scripts]
    -->local_scripts  [Users scripts]
```

Notes: 
* The following command creates the work folders if they do not exist:
    ```anylog
    create work directories
    ```
    The command needs to be issued only once on the physical or virtual machine.
    
* The following command list the directories on an AnyLog node:
     ```anylog
    get dictionary _dir
    ``` 
## Basic operations

### Initiating Configuring AnyLog instances

AnyLog is deployed and initiated using Docker or Kubernetes. The way the node operates depends on the configuration.  
AnyLog can be configured in many ways:
* Using command line arguments when AnyLog is called. These are a list of AnyLog commands separated by the _and_ keyword.
* By issuing configuration commands on the command line.
* By calling a script file that lists the AnyLog configuration commands (calling the command _process_ followed by the path to the script).
* By calling a configuration file that is hosted in a database.  
* Associating a Configuration Policy with the node. 

Related documentation:

| Section       | Information provided  |
| ------------- | ------------| 
| [Node configuration](node%20configuration.md#node-configuration) | Details on the configuration process. |
| [Deploying a node](deployments/deploying_node.md#deploying-a-node) | Basic deployment using Docker or Kubernetes. |
| [Network Setup](training/advanced/Network%20Setup.md) | A step by step example of a network deployment. |
| [Configuration Policies](policies.md#configuration-policies) | Policy based configuration. |

### AnyLog Command Line Interface
When a node starts, it provides the **AnyLog Command Line Interface** (AnyLog CLI).  
The command line prompt appear as `AL >` and it can be changed by issuing the following command on the CLI:
```anylog
set node name [node name]
```

Using the CLI, a user can interact with the node or peer nodes in the network.  
A more detailed description of the AnyLog CLI is available at [The AnyLog CLI](cli.md) section. 

Users issue commands to retrieve and modify configuration, state of different processes, query and update the blockchain data and
issue SQL queries to data stored locally and data that is stored by other members of the network.    

Exiting and terminating an AnyLog node is by issuing the command `exit node` on the CLI.

### The help command
The ***help*** command provides dynamic information on AnyLog commands.  
The help command is issued on the CLI and can be used in multiple ways:

* List the commands by typing ***help*** on the CLI.
```anylog
help
```
* List all commands that share the same prefix. For example: the keyword ***get*** is the prefix of a group of commands.
  These commands can be listed by typing ***help get***.   
  
Additional Examples:
 ```anylog
help get 
help set
help reset
help blockchain
```
* List command usage and examples - type ***help*** followed by the command text.  
  Examples:
```anylog
help connect dbms
help blockchain insert
help get msg client
```
The help provides the usage, examples, explanation and a link to the relevant documentation.
For example:
```anylog
help blockchain get

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
```

* List an index that classifies the commands.
```anylog
help index
```
* List commands associated with an index key.
```anylog
help index index-key
```
Note: **help index** followed by a key prefix, returns all the AnyLog commands associated with the key prefix.   
For example:
```anylog
help index s
```
Returns all commands associated with ***s*** in the index key prefix: ```script``` ```secure network``` ```streaming```.


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

The node dictionary is detailed in the [local dictionary](dictionary.md#the-local-dictionary) section.

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
Additional information is available at [Profiling and Monitoring Queries](profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries)

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

The basic configuration of a node can be done using the command:
```anylog
test node
```
The following command tests the availability of the network members:
```anylog
test network
```

Users can associate a node to different networks or configurations. This is a useful functionality for testing when users
deploy multiple networks, or they switch between a main-net and a testnet.

### Switching between different setups

Users may have multiple [directories setups](#local-directory-structure)
on the same node. Using the following command, users can associate a node to a different setup location:
```anylog
set anylog home [path to AnyLog root]
```
AnyLog root is the ***AnyLog-Network*** directory.  

If AnyLog is assigned to a new root directory, the subdirectories can be created using the 
**create work directories** command (see details in the [Local directory structure](#local-directory-structure) section).

## The Seed command
When a new node starts, or when a user wants to connect to a new network on the same root directory, user can retrieve 
and assign a node to a metadata using the following command:
```anylog
seed from [ip:port]
```
More details are in the [Blockchain Commands](blockchain%20commands.md#retrieving-the-metadata-from-a-source-node) section.

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
Additional information on the REST API to AnyLog is available at the following section: [Using REST](using%20rest.md).

 
## Sending messages to peers in the network

Nodes in the network can send messages to peers in the network. Each message includes a command and sometimes additional data.      
When a message is received at a node, the node retrieves the command and the data from the message and executes the command.    
Depending on the command in the message, some messages trigger a reply (for example, a command to derive a status, or a SQL query)
and some types of commands are only executed on the destination node (for example, a command to change a state, or a command to display a message).    
If authentication is disabled, a node will execute all the commands in the incoming messages.   
If authentication in enabled, the node will validate that the sender is authorized for the messaged command.
If validation fails, the node will discard the incoming message.  

The format to send a command from the node's CLI is the following:
```anylog
run client (destination) command
```
### The message sections:  
**run client** - Making the current node a client of a peer node (or nodes). The command is organized in a message
 delivered to one or more destination nodes and is executed on the destination nodes.    

**(destination)** - the destination nodes identified by the IP and Port assigned to their
[TCP Server configuration](background%20processes.md#the-tcp-server-process).
Destination can be represented in any of the following ways:
* As a comma (or space) separated list of IP-Ports pairs within parenthesis. For example: `(139.162.126.241 2048, 172.105.13.202 2048)`    
* For a single destination node - as an IP-Port string (a single destination does not require the parenthesis). For example:  `10.0.0.78:20348`  
* As variables. For example: `!dest_ip !dest_port`
* As a query to the metadata that returns a list of comma separated IPs and Ports.

Note: If more than a single destination is specified, the destinations are contained in parentheses.   
  
**command** - any of the AnyLog commands.  

### Examples:

```anylog
run client 10.0.0.78:20348 get status
run client (139.162.126.241:2048, 172.105.13.202:2048) get processes   
run client (!operator1_ip !operator1_port, !operator2_ip operator2_port) get operator
```
Queries are not required to specify destinations (and the parentheses are left empty).  
If destination is not specified, the network protocol identifies the destination nodes.  
For example:
```anylog
run client () sql my_dbms "select count(*) from my_table"
```
Destination can be a query to the metadata that generates a list of IPs and Ports.  
The example below returns the CPU usage from all the Operator nodes in the US: 
```anylog
run client (blockchain get operator where [country] contains US bring [operator][ip] : [operator][port]  separator = ,) get cpu usage
```

Additional information is available at [Queries and info requests to the AnyLog Network](queries.md#query-nodes-in-the-network).



