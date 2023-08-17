# Network Setup

This document demonstrates a network setup of 3 nodes:
* A Master Node - to contain the metadata
* An Operator Node - to host the user data
* A Query Node - to issue queries to the network

Note: 
* Configuration is done on the AnyLog command line.    
  
  To make the configuration persistent, place the configuration in a file and call the file on the AnyLog command line.  
    Example:   
    The config file is ***operator.al***, and the call is as follows:
    <pre>
    anylog.exe process !anylog_path/AnyLog-Network/demo/operator1.al
    </pre>
    Or, on the AnyLog CLI issue the following command:
    <pre>
    process !anylog_path/AnyLog-Network/demo/operator1.al
    </pre>

* If AnyLog is installed without a package that creates the environment (like Docker), the default directories can be created using the command:
    <pre>
    create work directories
    </pre>
    To define the root directory for AnyLog, use the following command:
    <pre>
     set anylog home [path to AnyLog root]
    </pre>
  
* This document demonstrates the following:
1. Bring 3 AnyLog Instances UP
2. Configure each node
3. Push data to the Operator
4. Run queries from the Query node

* The commands detailed in this doc include the commands to reset an existing setup to delete existing metadata and data files.

## Frequently used commands to monitor settings:
<pre>
get dictionary         # Default values in the dictionary
get dictionary _dir    # Directory setting
get dictionary ip      # Default ip setting
get connections        # Active listener services (for TCP, REST, and Broker services)
</pre>

## Declaring multiple nodes on the same physical or virtual machine

If the nodes are not isolated (i.e. not in containers and using the same machine), associate a different home path to each node.
For example:
<pre>
set anylog home D:\Node1
</pre>

## Configure the Master Node
<pre>
set authentication off    # Disable users authentication

# networking - if multiple nodes share the IP - use a unique port per node type 
<run tcp server where
    external_ip=!external_ip and external_port=32048 and
    internal_ip=!ip and internal_port=32048 and
    bind=false and threads=6>

<run rest server where
    external_ip=!external_ip and external_port=32049 and
    internal_ip=!ip and internal_port=32049 and
    bind=false and threads=6>

# Use SQLite as system dbms - needed only if Master is configured to satisfy queries
connect dbms system_query where type = sqlite and memory = true  

# use a DBMS to host the blockchain ledger
# For SQLite
connect dbms blockchain where type=sqlite

# or for PSQL 
<connect dbms blockchain where 
   type=psql and 
   ip=127.0.0.1 and 
   port=5432
   user=anylog and
   password=demo>

</pre>

### OPTIONAL - Execute the below commands to delete old blockchain data

<pre>
drop table ledger where dbms = blockchain
create table ledger where dbms = blockchain
blockchain delete local file
</pre>

### Run the below to init a blockchain table on the master node (only once or if blockchain table was deleted)

<pre>
create table ledger where dbms = blockchain                 # Create an internal table
run blockchain sync where source = dbms and time = 30 seconds and dest = file
</pre>

## Configure the Operator Node

<pre>
set authentication off    # Disable users authentication
operator_tcp_port = 7848
operator_rest_port = 7849
master_node = 10.0.0.25:2548     # <-- CHANGE to the TCP IP AND PORT of the MASTER NODE

# networking - if multiple nodes share the IP - use a unique port per node type 
# TCP
<run tcp server where
    external_ip=!external_ip and external_port=32048 and
    internal_ip=!ip and internal_port=32048 and
    bind=false and threads=6>
# REST
<run rest server where
    external_ip=!external_ip and external_port=32049 and
    internal_ip=!ip and internal_port=32049 and
    bind=false and threads=6>

# Use SQLite as system dbms
connect dbms system_query where type = sqlite and memory = true
 
# For AnyLog internal tables: Local management database
# Use SQLite
connect dbms almgm where type = sqlite
# OR Use PostgreSQL
connect dbms almgm where type = psql and user = anylog and ip = 127.0.0.1 and password = demo and port = 5432

# For the user data: 
Use SQLite for lsl_demo tables
connect dbms lsl_demo where type = sqlite
OR use PostgreSQL for lsl_demo tables
connect dbms lsl_demo where type = psql and user = anylog and ip = 127.0.0.1 and password = demo and port = 5432 and autocommit = false

partition lsl_demo ping_sensor using timestamp by 7 days  # Partition the data of the lsl_demo dbms by time

# Sync the blockchain data from the master every 30 seconds
run blockchain sync where source = master and time = 30 seconds and dest = file and connection = !master_node

# Configure the node as operator
run operator where create_table = true and update_tsd_info = true and archive = true and distributor = false and master_node = !master_node
</pre>


### Optional Delete all on Operator previous data (and ignore error messages if Operator does not have data) 

