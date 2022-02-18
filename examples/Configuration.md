# Configuration Examples

This document provides configuration examples.

## Starting a node with a configuration file

When an AnyLog node is initiated, it can be called with a command line parameters. The command line parameters 
are one or more AnyLog commands (with multiple commands, each command is enclosed by quotation mark and seperated by the keyword ***and***).  
Usage:
<pre>
python3 user_cmd.py "command 1" and "command 2" ... and "command n"
</pre>


The command ***process*** followed by a path and a file name will process all the commands in the specified file.  
The following example starts an AnyLog node and configures the node according to the commands listed in a file called ***autoexec.al***.

<pre>
python3 user_cmd.py "process !local_scripts\autoexec.al"
</pre>

## Updating the configuration file

Users can update the configuration file using an editor.

Alternatively, users can update the configuration file from the ***Remore CLI***.

### Configuring a node from the Remote CLI

#### Prerequisite: 
* An AnyLog node running.
* The node is configured with a REST connection (configuring a REST connection is detailed in the [Rest Requests](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests) section).

#### Updating the config file
* In the Remote CLI, select the config section.  
* In tne config section update the REST IP and Port of the destination node (the REST IP and Port assigned by the node).
* If authentication is enabled, add username and password in the appropriate fields.
* Select one of the following files from the pull-down menu:
  <pre>
  Autoexec
  Operator
  Publisher
  Query
  Master
  Standalone
  </pre>
* Select ***Load*** to retrieve the config file associated with the selected option.
* Note: Autoexec is the config file currently used. The other options are default options for a target role.
* Update the config file as needed.
* To update the changes, select ***Save***.
* Note: ***Changes are saved to the Autoexec file*** regardless the file selected with the ***Load***.

