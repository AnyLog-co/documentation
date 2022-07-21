# Publisher Node
A node that supports distribution of data from device(s) to operator nodes. In the example we have a running 
message broker, however the MQTT client is running against the local REST node for a sample data set  

To understand the steps taken to deploy a query node, please review the [deployment process](publisher_node_deployment_process.md). 

## Deployment Steps
1. In [deployments/anylog-node/envs/anylog_publisher.env]() update configurations. Please note, the `LEDGER_CONN` value 
is configured against our testnet / demo master node.  
```dotenv
#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy a query node
# If database Postgres (as configured) isn't enabled the code will automatically switch to SQLite
# Please make sure to update the MASTER_NODE to that of the active master_node IP:TCP_PORT
#-----------------------------------------------------------------------------------------------------------------------
NODE_TYPE=publisher
NODE_NAME=publisher-node
COMPANY_NAME=New Company
#EXTERNAL_IP=<EXTERNAL IP>
#LOCAL_IP=<LOCAL IP>
ANYLOG_SERVER_PORT=32248
ANYLOG_REST_PORT=32249
ANYLOG_BROKER_PORT=32250
LEDGER_CONN=45.33.41.185:32048
# blockchain sync time
SYNC_TIME=30 second

# if location is not set, will use `https://ipinfo.io/json` to get coordinates
LOCATION=""
COUNTRY=""
STATE=""
CITY=""

# An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port.
TCP_THREAD_POOL=6
# Amount of time (in seconds) until REST timesout
REST_TIMEOUT=30
# The number of concurrent threads supporting HTTP requests.
REST_THREADS=10
QUERY_POOL=8

# User should update DB_USER credentials
DB_TYPE=sqlite
#DB_IP=127.0.0.1
#DB_USER=admin
#DB_PASSWD=passwd
#DB_PORT=5432
# whether to have the node support system_query (ie querying data).
DEPLOY_SYSTEM_QUERY=false
# when memory is set to true, then the system_query database will automatically run using SQLite in memory. otherwise it'll use the default configs
MEMORY=flase

MQTT_ENABLE=true
BROKER=rest
MQTT_PORT=32249
#MQTT_USER=ibglowct
#MQTT_PASSWORD=MSY4e009J7ts
MQTT_LOG=false
MQTT_TOPIC_NAME=anylogrest
MQTT_TOPIC_DBMS="bring [dbms]" 
# original value was "bring [device]" (Random-Integer-Generator01). howerver, due to a PSQL table name limit size is 65 chars, it's manually changeds to: rand_int 
MQTT_TOPIC_TABLE="bring [table]" 
MQTT_COLUMN_TIMESTAMP="bring [timestamp]" 
MQTT_COLUMN_VALUE_TYPE=float
MQTT_COLUMN_VALUE="bring [value]"

DEPLOY_LOCAL_SCRIPT=false
```

2. Update the configurations in [.env]() file
```dotenv
CONTAINER_NAME=al-publisher-node
IMAGE=anylogco/anylog-network
VERSION=predevelop
ENV_FILE=envs/anylog_publisher.env
```
2b. If you're deploying all the nodes on a single machine / VM, then there needs to be a change in the docker-compose file.     
Please copy and paste the following instead of the current content in docker-compose. 
```yaml
version: "2.2"
services:
  anylog-publisher-node:
    image: ${REPOSITORY}:${TAG}
    env_file:
      - ${ENV_FILE}
    container_name: ${CONTAINER_NAME}
    stdin_open: true
    tty: true
    network_mode: "host" 
    volumes:
      - anylog-publisher-node-anylog:/app/AnyLog-Network/anylog
      - anylog-publisher-node-blockchain:/app/AnyLog-Network/blockchain
      - anylog-publisher-node-data:/app/AnyLog-Network/data
      - anylog-publisher-node-local-scripts:/app/AnyLog-Network/scripts
volumes:
  anylog-publisher-node-anylog:
      external:
        name: ${CONTAINER_NAME}-anylog
  anylog-publisher-node-blockchain:
    external:
      name: ${CONTAINER_NAME}-blockchain
  anylog-publisher-node-data:
    external:
      name: ${CONTAINER_NAME}-data
  anylog-publisher-node-local-scripts:
    external:
      name: ${CONTAINER_NAME}-local-scripts
```

3. Deploy anylog-query via docker 
```shell
cd deployments/docker-compose/anylog-node
bash docker-volume.sh 
docker-compose up -d 
```

Once volumes are created - 

### Validate Node 
* Get Status
```shell
curl -X GET ${PUBLISHER_NODE_IP}:${PUBLISHER_NODE_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${PUBLISHER_NODE_IP}:${PUBLISHER_NODE_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23" 
    Process         Status       Details                                                                      
    ---------------|------------|----------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 172.104.180.110:32248, Threads Pool: 6                        |
    REST           |Running     |Listening on: 172.104.180.110:32249, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Not declared|                                                                            |
    Publisher      |Running     |                                                                            |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                  |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                              |
    Distributor    |Not declared|                                                                            |
    Consumer       |Not declared|                                                                            |
    MQTT           |Running     |                                                                            |
    Message Broker |Running     |Listening on: 172.104.180.110:32250, Threads Pool: 4                        |
    SMTP           |Not declared|                                                                            |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes                |
    Query Pool     |Running     |Threads Pool: 3                                                             |
    Kafka Consumer |Not declared|                                                                            |
```

* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-publisher-node

# to detach press: ctrl-d
```
