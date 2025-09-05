# Upgrading AnyLog / EdgeLake

When deploying AnyLog or EdgeLake via container services like _Docker_, _Podman_ and _Kubernetes_ the deployment 
consists of two major parts: 
* The actual AnyLog or EdgeLake agent 
* <a href="https://github.com/AnyLog-co/deployment-scripts" target="_blank">Deployment Scripts</a> used to deploy an 
agent based on user-defined configurations. 

This means that when updating AnyLog (or EdgeLake) agents, there are 3 ways of deployment: 
* [**Network Reset**](#network-reset) - start from scratch 
* [**Update Agent Only**](#update-agent) - update AnyLog / EdgeLake software agent only 
* [**New Nodes with Updated Version**](#new-nodes-with-updated-version) - Having different version on the same network.
**Note**, all versions assume you've downloaded and ran using some flavor of our docker-compose or k8s-deployment. 


## AnyLog / EdgeLake Version 

AnyLog team tries to provide a new (stable) version every 4-6 weeks, with patches whenever issues are found. 

Our basic AnyLog / EdgeLake version number is [AnyLog Generation - currently 1].[Generation Version - currently 4].[yyymm]

**Version Lists**:
* 1.3.X - 2024-2025 
* 1.4.X - Aug 2025 to Present
* Latest - this gets updated less frequently, and is done only when we feel comfortable enough with the code "current" version. 
EdgeLake is usually updated in parallel to when we release a _latest_ version for AnyLog. 


## Network Reset

A network reset is exactly how it sounds. It's the idea of cleaning up AnyLog and redeploying it with latest. 

1. Stop the containers
```shell
make down ANYLOG_TYPE=[master | operator | query | publisher]
# - or - 
make down EDGELAKE_TYPE=[master | operator | query | publisher]
```

2. Remove docker volumes - this can be done with `make clean`  instead of `make down` **or** if you'd like to keep your 
data, remove only the blockchain volume and local scripts. 
```shell
docker volume rm docker-compose_{CONTAINER_NAME}-blockchain
docker volume rm docker-compose_{CONTAINER_NAME}-local-scripts
```

3. Removing Databases
   * **Option 1**: The first option when starting from scratch is to remove the logical databases
     * For master node: _blockchain_
     * For operator node: _[DEFAULT\_DBMS]_ and _[almg]_
   
**For Postgres**: 
```shell
# stored in postgres 
psql -h [ip] -p 5432 -U [user] -d postgres -c "drop database [DB NAME]"
```
   
**For SQLite**: This is stored under `docker-compose_{CONTAINER_NAME}-data`, users can simply remove the entire container, 
or just the _dbms_ directory within this volume. 

4. In your Makefile update the _TAG_ value for the desired version 



## Update Agent

## New Nodes with Updated Version