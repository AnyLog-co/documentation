# Network Processing

## overview

AnyLog is a peer-to-peer (P2P) network of nodes that facilitates data management on the distributed nodes. 
These nodes appear to users and applications as a single machine.  
This document describes low level details of the networking related configurations and operations allowing to treat the network nodes as a single machine.
These networking processes are combined with a shared metadata layer that allow for the network nodes and network hosted data to appear as a 
single machine that manages a unified collection of data.

The AnyLog Network Protocol deploys 2 layers of messaging:

* Messages between users/applications and the network. These messages are REST based (called REST messages), and delivered 
  to one node in the network. The AnyLog protocol on the node, when the REST message is delivered, transforms the message
  to a TCP message (see the TCP based messages section below) that is delivered to the proper nodes and if needed, 
  a reply is returned to the user or application using the same REST connection.

* Messages between nodes which are members of the network. A member node is an instance deployed with the AnyLog software.  
  These messages are TCP based (therefore called TCP messages), leverage the AnyLog messaging protocol
  and are sent between the AnyLog instances. 
  The TCP messages are triggered to support 2 types of functionalities: 
  1. AnyLog functionality to maintain the completeness of the network, These messages are transparent (to the users and applications) 
     allowing to manage the network and processes of the network. Examples of such messages are: Heartbeat messages, Messages to sync
     metadata, Recovery messages.
  2. User messages - Messages to support users and application requests.
     Users can log into a node and issue messages directed to any available peer in the network. Or users can issue 
     messages to nodes in the network using REST requests which are translated to a message exchange between nodes 
     in the network.
     
     Examples of such messages are: queries to data, query metadata, retrieve status of nodes in the network and copy data.
     
  
## The REST messages

Users and applications can query data or state by sending a request to a node in the network using REST. 
The node receiving the reply will process the request and if needed, return a reply to the caller. 
  
