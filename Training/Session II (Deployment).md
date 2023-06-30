# Session II - Deployment of the test network

If you do not have Docker credentials, or an AnyLog license key please contact us at [info@anylog.co](mailto:info@anylog.co) 

## The deployment process

This document describes how to deploy and configure an AnyLog Network. The example provides directions to:
* Deploy an  AnyLog Network consisting of  4 nodes (2 operators, 1 query, 1 master) 
* Deploy our Remote CLI - an open source web interface used for querying data 
* Configure EdgeX as a data source  
* Configure Grafana to visualize the data 

We recommend deploying an overlay network, such as [nebula](Networking%20&%20Security/nebula.md), or some other form of 
static IPs when deploying a production network.

## Nodes deployed
* Master – A node that manages the shared metadata (if a blockchain platform is used, this node is redundant).
* Operator – A node that hosts the data. For this deployment we will have 2 Operator nodes.
* Query – A node that coordinates the query process. 

**Deployment Diagram**:

![deployment diagram](../imgs/deployment_diagram.png)

## Deploy the Master Node
Assign a virtual or physical machine for a Master node and follow these steps:
1.
2.


## Deploy 2 Operator nodes
Assign 2 virtual or physical machines as Operator nodes and follow these steps:
1.
2.

## Deploy a Query node
Assign a virtual or physical machine for a Query node and follow these steps:


## Deploy the Remote CLI

Instructions to deploy the remote CLI are available [here](../deployments/Support/Remote-CLI.md).

## Deploy a data generator

## Deploy Grafana

Instructions to deploy the remote CLI are available [here](../deployments/Support/Remote-CLI.md).


## Basic operations on all nodes 

1. Log into AnyLog Docker Hub
```
docker login -u anyloguser -p ${DOCKER_LOGIN]
```

2. Start the Node
```
docker run -it --detach-keys=ctrl-d \
-e NODE_TYPE=none \
-e LICENSE_KEY=${ANYLOG_LICENSE_KEY} 
--net=host --rm anylogco/anylog-network
```

3. Set the License Key 
```
AL > set license where activation_key = !license_key
```

4. Disable Authentication

5. Enable the network protocol

```
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=true and threads=3>
```

6. Enable the REST service

```
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=false and threads=3 and timeout=30>
```

## Basic operations on specific nodes

1.  On the Master Node
* Enable the database services to host the metadata:
```
connect dbms ...
```

2.  On each Operator Node
* Enable the database services to host the user data:
```
connect dbms ...
```
* Enable the database services to support HA:
```
connect dbms ...
```
* Associate each operator with a data source
  - Operator 1, connecting to data simulator by providing a REST service:
```

```
  - Operator 2, connecting to Edgex by providing a broker service:
```

```


## Sample Commands

* _Help_ functions 
```
# general help 
help

# view help sections
help index

# list of commands associated with data streaming
help index streaming

# explanation of the command: run kafka consumer
help run kafka consumer
```

* _log_ commands
```
# view activity on the node 
get event log 

# view errors on the node 
get error log 

# for a node running a query, view the status of the query
query status [all]

# for operator and publisher nodes, view whether data is coming in 
get streaming
```

* _Local_ and _Environment_ variables
```
# view all local variables (in the AnyLog dictionary)
get dictionary 

# view Environment variables
get env vars 

# view a specific AnyLog variable  - in this case the TCP port value 
!anylog_server_port

# view a specific Environment variables
$HOME

# declare a new AnyLog variable & view it
abc = 123
!abc
```

* _Network_ Configuration 
```
# View connections 
get connections 


* Database  Configuration 
```
# connect to a logical database 
connect dbms test where  type=sqlite and memory=false 

# if you have PostgreSQL installed: 
connect dbms test where type=psql and ip=127.0.0.1 and port=5432 and user=[USERNAME] and password=[PASSWORD]

# view databases 
get databases
```
## Other Documents
* [Getting Started](../getting%20started.md)
* [Deployment Scripts](../deployments/deploying_node.md)
* [Cheatsheet](../deployments/Support/cheatsheet.md)
* Remote-CLI
  * [Deployment](../deployments/Support/Remote-CLI.md)
  * [Usage](../northbound%20connectors/remote_cli.md) 


