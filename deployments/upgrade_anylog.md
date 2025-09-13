# Upgrading AnyLog / EdgeLake

AnyLog is designed as an extension of EdgeLake, with the goal of making deployments and upgrades fully interchangeable. 
This allows users to seamlessly upgrade their systems—whether by moving to a newer code version or by migrating from an 
EdgeLake instance to an AnyLog (enterprise) network.

Before performing an upgrade, review the [Quick Start](../quick_start.md) guide, which introduces configurations and 
deployment details assumed in this document.

This document describes three common upgrade paths:
* **Network Reset** — restarting from scratch with a clean deployment 
* **Update Agent Only** — updating the AnyLog / EdgeLake software agent while preserving data and configurations 
* **New Nodes with Updated Version** — rolling out upgrades to a subset of nodes, while keeping older versions active on 
existing nodes

Note, when deploying AnyLog or EdgeLake via container services like _Docker_, _Podman_ and _Kubernetes_ the deployment 
consists of two major parts: 
* The actual AnyLog or EdgeLake agent 
* <a href="https://github.com/AnyLog-co/deployment-scripts" target="_blank">Deployment Scripts</a> used to deploy an 
agent based on user-defined configurations. 

## Versioning

The AnyLog team typically provides a new (stable) release every 4–6 weeks, with patches released as needed.

**Version Format**:
```shell
[Major Generation - currently 1].[Minor Generation - currently 4].[yyymm]
```

| Version    | Range/Timeline          | Notes                          |
| ---------- | ----------------------- | ------------------------------ |
| **1.3.X**  | 2024–2025               | Previous stable generation     |
| **1.4.X**  | Aug 2025 – Present      | Current stable generation      |
| **latest** | Updated less frequently | Marked only when highly stable |


EdgeLake versions are usually updated in parallel with AnyLog’s _latest_.


## Upgrading Nodes 

### Prepare for Upgrade

This section is relevant only for when users want to start from a clean deployment for preserving data and 
configurations. 
 
1. **Stops nodes**: On each of the active nodes of the network, stop AnyLog / EdgeLake agents. 

```shell
# for AnyLog 
make down ANYLOG_TYPE=[Node Type]

# for EdgeLake
make down EDGELAKE_TYPE=[Node Type]
```

2. (Optional) **Backup Scripts**: Make sure to backup any personalized scripts stored in AnyLog / EdgeLake volumes
    * Locate volume path - `docker insert docker-compose_[node-name]-local-scripts`
    * Copy content - `mkdir $HOME/bkup ; cp /var/lib/docker/volumes/docker-compose-files_[node-name]-local-scripts/_data/node-deployment/local_script.al $HOME/bkup`


3. (Optional) **Clean Databases**:  Remove logical databases for Operator node and Master node  


Access operator node and clean logical databases for operator node

* PostgresSQL option - `for DB_NAME in almgm [logical-database]; do psql -h 127.0.0.1 -p 5432 -U [user] -d "drop database ${DB_NAME}"; done`
* SQLite - this would be done via volume remove 


Access master node and remove blockchain logical database 

* PostgresSQL option - `psql -h 127.0.0.1 -p 5432 -U [user] -d "drop database blockchain"`
* SQLite - this would be done via volume remove 

4. **Remove volumes**: Remove docker volumes for all nodes in the network  

**Option 1**: Remove all volumes associated with the local AnyLog / EdgeLake 

```shell
# for AnyLog 
make clean-vols ANYLOG_TYPE=[Node Type]

# for EdgeLake
make clean-vols EDGELAKE_TYPE=[Node Type] 
```
**Note**: to remove docker image simply (and volumes) replace `make clean-vols` with `make clean`. 

**Option 2**: Remove specific volumes. AnyLog / EdgeLake directories are: 
* `anylog` - security and authentication keys 
* `blockchain` - a copy of the blockchain file 
* `local-scripts` - AnyLog / EdgeLake deployment scripts 
* `data` - copy of JSON / SQL data, as well as SQLite logical database 

```shell
docker volume rm docker-compose-[node_name]-[directoy-name]
```

### Update Makefile and Configs

1. In each of the nodes,  there’s a file called [Makefile](https://github.com/AnyLog-co/docker-compose/blob/main/Makefile), 
which a variable called `TAG`, which is used to specify the version of AnyLog / EdgeLake to run. There are 2 ways by 
which to update this value. Either one time manually **or** statically. 

**Option 1**: Update the value one time manually, by simply adding it into the `make up` CLI command. When using this 
option, make to complete everything else **before** executing `make up`. 

```shell
# for AnyLog
make up ANYLOG_TYPE=[node type] TAG=[AnyLog Version]

# for EdgeLake 
make up EDGELAKE_TYPE=[node type] TAG=[AnyLog Version]
```

**Option 2**: Update statically within the Makefile

```Makefile
# Before 
export TAG := 1.3.2501-beta11

# After 
export TAG := 1.4.2508-beta10
```

2. Update any configurations you'd like prior to redeployment

#### Switch from EdgeLake to AnyLog

The following provides directions from switch from EdgeLake to AnyLog. This is section can be ignored if you have 

1. Inside the docker-compose/docker-makefiles there's a [.env](https://github.com/EdgeLake/docker-compose/blob/main/docker-makefiles/.env)
file that contains an `IMAGE` param used by the _Makefile_ to dictate whether we'll be using AnyLog or EdgeLake. 
In order to use AnyLog instead of EdgeLake, you will need to update this value 

```shell
# before
IMAGE=anylogco/edgelake

# after
IMAGE=anylogco/anylog-network
```

2. Request Docker login credentials and 90-day AnyLog license key via <a href="https://www.anylog.network/download" target="_blank">our website</a> 

3. Login to docker 

```shell
docker login -u anyloguser -p [email provided password]
```

4. In your node configurations, include the LICENSE_KEY

```dotenv
LICENSE_KEY="[email provided license key]"
```

### Deploy New Version
Once you've updated the configurations its time to start the network 

1. Start node(s) 

```shell 
# for AnyLog 
make up ANYLOG_TYPE=[Node Type]

# for EdgeLake
make up EDGELAKE_TYPE=[Node Type]
```

2. Copy user-defined scripts into updated docker volumes.
   * Locate volume path - `docker insert docker-compose_[node-name]-local-scripts`
   * Copy content - `cp $HOME/bkup/local_script.al /var/lib/docker/volumes/docker-compose-files_[node-name]-local-scripts/_data/node-deployment/local_script.al`
 
3. Within AnyLog / EdgeLake CLI execute local script 

```
# attach to node 

make attach ANYLOG_TYPE=[Node Name] 

# - or - 
make attach EDGELAKE_TYPE=[Node Name] 

# Execute
process !local_scripts/local_script.al 
```

## Multiple Version Configurations

There are scenarios where users would like to keep the existing nodes running, and add new nodes that are using a newer version of 
AnyLog or EdgeLake. 

When running such a setup users need to be aware of a few things: 
1. Nodes using _EdgeLake_ do not support things like HA on operator nodes and security in general. Please review [FAQ](../FAQ.md#general-questions-) 
for farther details. 
2. Major versions (example 1.3 -> 1.4) may contain changes in the deployment scripts file paths. This is something to wary 
of as it can influence configuration policies. 

### Steps

Please follow the directions in [Quick Start](../quick_start.md). However, keep in mind that we high recommend you start 
using unique configuration policy naming as major version changes can have updated file paths.

Critical parameter name: `CONFIG_NAME`
* Location in EdgeLake is under the node dotenv configurations 
* Location in EdgeLake is under the node advanced dotenv configurations
