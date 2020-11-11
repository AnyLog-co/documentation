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

These processes are activated on the AL command line.  
The command ***show processes*** provides the list of the running processes.  
The ***show*** command provides options to detail the status of each process. The options of the ***show*** command are detailed in 
[commands](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#show-command).
 

## AnyLog Messaging

A process that receives messages from member nodes in the network. This process makes the node a member in the AnyLog Network.  

Usage:
<pre>
run tcp server [ip] [port] [threads]
</pre>
Explanation:  
[ip] [port] - The process listens for incomming messages on the assigned IP and and Port.
[Threads] - An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 1

 
## REST requests

A process that receives REST messages from users and applications which are not members of the network.  
This process receives requests to query data and metada, process the request and replies with the requested information.

Usage:
<pre>
run rest server [ip] [port] [timeout]
</pre>
Explanation:  
[ip] [port] - The process listens for incomming messages on the assigned IP and and Port.  
[timeout] - An optional parameter that determines wait a timeout period in seconds.    
When a REST request is issued, if a respond is not provided within the specified wait time, the request process terminates.  A 0 value means no wait limit and the default value is 20 seconds.

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
| delete_sql   | True/False for deletion of the SQL file if processing is successful.  | false |
| compress_json   | True/False to enable/disable compression of the JSON file if processing is successful.  | false |
| compress_sql   | True/False to enable/disable compression of the SQL file if processing is successful.  | false |
| move_json   | True moves the JSON file to the 'bkup' dir if processing is successful.  | false |
| move_sql   | True moves the SQL file to the 'bkup' dir if processing is successful.  | false |
| dbms_name   | The segment in the file name from which the database name is taken.  | 0 |
| table_name   | The segment in the file name from which the table name is taken.  | 1 |
| limit_tables   | a list of comma separated names within brackets listing the table names to process.  |  |
| craete_table   |  A True value creates a table if the table doesn\'t exists.  | true |
| master_node   |  The IP and Port of a Master Node (if a master node is used).  |  |
| update_tsd_info   | True/False to update a summary table (tsd_info table in almgm dbms) with status of files ingested.  |  |

Example:  
<pre>
run operator where create_table = true and dbms_name = file_name[0] and table_name = file_name[1] and source = file_name[2] and compress_sql = true and compress_json = true and update_tsd_info = true
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
| dbms_name   | The segment in the file name from which the database name is taken.  | 0 |
| table_name   | The segment in the file name from which the table name is taken.  | 1 |
| master_node   |  The IP and Port of a Master Node (if a master node is used).  |  |

Example:  
<pre>
run publisher where dbms_name = file_name[0] and table_name = file_name[3] and delete_json = true and delete_sql = true
</pre>

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
The command ***schedule**** declares a scheduled command that is placed in the scheduler.  
If the scheduler is active, the command will be repeatably executed according to the time specified in the options.
   
Examples:
<pre>
schedule time = 10 seconds command system date
schedule time = 1 minute command run client () "sql anylog_test text SELECT max(timestamp) ping_sensor"
</pre>


## HA Process
 
Delivers data files processed by the local node to a standby node or nodes.  
When an operator ingests data, the process records the hash values of the files ingested.
    
If HA is activated, every file processed is transferred to the standby nodes. 
Users can enable a synchronization process to validate that all the data on a particular node is available on the standby nodes and if differences are found, the process will transfer the needed data to make the nodes identical.

## MQTT Client

This process initiates a client that subscribes to a list of topics registered on a MQTT broker.

<pre>
run mqtt client where [list of options]
</pre>
The list of options are represented by 'key' = value' and separated by 'and'.

Options:  
| Option        | Explanation   |
| ------------- | ------------- | 
| broker  | The url or IP of the broker. |
| port  | The port of the broker. The default value is 1883.|
| topic  | The dbms and table to use for each topic using the following format[dbms name].[table name].[topic].[QoC] |

***QoC*** - The Quality of Service:  
0 - No guarantee of delivery. The recipient does not acknowledge receipt of the message.  
1 - Guarantees that a message is delivered at least one time to the receiver, but the same message may be delivered multiple times.  
2 - The highest level of service. Guarantees that each message is received only once by the client.  
 
Example:  
The example below connects to a broker to pull data assigned to a topic ***ping*** and associate the data to the DBMS ***lsl_demo*** and the ***ping_sensor*** table.
<pre>
run mqtt client where broker = "mqtt.eclipse.org" and topic = lsl_data.ping_sensor.ping.2
</pre>


 

