# PostgreSQL
On machines that will use PostgreSQL - make sure PostgreSQL is installed and accessible. Our deployments package 
provides a docker deployment for PostgreSQL - alternatively a user can deploy / use their own PostgreSQL database. If 
you'd like to install PostgreSQL locally, rather than via Docker feel free to utilize the following documentation: 
* [Install PostgreSQL as a Service](https://www.postgresql.org/download/)
* [Configure PostgreSQL for Remote Access](https://www.linode.com/docs/guides/configure-postgresql/)

1. In deployments/docker-compose/postgres/postgres.env update configuration
```dotenv
POSTGRES_USER=admin
POSTGRES_PASSWORD=passwd
```
2. Deploy PostgreSQL version 14.0-alpine
```shell
cd deployments/docker-compose/postgres 
docker-compose up -d 
```