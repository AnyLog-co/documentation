# Network Setup

This document demonstrates a network setup of 3 nodes:
* A Master Node - to contain the metadata
* An Operator Node - to host the user data
* A Query Node - to issue queries to the network

Directions to use pre-existing deployment scripts, using enviornment varibales can be found [here](../deployments).  

## Prepare Node
To manually deploy an AnyLog instance, users need to deploy node(s) without anything running. Please [contact us](mailto:info@anylog.co) 
if you do not have access to our Docker hub and/or an active license key. 

1. Log into AnyLog user
```shell
docker login -u anyloguser -p ${ANYLOG_DOCKER_PASSWORD}
```

2. Starting a node with nothing on it, this step should be done for **each** AnyLog instance. Make sure to update the 
following params:
* `LICENSE_KEY`, otherwise  the AnyLog instance will not be activated
* Docker container name should be unique 
* The example shows deployment with [volume configurations](../deployments/Networking%20&%20Security/docker_volumes.md).
This configuration is  optional; however, if used, make sure naming is unique per volume per container.    
```shell
docker run -it --detach-keys=ctrl-d --network host \
  -e LICENSE_KEY=${ANYLOG_LICENSE_KEY} \
  -e INIT_TYPE=raw  \
  -v anylog-node-blockchain:/app/AnyLog-Network/anylog \
  -v anylog-node-blockchain:/app/AnyLog-Network/blockchain \
  -v anylog-node-data:/app/AnyLog-Network/data \
  -v anylog-node-scripts:/app/deployment-scripts/scripts \
  -v  anylog-node-test:/app/deployment-scripts/tests \
--name anylog-node --rm anylogco/anylog-network:latest
```

## Deploy Master
1. Set license key - this step is done automatically, if set as environment variable
```anylog
set license where activation_key = ${ANYLOG_LICENSE_KEY}
```

2. Declare & create directories that are used within AnyLog  
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

3. Set params -- varibalese (ex. `!external_ip`) that are used but not declare are using the _default_ value.   
```anylog
company_name="New Company"

anylog_server_port=32048
anylog_rest_port=32049 

set tcp_bind=false
set rest_bind=false
set rest_ssl=false

tcp_threads=6 
rest_threads=6
rest_timeout=30 

ledger_conn=127.0.0.1:32048 
```

4. Connect to TCP and REST 

**Option 1**: Manually configure TCP and REST connectivity 
```anylog
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
    
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout and ssl=!rest_ssl>
```

**Option 2**: Configuration base connectivity 
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

5. Declare master node policy -- bsaed on the TCP binding, add the relevant _master node_ policy.  
```anylog
# if TCP bind is false, then state both external and local IP addaresses 
<new_policy = {"master": {
  "name": "master-node", 
  "company": !company_name, 
  "ip': !external_ip, 
  "local_ip": !ip,
  "port": !anylog_server_port, 
  "rest_port": !anylog_rest_port
}}>

# if TCP bind is true, then stae only the local IP  aaddress
<new_policy = {"master": {
  "name": "master-node", 
  "company": !company_name, 
  "ip": !ip,
  "port": !anylog_server_port, 
  "rest_port": !anylog_rest_port
}}> 

# declare policy 
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

6. Connect to blockchain logical database and create _ledger_ table
```anylog
# example with SQLite 
connect dbms blockchain where type=sqlite 

# example with PostgresSQL 
<coneect dbms blockchain where
  type=psql and
  ip=127.0.1 and
  port=5432 and 
  user=admin and
  password=passwd>
  
# create ledger table 
create table ledger where dbms=blockchain  
```

7. run scheduler & blockchain sync
```anylog
# start scheduler 
run scheduler 1

# blockchain sync 
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

## Deploy Query
1. Set license key - this step is done automatically, if set as environment variable
```anylog
set license where activation_key = ${ANYLOG_LICENSE_KEY}
```

2. Declare & create directories that are used within AnyLog  
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

3. Set params -- varibalese (ex. `!external_ip`) that are used but not declare are using the _default_ value.   
```anylog
company_name="New Company"

anylog_server_port=32348
anylog_rest_port=32349 

set tcp_bind=false
set rest_bind=false
set rest_ssl=false

tcp_threads=6 
rest_threads=6
rest_timeout=30 

# if the msater node is not on the same physical machine, then the IP addrress should be that of the master node, rather than `127.0.0.1`
ledger_conn=127.0.0.1:32048 
```

4. Connect to TCP and REST 

**Option 1**: Manually configure TCP and REST connectivity 
```anylog
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
    
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout and ssl=!rest_ssl>
```

**Option 2**: Configuration base connectivity 
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

# execute policy
policy_id = blockchain get config where name=anylog-master-network-configs and company=!company_name bring [*][id] 
config from policy where id = !policy_id
```

5. run scheduler & blockchain sync
```anylog
# start scheduler 
run scheduler 1

# blockchain sync 
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

6. Declare master node policy -- bsaed on the TCP binding, add the relevant _master node_ policy.  
```anylog
# if TCP bind is false, then state both external and local IP addaresses 
<new_policy = {"query": {
  "name": "query-node", 
  "company": !company_name, 
  "ip': !external_ip, 
  "local_ip": !ip,
  "port": !anylog_server_port, 
  "rest_port": !anylog_rest_port
}}>

# if TCP bind is true, then stae only the local IP  aaddress
<new_policy = {"query": {
  "name": "query-node", 
  "company": !company_name, 
  "ip": !ip,
  "port": !anylog_server_port, 
  "rest_port": !anylog_rest_port
}}> 

# declare policy 
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

7. Connect to system_query logical database against in-memory SQLite 
```anylog
# example with SQLite 
connect dbms blockchain where type=sqlite and memory=true  
```