The [Querying Data](examples/Querying Data.md#querying-data) section provides examples of issuing queries to retrieve 
data using REST.

The following example is a cURL call to determine the status of a node:

```anylog
curl --location --request GET http://10.0.0.78:7849 --header "User-Agent: AnyLog/1.23" --header "command: get status"
```

## The TCP messages

Users can log into a node and using the node's Command Line Interface (CLI) and query data or query and monitor state.  
When a command is processed on the CLI, unless specifically requested, it is processed locally. However, 
users can request to execute each command on members nodes whereas these nodes can be identified explicitly, or in the case of queries for data,
the network protocol can determine the relevant nodes (these would be the nodes that host the data that is need to be considered to 
satisfy the query).

A command that is prefixed with `run client (_destination_)` is executed against the relevant member nodes:    
* `run client` means that the command is executed from a process serving as a client to network nodes.  
* `(_destination_)` is the list of destination nodes (IP:Port and separated by commas) that are to process the request to follow.  
In case of a query for data, the parenthesis can be left empty. In this case, the network protocol determines the destination nodes.

The following example requests the status of a node:
```anylog
run client (139.162.164.95:32148) get status
```
Note, if only one destination node is specified, the parenthesis can be ignored.

The following example requests cpu usage information from 2 nodes:
```anylog
run client (139.162.164.95:32148, 139.162.164.95:32148) get cpu usage
```

The following example queries sensor data whereas destination nodes are determined by the query protocol.  
```anylog
run client () sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"
```

## Setting the message destinations

Using `run client (_destination_)` as a command prefix, delivers the command to the destination nodes. There are a few 
options to the way the destination nodes are specified:

* As a comma separated list of IP and Ports.  
    **Example**:
    ```anylog
    run client (139.162.164.95:32148, 139.162.164.95:32148) get cpu usage
    ```
    
* As an empty parenthesis followed by a query. The query includes 2 sections. The first starts with the keyword _sql_ followed by
a database name (and additional instructions on how to execute the query) and the second is the _select_ statement that includes the table
name. Using the command (and the metadata), the network protocol determines the nodes that host the data. This process
    is transparent to the caller.  
    **Example**:
    ```anylog
    run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor WHERE timestamp > NOW() - 1 day limit 100"
    ```

* Specifying the database name and the table name will deliver the command to the nodes that host the specified table.  
    **Example**:
    ```anylog
    run client (dbms = litsanleandro and table = ping_sensor) get cpu usage
    ```
    
* As a blockchain command that retrieves IP and Ports and formats the destination as a comma separated list.    
   **Example** (retrieving the disk space of all Operator nodes in the US):
    ```anylog
    run client (blockchain get operator where [country] contains US bring [operator][ip] : [operator][port]  separator = , ) get disk space .
    ```
    
This command can be also issued as an assignment of the blockchain command to a key and referencing the key as the destination:  
   **Example**:
    ```anylog
    destination = blockchain get operator where [country] contains US bring [operator][ip] : [operator][port]  separator = ,
    run client (!destination) get disk space .
    ```
   
## Queries messaging modes - the 'subset' flag

A message can be delivered to one or more nodes. Because of the intermittent nature of the network, some nodes may not be accessible.  
Users can configure their setup to deliver High Availability by replicating the data between nodes.
However, user's commands may be targeting specific nodes (rather than the data), and in that case a node may be unavailable.  
When the command is sent, and using a flag called _subset flag_, users can specify to consider the returned result from the participating nodes
and indicate which are the nodes that failed.  
If the subset is set to false (or is not specified), and a node does not return a reply, the entire command including the replies
from the participating nodes is considered as an error.

The following examples sets the subset flag to true, allowing the user to receive replies from the participating nodes,
including when some nodes fail to participate.

```anylog
run client (subset = True) sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"
run client (dbms = litsanleandro  and table = ping_sensor, subset = trure) get processes
```

### Associating peer replies to a key in the dictionary

A user can issue a command to target nodes using the **run client** command or assigning the CLI to one or more nodes.  

Replies from the target nodes can be stored in the node's local dictionary using one of the following methods:
* Using square brackets ([]) that extend the key, the replies are organized in a list. Every list entry is organized
  as a pair with the IP and Port of the target node, and the reply text.
* Using curly brackets ({}) that extend the key, the replies are organized in a dictionary. The keys in the dictionary
   are the IP and Port of the target nodes, and the values represent the reply message from each node. 

The examples below assume an [assigned CLI](training/advanced/background%20deployment.md#assigning-a-cli-to-multiple-peer-nodes).
 
**Example 1: replies organized as a list**
  ```anylog
current_status[] = get status where format = json
```
The reply from the target nodes is organized as a list and assigned to the key **current_status**.
Each entry in the list has 2 values: 1) the IP and Port of the target node and 2) the reply.

**Example 2: replies organized as a dictionary**
  ```anylog
current_status{} = get status where format = json
```
The reply from target nodes is organized as a dictionary and assigned to the key **current_status**.
The key in the dictionary is the IP and Port of each target node and the value is the reply from each node.

### Validating nodes replies

Users can determine the number of nodes participating in a process by evaluating the status of the replies as follows:

