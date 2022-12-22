# Database Configuration
AnyLog utilizes 3 logical databases -- SQLite and/or PostgresSQL for SQL data and MongoDB for non-SQL (aka blobs) data. 
SQLite database doesn't require extra configurations as it resides within AnyLog. 

## PostgresSQL
On machines that will use PostgresSQL - make sure PostgresSQL is installed and accessible. Our  deployments package 
provides a docker deployment for PostgresSQL - alternatively a user can deploy / use their own PostgresSQL database. 
If you'd like to install PostgresSQL locally, rather than via Docker feel free to utilize the  following documentation: 
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

## MongoDB 
On machines that will use MongoDB (usually Operator nodes) - make sure MongoDB is installed locally. Our deployments 
package provides a docker deployment for MongoDB - alternatively a user can deploy / use their own MongoDB database. If 
you'd like to install MongoDB locally, rather than via Docker feel free to utilize the  following documentation:
* [Install MongoDB](https://www.linode.com/docs/guides/mongodb-community-shell-installation/)
* [Accepting MongoDB data on AnyLog](setting_up_mongodb.md)

1. access configuration file 
```shell
vim $HOME/deployments/docker-compose/mongodb/.env
```

2.change configurations 
```dotenv
PORT=27017
MONGO_USER=admin
MONGO_PASSWORD=passwd
```

3. Deploy postgres 
```shell
cd $HOME/deployments/docker-compose/mongodb/
docker-compose up -d
```

**Note**: The docker-compose file deploys MongoDB latest version 
