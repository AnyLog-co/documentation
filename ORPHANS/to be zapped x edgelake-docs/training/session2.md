---
layout: default
parent: Training
title: Session II
nav_order: 4
---
# Deployment of the Test Network

This document describes how to deploy and configure an AnyLog/EdgeLake Network. This guided session provides directions to
deploy an AnyLog/EdgeLake Network consisting of 4 nodes (2 operators, 1 query, 1 master).

When an EdgeLake node is deployed, the software packages needs to be organized on the node with proper configurations.  
Each EdgeLake Node is using the same software stack, however, the nodes in the network are assigned to different roles, 
and these roles are determined by the configurations.    

The main roles are summarized in the table below:

<table>
    <tr>
        <td style="text-align: center"><b>Node Type</b></td>
        <td style="text-align: center"><b>Functionality</b></td>
    </tr>
    <tr>
        <td><a href="https://github.com/EdgeLake/docker-compose/blob/main/docker_makefile/edgelake_master.env" target="_blank">Master</a></td>
        <td>A node that manages the shared metadata (if a blockchain platform is used, this node is redundant)</td>
    </tr>
    <tr>
        <td><a href="https://github.com/EdgeLake/docker-compose/blob/main/docker_makefile/edgelake_operator.env" target="_blank">Operator</a></td>
        <td>A node that hosts the data. In this session, users deploy 2 Operator nodes</td>
    </tr>
    <tr>
        <td><a href="https://github.com/EdgeLake/docker-compose/blob/main/docker_makefile/edgelake_query.env" target="_blank">Query</a></td>
        <td>A node that coordinates the query process</td>
    </tr>
</table>

Additional information on the types of nodes is in the [Getting Started](../../getting_started/) document.

The roles are determined by configuration commands which are processed by each node at startup and enable services 
offered by the node. The same node may be assigned to multiple roles - there are no restrictions on the services that 
can be offered by a node.

Since configuration is "command based", it is simple to change configurations, and even dynamically (using the CLI),
by disabling a service or enabling a service using the proper commands.  

In this training, users will be using the default configuration file, and make some modifications to support their
proprietary settings.

