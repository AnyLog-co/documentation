# Overlay Networks

AnyLog utilizes overlay networks to allow nodes distributed across separate subnetworks to behave as if they are all on 
the same network. For demonstration purposes, we use **Nebula**, an open-source overlay network developed by the Slack 
team and now maintained by <a href="https://www.defined.net/" target="_blank">Defined</a>.

**Documentation**
* <a href="https://github.com/slackhq/nebula" target="_blank">Nebula GitHub Repository</a>
* <a href="https://nebula.defined.net/docs" target="_blank">Nebula Documentation</a>
* <a href="https://www.defined.net/" target="_blank">Defined's Website</a>

## Overview of Nebula's Architecture
Nebula's overlay network requires a minimum of two types of nodes: **Lighthouse** and regular nodes, also known as 
**Hosts**. In addition, authentication certificates are required for nodes to securely communicate with each other within 
the network.

### Terminology
* **Lighthouse** is a Nebula node responsible for facilitating node discovery. It acts as a static reference point, 
allowing other nodes (hosts) to locate each other. When host1 sends data to host2, the data is sent directly between the 
hosts. The lighthouse helps by providing host1 with the necessary information (like the IP address) to locate and connect 
with host2.
<br/>
To avoid reliance on a single lighthouse, Nebula supports configurations for 
<a href="https://www.defined.net/blog/newsletter-admin-api-cert-rotation-multiple-lighthouses/#support-for-multiple-lighthouses" target="_blank">multiple lighthouses</a>. 
We recommend using either a _generic_ or _query_ node to serve as the lighthouse.


* **Host** is any Nebula node in the network (e.g., server, laptop, phone, tablet). Each host has its own private key, 
which is used to verify its identity when establishing Nebula tunnels with other nodes.


* **Certificate Authority (CA)** is composed of two files: a _CA certificate_ (`ca.crt`) and an associated _private key_
(`ca.key`). The CA certificate is shared with and trusted by every host in the network. he CA private key, however, should 
be kept secure and offline, as it is used to sign new host certificates. The CA certificate is used by hosts to verify 
the authenticity of other nodes and should be shared with all hosts in the network.

## Deploy Nebula via AnyLog
AnyLog simplifies the process of setting up a Nebula-based overlay network by providing pre-configured keys for the 
lighthouse instance and a default **CIDR** value of `10.10.1.1/24`. This setup allows new nodes to seamlessly join the 
overlay network.

When using the default CIDR address, nodes distinguish themselves based on the `LIGHTHOUSE_NODE_IP`, which is the physical 
IP address of the node functioning as the Nebula lighthouse. This ensures effective node identification and connection 
within the network.

For a unique or custom CIDR value, AnyLog will generate new lighthouse keys as needed. However, it is the user's 
responsibility to transfer the appropriate keys (e.g., host certificates) to each node to ensure they are associated 
with the overlay network. Alternatively, users can also opt to deploy their own [Nebula](nebula.md) or any other overlay 
network. In such case, only the `OVERLAY_IP` environment variable needs to be set to integrate with the AnyLog deployment.

### Requirements
 
Nebula uses port 4242 (by default) as an entry point for communication between Nebula nodes. 

### Steps

In the following example, a **generic node** will be used as the Nebula lighthouse, while both the **operator** and 
**query** nodes will function as hosts, with the default CIDR. Note that the generic node will not appear on the 
blockchain, as it primarily serves as a "sandbox" with only TCP and REST services enabled.

**For Lighthouse**: The following section explains how to deploy a generic/sandbox AnyLog instance to serve as a 
Lighthouse for the overlay network. The same process can be applied to any other node intended to act as a lighthouse. 
To deploy <a href="https://www.defined.net/blog/newsletter-admin-api-cert-rotation-multiple-lighthouses/#support-for-multiple-lighthouses" target="_blank">multiple lighthouse instances</a>, 
you will need to modify the Nebula configuration file manually, as this feature is not supported by the autogenerated 
configuration file.

