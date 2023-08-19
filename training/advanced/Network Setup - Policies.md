## Network Setup using policies

This document details deployment of AnyLog nodes using policies.    

[Network Setup](Network%20Setup.md) is a similar installation guide, without configuration policies.  

## Docker Deployment Process

1. Log as AnyLog user (on each physical machine)
```shell
docker login -u anyloguser -p ${ANYLOG_DOCKER_PASSWORD}
```
2. Deploy the Docker container of AnyLog with no preset configurations. This step is done for **each** AnyLog instance.
    * `NODE_TYPE` represents a unique name for each container, and its corresponding volumes. For example, use **master**
     for the master node container and **operator-1** for an operator node.
    * `LICENSE_KEY` - the AnyLog provided key.
    * The example shows deployment with [volume configurations](../../deployments/Networking%20&%20Security/docker_volumes.md).
This configuration is  optional; however, if used, make sure naming is unique per volume per container.

```shell
NODE_TYPE=master
docker run -it --detach-keys=ctrl-d --network host \
  -e LICENSE_KEY=${ANYLOG_LICENSE_KEY} \
  -e INIT_TYPE=raw  \
  -v anylog-${NODE_TYPE}-anylog:/app/AnyLog-Network/anylog \
  -v anylog-${NODE_TYPE}-blockchain:/app/AnyLog-Network/blockchain \
  -v anylog-${NODE_TYPE}-data:/app/AnyLog-Network/data \
  -v anylog-${NODE_TYPE}-scripts:/app/deployment-scripts/scripts \
  -v  anylog-${NODE_TYPE}-test:/app/deployment-scripts/tests \
--name ${NODE_TYPE}-node --rm anylogco/anylog-network:latest
```

### Background Process
When deploying an AnyLog container, the AnyLog instance needs to be configured such that:

correct paths, and license key gets activated (if set). 

1. Directories get declared and created, with values that are preset in the [Dockerfile](../../deployments/Support/Dockerfile).

```anylog
# set env variables
if $ANYLOG_PATH then set anylog_path = $ANYLOG_PATH
set anylog home !anylog_path
if $ANYLOG_ID_DIR then set id_dir = $ANYLOG_ID_DIR

if $BLOCKCHAIN_DIR then
do set blockchain_dir = $BLOCKCHAIN_DIR
do set blockchain_file = !blockchain_dir/blockchain.json
do set blockchain_new = !blockchain_dir/blockchain.new
do set blockchain_sql = !blockchain_dir/blockchain/blockchain.sql

if $DATA_DIR then  # default: /app/AnyLog-Network/data
do set data_dir = $DATA_DIR
do set archive_dir = !data_dir/archive
do set bkup_dir = !data_dir/bkup
do set blobs_dir = !data_dir/blobs
do set bwatch_dir = !data_dir/bwatch
do set dbms_dir = !data_dir/dbms
do set distr_dir = !data_dir/distr
do set err_dir = !data_dir/error
do set pem_dir = !data_dir/pem
do set prep_dir = !data_dir/prep
do set test_dir = !data_dir/test
do set tmp_dir = !data_dir/tmp
do set watch_dir = !data_dir/watch

if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR

# create directories 
create work directories
```
**Note**: Creating the work directories needs to be done once. The next time the nodes starts, only the root directory 
needs to be re-declared. Users can view the work directories using the following command:
```anylog
get dictionary _dir
```


2. If a license key is set as en enviornment variable during `docker run`, then the AnyLog license key will be set. 
License key must be set for any other commands to be executed

```anylog
set license where activation_key = $LICENSE_KEY
```

## Master Node Configuration
A _master node_ is an alternative to the blockchain. With a master node, the metadata is updated into and retrieved from
 a dedicated AnyLog node.

* Attaching to the CLI (node name: `master-node`)
```shell
docker attach --detach-keys=ctrl-d master-node
```
* Detaching from Docker container: `ctrl-d`

Issue the following configuration commands on the AnyLog CLI, alternatively you can run:
```anylog
process !local_scripts/documentation_deployments/master_configuration.al
```

* All commands for this script can be run using the following script:
```anylog
process !local_scripts/documentation_deployments/master_network_policy.al
```

1. Disable authentication and enable message queue
```anylog
on error ignore           # ignore error messages
set debug off             # disable debugging, by setting debug to `on` users can view what happens in each step
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consul)
```
**Note**: when messages are placed in the queue, the CLI prompt is extended by a plus (+) sign.
The command `get echo queue` retrieves the messages and removes the plus sign.

2. Update the local dictionary with the key-value pairs that are used to declare the node's functionality and services.
```anylog
node_name = Master              # Adds a name to the CLI prompt
company_name="New Company"

anylog_server_port=32048
anylog_rest_port=32049

set tcp_bind=false
set rest_bind=false

tcp_threads=6
rest_threads=6
rest_timeout=30

ledger_conn=127.0.0.1:32048
```

