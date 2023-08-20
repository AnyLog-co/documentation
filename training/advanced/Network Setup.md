# Network Setup

**Table of content**

[Deployment Prerequisites](#deployment-prerequisites)  
[Configuring nodes using a script file](#configuring-nodes-using-a-script-file)  
[Frequently used commands](#frequently-used-commands-to-monitor-settings)    
[Deploy AnyLog using Docker](#deploy-anylog-using-docker)  
[Deployment comments](#master-node-configuration)   
[Restarting a Node](#restarting-a-node)  
[Master Node Configuration](#master-node-configuration)  
[Query Node Configuration](#query-node-configuration)  
[Operator Node Configuration](#operator-node-configuration)    
[Validate Network](#validate-network-is-up)    
[Insert Data](#insert-data-using-curl)    
[Smaple Queries](#sample-queries)  
[Data Info Commands](#sample-data-info-commands---on-the-operator-node)    
[Tables Info commands](#sample-tables-info-commands---on-any-node)  


This document details deployment of AnyLog nodes using the CLI of the participating nodes.    

## Deployment Prerequisites
* Docker installed
* Docker hub key
* Active license key

## Configuring nodes using a script file
The configuration commands for each node can be organized in a file and processed using the following command (on the CLI):
```
process [path and file name with the script]
```
In the examples below, the commands to configure each node are organized in a file.  
Users can configure each node using the following commands:


| Node Type     | Command | 
| ------------- | ------- | 
| Master        | process !local_scripts/documentation_deployments/master.al |
| query         | process !local_scripts/documentation_deployments/query.al |
| Operator      | process !local_scripts/documentation_deployments/operator.al |

Note that `!local_scripts` is substituted (dynamically) with the value assigned to the key **local_scripts** in the dictionary.


## Frequently used commands to monitor settings
Users are expected to be familiar with the commands and examples listed below:
```anylog
get dictionary         # Default values in the dictionary
!blockchain_file       # shows the value assigned to the key blockchain_file
get dictionary _dir    # The keys and values representing the work directories
get dictionary ip      # Default ip setting
get connections        # Active listener services (for TCP, REST, and Broker services)
get databases          # Get the list of databases configured
get processes          # Show background processes enabled
get inserts            # Statistics on data ingestion to the local database of an Operator node
run client !master_node get connections  # will show the config on the master
```
 
## Deploy AnyLog using Docker 

1. Log as AnyLog user (on each physical machine)
```shell
docker login -u anyloguser -p ${ANYLOG_DOCKER_PASSWORD}
```
2. Deploy the Docker containers for the AnyLog nodes. This step is done for **each** AnyLog instance.
    * `NODE_TYPE` represents a unique name for each container, and its corresponding volumes. For example, use **master** 
     for the master node container, **query-1** for a query node and **operator-1** for an operator node. 
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

## Deployment comments:

### Setting the work directories
The work directories store files associated with each node and are listed in the
[Local Directory Structure](../../getting%20started.md#local-directory-structure) document.

When an AnyLog node is deployed, the AnyLog dictionary includes keys that represent directory names
and values that represent the path to each directory.

To define the root directory for AnyLog (if different from the default), use the following command:
```anylog 
set anylog home [path to AnyLog root]
```
Declaring the path for **anylog home** will modify the locations of the work directories to be subdirectories 
of the newly declared **anylog home**.

If the root directory is changed or AnyLog is installed without a package that creates the work directories , 
the work directories can be created (under AnyLog root) using the command:

```anylog
create work directories
```
Note: The **create work directories** command is executed **once** to create the physical directories.

With this Docker install, the work directories are declared and created according to the 
values that are preset in the [Dockerfile](../../deployments/Support/Dockerfile).

In this deployment, 2 additional key value pairs are added to the AnyLog dictionary to identify a directory to host 
scripts and and a directory to host test files (see the example commands below).  

```anylog
if $LOCAL_SCRIPTS then set local_scripts = $LOCAL_SCRIPTS
if $TEST_DIR then set test_dir = $TEST_DIR
```

Users can view the work directories using the following command:
```anylog
get dictionary _dir
```

### The AnyLog license key

If a license key is set as en environment variable during `docker run`, then the AnyLog license key will be set in the Docker install process.   
The License key can be provided on the CLI as in the example below:
```anylog
set license where activation_key = $LICENSE_KEY
```

### System databases
Different nodes use local databases to manage different tasks. System databases are declared like the user databases and are the following:

| Node Type     | DBMS Name     | Table Name    | Description | Create table command | 
| ------------- | ------------- | ------------- | ------------------------- |----- |
| Master        | blockchain    | Ledger        | Host the network metadata | create table ledger where dbms=blockchain |
| Query         | system_query  | -----         | Manage query result sets  | The tables are created transparently |
| Operator      | almgm         | tsd_info      | Monitor data ingestion    | create table tsd_info where dbms=almgm |

### Using PostgreSQL

The examples below are provided with SQLite. Users can use PostgreSQL by declaring the dbms **type** to be **psql**
as follows:
```anylog
<coneect dbms [logical dbms name] where
  type=psql and
  ip=[IP of PostgreSQL] and
  port=[PSQL port] and 
  user=[user name] and
  password=[user password]>
```
Example: 

```anylog
<coneect dbms almgm where
  type=psql and
  ip=127.0.0.1 and
  port=5432 and 
  user=admin and
  password=passwd>
```

Note:
* For SQLite, databases are created in `!dbms_dir`
* The following link includes the info for deploying a [PostgresSQL database](../../deployments/deploying_dbms.md#postgressql).

### Authentication disabled
In this setup authentication is disabled on all nodes.

### The message queue 
The message queue is an internal buffer on each node that stores messages (like error messages or messages from peer nodes).  
In this setup, the message queue is enabled on all nodes.   
Note: when messages are placed in the queue, the CLI prompt is extended by a plus (+) sign.  
The cpmmand `echo [mesage text]` will place the message text in the queue.    
The command `get echo queue` retrieves the messages and removes the plus sign.

### The bind option in REST, TCP and Message Broker services
The REST, TCP and Message Broker services can be configured to service one or two IPs.    
2 IPs are used when a node is communicating with peers on a local network as well as on the Internet.  
This document include 2 options: 
1) Policies where bind is false - to support multiple IPs
2) Policies where bind is true - to support a single IP.  

With option 1, 2 IPs are published in the metadata such that the node can be discovered by members on a local  
network as well as members over the Internet.

## Restarting a Node

The configurations below are doing the following:
* Deploy Docker instances and Docker Volumes. The Docker Volumes are created once when the Docker container is installed.
* Add Policies to the AnyLog Metadata. A policy is created once, stored in the metadata layer and available when the node restarts.
* Set variables in the node dictionary - this process is done whenever a node restarts.
* Enable selected services on the node - this is done whenever a node restarts.

Note: The deployment process in this document creates policies whenever they are needed. It is advised to separate 
the creation of the policies from the configuration of a node that restarts.
 
## Master Node Configuration
A _master node_ is an alternative to the blockchain. With a master node, the metadata is updated into and retrieved from
 a dedicated AnyLog node.  

* Attaching to the CLI (node name: `master-node`)  
```shell 
docker attach --detach-keys=ctrl-d master-node
``` 
* Detaching from Docker container: `ctrl-d`

Issue the following configuration commands on the AnyLog CLI. 

1. Disable authentication and enable message queue

```anylog
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (With off value (default) printed to the console)
```

2. Update the local dictionary with the key-value pairs that are used to declare the node's functionality and services.
      
```anylog

node_name = Master              # Adds a name to the CLI prompt

company_name="My_Company"     # Update to your company name

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

```anylog
connect dbms blockchain where type=sqlite 

# create ledger table 
create table ledger where dbms=blockchain  
```
 
4. Enable the TCP and REST services - Manually configure TCP and REST connectivity 
```anylog
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
    
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>
```

5. Enable the Scheduler service
```anylog
run scheduler 1  # start scheduler (that service the rule engine)
```

6. Enable the metadata sync service
```anylog
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

7. Declare the Master Node policy on the shared metadata  
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


## Query Node Configuration
A _query node_ is an AnyLog node configured to satisfy queries.  
Any node can act as a query node, as long as [system_query](sandbox%20-%20Network%20setup.md#L189-L193) 
database is configured.

* Attaching to the CLI (node name: `query-node`)  
```shell 
docker attach --detach-keys=ctrl-d query-node
``` 
* Detaching from Docker container: `ctrl-d`

Issue the following configuration commands on the AnyLog CLI.

1. Disable authentication and enable message queue
```anylog
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consule)
```
2. Update the local dictionary with the key-value pairs that are used to declare the node's functionality and services. 
```anylog
node_name = Query              # Adds a name to the CLI prompt

company_name="my_Company"     # Update to your company name 

anylog_server_port=32348
anylog_rest_port=32349 

set tcp_bind=false
set rest_bind=false

tcp_threads=6 
rest_threads=6
rest_timeout=30 

# if the msater node is not on the same physical machine, then the IP addrress should be that of the master node, rather than `127.0.0.1`
ledger_conn=127.0.0.1:32048 
```

3.  Enable the TCP and REST services 

Configure TCP and REST connectivity 
```anylog
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
    
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>
```

4. Enable the scheduler service
```anylog
run scheduler 1
```

5. Enable the metadata sync process
```anylog 
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

6. Declare query node policy -- based on the TCP binding, add the relevant _query node_ policy.  
```anylog
# if TCP bind is false, then state both external and local IP addaresses 
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
  "name": "query-node", 
  "company": !company_name, 
  "ip": !ip,
  "port": !anylog_server_port.int, 
  "rest_port": !anylog_rest_port.int
}}> 

# declare policy 
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

7. Connect to system_query database (using in-memory SQLite).
```anylog
# example with SQLite - Note: no need to declare a table 
connect dbms system_query where type=sqlite and memory=true  
```

## Operator Node Configuration
An _operator node_ hosts user data.  

Deployment considerations:

* Attaching to the CLI (node name: `operator1-node`)  
```shell 
docker attach --detach-keys=ctrl-d operator1-node
``` 
* Detaching from Docker container: `ctrl-d`

Issue the following configuration commands on the AnyLog CLI.

1. Disable authentication and enable message queue.
```anylog
set authentication off    # Disable users authentication
set echo queue on         # Some messages are stored in a queue (otherwise printed to the consule)
```

2. Update the local dictionary with the key-value pairs that are used to declare the node's functionality and services.

```anylog
node_name = Operator1              # Adds a name to the CLI prompt

company_name="My_Company"          # Update to your company name
set default_dbms = test
 
anylog_server_port=32148
anylog_rest_port=32149 

set tcp_bind=false
set rest_bind=false

tcp_threads=6 
rest_threads=6
rest_timeout=30 
operator_threads=6

ledger_conn=127.0.0.1:32048 
```

3.  Enable the TCP and REST services 

Configure TCP and REST connectivity 
```anylog
<run tcp server where
    external_ip=!external_ip and external_port=!anylog_server_port and
    internal_ip=!ip and internal_port=!anylog_server_port and
    bind=!tcp_bind and threads=!tcp_threads>
    
<run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout>
```

4. Create a cluster policy 

Note: **In this setup, create a unique cluster for each participating operator by setting a unique cluster name**
```anylog
<new_policy = {"cluster": {
    "company": !company_name,
    "name": "cluster1"
}}>

blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

5. Enable the scheduler service
```anylog
# start scheduler 
run scheduler 1
```

6. Enable the metadata sync service
```anylog 
run blockchain sync where source=master and time="30 seconds" and dest=file and connection=!ledger_conn
```

7. Get cluster ID  
The cluster ID identifies the cluster policy, it is added to the Operator policy when created (see the step below).
```anylog
cluster_id = blockchain get cluster where company=!company_name and name=cluster1 bring.first [*][id] 
```

8. Declare operator node policy -- based on the TCP binding, add the relevant _master node_ policy.  

Note: **with multiple operators make sure that the Operator name is unique, and make sure that the operator is associated with the unique cluster ID**.
```anylog
# if TCP bind is false, then state both external and local IP addaresses 
<new_policy = {"operator": {
  "name": "operator1-node", 
  "company": !company_name, 
  "ip": !external_ip, 
  "local_ip": !ip,
  "port": !anylog_server_port.int, 
  "rest_port": !anylog_rest_port.int,
  "cluster": !cluster_id
}}>

# OR

# if TCP bind is true, then stae only the local IP  aaddress
<new_policy = {"operator": {
  "name": "operator-node", 
  "company": !company_name, 
  "ip": !ip,
  "port": !anylog_server_port.int, 
  "rest_port": !anylog_rest_port.int,
  "cluster": !cluster_id
}}> 

# declare policy 
blockchain prepare policy !new_policy
blockchain insert where policy=!new_policy and local=true and master=!ledger_conn
```

9. Get the operator ID

The Operator ID is retrieved and added to the Operator service initialization command (see the Operator init command below).
```anylog
operator_id = blockchain get operator where name=operator1-node and company=!company_name  bring.first [*][id] 
```

10. Create the system database **almgm** and **tsd_info** table

almgm` is the logical database and `tsd_info` is the table that logs the info on data ingestion.
 
```anylog
connect dbms almgm where type=sqlite 

create table tsd_info where dbms=almgm
```
11. Declare the databases hosting the user's data

```anylog
connect dbms !default_dbms where type=sqlite 
```
Note 1: The user tables are created dynamically according to the ingested data.  
Note 2: Repeat the call for each logical database. Note that the physical database (i.e. PSQL or SQLite) can be different for each logical dbms. 

12. (Optional) Partition the data 
```anylog 
partition !default_dbms * using insert_timestamp by 1 day

# view databases declared
get databases

# view partition configurations 
get partitions
```

13. Configure and enable the Operator services

```anylog
# buffer thresholds size and time 
set buffer threshold where time=60 seconds and volume=10KB and write_immediate=true 

# Enable the streamer service - to writes streaming data to files
run streamer

# Enable the Operator ingestion service
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
Details are available in Session II of the basic training - 
[Validating the setup of the nodes in the network](../Session%20II%20(Deployment).md#validating-the-setup-of-the-nodes-in-the-network)

## Insert Data using cURL

* Inserting 100 rows of data via cURL command  
```shell
curl -X PUT 127.0.0.1:32149 \
  -H "command: data" \
  -H "dbms: test" \
  -H "table: ping_sensor" \
  -H "type: json" \
  -H "mode: streaming" \
  -H "User-Agent: AnyLog/1.23" \
  -H "Content-Type: application/json" \
  -d '[{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 1021, "timestamp": "2019-10-11T17:05:53.1820068Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 2021, "timestamp": "2019-10-11T17:15:53.1500091Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 2100, "timestamp": "2019-10-11T17:15:58.1500091Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:25:53.2300109Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:25:58.1530151Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:35:58.126007Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:36:03.1430053Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-11-11T17:46:03.1420135Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:46:08.1420135Z"},{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 221, "timestamp": "2019-10-11T17:56:03.1590118Z"}]'
```

## Sample Queries
```anylog
run client () sql test format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor limit 100"
run client () sql test format = table "select count(*), min(value), max(value) from ping_sensor"
```

## Sample data info commands - on the Operator Node
```anylog 

get streaming # Statistics on the streaming processes. 

# Statistics on SQL Inserts of data to the local databases.
# Note - depending on the setup, it may take a few seconds until data is pushed from the streaming buffers to the databases.
get inserts

# Information on the Operator processes and configuration. 
get operator

# Get the count of rows in the specified table or all tables asigned to the specified database.
get rows count

# Get the count of rows in the specified table or all tables asigned to the specified database, group by table 
get rows count where group = table
```

## Sample tables info commands - On any node
```anylog
get virtual tables          # The list of the logical databases and tables in the network
get data nodes              # The physical nodes that host each logical table
```
