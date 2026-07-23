---
title: Network Processing
description: How messages are routed between AnyLog nodes once connectivity is established - REST vs. TCP messaging, reply/self-messaging addresses, run client destination targeting, blockchain-driven routing, and the subset flag for partial-failure tolerance.
layout: page
visibility: public
version: open source
tags:
- networking
- routing
---

<!--
## Changelog
- 2026-07-14 | Split from the original Network Processing.md, which also duplicated IP/REST/TCP-basics
  content now consolidated in Installation & Deployment / Networking.md. This document keeps only the
  message-routing material unique to it. Fixed a few typos along the way.
- 2026-07-14 (rev 2) | Restored a fuller "Reply and self-messaging addresses" section (Source Address,
  set reply ip / set reply ip and port, set self ip / set self ip and port), since the Installation &
  Deployment intro doc was condensed down to a one-pager and no longer carries this level of detail.
  Also corrected a copy-paste error in the original self-messaging examples, which used "set reply ip
  and port" where "set self ip and port" was clearly intended.
-->

# Network Processing
## overview

AnyLog is a peer-to-peer (P2P) network of nodes that facilitates data management on the distributed nodes. 
These nodes appear to users and applications as a single machine.  
This document describes low level details of the networking related configurations and operations allowing to treat the 
network nodes as a single machine. These networking processes are combined with a shared metadata layer that allow for 
the network nodes and network hosted data to appear as a single machine that manages a unified collection of data.

The AnyLog Network Protocol deploys 2 layers of messaging:

* Messages between users/applications and the network. These messages are REST based (called REST messages), and delivered 
  to one node in the network. The AnyLog protocol on the node, when the REST message is delivered, transforms the message
  to a TCP message (see the TCP based messages section below) that is delivered to the proper nodes and if needed, 
  a reply is returned to the user or application using the same REST connection.

* Messages between nodes which are members of the network. A member node is an instance deployed with the AnyLog software.  
  These messages are TCP based (therefore called TCP messages), leverage the AnyLog messaging protocol
  and are sent between the AnyLog instances. 
  The TCP messages are triggered to support 2 types of functionalities: 
  1. AnyLog functionality to maintain the completeness of the network, These messages are transparent to users and applications 
     allowing to manage the network and processes of the network. Examples of such messages are: Heartbeat messages, Messages to sync
     metadata, Recovery messages.
  2. User messages - Messages to support users and application requests.
     Users can log into a node and issue messages directed to any available peer in the network. Or users can issue 
     messages to nodes in the network using REST requests which are translated to a message exchange between nodes 
     in the network.
     
     Examples of such messages are: queries to data, query metadata, retrieve status of nodes in the network and copy data.
     
## The REST messages

Users and applications can query data or state by sending a request to a node in the network using REST. 
The node receiving the reply will process the request and if needed, return a reply to the caller. 
  
