---
title: Node Status
description: Validate node is connected to the network
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-25 | updated hyperlinks
--> 

A key component of AnyLog is the having nodes able to communicate between one another, in order to share both data and 
metadata. As such, validating the state of the node - both in terms of running services and network connectivity is 
crucial. 

> Parts of this document are a repeat for <a href="{{ '/docs/CLI/AnyLog-CLI/' | relative_url }}">AnyLog CLI</a>

## Validating Services 

### get processes

Lists all background services, their status, and key configuration details. See <a href="{{ '/docs/Network-Services/background-services/' | relative_url }}">Background Services</a>.

```anylog
get processes
get processes where format = json
```

### get connections

Returns the IPs and ports the node is listening on:

```anylog
get connections
```

Example output:
```
Type      External               Local                  Bind
---------|----------------------|-----------------------|----------------------|
TCP      |172.233.208.212:32348 |172.233.208.212:32348  |172.233.208.212:32348 |
REST     |172.233.208.212:32349 |172.233.208.212:32349  |0.0.0.0:32349         |
Messaging|172.233.208.212:32550 |172.233.208.212:32550  |0.0.0.0:32550         |
```
When you'll notice that the TCP connection has a static IP and Port (`172.233.208.212:32348`) - this means
it is bound against `172.233.208.212`. While a non-bound IP is `0.0.0.0`. 

## Validating Network Connectivity

### get status
 
Returns whether the node is running, its assigned name, and optional extra metrics:
 
```anylog
get status
get status where format = json
```
 
Extend the response to include monitored variables:
```anylog
get status where include = !!cpu_percent and include = !!disk_free
```
 
Example response:
```json
{
  "assigned_name": "bachelor-query@172.233.208.212:32348",
  "status": "running",
  "profiling": false
}
```
 
Issue against a peer node:
```anylog
run client (10.0.0.78:7848) get status
```

### Test Node 

The `test node` command verifies that the node's TCP and REST services are reachable. In addition, the command also 
checks that the local copy of the blockchain ledger is not malformed or corrupted in someway. 

```anylog
test node
```

### Test Network 

The test network command checks connectivity between the current node and other nodes in the AnyLog network.
In addition, the command can also check whether all the nodes have the same version of the metadata  


```anylog 
# basic check network status 

test network 

# check blockchain metadata version across the nodes in the network

test network metadata version
```


#### Network Error

If a node fails to respond, a pop-up text will be provided showing the exact details of the issue. Example shown below. 

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
