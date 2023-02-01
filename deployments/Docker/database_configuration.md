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

1. access configuration file 
```shell
vim $HOME/deployments/docker-compose/postgres/postgres.env
```

2.change configurations 
```dotenv
POSTGRES_USER=admin
POSTGRES_PASSWORD=passwd
```

3. Deploy postgres 
```shell
cd $HOME/deployments/docker-compose/postgres/
docker-compose up -d
```

**Note**: The docker-compose file deploys PostgresSQL version 14.0-alpine 

## SQLite

SQLite is installed by default with the AnyLog deployment.

## MongoDB 
On machines that will use MongoDB (usually Operator nodes) - make sure MongoDB is installed locally. Our deployments 
package provides a docker deployment for MongoDB - alternatively a user can deploy / use their own MongoDB database. 

The following documentation provides instruction to install MongoDB locally: 

* [Install MongoDB](https://www.linode.com/docs/guides/mongodb-community-shell-installation/)
* [Accepting MongoDB data on AnyLog](../Support/setting_up_mongodb.md)

1. access configuration file 
```shell
vim $HOME/deployments/docker-compose/mongodb/.env
```

2.change configurations 
```dotenv
MONGO_USER=admin
MONGO_PASSWORD=passwd
```

3. Deploy mongodb 
```shell
cd $HOME/deployments/docker-compose/mongodb/
docker-compose up -d
```

**Note**: The docker-compose file deploys MongoDB latest version 
