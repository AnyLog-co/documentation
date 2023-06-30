 # Database Configuration
Physical databases are a pluggable component. The configuration assigns a logical database to a physical database.
The command [connect dbms](../sql%20setup.md#connecting-to-a-local-database) associates a logical database with a 
physical database.  

The association of logical and physical databases are the users choice, and the same logical database can be associated 
with different physical databases (on different nodes).

The following table lists the supported databases and their common usage:

| Database Name   | Target Data    | Comments |
| --------------- | ------------- | ------------- |
| SQLite          | Structured or semi-structured (i.e. sensor data, PLC data, telemetry data) | For small nodes or data in RAM |
| PostgresSQL     | Structured or semi-structured (i.e. sensor data, PLC data, telemetry data  |   |
| MongoDB         | Unstructured data (i.e. images and video) |   |

Other physical databases can be added if an AnyLog connector to the physical database is developed.

## SQLite

SQLite is installed by default with the AnyLog deployment.


## PostgresSQL
On machines that will use PostgresSQL - make sure PostgresSQL is installed and accessible. Our  deployments package 
provides a docker deployment for PostgresSQL - alternatively a user can deploy / use their own PostgresSQL database. 

The following documentation provides instruction to install PostgresSQL locally: 
* [Install PostgresSQL as a Service](https://www.postgresql.org/download/)
* [Configure PostgresSQL for Remote Access](https://www.linode.com/docs/guides/configure-postgresql/)

1. (Optional) Update configurations
   * username / password 
   * PostgresSQL version - by default set to 14.0-alpine
   * service and volume naming
   * etc. 

**Docker Deployment**:
```shell
# contains only username and password
vim $HOME/deployments/docker-compose/postgres/postgres.env

# contains all other information 
vim $HOME/deployments/docker-compose/postgres/docker-compose.yaml
```

**Kubernetes Deployment**:
```shell
# contains all relevant information for deployment
vim $HOME/deployments/helm/sample-configurations/postgres.yaml
```

2. Deploy PostgresSQL physical database 

**Docker Deployment**
```shell
cd $HOME/deployments/docker-compose/postgres/
docker-compose up -d
```

**Kubernetes Deployment**
```shell
helm install $HOME/deployments/helm/packages/postgres-volume-14.0-alpine.tgz \
  --name-template psql-vol \
  --values $HOME/deployments/helm/sample-configurations/postgres.yaml

helm install $HOME/deployments/helm/packages/postgres-14.0-alpine.tgz \
  --name-template psql \
  --values $HOME/deployments/helm/sample-configurations/postgres.yaml 
```


## MongoDB 
On machines that will use MongoDB (usually Operator nodes) - make sure MongoDB is installed locally. Our deployments 
package provides a docker deployment for MongoDB - alternatively a user can deploy / use their own MongoDB database. 

The Docker deployment for MongoDB come with [mongo-express](https://github.com/mongo-express/mongo-express) 
Web-based MongoDB admin tool. The username/password or mongo-express is the same as the MongoDB credentials.

The following documentation provides instruction to install MongoDB locally: 

* [Install MongoDB](https://www.linode.com/docs/guides/mongodb-community-shell-installation/)
* [Accepting MongoDB data on AnyLog](Support/setting_up_mongodb.md)

1. (Optional) Update configurations
   * username / password 
   * MongoDB version - by default set to _latest_
   * service and volume naming
   * etc. 

**Docker Deployment**:
```shell
# contains only username and password
vim $HOME/deployments/docker-compose/mongodb/.env

# contains all other information 
vim $HOME/deployments/docker-compose/mongodb/docker-compose.yaml
```

**Kubernetes Deployment**:
```shell
# contains all relevant information for deployment
vim $HOME/deployments/helm/sample-configurations/mongodb.yaml
```

2. Deploy MongoDB physical database 

**Docker Deployment**
```shell
cd $HOME/deployments/docker-compose/mongodb/
docker-compose up -d
```

**Kubernetes Deployment**
```shell
helm install $HOME/deployments/helm/packages/mongodb-volume-4.tgz \
  --name-template mongo-vol \
  --values $HOME/deployments/helm/sample-configurations/mongodb.yaml

helm install $HOME/deployments/helm/packages/mongodb-4.tgz \
  --name-template mongo \
  --values $HOME/deployments/helm/sample-configurations/mongodb.yaml 
```