### This session includes 4 sections:
1. [Prerequisites & Support Software](#prerequisites--support-software)
2. [Network Configurations](#network-configurations)
3. [Deploy EdgeLake](#deploy-edgelake)
4. [Configuring Node](#configuring-node) 
5. [Test & Query EdgeLake](#test--query-edgelake)

## Prerequisites & Support Software
### Prerequisites 
Prior to this session, users are required to prepare:
<ul>
    <li>4 machines (virtual or physical) to host the EdgeLake nodes, as follows:
        <ul style="padding-left: 20px">
            <li>Linux, Windows or MacOSX environment with the following programs: 
                <ul>
                    <li><a href="https://docs.docker.com/engine/install/" target="_blank">Docker</a></li>
                    <li><a href="https://www.gnu.org/software/make/manual/make.html" target="_blank">Makefile</a></li>
                </ul>
            </li>
            <li>A minimum of 512MB of RAM</li>
            <li>A minimum of 10GB of disk space</li>
        </ul>
    </li>
    <li>1 Machine (physical or virtual) for applications that interact with the network (i.e. Grafana), as follows
        <ul style="padding-left: 20px">
            <li>Linux, Windows or MacOSX environment</li>
            <li>A minimum of 256MB of RAM</li>
            <li>A minimum of 10GB of disk space</li>
        </ul>
    </li>
    <li>Each node accessible by IP and Port (remove firewalls restrictions)</li>
</ul>

The prerequisites for a customer deployment are available [here](prerequisite.md).

**Note**: We recommend deploying an overlay network, such as <a herf="https://github.com/AnyLog-co/documentation/blob/master/deployments/Networking%20&%20Security/nebula.md" target="_blank">nebula</a>.
 * It provides a mechanism to maintain static IPs.
 * It provides the mechanisms to address firewalls limitations.
 * It isoltates the network addressing security considerations. 

**Note 3** If an overlay network is not used in the training, remove firewalls restrictions to allow for nodes to 
communicate with peers and with 3rd parties applications.


### Support Software

The following table summarizes the commonly used packages deployed with EdgeLake.
<table>
    <tr>
        <td style="text-align: center"><b>Software</b></td>
        <td style="text-align: center"><b>Functionality</b></td>
    </tr>
    <tr>
        <td><a href="../../northbound/remote_cli">Remote-CLI</a></td>
        <td>A web based interface to the network</td>
    </tr>
    <tr>
        <td><a href="https://www.postgresql.org/" target="_blank">PostgreSQL</a></td>
        <td>SQL-based local database</td>
    </tr>
    <tr>
        <td><a href="https://www.mongodb.com/" target="_blank">MongoDB</a></td>
        <td>Local database for unstructured data</td>
    </tr>
    <tr>
        <td>Northbound Visualization Tool
            <ul>
                <li><a href="../../northbound/Grafana">Grafana</a></li>
                <li><a href="../../northbound/PowerBI">PowerBI</a></li>
            </ul>
        </td>
        <td>BI tool for visualization of the data</td>
    </tr>
    <tr>
        <td>Southbound Data Generators
            <ul>
                <li><a href="../../southbound/edgex">EdgeX</a></li>
                <li><a href="../../southbound/fledge">FLEDGE</a></li>
                <li><a href="../../southbound/node_red">Node-RED</a></li>
            </ul>
        </td>
        <td>A connector to PLCs and sensors</td>
    </tr>
</table>


#### In this session, users will use the following packages:
* SQLite that serves as the local database (and is available by default without a dedicated install).
* Remote CLI - a WEB based application that interact with nodes in the network via REST. The Remote CLI is deployed with the Query Node.
* Grafana - a visualization application deployed on a dedicated node, as an example for an application interacting with the network data.


## Static IPs
EdgeLake requires static IPs for the nodes in the network. With cloud instances, users may require some cloud specific configuration
in order to enable static IPs. 
* <a href="https://cloud.google.com/compute/docs/ip-addresses/configure-static-external-ip-address" target="_blank">Google Cloud</a>
* <a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html" target="_blank">AWS</a>
* <a href="https://learn.microsoft.com/en-us/azure/virtual-network/ip-services/virtual-networks-static-private-ip-arm-pportal" target="_blank">Azure</a>

### Network Configurations
Users can configure the nodes to use any valid IP and Port. 

For simplicity, the default setup is associating the same port values to nodes of the same type. The following tables 
summarizes the default port values used by EdgeLake.

<table>
    <tr>
        <td style="text-align: center"><b>Node Type</b></td>
        <td style="text-align: center"><b>TCP</b></td>
        <td style="text-align: center"><b>REST</b></td>
        <td style="text-align: center"><b>Message Broker</b></td>
    </tr>
    <tr>
        <td>Master</td>
        <td style="text-align: right">32048</td>
        <td style="text-align: right">32049</td>
    </tr>
    <tr>
        <td>Operator</td>
        <td style="text-align: right">32148</td>
        <td style="text-align: right">32149</td>
        <td style="text-align: right">32150</td>
    </tr>
    <tr>
        <td>Query</td>
        <td style="text-align: right">32348</td>
        <td style="text-align: right">32349</td>
    </tr>
</table>

**Note**: 
* The port designated as **TCP** is used by the EdgeLake protocol when messages are send between nodes of the network. 
* The port designated as **REST** is used to message a node using the REST protocol. 3rd party apps would be using 
REST to communicate with nodes in the network.
* The port designated as **Message Broker** is optional and is used to accept message from 3rd party apps like Kafka
and MQTT

<h3>The Network ID</h3>

* With a Master Node deployment, the network ID is the Master's IP and Port.
* A node can leverage any valid IP and port. In this deployment, the nodes are using their default IP 
(the IP that identifies the node on the network), and the ports are set by default as described above.

<b>In this setup, the network ID is the IP of the Master and port 32048.</b>

If the default IP is not known, when the Master node is initiated, the command <code class="language-anylog">get connections</code> 
on the node CLI returns the IPs and ports used - the Network ID is the IP and port assigned to TCP-External.


## Deploy EdgeLake

Detailed directions for deploying each node can be found in [Fast Deployment](fast_deployment.md) document.

<ol start="0">
    <li>Clone docker-compose from EdgeLake repository
        <pre class="code-frame"><code class="language-shell">git clone https://github.com/EdgeLake/docker-compose
cd docker-compose</code></pre>
    </li>
    <li>Edit <code class="langauge-anylog">LEDGER_CONN</code> in <i>Query</i> and <i>Operator</i> using IP address of master node</li>
    <li>Update .env configurations for the node(s) being deployed
        <ul>
            <li><a href="https://github.com/EdgeLake/docker-compose/blob/main/docker_makefile/edgelake_master.env" target="_blank">docker_makefile/edgelake_master.env</a></li>
            <li><a href="https://github.com/EdgeLake/docker-compose/blob/main/docker_makefile/edgelake_operator.env" target="_blank">docker_makefile/edgelake_operator.env</a></li>
            <li><a href="https://github.com/EdgeLake/docker-compose/blob/main/docker_makefile/edgelake_query.env" target="_blank">docker_makefile/edgelake_query.env</a></li>
        </ul>
        <br/>
        <b>Sample Configuration File</b>:
        <pre class="code-frame"><code class="language-configs">#--- General ---
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols
NODE_TYPE=master
# Name of the AnyLog instance
NODE_NAME=anylog-master
# Owner of the AnyLog instance
COMPANY_NAME=New Company

#--- Networking ---
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32048
# Port address used by AnyLog's REST protocol
ANYLOG_REST_PORT=32049
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
TCP_BIND=false
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
REST_BIND=false

#--- Blockchain ---
# TCP connection information for Master Node
LEDGER_CONN=127.0.0.1:32048

#--- Advanced Settings ---
# Whether to automatically run a local (or personalized) script at the end of the process
DEPLOY_LOCAL_SCRIPT=false</code></pre></li>
    <li>Start Node using makefile
        <pre class="code-frame"><code class="language-configs">make up EDGELAKE_TYPE=[NODE_TYPE]</code></pre>
    </li>
</ol>

<h3>Makefile Commands for Docker</h3>

<ul>
    <li>Help
        <pre class="code-frame"><code class="language-shell">Usage: make [target] EDGELAKE_TYPE=[anylog-type]
Targets:
  build       Pull the docker image
  up          Start the containers
  attach      Attach to EdgeLake instance
  exec        Attach to shell interface for container
  down        Stop and remove the containers
  logs        View logs of the containers
  clean       Clean up volumes and network
  help        Show this help message
         supported EdgeLake types: master, operator and query
Sample calls: make up EDGELAKE_TYPE=master | make attach EDGELAKE_TYPE=master | make clean EDGELAKE_TYPE=master</code></pre>
    </li>
    <li>Bring up (Query) Node
        <pre class="code-frame"><code class="language-shell">make up EDGELAKE_TYPE=query</code></pre>
    </li>
    <li>Attach to (Query) Node
        <pre class="code-frame"><code class="language-shell"># to detach: ctrl-d
make attach EDGELAKE_TYPE=query</code></pre>
    </li>
    <li>Bring down (Query) Node
        <pre class="code-frame"><code class="language-shell">make down EDGELAKE_TYPE=query</code></pre>
    </li>
    <li>Clean (Query) Node - this removes the volume(s) and image from disk
        <pre class="code-frame"><code class="language-shell">make clean EDGELAKE_TYPE=query</code></pre>
    </li>
</ul>

## Configuring Node
For the demo purposes, everything should deploy automatically using configuration policies.

<ol start="1">
    <li>Based on used environment parameters (<code>.env</code> file), set EdgeLake parameters to be used</li>
    <li>Connect to network services (TCP and REST)
        <pre class="code-frame"><code class="language-anylog"># TCP Server
&lt;run tcp server where
  external_ip = [ip] and external_port = [port] and
  internal_ip = [local_ip] and internal_port = [local_port] and
  bind = [true/false] and threads = [threads count]&gt;

# REST server
&lt;run rest server where
  external_ip = [external_ip ip] and external_port = [external port] and
  internal_ip = [internal ip] and internal_port = [internal port] and
  timeout = [timeout] and ssl = [true/false] and bind = [true/false]&gt;
</code></pre>
    </li>
    <li>Using <code class="language-anylog">blockchain seed</code>, get the latest copy of the blockchain
        <pre class="code-frame"><code class="language-anylog">blockchain seed from !ledger_conn</code></pre>
    </li>
    <li>Declare Node policy - in Operator Node, it also creates the correlating Cluster Policy
        <pre class="code-frame"><code class="language-json">{"operator": {
    "name": "anylog-operator",
    "company": "AnyLog Co.",
    "ip": "136.23.47.189",
    "local_ip": "136.23.47.189",
    "port": 32148,
    "rest_port": 32149,
    "cluster": "f3e300855609ba4fc83b550179f584a4",
    "loc": "37.425423, -122.078360",
    "country": "US",
    "state": "CA",
    "city": "Mountain View"
}}
</code></pre>
    </li>
    <li>connect to logical database(s)
        <pre class="code-frame"><code class="language-anylog"># Master Node
connect dbms blockchain where type=sqlite

# Operator Node
connect dbms [DEFAULT_DBMS] where type=psql and host=127.0.0.1 and port=5432 and user=!db_user and port=!db_port
connect dbms almgm where type=psql and host=127.0.0.1 and port=5432 and user=!db_user and port=!db_port

# Query Node
connect dbms system_query where type=sqlite and memory=true</code></pre>
    </li>
    <li>Run blockchain sync
        <pre class="code-frame"><code class="language-anylog">run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn</code></pre>
    </li>
    <li>Monitor nodes - send Remote-CLI information like <code>cpu utilization</code>, <code>disk space</code> and <code>memory usage</code></li>
    <li>When setting <code>ENABLE_MQTT</code> to <i>true</i> on an Operator Node, that will automatically flow in from a 3rd party application via MQTT
        <pre class="code-frame"><code class="language-anylog">&lt;run msg client client where broker=139.144.46.246 and port=1883 and user=anyloguser and password=mqtt4AnyLog! and log=false and topic=(
    name=anylog-demo and
    dbms="bring [dbms]" and
    table="bring [table]" and 
    column.timestamp.timestamp="bring [timestamp]" and 
    column.value=(type=float and value="bring [value]")
)&gt;</code></pre>
    </li>
</ol>

## Test & Query EdgeLake

### Validate Node is Running

<ol start="1">
    <li>Validate node is reachable by the network members - On each deployed node issue the command
        <pre class="code-frame"><code class="language-anylog">test network</code></pre>
The command returns the list of registered nodes in the network and validates that the members are reachable using their 
published IPs and Ports. For each node, the value in the status column needs to be the plus sign (<b>+</b>) that designates connectivity.    
if the plus sign is missing, the node is down or not reachable.
    </li>
    <li>View the background processes enabled using the command
        <pre class="code-frame"><code class="language-anylog">get processes

# Sample processes for Operator Node:
    Process         Status       Details                                                                      
    ---------------|------------|----------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.105.86.168:32148, Threads Pool: 6                         |
    REST           |Running     |Listening on: 172.105.86.168:32149, Threads Pool: 5, Timeout: 20, SSL: False|
    Operator       |Running     |Cluster Member: True, Using Master: 45.79.74.39:32048, Threads Pool: 3      |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                  |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                              |
    Blobs Archiver |Running     |                                                                            |
    MQTT           |Running     |                                                                            |
    Message Broker |Running     |Listening on: 172.105.86.168:32150, Threads Pool: 5                         |
    SMTP           |Not declared|                                                                            |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes                |
    Query Pool     |Running     |Threads Pool: 3                                                             |
    Kafka Consumer |Not declared|                                                                            |
    gRPC           |Not declared|                                                                            |
    Publisher      |Not declared|                                                                            |
    Distributor    |Running     |                                                                            |
    Consumer       |Running     |No peer Operators supporting the cluster                                    |</code></pre>
    </li>
    <li>Communicate with peer nodes. The basic command is <code class="language-anylog">get status</code> 
(similar to <i>ping</i>) which is exemplified below (from the CLI of the master)
                <pre class="code-frame"><code class="language-anylog">EL edgelake-master > run client (198.74.50.131:32148) get status
[From Node 198.74.50.131:32148]  
'edgelake-operator_1@198.74.50.131:32148 running'</code></pre>
    </li>
    <li>On an Operator Node, users can view data coming in using an array of commands:
        <ul>
            <li>Statistics on the streaming processes
                <pre class="code-frame"><code class="language-anylog">get streaming

# Output
Flush Thresholds
Threshold        Value  Streamer 
----------------|------|--------|
Threshold Time  |    60|Running |
Threshold Volume|10,240|        |
Write Immediate |False |        |
Buffered Rows   |    49|        |
Flushed Rows    |   101|        |


Statistics
                     Put    Put     Streaming Streaming Cached Counter    Threshold   Buffer   Threshold  Time Left Last Process 
DBMS-Table           files  Rows    Calls     Rows      Rows   Immediate  Volume(KB)  Fill(%)  Time(sec)  (Sec)     HH:MM:SS     
--------------------|------|-----|-|---------|---------|------|----------|-----------|--------|----------|---------|------------|
edgex.rand_data     |     0|    0| |  243,780|  243,780|    49|         0|         10|   28.55|        60|       32|00:00:04    |</code></pre>
            </li>
            <li>Information on messages received by clients subscribed to message brokers.
                <pre class="code-frame"><code class="language-anylog">get msg client

# Output
Subscription ID: 0001
User:         anyloguser
Broker:       139.144.46.246:1883
Connection:   Connected

     Messages    Success     Errors      Last message time    Last error time      Last Error
     ----------  ----------  ----------  -------------------  -------------------  ----------------------------------
          24389       24389           0  2024-05-14 20:17:01
     
     Subscribed Topics:
     Topic       QOS DBMS  Table       Column name Column Type Mapping Function Optional Policies 
     -----------|---|-----|-----------|-----------|-----------|----------------|--------|--------|
     anylog-demo|  0|edgex|['[table]']|timestamp  |timestamp  |now()           |False   |        |
                |   |     |           |value      |float      |['[value]']     |False   |        |
    </code></pre></li>
        </ul>
    </li>
</ol>


### Sample Queries
<ul>
    <li>View list of tables 
        <pre class="code-frame"><code class="language-anylog">get tables where dbms=[DB_NAME]</code></pre>
    </li>
    <li>View columns in table
        <pre class="code-frame"><code class="language-anylog">get columns where dbms=[DB_NAME]  and table=rand_data</code></pre>
    </li>
    <li>Get row count 
        <pre class="code-frame"><code class="language-anylog"># Using AnyLog tool
get rows count where dbms=edgex and table=rand_data

# Using SQL 
run client () sql edgex "select count(*) from rand_data;"</code></pre>
    </li>
    <li>Get raw data 
        <pre class="code-frame"><code class="language-anylog">run client () sql edgex format=table "select timestamp, value from rand_data limit 100"</code></pre>
    </li>
    <li>Increment Function 
        <pre class="code-frame"><code class="language-anylog">run client () sql edgex format=table "select increments(day, 1, timestamp), min(timestamp), max(timestamp), min(value), avg(value), max(value), count(*) from rand_data"</code></pre>
    </li>
    <li>Period Function 
        <pre class="code-frame"><code class="language-anylog">run client () sql edgex format=table "select timestamp, value from rand_data where period(minute, 1, now(), timestamp)"</code></pre>
    </li>
</ul>




