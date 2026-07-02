[//]: # (---)

[//]: # (layout: default)

[//]: # (title: gRPC  )

[//]: # (parent: Southbound)

[//]: # (nav_order: 4)

[//]: # (---)

# Using gRPC

## Overview
gRPC (gRPC Remote Procedure Calls) is an open-source framework developed by Google. 
It is designed to be efficient, scalable, and interoperable across different programming languages.
gRPC is used in distributed systems, microservices architectures, and client-server applications to enable efficient 
communication between components. Detailed gRPC documentation is available [here](https://grpc.io/docs/what-is-grpc/introduction/#overview).

## EdgeLake as a gRPC client
EdgeLake can connect as a gRPC client to a gRPC Server to receive the data streams. 

Using EdgeLake policies, these streams are mapped to a target schema, and the data is hosted on the local EdgeLakee node.

## Setup
Users define the data extracted from the gRPC server using a **proto** file.    

A Protocol Buffers (proto file) is a language-agnostic data serialization format developed by Google.    
This file is compiled to generate 2 **grpc** files that manage the process between the client and the server.

## Prerequisites
<ol start="1">
<li>Install <a href="https://pypi.org/project/grpcio-tools/" target="_blank">grpcio-tools</a>
<pre class="code-frame"><code class="language-shell">python3 -m pip install --upgrade grpcio-tools</code></pre></li>

<li>Create the protocol buffer file - <b>Example file</b>: <code>dummy.proto</code>:
<pre class="code-frame"><code class="language-config">syntax = "proto3"; 
    package mygrpc;
    
    service SerializeService {
      rpc GetSampleData (Empty) returns (SampleDataResponse);
    }
    
    message Empty {}
    
    message SampleDataResponse {
      repeated string serialized_data = 1;
    }
</code></pre></li>

<li>Compile file - <b>Example</b>:
<pre class="code-frame"><code class="language-shell">python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dummy.proto</code></pre></li>
</ol>
    
**Notes**: 
* Compile in the proto file (target) directory.  
* The following files are gennerated in the target directory (if dummy.proto is compiled) :
    * dummy_pb2.py
    * dummy_pb2_grpc,py


## Initiating a gRPC client
The following command initiate a gRPC client on the EdgeLake node:

<pre class="code-frame"><code class="language-anylog">&lt;run grpc client where 
    name = [unique name] and 
    ip = [IP] and 
    port = [port] and 
    policy = [policy id] and 
    grpc_dir = [dir path] and 
    proto = [proto name] and 
    function = [proto function] and 
    request = [request message] and 
    response = [response message] and 
    service = [service name] and 
    value = (key1 = value1 and key2 = value2 ...) and 
    debug = [true/false] and 
    limit = [max events] and 
    dbms = [dbms name] and 
    table = [table name] and 
    ingest = [true /false]&gt; 
</code></pre>

**Command variables**:

| Key        | Mandatory | Value  | 
| ---------- | -------| ------- |
| name       | Y | A unique name to identify the gRPC process. The name serves as the ID of the connection. |
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
| add_info   | N | Updates the data retrieved from the server with additional info. For example, **added_info = conn**, includes the connection info. |

Examples (the < and > signs designate a code block that can be used on the CLI):
<pre class="code-frame"><code class="language-anylog">&lt;run grpc client where 
    name = kubearmor and 
    ip = 127.0.0.1 and port = 50051 and 
    grpc_dir = D:/EdgeLake-Code/EdgeLake-Network/dummy_source_code/kubearmor/proto and 
    proto = kubearmor and function = WatchLogs and request = RequestMessage and response = Log and 
    service = LogService and value = (Filter = policy) and debug = true and limit = 2 and ingest = false&gt; 
<br/>
&lt;run grpc client where name = kubearmor and ip = 127.0.0.1 and port = 50051 and 
    grpc_dir = D:/EdgeLake-Code/EdgeLake-Network/dummy_source_code/kubearmor/proto and 
    proto = kubearmor and function = HealthCheck and request = NonceMessage and response = ReplyMessage and 
    service = LogService and value = (nonce = 10.int) and debug = true and limit = 1 and ingest = false&gt; 
</code></pre>

### Options for added_info

If **added_info** is included in the **run grpc client** command, the keys and values are added to the JSON data retrieved 
from the server. The added keys (to the JSON struct) are contained within greater than and less than signs (<key>).

| Key        | Value added to the JSON  | 
| ---------- | -----------------------------|
| proto      | The name of the proto file   |
| request    | The name of the request message in the proto file   |
| conn       | The IP and Port used   |

**Example**:
<pre class="code-frame"><code class="language-anylog">&lt;run grpc client where name=kubearmor and ip = 10.0.0.251 and port = 32769 and 
    grpc_dir = D:/EdgeLake-Code/EdgeLake-Network/dummy_source_code/kubearmor/proto and 
    proto = kubearmor and function = WatchLogs and policy = kubearmor-system-policy and request = RequestMessage and 
    response = Log and service = LogService and value = (Filter = all) and debug = false  and limit = 10000 and 
    ingest = false and add_info = conn and add_info = proto and add_info = request&gt; 
</code></pre>


## Retrieving the list of gRPC clients
The following command returns the list of connected gRPC clients on the EdgeLake node:
<pre class="code-frame"><code class="language-anylog">get grpc clients</code></pre>

The info returns identifies each client by the connection info (IP and Port) and the proto file name (ID).
An example of the returned info is below: 

| ID       | Connection       | Proto     | Request Message | Policy Type | Policy Name             | Policy ID | Timeouts | Data Msg |
|----------|------------------|-----------|-----------------|-------------|-------------------------|-----------|----------|----------|
| health   | 10.0.0.251:32769| kubearmor | NonceMessage    |             |                         |       0   |    1254  |          |
| kubearmor| 10.0.0.251:32769| kubearmor | RequestMessage  | mapping     | kubearmor-system-policy|       0   |       0  |          |


## Terminate gRPC connection

A connection is terminated using the following command:
<pre class="code-frame"><code class="language-anylog">exit grpc [ID]</code></pre>

**ID** is the **name** provided to the connection in the **run grpc client** command.    
For example, the following command terminates a gRPC process: 

<pre class="code-frame"><code class="language-anylog">exit grpc kubearmor</code></pre>

To terminate all gRPC connections, use "all" as the connection string:

<pre class="code-frame"><code class="language-anylog">exit grpc all</code></pre>

## Retrieving the list of gRPC services
Users can retrieve the list of services offered by the gRPC server.    
This process requires that the server reflection on the gRPC server is implemented and enabled.   
Server Reflection (ServerReflectionRequest ) allows clients to query information about services provided by a gRPC server dynamically.

The following command returns the list of gRPC services from the gRPC server:

<pre class="code-frame"><code class="language-anylog">get grpc services where conn = [ip:port]</code></pre>

**Example returned info**:
<table>
  <tr>
    <th style="text-align:left;"><b>gRPC Services</b></th>
  </tr>
  <tr>
    <td style="text-align:left;">grpc.reflection.v1alpha.ServerReflection</td>
  </tr>
  <tr>
    <td style="text-align:left;">test.MyService</td>
  </tr>
</table>
