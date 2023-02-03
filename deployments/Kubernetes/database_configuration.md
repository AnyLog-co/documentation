 # Database Configuration
Physical databases are a pluggable component. A logical database is associated with a physical database when nodes start.  
The command [connect dbms](../../sql%20setup.md#connecting-to-a-local-database) associates a logical database with a 
physical database.  

The association of logical and physical databases are the users choice, and the same logical database can be associated 
with different physical databases (on different nodes).

The following table lists the supported databases and their common usage:

| Database Name   | Target Data    | Comments |
| --------------- | ------------- | ------------- |
| PostgresSQL     | Structured or semi-structured (i.e. sensor data, PLC data, telemetry data  |   |
| SQLite          | Structured or semi-structured (i.e. sensor data, PLC data, telemetry data) | For small nodes or data in RAM |
| MongoDB         | Unstructured data (i.e. images and video) |   |

Other physical databases can be added if an AnyLog connector to the physical database is developed.

## PostgresSQL
On machines that will use PostgresSQL - make sure PostgresSQL is installed and accessible. Our  deployments package 
provides a docker deployment for PostgresSQL - alternatively a user can deploy / use their own PostgresSQL database. 

The following documentation provides instruction to install PostgresSQL locally: 
* [Install PostgreSQL as a Service](https://www.postgresql.org/download/)
* [Configure PostgreSQL for Remote Access](https://www.linode.com/docs/guides/configure-postgresql/)

1. (optional) Update values in the configuration file 
```shell
vim $HOME/deployments/helm/sample-configurations/postgres.yaml
```

2. Deploy postgres 
```shell
helm install $HOME/deployments/helm/packages/postgres-volume-14.0-alpine.tgz \
  --name-template psql-vol \
  --values sample-configurations/postgres.yaml

helm install $HOME/deployments/helm/packages/postgres-14.0-alpine.tgz \
  --name-template psql \
  --values sample-configurations/postgres.yaml 
```

**Note**: The Kubernetes package deploys PostgresSQL version 14.0-alpine and is based on a [medium article](https://medium.com/@suyashmohan/setting-up-postgresql-database-on-kubernetes-24a2a192e962) 

## SQLite

SQLite is installed by default with the AnyLog deployment.

## MongoDB 
On machines that will use MongoDB (usually Operator nodes) - make sure MongoDB is installed locally. Our deployments 
package provides a docker deployment for MongoDB - alternatively a user can deploy / use their own MongoDB database. 

The following documentation provides instruction to install MongoDB locally: 

* [Install MongoDB](https://www.linode.com/docs/guides/mongodb-community-shell-installation/)
* [Accepting MongoDB data on AnyLog](../Support/setting_up_mongodb.md)

1. (optional) access configuration file 
```shell
vim $HOME/deployments/helm/sample-configurations/mongodb.yaml
```

2. Deploy mongodb 
```shell
helm install $HOME/deployments/helm/packages/mongodb-volume-4.tgz \
  --name-template mongo-vol \
  --values $HOME/deployments/helm/sample-configurations/mongodb.yaml

helm install $HOME/deployments/helm/packages/mongodb-4.tgz \
  --name-template mongo \
  --values $HOME/deployments/helm/sample-configurations/mongodb.yaml
```

**Note**: The Kubernetes package deploys MongoDB latest version and is based on a [DevOpsCube article](https://devopscube.com/deploy-mongodb-kubernetes/)


## AnyLog Configuration 
As explained in the [networking](networking.md) section, each time a Kubernetes pod is spun up, it generates a new
virtual IP. 

When connecting to non-SQLite database via AnyLog, the `connect dbms` configurations cannot use
an actual IP address for connecting between AnyLog and a physical database. Instead, they should connect via the relative
[Kubernetes Service Name](https://kubernetes.io/docs/concepts/services-networking/service/). 

By default, the PostgreSQL service name is `postgres-svs` and the MongoDB service name is `mongo-svs`.

When deploying an AnyLog node with the [deployment scripts](https://github.com/AnyLog-co/deployments) that is Kubernetes
based, the default Database Address is already pre-configured to use the service name, as opposed to the usual "default"
IP address `127.0.0.1`. 