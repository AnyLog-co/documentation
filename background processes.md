# Background Processes

Background processes are optional processes that if activated, are running using dedicated threads according to the user specifications.

The background processes are issued using an initialization script or on the AnyLog command lime and are detailed below:

| Command               | functionality  |
| --------------------- | ------------| 
| [run tcp server](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#the-tcp-server-process) | A listener for the AnyLog Peer-to-Peer Messaging  |
| [run rest server](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests) | A listener for REST Request from users and applications from nodes that are not members of the network |
| [run operator](#operator-process) | A configurable operator process that ingests data to the local tables |
| [run publisher](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#publisher-process) | A configurable publisher process that sends data to operators for processing |
| [run blockchain sync](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#blockchain-synchronizer) | A configurable process to periodically pull from the blockchain platform (or master node) to update a local copy of the metadata |
| [run scheduler](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#scheduler-process) | Initiate a scheduler to periodically monitor state of events and data  |
| [run mqtt client](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md#using-mqtt-broker) | Initiate a process that pulls data from MQTT brokers |
| [run smtp client](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#smtp-client) | Initiate an SMTP client allowing emails amd sms messages using the Simple Mail Transfer Protocol (SMTP) |
| [run streamer](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#streamer-process) | Initiate a process to flush streaming data to disk |
| [run data distributor](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#invoking-the-data-distributor-process) | A process that synchronizes data between different operators of the same cluster |
| [run data consumer](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#invoking-the-data-consumer-process) | A process that retrieves data to make the local databases consistent among operators of the same cluster |
| [run message broker](#message-broker) | A process that receives data from 3rd parties platforms using supported protocols |

## View the status of the Background Processes

The following command lists the background processes, their status, and for each process, the main configuration used.
<pre>
get processes
</pre>

Detailed information on each process can be retrieved using the ***get commands***. For example, the following command details the status of the Operator process:
<pre>
get operator
</pre>

The ***get*** command options are detailed in [Get Command](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#get-command) section.
 
## Process termination

The command ***exit*** followed by the process name terminates the process.  
Examples:
<pre>
exit TCP
exit operator
exit MQTT
exit SMTP
</pre>


## The TCP Server process

A process that listens for incoming messages from peer nodes. When a message is received, the process executes the command contained in the message.    
The IP and ports used by the process are published on the Blockchain and make the node recognizable, searchable and accessible by network peers.      
This process makes the node a member in the AnyLog Network.    

Usage:
<pre>
run tcp server [ip] [port] [local ip] [local port] [threads]
</pre>
Explanation:  
***[ip] [port]*** - The IP and Port of the socket that is in the listening state and accessible by peer nodes in the AnyLog network. These are referred to as the External IP and Port.  
***[local ip] [local port]*** - Optional parameters to indicate an IP and Port that are accessible from a local network.  
***[threads]*** - An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 6.

When an AnyLog instance initiates, it tries to identify the local IP and Port and the IP and Port that is accessible from the Internet.
These values are placed in the dictionary with the keys ***ip*** and ***external_ip*** respectively.  
The following example starts a TCP server instance using these values:  
<pre>
run tcp server !external_ip 20048 !ip 20048
</pre>

If a local IP and Port is specified, the listener process will use the local IP and Port and the 
router connected to the external networks needs to redirect the messages send to the External IP and Port to the Local IP and Port ([Port Forwarding](https://en.wikipedia.org/wiki/Port_forwarding)).  

To reconfigure the TCP server process, terminate the existing configuration using the command:
<pre>
exit tcp
</pre>

Additional information is available in the following sections:
* [network configuration](../network%20configuration.md#network-configuration)
* [Connecting Nodes](./examples/Connecting%20Nodes.md)   
 
## REST requests

A node in the network can be configured to receive HTTP requests from a client (from applications which are not members of the network). 

Usage:
<pre>
run rest server [ip] [port] where timeout = [timeout] and threads = [threads count] and ssl = [true/false]
</pre>

Options:  

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| ip  | The IP supporting the HTTP methods.  |   |
| port  | The port supporting the HTTP methods. |   |
| timeout  | Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns ***timeout error***. | 20 seconds  |
| threads  | The number of concurrent threads supporting HTTP requests. | 5  |
| ssl  | Boolean value to determine if messages are send over HTTPS with client certificates. | false  |

Notes:
* If ssl is set to True, connection is using HTTPS and authentication requires Certificates. These are explained in the section [Using SSL Certificates](https://github.com/AnyLog-co/documentation/blob/master/authentication.md#using-ssl-certificates).
* The following command provides the info on how the REST server is configured:
    <pre>
    get rest server info
    </pre>
* Debugging HTTP command calls:
    The following command displays (on the AnyLog REST server) the REST command issued by a client.
    <pre>
    trace level = 1 run rest server 
    </pre>
    The following command displays (on the AnyLog REST server) the REST command issued by a client including the header and the message body.
    <pre>
    trace level = 2 run rest server 
    </pre>


To reconfigure the REST server process, terminate the existing configuration using the command:
<pre>
exit rest
</pre>

Additional information is available in the following sections:
* [network configuration](../network%20configuration.md#network-configuration)
* [Connecting Nodes](./examples/Connecting%20Nodes.md)   
 
## Operator Process

A process that places users data local databases. The Operator identifies JSON files, transforms the files to a structure 
that can be assigned to data tables and inserts the data local databases.    
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

To check the status of the Operator process, use the following command:
<pre>
get operator
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

To check the status of the Publisher process, use the following command:
<pre>
get publisher
</pre>

## Blockchain Synchronizer

A process that periodically connects to the bloackchain platform (or a master node) to update the local copy of the metadata.  
This process maintains an updated version of the blockchain data on the local node such that when the node queries the metadata, it is able to satisfy the query locally.    
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
| connection  | The connection information that is needed to retrieve the data. For a Master node, the IP and Port of the master node.  |
| time  | The frequency of the synchronization.  |


### Example - synchronizing with a blockchain

<pre>
run blockchain sync where source = blockchain and platform = ethereum and time = 30 seconds and dest = file
</pre>

Information on blockchain configuration is available at [blockchain](https://github.com/AnyLog-co/documentation/blob/master/blockchain.md).

### Example - synchronizing with a master-node  
<pre>
run blockchain sync where source = master and time = 1 minute and dest = file and connection = !ip_port
</pre>

Information on Master Node configuration is available at [master node](https://github.com/AnyLog-co/documentation/blob/master/master%20node.md).

### Forcing synchronization

The Synchronization process may be configured to minutes or hours. When a node updates a new policy, the node can trigger synchronization using 
the synchronization command (without command options).  
Example:
<pre>
run blockchain sync
</pre>
The command will trigger the synchronization process once, within 10 seconds of the call. The following synchronizations will occur as scheduled, according to the configured time interval.   

## Scheduler Process
 
A process that triggers the scheduled tasks.

#### Overview
Users can declare scheduled tasks on each node of the network. For example, a node can be configured to run a particular report once a day, or to monitor the values generated from a device or a user may want to test the availability of disk space or a size of a database to determine if removal of data is needed.    
These are examples of scheduled tasks that can be declared as periodic processes or as rules which if met, process a task.    
The scheduled tasks can be an AnyLog command like a Query that needs to be periodically executed or multiple commands that are organized as a script file.  
When a scheduled task is declared, it is associated with a time interval and assigned to the scheduler. The scheduler will execute the task script in a frequency that depends on the assigned time interval.      

In order to use Scheduled Tasks, a node needs to be configured with a Scheduler running. If a scheduler is running, it is possible to assign tasks to the scheduler.  

### Invoking the scheduler
Usage:
<pre>
run scheduler
</pre>
This command will allow users to declare tasks that will be executed periodically.

The details of assigning tasks to the scheduler are available at the section [Alerts and Monitoring](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring).

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

To check the status of the Distributor process, use the following command:
<pre>
get distributor
</pre>

### Invoking the Data Consumer Process
The data consumer process considers a date range, all the source data assigned to time within the date range is validated - if data is missing, it retrieves the data from the cluster member nodes.   
Usage:  
<pre>
run data consumer where cluster_id = [id] and start_date = [date] and end_date = [date] and mode = [mode of operation]
</pre>
***[id]*** is the ID of the policy declaring the cluster. The default value is the cluster ID assigned to the current node.  
***[date]*** is provided in the following format: YY-MM-DD HH:MM:SS or by subtracting time from the current time, for example: -30d subtracts 30 days from the current date and time.      
start_date must be provided. if end_date is not provided, the current date and time is used.   
***[mode of operation]*** is "active" (the default) or "suspend". Suspend mode stops the requests for data files from peers. The process resumes when mode is changed to "active".  

Changing the mode of operation can be done dynamically using a ***set command*** as demonstrated below:
<pre>
set consumer mode = suspend
set consumer mode = active
</pre>

Example:  
The example below will test and sync the last 3 days of data.
<pre>
run data consumer where cluster_id = 87bd559697640dad9bdd4c356a4f7421 and start_date = -3d
</pre>

To check the status of the Consumer process, use the following command:
<pre>
get consumer
</pre>

## MQTT Client

The ***MQTT Client*** process provides a mechanism to subscribe to topics of a MQTT broker. When  messages are received,
the client retrieves the message and transforms the incoming messages to data structures that are processed by the node.    
Details on the MQTT Client process are available at the [Using MQTT Broker](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md#using-mqtt-broker) section.

## SMTP Client

The ***SMTP Client*** process initiates an SMTP client facilitating emails and SMS messages using the Simple Mail Transfer Protocol (SMTP).
Sending emails and SMS messages serves to alert and monitor the status of nodes and the data hosted by nodes.  
Details on how emails and SMS messages are triggered ate available in the [Alerts and Monitoring](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring) section.

The following command initiates the SMTP client:
<pre>
run smtp client where host = [optional host name] and port = [opttional port] and email = [email address] and password = [email password] and ssl = [true/false]
</pre>
 
| parameter        | Details   | Default |
| ------------- | ------------- | ------ |
| ***host name***  | The connection URL to the email server | "smtp.gmail.com"  |
| ***port***   | The email server port to use |
| ***email***  | The sender email address |  |
| ***password***  | The sender email password |  |
| ***ssl***  | Using an SMTP with secure connection | false |

Example:
<pre>
run smtp client where email = anylog.iot@gmail.com and password = google4anylog
</pre>

Note: To set a Google account for the sender email address - do the following:
* [create a new Google account](https://accounts.google.com/signup)
* Turn [Allow less secure apps to ON](https://myaccount.google.com/lesssecureapps). Be aware that this makes it easier for others to gain access to the account.  


## Streamer Process
A process that flushes streaming data to files.  
When streaming data is added to the internal buffers, the streamer process, based on time and data volume thresholds, writes the buffers to files.
Usage
<pre>
run streamer where prep_dir = [path to prep directory] and watch_dir = [path to watch directory] and err_dir = [path to err directory]
</pre>

If prep_dir, watch_dir and err_dir and not specified, the default locations are used.    
To view the default paths used, use the command ```get dictionary```.  
The streaming data thresholds are explained at [Setting and retrieving thresholds for a Streaming Mode](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#setting-and-retrieving-thresholds-for-a-streaming-mode).

To check the status of the Streamer Process, use the following command:
<pre>
get streaming
</pre>

## Message Broker
An AnyLog node can serve as a message broker to receive data from 3rd parties applications and platforms.  
When data is received in the broker, and depending on how the receiving AnyLog Node is configured, the data can be mapped to the 
destination format and transferred through the [Streamer Process](#streamer-process) to JSON files that can be ingested into a local database on the local node 
or transferred to Operator nodes that will host the data.

Usage:
<pre>
run message broker [ip] [port] [local ip] [Local port] [threads]
</pre>

The ***run message broker*** command configures a process in a listening mode on the specified IP and port.  
* The first pair of IP and Port that are used by a listener process to receive messages from members of the network.  
* The second pair of IP and Port are optional, to indicate the IP and Port that are accessible from a local network.  
* threads - an optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 6.  

An example of configuring AnyLog as an MQTT message broker is available at the section [Using EdgeX](https://github.com/AnyLog-co/documentation/blob/master/using%20edgex.md#using-edgex).

To check the status of the Message Broker, use the following command:
<pre>
get broker
</pre>

