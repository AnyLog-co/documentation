# Database Configuration
AnyLog utilizes 3 logical databases -- SQLite and/or PostgresSQL for SQL data and MongoDB for non-SQL (aka blobs) data. 
SQLite database doesn't require extra configurations as it resides within AnyLog. 

## PostgresSQL
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

