# Background Processes

Background processes are optional processes that if activated, are running using dedicated threads according to the user specifications.

The background processes are issued using an initialization script or on the AnyLog command lime and are detailed below:

| Command               | functionality  |
| --------------------- | ------------| 
| [run tcp server](background%20processes.md#the-tcp-server-process) | A listener for the AnyLog Peer-to-Peer Messaging  |
| [run rest server](background%20processes.md#rest-requests) | A listener for REST Request from users and applications from nodes that are not members of the network |
| [run operator](#operator-process) | A configurable operator process that ingests data to the local tables |
| [run publisher](background%20processes.md#publisher-process) | A configurable publisher process that sends data to operators for processing |
| [run blockchain sync](background%20processes.md#blockchain-synchronizer) | A configurable process to periodically pull from the blockchain platform (or master node) to update a local copy of the metadata |
| [run scheduler](background%20processes.md#scheduler-process) | Initiate a scheduler to periodically monitor state of events and data  |
| [run msg client](message%20broker.md#using-a-message-broker) | Initiate a process that pulls data from MQTT brokers |
| [run smtp client](background%20processes.md#smtp-client) | Initiate an SMTP client allowing emails amd sms messages using the Simple Mail Transfer Protocol (SMTP) |
| [run streamer](background%20processes.md#streamer-process) | Initiate a process to flush streaming data to disk |
| [run data distributor](background%20processes.md#invoking-the-data-distributor-process) | A process that synchronizes data between different operators of the same cluster |
| [run data consumer](background%20processes.md#invoking-the-data-consumer-process) | A process that retrieves data to make the local databases consistent among operators of the same cluster |
| [run message broker](#message-broker) | A process that receives data from 3rd parties platforms using supported protocols |

## View the status of the Background Processes

The following command lists the background processes, their status, and for each process, the main configuration used.
```anylog
get processes
```

Detailed information on each process can be retrieved using the ***get commands***. For example, the following command details the status of the Operator process:
```anylog
get operator
```

The ***get*** command options are detailed in [Get Command](anylog%20commands.md#get-command) section.
 
## Process termination

The command ***exit*** followed by the process name terminates the process.  
**Examples**:
```anylog
exit TCP
exit operator
exit MQTT
exit SMTP
```

## The TCP Server process

A process that listens for incoming messages from peer nodes. When a message is received, the process executes the command contained in the message.    
The IP and ports used by the process are published on the Blockchain and make the node recognizable, searchable and accessible by network peers. 
This process makes the node a member in the AnyLog Network.    

Each node is identified by one or two IP addresses:
* An ***External IP*** - an IP address that uniquely identifies the node and is accessible from the Internet.  
* An ***Internal IP*** - an IP address that uniquely identifies the node on a private network and is accessible from the private network.
A node is configured as follows:
* If both external and internal IP are provided, the node listens to the internal IP (and port).
* If one is provided, the node listens to the provided IP (and port).
* If the ***bind*** parameter is set to False (see details below), the nodes listens to all IPs which are reachable to the node on the specified port.

Usage:
```anylog
run tcp server where external_ip = [ip] and external_port = [port] and internal_ip = [local_ip] and internal_port = [local_port]] and bind = [true/false] and threads = [threads count]
```

Users can validate the configuration of the TCP listeners in all the nodes in the network by issuing the **test network** command. 
See details in the [Test Network](../test%20commands.md#test-network) page.

Options:  

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| external_ip  | An IP on the Internet that identifies the node.  |   |
| external_port  | A port number used to receive REST requests from the external IP. |   |
| internal_ip  | An IP on an internal network that identifies the node.  |   |
| internal_port  | A port number used to receive REST requests from the internal IP. |   |
| bind  |  A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs).  | true  |
| threads  | The number of concurrent threads supporting HTTP requests. | 6  |
 
### IP Configuration
When an AnyLog instance initiates, it identifies the default local IP (an IP accessible from a local network),
 and the external IP (that is accessible from the Internet).
These values are placed in the AnyLog dictionary with the keys ***ip*** and ***external_ip*** respectively.   
When a node starts, the configuration determines the IPs to use, These can be derived from the default values
or by an IP which is determined by the user (and overwrites the default setups).    
The following example starts a TCP server instance using dictionary values:  
```anylog
run tcp server !external_ip 20048 !ip 20048
```

To reconfigure the TCP server process, terminate the existing configuration using the command:
```anylog
exit tcp
```

### The bind parameter
Bind set to ***true*** determines that only one IP address supports incoming messages.  
Bind set to ***false*** determines that all IP addresses with the specified port support incoming messages.   

### Configuring a setup with external IP provided by a router 
If a local IP and Port is specified, the listener process will use the local IP and Port and the 
router connected to the external networks needs to redirect the messages send to the External IP and Port to the Local IP and Port ([Port Forwarding](https://en.wikipedia.org/wiki/Port_forwarding)).  

Additional information is available in the following sections:
* [Network Configuration](network%20configuration.md#network-configuration)
* [Connecting Nodes](examples/Connecting%20Nodes.md)
 
## REST requests

A node in the network can be configured to receive HTTP (or HTTPS) requests from a client (from applications which are not members of the network). 

Usage:
```anylog
run rest server where external_ip = [ip] and external_port = [port] and internal_ip = [local_ip] and internal_port = [local_port] and bind = [true/false] and timeout = 0 and threads = [threads count] and ssl = [true/false] and ca_org = [certificate authority name] and server_org = [sergver organization name]
```

Options:  

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| external_ip  | An IP on the Internet that identifies the node.  |   |
| external_port  | A port number used to receive REST requests from the external IP. |   |
| internal_ip  | An IP on an internal network that identifies the node.  |   |
| internal_port  | A port number used to receive REST requests from the internal IP. |   |
| bind  |  A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs).  | true  |
| timeout  | Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns ***timeout error***. | 20 seconds  |
| threads  | The number of concurrent threads supporting HTTP requests. | 5  |
| ssl  | Boolean value to determine if messages are send over HTTPS with client certificates. | false  |
| ca_org  | The name of the certificate authority. This name needs to match the name in the CA public key file (ca-CA-ORG-public-key.crt)  |   |
| server_org  | The name assigned to the AnyLog node. This name needs to match the name in the node's key files (server-SERVER-ORG-public-key.crt) and (server-SERVER-ORG-private-key.key) |   |

Notes:
* If ssl is set to True, connection is using HTTPS and authentication requires Certificates. These are explained in the section [Using SSL Certificates](authentication.md#using-ssl-certificates).
* The following command provides the info on how the REST server is configured:
    ```anylog
    get rest server info
    ```
* Debugging HTTP command calls:  
    The following command displays (on the AnyLog REST server) the REST command issued by a client.
    ```anylog
    trace level = 1 run rest server 
    ```
    The following command displays (on the AnyLog REST server) the REST command issued by a client including the header and the message body.
    ```anylog
    trace level = 2 run rest server 
    ```
* The ***get rest server info*** command returns the info on how the REST server is configured.  

* To reconfigure the REST server process, terminate the existing configuration using the command:
```anylog
exit rest
```
Additional information is available in the following sections:
* [Network Configuration](network%20configuration.md#network-configuration)
* [Connecting Nodes](examples/Connecting%20Nodes.md)   
* [Using SSL](authentication.md#using-ssl-certificates) 

## Operator Process

A process that adds users data to local databases. The Operator identifies JSON files, transforms the JSON files to SQL files 
and inserts the data to local databases.    

#### Overview
Files with new data are placed in a ***Watch Directory***. The Watch Directory is a designated directory such that every
file that is copied to the directory is being processed.  
Processing maps the JSON's key value pairs to column names and column values of the associate table.
Users can modify the processing by associating ***Instructions Policies*** to the processed files.

#### The mapping process
The JSON file name follows a convention that uniquely identifies the file and determines the processes that assign the JSON data to a table.  
The file naming convention is detailed at the [The file naming convention](../managing%20data%20files%20status.md#the-file-naming-convention) section.
From the file name, the logical database and table names are determined. In addition, the file name optionaly includes the ID of the Mapping Instructions.  
Mapping instructions are detailed in the [mapping data to tables section.](mapping%20data%20to%20tables.md)  

#### Recording file ingested
This is an optional process to recod the details of the ingested files.
When JSON files are processed, a local table named **tsd_info** assigned to a database named **almgm** is updated to 
reflect the list of files processed.  
Interaction with the data maintained by **tsd_info** is by the command ```time file```.  
The command provides the functionality to create the table and retrieve the data maintained in the table.    
The information maintained by **tsd_info** is leveraged to trace source data, source devices, and to support the
High Availability (HA) processes. Info on the ```time file``` is available at the 
[Time File commands](../managing%20data%20files%20status.md#time-file-commands) section.

#### The Operator policy
Every Operator Node is assigned with a policy that provides the operator info and associates the operator with a Cluster policy (see below).      
The following is an example of an operator policy:
```anylog
 {'operator' : {'hostname' : 'operator1',
                'name' : 'cluster1-operator1',
                'ip' : '155.248.209.193',
                'local_ip' : '10.0.0.173',
                'company' : 'AnyLog',
                'port' : 32148,
                'rest_port' : 32149,
                'cluster' : '06f093559c851c6d4c3e950ebc9c5499',
                'loc' : '37.3378,-121.8908',
                'country' : 'US',
                'state' : 'California',
                'city' : 'San Jose',
                'id' : 'd93487bec012c8847bca734bcc31a3a6',
                'date' : '2022-06-06T01:36:02.312181Z',
                'member' : 201,
                'ledger' : 'global'}}]
```

The ***cluster*** key represents an ID of a cluster policy. One or more Operators can be assigned to the same cluster.  
With proper configurations, when data is streamed to an Operator, it will be replicated to all the Operators that share the same cluster.  

#### The Cluster policy

The Cluster policy groups all the Operators that host the same data. In addition, it assigns tables to the cluster such that:  
Data associated with the tables can be hosted on an Operator assigned to the cluster, and if multiple Operators are assigned 
to the cluster, the data will be replicated to each Operator.  
The same table can be assigned to multiple clusters, in that case, the table's data can be partitioned between the clusters.  
The following is an example of a cluster policy:
```anylog
[{'cluster' : {'company' : 'AnyLog',
               'dbms' : 'AnyLog',
               'name' : 'cluster1',
               'id' : '06f093559c851c6d4c3e950ebc9c5499',
               'date' : '2022-06-06T01:36:02.304757Z',
               'status' : 'active',
               'ledger' : 'global'}}]
```

Note that the ***id*** in the cluster policy is the same id referenced by the key ***cluster*** in the [operator policy](#the-operator-policy).

#### Declaring an Operator:
```anylog
run operator where [option] = [value] and [option] = [value] ...
```
        
Explanation:  
Monitors new data added to the watch directory and load the new data to a local database.  

Options:  

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| policy  | The ID of the Operator policy.  |  |
| company  | A company name to be associated with the data.  |  |
| compress_json   | True/False to enable/disable compression of the JSON file if processing is successful.  | true |
| compress_sql   | True/False to enable/disable compression of the SQL file.  | True |
| archive_json   | True moves the JSON file to the 'bkup' dir if processing is successful. The JSON file deleted if archive_json is false. | true |
| archive_sql   | True moves the SQL file to the 'archive' dir if processing is successful. The SQL file deleted if archive_sql is false.| false |
| limit_tables   | a list of comma separated names within brackets listing the table names to process.  |  |
| craete_table   |  A True value creates a table if the table doesn\'t exists.  | true |
| master_node   |  The IP and Port of a Master Node (if a master node is used).  |  |
| update_tsd_info   | True/False to update a summary table (tsd_info table in almgm dbms) with status of files ingested.  |  |
| distributor   | A True value move the data to the directory assigned to the Distributor process.  | distr_dir  |
| archive   | A True value move the data to the archive directory.  |  |


Example:  
```anylog
run operator where policy = !operator_policy and create_table = true and update_tsd_info = true and archive = true and distributor = true and master_node = !master_node
```

To check the status of the Operator process, use the following command:
```anylog
get operator
```
Additional info on the ***get operator*** command is available [here](monitoring%20calls.md#get-operator)

### Operator data archival

#### Archival of the log files:

Data is treated by the Operator as a sequence of log files that are stored in local databases.  
Every log file has a representation as a JSON file. These files are stored in a special archival and are used in the following processes:
1) In the process of High Availability, when data is replicated between nodes.
2) In recovery processes.  
To enable the archival,  set the AnyLog **archive_json** option in the **run operator** command to **true**.

The root of the archive folder is assigned to the key **archive_dir** in the dictionary.  
Use the following command to view the path to the archive root:
```anylog
get !archive_dir
```

The structure of the archival folder is based on partitioning by days (using UTC timezone) and as follows:
* The root is partitioned by years. Every year contains the year's data.
* Every year folder is partitioned to months. Every month contains the month's data.
* A month folder is partitioned to days. Every day contains the files processed by the operator in the given day.

#### Archival of SQL files:
Depending on the configuration, local databases are updated as follows:
1. When an event reaches the AnyLog Node
2. As a collection of multiple (buffered) events.

This behavior is configured by the **set buffer threshold** command - see details in the 
[Setting and retrieving thresholds for a Streaming Mode](adding%20data.md#setting-and-retrieving-thresholds-for-a-streaming-mode) section.  
* **set buffer threshold where write_immediate = false** - Buffers the streaming data.
* **set buffer threshold where write_immediate = true** - No buffering, streaming data updates the databases when the data appears on the node.

If data is buffered (the value for **write_immediate** is **false**), AnyLog generates a file with the insert statement for each event in the buffer.    
Users can archive these files by setting the **archive_sql** flag in the **run operator** command to **true**.    
Note that these files are not used by the system, and are not generated in all use cases. Unless there is a special reason to collect
the SQL files, it is recommended to set **archive_sql** to **false**.  
Note: If **archive_sql** is set to **true**, the data is collected in the folder associated with the **bkup_dir** key.  
Use the following command to view the path to the folder:
```anylog
get !bkup_dir
```

#### View the JSON archived file
The following command returns the list of log files archieved on a particular day:

Usage:
```anylog
get archived files [YYYY-MM-DD]
```
Example:
```anylog
get archived files 2024-01-07
```
#### Delete archived JSON files

Users can configure a node to delete old archived files. This process can be done as a task on the node scheduler -
see details in the [alerts and monitoring](alerts%20and%20monitoring.md) section.    

The command specifies a number of days prior to the command issued day, from which, 
all files in folders from prior days are deleted.   
For example, if days is set as 10, all the data which was processed before 10 days ago, is deleted. 

Note: **Always have a proper backup prior to deleting archived data.**

Usage:
```anylog
delete archive where days = [number of days]
```
Example:
```anylog
delete archive where days = 60
```


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
```anylog
run publisher where [option] = [value] and [option] = [value] ...
```
        
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
```anylog
run publisher where delete_json = true and delete_sql = true
run publisher where company = anylog and delete_json = true and delete_sql = true
```
In the first example, the name of the database in each JSON file (the first segment in the file name) determines the company that owns the data (the dbms name and the company name are the same).      
In the second example, all the databases are considered as databases of the specified company ('anylog' in the example).

To check the status of the Publisher process, use the following command:
```anylog
get publisher
```

## Blockchain Synchronizer

A process that periodically connects to the blockchain platform (or a master node) to update the local copy of the metadata.  
This process maintains an updated version of the blockchain data on the local node such that when the node queries the metadata, it is able to satisfy the query locally.    
The source of the metadata depends on the node configuration and can be a blockchain or a master node.  

Usage:  
```anylog
run blockchain sync [options]
```

Options:  

| Option        | Explanation   |
| ------------- | ------------- | 
| source  | The source of the metadata with optional values: 'blockchain' and 'master'.  |
| dest  | The destination of the metadata such as a file (a local file) or a DBMS (a local DBMS). If dest includes both, the local file and the local DBMS are updated. |
| connection  | The connection information that is needed to retrieve the data. For a Master node, the IP and Port of the master node.  |
|             | If connection info is not provided - the connection info is retrieved from the policy of the Master node.  |
| time  | The frequency of the synchronization.  |
| platform  | The blockchain platform to use (like ethereum).  |


### Example - synchronizing with a blockchain

```anylog
run blockchain sync where source = blockchain and platform = ethereum and time = 30 seconds and dest = file
```


### Example - synchronizing with a master-node  
```anylog
run blockchain sync where source = master and time = 1 minute and dest = file and connection = !ip_port
```

Information on Master Node configuration is available at [master node](master%20node.md).

### Forcing synchronization

The Synchronization process may be configured to minutes or hours. When a node updates a new policy, the node can trigger synchronization using 
the synchronization command (without command options).  
Example:
```anylog
run blockchain sync
```
The command will trigger the synchronization process once, within 10 seconds of the call. The following synchronizations will occur as scheduled, according to the configured time interval.

### Synchronizer status
The **get metadata version** command returns the metadata version ID on the current node.
Usage:
```anylog
get metadata version
```

The **get synchronizer** command provides the synchronizer status with information on the status of the metadata.  

Example:
```anylog
get synchronizer

Status  Sync    Connection     Sync  Metadata Version                 Time          Calls Loads Policies
        Source                 Time                                   Since Update
-------|-------|--------------|-----|--------------------------------|-------------|-----|-----|--------|
Running|master |10.0.0.25:2548|   30|3275c57c0358ea787ef50d2454787335|00:03:21     |    7|    2|      21|
```

The following chart details the information provided:

| Column Name      | Info provided |
| ---------------- | ----------------------------------------- |
| Status           | Indication if the synchronizer is enabled |
| Sync Source      | Blockchain or Master Node as the source for the metadata |
| Connection       | Connection information to the source providing the metadata |
| Sync Time        | The configuration time setup of the periodic sync process |
| Metadata Version | The version of the metadata used by the node |
| Time Since Update | The duration since the last update of the metadata with a new metadata version |
| Calls           | The number of times the metadata version was tested to determine if an update is needed |
| Loads           | The number of times the metadata was updated with the new version |
| Policies         | The number of policies in the current metadata version |

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
```anylog
run scheduler
```
This command will allow users to declare tasks that will be executed periodically.

The details of assigning tasks to the scheduler are available at the section [Alerts and Monitoring](alerts%20and%20monitoring.md#alerts-and-monitoring).

## HA Process

The HA process is supported by 2 processes:  
1. Data Distributor - Distributing data to Peer Operators. When data is associated to a cluster. it is delivered to all the Operator nodes that are associated with the cluster. When the Operator receives data from a Publisher, the Operator identify the Cluster Members and transfers the data to these Members.  
2. Data Consumer - The Operator participates in a process that continuously validates the completeness of the data set on his local database and if data is missing, it pulls the data from the peer members of the cluster.    

The Distributor Process copies data placed in a distribution directory to the Cluster Members. It manages 2 types of files:
1.  Archived Data - files that include the data of specific partitions. These files were generated using the [backup command](anylog%20commands.md#backup-command).
2.  Source Data - Files delivered to the node by a Publisher and are maintained on a local database.  
This table summarizes the file types and their destination:

| File Type     | Content   | Copy Destination |
| ------------- | --------- | ---------------- |
| backup | Copy of a data table partition  | Logger Nodes |
| json | New data hosted on the node  | All cluster members |

### Invoking the Data Distributor Process
Usage:
```anylog
run data distributor where distr_dir = [data directory location] and archive_dir = [archive directory location]
```

***[data directory location]*** is the location to retrive the files to be distributed.  
***[archive directory location]*** is the location containing a backup of the source data and the database data (organized by partitions).    

Before the data is copied to a member machine, the data is compressed.  
After the copy, the data is transferred to the backup location on the current node.    

Example:
```anylog
run data distributor where cluster_id = 87bd559697640dad9bdd4c356a4f7421 and distr_dir = !distr_dir
```

To check the status of the Distributor process, use the following command:
```anylog
get distributor
```

### Invoking the Data Consumer Process
The data consumer process considers a date range, all the source data assigned to time within the date range is validated - if data is missing, it retrieves the data from the cluster member nodes.   
Usage:  
```anylog
run data consumer where start_date = [date] and end_date = [date] and mode = [mode of operation]
```
***[date]*** is provided in the following format: YY-MM-DD HH:MM:SS or by subtracting time from the current time, for example: -30d subtracts 30 days from the current date and time.      
start_date must be provided. if end_date is not provided, the current date and time is used.   
***[mode of operation]*** is "active" (the default) or "suspend". Suspend mode stops the requests for data files from peers. The process resumes when mode is changed to "active".  

Changing the mode of operation can be done dynamically using a ***set command*** as demonstrated below:
```anylog
set consumer mode = suspend
set consumer mode = active
```

Example:  
The example below will test and sync the last 3 days of data.
```anylog
run data consumer where start_date = -3d
```

To check the status of the Consumer process, use the following command:
```anylog
get consumer
```

## The Blobs Archiver

The data archiver is a process that manage blobs data by pushing the blobs (like image, video and sound) to a dedicated 
blobs database or to a dedicated folder (or both).  
Usage:
```anylog
run blobs archiver where bwatch_dir = [data directory location] and blobs_dir = [data directory location] and dbms = [true/false] and file = [true/false] and compress = [true/false]
```

| parameter        | Details   | Default |
| ------------- | ------------- | ------ |
| bwatch_dir  | A directory where the JSON data files with reference to the blobs data are placed  | The value assigned to !bwatch_dir |
| blob_dir  | A directory where blobs data is placed before archived  | The value assigned to !blobs_dir |
| dbms   | A boolean value to determine if blobs database is used | true |
| folder  | A boolean value to determine if file is saved in a folder as f(date) | false |
| compress  | A boolean value to determine if compression is applied | false |

Example:
```anylog
run blobs archiver where dbms = true and folder = true and compress = false
```

To check the status of the Blobs Archiver process, use the following command:
```anylog
get blobs archiver
```


## MQTT Client

The ***MQTT Client*** process provides a mechanism to subscribe to topics of a MQTT broker. When  messages are received,
the client retrieves the message and transforms the incoming messages to data structures that are processed by the node.    
Details on the MQTT Client process are available at the [Using a Message Broker](message%20broker.md#using-a-message-broker) section.

## SMTP Client

The ***SMTP Client*** process initiates an SMTP client facilitating emails and SMS messages using the Simple Mail Transfer Protocol (SMTP).
Sending emails and SMS messages serves to alert and monitor the status of nodes and the data hosted by nodes.  
Details on how emails and SMS messages are triggered ate available in the [Alerts and Monitoring](alerts%20and%20monitoring.md#alerts-and-monitoring) section.

The following command initiates the SMTP client:
```anylog
run smtp client where host = [optional host name] and port = [opttional port] and email = [email address] and password = [email password] and ssl = [true/false]
```
 
| parameter        | Details   | Default |
| ------------- | ------------- | ------ |
| ***host name***  | The connection URL to the email server | "smtp.gmail.com"  |
| ***port***   | The email server port to use |
| ***email***  | The sender email address |  |
| ***password***  | The sender email password |  |
| ***ssl***  | Using an SMTP with secure connection | false |

Example:
```anylog
run smtp client where email = anylog.iot@gmail.com and password = google4anylog
```

Note: To set a Google account for the sender email address - do the following:
* [create a new Google account](https://accounts.google.com/signup)
* Turn [Allow less secure apps to ON](https://myaccount.google.com/lesssecureapps). Be aware that this makes it easier for others to gain access to the account.  


## Streamer Process
A process that flushes streaming data to files.  
When streaming data is added to the internal buffers, the streamer process, based on time and data volume thresholds, writes the buffers to files.
Usage
```anylog
run streamer where prep_dir = [path to prep directory] and watch_dir = [path to watch directory] and err_dir = [path to err directory]
```

If prep_dir, watch_dir and err_dir and not specified, the default locations are used.    
To view the default paths used, use the command ```get dictionary```.  
The streaming data thresholds are explained at [Setting and retrieving thresholds for a Streaming Mode](adding%20data.md#setting-and-retrieving-thresholds-for-a-streaming-mode).

To check the status of the Streamer Process, use the following command:
```anylog
get streaming
```

## Message Broker
An AnyLog node can serve as a message broker to receive data from 3rd parties applications and platforms.  
When data is received in the broker, and depending on how the receiving AnyLog Node is configured, the data can be mapped to the 
destination format and transferred through the [Streamer Process](#streamer-process) to JSON files that can be ingested into a local database on the local node 
or transferred to Operator nodes that will host the data.

Usage:
```anylog
run message broker where external_ip = [ip] and external_port = [port] and internal_ip = [local_ip] and internal_port = [local_port] and bind = [true/false] and threads = [threads count]
```

The ***run message broker*** command configures a process in a listening mode on the specified IP and port.  
Options:  

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| external_ip  | An IP on the Internet that identifies the node.  |   |
| external_port  | A port number used to receive messages from the external IP. |   |
| internal_ip  | An IP on an internal network that identifies the node.  |   |
| internal_port  | A port number used to receive messages from the internal IP. |   |
| bind  |  A bool value that determines if to bind to a specific IP and Port (a false value binds to all IPs).  | true  |
| threads  | The number of concurrent threads supporting HTTP requests. | 6  |

An example of configuring AnyLog as an MQTT message broker is available at the section [Using EdgeX](using%20edgex.md#using-edgex).

To check the status of the Message Broker, use the following command:
```anylog
get local broker
```
Terminating the broker process is with the following command:
```anylog
exit broker
```

