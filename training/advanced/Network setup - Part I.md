# Network Setup

The following document provides directions to deploy AnyLog nodes using the node's CLI.
Alternatively, the configuration script can be organized in a file and processed using the following command:
```
process [path and file name with the script]
```
For example:  
```
process process !anylog_path/AnyLog-Network/demo/ha_master.al
```
Note: **!anylog_path** will be substituted for the value assigned to the key **anylog_path** in the dictionary.

## Frequently used commands to monitor settings
Users are expected to be familiar with the commands and examples listed below:
<pre>
get dictionary         # Default values in the dictionary
get dictionary _dir    # Directory setting
get dictionary ip      # Default ip setting
get connections        # Active listener services (for TCP, REST, and Broker services)
get databases          # Get the list of databases configured
get processes          # Show background processes enabled
get dictionary         # Show variables assigned
get inserts            # Statistics on data ingestion to the local database of an Operator node
!blockchain_file       # shows a variable value
run client !master_node get connections  # will show the config on the master
</pre>


## The root directory and the default directories
To define the root directory for AnyLog (which is different from the default), use the following command:
<pre>
set anylog home [path to AnyLog root]
</pre>
If the root directory is changed or AnyLog is installed without a package that creates the work directories, 
the default directories can be created using the command:
<pre>
create work directories
</pre>
 

## Prerequisites
* Docker hub key
* Active license key
 
1. Log into AnyLog user
```shell
docker login -u anyloguser -p ${ANYLOG_DOCKER_PASSWORD}
```

2. Starting a node with nothing on it, this step should be done for **each** AnyLog instance. Make sure to update the 
following params:
* `LICENSE_KEY`, otherwise  the AnyLog instance will not be activated
* Docker container name should be unique 
* The example shows deployment with [volume configurations](../../deployments/Networking%20&%20Security/docker_volumes.md).
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
A _master node_ is an alternative to the blockchain. With a master node, the metadata is updated into and retrieved from
 a dedicated AnyLog node. 

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

5. Declare master node policy -- based on the TCP binding, add the relevant _master node_ policy.  
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

6. Declare query node policy -- based on the TCP binding, add the relevant _master node_ policy.  
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

## Deploy Operator
An _operator node_ is one that's dedicated to hosting user data. When deploying multiple operators there are a few things to keep in mind: 
* Make sure each cluster has a unique name -- If multiple operators share a cluster, then when querying, results from **only 1** 
of the operators will be returned. More information can be found in  [high-avilability](../../high%20availability.md).    
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
<new_policy = {"config": {
   "name": "anylog-operator-network-configs",
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

6. Create cluster database 
```anylog
<new_policy = {"cluster": {
    "company": !company_name,
    "name": cluster1,
    "dbms": !default_dbms
}}>

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

7. Get cluster ID
```anylog
cluster_id = blockchain get cluster where company=!company_name and name=cluster1 bring.first [*][id] 
```

8. Declare operator node policy -- based on the TCP binding, add the relevant _master node_ policy.  
```anylog
# if TCP bind is false, then state both external and local IP addaresses 
<new_policy = {"operator": {
  "name": "operator-node", 
  "company": !company_name, 
  "ip': !external_ip, 
  "local_ip": !ip,
  "port": !anylog_server_port, 
  "rest_port": !anylog_rest_port,
  "cluster": !cluster_id
}}>

# if TCP bind is true, then stae only the local IP  aaddress
<new_policy = {"operator": {
  "name": "operator-node", 
  "company": !company_name, 
  "ip": !ip,
  "port": !anylog_server_port, 
  "rest_port": !anylog_rest_port,
  "cluster": !cluster_id
}}> 

# declare policy 
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

9. Get operator ID
```anylog
operator_id = blockchain get operator where name=operator-node and company=!company_name 
```

10. Connect to logical database(s)
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

11. (Optional) Partition the data 
```anylog 
partition !default_dbms * using insert_timestamp by 1 day
```

12. Accept data into AnyLog Operator
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

## Validate Network is Up
Once nodes are up and running, users can validate that everything is working properly using some basic commands, this can
be done on any of the nodes that are part of the network. 

* `test network` - will validate nodes can communicate with one another
* `blockchain get *` - will show policies on the network. Based on the directions above, users should see: 
  * master node policy 
  * query node policy 
  * cluster policy 
  * operator node policy 
  * if networking is set up via configuration, users should also see a config policy for each node 
* `get processes` - should be run on each node individually (or via `run client`) to validate which AnyLog services are 
running on a given node. 


## Inserting & Querying data 

* Inserting data via cURL command 
```shell
curl -X PUT 127.0.0.1:32149 \
  -H "command: data" \
  -H "dbms: test" \
  -H "table: ping_sensor" \
  -H "type: json" \
  -H "mode: streaming" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: application/json"
  --data '[{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 1021, "timestamp": "2019-10-11T17:05:53.1820068Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 2021, "timestamp": "2019-10-11T17:15:53.1500091Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 2100, "timestamp": "2019-10-11T17:15:58.1500091Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:25:53.2300109Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:25:58.1530151Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:35:58.126007Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:36:03.1430053Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-11-11T17:46:03.1420135Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:46:08.1420135Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 221, "timestamp": "2019-10-11T17:56:03.1590118Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:56:08.1440124Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-12-11T18:06:03.1300048Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T18:06:08.1450042Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2020-10-11T18:16:03.1470031Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2020-10-11T18:16:08.1470031Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2020-10-11T18:26:03.1480102Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-11-11T18:26:08.1790008Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T18:36:08.149002Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 221, "timestamp": "2019-10-11T18:36:13.1350097Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 261, "timestamp": "2019-10-11T18:46:08.1830139Z"},
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 121, "timestamp": "2019-10-11T18:46:13.152008Z"}]'
```

* Sample Queries
```anylog
run client () sql lsl_demo format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor limit 100"
run client () sql lsl_demo format = table "select count(*), min(value), max(value) from ping_sensor"
```

* Supporting commands to track data coming in
```anylog 
# Statistics on SQL Inserts of data to the local databases.
get inserts

# Statistics on the streaming processes. 
get streaming 

# Information on the Operator processes and configuration. 
get operator

# Get the count of rows in the specified table or all tables asigned to the specified database.
get rows count

# Get the count of rows in the specified table or all tables asigned to the specified database, group by table 
get rows count where group = table
```