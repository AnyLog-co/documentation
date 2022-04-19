# Connecting nodes

Nodes in the network are connected to peer nodes in the network and to 3rd parties applications.   
A connected node means that the node is configured with one or more listeners waiting for messages from peer nodes and applications. When messages are received, 
the node process the requests included in the messages (assuming proper permissions), and if needed, send a reply.
This document reviews how the listeners processes are configured. The table below summarizes the listeners types:
  
| Listener Name  | Functionality | Protocol/API |
| ------------- | ---- | --- |
| TCP | A listener on a dedicated IP and Port to receive messages from peer nodes.  | AnyLog |
| REST | A listener on a dedicated IP and Port to receive messages from 3rd parties applications.  | [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) |
| Messaging | A listener on a dedicated IP and Port to data published on the AnyLog node as a message broker.  | [MQTT](https://mqtt.org/)  |

Messages transferred to the TCP or REST listeners can be of the following:
* A query to retrieve data
* An AnyLog command to retrieve a state in a node. For example, to retrieve disk space availability or find how much data was ingested in the last hour.  
* An AnyLog command to enable a process. For example, to enable a process that will monitor data values received from a sensor.
* An AnyLog command that will retrieve or update policies on the shared metadata layer. For example, to retrieve the list of participating nodes that manage the sensor data.

The Messaging listener is enabled such that data can be published on an AnyLog Node like an MQTT broker (and assigned to a topic).

***Note: The IP and Ports used by the active listeners on each node needs to be open - remove firewall restrictions as needed.***

## The TCP listener - Communicating with peer nodes

When a node operates, it communicates with peer members of the network.    
When a node starts, it is configured to listen on a socket associated with an Internet Protocol (IP) address and a port number.  
The command that initiate the listener is: ```run tcp server``` and is detailed [here](../background%20processes.md#the-tcp-server-process).    
The IP and Port specified can be of a local network or of an external/public network or both:  
An external or public IP is used across the entire Internet to locate computer systems and devices.  
A local or internal IP address is used inside a private network to locate the computers and devices connected to it.  
If both are used, then a router needs to be configured with [port forwarding](https://en.wikipedia.org/wiki/Port_forwarding) to redirect messages from the external IP and port 
to the local IP and port.

## The REST listener - Communicating with 3rd parties applications

When a node operates, it can be configured to communicate with 3rd party applications using [REST](https://en.wikipedia.org/wiki/Representational_state_transfer).  
The command that initiate the listener is: ```run rest server``` and is detailed [here](../background%20processes.md#rest-requests).  

## The Messaging Listener - Publishing data on an AnyLog node

A node can be configured such that applications can treat the node as a [message broker](https://en.wikipedia.org/wiki/Message_broker) allowing data to be published (and assigned to a topic) on the node.  
Details of the configurations are available [here](../message%20broker.md#using-a-message-broker).

## Test peer connection
Use the AnyLog Command Line Interface (CLI) to test the connection.  
***Note: direct the call to the IP and Port declared using the ```run tcp server``` command.***  

To enter the AnyLog CLI (assuming Docker install, ```anylog-node``` is the name of the container):
<pre>
docker attach --detach-keys="ctrl-d" anylog-node
</pre>

Note: Messages (i.e. AnyLog commands) that are prefixed with ***run client*** followed by one or more destinations, will be delivered to the destination
nodes using the AnyLog protocol. The TCP listener configured on each destination node will receive the message, and if needed, a reply message is returned.  
To validate active and properly configured listener, a node can set the local IP and Port as the destination (note that
local processing of an AnyLog command does not require to pass the request to the listener as an AnyLog command issued on the CLI is processed locally).  
Destinations can be provided as IP:Port or as a list containing multiple IP:Port within parenthesis separated by a comma.

Note: To message a node on the local network, use the local IP and Port. To message a node which is outside the local network, use the external IP and Port.
  
***Status command***
<pre>
run client 10.0.0.78:7848 get status
</pre>

Example reply:
<pre>
'test-machine@24.23.250.144:7848 running'
</pre>
Note that the IP and Port can specify a different member node, which will return a reply if active. 

***get connections***
<pre>
get connections
</pre>

***View processes enabled***
<pre>
get processes
</pre>

***Run generic test***
<pre>
test node
</pre>


## Test REST connection 
The commands below can be issued using REST. The examples are done using [cURL](https://curl.se/docs/).  
***Note: direct the call to the IP and Port declared using the ```run rest server``` command.***

***Status command***  
The command ```get status``` returns the node status.

<pre>
curl -X GET http://10.0.0.78:7849 -H "command: get status" -H "User-Agent: AnyLOg/1.23"
</pre>

Example reply:
<pre>
test-machine@24.23.250.144:7848 running
</pre>

The command ```get connections``` returns the connection information.  

<pre>
curl -X GET http://10.0.0.78:7849 -H "command: get connections" -H "User-Agent: AnyLOg/1.23"
</pre>

Example reply:
<pre>
Type      External Address   Local Address
---------|------------------|--------------|
TCP      |24.23.250.144:7848|10.0.0.78:7848|
REST     |10.0.0.78:7849    |10.0.0.78:7849|
Messaging|24.23.250.144:7850|10.0.0.78:7850|
</pre>


The command ```get processes``` returns the processes enabled.
<pre>
curl -X GET 10.0.0.78:7849 -H "command: get processes" -H "User-Agent: AnyLog/1.23" 
</pre>

Example reply:
<pre>
   Process         Status       Details
    ---------------|------------|---------------------------------------------------------------------|
    TCP            |Running     |Listening on: 24.23.250.144:7848 and 10.0.0.78:7848, Threads Pool: 6 |
    REST           |Running     |Listening on: 10.0.0.78:7849, Threads Pool: 5, Timeout: 20, SSL: None|
    Operator       |Running     |Cluster Member: True, Using Master: 45.33.41.185:2048                |
    Publisher      |Not declared|                                                                     |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.33.41.185:2048           |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                       |
    Distributor    |Running     |                                                                     |
    Consumer       |Not declared|                                                                     |
    MQTT           |Not declared|                                                                     |
    Message Broker |Running     |Listening on: 24.23.250.144:7850 and 10.0.0.78:7850, Threads Pool: 4 |
    SMTP           |Not declared|                                                                     |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,000 bytes         |
    Query Pool     |Running     |Threads Pool: 3                                                      |
    Kafka Consumer |Not declared|                                                                     |
</pre>

