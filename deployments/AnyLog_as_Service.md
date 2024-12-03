# AnyLog as a Service

AnyLog is a platform that allows to manage data across multiple (edge) innstances as if they're 
centralized (on the cloud). 

Right now, the "standard" deployment process consists of a docker container that runs either via 
[Docker](Quick%20Deployment.md) or [Kubernetes](deploying_node.md). However, under certain conditions, such as
lack of space or regulatory requirements, network constraints, etc, users may select to install AnyLog (or EdgeLake) 
directly as a service.

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
[Unit]
Description=My Executable Service
After=network.target

[Service]
ExecStart=/home/user/anylog/anylog_v0.0.0_x86_64 process /home/user/deployment-scripts/node-deployment/main.al
Restart=always
User=root
Group=root
EnvironmentFile=/home/user//anylog/anylog_configs.env

[Install]
WantedBy=multi-user.target
```

5. Start service 
```shell
sudo systemctl daemon-reload
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