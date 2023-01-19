# Installing AnyLog using Docker

You can deploy AnyLog via _helm_ by using either our deployment script or manually. 

For login credentials contact us at: [info@anylog.co](mailto:info@anylog.co)

**Support Links**
* [Remote-CLI](../Support/Remote-CLI)
* [EdgeX](../Support/EdgeX.md)
* [Grafana](../Support/Grafana.md)
* [Trouble Shooting](../Support/cheatsheet.md)


**Requirements**
Unlike _Docker_, Kubernetes has [machine requirements](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin) 
in order to run. 
* \>= 2GB of RAM
* \>= 2 CPUs or more
* \>= 20GB of free disk space
* network connectivity between all machines in the cluster
* Unique hostname, MAC address, and product_uuid for every node
* Swap memory disabled

For testing purposes we use [minikube](https://minikube.sigs.k8s.io/docs/start/) and [helm](https://helm.sh/docs/) via 
Docker; but can also be used with [other deployment tools](https://kubernetes.io/docs/tasks/tools/). 

## Deployment
Please make sure to download [deployment scripts](https://github.com/AnyLog-co/deployments) and have AnyLog's docker 
login credentials in order to deploy the network.

### Deploying Database 
The AnyLog [deployment scripts](https://github.com/AnyLog-co/deployments) consists of Docker packages to install database 
services; however, they are not part of the automated deployment process at this time. Please note, alternatively users 
can manually install the database locally on their machines rather than as docker packages. 


#### Postgres 
PostgresSQL is used for storing time-series (non-blobs), usually provided in JSON format. If PostgresSQL is _not_ 
installed, AnyLog will automatically retry connecting to a SQLite logical database instead. 

Directions for installing PostgresSQL on your machine can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart)

1. Update [configurations](https://github.com/AnyLog-co/deployments/blob/master/helm/sample-configurations/postgres.yaml)  
   * deployment parameter naming (_pod_, _configs_, _volumes_, etc.)
   * Postgres credentials 
```shell
vim $HOME/deployments/helm/sample-configurations/postgres.yaml
```

2. Deploy PostgresSQL
```shell
# deploy volumes 
helm install $HOME/deployments/helm/packages/postgres-volume-14.0-alpine.tgz \
  --name-template psql-volume \
  --values $HOME/deployments/helm/sample-configurations/postgres.yaml
 
# deploy postgres 
helm install $HOME/deployments/helm/packages/postgres-14.0-alpine.tgz \
  --name-template psql \
  --values $HOME/deployments/helm/sample-configurations/postgres.yaml
```

#### MongoDB 
MongoDB is used to store blobs such as _images_, _videos_ and _files_.

Directions for installing MongoDB on your machine can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04)

1. Update [configurations](https://github.com/AnyLog-co/deployments/blob/master/helm/sample-configurations/mongodb.yaml)
   * deployment parameter naming (_pod_, _configs_, _volumes_, etc.)
   * MongoDB credentials 
```shell
vim $HOME/deployments/helm/sample-configurations/mongodb.yaml
```


2. Deploy MongoDB 
```shell
# deploy volumes 
helm install $HOME/deployments/helm/packages/mongodb-volume-4.tgz \
  --name-template mongo-volume \
  --values $HOME/deployments/helm/sample-configurations/mongodb.yaml
 
# deploy postgres 
helm install $HOME/deployments/helm/packages/mongodb-4.tgz \
  --name-template mongo \
  --values $HOME/deployments/helm/sample-configurations/mongodb.yaml
```

### Deploying Node
An AnyLog node can be deployed either manually, or through an easy-to-use questionnaire
