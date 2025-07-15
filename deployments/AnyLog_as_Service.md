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
  * [Deploying AnyLog](#deploy-using-deployment-scripts)
  * [Deploying AnyLog vis REST](#deploy-using-rest)

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


### Deploy using Deployment Scripts
1. Create a service file 
```editorconfig
# file path: /etc/systemd/system/anylog-service.service
[Unit]
Description=My Executable Service
After=network.target

[Service]
ExecStart=/home/user/anylog/anylog_v0.0.0_x86_64 process /home/user/deployment-scripts/node-deployment/main.al
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
```

### Deploying AnyLog via REST


3. Validate Service 
* Service status
```shell
sudo service anylog-service status
```

* cURL commands
```shell
# get status 
curl -X GET 127.0.0.1:32549

# get processes 
curl -X GET 127.0.0.1:32549 -H "command: get prcoesses" -H "User-Agent: AnyLog/1.23"
```

### Deploy for REST-based Deployment 
The following demonstrates deploying AnyLog as a service with only TCP and REST communications configured, allowing users 
to deploy their node 100% via REST.

1. Prepare a deployment script that setups networking configurations to the AnyLog instance.
```anylog 
# file path: $HOME/anylog/basic_deployment.al
on error ignore 
:prep-instance: 
# disable CLI 
set cli off

# disable authentication 
set authentication off

:set-params:
anylog_server_port=32548
anylog_rest_port=32549 
tcp_bind = false
rest_bind = false
tcp_threads=3
rest_threads=3
rest_timeout=30

:tcp-conn: 
on error goto tcp-conn-error
 <run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

:rest-conn: 
on error goto rest-conn-error
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>

:end-script: 
end script 

:tcp-conn-error: 
print "Failed to configure TCP connection" 
goto end-script 

:rest-conn-error: 
print "Failed to configure REST connection" 
goto end-script 
```

4. Using <a href="https://github.com/AnyLog-Co/AnyLog-API" target="_blank">AnyLog API</a> calls, create a program that 
initiates a set of services for the node. 
```shell
# set permissions for API script 
chmod +x /home/user/anylog/deployment_script.py 
```

5. Create a service file 
```editorconfig
# file path: /etc/systemd/system/anylog-service.service
[Unit]
Description=My Executable Service
After=network.target

[Service]
ExecStart=/home/user/anylog/anylog_v0.0.0_x86_64 process /home/user/anylog/basic_deployment.al
ExecStartPost=/usr/bin/python3 /home/user/anylog/deployment_script.py 127.0.0.1:32549 --configs /home/user/anylog/anylog_configs.envs
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

6. Start service 
```shell
sudo systemctl daemon-reload
sudo systemctl enable anylog-service.service # this step will allow it to start at reboot
sudo systemctl restart anylog-service.service
```

7. Validate Service 
* Service status
```shell
sudo service anylog-service status
```

* cURL commands
```shell
# get status 
curl -X GET 127.0.0.1:32549

# get processes 
curl -X GET 127.0.0.1:32549 -H "command: get prcoesses" -H "User-Agent: AnyLog/1.23"
```

