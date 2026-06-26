---
title: gRPC
description: Connect AnyLog as a gRPC client to receive data streams from gRPC servers and map them to local database tables.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | hyperlinks
--> 

<a href="https://en.wikipedia.org/wiki/GRPC" target="_blank">gRPC</a> is Google's open-source RPC framework — efficient, language-agnostic, and designed for high-throughput streaming. AnyLog connects as a gRPC **client**, receives data streams from a gRPC server, and maps them to a local database using policies.

---

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

---

## Starting a gRPC client

```anylog
<run grpc client where
  name    = [unique name] and
  ip      = [server IP] and
  port    = [server port] and
  grpc_dir = [path to proto/compiled files] and
  proto   = [proto file name, no extension] and
  function = [RPC method name] and
  request = [request message type] and
  response = [response message type] and
  service  = [service name] and
  policy   = [mapping policy ID] and
  value    = (key = value and ...) and
  debug   = [true/false] and
  limit   = [max events] and
  dbms    = [target database] and
  table   = [target table] and
  ingest  = [true/false] and
  invoke  = [true/false]>
```

### Parameter reference

| Parameter | Required | Description |
|---|---|---|
| `name` | ✅ | Unique ID for this gRPC connection |
| `ip` | ✅ | gRPC server IP |
| `port` | ✅ | gRPC server port |
| `grpc_dir` | ✅ | Directory containing the compiled proto files |
| `proto` | ✅ | Proto base filename (without extension) |
| `function` | ✅ | RPC method to call on the server |
| `request` | ✅ | Request message type name from the proto |
| `response` | ✅ | Response message type name from the proto |
| `service` | ✅ | Service name from the proto |
| `policy` | — | Mapping policy ID for schema mapping |
| `value` | — | Key-value pairs sent in the request message (e.g. `Filter = system and Type = 5.int`) |
| `debug` | — | `true` prints received data to the CLI (default: `false`) |
| `limit` | — | Stop after N events |
| `dbms` | — | Target database (if not provided by policy) |
| `table` | — | Target table (if not provided by policy) |
| `ingest` | — | `false` disables database ingestion — useful for testing (default: `true`) |
| `add_info` | — | Append metadata to each row: `conn` (IP:Port), `proto` (proto name), `request` (request type) |
| `invoke` | — | Whether to invoke immediately when called by another AnyLog process |

### Examples

```anylog
<run grpc client where
  name = kubearmor and ip = 127.0.0.1 and port = 50051 and
  grpc_dir = /app/AnyLog-Network/proto/kubearmor and
  proto = kubearmor and function = WatchLogs and
  request = RequestMessage and response = Log and
  service = LogService and value = (Filter = policy) and
  debug = true and limit = 2 and ingest = false>
```

```anylog
<run grpc client where
  name = kubearmor and ip = 127.0.0.1 and port = 50051 and
  grpc_dir = /app/AnyLog-Network/proto/kubearmor and
  proto = kubearmor and function = HealthCheck and
  request = NonceMessage and response = ReplyMessage and
  service = LogService and value = (nonce = 10.int) and
  debug = true and limit = 1 and ingest = false>
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
See <a href="{{ '/docs/Managing-Data-Southbound/video-streaming/' | relative_url }}">Video Streaming</a> for the full 
configuration including `video connect` and `run video stream`.