# Deploying a Node
This document provides general directions for deploying an AnyLog node, via _Docker_. There are 5 main types of 
AnyLog Nodes: 
* **REST** - An AnyLog node that has all the variables declared, as well as connecting to _TCP_, _REST_ and
_Broker_ (if declared). 
* **Master** – A node that manages the shared metadata (if a blockchain platform is used, this node is redundant).
* **Operator** – A node that hosts the data. For this deployment we will have 2 Operator nodes.
* **Query** – A node that coordinates the query process. 
* **Publisher** - A node that supports distribution of data from device(s) to operator nodes. This node is not part of the
deployment diagram. However, is often used in large scale projects. 


### Basic Deployment
Our basic deployment is a node of type REST. The deployment does not require any user-defined configurations, 
automatically connects to ports 2148 for _TCP_ and 2149 for _REST_. Users can easily extend the deployment to also 
connect to a message broker by setting an environment variable - `-e ANYLOG_BROKER_PORT=2150`. 

```shell
docker run --network host -it --detach-keys=ctrl-d \
  --name anylog-node \
  [-e ANYLOG_BROKER_PORT=2150]
  [--volume anylog-dir:/app/AnyLog-Network/anylog \]
  [--volume blockchain-dir:/app/AnyLog-Network/blockchain \]
  [--volume data-dir:/app/AnyLog-Network/data \]
  -rm anylogco/anylog-network:predevelop
```

### Configuration Based Deployment
For a simplified process, feel free to utilize our deployment script. 
```shell
bash $HOME/deployments/deployment_scripts/deploy_node.sh
```
1. Fill-out the Anylog configurations file for a node
   * If you're using AnyLog overlay network make sure INTERNAL_IP address of all the nodes are in the same subnet
   * Make sure the database credentials are the same as what's configured in your PostgresSQL database
   * If you're changing the `ANYLOG_SERVER_PORT` make sure to also change the port associated with the `LEDGER_CONN`
   * A location that's not preset will be autogenerated when node is deployed  

