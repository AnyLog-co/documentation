# Background Processes

Background processes are optional processes that if activated, are running using dedicated threads according to the user specifications.

The background processes:

1. A listener for the AnyLog Peer-to-Peer Messaging. Activated by the command: ```run tcp server```
2. A listener for a user REST Request.  Activated by the command: ```run rest server```
3. An automated Operator process. Activated by the command: ```run operator```
4. An automated Publisher process. Activated by the command: ```run publisher```
5. An automated Blockchain Synchronizer. Activated by the command: ```run blockchain sync```
6. A Scheduler process. Activated by the command ```run scheduler```
7. The HA process. Activated by the command ```run ha```
8. A MQTT client process that subscribes to a broker by the command ```run mqtt client```
9. A dedicated thread to flush streaming data to dis. Activated by the command ```run streamer```

These processes are activated on the AL command line.  
The command ***get processes*** provides the list of the running processes.  
The ***show*** command provides options to detail the status of each process. The options of the ***show*** command are detailed in 
[commands](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#get-command).
 

## AnyLog Messaging

A process that receives messages from member nodes in the network. This process makes the node a member in the AnyLog Network.  

Usage:
<pre>
run tcp server [ip] [port] [threads]
</pre>
Explanation:  
[ip] [port] - The process listens for incomming messages on the assigned IP and and Port.
[Threads] - An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 1

Additional information is available at (network configuration)[] 
 
## REST requests

A process that receives REST messages from users and applications which are not members of the network.  
This process receives requests to query data and metada, process the request and replies with the requested information.

Usage:
<pre>
run rest server [ip] [port] where timeout = [timeout] and ssl = [true/false]
</pre>
Explanation:  
[ip] [port] - The process listens for incomming messages on the assigned IP and and Port.  
[timeout] - An optional parameter that determines wait a timeout period in seconds.    
When a REST request is issued, if a respond is not provided within the specified wait time, the request process terminates.  A 0 value means no wait limit and the default value is 20 seconds.  
If ssl is set to True, connection is using HTTPS and authentication requires Certificates.

## Operator Process

A process that places users data in a local database. The Operator identifies JSON files, transforms the files to a structure that can be assigned to a data table and inserts the data to a local database.  
Files ingested are recorded such that it is possible to trace the source data and source device of data readings.

#### Overview
Files with new data are placed in a ***Watch Directory***. The Watch Directory is a designated directory such that every file that is copied to the directory is being processed.  
Processing is determined by the type of the file and by ***Instructions*** if the file is associated with policies that modify the default processing.    
The processing is by mapping the data in each JSON file to SQL Insert Statements that update a local database.

#### The mapping process
The JSON file name follows a convention that uniquely identifies the file and determines the processes that assign the JSON data to a table.  
The file naming convention id detailed at the [metadata section.](https://github.com/AnyLog-co/documentation/blob/master/metadata.md#file-names)
From the file name, the logical database and table names are determined. In addition, the file name optionaly includes the ID of the Mapping Instructions.  
Mapping instructions are detailed in the [mapping data to tables section.](https://github.com/AnyLog-co/documentation/blob/master/mapping%20data%20to%20tables.md)  

#### Recording file ingested
This is an optional process to recod the details of the ingested files.
When JSON files are processed, a local table named **tsd_info** assigned to a database named **almgm** is updated to reflect the list of files processed.  
Interaction with the data maintained by **tsd_info** is by the command ```time file```.  The command provides the functionality to create the table and retrieve the data maintained in the table.  
The information maintained by **tsd_info** is leveraged to trace source data, source devices, and to support the High Availability (HA) processes.

Usage:
<pre>
run operator where [option] = [value] and [option] = [value] ...
</pre>
        
Explanation:  
Monitors new data added to the watch directory and load the new data to a local database.  

Options:  

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| watch_dir  | The directory monitored by the Operator. Files placed on the Watch directory are processed by the Operator.  | !watch_dir  |
| bkup_dir   | The directory location to store JSON and SQL files that were processed successfully.  | !bkup_dir. |
| error_dir   | The directory location to store files containing data that failed processing.  | !error_dir. |
| delete_json   | True/False for deletion of the JSON file if processing is successful.  | false |
| compress_json   | True/False to enable/disable compression of the JSON file if processing is successful.  | false |
| compress_sql   | True/False to enable/disable compression of the SQL file.  | True |
| move_json   | True moves the JSON file to the 'bkup' dir if processing is successful.  | false |
| move_sql   | True moves the SQL file to the 'bkup' dir if processing is successful. The SQL file deleted if move_sql is false.| false |
| dbms_name   | The segment in the file name from which the database name is taken.  | 0 |
| table_name   | The segment in the file name from which the table name is taken.  | 1 |
| limit_tables   | a list of comma separated names within brackets listing the table names to process.  |  |
| craete_table   |  A True value creates a table if the table doesn\'t exists.  | true |
| master_node   |  The IP and Port of a Master Node (if a master node is used).  |  |
| update_tsd_info   | True/False to update a summary table (tsd_info table in almgm dbms) with status of files ingested.  |  |
| distributor   | A True value move the data to the directory assigned to the Distributor process.  | distr_dir  |
| archive   | A True value move the data to the archive directory.  |  |

Example:  
<pre>
run operator where create_table = true and update_tsd_info = true and distributor = true
</pre>

## Publisher Process

A process that identifies JSON files with new data and distributes the files to Operators that are hosting the data.

#### Overview
Files are placed in a ***Watch Directory***. The Watch Directory is a designated directory such that every file that is copied to the directory is being processed.  
The process locates from the blockchain the policies that determine which Operators host the data, designates an Operator to the file and transfers the file to the designated Operator.

#### Assigning an Operator to the data
To determine a target Operator to host the data, the Publisher determines the table associated with the data and considers 2 types of policies:

1) A Policy of type ***distribution***. A distribution policy assigns data from a specifc Publishers or types of Publishers to a particular Operator.
2) If there is no relevant distribution policy, the Publisher considers the Operators that declared support for the table and selects a target Operator.


Usage:  
<pre>
run publisher where [option] = [value] and [option] = [value] ...
</pre>
        
Explanation:  
Monitors new data added to the watch directory and distributes the new data to an Operator.

Options:  

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| watch_dir  | The directory monitored by the Publisher. Files placed on the Watch directory are processed by the Publisher.  | !watch_dir  |
| bkup_dir   | The directory location to store JSON and SQL files that were processed successfully.  | !bkup_dir. |
| error_dir   | The directory location to store files containing data that failed processing.  | !error_dir. |
| delete_json   | True/False for deletion of the JSON file if processing is successful.  | false |
| delete_sql   | True/False for deletion of the SQL file if processing is successful.  | false |
| compress_json   | True/False to enable/disable compression of the JSON file if processing is successful.  | false |
| compress_sql   | True/False to enable/disable compression of the SQL file if processing is successful.  | false |
| company   | The name of the company that owns the file. | The database name determines the company |
| master_node   |  The IP and Port of a Master Node (if a master node is used).  |  |

Example:  
<pre>
run publisher where delete_json = true and delete_sql = true
run publisher where company = anylog and delete_json = true and delete_sql = true
</pre>
In the first example, the name of the database in each JSON file (the first segment in the file name) determines the company that owns the data (the dbms name and the company name are the same).      
In the second example, all the databases are considered as databases of the specified company ('anylog' in the example).


## Blockchain Synchronizer

A process that updates the local copy of the metadata by periodically copying the metadata from a blockchian or a master node.  
This process maintains an updated version of the blockchain data on the local node.  
The source of the metadata depends on the node configuration and can be a blockchain or a master node.  

Usage:  
<pre>
run blockchain sync [options]
</pre>

Options:  

| Option        | Explanation   |
| ------------- | ------------- | 
| source  | The source of the metadata with optional values: 'blockchain' and 'master'.  |
| dest  | The destination of the metadata such as a file (a local file) or a DBMS (a local DBMS). If dest includes both, the local file and the local DBMS are updated. |
| connection  | The connection information that is needed to retrieve the data. For Master, the IP and Port of the master node.  |
| time  | The frequency of the synchronization.  |

Comments:

Examples:  
<pre>
run blockchain sync where source = master and time = 3 seconds and dest = file and connection = !ip_port
run blockchain sync where source = eos and time = 5 minutes and destination = file and destination = dbms
</pre>

Information on Master Node configuration is available at [master node](https://github.com/AnyLog-co/documentation/blob/master/master%20node.md).


## Scheduler Process
 
A process that triggers the scheduled tasks.

#### Overview
Users can declare scheduled tasks on each node of the network. For example, a node can be configured to run a particular report once a day, or to monitor the values generated from a device or a user may want to test the availability of disk space or a size of a database to determine if removal of data is needed.    
These are examples of scheduled tasks that can be declared as periodic processes or as rules which if met, process a task.    
The scheduled tasks can be an AnyLog command like a Query that needs to be periodically executed or multiple commands that are organized as a script file.  
The script can describe the terms that needs to be satisfied (if such are available) and the task to execute.  
When a scheduled task is declared, it is associated with a time interval and assigned to the scheduler. The scheduler will execute the task script in a frequency that depends on the assigned time interval.      

In order to use Scheduled Tasks, a node needs to be configured with a Scheduler running. If a scheduler is running, it is possible to assign tasks to the scheduler.  

### Invoking the scheduler
Usage:
<pre>
run scheduler
</pre>
This command will allow users to declare tasks that will be executed periodically.

### Adding tasks to the scheduler
Usage:
<pre>
schedule [options] command [command to execute]
</pre>
The command ***schedule**** declares a scheduled task that is placed in the scheduler.  
If the scheduler is active, the command will be repeatably executed according to the time specified in the options.  
Options include the following:
  
| Option        | Explanation   |
| ------------- | ------------- | 
| time  | The time intervals for the execution of the task.  |
| name  | A name that is associated with the task. |

   
Examples:
<pre>
schedule time = 10 seconds command system date
schedule time = 1 minute and name = "SQL command" command run client () "sql anylog_test text SELECT max(timestamp) ping_sensor"
</pre>


## HA Process

The HA process is supported by 2 processes:  
1. Data Distributor - Distributing data to Peer Operators. When data is associated to a cluster. it is delivered to all the Operator nodes that are associated with the cluster. When the Operator receives data from a Publisher, the Operator identify the Cluster Members and transfers the data to these Members.  
2. Data Consumer - The Operator participates in a process that continuously validates the completeness of the data set on his local database and if data is missing, it pulls the data from the peer members of the cluster.    

The Distributor Process copies data placed in a distribution directory to the Cluster Members. It manages 2 types of files:
1.  Archived Data - files that include the data of specific partitions. These files were generated using the [backup command](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#backup-command).
2.  Source Data - Files delivered to the node by a Publisher and are maintained on a local database.  
This table summarizes the file types and their destination:

| File Type     | Content   | Copy Destination |
| ------------- | --------- | ---------------- |
| backup | Copy of a data table partition  | Logger Nodes |
| json | New data hosted on the node  | All cluster members |

### Invoking the Data Distributor Process
Usage:
<pre>
run data distributor where distr_dir = [data directory location] and archive_dir = [archive directory location]
</pre>

***[data directory location]*** is the location to retrive the files to be distributed.  
***[archive directory location]*** is the location containing a backup of the source data and the database data (organized by partitions).    

Before the data is copied to a member machine, the data is compressed.  
After the copy, the data is transferred to the backup location on the current node.    

Example:
<pre>
run data distributor where cluster_id = 87bd559697640dad9bdd4c356a4f7421 and distr_dir = !distr_dir
</pre>

### Invoking the Data Consumer Process
The data consumer process considers a date range, all the source data within the date range is validated - if data is missing, it retrieves the data from the cluster member nodes.   
Usage:  
<pre>
run data consumer where cluster_id = [id] and start_date = [date] and end_date = [date]
</pre>
***[id]*** is the ID of the policy declaring the cluster.  
***[date]*** is provided in the following format: YY-MM-DD HH:MM:SS or by subtracting time from the current time, for example: -30d subtracts 30 days from the current date and time.      
start_date must be provided. if end_date is not provided, the current date and time is used.   

Example:  
The example below will test and sync the last 3 days of data.
<pre>
run data consumer where cluster_id = 87bd559697640dad9bdd4c356a4f7421 and start_date = -3d
</pre>


## MQTT Client

This process is explained in the [mqtt](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md) section.

## Streamer Process
A process that pushes streaming data to files.  
When streaming data is added to the internal buffers, the streamer process, based on a time threshold, writes the buffers to files.
Usage
<pre>
run streamer where prep_dir = [path to prep directory] and watch_dir = [path to watch directory] and err_dir = [path to err directory]
</pre>

If prep_dir, watch_dir and err_dir and not specified, the default locations are used.    
To view the default paths used, use the command ```show dictionary```.  
The streaming data thresholds are explained at [Setting and retrieving thresholds for a Streaming Mode](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#setting-and-retrieving-thresholds-for-a-streaming-mode).


