# AnyLog on Docker 

AnyLog can be run either directly on a physical machine, or as a Docker container.
Steps to install docker can be found here: https://docs.docker.com/engine/install/ 

Since our Docker repository is private, please <a href="mailto:info@anylog.co?subject=Request Docker access">contact us</a> for access.

## Docker Versions
AnyLog has 3 major versions, each version is built on both Ubuntu:20.04 with python:3.9-alpine. 
* develop - is a stable release that's been used as part of our Test Network for a number of weeks, and gets updated every 4-6 weeks.
* predevelop - is our beta release, which is being used by our Test Network for testing purposes.
* testing - Any time there's a change in the code we deploy a "testing" image to be used for (internal) testing purposes. Usually the image will be Ubuntu based, unless stated otherwise.

| Build | Base Image | CPU Architecture | Pull Command | Size | 
|---|---|---|---|---|
| develop | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:develop` |
| develop-alpine | python:3.9-alpine | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:develop-alpine` |
| predevelop | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:predevelop` |
| predevelop-alpine | python:3.9-alpine | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:predevelop-alpine` | 460MB| 
| testing | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:testing` |

For _develop_ and _predevelop_ builds users could also specify `preset` which downloads an AnyLog image with preset network configurations and gets deployed as a node of type REST.  

Sample Pull Command: `docker pull oshadmon/anylog:predevelop-alpine-preset`

## Docker Volumes 
When deploying AnyLog on Docker it's recommended to set volumes in order to access physical data stored within AnyLog. 
Details regarding data structure can be found in _[Getting Started](getting%20started.md#local-directory-structure)_
* anylog (`al-${NODE_NAME}-${NODE-TYPE}-anylog:/app/AnyLog-Network/anylog:rw`) - contains authentication keys and passwords
* blockchain (`al-${NODE_NAME}-${NODE-TYPE}-blockchain:/app/AnyLog-Network/blockchain:rw`) - contains a JSON copy of the blockchain
* data (`al-${NODE_NAME}-${NODE-TYPE}-data:/app/AnyLog-Network/data:rw`) - contains data files, as well as SQLite data
* local_scripts (`al-${NODE_NAME}-${NODE-TYPE}-local-scripts:/app/AnyLog-Network/local_scripts:rw`) - contains AnyLog scripts used to deploy an instance based on `NODE_TYPE` 
* scripts (`al-${NODE_NAME}-${NODE-TYPE}-scripts:/app/AnyLog-Network/scripts:rw`) - contains shell scripts used to deploy AnyLog

To manually access these directories use `docker inspect` command
```shell
docker volume inspect al-operator2-data 
[
    {
        "CreatedAt": "2021-12-13T02:56:51Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/al-operator2-data/_data",
        "Name": "afg-operator2-data",
        "Options": null,
        "Scope": "local"
    }
]
```


## Sample Docker Calls
Based on the `NODE_TYPE` environment the code is aware the kind of Anylog node type to be deployed
```shell
# general docker run call - parameters that are not required are set in [square brakets]
docker run --network host --name ${CONTAINER_NAME} \
    -e NODE_TYPE=${NODE_TYPE} \ # Node type 
    -e COMPANY_NAME=${COMPANY_NAME} \ # company name 
    -e NODE_NAME=${NODE_NAME} \ # node name
    [-e LOCATION=${LOCATION} \]  
    -e ANYLOG_SERVER_PORT=${ANYLOG_SERVER_PORT} \ # Port to be for TCP connection
    -e ANYLOG_REST_PORT=${ANYLOG_REST_PORT} \ # Port to be used for REST connections 
    [-e ANYLOG_BROKER_PORT=${ANYLOG_BROKER_PORT} \] # Port used for internal MQTT Broker -- optional  
    -e MASTER_NODE=${MASTER_NODE} \ # Master Node credentials (IP:PORT)
    -e SYNC_TIME="30 second" \ # Frequency to sync blockchain from master 
    -e DB_TYPE=${DB_TYPE} \ # Databsae type 
    -e DB_USER=${USER}@${IP}:${PASSOWRD} \ # Database credentials 
    -e DB_PORT=5432 \ # Database port 
    -e DEFAULT_DBMS=${DB_NAME} \ # Logical database name - required for Operator only
    -e CLUSTER_NAME=${CLUSTER_NAME} \ # cluster name
    -e ENABLE_PARTITION=${ENABLE_CLUSTER} \ # Whether or not to enable data partitioning (true | false) 
    [-e PARTITION_COLUMN=${PARTITION_COLUMN}] \ # (timestamp) column to partition by - required when partition is enabled 
    [-e PARTITION_INTERVAL=${PARTITION_INTERVAL}] \ # period of time to partition by - required when partition is enabled
    -e DROP_PARTITION=${DROP_PARTITION} \ # Whether or not to drop partition (true | false) 
    [-e PARTITION_KEEP=${PARTITION_KEEP} \]  # number of partitions to keep - required if drop partition is enabled 
    -e ENABLE_DATA_MONITOR={ENABLE_DATA_MONITOR} \ $ whether to monitor data (true | false) 
    [-e TABLE_NAME=* \] # table(s) to monitor - required when data monitoring is enabled
    [-e INTERVAL_VALUE=${INTERVAL_VALUE} \] # number of times to keep monitored results - required when data monitoring is enabled
    [-e DATA_MONITOR_INTERVAL=${DATA_MONITOR_INTERVAL} \] # frequency of data monitoring - required when data monitoring is enabled
    [-e DATA_MONITOR_COLUMN=${DATA_MONITOR_COLUMN} \] # column to monitor by - required when data monitoring is enabled
    -e MQTT_ENABLE=${MQTT_ENABLE} \ # whether or not to enable MQTT (true | false)
    [-e BROKER=${BROKER} \] # MQTT broker - required only if MQTT is enabled  
    [-e MQTT_PORT=${MQTT_PORT} \] # MQTT port - required only if MQTT is enabled
    [-e MQTT_USER=${$MQTT_USER} \] # MQTT user - required only if MQTT is enabled
    [-e MQTT_PASSWORD=${MQTT_PASSWORD} \] # MQTT user password - required only if MQTT is enabled 
    [-e MQTT_LOG=false \] - whether or not to enable MQTT logging - required only if MQTT is enabled (true | false)
    [-e MQTT_TOPIC_NAME=${TOPIC_NAME} \] # MQTT topic - required only if MQTT is enabled 
    [-e MQTT_TOPIC_DBMS=${DATABASE}  \] # logical database topic value - required only if MQTT is enabled
    [-e MQTT_TOPIC_TABLE=${TABLE} \] # table (in database) topic value - required only if MQTT is enabled 
    [-e MQTT_COLUMN_TIMESTAMP=${TIMESTAMP_COLUMN} \] # timestamp column topic value - required only if MQTT is enabled
    [-e MQTT_COLUMN_VALUE_TYPE=${COLUMN_VALUE_TYPE} \] # column value type topic value - required only if MQTT is enabled
    [-e MQTT_COLUMN_VALUE=${COLUMN_VALUE_NAME} \] # value column name topic value - required only if MQTT is enabled
    -v al-aiops-single-node-anylog:/app/AnyLog-Network/anylog:rw \
    -v al-aiops-single-node-blockchain:/app/AnyLog-Network/blockchain:rw \
    -v al-aiops-single-node-data:/app/AnyLog-Network/data:rw \
    -v al-aiops-single-node-local-scripts:/app/AnyLog-Network/local_scripts:rw \
    -v al-aiops-single-node-scripts:/app/AnyLog-Network/scripts:rw \
    -it --detach-keys="ctrl-d" --rm oshadmon/anylog:${BUILD}
```

* Empty Node - A node that doesn't contain anything, user should manually access it to deploy commands 
```shell
docker run --network host --name new \
  -e NODE_TYPE=none \
  -d --detach-keys="ctrl-d" --rm oshadmon/anylog:predevelop
```
* REST Node - A node that connects to TCP, REST and Message Broker (if set) as well as an optional authentication configurations

 
