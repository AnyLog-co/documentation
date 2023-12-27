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
run grpc client where ip = [IP] and port = [port] and policy = [policy id] anf grpc_dir = [dir path] and proto = [proto name] 
    and function = [proto function] and request = [request message] and response = [response message] and service = [service name]
    and value = (key1 = value1 and key2 = value2 ...) and debug = [true/false] and limit = [max events] and dbms = [dbms name] and table = [table name]
    and ingest = [true /false]
```

**Command variables**:

| Key        | Mandatory | Value  | 
| ---------- | -------| ------- |
| ip         | Y | The gRPC server IP. |
| Port       | Y | The gRPC server port. |
| policy     | N | The ID of the mapping policy to apply on the gRPC stream |
| grpc_dir   | Y | The target directory with the **proto** filr. |
| proto      | Y | The proto file name (dummy in the example above). |
| function   | Y | The proto function that is called on the server (**SampleDataResponse** in the proto file example above). |
| request    | Y | The .proto request message. |
| response   | Y | The .proto response message. |
| service    | Y | The name of the service  of method definition in the .proto file. |
| value      | N | One or more attribute name value pairs that update the attributes of the message send (ie.: Filter = system and Type = 5.int). |
| debug      | N | The value 'true' prints on the node CLI console the data received and processed. The default value is 'false' |
| limit      | N | Process ends after data events received from the gRPC servers reached the limit. |
| dbms       | N | A target database name (if not provided by a policy). |
| table      | N | A target table name (if not provided by a policy). |
| ingest     | N | The value 'false' ignores data ingestion. The default value is 'true' |

Examples (the < and > signs designate a code block that can be used on the CLI):
```anylog
<run grpc client where ip = 127.0.0.1 and port = 50051 and grpc_dir = D:/AnyLog-Code/AnyLog-Network/dummy_source_code/kubearmor/proto 
    and proto = kubearmor and function = WatchLogs and request = RequestMessage and response = Log 
    and service = LogService and value = (Filter = policy) and debug = true and limit = 2 and ingest = false>
```
```anylog
<run grpc client where ip = 127.0.0.1 and port = 50051 and grpc_dir = D:/AnyLog-Code/AnyLog-Network/dummy_source_code/kubearmor/proto 
    and proto = kubearmor and function = HealthCheck and request = NonceMessage and response = ReplyMessage and service = LogService 
    and value = (nonce = 10.int) and debug = true and limit = 1 and ingest = false>
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
