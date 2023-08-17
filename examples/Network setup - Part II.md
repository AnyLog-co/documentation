# Network Setup

The following document provides directions to manually restarting an AnyLog node, with persistent volumes,

Directions to deploy AnyLog nodes manually from scratch, can be found in [part 1](Network%20setup%20-%20Part%20I.md)

**Other Deployments** 
* [Training](../training) - Standard training used for explaining how to use AnyLog
* [Configuration Based](../deployments/deploying_node.md) - Deploy AnyLog using configuration file with environment variables
* [Quick Deployment](Quick%20Deployment.md) - Deploy an AnyLog with preset services, with limited environment configurations 

## Prepare Node
To manually deploy an AnyLog instance, users need to deploy node(s) without anything running. Please [contact us](mailto:info@anylog.co) 
if you do not have access to our Docker hub and/or an active license key. 

1. Log into AnyLog user
```shell
docker login -u anyloguser -p ${ANYLOG_DOCKER_PASSWORD}
```

2. Starting a node with nothing on it, this step should be done for **each** AnyLog instance. Make sure to use the 
same persistent volume names used when first deploying the node. 
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
A _master node_ is an alternative option to the blockchain, where metadata will reside on a dedicated AnyLog node. 

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

3. Set params -- variables (ex. `!external_ip`) that are used but not declare are using the _default_ value.   
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
# execute policy
policy_id = blockchain get config where name=anylog-master-network-configs and company=!company_name bring [*][id] 
config from policy where id = !policy_id
```

5. Connect to blockchain logical database and create _ledger_ table
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
```

7. run scheduler & blockchain sync
```anylog
# start scheduler 
run scheduler 1

# blockchain sync 
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

## Deploy Query
A _query node_ is one that's dedicated for issue queries against the network. Any node can act as a query node, 
as long as [system_query](sandbox%20-%20Network%20setup.md#L189-L193) database exists. 

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

3. Set params -- variables (ex. `!external_ip`) that are used but not declare are using the _default_ value.   
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

6. Connect to system_query logical database against in-memory SQLite 
```anylog
# example with SQLite 
connect dbms blockchain where type=sqlite and memory=true  
```

## Deploy Operator
An _operator node_ is one that's dedicated to hosting user data. When deploying multiple operators there are a few things to keep in mind: 
* Make sure each cluster has a unique name -- If multiple operators share a cluster, then when querying, results from **only 1** 
of the operators will be returned. More information can be found in  [high-avilability](../high%20availability.md).    
* Make sure each operator has a unique name
* If the operators are on the same physical machine, make sure each operator has unique port values. 

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

3. Set params -- variables (ex. `!external_ip`) that are used but not declare are using the _default_ value.
```anylog
company_name="New Company"
set default_dbms = test
 
anylog_server_port=32148
anylog_rest_port=32149 

set tcp_bind=false
set rest_bind=false
set rest_ssl=false

tcp_threads=6 
rest_threads=6
rest_timeout=30 
operator_threads=6

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

6. Get operator ID
```anylog
operator_id = blockchain get operator where name=operator-node and company=!company_name 
```

7. Connect to logical database(s)
**Part 1**: `!default_dbms` - this is where user data is resides 
```anylog
connect dbms !default_dbms where type=sqlite 

# example with PostgresSQL 
<coneect dbms !default_dbms where
  type=psql and
  ip=127.0.1 and
  port=5432 and 
  user=admin and
  password=passwd>
```
**Part 2**: `almgm` logical database and `tsd_info` table - this is used to keep a record of the data coming in 
```anylog
connect dbms almgm where type=sqlite 

# example with PostgresSQL 
<coneect dbms almgm where
  type=psql and
  ip=127.0.1 and
  port=5432 and 
  user=admin and
  password=passwd>
 
create table tsd_info where dbms=almgm
``` 

8. (Optional) Partition the data 
```anylog 
partition !default_dbms * using insert_timestamp by 1 day
```

9. Accept data into AnyLog Operator
```anylog
# buffer size until data is inerted 
set buffer threshold where time=60 seconds and volume=10KB and write_immediate=true 

# Writes streaming data to files
run streamer

# start operator to accept data coming in 
<run operator where
    create_table=true and
    update_tsd_info=true and
    compress_json=true and
    compress_sql=true and 
    archive=true and
    master_node=!ledger_conn and
    policy=!operator_id and
    threads = !operator_threads
> 
```