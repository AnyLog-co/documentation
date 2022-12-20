# Installing AnyLog using Docker

Deploying AnyLog via _docker-compose_ is one allows can be done using either our deployment script or manually. 
In addition, we also provide a single docker-compose that builds a [demo network](single_deployment_demo.md) 
(1 _Master_, 1 _Query_ and 2 _Operator_ nodes) on a single machine. 

For login credentials contact us at: [info@anylog.co](mailto:info@anylog.co)

**Support Links**
* Deploy [Remote-CLI](../Support/Remote-CLI)
* Deploy [EdgeX](../Support/EdgeX.md)
* Deploy [Grafana](../Support/Grafana.md)
* [Trouble Shooting]()
* [Sample Queries]()



### Requirements
* Docker
* docker-compose
* Python3 + [dotenv](https://pypi.org/project/python-dotenv/) - for utilizing [deployment scripts](../deplyoment_scripts) 

## Deployment 
### Scripted Process
0. Clone [deployments](https://github.com/AnyLog-co/deployments/) directory  & login into our Docker hub.  
```shell
cd $HOME ; git clone https://github.com/AnyLog-co/deployments
bash $HOME/deployments/installations/docker_credentials.sh ${USER_PASSWORD}
```
1. Manually deploy Postgres and/or MongoDB if planning to use in deployment
    * [Postgres Configuration](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/postgres/postgres.env)
    * [MongoDB Configurations](https://github.com/AnyLog-co/deployments/tree/master/docker-compose/mongodb/.env)
```shell
# deploy PostgreSQL 
cd $HOME/deployments/docker-compose/postgres/ ; docker-compose up -d 
# Deploy MongoDB 
cd $HOME/deployments/docker-compose/mongodb/ ; docker-compose up -d 
```
2. Initiate the deployment scripts - this will prepare the configurations (based on user input) and deploy an AnyLog 
instance.    
```shell
bash $HOME/deployments/deployment_scripts/deploy_node.sh 
```
3. (Optional) Deploy Remote-CLI -- A _query_ instance will also deploy Remote-CLI by itself; there's no need to redeploy it.
   * Access for Remote-CLI is [http://${LOCAL_IP_ADDRESS}:31800]() 
```shell
cd $HOME/deployments/docker-compose/remote-cli/ ; docker-compose up -d 
```
4. (Optional) Deploy Grafana
   * Access for Grafana is [http://${LOCAL_IP_ADDRESS}:3000]()
```shell
cd $HOME/deployments/docker-compose/grafana/ ; docker-compose up -d 
```

### Manual Process  
0. Clone [deployments](https://github.com/AnyLog-co/deployments/) directory & login into our Docker hub.
```shell
cd $HOME ; git clone https://github.com/AnyLog-co/deployments
bash $HOME/deployments/installations/docker_credentials.sh ${USER_PASSWORD}
```

1. Manually deploy Postgres and/or MongoDB if planning to use in deployment
    * [Postgres Configuration](postgres/postgres.env)
    * [MongoDB Configurations](mongodb/.env)
```shell
# deploy PostgreSQL 
cd $HOME/deployments/docker-compose/postgres/ ; docker-compose up -d 
# Deploy MongoDB 
cd $HOME/deployments/docker-compose/mongodb/ ; docker-compose up -d 
```
2. cd into the desired node 
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
6. (Optional) Deploy Remote-CLI -- A _query_ instance will also deploy Remote-CLI by itself; there's no need to redeploy it.
   * Access for Remote-CLI is [http://${LOCAL_IP_ADDRESS}:31800]() 
```shell
cd $HOME/deployments/docker-compose/remote-cli/ ; docker-compose up -d 
```
7. (Optional) Deploy Grafana
   * Access for Grafana is [http://${LOCAL_IP_ADDRESS}:3000]()
```shell
cd $HOME/deployments/docker-compose/grafana/ ; docker-compose up -d 
```


### Demo Cluster 
The [Demo Cluster Deployment](single_deployment_demo.md) is a standalone package that deploys the demo network on a single
AnyLog physical machine. This includes:
   * 1 Master 
   * 2 Operators (1 with SQLite and one with Postgres)
   * 1 Query Node 
   * Postgres 
   * Remote-CLI
   * Grafana

The single deployment will have data coming into 1 operator from _CloudMQTT_ broker and another via a local 
[EdgeX](../Support/EdgeX.md) instance; that needs to be deployed separately. 

0. Clone [deployments](https://github.com/AnyLog-co/deployments/) directory & login into our Docker hub.
```shell
cd $HOME ; git clone https://github.com/AnyLog-co/deployments
bash $HOME/deployments/installations/docker_credentials.sh ${USER_PASSWORD}
```

1. cd into [demo-cluster-deployment](demo-cluster-deployment)
```shell
cd $HOME/deployments/docker-compose/demo-cluster-deployment/
```
2. (Optional) Update configurations
```shell
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
3. Update image information (default is _predevelop_)
```shell
vim .env 
```
4. Deploy Node
   * Access for Remote-CLI is [http://${LOCAL_IP_ADDRESS}:31800]()
   * Access for Grafana is [http://${LOCAL_IP_ADDRESS}:3000]()
```shell
docker-compose up -d 
```
5. Deploy EdgeX using the directions in [lfedge-code](https://github.com/AnyLog-co/lfedge-code) to get data into the 
operator running with local broker 
