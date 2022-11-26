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

* Messages between nodes which are members of the network. A member node is a compute instance deployed with the AnyLog software.  
  These messages are TCP based (therefore called TCP messages), leverage the AnyLog messaging protocol
  and are sent between the AnyLog instances. 
  The TCP messages are triggered to support 2 types of functionalities: 
  1. AnyLog functionality to maintain the completeness of the network, These messages are transparent (to the users and applications) 
     allowing to manage the network and processes of the network. Examples of such messages are: Heartbeat messages, Messages to sync
     metadata, Recovery messages.
  2. User messages - Messages to support users and application requests.
     Users can login to a node and issue messages directed to any available peer in the network. Or users can issue 
     messages to nodes in the network using REST requests which are translated to a message exchange between nodes 
     in the network.
     
     Examples of such messages are: queries to data, query metadata, retrieve status of nodes in the network and copy data.
     
  
## The REST messages

Users and applications can query data or state by sending a request to a node in the network using REST. 
The node receiving the reply will process the request and if needed, return a reply to the caller. 
  
The [Querying Data](https://github.com/AnyLog-co/documentation/blob/master/examples/Querying%20Data.md#querying-data)
section provides examples of issueing queries to retrieve data using REST.

The following example is a cURL call to determine the status of a node:

<pre>
curl --location --request GET http://10.0.0.78:7849 --header "User-Agent: AnyLog/1.23" --header "command: get status"
</pre>

## The TCP messages

Users can login to a node and using the node's Command Line Interface (CLI) and query data or query and monitor state.  
When a command is processed on the CLI, unless specifically requested, it is processed locally. However, 
users can request to execute each command on members nodes whereas these nodes can be identified explicitly, or in the case of queries for data,
the network protocol can determine the relevant nodes (these would be the nodes that host the data that is need to be considered to 
satisfy the query).

A command that is prefixed with ***run client (destination)*** is executed against the relevant member nodes:    
* ***run client*** means that the command is executed from a process serving as a client to network nodes.  
* ***(destination)*** is the list of destination nodes (IP:Port and separated by commas) that are to process the request to follow.  
In case of a query for data, the parenthesis can be left empty. In this case, the network protocol determines the destination nodes.

The following example requests the status of a node:
<pre>
run client 139.162.164.95:32148 get status
</pre>
Note, if only one destination node is specified, the parenthesis can be ignored.

The following example requests cpu usage information from 2 nodes:
<pre>
run client (139.162.164.95:32148, 139.162.164.95:32148) get cpu usage
</pre>

The following example queries sensor data whereas destination nodes are determined by the query protocol.  
<pre>
run client () sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"
</pre>

## Setting the message destinations

Using ***run client (destination)*** as a command prefix, delivers the command to the destination nodes.  
There are a few options to the way the destination nodes are specified:

* As a comma separated list of IP and Ports.  
    Example:
    <pre>
    run client (139.162.164.95:32148, 139.162.164.95:32148) get cpu usage
    </pre>
    
* As an empty parenthesis followed by a query. The query includes 2 sections. The first starts with the keyword ***sql*** followed by
a database name (and additional instructions on how to execute the query) and the second is the ***select*** statement that includes the table
name. Using the command (and the metadata), the network protocol determines the nodes that host the data. This process
    is transparent to the caller.  
    Example:
    <pre>
    run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor WHERE timestamp > NOW() - 1 day limit 100"
    </pre>

* Specifying the database name and the table name will deliver the command to the nodes that host the specified table.  
    Example:
    <pre>
    run client (dbms = litsanleandro and table = ping_sensor) get cpu usage
    </pre>
    
* As a blockchain command that retrieves IP and Ports and formats the destination as a comma separated list.    
   Example (retrieving the disk space of all Operator nodes in the US):
    <pre>
    run client (blockchain get operator where [country] contains US bring [operator][ip] : [operator][port]  separator = , ) get disk space .
    </pre>
    
    This command can be also issued as an assignment of the blockchain command to a key and referencing the key as the destination:  
   Example:
    <pre>
    destination = blockchain get operator where [country] contains US bring [operator][ip] : [operator][port]  separator = ,
    run client (!destination) get disk space .
    </pre>
    
    
## Messaging reply modes - the 'subset' flag

A message can be delivered to one or more nodes. Because of the intermittent nature of the network, some nodes may not be accessible.  
Users can configure their setup to deliver High Availability by replicating the data between nodes.
However, user's commands may be targeting specific nodes (rather than the data), and in that case a node may be unavailable.  
When the command is send, and using a flag called ***subset flag***, users can specify to consider the returned result from the participating nodes
and indicate which are the nodes that failed.  
If the subset is set to false (or is not specified), and a node does not return a reply, the entire command including the replies
from the participating nodes is considered as an error.

The following examples sets the subset flag to true, allowing the user to receive replies from the participating nodes,
including when some nodes fail to participate.

<pre>
run client (subset = True) sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"
run client (dbms = litsanleandro  and table = ping_sensor, subset = trure) get processes
</pre>


## Network Configuration

Nodes in the network are configured to receive messages from 2 sources:  

a. From users and applications using a REST API.  
This functionality is enabled by calling the command: ***run rest server***  

b. From peer nodes using the native AnyLog API.  
This functionality is enables by calling the command: ***run tcp server***  

## Determining the IP addresses recognized by a node in the network

When a node starts, it determines the local IP addresses available to the node. These addresses initialize 2 dictionary variables:  

| Variable Name | Explanation   | Retrieve value |
| ------------- | ------------- | ------------- |
| ip            | The Public IP or a Local IP if the node is on a local network | !ip |
| external_ip   | The Public IP | !external_ip |


Some systems fail to identify their IP addresses, and the values can be set by the user.  
To view all IPs recognized by the node issue the following command:
<pre>
get ip list
</pre> 

## Configuring a REST server process
Any node in the network can be configured to receive requests using the REST API.  
Usage:
<pre>
run rest server [ip] [port] where timeout = [timeout] and threads = [threads count] and ssl = [true/false]
</pre>
More details on the REST API are available at [using rest](https://github.com/AnyLog-co/documentation/blob/master/using%20rest.md#using-rest).  
More details on setting a node as a REST server is available at [background processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests).  

## Configuring a TCP server process
This process makes each node a member in the AnyLog Network and allows communication between peers in the network.  

Usage:
<pre>
run tcp server [ip] [port] [threads]
</pre>
   
***[ip] [port]*** - The IP and Port of the socket that is in the listening state and accessible by peer nodes in the AnyLog Network.   
***[local ip] [local port]*** - Optional parameters to indicate an IP and Port that are accessible from a local network.  
***[threads]*** - An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 6.

Additional information is available in the [Background Processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#the-tcp-server-process) section. 

### The Source Address
When the command ***run tcp server*** is initiated, the node dedicates a process to listen to incoming messages on the declared IP and Port.
When the node sends a message to a peer, it requests that the reply is send to the declared IP and Port.  
Therefore, for an outgoing message, the declared IP and Port serve as a Source Address identifying the node that issued the message and an address for a reply message.   
 
A user can configure a node to use a different reply address in one of the following ways:

a) Request peers to reply using a different address.  
b) Request peers to determine the reply address from the message socket.

## Self messaging

For self-messaging, nodes use their configured Local IP address.  
In some setups (i.e., Kubernetes), a self-message does not work as it is needed to assign a different address for self-messaging.  
Using the ***set self ip*** command, a self-message is directed to use a different IP address than the configured address.
In this case, the port remains the same as the port configured for the local address (using the ***run tcp server*** command).
Therefore, this command needs to be set only if the TCP server is configured.  
Using the ***set self ip and port*** command, a self message is directed to use a different address than the configured address.   

if the keyword ***dynamic*** is used, the machine's local IP is used for self-messaging.

usage:
<pre>
set self ip = [ip]
set self ip and port = [IP:Port]
</pre>

Examples:
<pre>
set self ip = dynamic
set self ip = 10.0.0.178
set reply ip and port = 10.0.0.178:4078
set reply ip and port = dynamic:4078
set reply ip and port = !self_ip:!self_port
</pre>

### Reset self messaging
Calling reset will disable the use of self IP.  
Usage:
<pre>
reset self ip
</pre>


## Setting a different IP address for replies 
Using the ***set reply ip*** command, user can direct a node sending a message, to receive the reply on a different IP address.    
Using the ***set reply ip and port*** command, user can direct a node sending a message, to receive the reply on a different IP and port address.  

Usage:
<pre>
set reply ip = [ip]
set reply ip and port = [IP:Port]
</pre>

Examples:
<pre>
set reply ip = !external_ip
set reply ip = 24.23.250.144
set reply ip and port = 24.23.250.144:4078
</pre>

The value assigned to the ***reply ip*** can be retrieved using the following command:
<pre>
get reply ip
</pre>

### Using the message socket to determine the reply IP 
This configuration will retrieve the peer IP from the message socket and use the retrieved IP for the reply message.  
Usage:
<pre>
set reply ip = dynamic
</pre>

### Reset the reply IP to the Source IP 
Calling reset will disable the use of reply IP. Replies will use the Source IP.  
Usage:
<pre>
reset reply ip
</pre>


# Testing the network configuration

Different command calls can view and test the network configuration.  

View active connection using the command:
<pre>
get connections
</pre>

Test the node configuration including the status of the REST server and the TCP server using the command:
<pre>
test node
</pre>
 
Test connection between 2 peers in the network:
<pre>
run client (host:port) get status
</pre>

Test the REST server configuration:
<pre>    
rest get url =  http://ip:port type = info details = "get status"
</pre>  
Example:
<pre>
rest get url =  http://10.0.0.159:2049 type = info details = "get status"
</pre>

DIsplay the IP and Port used in a message:
<pre>
trace level = 1 tcp
</pre>

DIsplay the IP and Port used in a REST message by sending a VIEW request to the REST server.    
Example:
<pre>
curl --location --request VIEW 24.23.250.144:2049
</pre>
