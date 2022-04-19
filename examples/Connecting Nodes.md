# Connecting nodes

Nodes in the network are connected to peer nodes in the network and to 3rd parties applications.   
Connection means that the nodes are waiting for messages from peer nodes and applications. When messages are received, 
the nodes may process the requests included in the messages (assuming proper permissions), and if needed, send a reply. 

***Note: The IP and Ports declared for communication between members and applications needs to be open. Remove firewall restrictions as needed.***

## Communicating with peer nodes

When a node operates, it communicates with peer members of the network.    
When a node starts, it is configured to listen on a socket associated with an Internet Protocol (IP) address and a port number.  
The command that initiate the listener is: ```run tcp server``` and is detailed [here](../background%20processes.md#the-tcp-server-process).    
The IP and Port specified can be of a local network or of an external/public network or both:  
An external or public IP is used across the entire Internet to locate computer systems and devices.  
A local or internal IP address is used inside a private network to locate the computers and devices connected to it.  
If both are used, then a router needs to be configured with [port forwarding](https://en.wikipedia.org/wiki/Port_forwarding) to redirect messages from the external IP and port 
to the local IP and port.

## Communicating with 3rd parties applications

When a node operates, it can be configured to communicate with 3rd party applications using [REST](https://en.wikipedia.org/wiki/Representational_state_transfer).  
The command that initiate the listener is: ```run rest server``` and is detailed [here](../background%20processes.md#rest-requests).  

## Publishing data

A node can be configured such that applications can treat the node as a [message broker](https://en.wikipedia.org/wiki/Message_broker) allowing data to be published on the node.  
Details of the configurations are available [here](../message%20broker.md#using-a-message-broker).

## Test peer connection
Use the AnyLog Command Line Interface (CLI) to test the connection.  
***Note: direct the call to the IP and Port declared using the ```run tcp server``` command.***

<pre>
run client 10.0.0.78:7848 get status
</pre>

Example reply:
<pre>
'test-machine@24.23.250.144:7848 running'
</pre>


Note that the IP and Port can specify a different member node, which will return a reply if active. 

## Test REST connection 
The commands below can be issued using REST. The examples are done using [cURL](https://curl.se/docs/).  
***Note: direct the call to the IP and Port declared using the ```run rest server``` command.***

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