Restart the AnyLog Node - if the node is initiated as in the [example above](#starting-a-node-with-a-configuration-file), the updated ***Autoexec*** file will determine the configuration.

  
## Configuring data removal and archival

### Configuring Backup, Archive and Removal of data

Multiple options are available to backup, archive and remove old data.

#### Setting a standby node

Declare a second operator node associated with an existing cluster. The second node will be dynamically updated with the
data assigned to the cluster.  
This process is detailed in the [High Availability (HA)](../high%20availability.md#high-availability-ha) section.

#### Archival of data

If an Opertaor node is configured with archive option enabled, data that is streaming to the local database is organized in 
files, compressed, and stored in the archival directory by ingestion date.  
The default archival directory is ```AnyLog-Network\data\archive```  
If needed, these files can be copied to an AnyLog ***watch*** directory to be ingested to a new database.
Details are availabel in [Placing data in the WATCH directory](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#placing-data-in-the-watch-directory) section.

#### Partitioning of data

A table that is managed by AnyLog can be partitioned by time.  
The ***Partition Command*** id detailed [here](../anylog%20commands.md#partition-command).  
Partitions can be dropped by naming the partitions, or by requesting to drop the oldest partition, or by a request to
keep N number of partition, or to drop old partitions as long as disk space is lower than threshold.  
The ***Drop Partition*** command is detailed [here](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#drop-partition-command)

These processes can be placed on the AnyLog scheduler to be repeated periodically.  
For example, a table is partitioned by day and the scheduler is executed daily to remove the oldest partition if disk space 
is under a threshold.

Configuring the scheduler is detailed in the [Monitoring Nodes](../monitoring%20nodes.md#monitoring-nodes) section.

#### Backup Partition

Users can leverage the [archival directory](#archival-of-data) for the data backup.  
Alternatively, uses can actively archive a partition using the [backup table](../anylog%20commands.md#backup-command) 
command (and specify the needed partition).


# Example Configuration File

This is an example configuration file with commonly used configuration options and explanations to the selected options.     
Notes:
 1) The example below declares a ***standalone node***. A standalone node has the roles of a Master Node, an Operator Node and q Query Node. 
 2) The Hash Sign indicates start of a comment and the text that follows is ignored.

#### Disable authentication
If the nodes are trusted, behind a firewall, authentication can be disabled.  
If authentication is enabled, there are different layers that can be leveraged: passwords, signature of messages, and certificates.  
Details are available in the [Users Authentication](../authentication.md#users-authentication) section.

<pre>
set authentication off
</pre>


#### Assign values to variable names
Every node maintains a local dictionary with key value names. Users can associate values to variable names as needed.  
The command ```get dictionary``` shows the variables and their assigned values.  
The command get ```get ![variable name]``` returns the variable value (or, on the CLI the variable name prefixed by exclamation point returns the variable value, i.e. !ip).
<pre>

# Generic Variables

anylog_root_dir=C:\                 # associate the path to the root folder to a variable (NOTE C:\ is the windows version). 
hostname = get hostname             # assign the hostname of the local machine to the key hostname
node_name = anylog-node             # provide a name (preferably unique) to the node. Note, the name would appear on the CLI (i.e.: AL anylog-node > ) 
company_name = "New Company"        # The node owner (company name)

# IP / Port Variables

#external_ip=<external_ip>          # The node may be able to identify the external IP. Otherwise define the external IP. 
#ip=<local_ip>                      # The node may be able to identify the local IP. Otherwise define the local IP. 
anylog_server_port=2148             # The port to use for messages from nodes members of the network.
anylog_rest_port=2149               # The port to use for messages from 3rd parties applications.
master_node = !ip + ":" + !anylog_server_port  # This is declaration for a STANDALONE configuration. Otherwise assign the IP and Port of the master node.
sync_time="30 seconds"              # Synchronize the metadata (from a master node or blockchain) every 30 seconds.

# DBMS Variables

db_user=postgres                    # Use PostgreSQL as a local database (users can use SQLite or both)
db_passwd=postgres
db_ip=!ip
db_port=5432
default_dbms=test                   # !default_dbms will show the value test, to enable the database, the command ```connect dbms``` needs to be called (see below).

# Cluster and Partition Variables

cluster_name = new-cluster
partition_column = timestamp
partition_interval = "1 month"
partition_keep = 6

# Data Monitoring Variables

data_monitoring_table = *
data_monitoring_interval_value = 10
data_monitor_interval = "1 minute"
data_monitor_column = value

</pre>


#### Declare the root folder for the AnyLog files
AnyLog maintains scripts, configurations and data in different folders.  
The default folders structure is detailed in the a [local directory structure](../getting%20started.md#local-directory-structure) section.
The command below determines the path to the root folder (to the AnyLog-Network folder).  
  
<pre>
set anylog home !anylog_root_dir    # Declare the location of the AnyLog root folder. Note that anylog_root_dir was associated with a value above (anylog_root_dir=C:\).
</pre>

#### Create the AnyLog Directories
The command below will create the AnyLog folders (under the AnyLog root folder) if the folders do not exists.
<pre>
create work directories
</pre>


#### Making the node a member of the AnyLog Network
The nodes is configured to initiate a listener on a dedicated IP and Port to receive messages from peer nodes.  
Details are available in the [TCP Server process](../background%20processes.md#rest-requests) section.  

<pre>
run tcp server !external_ip !anylog_server_port !ip !anylog_server_port
</pre>
  
#### Enabling REST request
3rd party applications communicate with members of the network using REST requests.  
The nodes is configured to initiate a listener on a dedicated IP and Port to receive REST requests from 3rd parties applications.  
Details are available in the [REST requests](../background%20processes.md#rest-requests) section.

<pre>
run rest server !ip !anylog_rest_port
</pre>


#### Configuring the local database
The local database is used to store the user data and in some cases system data.  
Each line associates a logical database with a physical database.  
Details are available in the [configuring a local database](../sql%20setup.md#configuring-a-local-database) section.
  

<pre>

</pre>

#### Metadata
The nodes are configured to periodically retrieve the metadata (from a blockchain platform or a master node) and host it locally.   
Details are available in the [Blockchain Synchronizer](../background%20processes.md#blockchain-synchronizer) section.

<pre>
run blockchain sync where source=master and time=!sync_time and dest=file and connection=!master_node
</pre>


#### Initiating the scheduler
AnyLog commands can be placed on the scheduler and be executed periodically.  
The command below initiates a scheduler. Additional information is available in the [Alrts and Monitoring](../alerts%20and%20monitoring.md#alerts-and-monitoring) section.

<pre>
run scheduler 1         # Note: users can define multiple schedulers - 1 indicates scheduler #1. Scheduler #0 is a system scheduler.
</pre>

#### Connect System Database(s) and init system tables.

In this example, there are 2 system databases that are enabled:

1) As the node serves as the Master (the ***standalone*** configuration) - The metadata is hosted in a table called ***ledger*** and the dbms name is ***blockchain***.      
Below, postgreSQL is assigned to maintain the blockchain database and the table ***ledger*** is created (if it does not exist in the database).

2) As the node serves as an Operator - information about the ingested data is hosted in a set of tables in a database called ***almgm***.  
Below, postgreSQL is assigned to maintain the almgm database  and the table ***tsd_info*** is created (if it does not exist in the database).

3) As the node serves as a query node -  SQLite service the ***system_query*** database. This database is used in the query process.
  
<pre>
connect dbms blockchain where type=psql and user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port

is_table = info table blockchain ledger exists                      # Determine if the ***ledger*** table exists
if not !is_table then create table ledger where dbms=blockchain     # Create the ***ledger*** table if ledger table was not created

connect dbms !default_dbms where type=psql and user = !db_user and password = !db_passwd and ip = !db_ip and port = !db_port # Init the test dbms (for user data)
is_table = info table almgm tsd_info exists                         # Determine if the ***tsd_info*** table exists
if !is_table == false then create table tsd_info where dbms=almgm   # Create the ***tsd_info*** table if tsd_info table was not created

connect dbms system_query where type=sqlite

</pre>

#### Declare the node in the metadata layer

Notes: 
1) ***These policies are declared once*** and the below policies declarations can be moved to a dedicated script file that is called once when the node is installed.
2) Details on blockchain commands are available in the [blockchain commands](./blockchain%20commands.md#blockchain-commands) section. 

In a ***standalone*** contiguration the node serves multiple roles. We use a seperate policy for each role.  
If only one role is configured, only the policy that determines the configured role is needed.
 
Get the longitude and latitude of the node (this is an optional step). This info can be added to the policy.

<pre>
info = rest get where url = https://ipinfo.io/json
if !info then loc = from !info bring [loc]
else loc = "0.0, 0.0"
</pre>

***Declare the policy representing Master node*** (if the master policy is not available).  
Use the command ***blockchain get master*** (on the CLI or Remote-CLI) to view the Master Policy. 

<pre>
policy = blockchain get master where name=!node_name and company=!company_name and ip=!external_ip and port=!anylog_server_port
if not !policy then
do new_policy = {"master" : {"hostname": !hostname, "name": !node_name, "ip" : !external_ip, "local_ip": !ip, "company": !company_name, "port" : !anylog_server_port.int, "rest_port": !anylog_rest_port.int, "loc": !loc}}
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!master_node
</pre>

***Declare the policy representing the cluster*** (if not available).  
Note: In the cntext of the network, a cluster represents the group of tables that are managed by an Operator.
If a second Operator is associated with the same cluster, it will maintain a copy of the data.  
If a second operator is assigned to a new cluster, but the cluster is associated with a table that is associted to the first cluster, 
the data will be partitioned to the 2 clusters. 

<pre>

policy = blockchain get cluster where name=!cluster_name and company=!company_name bring.first
do new_policy = {"cluster": {"company": !company_name, "dbms": !default_dbms, "name": !cluster_name, "master": !master_node}}
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!master_node
do policy =  blockchain get cluster where name = !cluster_name and company=!company_name bring.first

cluster_id = from !policy bring [cluster][id]  # The key cluster_id is assigned with the ID of the cluster policy.

</pre>

***Declare the policy representing the Operator node*** (if not available).

<pre>

new_policy = {"operator": {"hostname": !hostname, "name": !node_name, "company": !company_name, "local_ip": !ip, "ip": !external_ip, "port" : !anylog_server_port.int, "rest_port": !anylog_rest_port.int, "loc": !loc, "cluster": !cluster_id}}
if not !cluster_id then new_policy = {"operator": {"hostname": !hostname, "name": !node_name, "company": !company_name, "local_ip" : !ip, "ip": !external_ip, "port" : !anylog_server_port.int, "rest_port": !anylog_rest_port.int, "dbms": !default_dbms, "loc": !loc}}
policy = blockchain get operator where name=!node_name and company=!company_name and ip=!external_ip and port=!anylog_server_port and cluster = !cluster_id
if not !policy then
do blockchain prepare policy !new_policy
do blockchain insert where policy=!new_policy and local=true and master=!master_node

</pre>


#### Data Partitioning
Data that is hosted in the local database can be partioned by date.     
Details are available in the [Partition Command](../anylog%20commands.md#partition-command) section.

<pre>

</pre>

#### Removal of old data
Using the scheduler, a process is triggered periodically and removes old partitions.
The [Drop Partition Command](../anylog%20commands.md#drop-partition-command) is used to remove old partitions.  
In the example below, the command is placed on the scheduler to be executed daily.
 
<pre>

</pre>