1. In advanced configs, set the overlay IP address and update nebula configs as shown below. 
The CIDR_OVERLAY_ADDRESS should have the same IP value as the overlay IP address.
```dotenv
... 
#--- Networking ---
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=10.10.1.1
# The number of concurrent threads supporting HTTP requests.
TCP_THREADS=6
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
REST_TIMEOUT=30
...
 
#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# create new nebula keys
NEBULA_NEW_KEYS=false
# whether node is type lighthouse
IS_LIGHTHOUSE=true
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24)
CIDR_OVERLAY_ADDRESS=10.10.1.1/24
# Nebula IP address for Lighthouse node (ex. 10.10.1.15)
LIGHTHOUSE_IP=""
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=""
```

2. Start Node
```shell 
make up ANYLOG_TYPE=generic
```

3. Validate node is working with overlay - the reason blockchain fails is that a generic node does not declare itseelf 
against a master of blockchain. 
```shell    
make test-node

<<COMMENT
root@localhost:~/docker-compose# make test-node
REST Connection Info for testing (Example: 127.0.0.1:32149):
10.10.1.1:32549
Node State against 10.10.1.1:32549
anylog-node@172.232.20.156:32548 running

Test                                    Status                                                               
---------------------------------------|--------------------------------------------------------------------|
Metadata Version                       |                                                                   0|
Metadata Test                          |Failed                                                              |
TCP test using 10.10.1.1:32548         |[From Node 10.10.1.1:32548] anylog-node@172.232.20.156:32548 running|
REST test using http://10.10.1.1:32549 |anylog-node@172.232.20.156:32548 running                            |


Process         Status       Details                                                                                          
---------------|------------|------------------------------------------------------------------------------------------------|
TCP            |Running     |Listening on: 172.232.20.156:32548 and 10.10.1.1:32548, Threads Pool: 6                         |
REST           |Running     |Listening on: 172.232.20.156:32549 and 10.10.1.1:32549, Threads Pool: 6, Timeout: 30, SSL: False|
Operator       |Not declared|                                                                                                |
Blockchain Sync|Not declared|                                                                                                |
Scheduler      |Running     |Schedulers IDs in use: [0 (system)]                                                             |
Blobs Archiver |Not declared|                                                                                                |
MQTT           |Not declared|                                                                                                |
Message Broker |Not declared|No active connection                                                                            |
SMTP           |Not declared|                                                                                                |
Streamer       |Not declared|                                                                                                |
Query Pool     |Running     |Threads Pool: 3                                                                                 |
Kafka Consumer |Not declared|                                                                                                |
gRPC           |Not declared|                                                                                                |
Publisher      |Not declared|                                                                                                |
Distributor    |Not declared|                                                                                                |
Consumer       |Not declared|                                                                                                |
<<     
```

**For Hosts**: The following section explains how to add a new AnyLog node to the overlay network. In this example, 
we’ll use a Query node, but the same process applies to Operator, Publisher, or Master nodes that function as Host nodes 
in Nebula.

1. In advanced configs, set the overlay IP address and update nebula configs as shown below. 
The LIGHTHOUSE_IP should be the same as the CIDR_OVERLAY_ADDRESS, but without the prefix value.
```dotenv
...
#--- Networking ---
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=10.10.1.31
# Port value to be used as an MQTT broker, or some other third-party broker
ANYLOG_BROKER_PORT=""```
...

#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# create new nebula keys
NEBULA_NEW_KEYS=false
# whether node is type lighthouse
IS_LIGHTHOUSE=false
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24)
CIDR_OVERLAY_ADDRESS=10.10.1.1/24
# Nebula IP address for Lighthouse node (ex. 10.10.1.15)
LIGHTHOUSE_IP=10.10.1.1
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=172.232.250.209
```

2. Start Node
```shell 
make up ANYLOG_TYPE=query
```

3. To validate overlay is running properly, users can attach into the AnyLog docker container and run `get status` 
against the generic / lighthouse node.
```anylog
EL anylog-query +> run client (10.10.1.1:32548) get status 