<pre>
time file drop all                            # Drop internal data ingestion monitoring table
create table tsd_info where dbms = almgm      # Create AnyLog Internal Table  
drop table ping_sensor where dbms = lsl_demo  # Drop user table (the table with the user data in this example)
blockchain delete local file                  # Delete the local copy of the metadata
</pre>

### Examples commands to test configuration

<pre>
get connections   # Get the IP and Ports used
get databases     # Get the list of databases configured
get processes     # Show background processes enabled
get dictionary    # Show variables assigned
!blockchain_file  # shows a variable value

run client !master_node get connections  # will show the config on the master
</pre>

### Create a cluster policy and publish on the blockchain

<pre>
# trace level = 3 run tcp server
<cluster = {"cluster" : {
                "company" : "anylog",
                "name"   : "cluster_1"
    }
}>

blockchain insert where policy = !cluster and local = true and master = !master_node
</pre>
Note: Details in the ***blockchain insert*** commands are available [here](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#the-blockchain-insert-command). 

### Create a policy representing the Operator and publish on the blockchain

Setup Variables
<pre>
operator_ip = 24.23.250.144   # <-- Needs to be the extarnal IP on the operator node
operator_port = 7848         # <-- Needs to be the extarnal Port on the operator node
cluster_id = blockchain get cluster where name = cluster_1 bring.first [cluster][id]
!cluster_id   # A print of the Cluster ID registered on the blockchain
</pre>
Define and add the policy
<pre>
< operator = {"operator" : {
    "cluster" : !cluster_id,
    "ip" : !operator_ip,
    "port" : !operator_port.int    }
} >
blockchain insert where policy = !operator and local = true and master = !master_node
</pre>

View the blockchain data
<pre>
blockchain get *
blockchain get operator
</pre>

## Configure the Query Node

<pre>
set authentication off    # Disable users authentication
master_node = 10.0.0.25:2548     # <-- CHANGE to the TCP IP AND PORT of the MASTER NODE

# networking - if multiple nodes share the IP - use a unique port per node type 
# TCP
<run tcp server where
    external_ip=!external_ip and external_port=32048 and
    internal_ip=!ip and internal_port=32048 and
    bind=false and threads=6>
# REST
<run rest server where
    external_ip=!external_ip and external_port=32049 and
    internal_ip=!ip and internal_port=32049 and
    bind=false and threads=6>

# Use SQLite as system dbms (to manage queries)
connect dbms system_query where type = sqlite and memory = true  


 # Sync the blockchain data from the master every 30 seconds
run blockchain sync where source = master and time = 30 seconds and dest = file and connection = !master_node # Sync the blockchain data
</pre>

## Push data to the network (on the Operator Node)
There many ways and interfaces to add data to the network. The simplest is to add a JSON file to the watch directory of the Operator Node.  
View the location of the watch directory using the command: 
<pre>
!watch_dir
</pre>
Note:  
* Use the following file name convention: [database name].[table name].json
* To be aligned with the example use: ***lsl_demo.ping_sensor.json***
* To assign the data to a different database, the database needs to be declared using the command ```connect dbms``:

### the process
* Create a file in a temporary directory
* Copy the file to the watch directory

File data Example

<pre>
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 1021, "timestamp": "2019-10-11T17:05:53.1820068Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 2021, "timestamp": "2019-10-11T17:15:53.1500091Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 2100, "timestamp": "2019-10-11T17:15:58.1500091Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:25:53.2300109Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:25:58.1530151Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:35:58.126007Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:36:03.1430053Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-11-11T17:46:03.1420135Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:46:08.1420135Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 221, "timestamp": "2019-10-11T17:56:03.1590118Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T17:56:08.1440124Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-12-11T18:06:03.1300048Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T18:06:08.1450042Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2020-10-11T18:16:03.1470031Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2020-10-11T18:16:08.1470031Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2020-10-11T18:26:03.1480102Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-11-11T18:26:08.1790008Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 21, "timestamp": "2019-10-11T18:36:08.149002Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 221, "timestamp": "2019-10-11T18:36:13.1350097Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 261, "timestamp": "2019-10-11T18:46:08.1830139Z"}
{"parentelement": "c3bb3b0c-9440-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70ADDu7w0CU6RG0ZdSFZFT0ugYrOFixifG1cDF4vF6HjWSwWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXDc3NyBEQVZJU1xQT1AgUk9PTVxBUEMgU01BUlQgWCAzMDAwfFVQU0JBVFRFUllURU1QRVJBVFVSRQ", "device_name": "APC SMART X 3000", "value": 121, "timestamp": "2019-10-11T18:46:13.152008Z"}
</pre>


### Examples commands to monitor status and state on the operator node

<pre>
get inserts
get operator
get rows count
get rows count where group = table
</pre>


## Run queries on the Query Node (or any other node with system_query database declared)

<pre>
run client () sql lsl_demo format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor limit 100"
run client () sql lsl_demo format = table "select count(*), min(value), max(value) from ping_sensor"
</pre>



