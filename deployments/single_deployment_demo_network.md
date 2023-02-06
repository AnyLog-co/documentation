# Demo Cluster Deployment 

The following provides directions for deploying AnyLog and its supported tools as a single _docker-compos_ deployment. 
The deployment will ultimately install 7 docker containers -   
* PostgresSQL 
* AnyLog Master 
* AnyLog Operator I  - receive data through a local [EdgeX deployment](https://github.com/AnyLog-co/lfedge-code) 
* AnyLog Operator II - receive EdgeX data through a third-party MQTT broker 
* AnyLog Query 
* [Remote-CLI](../northbound%20connectors/remote_cli.md) 
* [Grafana](../northbound%20connectors/using%20grafana.md) 

## Deployment Process
Download [deployments](https://github.com/AnyLog-co/deployments) and [lfedge-code](https://github.com/AnyLog-co/lfedge-code). 
In addition, install [Docker and docker-compose](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/docker_install.sh)
```shell
git clone https://github.com/AnyLog-co/deployments

git clone https://github.com/AnyLog-co/lfedge-code

bash deployments/docker-compose/docker_install.sh
```

### AnyLog Network
The following provides directions for deploying AnyLog using the [demo cluster deployment](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment) 
1. (Optional) Update the configurations before deployment 
   1. In [postgres.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/postgres.env) update _POSTGRES_USER_ & _POSTGRES_PASSWORD_
   2. In [anylog_master.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/anylog_master.env) & [anylog_query.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/anylog_query.env) update
      * NODE_NAME
      * COMPANY_NAME
      * _DB_USER_ & _DB_PASSWORD_ if using PostgreSQL & changed its credentials
   3. In [anylog_operator1.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/anylog_operator1.env) & [anylog_operator2.env](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/demo-cluster-deployment/envs/anylog_operator2.env) update
      * NODE_NAME
      * COMPANY_NAME
      * _DB_USER_ & _DB_PASSWORD_ if using PostgreSQL & changed its credentials
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
Directions for deploying a local EdgeX instance can be found [here](../Other%20Tools/EdgeX.md)  

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



