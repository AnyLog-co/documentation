# Docker / Podman Installation 

AnyLog's preferred deployment method is through **Docker** or **Podman**. This guide covers everything from installing 
prerequisites to deploying and managing nodes, and is structured to support both seasoned engineers and first-time users.

* [Requirements](#requirements)
  * [Install Docker](#install-docker)
  * [Install Podman](#install-podman)
* [Deploying Agent](#deploying-anylog-agent)
  * [`make` commands](#make-commands)
  * [Enabling Remote-CLI](#enable-remote-cli)
  * [Single Machine Network](#single-machine-deployment)
* [Advanced Docker Support](#advanced-docker-support)
  * [Networking](#networking)
  * [Persistent Data with Docker](#persistent-data-with-docker)


## Requirements

* [Docker](#install-docker) or [Podman](#install-podman) - the two are interchangeable from AnyLog's perspective
* <a href="https://linux.die.net/man/1/make#:~:text=This%20man%20page%20is%20an%20extract%20of%20the,is%20made%20from%20the%20Texinfo%20source%20file%20make.texi." target="_blank">Make</a> (installed by default on most Unix systems)
* Clone our <a href="https://github.com/AnyLog-co/docker-compose" target="_blank">docker-compose repository</a>
```shell
git clone https://github.com/AnyLog-co/docker-compose
```

### Install Docker

Directions for install Docker can be found on their [official website](https://docs.docker.com/engine/install/), 

Installation instructions for Docker (Ubuntu example):
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

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin make

# set permissions 
USER=`whoami`
sudo groupadd docker
sudo usermod -aG docker ${USER}
newgrp docker
```

### Install Podman

Directions for install Podman can be found on their [official website](https://podman.io/docs/installation), 

Installation instructions for Podman (Ubuntu example):
```shell
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get -y install podman
```

--- 

## Deploying AnyLog Agent

1. Request a trial license via <a href="https://anylog.network/download" target="_blank">Download Page</a>

2. Clone <a href="https://github.com/AnyLog-co/docker-compose" target="_blank">docker-compose</a> repository

```shell
cd $HOME
git clone https://github.com/AnyLog-co/docker-compose 
```

3. Log into AnyLog docker repository 

```shell
cd $HOME/docker-compose 
make login ANYLOG_TYPE=[DOCKER_PASSWORD]
```

4. Update Configurations - Sample configurations file can be found in [Quick Start](quick_start.md#configuration)

|                                                  Node Type                                                  |                                                	Role                                                 | |                                                                                                                               | 
|:-----------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:| :---: |:-----------------------------------------------------------------------------------------------------------------------------:|  
|                                                  Operator                                                   |                          	A node that hosts the data and satisfies queries.                          | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/operator-configs/base_configs.env) |   [advanced](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/operator-configs/advance_configs.env)    | 
|                               Query	|                              A node that orchestrates a query process.                               | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/query-configs/base_configs.env) |   [advanced](https://github.com/AnyLog-co/docker-compose/blob/query-dev/docker-makefile/query-configs/advance_configs.env)    |
| Master	| A node that hosts the metadata on a ledger and serves the metadata to the peer nodes in the network. | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/master-configs/base_configs.env) |    [advanced](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/master-configs/advance_configs.env)     |
| Publisher	| A node that receives data from a data source (i.e. devices, applications) and distributes the data to Operators. | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/publisher-configs/base_configs.env) | [advanced](https://github.com/AnyLog-co/docker-compose/blob/query-dev/docker-makefile/publisher-configs/advance_configs.env)  |

5.  Deploy Agent
```shell
cd $HOME/docker-compose
make up ANYLOG_TYPE=[NODE_TYPE]

# example
make up ANYLOG_TYPE=master
```

### `make` Commands

The docker-compose repository uses the `make` functionality in order to remove the need for users to manually execute 
`docker` related commands. This allows for ease of use and consistency.

```shell
Usage: make [target] [VARIABLE=value]

Available targets:
  login                 log into the docker hub for AnyLog - use `ANYLOG_TYPE` as the placeholder for password
  build                 pull image from the docker hub repository
  dry-run               create docker-compose.yaml file based on the .env configuration file(s)
  up                    start AnyLog instance
  down                  Stop AnyLog instance
  clean-vols            Stop AnyLog instance and remove associated volumes
  clean                 Stop AnyLog instance and remove associated volumes & image
  attach                Attach to docker / podman container (use ctrl-d to detach)
  exec                  Attach to the shell executable for the container
  logs                  View container logs
  test-node             Test a node via REST interface
  test-network          Test the network via REST interface
  check-vars            Show all environment variable values

Common variables you can override:
  IS_MANUAL           Use manual deployment (true/false) - required to overwrite
  ANYLOG_TYPE         Type of node to deploy (e.g., master, operator)
  TAG                 Docker image tag to use
  NODE_NAME           Custom name for the container
  CLUSTER_NAME           Cluster Operator node is associted with
  ANYLOG_SERVER_PORT  Port for server communication
  ANYLOG_REST_PORT    Port for REST API
  ANYLOG_BROKER_PORT  Optional broker port
  LEDGER_CONN         Master node IP and port
  LICENSE_KEY         AnyLog License Key
  TEST_CONN           REST connection information for testing network connectivity
```

--- 

### Enable Remote-CLI

The **[_Remote-CLI_](northbound%20connectors/remote_cli.md)** is an open-source GUI tool developed by AnyLog for 
interacting with nodes using REST APIs. While tools like Postman can be used for standard SQL queries, Remote-CLI offers 
dedicated capabilities tailored to the AnyLog environment—particularly for handling blob (binary large object) data.

One of Remote-CLI’s key features is its ability to retrieve blob data via a shared local directory between itself and 
the target AnyLog node. Because of this, both services must run on the same machine and have access to the same file 
system path.

Remote-CLI can be deployed independently, or more commonly, alongside an AnyLog node—typically a Query node. The 
default `docker-compose` setup supports this bundled deployment. To enable Remote-CLI in a containerized environment, 
simply set `REMOTE_CLI=true` in the advanced configuration file for the node.

This setup ensures you get a visual interface for exploring the network, running SQL queries, and managing blob data 
with minimal setup effort.

### Single Machine Deployment
Users may want to deploy multiple agents of the same type (usually Operator) on the same machine.

In order to do this, each docker container needs a **unique** name and associated ports. When deploying agents of the 
same type on **different** machines, there's no 
need to deal with this section. 

1. Copy configurations into a directory 
```shell
cp -r $HOME/docker-compose/docker-compose/anylog-operator $HOME/docker-compose/docker-compose/anylog-operator2 
```

2. Update configurations for node - make sure each of the node has unique _PORT_ values and _NODE_NAME_. 

3. Deploy operator(s) 
```shell
cd $HOME/docker-compose
make up ANYLOG_TYPE=[NODE_TYPE]

# deploy operator 1
make up ANYLOG_TYPE=operator

# deploy operator 2
make up ANYLOG_TYPE=operator2
```

---

## Advanced Docker Support

### Networking

<a href="https://docs.docker.com/engine/network/" target="_blank">Docker offers several networking modes</a> that define 
how containers communicate with each other, with the host, and with the outside world. Proper network configuration is 
crucial when deploying distributed systems like AnyLog across machines or within orchestrated environments.

On Unix-based machines (such as Linux and Mac OSX),  `network_mode: host` allows the container to share the host's 
network stack. while other operating systems (like Windows) use Port forwarding as `network_mode: host` is not fully 
supported due to virtualization limitations. Instead, explicit port mapping between the host and container is used.

**Example for `network_mode: host`**: 
```yaml
services:
  anylog:
    network_mode: host
```

**Example for Port Mapping**:
```yaml
services:
  anylog:
    ports:
      - "2045:2045"
      - "2046:2046"
      - "3210:3210"
```

When using the `make` utility in the docker-compose repository, a shell script is utilized in order to build the docker 
file(s). One of the things this script does is check the base operating system of the machine, and configure the 
networking accordingly.

#### Overlay Networking
When deploying containers across multiple physical or virtual machines there's often a need for them to reside on a 
shared network with static IPs. One way to resolve this is by having the containers connect to an overlay network. 

One of the things AnyLog / EdgeLake provides within its configuration files is the ability to enable <a href="https://nebula.defined.net/docs/" target="_blank">Nebula</a> 
an overlay network developed by _Slack_ and _Defined_. 

Directions for deploying Nebula as part of the network can be found [here](third-party/nebula.md). 

### Persistent Data with Docker
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