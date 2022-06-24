# AnyLog Commands

## Overview

Commands can be issued in 2 ways:  
a) Using the AnyLog command line - AnyLog instances provide a command line interface. Users can issue commands using the command line interface.  
All the available commands are supported by the command line interface.  
b) Using a REST API - A subset of the commands are supported using a REST API.
The REST API is the main method to issue queries that evaluate data maintained by members of the network. 

## The AnyLog Command Line

The AnyLog command line is a text interface providing the ability to manage how compute instances operate, process data and metadata.  
The commands are listed and detailed below. The help command provides an interactive help on the particular commands including usage examples.    
Commands can be organized in a file and processed using the command ```script``` followed by the path and name of the script.  
Commands organized in a script can be also executed using the command ```thread```. The thread command dedicates a thread to execute the script commands and it is unusably the case for a sequence of commands that are continuously running.    
Commands can be also placed on the blockchain, identified with a unique ID and processed by calling the ID using the command ```policy```.  
This method of organizing commands allows to impact and modify behaiviour of running nodes by declaring policies on the blockchain.  
   

#### The help command

The command: ```help``` lists all the coommand options.
The command ```help``` followed by a specific command, provides information and examples on the specific command.  
Example: ```help blockchain```  provides information and command options to the command ```blockchain```.

#### Scripts, Threads and Policies

These are different methods to execute commands on the command line.

##### script
The command ```script``` folowed by a path and file name will execute all the script commands.

##### thread
The command ```thread``` folowed by a path and file name will execute all the commands that are specified in the script file.  
The command ```thread``` allocates a dedecated thread to execute the commands. This option supports commands that are executed continuously.    
An example would be a script that waits for files to be generated and process the files when identified. When the processing of the identified files is completed, the process restarts to wait for new data files. 
    
##### policy
A set of commands that are placed on the blockchhain.
When the policy is called, the commands associated with the policy are executed.  
Policies allows to initiate and modify processes on nodes by publishing processes on the blockchain.   
Policies impact one or more nodes vs. scripts which are private and maintained on the local drive of each node. 

# The node dictionary

Every node maintains a dictionary that associates keys with values.   
When a node is initialized, some keys are preassigned with values. Users and processes can assign new values
to new or existing keys.  
Users and processes can use the keys as representatives of the values by prefixing the key with an exclamation point.   
Assigning a value to a key is done with the following calls:
<pre>
[key] = [value]
</pre>
Or use the set command:
<pre>
set [key] = [value]
</pre>

The following example assigned a path to the key dbms_dir:
<pre>
dbms_dir = D:\AnyLog-Code\AnyLog-Network\data\dbms
</pre>

Use the following command to delete an assignment:
<pre>
[key] = ""
</pre>
Or
<pre>
set [key] = ""
</pre>


To retrieve the value assigned to a key use exclamation point prefixed to the key name.
<pre>
![key]
</pre>
Or use the get command:
<pre>
get ![key]
</pre>

The following example returns the path string assigned to the key ***dbms_dir***:
<pre>
!dbms_dir
</pre>

The following command retrieves all keys and values from the dictionary:
<pre>
get dictionary
</pre>


