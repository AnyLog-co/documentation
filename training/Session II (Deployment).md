# Session II - Deployment of the test network

This session includes 4 sections:

1. An [Overview](#overview)
2. A step by step [Install](#install) of a test network
3. Connecting sample data sources and [Populating Data](#populating-data)
4. [View status and query data (using the AnyLog Node CLI)](#view-status-and-query-data-using-the-anylog-node-cli)
5. [Reference Documentation](#reference-documentation) to deploy and configure the Remote CLI and Grafana

# Overview

This document describes how to deploy and configure an AnyLog Network. This guided session provides directions to:
Deploy an  AnyLog Network consisting of  4 nodes (2 operators, 1 query, 1 master).

When an AnyLog node is deployed, the software packages needs to be organized on the node with proper configurations.  
Each AnyLog Node is using the same software stack, however, the nodes in the network are assigned to different roles, and
these roles are determined by the configurations.    
The main roles are summarized in the table below:

| Node Name (Role)  | Functionality |
| -------------     | ------------- |
| Master            | A node that manages the shared metadata (if a blockchain platform is used, this node is redundant). |
| Operator          | A node that hosts the data. In this session, users deploy 2 Operator nodes. |
| Query             | A node that coordinates the query process. |

Additional information on the types of nodes is in the [Getting Started](../getting%20started.md) document.
  
The roles are determined by configuration commands which are processed by each node at startup and enable services 
offered by the node. The same node may be assigned to multiple roles - there are no restrictions on the services that can be
offered by a node.

The following table summarizes different supported deployment and configuration options:

| Functionality  | Option         | Comments       |
| ---------------| -------------- | -------------  |
| Deployment     | Docker         | Supported      |
| Deployment     | Kubernetes     | Supported      |
| Configuration  | AnyLog CLI     | Interactively issuing configuration commands on the CLI    |
| Configuration  | REST           | Interactively issuing configuration commands via REST    |
| Configuration  | Script file    | Organizing the configuration command in a file and associating the file to a node |
| Configuration  | Questionnaire  | Creating a configuration file using a questionnaire  |
| Configuration  | Policy         | Organizing the configuration commands in a policy and associating the policy to a node |

Since configuration is "command based", it is simple to change configurations, and even dynamically (using the CLI),
by disabling a service or enabling a service using the proper commands.  

In this training, users will be using the default configuration file, and make some modifications to support their
proprietary settings.

In this session, the configuration file is named **anylog_configs.env** and sored in a folder as follows:

| Node Type         | Folder |
| -------------     | ------------- |
| Master            | deployments/docker-compose/anylog-master |
| Operator          | deployments/docker-compose/anylog-operator |
| Query             |  deployments/docker-compose/anylog-query |

Note that users can generate their own configuration files using a questionnaire, or placing the commands in files or in policies.
* The [deploying_node](../deployments/deploying_node.md) document is a guide to deploy a network using a questionnaire
that to generate the config file.
* The [Netowrk Setup](../examples/Network%20setup.md) document is a step by step guide to deploy an AnyLog network without 
a pre-existing configuration.
* The [Policies based Configuration](../policies.md#policies-based-configuration) section details how to use 
policies (placed on the shared metadata layer) to configure nodes in the network.

**Deployment Diagram**:

![deployment diagram](../imgs/deployment_diagram.png)

In this test network, data is ingested by the 2 operator nodes. 
Users interact with the network, by issuing commands and queries to the Query node, and these are satisfied as if 
the data is hosted on a single database and as if the distributed nodes are a single machine.
In addition, users will notice that data management and monitoring are automated and activated as a service by the 
proper configuration commands. 

## The deployed software

The following table summarizes the commonly used packages deployed with AnyLog.  

| Package Name                                        | Functionality | Reference Document | 
| --------------------------------------------------- | ------------- |-------------- |
| [AnyLog](https://www.anylog.co/)                    | The AnyLog software package on each node.  | [Deploying a Node](../deployments/deploying_node.md) |
| [PostgreSQL](https://www.postgresql.org/)           |  A local database.  | [PostgreSQL Install](https://www.postgresql.org/download/)|
| [MongoDB](https://www.mongodb.com/)           |  A local database for unstructured data.  | [MongoDB Download](https://www.mongodb.com/try/download/community)|
| [A data generator](https://github.com/AnyLog-co/Sample-Data-Generator)  |  A data generator that generates simulated data for learning and testing purposes.  | [Data Generator READ.ME](https://github.com/AnyLog-co/Sample-Data-Generator/blob/master/README.md)|
| [Edgex](https://www.edgexfoundry.org/)              |  A connector to PLCs and sensors.  | [EdgeX](https://docs.edgexfoundry.org/2.1/getting-started/quick-start/) |
| [Remote-CLI](../northbound%20connectors/remote_cli.md)   | A web based interface to the network.  |  |
| [Grafana](https://grafana.com/)                     |  A visualization tool. | [Get Started with Grafana](https://grafana.com/get/?plcmt=top-nav&cta=downloads&tab=self-managed) |

**In this session, users will use the following packages:**
* AnyLog - on each of the 4 network nodes. Configuration will be using the default setting (other than the changes listed below). 
* Local database is SQLite (and is available by default without a dedicated install).
* Remote CLI - deployed with the Query Node.
* Data Generator - deployed on operator I and configured to send data to both - Operator I and Operator II.
* Grafana, on a dedicated node, as an example for an application interacting with the network data.

# Install

## Prerequisites
Prior to this session, users are required to prepare:
* 4 machines (virtual or physical) to host the AnyLog nodes, as follows:
    - A Linux environment.
    - A minimum of 256MB of RAM.
    - A minimum of 10GB of disk space.
* 1 Machine (physical or virtual) for applications that interact with the network (i.e. Grafana), as follows:
    - Linux or Windows environment.
    - A minimum of 256MB of RAM.
    - A minimum of 10GB of disk space.
* Each node accessible by IP and Port (remove firewalls restrictions).
* [Docker](https://docs.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) installed (navigate to [Get Docker](https://docs.docker.com/get-docker/) site to access
   the Docker download that’s suitable for your platform).
* To enable the questionnaire (optional), install the following packages (these packages are redundant for deployments with pre-packaged configurations,
or if the questionnaire is not used to create the **anylog_configs.env** file):  
    - [Python](https://www.python.org/downloads/)
    - [Dotenv](https://pypi.org/project/python-dotenv/)     

**Note 1**: The prerequisites for a customer deployment are available [here](../deployments/prerequisite.md).

**Note 2** We recommend deploying an overlay network, such as [nebula](../deployments/Networking%20&%20Security/nebula.md).
 * It provides a mechanism to maintain static IPs.
 * It provides the mechanisms to address firewalls limitations.
 * It Isolate the network addressing security considerations. 

**Note 3** If an overlay network is not used in the training, remove firewalls restrictions to allow the the nodes
to communicate with peers and with 3rd parties applications.

## Associate the training machines with their roles 

Identify the machine assigned to each of the 4 AnyLog Instances (Master, Query and 2 Operators).

## Static IPs
AnyLog requires static IPs for the nodes in the network. Some setups are not providing static IPs. There are different ways
to represent nodes with static IPs through redirection. For example, [Nginx](https://www.nginx.com/) provide the functionality
and an example of Nginx with Kubernetes is detailed [here](https://kubernetes.github.io/ingress-nginx/examples/static-ip/). 

## Ports to use

Users can configure the nodes to use any valid IP and Port.
For simplicity, the default setup is associating the same port values to nodes of the same type.  
The following tables sumerizes the default port values:
  
| Node Type         | TCP    |   REST |
| -------------     | ------ | ------ |
| Master            | 32048  |  32049 |
| Operator          | 32148  |  32149 |
| Query             | 32348  |  32349 |

Note: 
* The Port designated as TCP is used by the AnyLog protocol when messages are send between nodes of the network. 
* The Port designated as REST is used to message a node using the REST protocol. 3rd party apps would be using 
REST to communicate with nodes in the network.

## The Network ID

* With a Master Node deployment, the network ID is the Master's IP and Port.
* A node can leverage any valid IP and port. In this deployment, the nodes are using their default IP 
(the IP that identifies the node on the network used) and the ports are set by default as described [above](#ports-to-use).  
In this setup, the network ID is the IP of the Master and port 32048.
    
**Note:** 
If the default IP is not known, when the Master node is initiated, the command **get connections** on the node CLI returns
the IPs and ports used - the Network ID is the IP and port assigned to TCP-External.

## Deploy the Network Nodes

Other than the exceptions listed below, the AnyLog nodes will be using the default configuration:
 1. Update the AnyLog license key in every node that joins the network.
 2. Update your company name (the user company name) in every node that joins the network.
 3. Add the network ID (the IP and port of the Master) to the Operators and the Query Node.
 4. Enable monitoring (in the default configuration, monitoring is disabled). In this training, in every node that joins the network.
 5. Provide a unique name to each Operator Node (i.e.: anylog-operator_1, and anylog-operator_2).
 6. Designate on each Operator a unique data cluster (i.e. anylog-cluster_1 and anylog-cluster_2).
 
 In this training, users will modify these parameters (using an editor) in the config file of each node.  
 (note that in a customer deployment, these configurations can be pre-packaged or updated using a questionnaire during the install).
 
## Get the Docker credentials and the AnyLog license key   
If you do not have Docker credentials, or an AnyLog license key please contact us at [info@anylog.co](mailto:info@anylog.co) 
 
## Deploy an AnyLog Instance on each node

Follow these steps on each of the 4 nodes (Master, Query and 3 Operator nodes).

1. Clone AnyLog deployment.
```shell 
git clone https://github.com/AnyLog-co/deployments  
```

Note: to re-install, move older install using the following command:
```
rm -rf deployments
```

2. Register docker credentials 
```shell
bash deployments/installations/docker_credentials.sh [DOCKER_ACCESS_CODE]
```

## The AnyLog Configuration file

After the install, each node maintains a configuration file named: **anylog_configs.env**.  
This file is in the following directories:

| Node              | Folder |
| -------------     | ------------- |
| Master            | deployments/docker-compose/anylog-master |
| Operator          | deployments/docker-compose/anylog-operator |
| Query             |  deployments/docker-compose/anylog-query |

## Modify configurations 

### Option 1: Using a questionnaire
The following section guides through the values to modify in the config file of each node.
Users can replace this process by a questionnaire that creates the config file with the needed modification. 
Using the questionnaire is detailed in the [deploying_node](../deployments/deploying_node.md) document.

### Option 2: Modify the config file using an editor
On each machine, modify the ```anylog_configs.env``` according to the following instructions:

1. Using an editor, enter the file:
   ```
   vi anylog_configs.env
   ```
   
2. Update the following values in the anylog_configs.env of each node:  
    **On the Master Node:**
    * LICENSE_KEY with the AnyLog License Key (and uncomment the entry).
    * COMPANY_NAME with your company name.
    * MONITOR_NODES set the value to **true**.
    * MONITOR_NODE_COMPANY with your company name (make sure its the same name assigned to COMPANY_NAME).
    
    If you don't know the Network ID, [start](#start--restart-a-deployed-node) 
    the master, [attach](#attach-to-the-process---allowing-users-to-operate-on-the-node-cli)
    to the node. On the CLI - get the Master IP and Port using the command ```get connections```.
    the Network-ID is the address under TCP/External-address (this value is updated on the config file of the Query and Operators nodes). 
    Use the keys **ctrl+d** to detach from the node. 
    
    **On the Query Node:**  
    * LICENSE_KEY with the AnyLog License Key (uncomment the entry).
    * COMPANY_NAME with your company name.
    * MONITOR_NODES set the value to **true**.
    * MONITOR_NODE_COMPANY with your company name (make sure its the same name assigned to COMPANY_NAME).
    * LEDGER_CONN with the Network ID - the IP and Port of the Master Node (for example: LEDGER_CONN=198.74.50.131:32048).
    
    **On each Operator Node:**
    * LICENSE_KEY with the AnyLog License Key (uncomment the entry).
    * COMPANY_NAME with your company name.
    * MONITOR_NODES set the value to **true**.
    * MONITOR_NODE_COMPANY with your company name (make sure its the same name assigned to COMPANY_NAME).
    * LEDGER_CONN with the Network ID - the IP and Port of the Master Node (for example: LEDGER_CONN=198.74.50.131:32048).
    * NODE_NAME - currently showing **anylog-operator**, change to be unique (and anylog can be replaced with your company name):
        - for operator 1: **anylog-operator_1**
        - for operator 2: **anylog-operator_2**
    * CLUSTER_NAME - currently showing **new-company-cluster**. change to your company name (the example below is 
    using anylog for new-company) and a unique prefix like the example below:
        - for operator 1: **anylog-cluster_1**
        - for operator 2: **anylog-cluster_2**
    
## Start / Restart a deployed node
 
```shell
# master 
cd deployments/docker-compose/anylog-master
docker-compose up -d

# operator
cd deployments/docker-compose/anylog-operator
docker-compose up -d

# query with remote-cli 
cd deployments/docker-compose/anylog-query
docker-compose up -d
```

View running containers:
```
docker ps -a 
``` 

##Attach to the process - allowing users to operate on the node CLI:

1. Attach
```
docker attach --detach-keys=ctrl-d [NODE NAME]
```
**Nodes Names**:
* Master - **anylog-master**
* Operator - **anylog-operator**
* Query - **anylog-query-node**
 
Example:
```
docker attach --detach-keys=ctrl-d anylog-query-node
```
Note: Some setups require to press the "Enter" key to see the AnyLog CLI (with the node name), like the example below:
```
AL anylog-query > 
```

2. Detach from the process (AnyLog remains active)

Using the keys: **ctrl+d**

3. Shutdown an AnyLog node

On the CLI:
```
exit node
```
Terminate a docker process:

In the the docker-compose directory of the node to terminate (Master in the example below):
```
 cd deployments/docker-compose/anylog-master
```
Do one of the following:
```
docker-compose down               # will stop the process 
docker-compose down -v            # stop the process + will also remove the volume
docker-compose down --rmi all     # stop the process + will also remove the image 
docker-compose down -v --rmi all  # will do all three  
```

## Basic initial operations
On each node (using the CLI) use the following commands:
1) View the network services using the command ```get connections```
2) View the background processes enabled using the command ```get processes```
3) Test connectivity to nodes in the network using the command ```test network``` (V sign means active and accessible).
4) Query the metadata ```blockchain get (master,operator,query) bring.table [*] [*][ip] [*][port]```


# Populating Data

There are multiple ways to deliver data to nodes in the network, in this session data will be delivered in 2 methods:
 
* Using a data generator, simulated data will be populated to the 2 operator nodes.  
    * The data generator requires [Python](https://www.python.org/downloads/) pre-installed. 
    * The data generator source code and documentation are available on Github: [Sample-Data-Generator](https://github.com/AnyLog-co/Sample-Data-Generator).
    * Advanced users can use other data generators. For example, by leveraging an [EdgeX deployment](https://github.com/AnyLog-co/lfedge-code).
    
  The data generator will generate data that will be hosted on the 2 operators nodes in a database named **test** and a table named **ping_sensor**. 
  
* Operator I, will subscribe to a 3rd party broker (in addition to data received from the data generator).  

  The broker delivers data that will be associated with database **test** and 4 tables named **lightout1, lightout2, lightout3, lightout4**
  

## Using the data generator 

The data generator generates data and delivers the data via REST to one or more nodes.  

The destination node or nodes that receive the data are specified with the **CONN** parameter on the command line
(either one or multiple destinations specified by a comma separated IP:Port values).   

Note: In the examples below, the AnyLog nodes are identified as follows:
```
Address              Node Type Node Name         
--------------------|---------|-----------------|
198.74.50.131:32348 |query    |anylog-query     |
198.74.50.131:32048 |master   |anylog-master    |
198.74.50.131:32148 |operator |anylog-operator_1|
178.79.143.174:32148|operator |anylog-operator_2|
```

1. Modify the CONN information of the command below to the destination IP and Port of the 2 Operator Nodes.  
    **Note: Use the IP and port on the Operator nodes which are designated as REST/External. The default REST/External Port on the Operators nodes is 32149**
```shell
docker run -it --detach-keys=ctrl-d --network host \
   -e DATA_TYPE=ping \
   -e INSERT_PROCESS=put \
   -e DB_NAME=test \
   -e TOTAL_ROWS=100 \
   -e BATCH_SIZE=10 \
   -e SLEEP=0.5 \
   -e CONN=198.74.50.131:32149,178.79.143.174:32149 \
   -e TIMEZONE=utc \
--rm anylogco/sample-data-generator:latest
```

2. Run the generator  
   Copy the code block (with the IP and Port of the target node) to the OS CLI. 
   
## Get data from an external MQTT broker (optional)

1. Attach to Operator #1 using the following command:
```
docker attach --detach-keys="ctrl-d" anylog-operator
Hit "Enter" to see the CLI
```   

2) Copy the following code block to the CLI:
```
<run mqtt client where broker=driver.cloudmqtt.com and port=18785 and user=ibglowct and password=MSY4e009J7ts and log=false and topic=(
   name=anylogedgex-demo and 
   dbms=test and 
   table="bring [sourceName]" and 
   column.timestamp.timestamp=now and 
   column.value=(type=int and value="bring [readings][][value]")
)> 
```
Note: in the command above, the greater than less then signs designate a code-block. 


# View status and query data (using the AnyLog Node CLI)

The sample commands below are using the CLI to test the deployment by issuing status commands and data queries.
Note that results vary based on the data inserted.

* Attach to the query node

```shell
docker attach --detach-keys="ctrl-d" anylog-query-node
```

* View basic configurations on the current node:
```shell
get connections
get processes
get databases
```

* View basic configurations on the operators:
Note: the commands below are executed on the query node. These commands can be executed on the CLI of each operator independently.
```shell
dest = 198.74.50.131:32148,178.79.143.174:32148   # These are the TCP values (IP:Port) of the operators
run client (!dest) get connections
run client (!dest) get processes
run client (!dest) get databases
```

* View data ingested on the Operator Nodes:
```shell
run client (!dest) get streaming
run client (!dest) get operator
```

* View the logical tables defined (in the entire network):
```shell
get virtual tables
```

* View columns in a table:
```shell
get columns where dbms = test and table = ping_sensor 
```

* View which are the nodes that host the data:
```shell
get data nodes
```

* Sample queries:
Note: there is no need to specify the destination node (unless the user needs to force the query to particular nodes).
```shell
run client () sql test format=table "select count(*) from ping_sensor"
run client () sql test format=table "select insert_timestamp, tsd_name, device_name, timestamp, value  from ping_sensor limit 10" 
run client () sql test format=table "select increments(minute, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as max_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value from ping_sensor where timestamp >= NOW() - 1hour GROUP BY device_name ORDER BY min_ts DESC"
sql test format=table and extend=(+node_name as node) "select device_name, timestamp, value,  from ping_sensor where period(minute, 10, now(), timestamp)"
```

# Reference Documentation

## Remote CLI
* [Deploy the Remote CLI](https://github.com/AnyLog-co/documentation/blob/master/deployments/Support/Remote-CLI.md)
* [Configure the Remote CLI](https://github.com/AnyLog-co/documentation/blob/master/northbound%20connectors/remote_cli.md)

## Grafana
* [Deploy Grafana](https://github.com/AnyLog-co/documentation/blob/master/deployments/Support/Grafana.md)
* [Configuring Grafana](https://github.com/AnyLog-co/documentation/blob/master/northbound%20connectors/using%20grafana.md) 

