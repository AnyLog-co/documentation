# Query Node
A node that coordinates the query process. This node is ideal for communicating with [North Bound](../../northbound%20connectors) 
connectors, as heavy in terms of I/O against other nodes, unless requested by a user or application. 

To understand the steps taken to deploy a query node, please review the [deployment process](query_node_deployment_process.md). 

## Deployment Steps
1. In [deployments/docker-compose/anylog-query/anylog_configs.env](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-query/anylog_configs.env) 
update configurations Please note, the `LEDGER_CONN` value is configured against our testnet / demo master node.  
```dotenv
#-----------------------------------------------------------------------------------------------------------------------
# The following is intended to deploy a query node
# If database Postgres (as configured) isn't enabled the code will automatically switch to SQLite
# Please make sure to update the MASTER_NODE to that of the active master_node IP:TCP_PORT
#-----------------------------------------------------------------------------------------------------------------------
NODE_TYPE=query
NODE_NAME=query-node
COMPANY_NAME=New Company
#EXTERNAL_IP=<EXTERNAL IP>
#LOCAL_IP=<LOCAL IP>
ANYLOG_SERVER_PORT=32348
ANYLOG_REST_PORT=32349
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
DEPLOY_SYSTEM_QUERY=true
# when memory is set to true, then the system_query database will automatically run using SQLite in memory. otherwise it'll use the default configs
MEMORY=true

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

3. Deploy anylog-query via Docker 
```shell
cd deployments/docker-compose/anylog-query

# to start node with the latest code
docker-compose up -d 

# to start a node with existing build 
docker-compose up -d --no-build
```


### Validate Node 
* Get Status
```shell
curl -X GET ${QUERY_NODE_IP}:${QUERY_NODE_PORT} -H "command: get status" -H "User-Agent: AnyLog/1.23"  -w "\n"
```
* Expected `get processes` behavior
```shell
curl -X GET ${QUERY_NODE_IP}:${QUERY_NODE_PORT} -H "command: get processes" -H "User-Agent: AnyLog/1.23" 
    Process         Status       Details                                                                    
    ---------------|------------|--------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 23.239.12.151:32348, Threads Pool: 6                        |
    REST           |Running     |Listening on: 23.239.12.151:32349, Threads Pool: 5, Timeout: 30, SSL: None|
    Operator       |Not declared|                                                                          |
    Publisher      |Not declared|                                                                          |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 45.79.74.39:32048                |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                            |
    Distributor    |Not declared|                                                                          |
    Consumer       |Not declared|                                                                          |
    MQTT           |Not declared|                                                                          |
    Message Broker |Not declared|No active connection                                                      |
    SMTP           |Not declared|                                                                          |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,240 bytes              |
    Query Pool     |Running     |Threads Pool: 3                                                           |
    Kafka Consumer |Not declared|                                                                          |
```
* Attach / detach to node 
```shell
docker attach --detach-keys="ctrl-d" al-query-node

# to detach press: ctrl-d
```
