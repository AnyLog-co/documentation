# Using gRPC

## Overview
gRPC (gRPC Remote Procedure Calls) is an open-source remote procedure call (RPC) framework developed by Google. 
It is designed to be efficient, scalable, and interoperable across different programming languages.
gRPC is used in distributed systems, microservices architectures, and client-server applications to enable efficient 
communication between components. Detailed gRPC documentation is available [here](https://grpc.io/docs/what-is-grpc/introduction/#overview).  

## AnyLog as a gRPC client
AnyLog can connect as a gRPC client to a gRPC Server to receive the data streams.  
Using AnyLog policies, these streams are mapped to a target schema, and the data is hosted on the local AnyLog node.

## Setup
Users define the data extracted from the gRPC server using a "proto file".  
A Protocol Buffers (proto file) is a language-agnostic data serialization format developed by Google.  
This file is compiled to generate 2 **grpc** files that manage the process between the client and the server.

## Prerequisites

1. Install [grpcio-tools](https://pypi.org/project/grpcio-tools/)
```shell
python3 -m pip install --upgrade grpcio-tools
```

2. Create the protocol buffer file  
    Example file: **dummy.proto**:
    ```shell
    syntax = "proto3";
    
    package mygrpc;
    
    service SerializeService {
      rpc GetSampleData (Empty) returns (SampleDataResponse);
    }
    
    message Empty {}
    
    message SampleDataResponse {
      repeated string serialized_data = 1;
    }
    ```    

3. Compile file  
    Example:
    ```shell
    python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dummy.proto
    ```
    Notes: 
    * Compile in the proto file (target) directory.  
    * The following files are gennerated in the target directory (if dummy.proto is compiled) :
        * dummy_pb2.py
        * dummy_pb2_grpc,py


## Initiating a gRPC client
The following command initiate a gRPC client on the AnyLog node:

```anylog
run grpc client where ip = [IP] and port = [port] and policy = [policy id] anf grpc_dir = [dir path] and proto = [proto name] and function = [proto function]
```

**Command variables**:

| Key        | Value  | 
| ---------- | -------| 
| ip         | The gRPC server IP. |
| Port       | The gRPC server port. |
| policy     | The ID of the mapping policy to apply on the gRPC stream |
| grpc_dir   | The target directory with the **proto** filr. |
| proto      | The proto file name (dummy in the example above). |
| function   | The proto function that is called on the server (**SampleDataResponse** in the proto file example above) |

example:
```anylog
 run grpc client where ip = 127.0.0.1 and port = 50051 and policy = deff520f1096bcd054b22b50458a5d1c and grpc_dir = D:/AnyLog-Code/AnyLog-Network/dummy_source_code/gRPC and proto = dummy and function = Empty
```

## Retrieving the list of gRPC clients
The following command returns the list of connected gRPC clients on the AnyLog node:
```anylog
get grpc clients 
```
The info returns identifies each client by the connection info (IP and Port) and lists the policy type, name and ID.  
Example returned info:
```anylog
ID                   Connection      Proto Request Message Policy Type Policy Name Policy ID
--------------------|---------------|-----|---------------|-----------|-----------|--------------------------------|
127.0.0.1:50051.test|127.0.0.1:50051|test |MyRequest      |cluster    |cluster_1  |deff520f1096bcd054b22b50458a5d1c|
```

## Terminate gRPC connection

A connection is terminated using the following command:
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

## Retrieving the list of gRPC services
Users can retrieve the list of services offered by the gRPC server.    
This process requires that the server reflection on the gRPC server is implemented and enabled.   
Server Reflection (ServerReflectionRequest ) allows clients to query information about services provided by a gRPC server dynamically.

The following command returns the list of gRPC services from the gRPC server:
```anylog
get grpc services where conn = [ip:port]
```

Example returned info:
```anylog
gRPC Services
----------------------------------------|
grpc.reflection.v1alpha.ServerReflection|
test.MyService                          |
```
