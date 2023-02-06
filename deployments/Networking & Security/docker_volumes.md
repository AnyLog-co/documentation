# Persistent Data

## Persistent Volumes in AnyLog Deployment 
In Docker data is persistent through the use of [Docker Volumes](https://docs.docker.com/storage/volumes/).     
In an AnyLog deployment, the following 4 volumes on each node needs to be persistent:

| Volume                        | Usage (storage of)                              | Comments                   |
| ----------------------------- | ---------------------------------  | ---------------------------------------------------- |
| `${CONTAINER_NAME}-anylog`    | The node keys                      | Required if node and user authentication is enabled  |
| `${CONTAINER_NAME}-blockchain` | A local copy of the metadata      | Multiple files representing versions   |
| `${CONTAINER_NAME}-local-scripts` | The deployment scripts       |   |
| `${CONTAINER_NAME}-data` | A root directory of different sub volumes  | See details below  |


```editorconfig
# The following provides a breakdown of the different directories under ${CONTAINER_NAME}-data 
/var/lib/docker/volumes/anylog-node-data/_data
├── archive <-- Archive/Backup of data hosted on the node  
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

```