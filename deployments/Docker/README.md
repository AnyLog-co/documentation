# Installing AnyLog using Docker

You can deploy AnyLog via _docker-compose_ by using either our deployment script or manually. Additionally, we provide a 
single docker-compose that builds a [demo network](single_deployment_demo_network.md) [1 _Master_, 1 _Query_ and 
2 _Operator_ nodes] on a single machine.  

For login credentials contact us at: [info@anylog.co](mailto:info@anylog.co)

**Support Links**
* [Remote-CLI](../Support/Remote-CLI.md)
* [EdgeX](../Support/EdgeX.md)
* [Grafana](../Support/Grafana.md)
* [Trouble Shooting](../Support/cheatsheet.md)


**Requirements**
* Docker
* docker-compose
* Python3 + [dotenv](https://pypi.org/project/python-dotenv/) - for utilizing [deployment scripts](https://github.com/AnyLog-co/deployments) 

Directions for downloading Docker / docker-compose can be found in the [Docker Engine Installation](https://docs.docker.com/engine/install/)

## Deployment Process 
1. Download [deployments](https://github.com/AnyLog-co/deployments) & log into AnyLog Docker Hub
```shell
cd $HOME

git clone https://github.com/AnyLog-co/deployments

cd $HOME/deployments/

bash $HOME/deployments/installations/docker_credentials.sh ${YOUR_ANYLOG_DOCKER_CREDENTIALS}
```

2. Deploy relevant database, this can be done as docker image(s) or as services on your machine. Directions can be found 
[here](database_configuration.md)


3. [Deploy AnyLog](deploying_node.md)


4. Deploy other services like [Remote-CLI](../Support/Remote-CLI.md) and [Grafana](../Support/Grafana.md)


If you are planning to deploy a [single deployment demo network](single_deployment_demo_network.md), there is no need to
complete step 2 through 4 prior to deploying your node. The single demo network will automatically deploy: 
* 1 master 
* 2 operator nodes (1 using PostgresSQL and another using SQLite)
* 1 Query Node 
* PostgresSQL (used by 1 of the operators)
* Remote CLI 
* Grafana 

