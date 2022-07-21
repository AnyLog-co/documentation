# Persistent Data & Executing AnyLog Scripts

## Volumes 
In Docker data is persistent through the use of [Docker Volumes](https://docs.docker.com/storage/volumes/). For AnyLog,
in specific, each node has 4 volumes that should be persistent. The volumes are: 
* `${CONTAINER_NAME}-anylog` contains access keys and special permissions. Using the default configurations, 
_authentication_ is not configured, and thus there's very limited (if any) content in there. 
* `${CONTAINER_NAME}-blockchain` contains a copy of the blockchain. This is **not** the actual blockchain, but rather 
a JSON file with a copy of the blockchain generated using `blockchain sync`
* `${CONTAINER_NAME}-data` contains a set of directories with the actual data stored on the node
```editorconfig
# The following provides a breakdown of the different directories under ${CONTAINER_NAME}-data 
/var/lib/docker/volumes/anylog-node-data/_data
├── archive <-- that that has been stored in operator  
│   └── 22 <-- Year of when data came in 
│       └── 06 <-- Month of when data came in 
│          ├── 05 <-- Day of when data came in
│          ├── 06
│          ├── 07
│          ├── 08
│          ├── 09
│          └── 10
├── bkup <-- Data that has been sent to an operator (on publisher node) 
├── dbms <-- directory containing SQLite (non-memory) data 
├── distr <-- That coming in from other operator nodes on the same cluster
├── error <-- Data files that filed to get processed 
├── pem 
├── prep <-- Data being prepared to be stored 
├── rest <-- Data coming in via REST  
├── test <-- Test case 
└── watch <-- Data ready to be stored or sent to other operators
```
* `${CONTAINER_NAME}-local-scripts` is a directory that contains the deployment scripts used when starting up a node. 
In addition, if an AnyLog user would like to change a deployment script and/or add additional scripts to be deployed 
process those scripts would be stored here.  

## Accessing Volume
1. Get list of all your volumes 
```shell
docker volume ls 
<< COMMENT
DRIVER    VOLUME NAME
local     anylog-node-anylog
local     anylog-node-blockchain
local     anylog-node-data
local     anylog-node-local-scripts
local     postgres_pgdata
<< 
```

2. Using the `inspect` command get the directory path of the volume
```shell
docker volume inspect anylog-node-local-scripts
<< COMMENT
[
    {
        "CreatedAt": "2022-07-04T18:11:50Z",
        "Driver": "local",
        "Labels": {},
        "Mountpoint": "/var/lib/docker/volumes/anylog-node-local-scripts/_data",
        "Name": "anylog-node-local-scripts",
        "Options": {},
        "Scope": "local"
    }
]
<< 
```

3. Once you know the _Mountpoint_, you can access the content within that volume. Note - Depending on the permissions, 
you may need to do a `sudo` command.
```shell
sudo tree /var/lib/docker/volumes/anylog-node-local-scripts/_data
<< COMMENT
/var/lib/docker/volumes/anylog-node-local-scripts/_data
├── README.md
├── create_dir_structure.sh
├── deployment_clean.sh
├── deployment_scripts
│   ├── configure_dbms_almgm.al
│   ├── configure_dbms_blockchain.al
│   ├── configure_dbms_operator.al
│   ├── configure_dbms_system_query.al
│   ├── data_partitioning.al
│   ├── declare_cluster.al
│   ├── declare_generic_policy.al
│   ├── declare_k8s_generic_policy.al
│   ├── declare_k8s_operator.al
│   ├── declare_operator.al
│   ├── deploy_operator.al
│   ├── deploy_publisher.al
│   ├── local_script.al
│   ├── mqtt.al
│   ├── network_configs.al
│   ├── pre_deployment.al
│   ├── run_scheduler.al
│   ├── set_params.al
│   └── validate_policy.al
├── sample_code
│   ├── edgex.al
│   ├── fledge.al
│   └── fledge_old.al
└── start_node.al

<<
```

## Executing Script
Personalized scripts are executed using the `process`, they can be done as part of the deployment process (after the 
first time), or manually. For this example we'll be executing `sample_code/edegex.al` which is the same as the EdgeX 
we've been doing throughout the documentation, but using (metadata) policies to declare the _MQTT client_, rather than
parameters and variables. 

1. Using the `inspect` command get the path for anylog-node-local-scripts
```shell
docker volume inspect anylog-node-local-scripts
```

2. Based on the _Mountpoint_ copy `sample_code/edgex.al` into `deployment_scripts/local_script.al`
    * Feel free to `vim` into either file to see their content, or develop your own (local) deployment script
```shell
sudo cp /var/lib/docker/volumes/anylog-node-local-scripts/_data/sample_code/edgex.al /var/lib/docker/volumes/anylog-node-local-scripts/_data/deployment_scripts/local_script.al 
```

3. attach to the node 
```shell
docker attach --detach-keys="ctrl-d" anylog-node 

# to detach press ctrl-d
```

4. Within AnyLog CLI execute the new local script. 
```shell
AL anylog-node > process !local_scripts/local_script.al  
```

5. Once the script is done you should be able to see the following changes:
    1. New policies added to the blockchain -- `blockchain get *`
    2. Data coming in to MQTT client -- `get msg client`
   

6. Detach from docker container -- `ctrl-d`


7. Update the .env file to have `DEPLOY_LOCAL_SCRIPT=true` instead of `DEPLOY_LOCAL_SCRIPT=false` so that the local 
script will be deployed each time the node starts up. 
