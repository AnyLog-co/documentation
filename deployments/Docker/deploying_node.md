# Deploying a Node

There are 4 main types of AnyLog instance (_Master_, _Operator_, _Query_ and _Publisher_), as-well-as an option to 
deploy a _Generic_ instance - which includes only TCP, REST and an optional Message Broker connection. 

An AnyLog deployment type is based on **system variables**, which users can assign values to different keys. These keys  
are referenced in the node configuration process to apply a configuration option or a configuration value.

## Basic Deployment
Our basic deployment is a _Generic_ node that automatically connects to TCP and REST, without any user-defined 
configurations. However, users can easily extend the deployment to inclue things like 
* persistent data (volumes) 
* Message Broker 
* Node name other [environment variables](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/anylog-rest/anylog_configs.env)

By default, the _Generic_ node connect to port 2148 for _TCP_ and 2149 for _REST_. 

```shell
docker run --network host -it --detach-keys=ctrl-d \
  --name anylog-node \
  [-e ANYLOG_SERVER_PORT=32148 \] 
  [-e ANYLOG_REST_PORT=32149 \] 
  [-e ANYLOG_BROKER_PORT=2150 \] 
  [--volume anylog-dir:/app/AnyLog-Network/anylog \]
  [--volume blockchain-dir:/app/AnyLog-Network/blockchain \]
  [--volume data-dir:/app/AnyLog-Network/data \]
  -rm anylogco/anylog-network:predevelop
```

## Configuration Based Deployment
AnyLog's [deployment scripts](https://github.com/AnyLog-co/deployments) provides users with a series of questions to assist
with deployment of an AnyLog instance of either _Docker_ or _Kubernetes_. For a _Docker_ instance the deployment script 
updates the correlating `.env` file of the node. 

**Disclaimer**: The deployment scripts do not [deploy physical database](database_configuration.md). Make sure your 
non-SQLite database(s) is deployed prior to starting your AnyLog instance.   

0. Requirements
    * [Docker and docker-compose](https://docs.docker.com/engine/install/)
    * Python3
      * [dotenv](https://pypi.org/project/python-dotenv/) - Python3 package utilized in the deployment scripts 

1. Download [deployment scripts](https://github.com/AnyLog-co/deployments)
```shell
cd $HOME
git clone https://github.com/AnyLog-co/deployments
cd $HOME/deployments/
```

2. Log into AnyLog's Dockerhub - [contact us](mailto:info@anylog.co) if you do not have login credentials
```shell
bash $HOME/deployments/installations/docker_credentials.sh ${YOUR_ANYLOG_DOCKER_CREDENTIALS}
```

3. Deploy AnyLog 
```shell
bash $HOME/deployments/deployment_scripts/deploy_node.sh
```

**Note**: When deploying an AnyLog _Query_ node, the deployment scripts will also deploy [Remote-CLI](../Support/Remote-CLI.md)


### Sample Questionare 