# List of Commands:
| Commands        | 
| ------------- |
| [alerts](https://https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring) |
| [backup](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#backup-command) | 
| [blockchain](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md) | 
| [drop partition](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#drop-partition-command) | 
| [file](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md) | 
| [get](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#get-command) |
| [partition](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#partition-command) | 
| [rest](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#rest-command) | 
| [set](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#set-command) | 
| [sql](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#sql-command) | 
| [test](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#sql-command) | 
| [time file](https://github.com/AnyLog-co/documentation/blob/master/managing%20data%20files%20status.md#time-file-command) | 


## Set Command

The ***set*** commands allows to set variables and configuration parameters.  

Options:  

| Option        | Explanation  |
| ------------- | ------------| 
| [set query mode](#set-query-mode)  | Setting execution instructions to the issued queries. |
| [set query log on/off](https://github.com/AnyLog-co/documentation/blob/master/logging%20events.md#the-query-log) | Enable/Disable a log to record the executed queries. |
| [set query log profile [n] seconds](https://github.com/AnyLog-co/documentation/blob/master/logging%20events.md#the-query-log)  | Applying the Query Log to queries with execution time higher than threshold.  |
| set rest log on/off | Enable/Disable a log to record the processed REST commands. The log is retrieved using the 'get rest log' command. |
| set debug [on/off]  | Displays the executed commands processed in scripts. |
| set mqtt debug [on/off]  | Displays the MQTT messages and their processing status. |
| set debug interactive  | Waits for the user interactive command \'next\' to move to the next command. |
| set threads pool [n]  | Creates a pool of workers threads that distributes query processing to multiple threads. |
| set echo queue [on/off]  | Creates a queue to contain echo commands and messages. |
| set authentication [on/off]  | Enable / Disable user and message authentication. Default value is ON. |
| set encryption [on/off]  | Enable / Disable encryption of TCP messages. Default value is OFF. |
| set compression [on/off]  | Enable / Disable compression of data messages. Default value is OFF. |
| set local password = [password]  | Provide a password to protect sensitive information that is kept on the node (like private keys and users passwords). See also [Using passwords](https://github.com/AnyLog-co/documentation/blob/master/authentication.md#using-passwords).|
| set private password = [password] [in file] | Provide the password of the private key with an optional command text [in file] to keep encrypted copy on the filesystem. See also [Using passwords](https://github.com/AnyLog-co/documentation/blob/master/authentication.md#using-passwords).|
| set anylog home [absolute path]  | Declare a path to the AnyLog data files. |
| set traceback [on/off]  | Print the code path with every call to the error log. If text is specified, stacktrace is added only if the text is a substring in the error message",|
| set reply ip = [ip/none]  | Set the IP address that for a reply message. |
| set consumer mode = [mode]  | Change the consumer mode of operation. Optional modes are: "active" and "suspend". |
| set rest timeout [time and time-unit]  |  Sets a time limit for a rest reply. If limit is 0, the process will wait for a reply without timeout. |
| [set data distribution](#set-data-distribution) where ... |  Define how data is distributed to the storage nodes. |


#### Set query mode

The query mode sets a cap on query execution at the Operator Node by setting a limit on execution time or data volume transferred or both.
  
Params options can be the following:

| param        | Explanation  |
| ------------- | ------------| 
| timeout     | limit execution on each server by the provided time limit. | 
| max_volume  | limit data volume returned by each participating operator. |
| send_mode   | use \'all\' to return an error if any of the participating servers is not connected. |
|             | use \'any\' to send the query only to the connected servers. |
|             | The default value is \'all\'. |
| reply_mode  | use \'all\' to return an error if any of the participating servers did not reply after timeout. |
|             | use \'any\' to return the query results using the available data after timeout. |
|             | The default value is \'all\'. |

#### Set data distribution

Define the destination of data based on the database and table assigned to the data.   
Force a publisher to a defined distribution of the data.  
Usage:
<pre>
set data distribution where dbms = [dbms_name] and table = [table_name] and dest = [ip:port]
</pre>
dbms - the database associated with the data  
table - the table associated with the data  
dest - the destination ip and port (one or more)  

Example:
<pre>
set data distribution where dbms = lsl_demo and table = * and dest = 10.12.32.148:2048 and dest = 10.181.231.18:2048
</pre>

Removal of an existing distribution is by adding the keyword and value: ```remove = true```.  
Usage:
<pre>
set data distribution where dbms = [dbms_name] and table = [table_name] and remove = true
</pre>
Example:
<pre>
set data distribution where dbms = lsl_demo and table = ping_sensor and remove = true
</pre>

View the distribution definitions using the command:
<pre>
get  data distribution
</pre>

## Reset Command

The ***reset*** commands allows to reset variables and configuration parameters.  

Options:  

| Option        | Explanation  |
| ------------- | ------------| 
| reset [event/error/file/query] log | Deletes the log entries in the specified file  |
| reset query timer | Reset the query timer. | 
| reset echo queue  | Reset the queue. |
| reset echo queue where size = [n] | Resets the queue and sets the size of the queue to maintain the last n messages (between 1 and 100). |
| reset reply IP | Assign the reply IP to be the Source IP. Details are available at [Network Configuration](https://github.com/AnyLog-co/documentation/blob/master/network%20configuration.md#reset-the-reply-ip-to-the-source-ip).|


## Get Command

The get command provides information on hardware state and status, files, resources and security of the node. 

Options:  

| Option        | Information provided  |
| ------------- | ------------| 
| [get event log](https://github.com/AnyLog-co/documentation/blob/master/logging%20events.md#the-event-log)  | Records the Last commands processed by the node. | 
| [get error log](https://github.com/AnyLog-co/documentation/blob/master/logging%20events.md#the-error-log)  | Records the last commands that returned an error. Adding a list of keywords narrows the output to error events containing the keywords.|
| [get file log](#get-logged-instances)  | Records the last data files processed by the node. |
| [get rest log](#get-logged-instances)  | Records the REST calls returning an error. Can record all REST calls by setting "set rest log on" |
| [get query log](https://github.com/AnyLog-co/documentation/blob/master/logging%20events.md#the-query-log)  | The last queries processed by the node. Enable this log using the ***set query log*** command|
| [get processes](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#the-get-processes-command)| The list of background processes. More details are available in [background processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md).|
| get members status | Get status of members nodes that are messaged by this node. |
| get synchronizer | Information on the blockchain synchronize process. |
| [get operator](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-operator) | Information on the Operator processes. |
| get publisher | Information on the Publisher processes. |
| get distributor | With HA enabled, information on the distributions of source files to cluster members. |
| get consumer | With HA enabled, information on pulling source files from cluster members. |
| [get streaming](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-streaming) | Information on streaming data from REST and MQTT calls. |
| get cluster info | Information on the cluster supported by the node including Cluster ID, Member ID and Operators supporting the cluster. |
| get tsd info [table name] | Information on the synchronization status between the cluster members. |
| [get rest calls](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-rest-calls) | Statistical information on the REST calls. |
| [get rest server info](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#rest-server-configuration) | Information on the REST server configuration. |
| [get msg clients](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-msg-clients) | Information on clients subscribed to topics. |
| get msg brokers | Information on message brokers and the topics subscribed with each broker. |
| get broker | Information on the Message Broker. |
| [get status](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#the-get-status-command)  | Replies with the string 'running' if the node is active. Can be extended to include additional status information | 
| get connections | The list of TCP and REST connections supported by the node. |
| get machine connections | The system-wide socket connection. Users can detail specific port: ```get machine connections where port = [port]```|
| get platforms | The list connected blockchain platforms. |
| [get dictionary](monitoring%20nodes.md#the-get-dictionary-command) | The list of the variable names and their assigned values. |
| [get env var](monitoring%20nodes.md#the-get-env-var-command) | The environment variables keys and values. |
| get databases  | The list of databases managed on the local node. |
| get partitions | Information on how data is partitioned on the local databases. |
| get partitions where dbms = [dbms_name] and table = [table name] | Partition details on a specific table. |
| get query mode | The query param variables assigned by the command ***set query mode***. |
| [get workers pool](#get-pools-info) | Details the status of query workers assigned by the command ***set threads pool [n]***. The value 0 means thread in rest and 1 processing data.|
| [get tcp pool](#get-pools-info) | Details the number TCP workers thread that execute peer command. The number of threads is set by the command ***run tcp server***. |
| [get rest pool](#get-pools-info) | Details the number REST workers thread that execute REST calls. The number of threads is set by the command ***run rest server***. |
| get threads | The list of the threads executing users scripts. |
| get scheduler [n]| Information on the scheduled tasks. [n] - an optional ID for the scheduler, the default value is 1, 0 is the system scheduler.|
| get hostname | The name assigned to the node. | 
| get version | The code version. |
| get git [version/info] [path to github root] | ***git version*** returns the first 5 digits of the commit used, ***git info*** provides additional information. If path is not specified, the dictionary variable ***!anylog_path*** is used to identify the ***AnyLog-Network*** directory.|
| get queries time | Statistics on queries execution time. The statistics is configurable by the command ***set query log profile [n] seconds***  |
| get watch directories | The list of the Watch directories on the node. |
| get inserts | Statistics on SQL Inserts of data to the local databases. |
| get database size [database name] | The size of the named database in bytes. |
| get node id | Returns a unique identifier of the node. |
| get hardware id | Returns a unique identfier of the hardware. |
| [get servers](#get-servers) | Retrurn info on the the servers supporting the table. |
| get tables for dbms [dbms name] | The list of tables of the named database and where the table is declared (local database and/or blockchain) |
| get table [exist status/local status/blockchain status/rows count/complete status] where name = table_name and dbms = dbms_name | Returns information on the specified table |
| get views for dbms [dbms name] | The list of views of the named database. |
| get files in [dir name] where type = [file type] and hash = [hash value] | The list of files in the specified dir that satisfy the optional filter criteria. |
| get file timestamp [file path and name] | Get the file's timestamp. |
| get error [error number] | Get the error text for the error number. |
| get echo queue | Get the queue with the ***echo*** commands and messages. |
| get files [directory path] | Details the files in the specified directory. |
| get directories [directory path] | Details the sub-directories in the specified directory. |
| get json file structure | Details the convention for JSON file name. |
| get users | The list of users declared using the command ```id add user ...```. |
| get reply ip | Retrieve the IP address for reply messages. |
| get archived files [YYYY-MM-DD] | List the files archived on the provided date. |
| get size [dir name] [YYYY-MM-DD] | List the size of a directory including sub-directories. |
| get access [path and file name or directory name] | Get the access rights to the provided file or directory. |
| get data nodes | Details the Operators that host each table's data. |
| [get rows count](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#monitoring-data-commands) | Details the number of rows in all or specified tables. Details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#monitoring-data-commands).|
| [get query execution](https://github.com/AnyLog-co/documentation/blob/master/profiling%20and%20monitoring%20queries.md#retrieving-the-status-of-queries-being-processed-on-an-operator-node) | Provides the status of queries being executed on an Operator node.|
| get timezone info | Get the timezone on the local machine. |
| get datetime [date-time function](https://github.com/AnyLog-co/documentation/blob/master/queries.md#get-datetime-command) | Translate a date-time function to the date-time string. |

#### Monitoring node status options:

| Option        | Information provided  |
| ------------- | ------------| 
| get disk [usage/total/used/free] [path]  | Disk statistics about the provided path. |
| get platform info | Info on the type and version of the OS, node name and type of processor. |
| get memory info | Info on the memory of the current node. The function depends on psutil installed. |
| get cpu info | Info on the CPU of the current node.  The function depends on psutil installed. |
| get ip list | The list of IP addresses available on the node. |
| get cpu temperature | The CPU temperature. |
| get node info [options] | Different statistics on the node. |
| get monitored | Retrieve the list of topics monitored by an aggregator node. Details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#organizing-nodes-status-in-an-aggregator-node). |
| get monitored [topic] | Retrieve monitored info on a specific topic from an aggregator node. Details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#organizing-nodes-status-in-an-aggregator-node). |


Additional information is available at [monitoring nodes](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#monitoring-nodes).

#### Security and encryption related options:  

| Option        | Information provided  |
| ------------- | ------------| 
| get public key  | The node\'s public key. | 
| get public key using keys_file = [file name] | Retrieves the public key from the specified file. |
| get permissions | Provide the permissions for the current node using the node public key. |
| get permissions for member [member id] | The permissions for the member identified by its public key. |
| get authentication | Returns ON or OFF depending on the current status. |
| get encryption | Returns ON or OFF depending on the current status. |
| get compression | Returns ON or OFF depending on the current status. |

## Get servers
The ***get servers*** command returns information on the Operators hosting data.  
Usage:
<pre>
get servers where company = [company name] and dbms = [dbms name] and table = [table name] bring [key string]
</pre>
The ***where*** condition and the ***bring*** keywords are optional.  
If the ***where*** condition is used, the process is satisfied with Operators associated with the company, dbms and table values provided.  
If a value for a company, dbms or table is not provided - an asterisk value is assumed ('*') such that all values satisfy the call.  
The bring command determines the values retrieved from the policies and formatting options.  
If ***bring*** is omitted, the IP and Port of the servers are retrieved.  
Details on the bring command are available in the section [The 'From JSON Object Bring' command](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#the-from-json-object-bring-command).   
Examples:
<pre>
get servers
get servers where dbms = lsl_demo and table = ping_sensor
get servers where company = anylog and dbms = lsl_demo and table = ping_sensor
get servers where company = anylog bring [operator][ip] : [operator][port] --- [operator][id]
</pre>


## Get pools info

These commands return the number of threads aligned to satisfy tasks and a flag indicating if each thread is busy executing a task or in a wait state for a new task.  
For example:
<pre>
get workers pool
</pre>
returns:
<pre>
Workers Pool with 3 workers: [0, 1, 1]
</pre>
Meaning that the first thread of the 3 is in rest while 2 threads are busy.
<pre>
get query pool
</pre>
returns:
<pre>
Query Pool with 3 workers: [0, 1, 1]
</pre>
Meaning that the first thread of the 3 is in rest while 2 threads are busy.


## REST Command

The ***rest*** command allows to send REST requestd to a REST server. The Rest server can be an AnyLog node that provides a REST connection or a non-AnyLog node that satisfies REST requests. 

<pre>
rest [operation] where url=[url] and [option] = [value] and [option] = [value] ...
</pre>

Explanation:  
When an AnyLog node is running, it offers a REST API. The REST allows to accept REST calls from users and applications (like Grafana) to the Network members.    
Activating the REST API on a particular node is explained in [REST requests](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests).  
Using the REST command users can issue REST calls between members of the network and between non-members to members of the network.         
The rest call provides the target URL (of the REST server) and additional values.  
The URL must be provided, the other key value pairs are optional headers and data values.

Supported REST commands:
GET - to retrieve data and metadata from the AnyLog Network.  
PUT - to add data to the AnyLog Network. 

Examples:
<pre>
'rest get where url = http://10.0.0.159:2049 and type = info and details = "get status"\n'
'rest put where url = http://10.0.0.25:2049 and dbms = alioi and table = temperature and mode = file and body = "{"value": 50, "timestamp": "2019-10-14T17:22:13.0510101Z"}"',
</pre>


### Using REST command to retrive data from a data source

Using a ***REST GET*** command data can be pulled from a REST data source and written to a file.  
To pull data, the command results are assigned to a process that directs the data to a file as follows:
<pre>
[File and Data Format Instructions] = rest get where url=[url] and [option] = [value] and [option] = [value] ...
</pre>

File and data format instructions are key value pairs separated by the equal sign and provide several options:


| Key        | Value  |
| ---------- | -------| 
| file       | Path and File Name. |
| key        | If the GET request reurnes a dictionary, output the values of the provided key. |
| show       | True/False - designating to display status as data is written to the output file. The default value is False. |


Example:  
The following example extract data from the [PurpleAir Website](https://www2.purpleair.com/).  
The call to https://www.purpleair.com/json provides latest sensor reading which are organized as a list within a dictionary.    
The following command, pulls the dictionary using a ***GET*** call, from the dictionary the key ***results*** provides the list with the readings and the data is saved to a file called purpleair.json in the prep directory.
<pre>
[file=!prep_dir/purpleair.json, key=results, show=true] = rest get where url = https://www.purpleair.com/json
</pre>
An Example of the usage of the REST GET command is available in the section [Mapping Data to Tables](https://github.com/AnyLog-co/documentation/blob/master/mapping%20data%20to%20tables.md#purpleair-example).

 
## SQL Command

The ***sql*** command allows to execute sql statements on the data hosted by members of the network. 

<pre>
sql [dbms name] [options] [sql statement]
</pre>

Explanation:  
The SQL statement is applied to the logical database and is executed according to the options provided.  
If the sql is send to nodes in the network, there is no need to specify the target servers, the network protocol identifies all the nodes that host data for the logical database.  
The format to distribute the call to all the servers with relevant data is as follows:  

Usage:
<pre>
run client () sql [dbms name] [options] [sql statement]
</pre>
Whereas processing the query on designated servers is done by specifying the IPs and Ports of the servers inside the parenthesis as in the example below:  
<pre>
run client (ip:port, ip:port ...) sql [dbms name] [options] [sql statement]
</pre>
Nodes that receives the SQL statement will execute the statement if a logical database is declared on their node. 
To assign a logical database to a physical database use the command: ```connect dbms```.     
To view the list of logical databases on a particular node use the command: ```get databases```.  
If a logical database is not declared on the node, the node will return an error message.  
A node that issues a query needs to declare a logical database to host the query results and the name of the logical database is ***system_query***.  
An example of using SQLite as the physical database for ***system_query*** is the following:
<pre>  
connect dbms sqlite !db_user !db_port system_query memory
</pre>
The ***memory*** keyword is optional and directs the database to reside in RAM.  
The ***sqlite*** keyword can be replaced with ***psql*** to leverage PostgreSQL to host the results sets.  

### Options

Options are provided in the format ```key = value``` and multiple options are seperated by the```and``` keyword. 
detaile are provided in the [Query options](https://github.com/AnyLog-co/documentation/blob/master/queries.md#query-options) section.

### Example
<pre>  
run client () sql purpleair file = !prep_dir/my_data.json and dest = file and format = json "select * from readings limit 10"
</pre>

### Predefined SQL functions
Details on queries executed against time series data are available in [Optimized time series data queries](https://github.com/AnyLog-co/documentation/blob/master/queries.md#optimized-time-series-data-queries).
### Monitoring queries  
Details on profiling and monitoring queries are available in [Profiling and Monitoring Queries](https://github.com/AnyLog-co/documentation/blob/master/profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries)

# Backup Command

The ***backup*** command transfers data from local database to a file for archival.  
If the table's data is not partitioned, the backup includes the entire table's data set.  
If the table data is partitioned, the backup operates at a partition level and can include one partition or all the partitions of the table.

Usage:
<pre>
backup table where dbms = [dbms name] and table = [table name] and partition = [partition name] and dest = [output directory]
</pre>

Explanation:

Backup the data of a particular partition or all the partitions of a table.  
Partition name is optional, if omitted all the partitions of the table participate in the backup process.  
If the table is not partitioned, the entire table participates in the backup process.
The data of each partition is written into a file at the location specified with the keyword 'dest'.    
The file data is organized in a JSON format which can be processed and ingested by a node in the network. 

Examples:
<pre>
backup table where dbms = purpleair and table = readings and dest = !bkup_dir
backup partition where dbms = purpleair and table = readings and partition = par_readings_2018_08_00_d07_timestamp and dest = !bkup_dir
</pre>

# Partition Command

Users' data is maintained on local databases organized in tables. As the data is ***time series data***, it is possible to organize the data in partitions based on time.    
If the data of a table is partitioned, the partitioning is hidden from the users and applications. Users interact with the data using the table name and the distribution of the processing to the different partitions is transparent.       
Any date-time column can be leveraged as the partition column. 

Usage:  
<pre>
partition [dbms name] [table name] using [column name] by [time interval]
</pre>

Time intervals options are: 
* year 
* month 
* week 
* day 
  
The time interval can be assigned with a counter (and cam be expressed as singular or plurals) - for example, ***3 months*** sets 4 months partitions.  
 
Examples:
<pre>
partition lsl_demo ping_sensor using timestamp by 2 days
partition lsl_demo ping_sensor using timestamp by month
partition lsl_demo * using timestamp by month
</pre>

## partitions status and configurations

The following command lists the partitions configurations:
<pre>
get partitions
</pre>

The ***info table*** command provides information on the partitions that are existing on the node:  

Usage:
<pre>
 info table [db name] [table name] [info type]
</pre>
[dbms name] - the name of the logical database containing the table and its partitions  
[table name] - the name of the table  
[info type] - the type of the requested info:  

The type of information provided on each table is determined by the ***info type*** as follows:

| Info Type  | Details  |
| ---------- | -------| 
| exists | Returns 'true' or 'false' indicating if the table exists  |
| columns    | The table's/partition's columns names and data types  |
| partitions | The list of partitions of the specified table  |
| partitions last | The name of the last partition (by the partition date/time interval)  |
| partitions first | The name of the first partition (by the partition date/time interval)  |
| partitions count | The number of partitions  |
| partitions dates | The date/time interval assigned to each partition  |

Examples:
<pre>
info table sensors readings columns
info table sensors readings exists
info table sensors readings partitions
info table sensors readings partitions last
info table sensors readings partitions first
info table sensors readings partitions count
</pre>

# Drop Partition Command

When data needs to be removed from a node, users can process the removal by dropping partitions. As the data is partitioned by time, it is possible to drop the oldest partition while the system continues to process data with the remaining partitions.  
Users can leverage the [backup](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#backup-command) process prior to the drop of the partition.

Usage:  
<pre>
drop partition [partition name] where dbms = [dbms name] and table = [table name] and keep = [value]
</pre>
  
Explanation:  
Drops a partition in the named database and table.  
* [partition name] is optional. If partition name is omitted, the oldest partition of the table is dropped and if the table has only one partition, an error value is returned.    
* [keep] is optional. If a value is provided, the oldest partitions will be dropped to keep the number of partitions as the value provided.  
* If table name is asterisk (*), a partition from every table from the specified database is dropped.  
* If partition name is asterisk (*), all the partitions are dropped.  

Examples:
<pre>
drop partition par_readings_2019_08_02_d07_timestamp where dbms = purpleair and table = readings
drop partition where dbms = purpleair and table = readings
drop partition * where dbms = purpleair and table = readings
drop partition where dbms = aiops and table = factualvalue and keep = 5
</pre>


## Test Command

The ***test*** command executes the requested tests on the current node.  

Options:  

### Test Node
The ***test node*** command tests the node connections and the local blockchain file.

Example:
<pre>
test node
</pre>

### Test Connection
The ***test connection*** command tests the given IP and Port to determine if accessible and open.

Example:
<pre>
test connection 10.0.0.223:2041
</pre>

### Test Table
The ***test table*** command compares the table definition in the local dbms and the blockchain definition of the table.  

Usage:  
<pre>
test table [table name] where dbms = [dbms name]
</pre>
  
Example:
<pre>
test table ping_sensor where dbms = lsl_demo
</pre>


# Conditional execution

AnyLog supports conditional executions using ***if and else*** statements. 
An ***if and else*** statements are with the following structure:

<pre>
if [condition] then [command A]
else [command B]
</pre>

* [condition] - an expression that will be evaluated
* [command] - any of the AnyLog commands

The condition is an expression that is validated, a true result triggers the execution of the command following the  ***then*** keyword.  
A false result triggers the execution of the commands following the ***else*** keyword. Multiple ***else*** statements are allowed.

AnyLog supports the following conditions:


| Sign  | Details                 | Comments     |
| ----- | ------------------------| ---------- | 
| ==    | Equal                   |            |
| !=    | Not Equal               |            |
| <     | Less than               |            |
| <=    | Less than or equal to   |            |
| >     | Greater than            |            |
| >=    | Greater than or equal to |            |
|       | Is defined             | No sign - Returns True if the variable is defined in the local dictionary |
| not   | Is not defined         | Returns True if the variable is not defined in the local dictionary |
| contains  | Includes the provided substring using case insensitive comparison | if X contains Y - Returns True if X and Y are strings and Y is a substring of X  |

Multiple conditions within parenthesis are allowed with an ***and*** or ***or*** keyword separation.  
The allowed structure is the following:

<pre>
if ([condition a]) and/or ([condition b]) then [command]
else [command]
</pre>

Note:  
* By default, comparison treats all values as strings, if data type is specified, the comparison is treating the compared values by their
data types.  
The supported data types are ***str*** (the default), ***int*** and ***float***.
Data types are specified by adding a dot, and a data type to the variable considered. For example: ```if !a.float == 1.234```.
  
* The result of an if statement can be assigned to a variable, for example: ```a = if not !a```.
  
* Users can test if statements on the AnyLog CLI by executing the if statement, for example: ```if not !a```.

* Nested parenthesis are not supported.

Examples:

<pre> 
if not !json_data then process !script_create_table
</pre>
<pre>
if !old_value.int == 128 then print values are equal
</pre>
<pre>
if !number.int < !value then echo true
</pre>
<pre>
if not !old_value then old_value = 5
</pre>
<pre>
if not !a then a = "new value"
else message = "The dictionary value for a is: " + !a
else print !message
</pre>
<pre>
if (!a and !b == 123) or (!c and !d) then print "with value"
else print "no value"
</pre>
<pre>
if !a.int == 5 then print "Comparison as integers succeeded"
</pre>
<pre>
if !a then print with value
else print "without value"
</pre>
<pre>
if not !a then print "without value"
else print "with value"
</pre>
<pre>
a = if not !a
</pre>
<pre>
if !company_name includes "anylog"
</pre>


## Multiple do - then instruction

Conditional execution can make multiple commands dependent on a condition.   
The commands that are executed if the condition returns ***true*** are prefixed by the ***do*** keyword.    
The commands that are executed if the condition returns ***false*** are prefixed by the ***else*** keyword.    
  
Usage:
<pre>
if [condition] then 
do [command A]
do [command B]
do [command C]
else [command d]
else [command f]
else [command f]
</pre>

Example:

<pre>
if (!external_ip and !node_1_port and !ip and !node_1_port) then 
do run tcp server !external_ip !node_1_port !ip !node_1_port
do print "Node connected to the AnyLog Network" 
do get connections
else print "Missing configurations for IP and Port to connect to the AnyLog Network"
else email to my_name@my_company.co where subject = "anylog node" and message = "not connected"
</pre>