3. Declare a database to service the metadata table (the _ledger_ table)
* For SQLite, databases are created in `!dbms_dir`
* Directions for deploying a [PostgresSQL database](../../deployments/deploying_dbms.md#postgressql) 
```anylog
connect dbms blockchain where type=sqlite
creaate table ledger where dbms=blocchain 
```
**Note**: If SQLite is used, databases are created in `!dbms_dir`. 
 
4. Enable the TCP and REST services - Configuration base connectivity
```anylog
<new_policy = {"config": {
   "name": "anylog-master-network-configs",
   "company": !company_name,
   "ip": "!external_ip",
   "local_ip": "!ip",
   "port": "!anylog_server_port.int",
   "rest_port": "!anylog_rest_port.int"
}}>

# declare policy
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```
**Note**: There is no need to recreate the policy in a situation where the node restarts itself, and the data is persistent.  

5. execute policy
```anylog
policy_id = blockchain get config where name=anylog-master-network-configs and company=!company_name bring [*][id]
config from policy where id = !policy_id
```

6. run the scheduler & blockchain sync process
```anylog
# start scheduler (that service the rule engine)
run scheduler 1

# blockchain sync 
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

7. Declare the master node on the shared metadata  
```anylog
# if TCP bind is false, then state both external and local IP addresses 
<new_policy = {"master": {
  "name": "master-node", 
  "company": !company_name, 
  "ip": !external_ip, 
  "local_ip": !ip,
  "port": !anylog_server_port.int, 
  "rest_port": !anylog_rest_port.int
}}>

# OR

# if TCP bind is true, then stae only the local IP  aaddress
<new_policy = {"master": {
  "name": "master-node", 
  "company": !company_name, 
  "ip": !ip,
  "port": !anylog_server_port.int, 
  "rest_port": !anylog_rest_port.int
}}> 

# declare policy 
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```
**Note**: There is no need to recreate the policy in a situation where the node restarts itself, and the data is persistent.

## Query Node Configuration
A _query node_ is an AnyLog node configured to satisfy queries. Any node can act as a query node, as long as 
[system_query](sandbox%20-%20Network%20setup.md#L189-L193) database is configured. 

* Attaching to the CLI (node name: `query-node`)
```shell
docker attach --detach-keys=ctrl-d query-node
```
* Detaching from Docker container: `ctrl-d`

Issue the following configuration commands on the AnyLog CLI, alternatively you can run:
```anylog
process !local_scripts/documentation_deployments/query_configuration.al
```

* All commands for this script can be run using the following script:
```anylog
process !local_scripts/documentation_deployments/master_network_policy.al
```

* All commands for this script can be run using the following script:
```anylog
process !local_scripts/documentation_deployments/query_network_policy.al
```

1. Disable authentication and enable message queue
```anylog
on error ignore           # ignore error messages
set debug off             # disable debugging, by setting debug to `on` users can view what happens in each step
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consul)
```
**Note**: when messages are placed in the queue, the CLI prompt is extended by a plus (+) sign.
The command `get echo queue` retrieves the messages and removes the plus sign.

2. Update the local dictionary with the key-value pairs that are used to declare the node's functionality and services.
```anylog
node_name = Query             # Adds a name to the CLI prompt
company_name="New Company"

anylog_server_port=32348
anylog_rest_port=32349

set tcp_bind=false
set rest_bind=false

tcp_threads=6
rest_threads=6
rest_timeout=30

ledger_conn=127.0.0.1:32048
```

3. Connect to system_query logical database against in-memory SQLite.
* For SQLite, databases are created in `!dbms_dir`
* Directions for deploying a [PostgresSQL database](../../deployments/deploying_dbms.md#postgressql) 
```anylog
# example with SQLite 
connect dbms system_query where type=sqlite and memory=true 
```
**Note**: If SQLite is used, the SQLite databases are created in `!dbms_dir`. 
 
4. Enable the TCP and REST services - Configuration base connectivity
```anylog
<new_policy = {"config": {
   "name": "anylog-query-network-configs",
   "company": !company_name,
   "ip": "!external_ip", 
   "local_ip": "!ip",
   "port": "!anylog_server_port.int",
   "rest_port": "!anylog_rest_port.int" 
}}>

# declare policy
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```
**Note**: There is no need to recreate the policy in a situation where the node restarts itself, and the data is persistent.  

5. execute policy
```anylog
policy_id = blockchain get config where name=anylog-master-network-configs and company=!company_name bring [*][id]
config from policy where id = !policy_id
```

6. run the scheduler & blockchain sync process
```anylog
# start scheduler (that service the rule engine)
run scheduler 1

# blockchain sync 
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

7. Declare the query node on the shared metadata  
```anylog
# if TCP bind is false, then state both external and local IP addresses 
<new_policy = {"query": {
  "name": "query-node", 
  "company": !company_name, 
  "ip": !external_ip, 
  "local_ip": !ip,
  "port": !anylog_server_port.int, 
  "rest_port": !anylog_rest_port.int
}}>

# OR

# if TCP bind is true, then stae only the local IP  aaddress
<new_policy = {"query": {
  "name": "master-node", 
  "company": !company_name, 
  "ip": !ip,
  "port": !anylog_server_port.int, 
  "rest_port": !anylog_rest_port.int
}}> 

# declare policy 
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```
**Note**: There is no need to recreate the policy in a situation where the node restarts itself, and the data is persistent.
