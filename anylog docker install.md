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
| develop | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:develop` | 664MB | 
| develop-alpine | python:3.9-alpine | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:develop-alpine` | 460MB| 
| predevelop | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:predevelop` | ~245MB | 
| predevelop-alpine | python:3.9-alpine | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:predevelop-alpine` | ~178MB | 
| testing | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull oshadmon/anylog:testing` |

For _develop_ and _predevelop_ builds users could also specify `preset` which downloads an AnyLog image with preset TCP/REST network configurations and gets deployed as a node of type REST. `preset` deployment uses the following environment variables:
```dockerfile 
ENV NODE_TYPE=rest
ENV ANYLOG_SERVER_PORT=2048
ENV ANYLOG_REST_PORT=2049
ENV ANYLOG_BROKER_PORT=2050
```

Sample Pull Command: `docker pull oshadmon/anylog:predevelop-alpine-preset`

## Docker Volumes 
When deploying AnyLog on Docker it's recommended to set volumes in order to access physical data stored within AnyLog. 
Details regarding data structure can be found in _[Getting Started](getting%20started.md#local-directory-structure)_
* anylog (`al-${NODE_NAME}-anylog:/app/AnyLog-Network/anylog:rw`) - contains authentication keys and passwords
* blockchain (`al-${NODE_NAME}-blockchain:/app/AnyLog-Network/blockchain:rw`) - contains a JSON copy of the blockchain
* data (`al-${NODE_NAME}-data:/app/AnyLog-Network/data:rw`) - contains data files, as well as SQLite data
* local_scripts (`al-${NODE_NAME}-local-scripts:/app/AnyLog-Network/local_scripts:rw`) - contains AnyLog scripts used to deploy an instance based on `NODE_TYPE` 
* scripts (`al-${NODE_NAME}-scripts:/app/AnyLog-Network/scripts:rw`) - contains shell scripts used to deploy AnyLog

To manually access these directories use `docker inspect` command
```bash
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


## Sample Docker Call
Based on the `NODE_TYPE` environment variable the code is aware the kind of AnyLog node type to be deployed. An explanation of the base node types can be found in _[Getting Started](getting%20started.md#type-of-instances)_ 

* [Empty Node](examples/Docker%20Calls/empty_node.sh) - node that doesn't contain anything, user should manually access it to deploy commands 
  * Env Params: `NODE_TYPE=none`
* [REST Node](examples/Docker%20Calls/rest_node.sh) - node that connects to TCP, REST and Message Broker (if set) as well as an optional authentication configurations 
  * Env Params: `NODE_TYPE=none`
* [Master Node](examples/Docker%20Calls/master_node.sh) - node that maintains a complete copy of the metadata and receives updates when the metadata is updated 
  * Env Params: `NODE_TYPE=master`
* [Operator Node](examples/Docker%20Calls/operator_node.sh) - node that hosts the data and satisfies queries
  * Env Params: `NODE_TYPE=operator`
* [Publisher Node](examples/Docker%20Calls/publisher_node.sh) - node that receives data from a data source (i.e. devices, applications) and distributes the data to Operators 
  * Env Params: `NODE_TYPE=publisher`
* [Query Node](examples/Docker%20Calls/query_node.sh) - node that orchestrates a query process 
  * Env Params: `NODE_TYPE=query`
* [Single Node](examples/Docker%20Calls/single_node.sh) - node that consists of both master process and operator processes in a single AnyLog instance 
  * Env Params: `NODE_TYPE=single-node`
* [Single Node Publisher](examples/Docker%20Calls/single_node_publisher.sh) - node that consists of both master process and publisher process in a single AnyLog instance 
  * Env Params: `NODE_TYPE=single-node-publisher`
* [Hidden Query Node](examples/Docker%20Calls/hidden_query.sh) - A node that's able to query against the network but isn't declared on the blockchain 
  * Env Params: `NODE_TYPE=hidden-query`

### Generic Docker Command 
parameters that are not required are set in [square brackets]
```bash
docker run --network host --name ${CONTAINER_NAME} \
    -e NODE_TYPE=${NODE_TYPE} \ # Node type 
    -e COMPANY_NAME=${COMPANY_NAME} \ # company name 
    -e NODE_NAME=${NODE_NAME} \ # node name
    [-e LOCATION=${LOCATION} \]  
    [-e EXTERNAL_IP=${EXTERNAL_IP} \] # External IP - optional 
    [-e LOCAL_IP=${LOCAL_IP} \] # Local IP - optional 
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
    -v al-{CONTAINER_NAME}-anylog:/app/AnyLog-Network/anylog:rw \
    -v al-{CONTAINER_NAME-blockchain:/app/AnyLog-Network/blockchain:rw \
    -v al-{CONTAINER_NAME}-data:/app/AnyLog-Network/data:rw \
    -v al-{CONTAINER_NAME}-local-scripts:/app/AnyLog-Network/local_scripts:rw \
    -v al-{CONTAINER_NAME}-scripts:/app/AnyLog-Network/scripts:rw \
    -d -it --detach-keys="ctrl-d" --rm oshadmon/anylog:${BUILD}
```

## Preparing & Executing Personalized Scripts

In addition to the default deployment scripts, can enhance their AnyLog deployment by embedding personalized processes 
to be executed as part of the deployment process. 

1. Execute `docker create` for the new AnyLog instance you'd like to run
```bash
docker create --name ${CONTAINER_NAME} \
    -v al-{CONTAINER_NAME}-anylog:/app/AnyLog-Network/anylog:rw \
    -v al-{CONTAINER_NAME-blockchain:/app/AnyLog-Network/blockchain:rw \
    -v al-{CONTAINER_NAME}-data:/app/AnyLog-Network/data:rw \
    -v al-{CONTAINER_NAME}-local-scripts:/app/AnyLog-Network/local_scripts:rw \
    -v al-{CONTAINER_NAME}-scripts:/app/AnyLog-Network/scripts:rw \
    --rm oshadmon/anylog:${BUILD}
```

2. Get the path for `AnyLog-Network/local_scripts` 
```bash
docker inspect al-${CONTAINER_NAME}-local_scripts
[
    {
        "CreatedAt": "2022-01-26T21:46:52Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/al-${CONTAINER_NAME}-local-scripts/_data",
        "Name": "al-single-node-local-scripts",
        "Options": null,
        "Scope": "local"
    }
]
```

3. Open `local_script.al`, in which you can write AnyLog code to be deployed, and update with new content
```shell
sudo vim /var/lib/docker/volumes/al-${CONTAINER_NAME}-local-scripts/_data/local_script.al
```

4. Execute `docker run` ([as shown above](###Generic-Docker-Command)) - make sure volume names are consistent. 
 
Once the "default script" selected to run (based on `NODE_TYPE`) will complete, `local_script.al` gets executed.  