# Network Configuration

## overview

Nodes in the network are configured to receive messages from 2 sources:  

a. From users and applications using a REST API.  
This functionality is enabled by calling the command: ***run rest server***  

b. From peer nodes using the native AnyLog API.  
This functionality is enables by calling the command: ***run tcp server ip port***  

## Configuring a REST server process
Any node in the network can be configured to receive requests using the REST API.
More details on the REST API are available at (using rest)[https://github.com/AnyLog-co/documentation/blob/master/using%20rest.md#using-rest].  
More details on setting a node as a REST server is available at (background processes)[https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests].  

## Configuring a TCP server process
This process is used for communication between peers in the network.
 

Each node can send a message to a peer in the network.  
The command ```run client (list of servers) command``` makes a node a client to one or more peer nodes
and the message is delivered by specifying the destination hosts and ports.

The servers to receive the message can be specified as follows:
* a single server can be specified as host:port or host and port with space separated.
* multiple servers in parenthesis with comma separated - (host:port, host:port) or (host port, host port).  
for exampple: ```run client (10.0.0.124:2048, 125.128.23.8:2048) "blockchain test"```
* A condition that is satisfied from the blockchain and provides a list of servers.  
For example: ```run client (blockchain get operator where dbms = lsl_demo bring ['operator']['ip'] ":" ['operator']['port'] seperator = ",") "blockchain test"```
* A name of a database will provide the IP and ports of the Operators that support the database.     
For example: ```run client (dbms = lsl_demo) "blockchain test"```
 

## Tesing the host and ports

When a server is up, the configured ips and ports can be tested as follows:  

To test the TCP server configuration use the command:  
```run client (host:port) "get status"```

To test the REST server configuration use the command:    
```rest get url =  http://ip:port type = info details = "get status"```  
Example:  
```rest get url =  http://10.0.0.159:2049 type = info details = "get status"```


