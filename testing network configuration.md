# Testing the network configuration

## overview

Nodes in the network are configured to receive messages from 2 sources:  

a. From peer nodes using TCP protocol.  
This functionality is enables by calling the command: ```run tcp server ip port```  

b. From users and applications using REST API.  
This functionality is enabled by calling the command: ```run REST server ip port```  

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

For simplicity disable authentication:
```set authentication off```

To test the TCP server configuration use the command:  
```run client (host:port) "get status"```

To test the REST server configuration use the command:    
```rest get url =  http://ip:port type = info details = "get status"```  
Example:  
```rest get url =  http://10.0.0.159:2049 type = info details = "get status"```


