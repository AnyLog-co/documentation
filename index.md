---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
title: EdgeLake
nav_order: 1
---
# EdgeLake

Transform your edge nodes into members of a permissioned decentralized network, optimized to manage and monitor data and resources at the edge.
* Deploy EdgeLake instances on your nodes at the edge. 
* Enable services on each node. 
* Stream data from your PLCs, Sensors, and applications to the edge nodes. 
* Query the distributed data from a single point (as if the data is hosted in a centralized database). 
* Manage your edge resources from a single point (the network of nodes reflects a [Single System Image](https://en.wikipedia.org/wiki/Single_system_image)).

### Table of Content
* [How it Works](#how-it-works)
* [Download & Install](#download-and-install)
* [Prerequisite & Setup Considerations](#prerequisite-and-setup-considerations)


## How it Works
* By deploying EdgeLake on a node, the node joins a decentralized, P2P network of nodes.
* Using a network protocol and a shared metadata layer, the nodes operate as a single machine that is optimized to capture, host, manage and query data at the edge. 
* The nodes share a metadata layer. The metadata includes policies that describe the schemas of the data, the data distribution, the participating nodes, security and data ownerships and more. 
The shared metadata is hosted in one of the following:
  * A member node designated as a Master Node.
  * A blockchain (making the network fully decentralized).
* Each node in the network is configured to provide data services. Examples of services:
  * Capture data via _REST_, _MQTT_, _gRPC_, _JSON Files_.
  * Host data in a local database (like _SQLite_ or _PostgreSQL_, _MongoDB_).
  * Satisfy Queries.

When an application issues a query, it is delivered to one of the nodes in the network. This node serves as an orchestrator of the query and operates as follows:
Using the shared metadata, the node determines which are the target nodes that host the relevant data. The query is transferred to the target nodes and the replies from all the target nodes are aggregated dynamically and returned as a unified reply to the application. 
This process is similar to [MapReduce](https://en.wikipedia.org/wiki/MapReduce), whereas the target nodes are determined dynamically by the query and the shared metadata. Monitoring of resources operates in a similar way.

Deploying an EdgeLake node and making the node a member of a network is done as follows:
* [Download and install](#download-and-install) the EdgeLake software on the Edge Node.
* Enable the services that determine the functionalities provided by the node. 
  
Services are enabled by one, or a combination of the following:
* Issuing configuration commands using the Node's Command Line Interface (CLI).
* Listing configuration commands in script files and associating the node with the files.
* Listing configuration commands in policies that are hosted in the shared metadata and associating the node with the policies.
   
The services configured determine the role of a node which can be one or multiple of the following:  
* **Operator Node** - a node that captures data and hosts the data on a local DBMS. Data sources like devices, PLCs and applications deliver data to Operator Nodes for storage. 
* **Query Node** - a node that orchestrates a query process. Applications deliver their queries to Query Nodes, these nodes interact with Operator Nodes (that host the data) to return a unified and complete reply for each query. 
* **Master Node** - a node that replaces a blockchain platform for storage of metadata policies. The network metadata is organized in Policies and users can associate a blockchain or alternatively a Master Node for metadata storage.

In a deployed network, devices, sensors, PLCs and applications send their data to Operator Nodes. Data management on 
each Operator Node is automated.   
Queries are satisfied by Query Nodes as if all the distributed data is managed in a centralized database.     
The same setup monitors edge resources - for example, users and applications can monitor CPU, Network, disk-space, 
of the distributed edge resources from a single point.

## Download and Install

Detailed directions for Install EdgeLke can be found in [docker-compose repository](https://github.com/EdgeLake/docker-compose)

**Prepare Node(s)**:
<ol start="1">
  <li>Install requirements
    <ul style="padding-left: 20px;">
      <li>Docker</li>
      <li>docker-compose</li>
      <li>Makefile</li>
    </ul>
  </li>
  <li>Clone <i>docker-compose</i> repository from EdgeLake</li>
  <pre class="code-frame"><code class="language-shell">sudo snap install docker
sudo apt-get -y install docker-compose 
sudo apt-get -y install make
 
# Grant non-root user permissions to use docker
USER=`whoami` 
sudo groupadd docker 
sudo usermod -aG docker ${USER} 
newgrp docker
</code></pre>

<b>Deploy EdgeLake</b>:
<li>Update <code>.env</code> configurations for the node(s) being deployed -- specifically <code>LEDGER_CONN</code> for <i>Query Nodes</i> and <i>Operator Nodes</i>
    <ul style="padding-left: 20px;">
      <li><a href="https://github.com/EdgeLake/docker-compose/tree/main/docker_makefile/edgelake_master.env" target="_blank">master node</a></li>
      <li><a href="https://github.com/EdgeLake/docker-compose/tree/main/docker_makefile/edgelake_operator.env" target="_blank">operator node</a></li>
      <li><a href="https://github.com/EdgeLake/docker-compose/tree/main/docker_makefile/edgelake_query.env" target="_blank">query node</a></li>
    </ul>
</li>
<pre class="code-frame"><code class="language-config">#--- General ---
# Information regarding which EdgeLake node configurations to enable. By default, even if everything is disabled, EdgeLake starts TCP and REST connection services.
NODE_TYPE=master
# Name of the EdgeLake instance
NODE_NAME=anylog-master
# Owner of the EdgeLake instance
COMPANY_NAME=New Company

#--- Networking ---
# Port address used by EdgeLake's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32048
# Port address used by EdgeLake's REST protocol
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
DEPLOY_LOCAL_SCRIPT=false
</code></pre>

<li>Start Node using <i>makefile</i></li>
<pre class="code-frame"><code class="language-shell">make up [NODE_TYPE]

# examples
make up master
make up operator
make up query
</code></pre></ol>

## Prerequisite and Setup considerations
<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Requirement</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Operating System</td>
      <td>Linux (Ubuntu, RedHat, Alpine, Suse), Windows, OSX</td>
    </tr>
    <tr>
      <td>Memory footprint</td>
      <td>100 MB available for EdgeLake deployed without Docker</td>
    </tr>
    <tr>
      <td></td>
      <td>300 MB available for EdgeLake deployed with Docker</td>
    </tr>
    <tr>
      <td>Databases</td>
      <td>PostgreSQL installed (optional)</td>
    </tr>
    <tr>
      <td></td>
      <td>SQLite (default, no need to install)</td>
    </tr>
    <tr>
      <td></td>
      <td>MongoDB installed (Only if blob storage is needed)</td>
    </tr>
    <tr>
      <td>CPU</td>
      <td>Intel, ARM and AMD are supported.</td>
    </tr>
    <tr>
      <td></td>
      <td>EdgeLake can be deployed on a single CPU machine and up to the largest servers (can be deployed on gateways, Raspberry PI, and all the way to the largest multi-core machines).</td>
    </tr>
    <tr>
      <td>Storage</td>
      <td>EdgeLake supports horizontal scaling - nodes (and storage) are added dynamically as needed, therefore less complexity in scaling considerations. Requirements are based on expected volume and duration of data on each node. EdgeLake supports automated archival and transfer to larger nodes (if needed).</td>
    </tr>
    <tr>
      <td>Network</td>
      <td>Required: a TCP based network (local TCP based networks, over the internet and combinations are supported)</td>
    </tr>
    <tr>
      <td></td>
      <td>An overlay network is recommended. Most overlay networks can be used transparently. Nebula used as a default overlay network.</td>
    </tr>
    <tr>
      <td></td>
      <td>Static IP and 3 ports open and accessible on each node (either via an Overlay Network, or without an Overlay).</td>
    </tr>
    <tr>
      <td>Cloud Integration</td>
      <td>Build in integration using REST, Pub-Sub, and Kafka.</td>
    </tr>
    <tr>
      <td>Deployment options</td>
      <td>Executable (can be deployed as a background process), or Docker or Kubernetes.</td>
    </tr>
  </tbody>
</table>


**Comments**:
* Databases: 
  - SQLite recommended for smaller nodes and in-memory data.
  - PostgreSQL recommended for larger nodes.
  - MongoDB used for blob storage.
  - Multiple databases can be deployed and used on the same node.
    
* Network:
    An Overlay network is recommended for the following reasons:
    - Isolate the network for security considerations.
    - Manage IP and Ports availability. Without an overlay network, users needs to configure and manage availability 
      of IP and Ports used.
