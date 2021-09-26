# Network Setup

This document demonstrates a network setup of 3 nodes:
* A Master Node - to contain the metadata
* An Operator Node - to host the user data
* A Query Node - to issue queries to the network

Note: 
* Configuration is done on the AnyLog command line. To make the configuration persistent, place the configuration in a file and call the file on the AnyLog command line.  
    Example: 
    The config file is ***operator.al***, and the call is as follows:
    <pre>
    D:\AnyLog-Code\AnyLog-Network\source\cmd\user_cmd.py process !anylog_path/AnyLog-Network/demo/operator1.al
    </pre>
    Or, on the AnyLog CLI issue the following command:
    <pre>
    !anylog_path/AnyLog-Network/demo/operator1.al
    </pre>
* If AnyLog is installed without a package that creates the enviornment (like Docker), the default directories can be created using the command:
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


## Configure the Master Node
<pre>
set authentication off    # Disable users authentication
run tcp server !ip 2548   # The connection to the network nodes
run rest server !ip 2549  # Enable REST calls
connect dbms sqlite !db_user !db_port  system_query memory  # Use SQLite as system dbms
connect dbms sqlite !db_user !db_port blockchain            # use SQLite for the blockchain ledger
run blockchain sync where source = dbms and time = 30 seconds and dest = file # Copy the blockchain data to a file every 30 seconds
</pre>

### Execute the below commands to delete old blockchain data

<pre>
drop table ledger where dbms = blockchain
create table ledger where dbms = blockchain
blockchain delete local file
</pre>

### Run the below to init a blockchain table on the master node (only once or if blockchain table was deleted)

<pre>
create table ledger where dbms = blockchain                 # Create an internal table
</pre>


<pre>
</pre>

# Configure the Operator Node

<pre>
set authentication off    # Disable users authentication
operator_tcp_port = 7848
operator_rest_port = 7849
master_node = 10.0.0.25:2548     # <-- CHANGE to the TCP IP AND PORT of the MASTER NODE

run tcp server !external_ip !operator_tcp_port !ip !operator_tcp_port # The connection to the network nodes
run rest server !ip !operator_rest_port # Enable REST calls

connect dbms psql anylog@127.0.0.1:demo 5432 system_query # Use SQLite as system dbms
connect dbms psql anylog@127.0.0.1:demo 5432  lsl_demo  # use Postgres for lsl_demo tables
connect dbms sqlite anylog@127.0.0.1:demo 5432 almgm # Local management database

partition lsl_demo ping_sensor using timestamp by 7 days  # Partition the data of the lsl_demo dbms by time

# Sync the blockchain data from the master every 30 seconds
run blockchain sync where source = master and time = 30 seconds and dest = file and connection = !master_node

# Configure the node as operator
run operator where create_table = true and update_tsd_info = true and archive = true and distributor = true and master_node = !master_node
</pre>


### Delete all on Operator previous data (ignore error messages if Operator does not have data) 

<pre>
time file drop all
create table tsd_info where dbms = almgm
drop table ping_sensor where dbms = lsl_demo
drop table ping_sensor where dbms = anylog
drop table new_sensor where dbms = lsl_demo
blockchain delete local file
</pre>

### Examples commands to test configuration

<pre>
get connections   # Get the IP and Ports used
get databases     # Get the list of databases configured
get processes     # Show background processes enabled
get dictionary    # Show variables assigned
!blockchain_file  # shows a variable value
help get          # shows the get options

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

run client !master_node blockchain push !cluster
run blockchain sync   # Force blockchain sync now
blockchain wait where command = "blockchain get cluster where name = cluster_1" # wait for the local update
</pre>

### Create a policy representing the Operator and publish on the blockchain
