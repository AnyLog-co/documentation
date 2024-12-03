# AnyLog as a Service

AnyLog is a platform that allows to manage data across multiple (edge) innstances as if they're 
centralized (on the cloud). 

Right now, the "standard" deployment process consists of a docker container that runs either via 
[Docker](Quick%20Deployment.md) or [Kubernetes](deploying_node.md). However, under certain conditions, such as
lack of space or regulatory requirements, network constraints, etc, users may select to install AnyLog (or EdgeLake) 
directly as a service.

When deploying as a service the CLI interface is disabled. As such, communication with AnyLog is done via REST once the 
node is up and running. This document provides to ways by which AnyLog can run as a service - deploying AnyLog with 
the pre-existing deployment-scripts, and deploying AnyLog entirely via REST.

## Deploying AnyLog as a Service
Download AnyLog binary image - a full list of images can be found <a href="http://45.33.11.32/" target="blank">here</a>
```shell
mkdir $HOME/anylog/
cd $HOME/anylog
wget http://45.33.11.32/anylog_v0.0.0_x86_64
sudo chmod -R 750 $HOME/anylog/anylog_v0.0.0_x86_64
```

### Deploy using Deployment Scripts
The <a href="https://github.com/AnyLog-co/deployment-scripts" target="_blank">deployment scripts</a> provide the
ability to deploy AnyLog as a service with the same script we use for a docker-based deployment.

1. Prepare deployment scripts 
* Use pre-existing deployment-scripts 
```shell
cd $HOME/
git clone https://github.com/AnyLog-co/deployment-scripts
```

2. Prepare configuration file(s)
```shell
cd $HOME/
git clone https://github.com/AnyLog-co/docker-compose
cat $HOME/docker-compose/docker-makefile/* >> $HOME/anylog/anylog_configs.env 
```

3. Update `anylog_configs.env` config file 
```dotenv
# file path: $HOME/anylog/anylog_configs.env
# The following provides the key components of the configuration file for deploying via service 

#--- Directories ---
# AnyLog Root Path - if changed make sure to change volume path in docker-compose-template
ANYLOG_PATH=/home/user
# !local_scripts: ${ANYLOG_HOME}/deployment-scripts/scripts
LOCAL_SCRIPTS=/home/user/deployment-scripts/node-deployment
# !test_dir: ${ANYLOG_HOME}/deployment-scripts/tests
TEST_DIR=/home/user/deployment-scripts/tests

# --- General ---
# AnyLog License Key
LICENSE_KEY=""
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, 
# AnyLog starts TCP and REST connection protocols
NODE_TYPE=generic
# Name of the AnyLog instance
NODE_NAME=anylog-node
# Owner of the AnyLog instance
COMPANY_NAME=New Company

# Disable AnyLog's CLI interface
DISABLE_CLI=true
# Enable Remote-CLI
REMOTE_CLI=false

#--- Networking ---
# Port address used by AnyLog's TCP protocol to communicate with other nodes in the network
ANYLOG_SERVER_PORT=32548
# Port address used by AnyLog's REST protocol
ANYLOG_REST_PORT=32549
# Port value to be used as an MQTT broker, or some other third-party broker
ANYLOG_BROKER_PORT=""

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

#--- Blockchain ---
# TCP connection information for Master Node
LEDGER_CONN=127.0.0.1:32048
... 
```


4. Create a service file 
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
EnvironmentFile=/home/user/anylog/anylog_configs.env

[Install]
WantedBy=multi-user.target
```

5. Start service 
```shell
sudo systemctl daemon-reload
sudo systemctl enable anylog-service.service # this step will allow it to start at reboot
sudo systemctl restart anylog-service.service
```

6. Validate Service 
* Service status
```shell
sudo service anylog-service status
```

* cURL commands
```shell
# get status 
curl -X GET 127.0.0.1::32549

# get processes 
curl -X GET 127.0.0.1::32549 -H "command: get prcoesses" -H "User-Agent: AnyLog/1.23"
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
ExecStartPost=/usr/bin/python3 /home/user/anylog/deployment_script.py [OPTIONAL PARAMS]
Restart=always
User=root
Group=root
EnvironmentFile=/home/user/anylog/anylog_configs.env

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
curl -X GET 127.0.0.1::32549

# get processes 
curl -X GET 127.0.0.1::32549 -H "command: get prcoesses" -H "User-Agent: AnyLog/1.23"
```

