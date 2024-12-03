# AnyLog as a Service

AnyLog is a platform that allows to manage data across multiple (edge) innstances as if they're 
centralized (on the cloud). 

Right now, the "standard" deployment process consists of a docker container that runs either via 
[Docker](Quick%20Deployment.md) or [Kubernetes](deploying_node.md). However, under certain conditions, such as
lack of space or regulatory requirements, network constraints, etc, users may select to install AnyLog (or EdgeLake) 
directly as a service.

## Deploying AnyLog as a Service 
**Step 1**: Download AnyLog binary image - a full list of images can be found <a href="http://45.33.11.32/" target="blank">here</a>
```shell
mkdir $HOME/anylog/
cd $HOME/anylog
wget http://45.33.11.32/anylog_v0.0.0_x86_64
sudo chmod root:root $HOME/anylog/anylog_v0.0.0_x86_64
sudo chmod -R 775 $HOME/anylog/anylog_v0.0.0_x86_64
```

**Step 2**: Prepare deployment scripts 
* Use pre-existing deployment-scripts 
```shell
cd $HOME/anylog
git clone https://github.com/AnyLog-co/deployment-scripts
```

When using deployment-scripts, there's  a need to provide .env configuration files, which are the same as 
those used for <a href="https://github.com/AnyLog-co/docker-compose/tree/main/docker-makefile/generic-configs" target="_blank">docker-compose</a>.
Note, you will need to disable the CLI. 
```dotenv
# subset of Dotenv file(s) 
#--- General ---
# AnyLog License Key
LICENSE_KEY=""
# Information regarding which AnyLog node configurations to enable. By default, even if everything is disabled, AnyLog starts TCP and REST connection protocols
NODE_TYPE=generic
# Name of the AnyLog instance
NODE_NAME=anylog-node
# Owner of the AnyLog instance
COMPANY_NAME=New Company

# Disable AnyLog's CLI interface
DISABLE_CLI=true

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

Once .env file(s) are created, make sure to set permissions level to 600 (owner read/write)
```shell
sudo chmod -R 600 $HOME/anylog/anylog_configs.env
```

* Manually create a basic deployment script, note `!external_ip` and `ip` are predefined by the system, and there's 
no need to declare them, unless using overlay network.
```anylog
# file path: $HOME/anylog/basic_deployment.al
set cli off
set authentication off
create work directories
tcp_bind = true
rest_bind = true
tcp_threads=3
rest_threads=3
rest_timeout=30

 <run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>

<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>
```

 

**Step 3**: Create a service file that executes AnyLog with the appropriate start-up script 
* Utilizing pre-existing deployment-scripts
```editorconfig
[Unit]
Description=My Executable Service
After=network.target

[Service]
ExecStart=$HOME/anylog/anylog_v0.0.0_x86_64 process $HOME/anylog/deployment-scripts/node-deployment/main.al
Restart=always
User=root
Group=root
EnvironmentFile=$HOME/anylog/anylog_configs.env

[Install]
WantedBy=multi-user.target
```

* Personalized deployment script -- When utilizing this format, we recommend minimizing the deployment scripts to **only**
set up networking configurations (TCP, REST and message broker), and complete all other steps via REST.
```editorconfig
# /etc/systemd/system/anylog-service.service
[Unit]
Description=AnyLog Node as a Service 
After=network.target

[Service]
ExecStart=$HOME/anylog/anylog_v0.0.0_x86_64 process $HOME/anylog/basic_deployment.al
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
```

**Step 4**: Upload & Starat Service
```shell
sudo systemctl daemon-reload
sudo systemctl restart anylog-service.service
sudo service anylog-service status
```