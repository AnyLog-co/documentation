# Installing AnyLog using Docker

You can deploy AnyLog via _docker-compose_ by using either our deployment script or manually. Additionally, we provide a 
single docker-compose that builds a [demo network](single_deployment_demo_network.md) [1 _Master_, 1 _Query_ and 
2 _Operator_ nodes] on a single machine.  

For login credentials contact us at: [info@anylog.co](mailto:info@anylog.co)

**Support Links**
* [Remote-CLI](../Support/Remote-CLI)
* [EdgeX](../Support/EdgeX.md)
* [Grafana](../Support/Grafana.md)
* [Trouble Shooting](../Support/cheatsheet.md)


**Requirements**
* Docker
* docker-compose
* Python3 + [dotenv](https://pypi.org/project/python-dotenv/) - for utilizing [deployment scripts](../deplyoment_scripts) 

Directions for downloading Docker / docker-compose can be found here: [Docker Engine Installation](https://docs.docker.com/engine/install/)

## Deployment
Please make sure to download [deployment scripts](https://github.com/AnyLog-co/deployments) and have AnyLog's docker 
login credentials in order to deploy the network.

```shell
cd $HOME 
git clone https://github.com/AnyLog-co/deployments

bash $HOME/deployments/installations/docker_credentials.sh ${ANYLOG_PASSWORD}
```

### Deploying Database 
The AnyLog [deployment scripts](https://github.com/AnyLog-co/deployments) consists of Docker packages to install database 
services; however, they are not part of the automated deployment process at this time. Please note, alternatively users 
can manually install the database locally on their machines rather than as docker packages. 


#### Postgres 
PostgresSQL is used for storing time-series (non-blobs), usually provided in JSON format. If PostgresSQL is _not_ 
installed, AnyLog will automatically retry connecting to a SQLite logical database instead. 

Directions for installing PostgresSQL on your machine can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart)

1. Update [configurations](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/postgres/postgres.env)  
   * POSTGRES_USER
   * POSTGRES_PASSWORD 
```shell
cd $HOME/deployments/docker-compose/postgres/
vim postgres.env
```

2. Deploy PostgresSQL
```shell
cd $HOME/deployments/docker-compose/postgres/
docker-compose up -d
```

#### MongoDB 
MongoDB is used to store blobs such as _images_, _videos_ and _files_.

Directions for installing MongoDB on your machine can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04)

1. Update [configurations](https://github.com/AnyLog-co/deployments/blob/master/docker-compose/mongodb/.env)
   * MONGO_USER
   * MONGO_PASSWORD 
```shell
cd $HOME/deployments/docker-compose/mongodb/  
vim .env
```

2. Deploy MongoDB 
```shell
cd $HOME/deployments/docker-compose/mongodb/
docker-compose up -d
```

### Deploying Node
An AnyLog node can be deployed either manually, or through an easy-to-use questionnaire

#### Questionnaire Based Deployment 
A questionnaire based deployment will ask a series of question (including whether you'd like to deploy on _Docker_ or 
_Kubernetes_ and will attempt to deploy the node).

```shell
bash $HOME/deployments/deployment_scripts/deploy_node.sh 
```

**Note** - when deploying a Query node (via Docker) with the deployment script, the process will also include Remote-CLI. 
This is because when querying for blobs (ie MongoDB), the data must be accessible by **both** the Query Node and 
Remote-CLI.


#### Manual Deployment
1. cd into the desired node 
```shell
# master node
cd $HOME/deployments/docker-compose/anylog-master/

# operator node 
cd $HOME/deployments/docker-compose/anylog-operator/

# publisher node 
cd $HOME/deployments/docker-compose/anylog-publisher/

# query with Remote-CLI node 
cd $HOME/deployments/docker-compose/query-remote-cli/
```
3. Update deployment configurations
```shell
vim anylog_configs.env
```
4. Update image information (default is _predevelop_)
```shell
vim .env 
```
**Note** - If you'd like to deploy multiple operator nodes on a single machine, then the service name 
(`anylog-operator-node`) and volume names in [docker-compose.yaml](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/anylog-operator/docker-compose.yml)
needs to be updated. 

5. Deploy Node 
```shell
docker-compose up -d 
```

#### Demo Network 
A standalone package that deploys a small network on a single machine. This includes:
   * 1 Master 
   * 2 Operators (1 with SQLite and one with Postgres)
   * 1 Query Node 
   * Postgres 
   * Remote-CLI
   * Grafana  

The single deployment will have data coming into 1 operator from _CloudMQTT_ broker and another via a local [EdgeX](../Support/EdgeX.md) 
instance with data coming from a cloud-based MQTT broker. There is no need to deploy PostgresSQL on its own when running 
a standalone demo network.

1. (Optional) Update configurations
```shell
cd $HOME/deployments/docker-compose/anylog-demo-network/

# Postgres 
vim envs/postgres.env 

# Master 
vim envs/anylog_master.env 

# Operator 1 
vim envs/anylog_operator1.env 

# Operator 2  
vim envs/anylog_operator2.env

# Query 
vim envs/anylog_query.env
```
2. (Optional) Update AnyLog build version
```shell
vim .env
```
3. Deploy Demo Network
```shell
docker-compose up -d 
```
