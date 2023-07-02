# Session II - Deployment of the test network

If you do not have Docker credentials, or an AnyLog license key please contact us at [info@anylog.co](mailto:info@anylog.co) 

## Overview

This document describes how to deploy and configure an AnyLog Network. This guided session provides directions to:
* Deploy an  AnyLog Network consisting of  4 nodes (2 operators, 1 query, 1 master).
* Deploy and Configure [PostgreSQL](https://www.postgresql.org/) as a local database on the nodes in the network.
* Deploy and Configure [EdgeX](https://www.edgexfoundry.org/) as a data source.
* Deploy AnyLog's [Remote CLI](../northbound%20connectors/remote_cli.md) - a web based REST client for querying data, send requests and inspect responses.
* Deploy and Configure [Grafana](https://grafana.com/) to visualize the data. 

**Deployment Diagram**:

![deployment diagram](../imgs/deployment_diagram.png)

## Prerequisites
Prior to this session, users are required to prepare:
* 4 machines (physical or virtual) to host the AnyLog nodes, as follows:
    - A Linux environment.
    - A minimum of 256MB of RAM.
    - A minimum of 10GB of disk space.
* 1 Machine (physical or virtual) for applications that interact with the network, as follows:
    - Linux or Windows environment.
    - A minimum of 256MB of RAM.
    - A minimum of 10GB of disk space.
* Each node accessible by IP and Port (remove firewalls restrictions).
* [Docker](https://docs.docker.com/) installed (navigate to [Get Docker](https://docs.docker.com/get-docker/) site to access
   the Docker download that’s suitable for your platform).

**Note 1**: The prerequisites for a customer deployment are available [here](../deployments/prerequisite.md).

**Note 2** We recommend deploying an overlay network, such as [nebula](../deployments/Networking%20&%20Security/nebula.md).
 * It provides a mechanism to maintain static IPs.
 * It provides the mechanisms to address firewalls limitations.
 * It Isolate the network addressing security considerations. 

**Note 3** If an overlay network is not used in the training, remove firewalls restrictions to allow the the nodes
to communicate with peers and with 3rd parties applications.

## Nodes deployed in the training session

| Node Name   | Functionality |
| ------------- | ------------- |
| Master  | A node that manages the shared metadata (if a blockchain platform is used, this node is redundant). |
| Operator  |  A node that hosts the data. In this session, users deploy 2 Operator nodes. |
| Query  | A node that coordinates the query process. |

Additional information on the types of nodes is in the [Getting Started](../getting%20started.md) document.

## Additional Software Deployed

| Package Name  | Functionality |
| ------------- | ------------- |
| [PostgreSQL](https://www.postgresql.org/download/)   | A local database on each node.  |
| [EdgeX](https://github.com/AnyLog-co/lfedge-code)  | A conector to PLCs and sensors.  |
| [Remote-CLI](../northbound%20connectors/remote_cli.md)   | A web based interface to the network.  |
| [Grafana](../northbound%20connectors/using%20grafana.md)   |  A visualization tool. |

## Data sources
 
Data will be added to the 2 Operator nodes in the following manner:
 
* AnyLog Operator I  - receive data as a message broker through a local [EdgeX deployment](https://github.com/AnyLog-co/lfedge-code). 
* AnyLog Operator II - receive data by subscribing to a 3rd-party MQTT broker. 


## Deployment Process

* Identify the machine assigned to each of the 4 AnyLog Instances.

* On each  machine, download and deploy the AnyLog deployment package using the commands below. 
```shell
git clone https://github.com/AnyLog-co/deployments
bash deployments/docker-compose/docker_install.sh
```
**Note:** deployments details are in the - [Deploying a Node](../deploying_node.md) document.

* On 1 Operator Nodes, using the git clone command below, download the LF-Edge code (that includes Edgex) that will be 
used to generate data.  
```shell
git clone https://github.com/AnyLog-co/lfedge-code
```
**Note:** deployments details are in the - [lfedge-code](https://github.com/AnyLog-co/lfedge-code) document. 
Note that the LF-Edge package is not eequired for the second Operator, as the data source used is a 3rd party message broker.




 
In addition, install [Docker and docker-compose](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/docker_install.sh).

```shell
git clone https://github.com/AnyLog-co/deployments

git clone https://github.com/AnyLog-co/lfedge-code

bash deployments/docker-compose/docker_install.sh
```

### AnyLog Network
The following provides directions for deploying AnyLog using the [demo cluster deployment](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment) 
1. For all nodes update the `LICENSE_KEY` value
   *  [master](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-demo-network/envs/anylog_master.env)
   *  [Operator 1](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-demo-network/envs/anylog_operator1.env) 
   *  [Operator 2](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-demo-network/envs/anylog_operator2.env)
   *  [Query](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-demo-network/envs/anylog_query.env)

2. (Optional) Update the configurations before deployment 
   1. In [postgres.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/postgres.env) update _POSTGRES_USER_ & _POSTGRES_PASSWORD_
   2. In [anylog_master.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/anylog_master.env) & [anylog_query.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/anylog_query.env) update
      * NODE_NAME
      * COMPANY_NAME
      * _DB_USER_ & _DB_PASSWORD_ if using PostgresSQL & changed its credentials
   3. In [anylog_operator1.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/anylog_operator1.env) & [anylog_operator2.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/anylog_operator2.env) update
      * NODE_NAME
      * COMPANY_NAME
      * _DB_USER_ & _DB_PASSWORD_ if using PostgresSQL & changed its credentials
      * logical database name (_DEFAULT_DBMS_ and _MQTT_TOPIC_DBMS_)
      * _CLUSTER_NAME_
   4. By default, the deployment is set to download anylog-network version: `develop`. To use a different version 
(such as `predevelop`) change the _tag_ value in [.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/.env) file. 
```dotenv
# current config: 
tag=develop

# update to predevelop
tag=predevelop
```

2. Start Cluster
```shell
docker-compose up -d
```

### Install EdgeX
_Operator1_ utilizes a local MQTT client. In our demonstration, we utilize a local EdgeX instance.  
Directions for deploying a local EdgeX instance can be found [here](Support/EdgeX.md)  

## Validate Deployment
* Attaching to an AnyLog node 
```shell
# master 
docker attach --detach-keys="ctrl-d" anylog-master-node 

# operator 1 
docker attach --detach-keys="ctrl-d" anylog-operator-node1

# operator 2
docker attach --detach-keys="ctrl-d" anylog-operator-node2

# query 
docker attach --detach-keys="ctrl-d" anylog-query-node

# detach from AnyLog node - ctrl-d
```

* View basic configurations -- `get connections`, `get processes` and `get databases`   
```shell
ubuntu@demo:~$ docker attach --detach-keys="ctrl-d" anylog-master-node

AL master-node +> get connections (need to update this to the new format showing binds)

Type      External Address     Local Address        
---------|--------------------|--------------------|
TCP      |139.162.200.15:32048|139.162.200.15:32048|
REST     |139.162.200.15:32049|139.162.200.15:32049|
Messaging|Not declared        |Not declared        |

AL master-node +> get processes 

    Process         Status       Details                                                                     
    ---------------|------------|---------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 139.162.200.15:32048, Threads Pool: 6                        |
    REST           |Running     |Listening on: 139.162.200.15:32049, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Not declared|                                                                           |
    Publisher      |Not declared|                                                                           |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 127.0.0.1:32048                   |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                             |
    Distributor    |Not declared|                                                                           |
    Consumer       |Not declared|                                                                           |
    MQTT           |Not declared|                                                                           |
    Message Broker |Not declared|No active connection                                                       |
    SMTP           |Not declared|                                                                           |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes               |
    Query Pool     |Running     |Threads Pool: 3                                                            |
    Kafka Consumer |Not declared|                                                                           |

AL master-node +> get databases 

List of DBMS connections
Logical DBMS         Database Type IP:Port                        Storage
-------------------- ------------- ------------------------------ -------------------------
blockchain           psql          127.0.0.1:5432                 Persistent
system_query         sqlite        Local                          MEMORY

# detach from AnyLog node - ctrl-d 
```

* Make sure data is coming into Operator node - `get msg client`, `get streaming`, `get operator`
```shell
ubuntu@demo:~$ docker attach --detach-keys="ctrl-d" anylog-operator-node1 

AL anylog-operator-node1 +> get msg client 

Subscription: 0001
User:         unused
Broker:       local
Connection:   Not connected: MQTT_ERR_NO_CONN

     Messages    Success     Errors      Last message time    Last error time      Last Error
     ----------  ----------  ----------  -------------------  -------------------  ----------------------------------
            843         843           0  2022-07-29 00:34:24
     
     Subscribed Topics:
     Topic       QOS DBMS  Table     Column name Column Type Mapping Function        Optional Policies 
     -----------|---|-----|---------|-----------|-----------|-----------------------|--------|--------|
     anylogedgex|  0|test|rand_data|timestamp  |timestamp  |now()                  |False   |        |
                |   |     |         |value      |float      |['[readings][][value]']|False   |        |

     
     Directories Used:
     Directory Name Location                       
     --------------|------------------------------|
     Prep Dir      |/app/AnyLog-Network/data/prep |
     Watch Dir     |/app/AnyLog-Network/data/watch|
     Error Dir     |/app/AnyLog-Network/data/error|

AL anylog-operator-node1 +> get streaming 

Flush Thresholds
Threshold         Value  Streamer 
-----------------|------|--------|
Default Time     |    60|Running |
Default Volume   |10,240|        |
Default Immediate|True  |        |
Buffered Rows    |     8|        |
Flushed Rows     |     9|        |


Statistics
DBMS-Table      File Put File Rows Streaming Put Streaming Rows Streaming Cached Immediate Last Process        
---------------|--------|---------|-------------|--------------|----------------|---------|-------------------|
test.rand_data|       0|        0|          846|           846|               8|      824|2022-07-29 00:34:44|

AL anylog-operator-node1 +> get operator 

Status:     Active
Time:       1:37:43 (H:M:S)
Policy:     29ebc0cf136de22b25c3036a32363f65
Cluster:    e9c30c8935f845a8976ff0f827378b92
Member:     113
Statistics JSON files:
DBMS                   TABLE                  FILES      IMMEDIATE  LAST PROCESS
---------------------- ---------------------- ---------- ---------- --------------------
test                  rand_data                       4         90 2022-07-29 00:34:07

Statistics SQL files:
DBMS                   TABLE                  FILES      IMMEDIATE  LAST PROCESS
---------------------- ---------------------- ---------- ---------- --------------------
test                  rand_data                       4          0 2022-07-29 00:01:05

Errors summary
Error Type           Counter DBMS Name Table Name Last Error Last Error Text 
--------------------|-------|---------|----------|----------|---------------|
Duplicate JSON Files|      0|         |          |         0|               |
JSON Files Errors   |      0|         |          |         0|               |
SQL Files Errors    |      0|         |          |         0|               |

# detach from AnyLog node - ctrl-d
```

* Query data -- `get data nodes` and `select * from rand_data limit 10;` 
```shell
ubuntu@demo:~$ docker attach --detach-keys="ctrl-d" anylog-query-node 

AL query-node +> get data nodes 

Company DBMS  Table     Cluster ID                       Cluster Status Node Name             Member ID External IP/Port     Local IP/Port        Node Status 
-------|-----|---------|--------------------------------|--------------|---------------------|---------|--------------------|--------------------|-----------|
AnyLog |test |rand_data|b8517462b22804cfc357c86030e04520|active        |anylog-operator-node2|       59|139.162.200.15:32158|139.162.200.15:32158|active     |
       |     |         |e9c30c8935f845a8976ff0f827378b92|active        |anylog-operator-node1|      113|139.162.200.15:32148|139.162.200.15:32148|active     |

AL query-node +> run client () sql test format=table "select * from rand_data limit 10;" 
[0]
AL query-node +> 
row_id insert_timestamp           tsd_name tsd_id timestamp                  value      
------ -------------------------- -------- ------ -------------------------- ---------- 
     1 2022-07-28 22:58:16.526417       59      2 2022-07-28 22:57:12.078936 2062547502 
     2 2022-07-28 22:58:16.526417       59      2 2022-07-28 22:57:15.288161     -21506 
     3 2022-07-28 22:58:16.526417       59      2 2022-07-28 22:57:15.365373        -88 
     4 2022-07-28 22:58:16.526417       59      2 2022-07-28 22:57:15.365744 1140863460 
     5 2022-07-28 22:58:16.526417       59      2 2022-07-28 22:57:35.288549       -631 
     6 2022-07-28 22:58:16.526417       59      2 2022-07-28 22:57:35.365486        -49 
     7 2022-07-28 22:58:16.526417       59      2 2022-07-28 22:57:35.365981 1699705479 

row_id insert_timestamp           tsd_name tsd_id timestamp                  value 
------ -------------------------- -------- ------ -------------------------- ----- 
     1 2022-07-28 22:58:22.252761      113      1 2022-07-28 22:57:20.004870    35 

row_id insert_timestamp           tsd_name tsd_id timestamp                  value  
------ -------------------------- -------- ------ -------------------------- ------ 
     1 2022-07-29 00:00:19.696563       59     66 2022-07-29 00:00:15.367675 -25863 

row_id insert_timestamp           tsd_name tsd_id timestamp                  value  
------ -------------------------- -------- ------ -------------------------- ------ 
     1 2022-07-29 00:00:05.287433      113     61 2022-07-29 00:00:04.050341 -12346 

{"Statistics":[{"Count": 10,
                "Time":"00:00:00",
                "Nodes": 2}]}
# detach from AnyLog node - ctrl-d
```