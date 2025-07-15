# Installing AnyLog

AnyLog / EdgeLake can be deployed using a variety of deployment options.

* [Network Architecture](#network-architecture)
* [Deployment Options](#deployment-options)
  * [Requirements](#requirements) 
  * [Configurations](#configuration)
  * [Docker / Podman](deployments/docker_podman.md)
  * [Kubernetes](deployments/k8s.md) 
  * [AnyLog as Service](deployments/AnyLog_as_Service.md)
  * [Pip Package](deployments/Pip_Install.md)
  * VirtualBox
  * [Third-Party Deployments](#third-party-deployments)
* [Agent Components](#agent-components)
  * [Local Directories](#local-directory-structure)
  * [Services & Databases](#services--databases)
* [CLI Commands](#anylog-cli)

--- 

## Network Architecture

AnyLog is a network of agents that allows you to manage real-time and IoT data directly at the edge. Think of it as moving data from a centralized, cloud-based data lake to transforming your edge nodes into a distributed data lake with cloud-level capabilities.


To demonstrate the capabilities of AnyLog / EdgeLake, we recommend deploying a network of four agents, as shown in the diagram below.
* 1 Master node 
* 2 Operators 
* 1 Query 

These nodes can be deployed across multiple machines or run as four separate containers on a single machine.
1. Each container must be assigned unique ports.
2. Use SQLite or assign a unique logical database name to each operator to avoid data overlap when deploying multiple operators on the same machine
3. Each AnyLog agent should generally have a unique name.

<div style="text-align: center;">
  <img src="imgs/deployment_diagram.png" alt="AnyLog Deployment Diagram" width="600" />
</div>




--- 

## Deployment Options
The AnyLog agents are less than 150MB, however, since they are service based all relevant pip packages get installed 
when deploying via container services like _Docker_ and _Kubernetes_

### Requirements
AnyLog / EdgeLake is a Python-based program supported with Python version 3.9 or newer. 

| Package Name                    | Description                                     | PyPI Link                                                                  | Required |
| ------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------- | -------- |
| **cython**                      | Optimizing static compiler for Python           | [cython](https://pypi.org/project/cython/)                                 | ✅        |
| **pyyaml**                      | YAML parser and emitter for Python              | [pyyaml](https://pypi.org/project/PyYAML/)                                 | ✅        |
| **pyinstaller**                 | Bundle Python apps into stand-alone executables | [pyinstaller](https://pypi.org/project/pyinstaller/)                       | ✅        |
| **six**                         | Python 2 and 3 compatibility utilities          | [six](https://pypi.org/project/six/)                                       | ✅        |
| **requests**                    | HTTP library for human-friendly networking      | [requests](https://pypi.org/project/requests/)                             | ✅        |
| **cryptography**                | Secure communications and encryption            | [cryptography](https://pypi.org/project/cryptography/)                     | ✅        |
| **pyjwt**                       | JSON Web Token implementation                   | [pyjwt](https://pypi.org/project/PyJWT/)                                   | ✅        |
| **pyOpenSSL**                   | Python interface to OpenSSL                     | [pyOpenSSL](https://pypi.org/project/pyOpenSSL/)                           | ✅        |
| **psutil**                      | Process and system utilities                    | [psutil](https://pypi.org/project/psutil/)                                 | ✅        |
| **orjson**                      | Ultra-fast JSON parsing and serialization       | [orjson](https://pypi.org/project/orjson/)                                 | ✅        |
| **python-dateutil**             | Extensions to the `datetime` module             | [python-dateutil](https://pypi.org/project/python-dateutil/)               | ✅        |
| **pytz**                        | Time zone definitions for Python                | [pytz](https://pypi.org/project/pytz/)                                     | ✅        |
| **psycopg2-binary**             | PostgreSQL database adapter                     | [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)               | ✅        |
| **pymongo**                     | MongoDB driver for Python                       | [pymongo](https://pypi.org/project/pymongo/)                               | ✅        |
| **paho-mqtt**                   | MQTT client library for IoT messaging           | [paho-mqtt](https://pypi.org/project/paho-mqtt/)                           | ✅        |
| **kafka-python**                | Apache Kafka client for Python                  | [kafka-python](https://pypi.org/project/kafka-python/)                     | ✅        |
| **opcua**                       | OPC UA protocol support                         | [opcua](https://pypi.org/project/opcua/)                                   | ✅        |
| **xhtml2pdf**                   | HTML/CSS to PDF converter                       | [xhtml2pdf](https://pypi.org/project/xhtml2pdf/)                           | ❌        |
| **grpcio**                      | gRPC core library                               | [grpcio](https://pypi.org/project/grpcio/)                                 | ❌        |
| **grpcio-tools**                | Protobuf/gRPC compiler tools                    | [grpcio-tools](https://pypi.org/project/grpcio-tools/)                     | ❌        |
| **grpcio-reflection**           | Reflection support for gRPC servers             | [grpcio-reflection](https://pypi.org/project/grpcio-reflection/)           | ❌        |
| **py-ecc**                      | ECC for blockchain (Ethereum)                   | [py-ecc](https://pypi.org/project/py-ecc/)                                 | ❌        |
| **web3**                        | Ethereum blockchain interface                   | [web3](https://pypi.org/project/web3/)                                     | ❌        |
| **numpy**                       | Core numerical computing library                | [numpy](https://pypi.org/project/numpy/)                                   | ❌        |
| **opencv-python-headless**      | OpenCV library without GUI features             | [opencv-python-headless](https://pypi.org/project/opencv-python-headless/) | ❌        |
| **base64** *(not listed)*       | Encoding/decoding base64 (part of stdlib)       | *(builtin)*                                                                | ❌        |
| **reportlab** *(commented out)* | PDF generation toolkit                          | [reportlab](https://pypi.org/project/reportlab/)                           | ❌        |


### Configuration
When deploying AnyLog via containers or third-party deployments, the services enabled on the agent are based on user-defined
environment configurations. While most of the configurations have default values, at the very least, a deployment must include:
* `INIT_TYPE` - prod or bash (will enter shell interface)
* `NODE_TYPE` - master, operator, query or publisher
* `NODE_NAME`
* `COMPANY_NAME`
* `LICENSE_KEY` - To get a license key please reach out to our <a href="https://www.anylog.network/download" target="_blank">Download Page</a>

**Base Configurations** 
```dotenv
#--- General ---
# AnyLog License Key
LICENSE_KEY=""
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols
NODE_TYPE=generic
# Name of the AnyLog instance
NODE_NAME=anylog-node
# Owner of the AnyLog instance
COMPANY_NAME=New Company

#--- Networking ---
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32548
# Port address used by AnyLog's REST protocol
ANYLOG_REST_PORT=32549
# Port value to be used as an MQTT broker, or some other third-party broker
ANYLOG_BROKER_PORT=32550
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
# Whether to start to start system_query logical database
SYSTEM_QUERY=false
# Run system_query using in-memory SQLite. If set to false, will use pre-set database type
MEMORY=true

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
# TCP connection information for Master Node
LEDGER_CONN=127.0.0.1:32048

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

#--- Monitoring ---
# Whether to monitor the node or not
MONITOR_NODES=true
# Store monitoring in Operator node(s)
STORE_MONITORING=false
# For operator, accept syslog data from local (Message broker required)
SYSLOG_MONITORING=false

#--- Advanced Settings ---
# Whether to automatically run a local (or personalized) script at the end of the process
DEPLOY_LOCAL_SCRIPT=false
# Run code in debug mode
DEBUG_MODE=false
```

**Advanced Configurations**: 
```dotenv
#--- Directories ---
# AnyLog Root Path
ANYLOG_PATH=/app
# !local_scripts: ${ANYLOG_HOME}/deployment-scripts/scripts
LOCAL_SCRIPTS=/app/deployment-scripts/scripts
# !test_dir: ${ANYLOG_HOME}/deployment-scripts/tests
TEST_DIR=/app/deployment-scripts/tests

# --- General ---
# Disable AnyLog's CLI interface
DISABLE_CLI=false
# Enable Remote-CLI
REMOTE_CLI=false

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
# Overlay IP address - if set, will replace local IP address when connecting to network
OVERLAY_IP=""
# The number of concurrent threads supporting HTTP requests.
TCP_THREADS=6
# Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
REST_TIMEOUT=30
# The number of concurrent threads supporting HTTP requests.
REST_THREADS=6
# The number of concurrent threads supporting broker requests.
BROKER_THREADS=6

#--- Blockchain ---
# How often to sync from blockchain
BLOCKCHAIN_SYNC=30 second
# Source of where the data is coming from
BLOCKCHAIN_SOURCE=master
# Where will the copy of the blockchain be stored
BLOCKCHAIN_DESTINATION=file

#--- Operator ---
# Operator ID
MEMBER=""
# How many days back to sync between nodes
START_DATE=30
# Whether to enable partitioning
ENABLE_PARTITIONS=true
# Which tables to partition
TABLE_NAME=*
# Which timestamp column to partition by
PARTITION_COLUMN=insert_timestamp
# Time period to partition by
PARTITION_INTERVAL=1 day
# How many partitions to keep
PARTITION_KEEP=3
# How often to check if an old partition should be removed
PARTITION_SYNC=1 day

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
ENABLE_NEBULA=false
# create new nebula keys
NEBULA_NEW_KEYS=false
# whether node is type lighthouse
IS_LIGHTHOUSE=false
# Nebula CIDR IP address for itself - the IP component should be the same as the OVERLAY_IP (ex. 10.10.1.15/24)
CIDR_OVERLAY_ADDRESS=""
# Nebula IP address for Lighthouse node (ex. 10.10.1.15)
LIGHTHOUSE_IP=""
# External physical IP of te node associated with Nebula lighthouse
LIGHTHOUSE_NODE_IP=""
```

### Third-Party Deployments

AnyLog / EdgeLake is supported by third-party orchestrators such as
* IBM's OpenHorizon
* Dell NativeEdge
* Intel Tiber 
* Zededa / Eve Orchestrator



--- 

## Agent Components

A node in the network is assigned with one or more roles, those roles are based on differnt services and logical databases
being utilized by the agent. The optional roles are the following:

|                                                  Node Type                                                  |                                                	Role                                                 |
|:-----------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:| 
|                                                  Operator                                                   |                          	A node that hosts the data and satisfies queries.                          |
|                               Query	|                              A node that orchestrates a query process.                               | 
| Master	| A node that hosts the metadata on a ledger and serves the metadata to the peer nodes in the network. | 
| Publisher	| A node that receives data from a data source (i.e. devices, applications) and distributes the data to Operators. |

### Local directory structure
AnyLog directory setup is configurable. The default setup is detailed below:

```tree
Directory Structure   Explabnation
-------------------   -----------------------------------------
--> AnyLog-Network    [AnyLog Root]
    -->anylog         [Directory containing authentication keys and passwords]
    -->blockchain     [A JSON file representing the metadata relevant to the node]
    -->data           [Users data and intermediate data processed by this node]
       -->archive     [The root directory of and archival directory]
       -->bkup        [Optional location for backup of user data]
       -->blobs       [Directory containing unstructured data]
       -->dbms        [Optional location for persistent database data. If using SQLite, used for persistent SQLIte data]
       -->distr       [Directory used in the High Availability processes]
       -->error       [The storage location for new data that failed database storage]
       -->pem         [Directory containing keys and certificates]
       -->prep        [Directory for system intermediate data]
       -->test        [Directory location for output data of test queries] 
       -->watch       [Directory monitored by the system, data files placed in the directory are being processed] 
       -->bwatch      [Directory monitored by the system, managing unstructured data]
    -->source         [The root directory for source or executable files]
    -->scripts        [System scripts to install and configure the AnyLog node]
       -->install     [Installation scripts]
       -->anylog      [Configuration Scripts]
    -->local_scripts  [Users scripts]
```

* The following command creates the work folders if they do not exist:
```anylog
create work directories
```
The command needs to be issued only once on the physical or virtual machine.

* The following command list the directories on an AnyLog node:
```anylog
get dictionary _dir
```

### Services & Databases

* View the list of active services - `get processes` 

```anylog
    Process         Status       Details                                                                     
    ---------------|------------|---------------------------------------------------------------------------|
    TCP            |Running     |Listening on: 10.10.1.31:32348, Threads Pool: 6                            |
    REST           |Running     |Listening on: 23.239.12.151:32349, Threads Pool: 5, Timeout: 20, SSL: False|
    Operator       |Not declared|                                                                           |
    Blockchain Sync|Running     |Sync every 30 seconds with master using: 10.10.1.10:32048                  |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)] [1 (user)]                             |
    Blobs Archiver |Not declared|                                                                           |
    MQTT           |Not declared|                                                                           |
    Message Broker |Not declared|No active connection                                                       |
    SMTP           |Not declared|                                                                           |
    Streamer       |Not declared|                                                                           |
    Query Pool     |Running     |Threads Pool: 3                                                            |
    Kafka Consumer |Not declared|                                                                           |
    gRPC           |Not declared|                                                                           |
    PLC Client     |Not declared|                                                                           |
    Pull Processes |Not declared|                                                                           |
    Publisher      |Not declared|                                                                           |
    Distributor    |Not declared|                                                                           |
    Consumer       |Not declared|                                                                           |
```

* View list of connected databases - `get databases`

```anylog
Active DBMS Connections
Logical DBMS Database Type Owner  IP:Port         Configuration                                Storage                                       
------------|-------------|------|---------------|--------------------------------------------|---------------------------------------------|
almgm       |sqlite       |system|Local          |Autocommit On, Fsync full (after each write)|/app/AnyLog-Network/data/dbms/almgm.dbms     |
blobs_edgex |mongo        |user  |127.0.0.1:27017|                                            |Blobs Persistent                             |
edgex       |sqlite       |user  |Local          |Autocommit On, Fsync full (after each write)|/app/AnyLog-Network/data/dbms/edgex.dbms     |
monitoring  |sqlite       |user  |Local          |Autocommit On, Fsync full (after each write)|/app/AnyLog-Network/data/dbms/monitoring.dbms|
```