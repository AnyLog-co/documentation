# Operator Node
A node that hosts the data. This operator will receive data directly from EdgeX via MQTT. 

To understand the steps taken to deploy a operator node, please review the [deployment process](operator_node_deployment_process.md). 

Directions for configuring EdgeX send data to a local AnyLog broker can be found [here](EdgeX.md).

## Deployment Steps 
0. The sample deployment uses [PostgreSQL](Postgres.md). Please make sure  PostgreSQL is installed.


1. In [deployments/anylog-node/envs/anylog_operator.env]() update configurations. Please note, the `LEDGER_CONN` value 
is configured against our testnet / demo master node.  
```dotenv
#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy an Operator node.
# If database Postgres (as configured) isn't enabled the code will automatically switch to SQLite
# Please make sure to update the MASTER_NODE to that of the active master_node IP:TCP_PORT
#-----------------------------------------------------------------------------------------------------------------------
NODE_TYPE=operator
NODE_NAME=anylog-operator-node1
COMPANY_NAME=AnyLog
#EXTERNAL_IP=<EXTERNAL IP>
#LOCAL_IP=<LOCAL IP>
ANYLOG_SERVER_PORT=32148
ANYLOG_REST_PORT=32149
ANYLOG_BROKER_PORT=32150
LEDGER_CONN=45.79.74.39:32049
# blockchain sync time
SYNC_TIME=30 second

# User should update DB_USER credentials
DB_TYPE=psql
DB_IP=127.0.0.1
DB_USER=admin
DB_PASSWD=passwd
DB_PORT=5432
DEFAULT_DBMS=test
# whether to have the node support system_query (ie querying data).
DEPLOY_SYSTEM_QUERY=true
# when memory is set to true, then the system_query database will automatically run using SQLite in memory. otherwise it'll use the default configs
MEMORY=true

# Operator specific parameters
# for operator - If you'd like to reset the blockchain but keep the original Member ID then uncomment "Member" and set to the desired member_id (int)
#MEMBER=<MEMBER_ID>
CLUSTER_NAME=new-cluster
ENABLE_PARTITION=true
PARTITION_COLUMN=timestamp
PARTITION_INTERVAL=day
PARTITION_KEEP=7
TABLE_NAME=*

# Operator params
# run operator where create_table=!create_table and update_tsd_info=!update_tsd_info and archive=!archive and distributor=!distributor and master_node=!master_node and policy=!policy_id
CREATE_TABLE=true
UPDATE_TSD_INFO=true
ARCHIVE=true
DISTRIBUTOR=true
COMPRESS_FILE=true

WRITE_IMMEDIATE=true
THRESHOLD_TIME=60 seconds
THRESHOLD_VOLUME=10KB

# An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port.
TCP_THREAD_POOL=6
# Amount of time (in seconds) until REST timesout
REST_TIMEOUT=30
# The number of concurrent threads supporting HTTP requests.
REST_THREADS=5
QUERY_POOL=3

# MQTT parameters - the default recieves data from a remote MQTT broker
MQTT_ENABLE=true
BROKER=local
MQTT_PORT=32150
#MQTT_USER=ibglowct
#MQTT_PASSWORD=MSY4e009J7ts
MQTT_LOG=false
MQTT_TOPIC_NAME=anylogedgex
MQTT_TOPIC_DBMS=test
# original value was "bring [device]" (Random-Integer-Generator01). howerver, due to a PSQL table name limit size is 65 chars, it's manually changeds to: rand_int 
MQTT_TOPIC_TABLE=rand_data
MQTT_COLUMN_TIMESTAMP=now
MQTT_COLUMN_VALUE_TYPE=float
MQTT_COLUMN_VALUE="bring [readings][][value]"

DEPLOY_LOCAL_SCRIPT=true
```

2. Update the configurations in [.env]() file
```dotenv
CONTAINER_NAME=al-operator-node1
IMAGE=anylogco/anylog-network
VERSION=predevelop
ENV_FILE=envs/anylog_operator.env
```
2b. If you're deploying all the nodes on a single machine / VM, then there needs to be a change in the docker-compose file.     
Please copy and paste the following instead of the current content in docker-compose. 
```yaml
version: "2.2"
services:
  anylog-operator-node1:
    image: ${REPOSITORY}:${TAG}
    env_file:
      - ${ENV_FILE}
    container_name: ${CONTAINER_NAME}
    stdin_open: true
    tty: true
    network_mode: "host" 
    volumes:
      - anylog-operator-node1-anylog:/app/AnyLog-Network/anylog
      - anylog-operator-node1-blockchain:/app/AnyLog-Network/blockchain
      - anylog-operator-node1-data:/app/AnyLog-Network/data
      - anylog-operator-node1-local-scripts:/app/AnyLog-Network/scripts
volumes:
  anylog-operator-node1-anylog:
      external:
        name: ${CONTAINER_NAME}-anylog
  anylog-operator-node1-blockchain:
    external:
      name: ${CONTAINER_NAME}-blockchain
  anylog-operator-node1-data:
    external:
      name: ${CONTAINER_NAME}-data
  anylog-operator-node1-local-scripts:
    external:
      name: ${CONTAINER_NAME}-local-scripts
```

3. Deploy anylog-operator via docker 
```shell
cd deployments/docker-compose/anylog-node 
docker-compose up -d 
```

### Validate Node 
* Get Status
```shell
curl -X GET ${OPERATOR_NODE_IP}:${OPERATOR_NODE_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${OPERATOR_NODE_IP}:${OPERATOR_NODE_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23"  
    Process         Status       Details                                                                    
    ---------------|------------|--------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 139.162.56.87:32148, Threads Pool: 6                        |
    REST           |Running     |Listening on: 139.162.56.87:32149, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Running     |Cluster Member: True, Using Master: 45.79.74.39:32048                     |
    Publisher      |Not declared|                                                                          |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                            |
    Distributor    |Running     |                                                                          |
    Consumer       |Not declared|                                                                          |
    MQTT           |Running     |                                                                          |
    Message Broker |Running     |Listening on: 139.162.56.87:32150, Threads Pool: 4                        |
    SMTP           |Not declared|                                                                          |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes              |
    Query Pool     |Running     |Threads Pool: 3                                                           |
    Kafka Consumer |Not declared|                                                                          |
```
* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-operator-node1

# to detach press: ctrl-d
```
