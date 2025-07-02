# Deploying AnyLog

## Requirements 
* <a href="https://docs.docker.com/engine/install/" target="_blank">Docker</a> with docker-compose
* <a herf="https://www.gnu.org/software/make/" target="_blank">make</a>  
```shell
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y make docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Grant non-root user permissions to use docker
USER=`whoami`
sudo groupadd docker 
sudo usermod -aG docker ${USER} 
newgrp docker
```

AnyLog is also deployed via Podman and Kubernetes. 

## Steps

1. download repo
```shell
cd $HOME ; git clone https://github.com/AnyLog-co/docker-compose 
cd $HOME/docker-compose
```

2. Login to AnyLog's docker repository
```shell
make login ANYLOG_TYPE=a24356db46c91412a00e2a630f9264ebd5b7602b7d8649fee12928ae86356254003808d6094169657bb337161d8e8619df982d22bbe587b8de5442bc8d852c83217e7f34b17bc5accedeca247d27bb02edfaa7f26753a85e996840454a4b2be80917d82c151df03ad0b225c5e62d4ed66fd108671683fb8c1a1a14ac34d3b771{'company':'Guest','expiration':'2025-09-01','type':'beta'}
```

3. Configure Node - Details can be found in [docker-compose's readme](https://github.com/AnyLog-co/docker-compose?tab=readme-ov-file#configuration-files-breakdown)
* General configurations
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
```

* Networking
```dotenv
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
```

* Database
```dotenv
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
# Whether to start system_query logical database
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
```

* Blockchain  
```dotenv
#--- Blockchain ---
# How often to sync from blockchain
BLOCKCHAIN_SYNC=30 second
# Source of where the data is metadata stored/coming from. This can either be master for "local" install or specific
# blockchain network to be used (ex. optimism)
BLOCKCHAIN_SOURCE=master
# TCP connection information for Master Node
LEDGER_CONN=127.0.0.1:32048
```

* Operator specific configs
```dotenv
#--- Operator ---
# Owner of the cluster
CLUSTER_NAME=nc-cluster1
# Logical database name
DEFAULT_DBMS=new_company
# Whether to enable partitioning
ENABLE_PARTITIONS=true
# Which tables to partition
TABLE_NAME=*
# Which timestamp column to partition by
PARTITION_COLUMN=insert_timestamp
# Time period to partition by
PARTITION_INTERVAL=14 days
# How many partitions to keep
PARTITION_KEEP=3
# How often to check if an old partition should be removed
PARTITION_SYNC=1 day
```

* [Data Aggregation](https://github.com/AnyLog-co/documentation/blob/master/aggregations.md) & Other services
```dotenv
#--- Data Aggregation --
# Enable data aggregation based om timestamp / column
ENABLE_AGGREGATIONS=false
# Timestamp column to aggregate against
AGGREGATION_TIME_COLUMN=insert_timestamp
# Value column to aggregate against
AGGREGATION_VALUE_COLUMN=value

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
MSG_TIMESTAMP_COLUMN=bring [timestamp]
# Value column name
MSG_VALUE_COLUMN=bring [value]
# Column value type
MSG_VALUE_COLUMN_TYPE=float

#----- OPC-UA ---
# Whether or not to enable to OPC-UA service
ENABLE_OPCUA=false
# OPC-UA URL address (ex. opcua.tcp:;//127.0.0.1:4840)
OPCUA_URL=""
# Node information the root is located in (ex. ns=2;s=DataSet)
OPCUA_NODE=""
# How often to pull data from OPC-UA
OPCUA_FREQUENCY=""
```

* Node Monitoring
```dotenv
#--- Monitoring ---
# Whether to monitor the node or not
MONITOR_NODES=true
# Store monitoring in Operator node(s)
STORE_MONITORING=false
# For operator, accept syslog data from local (Message broker required)
SYSLOG_MONITORING=false
```

4. Bring up Node
```shell
make up ANYLOG_TYPE=[master | operator | query | publisher]
```