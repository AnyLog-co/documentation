## Network Setup

The following provides directions to manually deploy an AnyLog of type _master_, _operator_ or _query_ node with network
being set using a blockchain policy. 

[Network Setup](Network%20Setup.md) provides the same directions, but with network condifigurations set manually. 

## Docker deployment process

1. Log into AnyLog user (on each physical machine)
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
When deploying an AnyLog container, 2 things happen in the background during start up. This is done using the 
[start_empty_node.al](..%2F..%2F..%2Fdeployment-scripts%2Fscripts%2Frun_scripts%2Fstart_empty_node.al) 

1. Directories get declared and created, with values that are preset in the [Dockerfile](../../deployments/Support/Dockerfile).

2. If a license key is set as en enviornment variable during `docker run`, then the AnyLog license key will be set. 
```anylog
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

1. Set license key - this step is redundant, and will not be re-executed, if license key was provided in the [docker deployment process](#docker-deployment-process).
```anylog
set license where activation_key = ${ANYLOG_LICENSE_KEY}
```

2. Disable authentication and enable message queue
```anylog
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consule)
```
Note: when messages are placed in the queue, the CLI prompt is extended by a plus (+) sign.
The command `get echo queue` retrieves the messages and removes the plus sign.

3. Declare the root directory and create the work directories
```anylog
# This is an ENV variable, that's preset as part of the dockerfile - $ANYLOG_PATH = /app
anylog_path = $ANYLOG_PATH

# define the root directory for AnyLog
set anylog home !anylog_path

# This is an ENV variable, that's preset as part of the dockerfile - $LOCAL_SCRIPTS=/app/deployment-scripts/scripts
set local_scripts = $LOCAL_SCRIPTS

# This is an ENV variable, that's preset as part of the dockerfile - $TEST_DIR=/app/deployment-scripts/tests
set test_dir = $TEST_DIR

# create directories (such as blockchain, data/watch. anylog) that are used by the AnyLog node
create work directories
```
Note: Creating the work directories needs to be done once. The next time the nodes starts, only the root directory needs to be re-declared.
Users can view the work directories using the following command:
```anylog
get dictionary _dir
```

4. Update the local dictionary with the key-value pairs that are used to declare the node's functionality and services.
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

5. Declare a database to service the metadata table (the _ledger_ table)
* For SQLite, databases are created in `!dbms_dir`
* Directions for deploying a [PostgresSQL database](../../deployments/deploying_dbms.md#postgressql) 
```anylog
connect dbms blockchain where type=sqlite
creaate table ledger where dbms=blocchain 
```
Note: If SQLite is used, databases are created in `!dbms_dir`.

6. Enable the TCP and REST services - Configuration base connectivity
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

# execute policy
policy_id = blockchain get config where name=anylog-master-network-configs and company=!company_name bring [*][id]
config from policy where id = !policy_id
```

7. run the scheduler & blockchain sync process
```anylog
# start scheduler (that service the rule engine)
run scheduler 1

# blockchain sync 
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

8. Declare the master node on the shared metadata  
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
