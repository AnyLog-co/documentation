# Operator Node
A node that hosts the data. This operator will receive data directly from EdgeX via [third-party MQTT broker](https://www.cloudmqtt.com/). 

To understand the steps taken to deploy a operator node, please review the [deployment process](operator_node_deployment_process.md). 

## Deployment Steps
1. In [deployments/docker-compose/anylog-operator2/anylog_configs.env](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-operator2/anylog_configs.env) 
update configurations Please note, the `LEDGER_CONN` value is configured against our testnet / demo master node.  
```dotenv
#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy an Operator node.
# If database Postgres (as configured) isn't enabled the code will automatically switch to SQLite
# Please make sure to update the MASTER_NODE to that of the active master_node IP:TCP_PORT
#-----------------------------------------------------------------------------------------------------------------------
NODE_TYPE=operator
NODE_NAME=anylog-operator-node2
COMPANY_NAME=AnyLog
#EXTERNAL_IP=<EXTERNAL IP>
#LOCAL_IP=<LOCAL IP>
ANYLOG_SERVER_PORT=32158
ANYLOG_REST_PORT=32159
ANYLOG_BROKER_PORT=""
LEDGER_CONN=45.79.74.39:32049
# blockchain sync time
SYNC_TIME=30 second

# if location is not set, will use `https://ipinfo.io/json` to get coordinates
LOCATION=""
COUNTRY=""
STATE=""
CITY=""

# User should update DB_USER credentials
DB_TYPE=sqlite
#DB_IP=127.0.0.1
#DB_USER=admin
#DB_PASSWD=passwd
#DB_PORT=5432
#DEFAULT_DBMS=test
# whether to have the node support system_query (ie querying data).
DEPLOY_SYSTEM_QUERY=true
# when memory is set to true, then the system_query database will automatically run using SQLite in memory. otherwise it'll use the default configs
MEMORY=true

# Operator specific parameters
# for operator - If you'd like to reset the blockchain but keep the original Member ID then uncomment "Member" and set to the desired member_id (int)
#MEMBER=<MEMBER_ID>
CLUSTER_NAME=new-cluster2
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
BROKER=driver.cloudmqtt.com
MQTT_PORT=18785
MQTT_USER=ibglowct
MQTT_PASSWORD=MSY4e009J7ts
MQTT_LOG=false
MQTT_TOPIC_NAME=anylogedgex
MQTT_TOPIC_DBMS=test
# original value was "bring [device]" (Random-Integer-Generator01). howerver, due to a PSQL table name limit size is 65 chars, it's manually changeds to: rand_int 
MQTT_TOPIC_TABLE=rand_data
MQTT_COLUMN_TIMESTAMP=now
MQTT_COLUMN_VALUE_TYPE=float
MQTT_COLUMN_VALUE="bring [readings][][value]"

DEPLOY_LOCAL_SCRIPT=false
```
**Disclaimer**: The `LEDGER_CONN` parameter is sometimes called `!master_node` in other parts of the documentation.

2. (Optional) By default the [docker-compose](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-master/docker-compose.yml)  
file is configured to run develop build. In order to run a different build, update _line 4_ with the desired version. 
```yaml
# current config: 
image: anylogco/anylog-network:develop

# update to predevelop
image: anylogco/anylog-network:predevelop
```

3. Deploy anylog-operator via Docker 
```shell
cd deployments/docker-compose/anylog-operator2

# to start node with the latest code
docker-compose up -d 

# to start a node with existing build 
docker-compose up -d --no-build
```

### Validate Node 
* Get Status
```shell
curl -X GET ${OPERATOR_NODE2_IP}:${OPERATOR_NODE2_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${OPERATOR_NODE2_IP}:${OPERATOR_NODE2_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23"  
    Process         Status       Details                                                                     
    ---------------|------------|---------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.105.86.168:32148, Threads Pool: 6                        |
    REST           |Running     |Listening on: 172.105.86.168:32149, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Running     |Cluster Member: True, Using Master: 45.79.74.39:32048                      |
    Publisher      |Not declared|                                                                           |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                 |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                             |
    Distributor    |Running     |                                                                           |
    Consumer       |Not declared|                                                                           |
    MQTT           |Running     |                                                                           |
    Message Broker |Not declared|No active connection                                                       |
    SMTP           |Not declared|                                                                           |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes               |
    Query Pool     |Running     |Threads Pool: 3                                                            |
    Kafka Consumer |Not declared|                                                                           |
```
* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-operator-node2

# to detach press: ctrl-d
```