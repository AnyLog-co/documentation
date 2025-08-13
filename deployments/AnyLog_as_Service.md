# AnyLog as a Service

AnyLog is a platform that allows to manage data across multiple (edge) instances as if they're centralized (on the 
cloud). Essentially creating a data lake on the edge.  

Right now, the "standard" deployment process consists of a docker container that runs either via 
[Docker](docker_podman.md) or [Kubernetes](kubernetes.md). However, under certain conditions, such as
lack of space or regulatory requirements, network constraints, etc, users may select to install AnyLog (or EdgeLake) 
directly as a service.


* [Requirements](#requirements)
* [Deploying AnyLog](#deploying-anylog-as-a-service)
  * [Setting Up the Machine](#prep-environment)
    * [Networking](#default-ports)
  * [Deploying AnyLog](#deploy-using-deployment-scripts)
  * [Deploying AnyLog vis REST](#deploy-using-rest)
* [Validate Agent is Running](#validate-agent)

--- 

## Requirements

* Software Requirements 
    * Relational database - either _SQLite_ (built-in) or _PostgresSQL_
    * BLobs database (if images / data files) - either File-store (built-in) or MongoDB
    * Python3.9 or higher
      * Python pip packages can be found in [Quick Start](../quick_start.md#requirements)
* Hardware Requirements 

|                                               |                                                  Requirements                                                   | 
|:---------------------------------------------:|:---------------------------------------------------------------------------------------------------------------:| 
| Operating System |                            Ideally Linux-based, but also support Mac OSX and Windows                            |
|                      RAM                      |                                                  2 GB or more                                                   | 
|                      CPU                      |                                    2 or more - both arm64 and am64 supported                                    |
| Image Size |              AnyLog / EdgeLake is less than 150MB - everything else is either pip package or data               | 
|                  Networking                   | Network connectivity between machines in cluster<br/><br/>Unique hostname / MAC address for every physical node | 

--- 

## Deploying AnyLog as a Service

### Prep Environment

1. Request a trial license via <a href="https://anylog.network/download" target="_blank">Download Page</a>

2. Download AnyLog binary image - a full list of images can be found <a href="http://45.33.11.32/" target="blank">here</a>
```shell
mkdir $HOME/anylog/
cd $HOME/anylog
wget http://45.33.11.32/anylog_v0.0.0_x86_64
sudo chmod -R 750 $HOME/anylog/anylog_v0.0.0_x86_64
```

3. Clone our <a href="https://github.com/AnyLog-co/docker-compose" target="_blank">docker-compose repository</a> - 
this contains the needed environment variables for deploying AnyLog / EdgeLake  
```shell
mkdir $HOME/anylog/
git clone https://github.com/AnyLog-co/docker-compose
```

4. Clone our <a href="https://github.com/AnyLog-co/docker-compose" target="_blank">deployment-scripts repository</a> - 
these scripts  provide the ability to deploy AnyLog / EdgeLAke as a service with the same script we use for a 
docker-based deployment. 
```shell
mkdir $HOME/anylog/
git clone https://github.com/AnyLog-co/deployment-scripts
```

5. Update Configurations - Sample configurations file can be found in [Quick Start](quick_start.md#configuration)

|                                                  Node Type                                                  |                                                	Role                                                 | |                                                                                                                               | 
|:-----------------------------------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------:| :---: |:-----------------------------------------------------------------------------------------------------------------------------:|  
|                                                  Operator                                                   |                          	A node that hosts the data and satisfies queries.                          | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/operator-configs/base_configs.env) |   [advanced](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/operator-configs/advance_configs.env)    | 
|                               Query	|                              A node that orchestrates a query process.                               | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/query-configs/base_configs.env) |   [advanced](https://github.com/AnyLog-co/docker-compose/blob/query-dev/docker-makefile/query-configs/advance_configs.env)    |
| Master	| A node that hosts the metadata on a ledger and serves the metadata to the peer nodes in the network. | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/master-configs/base_configs.env) |    [advanced](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/master-configs/advance_configs.env)     |
| Publisher	| A node that receives data from a data source (i.e. devices, applications) and distributes the data to Operators. | [basic](https://github.com/AnyLog-co/docker-compose/blob/os-dev/docker-makefile/publisher-configs/base_configs.env) | [advanced](https://github.com/AnyLog-co/docker-compose/blob/query-dev/docker-makefile/publisher-configs/advance_configs.env)  |

> When deploying as a service the CLI interface is disabled. As such, communication with AnyLog is done via REST once the 
node is up and running. This document provides to ways by which AnyLog can run as a service - deploying AnyLog with 
the pre-existing deployment-scripts, and deploying AnyLog entirely via REST.
<br/>
To disable the CLI, simply update configurations to have `DISABLE_CLI=true`

#### Default Ports

When deploying AnyLog / EdgeLake one thing to be aware of is there 3 network configurations used to communicate between 
and with the network. Just like containers, each service of AnyLog  / EdgeLake agent should have unique ports when 
deploying multiple agents on the same machine. 

* **TCP Service** - Used for communicating with other AnyLog / EdgeLake agents in the network
* **REST Service** - Used for communicating with a specific AnyLog / EdgeLake agent via the REST-API. 
* **Message Broker** - Built-in topic-based consumer. Currently supporting _MQTT_ and _Kafka_ messaging.  

| | TCP Service | REST Service | Message Broker (optional) | 
| :---: | :---: | :---: |:-------------------------:| 
| Master | 32048 | 32049 |                           |
| Operator | 32148 | 32149 | 32150 | 
| Query | 32348 | 32349 | | 
| Publisher | 32248 | 32249 | 32250 |

### Deploy using Deployment Scripts
1. Create a service file 

```editorconfig
# file path: /etc/systemd/system/anylog-service.service
[Unit]
Description=My Executable Service
After=network.target
[Service]
ExecStart=/home/user/anylog/anylog_v0.0.0_x86_64 process /home/user/anylog/deployment-scripts/node-deployment/main.al
Restart=always
User=root
Group=root
# this path should be for updated based on  docker-compose/docker-makefiles/[node-type]/*.env
EnvironmentFile=/home/user/anylog/anylog_configs.env
[Install]
WantedBy=multi-user.target
```

2. Start service 
```shell
sudo systemctl daemon-reload
sudo systemctl enable anylog-service.service # this step will allow it to start at reboot
sudo systemctl restart anylog-service.service
sudo systemctl status anylog-service.service
```

### Deploying Empty Node

One of the Key services on AnyLog / EdgeLake is the [API interface](../third-party/REST_API.md), which allows for users
to interact with the AnyLog / EdgeLake via REST.

#### Prep Environment

1. Request a trial license via <a href="https://anylog.network/download" target="_blank">Download Page</a>

2. Download AnyLog binary image - a full list of images can be found <a href="http://45.33.11.32/" target="blank">here</a>
```shell
mkdir $HOME/anylog/
cd $HOME/anylog
wget http://45.33.11.32/anylog_v0.0.0_x86_64
sudo chmod -R 750 $HOME/anylog/anylog_v0.0.0_x86_64
```

3. Create an AnyLog script that connects to TCP, REST and (optionally) Message Broker
```anylog
# file name: $HOME/anylog/my_script.al
# ignore any error messages that arise from script
on error ignore 
# enable echo queue  
set echo queue on 
# disable interactive mode
set cli off
# set networking params 
set tcp_bind  = true 
tcp_threads = 6
set rest_bind = false 
rest_threads = 6
# REST internal timeout 
rest_timeout = 30 
set broker_bind = false 
broker_threads = 6
# TCP Service 
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!overlay_ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
# REST Service
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>s
# Message Broker service 
<run message broker where
    external_ip=!external_ip and external_port=!anylog_broker_port and
    internal_ip=!ip and internal_port=!anylog_broker_port and
    bind=!broker_bind and threads=!broker_threads>
```

#### Deploy Node 
1. Create a service file
```editorconfig
# file path: /etc/systemd/system/anylog-service.service
[Unit]
Description=My Executable Service
After=network.target
[Service]
ExecStart=/home/user/anylog/anylog_v0.0.0_x86_64 process $HOME/anylog/my_script.al
Restart=always
User=root
Group=root
[Install]
WantedBy=multi-user.target
```

2. Start service 
```shell
sudo systemctl daemon-reload
sudo systemctl enable anylog-service.service # this step will allow it to start at reboot
sudo systemctl restart anylog-service.service
sudo systemctl status anylog-service.services
```

---

## Validate Agent

When deploying AnyLog / EdgeLake as a service, there's no CLI to communicate with the network, hence the need for A 
REST-API. As such there' are 4 basic commands that can be used to validate whether a node is running, and whether it's 
able to communicate with the rest of the network.

* `get status` - this is a basic command that validate the user can communicate with the agent via REST 
```shell
curl -X GET [IP]:[REST_Port] \
  -H "command: get status" \
  -H "User-Agent: AnyLog/1.23" 
```

* `get processes` - check which services are enabled on the node
```shell
curl -X GET [IP]:[REST_Port] \
  -H "command: get processes" \
  -H "User-Agent: AnyLog/1.23"
```

* `test node` -  validate agent communication for TCP and REST
```shell
curl -X GET [IP]:[REST_Port] \
  -H "command: test node" \
  -H "User-Agent: AnyLog/1.23"
```

* `test network` -  validate communication with all other agents in the network
```shell
curl -X GET [IP]:[REST_Port] \
  -H "command: test network" \
  -H "User-Agent: AnyLog/1.23"
```