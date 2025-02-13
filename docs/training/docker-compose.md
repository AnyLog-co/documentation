# Deploy AnyLog 

## Requirements
* [Docker](https://docs.docker.com/engine/install/) 
* [docker-compose](https://docs.docker.com/compose/install/) 
* make

```shell
sudo apt-get -y update 
sudo apt-get -y install docker docker-compose make 

# set permissions 
USER=`whoami`
sudo groupadd docker
sudo usermod -aG docker ${USER}
newgrp docker
```

## General Steps
1. Download [docker-compose](https://github.com/AnyLog-co/docker-compose)
```shell
cd $HOME
git clone https://github.com/AnyLog-co/docker-compose 
```

2. Log into AnyLog docker repository 
   * [Request license key](https://anylog.co/download-anylog/)
   * Log into AnyLog 
```shell
cd $HOME/docker-compose 
make login ANYLOG_TYPE=[DOCKER_PASSWORD]
```

3. Update Configurations
    * **Master**: [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/master-configs/base_configs.env) | [advanced](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/master-configs/advance_configs.env)
    * **Operator**: [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/operator-configs/base_configs.env) | [advanced](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/operator-configs/advance_configs.env)
    * **Query**: [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/query-configs/base_configs.env) | [advanced](https://github.com/AnyLog-co/docker-compose/blob/query-dev/docker-makefile/query-configs/advance_configs.env)
    * **Publisher**: [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/publisher-configs/base_configs.env) | [advanced](https://github.com/AnyLog-co/docker-compose/blob/query-dev/docker-makefile/publisher-configs/advance_configs.env)

Basic sample configurations for Operator Node     

**Basic Configurations**:
```dotenv
#--- General ---
# AnyLog License Key
LICENSE_KEY=""
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols
NODE_TYPE=operator
# Name of the AnyLog instance
NODE_NAME=anylog-operator
# Owner of the AnyLog instance
COMPANY_NAME=New Company

#--- Networking ---
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32148
# Port address used by AnyLog's REST protocol
ANYLOG_REST_PORT=32149
# Port value to be used as an MQTT broker, or some other third-party broker
ANYLOG_BROKER_PORT=""
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
TCP_BIND=false
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
REST_BIND=false
# A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
BROKER_BIND=false

#--- Database ---
# Physical database type (sqlite or psql)
DB_TYPE=sqlite
# Username for SQL database connection
DB_USER=""
# Password correlated to database user
DB_PASSWD=""
# Database IP address
DB_IP=127.0.0.1
# Database port number
DB_PORT=5432
# Whether to set autocommit data
AUTOCOMMIT=false
# Whether to enable NoSQL logical database
ENABLE_NOSQL=false

#--- Blockchain ---
# TCP connection information for Master Node
LEDGER_CONN=127.0.0.1:32048

#--- Operator ---
# Owner of the cluster
CLUSTER_NAME=new-company-cluster1
# Logical database name
DEFAULT_DBMS=new_company

#--- MQTT ---
# Whether to enable the default MQTT process
ENABLE_MQTT=false

# IP address of MQTT broker
MQTT_BROKER=139.144.46.246
# Port associated with MQTT broker
MQTT_PORT=1883
# User associated with MQTT broker
MQTT_USER=anyloguser
# Password associated with MQTT user
MQTT_PASSWD=mqtt4AnyLog!
# Whether to enable MQTT logging process
MQTT_LOG=false

# Topic to get data for
MSG_TOPIC=anylog-demo
# Logical database name
MSG_DBMS=new_company
# Table where to store data
MSG_TABLE=bring [table]
# Timestamp column name
MSG_TIMESTAMP_COLUMN=now
# Value column name
MSG_VALUE_COLUMN=bring [value]
# Column value type
MSG_VALUE_COLUMN_TYPE=float

#--- Advanced Settings ---
# Whether to automatically run a local (or personalized) script at the end of the process
DEPLOY_LOCAL_SCRIPT=false
# Deploy a process that accepts syslog - requires Message broker running
DEPLOY_SYSLOG=false
# Whether to monitor the node or not
MONITOR_NODES=false
```

**Advanced Configurations**:
```dotenv

#--- Directories ---
# AnyLog Root Path - if changed make sure to change volume path in docker-compose-template
ANYLOG_PATH=/app
# !local_scripts: ${ANYLOG_HOME}/deployment-scripts/scripts
LOCAL_SCRIPTS=/app/deployment-scripts/node-deployment
# !test_dir: ${ANYLOG_HOME}/deployment-scripts/test
TEST_DIR=/app/deployment-scripts/tests

# --- General ---
# Disable AnyLog's CLI interface
DISABLE_CLI=false

#--- Geolocation ---
# Coordinates of the machine - used by Grafana to map the network
LOCATION=""
# Country where machine is located
COUNTRY=""
# State where machine is located
STATE=""
# City where machine is located
CITY=""

#--- Networking ---
# Declare Policy name
CONFIG_NAME=""
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=""
# Configurable (local) IP address that can be used when behind a proxy, or using Kubernetes for static IP
PROXY_IP=""
# The number of concurrent threads supporting HTTP requests.
TCP_THREADS=6
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
REST_TIMEOUT=30
# The number of concurrent threads supporting HTTP requests.	
REST_THREADS=6
# The number of concurrent threads supporting broker requests.
BROKER_THREADS=6

#--- Database ---
# Whether to start to start system_query logical database
SYSTEM_QUERY=false
# Run system_query using in-memory SQLite. If set to false, will use pre-set database type
MEMORY=false
# Whether to enable NoSQL logical database
ENABLE_NOSQL=false
# Physical database type
NOSQL_TYPE=mongo
# Username for SQL database connection
NOSQL_USER=""
# Password correlated to database user
NOSQL_PASSWD=""
# Database IP address
NOSQL_IP=127.0.0.1
# Database port number
NOSQL_PORT=27017
# Store blobs in database
BLOBS_DBMS=false
# Whether (re)store a blob if already exists
BLOBS_REUSE=true

#--- Blockchain ---
# How often to sync from blockchain
SYNC_TIME=30 second
# Source of where the data is coming from
BLOCKCHAIN_SOURCE=master
# Where will the copy of the blockchain be stored
BLOCKCHAIN_DESTINATION=file

#--- Operator ---
# Operator ID
MEMBER=""
# Whether of not to enable HA against the cluster
ENABLE_HA=false
# How many days back to sync between nodes
START_DATE=30
# Whether to enable partitioning
ENABLE_PARTITIONS=true
# Which tables to partition
TABLE_NAME=*
# Which timestamp column to partition by
PARTITION_COLUMN=timestamp
# Time period to partition by
PARTITION_INTERVAL=14 days
# How many partitions to keep
PARTITION_KEEP=3
# How often to check if an old partition should be removed
PARTITION_SYNC=1 day
# How many threads to use in the operator process
OPERATOR_THREADS=3

#--- Monitoring ---
# Which node type to send monitoring information to
MONITOR_NODE=query

#--- Advanced Settings ---
# Compress JSON and SQL file(s) backup
COMPRESS_FILE=true
# Number of parallel queries
QUERY_POOL=6
# When data comes in write to database immediately, as opposed to waiting for a full buffer
WRITE_IMMEDIATE=false
# If buffer is not full, how long to wait until pushing data through
THRESHOLD_TIME=60 seconds
# Buffer size to reach, at which point data is pushed through
THRESHOLD_VOLUME=10KB

#--- Nebula ---
# whether to enable Lighthouse
ENABLE_NEBULA=true
# whether node is type lighthouse
IS_LIGHTHOUSE=false
# Nebula IP address for Lighthouse node
LIGHTHOUSE_IP=""
# External physical IP of the node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=""
```

3. Deploy AnyLog 
```shell
cd $HOME/docker-compose
make up ANYLOG_TYPE=[NODE_TYPE]

# example
make up ANYLOG_TYPE=master
```


## Extending docker-compose

### Enable Remote-CLI
The default _docker-compose_ can be extended to install [_Remote-CLI_](../northbound%20connectors/remote_cli.md) as part 
of the same (Query node) deployment. This is important when querying blob data.

**Steps**
1. Update configurations for node

2. Uncomment [docker-compose-template.yaml](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/docker-compose-template.yaml)
```yaml
version: "3"
services:
  remote-cli:
    image: anylogco/remote-cli:latest
    container_name: remote-cli
    restart: always
    stdin_open: true
    tty: true
    ports:
      - ${CLI_PORT}:${CLI_PORT}
    environment:
      - CONN_IP=${CONN_IP}
     - CLI_PORT=${CLI_PORT}
    volumes:
      - remote-cli:/app/Remote-CLI/djangoProject/static/json
      - remote-cli-current:/app/Remote-CLI/djangoProject/static/blobs/current/
  anylog-${ANYLOG_TYPE}:
    image: anylogco/anylog-network:${TAG}
    restart: always
    env_file:
      - ${ANYLOG_TYPE}-configs/base_configs.env
      - ${ANYLOG_TYPE}-configs/advance_configs.env
      - .env
    container_name: anylog-${ANYLOG_TYPE}
    stdin_open: true
    tty: true
    network_mode: host
    volumes:
      - anylog-${ANYLOG_TYPE}-anylog:/app/AnyLog-Network/anylog
      - anylog-${ANYLOG_TYPE}-blockchain:/app/AnyLog-Network/blockchain
      - anylog-${ANYLOG_TYPE}-data:/app/AnyLog-Network/data
      - anylog-${ANYLOG_TYPE}-local-scripts:/app/deployment-scripts
      - anylog-${NODE_TYPE}-nebula:/app/AnyLog-Network/nebula
      - remote-cli-current:/app/Remote-CLI/djangoProject/static/blobs/current/
volumes:
  anylog-${ANYLOG_TYPE}-anylog:
  anylog-${ANYLOG_TYPE}-blockchain:
  anylog-${ANYLOG_TYPE}-data:
  anylog-${ANYLOG_TYPE}-local-scripts:
  anylog-${NODE_TYPE}-nebula:
  remote-cli:
  remote-cli-current:
```
 
3. Deploy AnyLog 
```shell
cd $HOME/docker-compose
make up ANYLOG_TYPE=[NODE_TYPE]

# example
make up ANYLOG_TYPE=query
```

### Multiple Nodes of the Same Type on a single machine
Users may want to deploy multiple nodes of the same type (usually Operator) on the same machine. In order to do this,
each docker container needs a **unique** name. When deploying nodes of the same type on **different** machines, there's no
need to deal with this section. 

1. Copy configurations into a directory 
```shell
cp -r $HOME/docker-compose/docker-compose/anylog-operator $HOME/docker-compose/docker-compose/anylog-operator2 
```

2. Update configurations for node - make sure each of the node has unique PORT values

3. Deploy operator(s) 
```shell
cd $HOME/docker-compose
make up ANYLOG_TYPE=[NODE_TYPE]

# deploy operator 1
make up ANYLOG_TYPE=operator

# deploy operator 2
make up ANYLOG_TYPE=operator2
```

## Other Services
[Support Tools director](https://github.com/AnyLog-co/docker-compose/tree/os-dev/support-tools) provides docker deployment commands / .env files for
* Grafana
* MongoDB 
* Postgres
* nginx 
* AnyLog's Remote-CLI


