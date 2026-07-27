---
title: "Test & Network Validation"
description: "Commands that determine the consistency and availability of data, metadata, and processes in the network: test node, test network, test connection, test process, and the test suite."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-26 | Ori Shadmon    | Merged "04 Test Commands.md" and "04 node-status commands.md" (near-total overlap) into a single page; `get status`/`get processes`/`get connections` now live only in Get and Set Reference | |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
--->

# Test & Network Validation

A key component of AnyLog is having nodes able to communicate with one another, in order to share both data and
metadata. Validating the state of the node — both in terms of running services and network connectivity — is
crucial. For the commands that report a node's own status and configuration (`get status`, `get processes`,
`get connections`), see [Get and Set Reference](03-%20Get%20and%20Set%20Reference.md#node-status).

## Test Node

The ***test node*** command tests the node's connections, and the structure of the local blockchain file. It verifies
that the node's TCP and REST services are reachable, and that the local copy of the blockchain ledger is not malformed
or corrupted in some way.

Example:
```anylog
test node
```

## Test Connection

The ***test connection*** command tests the given IP and Port to determine if it is accessible and open.

Example:
```anylog
test connection 10.0.0.223:2041
```

## Test Process

The ***test process*** command determines if the named service is enabled.

Usage:
```anylog
test process [process name]
```
The command returns **true** if the service is enabled, otherwise the value returned is **false**.
Users can retrieve the list of services using the **get processes** command.

Example:
```anylog
test process operator
```

## Test Network

The ***test network*** command determines the availability and consistency of multiple nodes in the network. It is
similar to issuing a `get status` command to every node in the network. Replies are organized in a table structure,
with a row representing each participating node.

Example:
```anylog
test network
```

Users can validate the configuration of the TCP listeners by issuing the **test network** command on the AnyLog CLI.
The command retrieves the list of participating AnyLog nodes and their addresses from the metadata and communicates
with each node. The output is the list of member nodes and their addresses. The **+** sign indicates a reachable node.
If the **+** sign is omitted, the node is not configured properly or is not reachable.

Example command and output:
<pre>
AL > test network

Address             Node Type Node Name       Status
-------------------|---------|---------------|------|
67.180.101.158:7848|operator |operator1      |   +  |
67.180.101.158:3048|operator |second_operator|   +  |

</pre>

### Test network with [object]

Object can be a node type or an IP and Port, to test connectivity with the specified nodes.

Examples:
```anylog
test network with master
test network with operator
test network with 67.180.101.158:7848
```

### Test Network Metadata Version

Similar to issuing a `get metadata version` command to all the nodes in the network.

Example:
```anylog
test network metadata version
```

### Test Network Table

The ***test network table*** command compares the table schema in the blockchain ledger against the schema in the local table. It is
similar to issuing a `test network table` command to all the nodes that host the table's data.

Usage:
```anylog
test network table where name = [table name] and dbms = [dbms name]
```
If table name is asterisk (`*`), all tables of the specified database are tested.

Examples:
```anylog
test network table where name = ping_sensor and dbms = lsl_demo
test network table where name = * and dbms = lsl_demo
test network table ping_sensor where dbms = lsl_demo
test network table * where dbms = lsl_demo
```

### Network error example

If a node fails to respond, a pop-up text will show the details of the issue. Example:

```error
|=====================================================================================================================================================================================================================================|
|TCP Client Error [Timeout] attempt 3/3                                                                                                                                                                                               |
|Dest=(172.105.112.207:32148) Local=('172.233.208.212', 41764) Sock=<socket.socket fd=14, family=2, type=1, proto=0, laddr=('172.233.208.212', 41764)>                                                                                |
|Reason: Timed out (no SYN-ACK)                                                                                                                                                                                                       |
|Hint: Likely filtered by firewall/security group or the host is down. Verify listener and inbound rules.                                                                                                                             |
|Elapsed: 6.00s (limit 6s)                                                                                                                                                                                                            |
|TCP_INFO: {'tcpi_state': 2, 'tcpi_retransmits': 5, 'tcpi_probes': 0, 'tcpi_backoff': 1, 'tcpi_options': 0, 'tcpi_rto_ms': 2000, 'tcpi_rtt_ms': 0, 'tcpi_rttvar_ms': 0, 'tcpi_snd_ssthresh': 88, 'tcpi_snd_cwnd': 1, 'tcpi_advmss': 0}|
|Command: event metadata_ping                                                                                                                                                                                                         |
|=====================================================================================================================================================================================================================================|
```

## The Test Suite

The test suite commands compare query results to a predefined trusted set of results. Commands: `test case`, `test suite`.
*(Source content for the linked Test Suite section was in the orphaned `x02-cli/test suites.md` file and was not available at reorg time — link pending.)*

## High Availability Tests

Tests relating to High Availability are detailed in the High Availability section. The HA test commands are:
`test cluster setup`, `test cluster data`, `test cluster databases`, `test cluster partitions`.
