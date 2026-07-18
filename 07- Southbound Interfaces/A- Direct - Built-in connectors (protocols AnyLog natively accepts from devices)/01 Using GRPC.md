---
title: "Using gRPC"
description: "Connect AnyLog as a gRPC client to receive data streams from gRPC servers and map them to local database tables."
layout: page
source_path: "01 Using GRPC.md"
---

### 📜 Change Log
 **Date**   | **Name** | **Change**       | **Version** |
 |------------|--|------------------|----------|
 | 2026-07-17 | Eric Aquaronne | added change log | 2.0.2606 |



# Using gRPC

<a href="https://en.wikipedia.org/wiki/GRPC" target="_blank">gRPC</a> is Google's open-source RPC framework — efficient, language-agnostic, and designed for high-throughput streaming. AnyLog connects as a gRPC **client**, receives data streams from a gRPC server, and maps them to a local database using policies.

## AnyLog as a gRPC client
AnyLog can connect as a gRPC client to a gRPC Server to receive the data streams.  
Using AnyLog policies, these streams are mapped to a target schema, and the data is hosted on the local AnyLog node.

## Setup

### 1. Install grpcio-tools

```bash
python3 -m pip install --upgrade grpcio-tools
```

### 2. Create a proto file

The proto file defines the service, RPC methods, and message types. Example `dummy.proto`:

```protobuf
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

### 3. Compile the proto file

Run from the same directory as the `.proto` file:

```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dummy.proto
```

This generates two files (e.g. `dummy_pb2.py` and `dummy_pb2_grpc.py`) that AnyLog uses to communicate with the server.


## Initiating a gRPC client
The following command initiates a gRPC client on the AnyLog node:

```anylog
run grpc client where name = [unique name] and ip = [IP] and port = [port] and policy = [policy id] and grpc_dir = [dir path] and proto = [proto name] 
    and function = [proto function] and request = [request message] and response = [response message] and service = [service name]
    and value = (key1 = value1 and key2 = value2 ...) and debug = [true/false] and limit = [max events] and dbms = [dbms name] and table = [table name]
    and ingest = [true /false]
```

**Command variables**:

| Key        | Mandatory | Value  | 
| ---------- | -------| ------- |
| name       | Y | A unique name to identify the gRPC process. The name serves as the ID of the connection. |
| ip         | Y | The gRPC server IP. |
| Port       | Y | The gRPC server port. |
| policy     | N | The ID of the mapping policy to apply on the gRPC stream |
| grpc_dir   | Y | The target directory with the **proto** file. |
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
| add_info   | N | Updates the data retrieved from the server with additional info. For example, **added_info = conn**, includes the connection info. |
| invoke     | N | Whether the gRPC client is invoked by a process in AnyLog. |

Examples (the < and > signs designate a code block that can be used on the CLI):
```anylog
<run grpc client where name = kubearmor and ip = 127.0.0.1 and port = 50051 and grpc_dir = D:/AnyLog-Code/AnyLog-Network/dummy_source_code/kubearmor/proto 
    and proto = kubearmor and function = WatchLogs and request = RequestMessage and response = Log 
    and service = LogService and value = (Filter = policy) and debug = true and limit = 2 and ingest = false and invoke = [true / false]>
```
```anylog
<run grpc client where name = kubearmor and ip = 127.0.0.1 and port = 50051 and grpc_dir = D:/AnyLog-Code/AnyLog-Network/dummy_source_code/kubearmor/proto 
    and proto = kubearmor and function = HealthCheck and request = NonceMessage and response = ReplyMessage and service = LogService 
    and value = (nonce = 10.int) and debug = true and limit = 1 and ingest = false and invoke = [true / false] >
```

### Options for added_info

If **added_info** is included in the **run grpc client** command, the keys and values are added to the JSON data retrieved 
from the server.  
The added keys (to the JSON struct) are contained within greater than and less than signs (<key>).

| Key        | Value added to the JSON  | 
| ---------- | -----------------------------|
| proto      | The name of the proto file   |
| request    | The name of the request message in the proto file   |
| conn       | The IP and Port used   |

Example:
```anylog
<run grpc client where name=kubearmor and ip = 10.0.0.251 and port = 32769 and grpc_dir = D:/AnyLog-Code/AnyLog-Network/dummy_source_code/kubearmor/proto 
and proto = kubearmor and function = WatchLogs and policy = kubearmor-system-policy and request = RequestMessage and response = Log 
and service = LogService and value = (Filter = all) and debug = false  and limit = 10000 and ingest = false  
and add_info = conn and add_info = proto and add_info = request>
```


---

## Monitor and manage

```anylog
# List all active gRPC clients
get grpc clients
```

Example output:
```
ID        Connection       Proto     Request Message  Policy ID                Timeouts  Data Msg
---------|----------------|---------|----------------|------------------------|--------|--------|
health   |10.0.0.251:32769|kubearmor|NonceMessage    |                        |       0|    1254|
kubearmor|10.0.0.251:32769|kubearmor|RequestMessage  |kubearmor-system-policy |       0|       0|
```

```anylog
# List services offered by the gRPC server (requires server reflection)
get grpc services where conn = [ip:port]

# Stop a specific client
exit grpc [name]

# Stop all clients
exit grpc all
```

---

## gRPC for video inference

When used with video streaming, the gRPC client connects to a YOLOv5 (or similar) inference server. 
See <a href="/docs/managing-data-southbound/video-streaming/" target="_blank">Video Streaming</a> for the full 
configuration including `video connect` and `run video stream`.