Sample configurations for specific node types can be found in [deployments](https://github/AnyLog-co/deployments/docker-compose) Invalid link
* [master](https://raw.githubusercontent.com/AnyLog-co/deployments/master/docker-compose/anylog-master/anylog_configs.env)
* [operator](https://raw.githubusercontent.com/AnyLog-co/deployments/master/docker-compose/anylog-operator/anylog_configs.env)
* [query](https://raw.githubusercontent.com/AnyLog-co/deployments/master/docker-compose/anylog-query/anylog_configs.env)
* [publisher](https://raw.githubusercontent.com/AnyLog-co/deployments/master/docker-compose/anylog-publisher/anylog_configs.env)

```dotenv
# --- General ---
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols [Default: rest]
NODE_TYPE=rest
# Name of the AnyLog instance [Default: anylog-node]
NODE_NAME=anylog-node
# Owner of the AnyLog instance [Default: New Company]
COMPANY_NAME=New Company
# Coordinates of the machine - used by Grafana to map the network [Default: 0.0, 0.0]
#LOCATION=<GENERAL_LOCATION>
# Country where machine is located [Default: Unknown]
#COUNTRY=<GENERAL_COUNTRY>
# State where machine is located [Default: Unknown]
#STATE=<GENERAL_STATE>
# City where machine is located [Default: Unknown]
#CITY=<GENERAL_CITY>

# --- Authentication ---
# When using AnyLog authentication, nodes should have authentcation enabled once declared as a member on the blockchain [Default: false]
ENABLE_AUTH=false
# Whether or not to enable authentication when accessing node via REST [Default: false]
ENABLE_REST_AUTH=false
# Provide a password to protect sensitive information that is kept on the node
#NODE_PASSWORD=<AUTHENTICATION_NODE_PASSWORD>
# user that can connect to this node [Default: user1]
USER_NAME=user1
# Password associated with the user
#USER_PASSWORD=<AUTHENTICATION_USER_PASSWORD>
# The type of user [Default: admin]
USER_TYPE=admin
# Password used by the ROOT member in authentication
#ROOT_PASSWORD=<AUTHENTICATION_ROOT_PASSWORD>

# --- Networking ---
# External IP address of the machine
#EXTERNAL_IP=<NETWORKING_EXTERNAL_IP>
# Local or  internal network IP address of the machine
#INTERNAL_IP=<NETWORKING_INTERNAL_IP>
# Configurable (local) IP address that can be used when behind a proxy, or using Kubernetes for static IP
#PROXY_IP=<NETWORKING_PROXY_IP>
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network [Default: 32048]
ANYLOG_SERVER_PORT=32048
# Port address used by AnyLog's REST protocol [Default: 32049]
ANYLOG_REST_PORT=32049
# Port value to be used as an MQTT broker, or some other third-party broker
ANYLOG_BROKER_PORT=32050
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs) [Default: false]
TCP_BIND=false
# The number of concurrent threads supporting HTTP requests.	 [Default: 6]
TCP_THREADS=6
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs) [Default: true]
REST_BIND=true
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error. [Default: 20]
REST_TIMEOUT=20
# The number of concurrent threads supporting HTTP requests.	 [Default: 6]
REST_THREADS=6
# Boolean value to determine if messages are send over HTTPS with client certificates. [Default: False]
REST_SSL=False
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs) [Default: false]
BROKER_BIND=false
# The number of concurrent threads supporting HTTP requests.	 [Default: 6]
BROKER_THREADS=6

# --- Database ---
# Physical database type [Default: sqlite]
DB_TYPE=psql
# Username for SQL database connection
DB_USER=admin
# Password correlated to database user
DB_PASSWD=passwd
# Database IP address [Default: 127.0.0.1]
DB_IP=127.0.0.1
# Database port number [Default: 5432]
DB_PORT=5432
# Whether to set autocommit data [Default: false]
AUTOCOMMIT=true
# Whether to start to start system_query logical database [Default: false]
SYSTEM_QUERY=true
# Run system_query using in-memory SQLite. If set to false, will use pre-set database type [Default: true]
MEMORY=true
# Whether to enable NoSQL logical database [Default: false]
NOSQL_ENABLE=true
# Physical database type [Default: mongo]
NOSQL_TYPE=mongo
# Username for SQL database connection
NOSQL_USER=admin
# Password correlated to database user
NOSQL_PASSWD=passwd
# Database IP address [Default: 127.0.0.1]
NOSQL_IP=127.0.0.1
# Database port number [Default: 27017]
NOSQL_PORT=27017
# Store blobs in database [Default: true]
NOSQL_BLOBS_DBMS=true
# Store blobs in folder [Default: true]
NOSQL_BLOBS_FOLDER=true
# Compress stored blobs [Default: false]
NOSQL_BLOBS_COMPRESS=false
# Whether (re)store a blob if already exists [Default: true]
NOSQL_BLOBS_REUSE=true

# --- Blockchain ---
# TCP connection information for Master Node [Default: 127.0.0.1:32048]
LEDGER_CONN=127.0.0.1:32048
# How often to sync from blockchain [Default: 30 second]
SYNC_TIME=30 second
# Source of where the data is coming from [Default: master]
BLOCKCHAIN_SOURCE=master
# Where will the copy of the blockchain be stored [Default: file]
BLOCKCHAIN_DESTINATION=file

# --- Operator ---
# Operator ID
#MEMBER=<OPERATOR_MEMBER>
# Owner of the cluster [Default: new-company-cluster]
CLUSTER_NAME=new-company-cluster
# Logical database name [Default: test]
DEFAULT_DBMS=test
# Whether of not to enable HA against the cluster [Default: false]
ENABLE_HA=false
# How many days back to sync between nodes [Default: 30]
START_DATE=30
# Whether to enable partitioning [Default: false]
ENABLE_PARTITIONS=false
# Which tables to partition [Default: *]
TABLE_NAME=*
# Which timestamp column to partition by [Default: insert_timestamp]
PARTITION_COLUMN=insert_timestamp
# Time period to partition by [Default: 14 days]
PARTITION_INTERVAL=14 days
# How many partitions to keep [Default: 6]
PARTITION_KEEP=6
# How often to check if an old partition should be removed [Default: 1 day]
PARTITION_SYNC=1 day
# Whether to create a new table in the operator [Default: true]
CREATE_TABLE=true
# Record data inserted on Operator [Default: true]
UPDAE_TSD_INFO=true
# Archive data coming in [Default: true]
ARCHIVE=true
# Compress JSON and SQL file(s) backup [Default: true]
COMPRESS_FILE=true
# How many threads to use in the operator process [Default: 1]
OPERATOR_THREADS=1

# --- Publisher ---
# Location of logical database name within file name [Default: 0]
DBMS_FILE_LOCATION=file_name[file_name[0]]
# Location of table name within file name [Default: 1]
TABLE_FILE_LOCATION=file_name[file_name[1]]
# Compress JSON and SQL file(s) backup [Default: true]
PUBLISHER_COMPRESS_FILE=true

# --- MQTT ---
# Whether to enable the default MQTT process [Default: false]
ENABLE_MQTT=true
# Whether to enable MQTT logging process [Default: false]
MQTT_LOG=false
# IP address of MQTT broker [Default: driver.cloudmqtt.com]
MQTT_BROKER=driver.cloudmqtt.com
# Port associated with MQTT broker [Default: 18785]
MQTT_PORT=18785
# User associated with MQTT broker [Default: ibglowct]
MQTT_USER=ibglowct
# Password associated with MQTT user [Default: MSY4e009J7ts]
MQTT_PASSWD=MSY4e009J7ts
# Topic to get data for [Default: anylogedgex]
MQTT_TOPIC=anylogedgex
# Logical database name [Default: test]
MQTT_DBMS=test
# Table where to store data [Default: rand_data]
MQTT_TABLE=rand_data
# Timestamp column name [Default: now]
MQTT_TIMESTAMP_COLUMN=now
# Value column name [Default: bring [readings][][value]]
MQTT_VALUE_COLUMN=bring [readings][][value]
# Column value type [Default: float]
MQTT_VALUE_COLUMN_TYPE=float

# --- Advanced Settings ---
# Whether to automatically run a local (or personalized) script at the end of the process [Default: false]
DEPLOY_LOCAL_SCRIPT=false
# Number of parallel queries [Default: 3]
QUERY_POOL=3
# When data comes in write to database immidiately, as opposed to waiting for a full buffer [Default: true]
WRITE_IMMEDIATE=true
# If buffer is not full, how long to wait until pushing data through [Default: 60 seconds]
THRESHOLD_TIME=60 seconds
# Buffer size to reach, at which point data is pushed through [Default: 10KB]
THRESHOLD_VOLUME=10KB
```

2. By default, AnyLog is deployed using our `predevelop` version. Version changes can be done in the [.env](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-rest/.env)
```dotenv
BUILD=predevelop
ENV_FILE=anylog_configs.env
CONTAINER_NAME=anylog-node
NETWORK=host
```

3. Deploy Node
```shell
cd $HOME/deployments/docker-compose/anylog-rest/
docker-compose up -d
```


### Deployment Process 
Details regarding what AnyLog needs to accomplish in order for a node to act as: 
* [master](master_node_deployment_process.md)
* [operator](operator_node_deployment_process.md)
* [query](query_node_deployment_process.md)
* [publisher](publisher_node_deployment_process.md)