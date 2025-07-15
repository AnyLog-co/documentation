# AnyLog Deployment using Kubernetes 

## Overview
This document demonstrate a deployment of an AnyLog node as a Kubernetes instance with Minikube and Helm.
The deployment makes AnyLog scripts persistent (using PersistentVolumeClaim). In a customer deployment, it is recommended 
to predefine the services for each Pod.

## Table of Content

* [Requirements](#requirements)
* [Deploying AnyLog](#deploy-anylog)
    * [Validate Connectivity](#using-node)
* [Network & Volume Configuration](#networking-and-volume-management)

## Requirements
* [Kubernetes Cluster manager](https://kubernetes.io/docs/tasks/tools/) - deploy Minikube with [Docker](https://minikube.sigs.k8s.io/docs/drivers/docker/) 
* [helm](https://helm.sh/)
* [kubectl](https://kubernetes.io/docs/reference/kubectl/)
* Hardware Requirements - based on [official documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin)

|   Requirements   | 
|:----------------:| 
| 2 GB or more RAM | 
| 2 or more CPUs  |
| Network connectivity between machines in cluster | 
| Unique hostname / MAC address for every physical node | 
| Disable swap on machine |  

## Deploy AnyLog
0. Validate connectivity between machines in the network 

1. Sign into AnyLog's docker repo - [Docker login credentials and license](https://anylog.co/download)  
```shell
bash secret.sh [DOCKER_LOGIN]
```
2. Select preferred [configurations](configurations/) and update values in `node_configs`

**Note**: In the configurations below, the value of `LEDGER_CONN` needs to be the  TCP connection information that can 
reach the master node.
```yaml
...
  directories:
    # AnyLog Root Path
    ANYLOG_PATH: /app
    # !local_scripts: ${ANYLOG_HOME}/deployment-scripts/scripts
    LOCAL_SCRIPTS: /app/deployment-scripts/scripts
    # !test_dir: ${ANYLOG_HOME}/deployment-scripts/tests
    TEST_DIR: /app/deployment-scripts/tests

  general:
    # AnyLog License Key
    LICENSE_KEY: ''
    # Disable AnyLog's CLI interface
    DISABLE_CLI: false

    # Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols
    NODE_TYPE: generic
    # Name of the AnyLog instance
    NODE_NAME: anylog-node
    # Owner of the Anylog instance
    COMPANY_NAME: New Company

  geolocation:
    # Coordinates of the machine - used by Grafana to map the network
    LOCATION: ""
    # Country where machine is located
    COUNTRY: ""
    # State where machine is located
    STATE: ""
    # City where machine is located
    CITY: ""

  networking:
    # Internal IP address of the machine the container is running on - if not set, then a unique IP will be used each time
    OVERLAY_IP: ""
    # Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
    ANYLOG_SERVER_PORT: 32548
    # Port address used by AnyLog's REST protocol
    ANYLOG_REST_PORT: 32549
#    # Port value to be used as an MQTT broker, or some other third-party broker
#    ANYLOG_BROKER_PORT: ""
    # A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
    TCP_BIND: false
    # A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
    REST_BIND: false
#    # A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs)
#    BROKER_BIND: false

    # Advanced configs for networking
    # Declare Policy name
    CONFIG_NAME: ""
    # The number of concurrent threads supporting HTTP requests.
    TCP_THREADS: 6
    # Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns timeout error.
    REST_TIMEOUT: 30
    # The number of concurrent threads supporting HTTP requests.
    REST_THREADS: 6
    # The number of concurrent threads supporting broker requests.
    BROKER_THREADS: 6

  database:
    # Physical database type (sqlite or psql)
    DB_TYPE: sqlite
    # Username for SQL database connection
    DB_USER: ""
    # Password correlated to database user
    DB_PASSWD: ""
    # Database IP address
    DB_IP: 127.0.0.1
    # Database port number
    DB_PORT: 5432
    # Whether to set autocommit data
    AUTOCOMMIT: false
    # Whether to enable NoSQL logical database
    ENABLE_NOSQL: false

    # Advanced configs for database
    # Whether to start system_query logical database
    SYSTEM_QUERY: false
    # Run system_query using in-memory SQLite. If set to false, will use pre-set database type
    MEMORY: false
    # Physical database type
    NOSQL_TYPE: mongo
    # Username for SQL database connection
    NOSQL_USER: ""
    # Password correlated to database user
    NOSQL_PASSWD: ""
    # Database IP address
    NOSQL_IP: 127.0.0.1
    # Database port number
    NOSQL_PORT: 27017
    # Store blobs in database
    BLOBS_DBMS: false
    # Whether (re)store a blob if already exists
    BLOBS_REUSE: true

  blockchain:
    # TCP connection information for Master Node
    LEDGER_CONN: 127.0.0.1:32048

    # Advanced configs for blockchain
    # How often to sync from blockchain
    SYNC_TIME: 30 second
    # Source of where the data is coming from
    BLOCKCHAIN_SOURCE: master
    # Where will the copy of the blockchain be stored
    BLOCKCHAIN_DESTINATION: file

  operator:
    # Operator ID
    MEMBER: ""
    # How many days back to sync between nodes
    START_DATE: 30
    # Which tables to partition - In the code, the default value is all tables associated with logical database
    TABLE_NAME: ""
    # Which timestamp column to partition by
    PARTITION_COLUMN: insert_timestamp
    # Time period to partition by
    PARTITION_INTERVAL: 1 day
    # How many partitions to keep
    PARTITION_KEEP: 3
    # How often to check if an old partition should be removed
    PARTITION_SYNC: 1 day

  mqtt:
    # Whether to enable the default MQTT process
    ENABLE_MQTT: false

    # IP address of MQTT broker
    MQTT_BROKER: 139.144.46.246
    # Port associated with MQTT broker
    MQTT_PORT: 1883
    # User associated with MQTT broker
    MQTT_USER: anyloguser
    # Password associated with MQTT user
    MQTT_PASSWD: mqtt4AnyLog!
    # Whether to enable MQTT logging process
    MQTT_LOG: false

    # Topic to get data for
    MSG_TOPIC: nylog-demo
    # Logical database name
    MSG_DBMS: new_company
    # Table where to store data
    MSG_TABLE: bring [table]
    # Timestamp column name
    MSG_TIMESTAMP_COLUMN: now
    # Value column name
    MSG_VALUE_COLUMN: bring [value]
    # Column value type
    MSG_VALUE_COLUMN_TYPE: float

  advanced:
    # Whether to automatically run a local (or personalized) script at the end of the process
    DEPLOY_LOCAL_SCRIPT: false
    # Deploy a process that accepts syslog - requires Message broker running
    DEPLOY_SYSLOG: false
    # Whether to monitor the node or not
    MONITOR_NODES: false
    # Which node type to send monitoring information to
    MONITOR_NODE: query
    # Compress JSON and SQL file(s) backup
    COMPRESS_FILE: true
    # Number of parallel queries
    QUERY_POOL: 6
    # When data comes in write to database immediately, as opposed to waiting for a full buffer
    WRITE_IMMEDIATE: false
    # If buffer is not full, how long to wait until pushing data through
    THRESHOLD_TIME: 60 seconds
    # Buffer size to reach, at which point data is pushed through
    THRESHOLD_VOLUME: 10KB
```

3. Deploy AnyLog using [deploy_node.sh](deploy_node.sh)
* package AnyLog instance 
```shell
bash deploy_node.sh package
```

* Start AnyLog based on configuration file - this will also start the volumes and enable port-forwarding against the node  
```shell
bash deploy_node. start configurations/${CONFIG_FILE} ${INTERNAL_IP_ADDRESS}

# Sample Call 
bash deploy_node. start configurations/anylog_master.yaml 192.168.0.121
```

* Stop AnyLog instance and corresponding port-forwarding, it will not remove volumes 
```shell
bash deploy_node. stop configurations/${CONFIG_FILE} 

# Sample Call 
bash deploy_node. stop configurations/anylog_master.yaml
```

### Using Node
* Attach to AnyLog CLI   
```shell
# to detach ctrl-p-q
kubectl attach -it pod/anylog-master-deployment-7b4ff75fb7-mnsxf 
```

* Attach to the shell interface of the node  
```shell
# to detach ctrl-p-q
kubectl exec -it pod/anylog-master-deployment-7b4ff75fb7-mnsxf -- /bin/bash  
```

## Networking and Volume management

### Networking 

AnyLog uses [dynamic ClusterIP](https://kubernetes.io/docs/concepts/services-networking/cluster-ip-allocation/) as it's preferred setup. This means a unique IP address is automatically assigned 
to the services as they are created and ensures load balancing across the pods in the service.

#### Configuring the network services on the AnyLog node

Since dynamic ClusterIP generates a new IP whenever a pod is deployed, this causes a issue with AnyLog's metadata 
(hosted in a blockchain or a master node) as each new IP will generate a new policy.  
To resolve this issue, and avoid policy updates, specify the host's internal IP as the `OVERLAY_IP` value. 

The following chart summarizes the setup:

|   Connection Type    | External IP | Internal IP |    Config Command    | 
|:--------------------:| :---: | :---: |:--------------------:| 
|         TCP          | External IP | Overlay IP |   `run tcp server`   | 
|         REST         | External IP | Overlay IP |   `run REST server`  |
| Message Broker (TCP) | External IP | Overlay IP | `run message broker` |

Additional information on the network configuration are in the [networking section](https://github.com/AnyLog-co/documentation/blob/master/network%20configuration.md).

#### Enable P2P messaging between the AnyLog Nodes 

The second part is in AnyLog's networking configuration is the need for nodes to communicate between one another; to 
accomplish this recommend using [port-forwarding](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_port-forward/).

The process fpr port-forwarding is configured to run automatically as part of [deploy_node.sh](deploy_node.sh). 

**Note**: When using Kubernetes, makes sure ports are open and accessible across your network.   

### Volume

The base deployment has the same general volumes as a docker deployment, and uses [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) - _data_, 
_blockchain_, _anylog_ and _local-scripts (deployments)_.

While _data_, _blockchain_ and _anylog_ are autogenerated and populated, _local-scripts_ gets downloaded as part of the 
container image. Therefore, we utilize an `if/else` process to make this data persistent. 

Note: we copy the scripts to a persistent volume that is created after the initialization of the Pod.

```shell
if [[ -d $ANYLOG_PATH/deployment-scripts ]] && [[ -z $(ls -A $ANYLOG_PATH/deployment-scripts) ]]; then # if directory exists but empty
  git clone -b os-dev https://github.com/AnyLog-co/deployment-scripts deployment-scripts-tmp
  mv deployment-scripts-tmp/* deployment-scripts
  rm -rf deployment-scripts-tmp
elif [[ ! -d $ANYLOG_PATH/deployment-scripts ]] ; then  # if directory DNE
  git clone -b os-dev https://github.com/AnyLog-co/deployment-scripts
fi
```

Once a node is up and running, users can change content in _local-scripts_ using `kubectl exec ${POD_NAME} -- /bin/bash`.

Volumes are deployed automatically as part of [deploy_node.sh](deploy_node.sh), and remain persistent as long as PersistentVolumeClaims
are not removed. 




