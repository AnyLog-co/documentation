# Using gRPC

## Overview
gRPC (gRPC Remote Procedure Calls) is an open-source remote procedure call (RPC) framework developed by Google. 
It is designed to be efficient, scalable, and interoperable across different programming languages.
gRPC is used in distributed systems, microservices architectures, and client-server applications to enable efficient 
communication between components. Detailed gRPC documentation is available [here](https://grpc.io/docs/what-is-grpc/introduction/#overview).  

## AnyLog as a gRPC client
AnyLog can connect as a gRPC client to a gRPC Server to receive the data streams.  
Using AnyLog policies, these streams are mapped to a target schema, and the data is hosted on the local AnyLog node.  
Note, this process bypasses the need to use a **.proto** file, as the mapping instructions are represented in the policies.

# Initiating a gRPC client
The following command initiate a gRPC client on the AnyLog node:

```anylog
run grpc client where ip = [IP] and port = [port] and policy = [policy id] 
```

**Command variables**:

| Key        | Value  | 
| ---------- | -------| 
| ip         | The gRPC server IP. |
| Port       | The gRPC server port. |
| policy     | The ID of the mapping policy to apply on the gRPC stream |


# Retrieving the list of gRPC clients
The following command returns the list of connected gRPC clients on the AnyLog node:
```anylog
get grpc clients 
```
The info returns identifies each client by the connection info (IP and Port) and lists the policy type, name and ID.  
Example returned info:
```anylog
Connection      Policy Type Policy Name Policy ID
---------------|-----------|-----------|--------------------------------|
127.0.0.1:50051|mapping    |kuberarmor |deff520f1096bcd054b22b50458a5d1c|
```

# Terminate gRPC connection

A connection is terminated using the followng command:
```anylog
exit grpc [connection]
```
**connection** is the IP:Port string that identifies the server.    
For example, the following command terminates a gRPC process: 
```anylog
exit grpc 127.0.0.1:50051
```
To terminate all gRPC connections, use "all" as the connection string:
```anylog
exit grpc all
```


