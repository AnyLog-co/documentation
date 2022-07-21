# Master Node
A node that manages the shared metadata (if a blockchain platform is used, this node is redundant).

To understand the steps taken to deploy a master node, please review the [deployment process](master_node_deployment_process.md). 

## Deployment Steps 
0. The sample deployment uses [PostgreSQL](Postgres.md). Please make sure  PostgreSQL is installed.
1. In [deployments/anylog-node/envs/anylog_master.env]() update configurations
```dotenv
#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy Master node
# If database Postgres (as configured) isn't enabled the code will automatically switch to SQLite
#-----------------------------------------------------------------------------------------------------------------------
NODE_TYPE=ledger
NODE_NAME=master-node
COMPANY_NAME=New Company
#EXTERNAL_IP=<EXTERNAL IP>
#LOCAL_IP=<LOCAL IP>
ANYLOG_SERVER_PORT=32048
ANYLOG_REST_PORT=32049
LEDGER_CONN=127.0.0.1:32048
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
REST_THREADS=5
# Sets the number of threads supporting queries (the default is 3).
QUERY_POOL=3

# User should update DB_USER credentials
DB_TYPE=psql
DB_IP=127.0.0.1
DB_USER=admin
DB_PASSWD=passwd
DB_PORT=5432
# whether to have the node support system_query (ie querying data).
DEPLOY_SYSTEM_QUERY=false
# when memory is set to true, then the system_query database will automatically run using SQLite in memory. otherwise it'll use the default configs
MEMORY=true

DEPLOY_LOCAL_SCRIPT=false
```

2. Update the configurations in [.env]() file
```dotenv
CONTAINER_NAME=al-master-node
IMAGE=anylogco/anylog-network
VERSION=predevelop
ENV_FILE=envs/anylog_master.env
```
2b. If you're deploying all the nodes on a single machine / VM, then there needs to be a change in the docker-compose file.     
Please copy and paste the following instead of the current content in docker-compose. 
```yaml
version: "2.2"
services:
  anylog-master-node:
    image: ${REPOSITORY}:${TAG}
    env_file:
      - ${ENV_FILE}
    container_name: ${CONTAINER_NAME}
    stdin_open: true
    tty: true
    network_mode: "host" 
    volumes:
      - anylog-master-node-anylog:/app/AnyLog-Network/anylog
      - anylog-master-node-blockchain:/app/AnyLog-Network/blockchain
      - anylog-master-node-data:/app/AnyLog-Network/data
      - anylog-master-node-local-scripts:/app/AnyLog-Network/scripts
volumes:
  anylog-master-node-anylog:
      external:
        name: ${CONTAINER_NAME}-anylog
  anylog-master-node-blockchain:
    external:
      name: ${CONTAINER_NAME}-blockchain
  anylog-master-node-data:
    external:
      name: ${CONTAINER_NAME}-data
  anylog-master-node-local-scripts:
    external:
      name: ${CONTAINER_NAME}-local-scripts
```

3. Deploy anylog-master via docker 
```shell
cd deployments/docker-compose/anylog-node 
docker-compose up -d 
```

### Validate Node 
* Get Status
```shell
curl -X GET ${MASTER_NODE_IP}:${MASTER_NODE_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${MASTER_NODE_IP}:${MASTER_NODE_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23"  #| jq 

    Process         Status       Details                                                                  
    ---------------|------------|------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 45.79.74.39:32048, Threads Pool: 6                        |
    REST           |Running     |Listening on: 45.79.74.39:32049, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Not declared|                                                                        |
    Publisher      |Not declared|                                                                        |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 127.0.0.1:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                          |
    Distributor    |Not declared|                                                                        |
    Consumer       |Not declared|                                                                        |
    MQTT           |Not declared|                                                                        |
    Message Broker |Not declared|No active connection                                                    |
    SMTP           |Not declared|                                                                        |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes            |
    Query Pool     |Running     |Threads Pool: 3                                                         |
```
* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-master-node

# to detach press: ctrl-d
```