The [Querying Data](examples/Querying%20Data.md#querying-data) section provides examples of issuing queries to retrieve 
data using REST.

The following example is a cURL call to determine the status of a node:

```anylog
curl --location --request GET http://10.0.0.78:7849 \
    --header "User-Agent: AnyLog/1.23" \
    --header "command: get status"

curl --location --request POST http://10.0.0.78:7849 \
    --header "Content-Type: application/json" \
    -d '{"command": "get status", "AnyLog-Agent": "AnyLog/1.23"}'
```

## The TCP messages

Users can attach to any AnyLog agent in the Edge Data Fabric (EDF) and from a single point interact with all the nodes 
in the network over TCP. 

When a command is processed on the CLI, unless specifically requested, it is processed locally. However, users can 
request to execute each command on members nodes whereas these nodes can be identified explicitly, or in the case of 
queries for data, the network protocol can determine the relevant nodes (these would be the nodes that host the data 
that is need to be considered to satisfy the query).

A command that is prefixed with `run client (_destination_)` is executed against the relevant member nodes:    
* `run client` means that the command is executed from a process serving as a client to network nodes.  
* `(_destination_)` is the list of destination nodes (IP:Port and separated by commas) that are to process the request to follow.  
In case of a query for data, the parenthesis can be left empty. In this case, the network protocol determines the destination nodes.

The following example requests the status of a node:
```anylog
run client (139.162.164.95:32148) get status
```
Note, if only one destination node is specified, the parenthesis can be ignored.

The following example requests cpu usage information from 2 nodes:
```anylog
run client (139.162.164.95:32148, 139.162.164.95:32148) get cpu usage
```

The following example queries sensor data whereas destination nodes are determined by the query protocol.  
```anylog
run client () sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"
```
## Reply and self-messaging addresses

When the command `run tcp server` is initiated, the node dedicates a process to listen for incoming messages on the 
declared IP and port. When the node sends a message to a peer, it requests that the reply be sent back to that same 
declared IP and port — this is the message's **Source Address**, identifying both who sent it and where a reply 
should go.

Two situations call for overriding that default.

### A different reply address

Using `set reply ip`, a user can direct a node sending a message to receive the reply on a different IP address. 
Using `set reply ip and port`, both the IP and port can be overridden together.

**Usage:**
```anylog
set reply ip = [ip]
set reply ip and port = [ip:port]
```

**Examples:**
```anylog
set reply ip = !external_ip
set reply ip = 24.23.250.144
set reply ip and port = 24.23.250.144:4078
```

Retrieve the current value:
```anylog
get reply ip
```

**Using the message socket to determine the reply IP** — rather than a fixed address, this retrieves the peer IP 
directly from the message socket and uses it for the reply:
```anylog
set reply ip = dynamic
```

**Reset** — disables the use of a reply IP; replies fall back to the Source IP:
```anylog
reset reply ip
```

### Self-messaging

For self-messaging, nodes normally use their own configured local IP address. In some setups — Kubernetes, for 
example — self-messaging doesn't work this way, because the configured address isn't reachable from the node 
itself, so a different address needs to be assigned specifically for messaging the node to itself.

`set self ip` directs self-messages to use a different IP than the configured address; the port stays the same as 
whatever's configured for the local address via `run tcp server`. This only needs to be set if the TCP server is 
already configured. `set self ip and port` overrides both together. Using the keyword `dynamic` uses the machine's 
local IP for self-messaging.

**Usage:**
```anylog
set self ip = [ip]
set self ip and port = [ip:port]
```

**Examples:**
```anylog
set self ip = dynamic
set self ip = 10.0.0.178
set self ip and port = 10.0.0.178:4078
set self ip and port = dynamic:4078
set self ip and port = !self_ip:!self_port
```

**Reset** — disables the use of a self IP:
```anylog
reset self ip
```

## Setting the message destinations

Using `run client (_destination_)` as a command prefix, delivers the command to the destination nodes. There are a few 
options to the way the destination nodes are specified:

* As a comma separated list of IP and Ports.  
    **Example**:
    ```anylog
    run client (139.162.164.95:32148, 139.162.164.95:32148) get cpu usage
    ```
    
* As an empty parenthesis followed by a query. The query includes 2 sections. The first starts with the keyword _sql_ followed by
a database name (and additional instructions on how to execute the query) and the second is the _select_ statement that includes the table
name. Using the command (and the metadata), the network protocol determines the nodes that host the data. This process
is transparent to the caller.  
**Example**:
```anylog
run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor WHERE timestamp > NOW() - 1 day limit 100"
```

* Specifying the database name and the table name will deliver the command to the nodes that host the specified table.  
**Example**:
```anylog
run client (dbms = litsanleandro and table = ping_sensor) get cpu usage
```
    
* As a blockchain command that retrieves IP and Ports and formats the destination as a comma separated list.    
**Example** (retrieving the disk space of all Operator nodes in the US):
```anylog
run client (blockchain get operator where [country] contains US bring [operator][ip] : [operator][port]  separator = , ) get disk usage .
```

This blockchain command can be replaced with a specific call to retrieve the list of IPs and Ports:
```anylog
run client (blockchain get operator where [country] contains US bring.ip_port) get disk usage .
```
    
This command can be also issued as an assignment of the blockchain command to a key and referencing the key as the destination:  
**Example**:
```anylog
destination = blockchain get operator where [country] contains US bring.ip_port
run client (!destination) get disk usage .
```
## Using shortcuts to specify the destination of a TCP message

User can reference the metadata from a **run client** command by ignoring the **blockchain get** keywords and the **bring.ip_port** directive.  
This shortcut representation applies in 2 use cases:
* With a **run client** command.
* With an assigned CLI [assigned CLI](training/advanced/background%20deployment.md#assigning-a-cli-to-a-peer-node).

The example below demonstrates a shortcut (and retrieves the same destination IPs and Ports as in the examples above):
```anylog
run client (operator where [country] contains US) get disk usage .
```
This type of shortcut is applied when the information inside the parenthesis is as follows:
* Starts with one of a keywords that represents a node type: **master**, **query**, **operator**, or a **publisher**.
* Starts with a parenthesis. The example below returns the IP and Ports of all Operators and Query nodes:
```anylog
run client ((operator,query) where [country] contains US) get cpu usage
```
## Organizing replies from multiple nodes

Users can associate replies from multiple nodes to a key in the dictionary. It allows to reference the replies and 
determine which are the nodes that participated in the process.  
Details are available in the [Associating peer replies to a key in the dictionary](Network Processing.md#associating-peer-replies-to-a-key-in-the-dictionary) section.

## Queries messaging modes - the 'subset' flag

A message can be delivered to one or more nodes. Because of the intermittent nature of the network, some nodes may not be accessible.  
Users can configure their setup to deliver High Availability by replicating the data between nodes.
However, user's commands may be targeting specific nodes (rather than the data), and in that case a node may be unavailable.  
When the command is sent, and using a flag called _subset flag_, users can specify to consider the returned result from the participating nodes
and indicate which are the nodes that failed.  
If the subset is set to false (or is not specified), and a node does not return a reply, the entire command including the replies
from the participating nodes is considered as an error.

The following examples sets the subset flag to true, allowing the user to receive replies from the participating nodes,
including when some nodes fail to participate.

```anylog
run client (subset = True) sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor WHERE timestamp > NOW() - 1 day;"
run client (dbms = litsanleandro  and table = ping_sensor, subset = true) get processes
```

### Associating peer replies to a key in the dictionary

A user can issue a command to target nodes using the **run client** command or assigning the CLI to one or more nodes.  

Replies from the target nodes can be stored in the node's local dictionary using one of the following methods:
* Using square brackets ([]) that extend the key, the replies are organized in a list. Every list entry is organized
  as a pair with the IP and Port of the target node, and the reply text.
* Using curly brackets ({}) that extend the key, the replies are organized in a dictionary. The keys in the dictionary
   are the IP and Port of the target nodes, and the values represent the reply message from each node. 

The examples below assume an [assigned CLI](training/advanced/background%20deployment.md#assigning-a-cli-to-multiple-peer-nodes).
 
**Example 1: replies organized as a list**
  ```anylog
current_status[] = get status where format = json
```
The reply from the target nodes is organized as a list and assigned to the key **current_status**.
Each entry in the list has 2 values: 1) the IP and Port of the target node and 2) the reply.

**Example 2: replies organized as a dictionary**
  ```anylog
current_status{} = get status where format = json
```
The reply from target nodes is organized as a dictionary and assigned to the key **current_status**.
The key in the dictionary is the IP and Port of each target node and the value is the reply from each node.

### Validating nodes replies

Users can determine the number of nodes participating in a process by evaluating the status of the replies as follows:

| Key extension | Example                 |  Explanation             |
| ------------- | ------------------------| ---------------------- |
| .len          | current_status.len      | The number of elements in the list or dictionary (representative of the number of target nodes).   |
| .replies      | current_status.replies  | The number of nodes replied to the message.   |
| .diff         | current_status.diff     | The difference between .len and .replies (representative of the number of nodes that did not reply.  |

Note: users can issue a **wait** command after the target nodes are messaged to pause execution until all nodes replied 
and a time threshold - whichever comes first. Details are available in the [wait command](anylog%20commands.md#the-wait-command) section.