| Key extension | Example                 |  Explanation             |
| ------------- | ------------------------| ---------------------- |
| .len          | current_status.len      | The number of elements in the list or dictionary (representative of the number of target nodes).   |
| .replies      | current_status.replies  | The number of nodes replied to the message.   |
| .diff         | current_status.diff     | The difference between .len and .replies (representative of the number of nodes that did not reply.  |

Note: users can issue a **wait** command after the target nodes are messaged to pause execution untill all nodes replied 
and a time threshold - whichever comes first. Details are available in the [wait command](anylog%20commands.md#the-wait-command) section.

## Network Configuration

Nodes in the network are configured to receive messages from 2 sources:  

a. From users and applications using a REST API.  
This functionality is enabled by calling the command: `run rest server`  

b. From peer nodes using the native AnyLog API. This functionality is enables by calling the command: `run tcp server`  

## Determining the IP addresses recognized by a node in the network

When a node starts, it determines the local IP addresses available to the node. These addresses initialize 2 dictionary variables:  

| Variable Name | Explanation   | Retrieve value |
| ------------- | ------------- | ------------- |
| ip            | The Public IP or a Local IP if the node is on a local network | !ip |
| external_ip   | The Public IP | !external_ip |


Some systems fail to identify their IP addresses, and the values can be set by the user.  
To view all IPs recognized by the node issue the following command:
```anylog
get ip list
``` 

## Configuring a REST server process
Any node in the network can be configured to receive requests using the REST API.  
Usage:
```anylog
run rest server [ip] [port] where timeout = [timeout] and threads = [threads count] and ssl = [true/false]
```
More details on the REST API are available at [using rest](using%20rest.md#using-rest).  
More details on setting a node as a REST server is available at [background processes](background%20processes.md#rest-requests).  

## Configuring a TCP server process
This process makes each node a member in the AnyLog Network and allows communication between peers in the network.  

**Usage**:
```anylog
run tcp server [ip] [port] [threads]
```
   
* [ip] [port] - The IP and Port of the socket that is in the listening state and accessible by peer nodes in the AnyLog Network.   
* [local ip] [local port] - Optional parameters to indicate an IP and Port that are accessible from a local network.  
* [threads] - An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 6.

Additional information is available in the [Background Processes](background%20processes.md#the-tcp-server-process) section. 

### The Source Address
When the command `run tcp server` is initiated, the node dedicates a process to listen to incoming messages on the declared IP and Port.
When the node sends a message to a peer, it requests that the reply is sent to the declared IP and Port.  
Therefore, for an outgoing message, the declared IP and Port serve as a Source Address identifying the node that issued the message and an address for a reply message.   
 
A user can configure a node to use a different reply address in one of the following ways:

a) Request peers to reply using a different address.  
b) Request peers to determine the reply address from the message socket.

## Self messaging

For self-messaging, nodes use their configured Local IP address.  
In some setups (i.e., Kubernetes), a self-message does not work as it is needed to assign a different address for self-messaging.  
Using the `set self ip` command, a self-message is directed to use a different IP address than the configured address.
In this case, the port remains the same as the port configured for the local address (using the `run tcp server` command).
Therefore, this command needs to be set only if the TCP server is configured.  
Using the `set self ip` and port command, a self message is directed to use a different address than the configured address.   

if the keyword _dynamic_ is used, the machine's local IP is used for self-messaging.
**Usage**:
```anylog
set self ip = [ip]
set self ip and port = [IP:Port]
```

**Examples**:
```anylog
set self ip = dynamic
set self ip = 10.0.0.178
set reply ip and port = 10.0.0.178:4078
set reply ip and port = dynamic:4078
set reply ip and port = !self_ip:!self_port
```

### Reset self messaging
Calling reset will disable the use of self IP.  
**Usage**:
```anylog
reset self ip
```

## Setting a different IP address for replies 
Using the `set reply ip` command, user can direct a node sending a message, to receive the reply on a different IP address.    
Using the `set reply ip and port` command, user can direct a node sending a message, to receive the reply on a different IP and port address.  

**Usage**:
```anylog
set reply ip = [ip]
set reply ip and port = [IP:Port]
```

**Examples**:
```anylog
set reply ip = !external_ip
set reply ip = 24.23.250.144
set reply ip and port = 24.23.250.144:4078
```

The value assigned to the `reply ip` can be retrieved using the following command:
```anylog
get reply ip
```

### Using the message socket to determine the reply IP 
This configuration will retrieve the peer IP from the message socket and use the retrieved IP for the reply message.  
**Usage**:
```anylog
set reply ip = dynamic
```

### Reset the reply IP to the Source IP 
Calling reset will disable the use of reply IP. Replies will use the Source IP.  
**Usage**:
```anylog
reset reply ip
```


# Testing the network configuration

Different command calls can view and test the network configuration.  

View active connection using the command:
```anylog
get connections
```

Test the node configuration including the status of the REST server and the TCP server using the command:
```anylog
test node
```
 
Test connection between 2 peers in the network:
```anylog
run client (host:port) get status
```

Test the REST server configuration:
```anylog    
rest get url =  http://ip:port type = info details = "get status"
```  
**Example**:
```anylog
rest get url =  http://10.0.0.159:2049 type = info details = "get status"
```

Display the IP and Port used in a message:
```anylog
trace level = 1 tcp
```

Display the IP and Port used in a REST message by sending a VIEW request to the REST server.    
**Example**:
```anylog
curl --location --request VIEW 24.23.250.144:2049
```