[From Node 10.10.1.1:32548] 

'anylog-node@10.10.1.1:32548 running'
```

4. Validate node is configured properly
```shell
make test-node

<<COMMENT
REST Connection Info for testing (Example: 127.0.0.1:32149):
172.232.209.244:32349
Node State against 172.232.209.244:32349
anylog-query@10.10.1.31:32348 running

Test                                     Status                                                             
----------------------------------------|------------------------------------------------------------------|
Metadata Version                        |fcb2a29a294853c6ee289079e761a53d                                  |
Metadata Test                           |Pass                                                              |
TCP test using 10.10.1.31:32348         |[From Node 10.10.1.31:32348] anylog-query@10.10.1.31:32348 running|
REST test using http://10.10.1.31:32349 |anylog-query@10.10.1.31:32348 running                             |


Process         Status       Details                                                                                       
---------------|------------|---------------------------------------------------------------------------------------------|
TCP            |Running     |Listening on: 10.10.1.31:32348, Threads Pool: 6                                              |
REST           |Running     |Listening on: 172.18.0.3:32349 and 10.10.1.31:32349, Threads Pool: 6, Timeout: 30, SSL: False|
Operator       |Not declared|                                                                                             |
Blockchain Sync|Running     |Sync every 30 seconds with master using: 10.10.1.10:32048                                    |
Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                                               |
Blobs Archiver |Not declared|                                                                                             |
MQTT           |Not declared|                                                                                             |
Message Broker |Not declared|No active connection                                                                         |
SMTP           |Not declared|                                                                                             |
Streamer       |Not declared|                                                                                             |
Query Pool     |Running     |Threads Pool: 3                                                                              |
Kafka Consumer |Not declared|                                                                                             |
gRPC           |Not declared|                                                                                             |
<<
```

### Communication Between Nodes
The following example shows that a request sent from the query node to the operator uses the overlay IP addresses

**Node Communication**: On the query node, check which nodes on the network the query node can communicate with
```anylog
EL anylog-query +> test network 
                                                                      
Test Network
[****************************************************************]

EL anylog-query +> 
Address          Node Type Node Name       Status 
----------------|---------|---------------|------|
10.10.1.10:32048|master   |anylog-master  |  +   |
10.10.1.31:32348|query    |anylog-query   |  +   |
10.10.1.21:32148|operator |anylog-operator|  +   |
```

**Sample Query**:
```anylog 
EL anylog-query +> run client () sql new_company format=table "select timestamp, value FROM rand_data WHERE timestamp >= NOW() - 15 seconds;" 
[5]
EL anylog-query +> 
timestamp                  value
-------------------------- ------- 
2024-10-16 00:45:00.805401 112.903 
2024-10-16 00:45:01.306022  44.985 
2024-10-16 00:45:01.806653 279.884 
2024-10-16 00:45:02.307448 473.934 
2024-10-16 00:45:02.808262 571.268 
2024-10-16 00:45:03.308946  186.11 
2024-10-16 00:45:03.809610   3.015 
2024-10-16 00:45:04.310321 184.297 
2024-10-16 00:45:04.810974  46.105 
2024-10-16 00:45:05.311127   6.686 

{"Statistics":[{"Count": 10,
                "Time":"00:00:00",
                "Nodes": 1}]}
```

**Query Status**: Notice data is arriving from the OVERLAY_IP
```anylog
EL anylog-query +> query status 

Job  ID Output Run Time Operator         Par Status    Blocks Rows Command                                                                       
----|--|------|--------|----------------|---|---------|------|----|-----------------------------------------------------------------------------|
0005| 6|stdout|00:00:00|All             |---|Completed|     1|  10|select timestamp, value FROM rand_data WHERE timestamp >= NOW() - 15 seconds;|
    |  |      |00:00:00|10.10.1.21:32148|  0|Completed|     1|  10|                                                                             |
```