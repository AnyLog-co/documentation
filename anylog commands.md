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
Commands can be organized in a file and processed using the command `script` followed by the path and name of the script.  
Commands organized in a script can be also executed using the command `thread`. The thread command dedicates a thread to execute the script commands, and it is unusably the case for a sequence of commands that are continuously running.    
Commands can be also placed on the blockchain, identified with a unique ID and processed by calling the ID using the command `policy`.  
This method of organizing commands allows to impact and modify behavior of running nodes by declaring policies on the blockchain.  
   

#### The help command

The command: ```help``` lists all the command options.
The command ```help``` followed by a specific command, provides information and examples on the specific command.  
Example: ```help blockchain```  provides information and command options to the command ```blockchain```.

#### Scripts, Threads and Policies

These are different methods to execute commands on the command line.

##### script
The command `script` followed by a path and file name will execute all the script commands.

##### thread
The command `thread` followed by a path and file name will execute all the commands that are specified in the script file.  
The command `thread` allocates a dedicated thread to execute the commands. This option supports commands that are executed continuously.    
An example would be a script that waits for files to be generated and process the files when identified. When the processing of the identified files is completed, the process restarts to wait for new data files. 
    
##### policy
A set of commands that are placed on the blockchain.
When the policy is called, the commands associated with the policy are executed.  
Policies allows to initiate and modify processes on nodes by publishing processes on the blockchain.   
Policies impact one or more nodes vs. scripts which are private and maintained on the local drive of each node. 

# The node dictionary

Every node maintains a dictionary that associates keys with values.   
When a node is initialized, some keys are preassigned with values. Users and processes can assign new values
to new or existing keys.  
Users and processes can use the keys as representatives of the values by prefixing the key with an exclamation point.   
Assigning a value to a key is done with the following calls:
```anylog
[key] = [value]
```
Or use the set command:
```anylog
set [key] = [value]
```

The following example assigned a path to the key dbms_dir:
```anylog
dbms_dir = D:\AnyLog-Code\AnyLog-Network\data\dbms
```

Use the following command to delete an assignment:
```anylog
[key] = ""
```
Or
```anylog
set [key] = ""
```

To retrieve the value assigned to a key use exclamation point prefixed to the key name.
```anylog
![key]
```
Or use the get command:
```anylog
get ![key]
```

The following example returns the path string assigned to the key ***dbms_dir***:
```anylog
!dbms_dir
```

The following command retrieves all keys and values from the dictionary:
```anylog
get dictionary
```


# List of Commands:
| Commands                                                                                              | 
|-------------------------------------------------------------------------------------------------------|
| [alerts](alerts%20and%20monitoring.md#alerts-and-monitoring)                            |
| [backup](anylog%20commands.md#backup-command)                 | 
| [blockchain](blockchain%20commands.md)                                                  | 
| [drop partition](anylog%20commands.md#drop-partition-command) | 
| [file](file%20commands.md)                                    | 
| [get](anylog%20commands.md#get-command)                       |
| [partition](anylog%20commands.md#partition-command)           | 
| [rest](anylog%20commands.md#rest-command)                     | 
| [set](anylog%20commands.md#set-command)                       | 
| [sql](anylog%20commands.md#sql-command)                       | 
| [test](anylog%20commands.md#sql-command)                      | 
| [time file](managing%20data%20files%20status.md#Time-file-commands)                     | 


## Set Command

The ***set*** commands allows to set variables and configuration parameters.  

Options:  

| Option                                           | Explanation  |
|--------------------------------------------------| ------------|
| [set node name [node name]](#set-node-name)       |  Declare the node name. The name appears on the local CLI. |
| [set query mode](#set-query-mode)                                                                                                                  | Setting execution instructions to the issued queries. |
| [set query log on/off](logging%20events.md#the-query-log)                                                                            | Enable/Disable a log to record the executed queries. |
| [set query log profile [n] seconds](logging%20events.md#the-query-log)                                                               | Applying the Query Log to queries with execution time higher than threshold.  |
| set rest log on/off                                                                                                                                | Enable/Disable a log to record the processed REST commands. The log is retrieved using the 'get rest log' command. |
| set debug [on/off]                                                                                                                                 | Displays the executed commands processed in scripts. |
| set mqtt debug [on/off]                                                                                                                            | Displays the MQTT messages and their processing status. |
| set debug interactive                                                                                                                              | Waits for the user interactive command \'next\' to move to the next command. |
| set threads pool [n]                                                                                                                               | Creates a pool of workers threads that distributes query processing to multiple threads. |
| set echo queue [on/off]                                                                                                                            | Creates a queue to contain echo commands and messages. |
| set authentication [on/off]                                                                                                                        | Enable / Disable user and message authentication. Default value is ON. |
| set encryption [on/off]                                                                                                                            | Enable / Disable encryption of TCP messages. Default value is OFF. |
| set compression [on/off]                                                                                                                           | Enable / Disable compression of data messages. Default value is OFF. |
| set local password = [password]                                                                                                                    | Provide a password to protect sensitive information that is kept on the node (like private keys and users passwords). See also [Using passwords](../security%20authentication/authentication.md#using-passwords).|
| set private password = [password] [in file]                                                                                                        | Provide the password of the private key with an optional command text [in file] to keep encrypted copy on the filesystem. See also [Using passwords](../security%20authentication/authentication.md#using-passwords).|
| set anylog home [absolute path]                                                                                                                    | Declare a path to the AnyLog data files. |
| set traceback [on/off]                                                                                                                             | Print the code path with every call to the error log. If text is specified, stacktrace is added only if the text is a substring in the error message",|
| [set reply ip = [ip]](network%20configuration.md#setting-a-different-ip-address-for-replies) | Set the IP address that for a reply message. |
| [set self ip = [ip]](network%20configuration.md#self-messaging)                             | Set the IP address when the sender and receiver are the same node. |
| set consumer mode = [mode]                                                                                                                         | Change the consumer mode of operation. Optional modes are: "active" and "suspend". |
| set rest timeout [time and time-unit]                                                                                                              |  Sets a time limit for a rest reply. If limit is 0, the process will wait for a reply without timeout. |
| [set data distribution](#set-data-distribution) where ...                                                                                          |  Define how data is distributed to the storage nodes. |
| [set streaming condition](streaming%20conditions.md#condition-declaration)        |  Declare a condition on streaming data. |


#### Set node name
Declare the node name. The name appears on the CLI prompt.    
Example:
```anylog
set node name Opreator_3
```
The CLI prompt will appear as: 
```anylog
AL Operator_3 >
```
Whereas **AL** stands for AnyLog and **Operator_1** is the assigned name.

Use the following command to reset the node name: 
```anylog
set node name ""
```

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
```anylog
set data distribution where dbms = [dbms_name] and table = [table_name] and dest = [ip:port]
```
dbms - the database associated with the data  
table - the table associated with the data  
dest - the destination ip and port (one or more)  

Example:
```anylog
set data distribution where dbms = lsl_demo and table = * and dest = 10.12.32.148:2048 and dest = 10.181.231.18:2048
```

Removal of an existing distribution is by adding the keyword and value: ```remove = true```.  
Usage:
```anylog
set data distribution where dbms = [dbms_name] and table = [table_name] and remove = true
```
Example:
```anylog
set data distribution where dbms = lsl_demo and table = ping_sensor and remove = true
```

View the distribution definitions using the command:
```anylog
get publisher distribution
```

## Reset Command

The ***reset*** commands allows to reset variables and configuration parameters.  

Options:  

| Option        | Explanation  |
| ------------- | ------------| 
| reset [event/error/file/query] log | Deletes the log entries in the specified file  |
| reset query timer | Reset the query timer. | 
| reset echo queue  | Reset the queue. |
| reset echo queue where size = [n] | Resets the queue and sets the size of the queue to maintain the last n messages (between 1 and 100). |
| reset reply IP | Identify a reply IP to be used by the replying node. Details are available at [Network Configuration](network%20configuration.md#reset-the-reply-ip-to-the-source-ip).|
| reset self IP | Identify an IP to be used when sender and receiver are the same node. Details are available at [Network Configuration](network%20configuration.md#reset-self-messaging).|
| reset streaming conditions | Remove one or more streaming conditions. Details are available at [Reset Streaming Condition](streaming%20conditions.md#reset-streaming-condition).|


## Get Command

The get command provides information on hardware state and status, files, resources and security of the node. 

Options:  

| Option                                                           | Information provided  |
|------------------------------------------------------------------| ------------|
| [get node name](#get-node-name)                                  | Return the name assigned to the node including the IP and Port identifying the node. |
| [get event log](logging%20events.md#the-event-log)               | Records the Last commands processed by the node. | 
| [get error log](logging%20events.md#the-error-log)               | Records the last commands that returned an error. Adding a list of keywords narrows the output to error events containing the keywords.|
| [get file log](#get-logged-instances)                            | Records the last data files processed by the node. |
| [get rest log](#get-logged-instances)                            | Records the REST calls returning an error. Can record all REST calls by setting "set rest log on" |
| [get query log](logging%20events.md#the-query-log)               | The last queries processed by the node. Enable this log using the ***set query log*** command|
| [get processes](®#the-get-processes-command)                     | The list of background processes. More details are available in [background processes](background%20processes.md).|
| get members status                                               | Get status of members nodes that are messaged by this node. |
| get synchronizer                                                 | Information on the blockchain synchronize process. |
| [get operator](monitoring%20calls.md#get-operator)               | Information on the Operator processes. |
| [get blobs archiver](background%20processes.md#the-blobs-archiver)      | Information on the Blobs Archiving processes. |
| get publisher                                                           | Information on the Publisher processes. |
| get distributor                                                         | With HA enabled, information on the distributions of source files to cluster members. |
| get consumer                                                            | With HA enabled, information on pulling source files from cluster members. |
| [get streaming](monitoring%20calls.md#get-streaming)                    | Information on streaming data from REST and MQTT calls. |
| get cluster info                                                        | Information on the cluster supported by the node including Cluster ID, Member ID and Operators supporting the cluster. |
| get tsd info [table name]                                               | Information on the synchronization status between the cluster members. |
| [get rest calls](monitoring%20calls.md#get-rest-calls)                  | Statistical information on the REST calls. |
| [get rest server info](monitoring%20calls.md#rest-server-configuration) | Information on the REST server configuration. |
| [get msg clients](monitoring%20calls.md#get-msg-clients)                | Information on clients subscribed to topics. |
| get msg brokers                                                         | Information on message brokers and the topics subscribed with each broker. |
| get local broker                                                           | Information on the Message Broker. |
| [get status](monitoring%20nodes.md#the-get-status-command)   | Replies with the string 'running' if the node is active. Can be extended to include additional status information | 
| get connections                                                            | The list of TCP and REST connections supported by the node. |
| get machine connections                                                    | The system-wide socket connection. Users can detail specific port: ```get machine connections where port = [port]```|
| get platforms                                                              | The list connected blockchain platforms. |
| [get dictionary](../monitoring%20nodes.md#the-get-dictionary-command)      | The list of the variable names and their assigned values. |
| [get env var](../monitoring%20nodes.md#the-get-env-var-command)            | The environment variables keys and values. |
| get databases                                                              | The list of databases managed on the local node. |
| get partitions                                                             | Information on how data is partitioned on the local databases. |
| get partitions where dbms = [dbms_name] and table = [table name]           | Partition details on a specific table. |
| get query mode                                                             | The query param variables assigned by the command ***set query mode***. |
| [get query pool](#get-pool-info)                                           | Details the status of query workers assigned by the command ***set threads pool [n]***. The value 0 means thread in rest and 1 processing data.|
| [get tcp pool](#get-pool-info)                                             | Details the number TCP workers thread that execute peer command. The number of threads is set by the command ***run tcp server***. |
| [get rest pool](#get-pool-info)                                            | Details the number REST workers thread that execute REST calls. The number of threads is set by the command ***run rest server***. |
| [get msg pool](#get-pool-info)                                             | Details the number Message Broker workers thread that execute REST calls. The number of threads is set by the command ***run message broker***. |
| [get operator pool](#get-pool-info)                                        | Details the number of operator threads. The number of threads is set by the command ***run operator***. |
| get threads                                                                | The list of the threads executing users scripts. |
| get scheduler [n]                                                          | Information on the scheduled tasks. [n] - an optional ID for the scheduler, the default value is 1, 0 is the system scheduler.|
| get hostname                                                               | The name assigned to the node. | 
| get version                                                                | The code version. |
| get git [version/info] [path to github root]                               | ***git version*** returns the first 5 digits of the commit used, ***git info*** provides additional information. If path is not specified, the dictionary variable ***!anylog_path*** is used to identify the ***AnyLog-Network*** directory.|
| get queries time                                                           | Statistics on queries execution time. The statistics is configurable by the command ***set query log profile [n] seconds***  |
| get watch directories                                                      | The list of the Watch directories on the node. |
| get metadata info                                                          | Returns summary info on the metadata including version and time since last update . |
| get database size [database name]                                          | The size of the named database in bytes. |
| get node id                                                                | Returns a unique identifier of the node. |
| get hardware id                                                            | Returns a unique identfier of the hardware. |
| [get servers](#get-servers)                                                | Retrurn info on the the servers supporting the table. |
| get tables for dbms [dbms name]                                            | The list of tables of the named database and where the table is declared (local database and/or blockchain) |
| get table [exist status/local status/blockchain status/rows count/complete status] where name = table_name and dbms = dbms_name                     | Returns information on the specified table |
| get views for dbms [dbms name]                                             | The list of views of the named database. |
| get files in [dir name] where type = [file type] and hash = [hash value]   | The list of files in the specified dir that satisfy the optional filter criteria. |
| get file timestamp [file path and name]                                    | Get the file's timestamp. |
| get error [error number]                                                   | Get the error text for the error number. |
| get echo queue                                                             | Get the queue with the ***echo*** commands and messages. |
| get files [directory path]                                                 | Details the files in the specified directory. |
| get directories [directory path]                                           | Details the sub-directories in the specified directory. |
| get json file structure                                                    | Details the convention for JSON file name. |
| get users                                                                  | The list of users declared using the command ```id add user ...```. |
| get reply ip                                                               | Retrieve the IP address for reply messages. |
| get archived files [YYYY-MM-DD]                                            | List the files archived on the provided date. |
| get size [dir name] [YYYY-MM-DD]                                           | List the size of a directory including sub-directories. |
| get access [path and file name or directory name]                          | Get the access rights to the provided file or directory. |
| get data nodes                                                             | Details the Operators that host each table's data. |
| [get rows count](monitoring%20nodes.md#monitoring-data-commands)           | Details the number of rows in all or specified tables.|
| [get files count](../dat%20manaement/image%20mapping.md#get-files-count)   | Details the number of files stored in all or specified tables.|
| [get query execution](../profiling%20and%20monitoring%20queries.md#retrieving-the-status-of-queries-being-processed-on-an-operator-node) | Provides the status of queries being executed on an Operator node.|
| get timezone info                                                          | Get the timezone on the local machine. |
| get datetime [date-time function](queries.md#get-datetime-command)                                                                  | Translate a date-time function to the date-time string. |
| [get streaming conditions](streaming%20conditions.md#condition-declaration)                  | List the conditions assigned to streaming data. |

#### Monitoring node status options:

| Option        | Information provided                                                                                                                                                                  |
| ------------- |---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
| get disk [usage/total/used/free] [path]  | Disk statistics about the provided path.                                                                                                                                              |
| get platform info | Info on the type and version of the OS, node name and type of processor.                                                                                                              |
| get memory info | Info on the memory of the current node. The function depends on psutil installed.                                                                                                     |
| get cpu info | Info on the CPU of the current node.  The function depends on psutil installed.                                                                                                       |
| get cpu usage | Info on current usage of each CPU.  The function depends on psutil installed.                                                                                                         |
| get ip list | The list of IP addresses available on the node.                                                                                                                                       |
| get cpu temperature | The CPU temperature.                                                                                                                                                                  |
| get os process [options] | Different statistics on the OS processes. Details are available [here](../monitoring%20nodes.md#the-get-os-process-command).                                                          |
| get node info [options] | Different statistics on the node. Details are available [here](../monitoring%20nodes.md#the-get-node-info-command).                                                                   |
| get monitored | Retrieve the list of topics monitored by an aggregator node. Details are available [here](monitoring%20nodes.md#organizing-nodes-status-in-an-aggregator-node).         |
| get monitored [topic] | Retrieve monitored info on a specific topic from an aggregator node. Details are available [here](monitoring%20nodes.md#organizing-nodes-status-in-an-aggregator-node). |



Additional information is available at [monitoring nodes](monitoring%20nodes.md#monitoring-nodes).

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


### get node name
Return the node name including the IP and Port that identifies the node.  
The node name is assigned using the command [set node name](#set-node-name). if a name was not assigned, the name returned is "AnyLog".


## Get servers
The ***get servers*** command returns information on the Operators hosting data.  
Usage:
```anylog
get servers where company = [company name] and dbms = [dbms name] and table = [table name] bring [key string]
```
The ***where*** condition and ***bring*** keywords are optional.  
If the ***where*** condition is used, the process is satisfied with Operators associated with the company, dbms and table values provided.  
If a value for a company, dbms or table is not provided - an asterisk value is assumed ('*') such that all values satisfy the call.  
The bring command determines the values retrieved from the policies and formatting options.  
If ***bring*** is omitted, the IP and Port of the servers are retrieved.  
Details on the bring command are available in the section [The 'From JSON Object Bring' command](json%20data%20transformation.md#the--from-json-object-bring-command).   
Examples:
```anylog
get servers
get servers where dbms = lsl_demo and table = ping_sensor
get servers where company = anylog and dbms = lsl_demo and table = ping_sensor
get servers where company = anylog bring [operator][ip] : [operator][port] --- [operator][id]
```

## Get pool info

These are a group of commands that provides statistical information on groups of threads that are leveraged in different processes.  
These commands return, for each thread in the group, its current status and usage.  
Usage:
```anylog
get [group name] pool where details = [true/false] and reset = [true/false]
```
* The ***where*** condition is optional. 
* ***details*** provide additional details on the usage of each thread.
* ***reset*** is optional. If used, the pool statistics are set to 0.

Group names are one of the following:

| Group Name    | Usage       |
| ------------- | ------------| 
| query | Threads supporting queries |
| operator | Threads supporting the operator proccesses |
| rest | Threads supporting communications with applications |
| tcp | Threads supporting communications with network peers |
| msg | Threads supporting the message broker functionalities |

Example 1:
```anylog
get tcp pool
```
returns:
```anylog
TCP Pool with 6 threads: [1, 1, 0, 0, 0, 0]
```
Meaning that the first 2 threads of the 6 are busy while 4 threads are busy.

Example 2:
```anylog
get query pool where details = true
```
The command lists the threads and provides, for each thread:
* Status - 0 means currently at rest and 1 busy.
* Calls - the number of time the thread was called.
* Percentage - percentage of usage.


## REST Command

The ***rest*** command allows to send REST requested to a REST server. The Rest server can be an AnyLog node that provides a REST connection or a non-AnyLog node that satisfies REST requests. 

```anylog
rest [operation] where url=[url] and [option] = [value] and [option] = [value] ...
```

Explanation:  
When an AnyLog node is running, it offers a REST API. The REST accepts REST calls from users and applications (like Grafana) to the Network members.    
Activating the REST API on a particular node is explained in [REST requests](background%20processes.md#rest-requests).

Using the REST command users can issue REST calls between members of the network and between non-members to members of the network.         
The rest call provides the target URL (of the REST server) and additional values.  
The URL must be provided, the other key value pairs are optional headers and data values.

Supported REST commands:
GET - to retrieve data and metadata from the AnyLog Network.  
PUT - to add data to the AnyLog Network. 

Examples:

1. The following example is using REST **GET** to retrieve the status of an AnyLog node using the REST service:
    ```anylog
    rest get where url = http://73.202.142.172:7849 and User-Agent = AnyLog/1.23 and command = "get status"
    ```

2. The following example is using REST **GET** to retrieve the value assigned to a key using the REST service:
    ```anylog
    rest get where url = http://73.202.142.172:7849 and User-Agent = AnyLog/1.23 and command = "get !my_key"
    ```

3. The following example is using REST **GET** to query an AnyLog network:
    ```anylog
    rest get where url =  http://10.0.0.78:7849 and command = "sql litsanleandro format = table select timestamp, value from ping_sensor limit 10" and User-Agent = AnyLog/1.23 and destination = network

    ```
         
4. The following example is using REST **POST** to send a message to a  Slack Channel:
    ```anylog
    url = "https://hooks.slack.com/services/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"

    date_time = python "datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')"
    text_msg = "test at: " + !date_time 
    message = json {"text": !text_msg}
    rest post where url = !url and body = !message and headers = "{'Content-Type': 'application/json'}" 
    ```
5. The following example is using REST **PUT** to add data to an AnyLog node:
    ```anylog
    rest put where url = http://10.0.0.78:7849 and dbms = alioi and table = temperature and mode = file and body = "{"value": 50, "timestamp": "2019-10-14T17:22:13.0510101Z"}"
    ```
   
6. The following example is using REST **VIEW** to retrieve info from the AnyLog node:
    ```anylog
    rest view where url = http://10.0.0.78:7849 
    ```

### Using REST command to retrieve data from a data source

Using a REST _GET_ command data can be pulled from a REST data source and written to a file.  
To pull data, the command results are assigned to a process that directs the data to a file as follows:
```anylog
[File and Data Format Instructions] = rest get where url=[url] and [option] = [value] and [option] = [value] ...
```

File and data format instructions are key value pairs separated by the equal sign and provide several options:


| Key        | Value  |
| ---------- | -------| 
| file       | Path and File Name. |
| key        | If the GET request reurnes a dictionary, output the values of the provided key. |
| show       | True/False - designating to display status as data is written to the output file. The default value is False. |


Example:  
The following example extract data from the [PurpleAir Website](https://www2.purpleair.com/).  
The call to https://www.purpleair.com/json provides the latest sensor reading which are organized as a list within a dictionary.    
The following command, pulls the dictionary using a ***GET*** call, from the dictionary the key ***results*** provides the list with the readings and the data is saved to a file called purpleair.json in the prep directory.
```anylog
[file=!prep_dir/purpleair.json, key=results, show=true] = rest get where url = https://www.purpleair.com/json
```
An Example of the usage of the REST _GET_ command is available in the section [Mapping Data to Tables](mapping%20data%20to%20tables.md#mapping-data).

 
## SQL Command

The ***sql*** command allows to execute sql statements on the data hosted by members of the network. 

```anylog
sql [dbms name] [options] [sql statement]
```

Explanation:  
The SQL statement is applied to the logical database and is executed according to the options provided.  
If the SQL is sent to nodes in the network, there is no need to specify the target servers, the network protocol identifies all the nodes that host data for the logical database.  
The format to distribute the call to all the servers with relevant data is as follows:  

Usage:
```anylog
run client () sql [dbms name] [options] [sql statement]
```
Whereas processing the query on designated servers is done by specifying the IPs and Ports of the servers inside the parenthesis as in the example below:  
```anylog
run client (ip:port, ip:port ...) sql [dbms name] [options] [sql statement]
```
Nodes that receives the SQL statement will execute the statement if a logical database is declared on their node. 
To assign a logical database to a physical database use the command: ```connect dbms```.     
To view the list of logical databases on a particular node use the command: ```get databases```.  
If a logical database is not declared on the node, the node will return an error message.  
A node that issues a query needs to declare a logical database to host the query results and the name of the logical database is ***system_query***.  
An example of using SQLite as the physical database for ***system_query*** is the following:
```anylog  
connect dbms sqlite !db_user !db_port system_query memory
```
The ***memory*** keyword is optional and directs the database to reside in RAM.  
The ***sqlite*** keyword can be replaced with ***psql*** to leverage PostgresSQL to host the results sets.  

### Options

Options are provided in the format of `key = value` and multiple options are separate by the `and` keyword. 
detail are provided in the [Query options](queries.md#query-options) section.

### Example
```anylog  
run client () sql purpleair file = !prep_dir/my_data.json and dest = file and format = json "select * from readings limit 10"
```

### Predefined SQL functions
Details on queries executed against time series data are available in [Optimized time series data queries](queries.md#optimized-time-series-data-queries).
### Monitoring queries  
Details on profiling and monitoring queries are available in [Profiling and Monitoring Queries](profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries)

# Backup Command

The ***backup*** command transfers data from local database to a file for archival.  
If the table's data is not partitioned, the backup includes the entire table's data set.  
If the table data is partitioned, the backup operates at a partition level and can include one partition or all the partitions of the table.

Usage:
```anylog
backup table where dbms = [dbms name] and table = [table name] and partition = [partition name] and dest = [output directory]
```

Explanation:

Backup the data of a particular partition or all the partitions of a table.  
Partition name is optional, if omitted all the partitions of the table participate in the backup process.  
If the table is not partitioned, the entire table participates in the backup process.
The data of each partition is written into a file at the location specified with the keyword `dest`.    
The file data is organized in a JSON format which can be processed and ingested by a node in the network. 

Examples:
```anylog
backup table where dbms = purpleair and table = readings and dest = !bkup_dir
backup partition where dbms = purpleair and table = readings and partition = par_readings_2018_08_00_d07_timestamp and dest = !bkup_dir
```

# Partition Command

Users' data is maintained on local databases organized in tables. As the data is ***time series data***, it is possible to organize the data in partitions based on time.    
If the data of a table is partitioned, the partitioning is hidden from the users and applications. Users interact with the data using the table name and the distribution of the processing to the different partitions is transparent.       
Any date-time column can be leveraged as the partition column. 

Usage:  
```anylog
partition [dbms name] [table name] using [column name] by [time interval]
```

Time intervals options are: 
* year 
* month 
* week 
* day 
  
The time interval can be assigned with a counter (and cam be expressed as singular or plurals) - for example, ***3 months*** sets 4 months partitions.  
 
Examples:
```anylog
partition lsl_demo ping_sensor using timestamp by 2 days
partition lsl_demo ping_sensor using timestamp by month
partition lsl_demo * using timestamp by month
```

## Partitions status and configurations

The following command lists the partitions configurations:
```anylog
get partitions
```

The ***info table*** command provides information on the partitions that are existing on the node:  

Usage:
```anylog
 info table [db name] [table name] [info type]
```
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
```anylog
info table sensors readings columns
info table sensors readings exists
info table sensors readings partitions
info table sensors readings partitions last
info table sensors readings partitions first
info table sensors readings partitions count
```

# Drop Partition Command

When data needs to be removed from a node, users can process the removal by dropping partitions. As the data is partitioned by time, it is possible to drop the oldest partition while the system continues to process data with the remaining partitions.  
Users can leverage the [backup](anylog%20commands.md#backup-command) process prior to the drop of the partition.

Usage:  
```anylog
drop partition [partition name] where dbms = [dbms name] and table = [table name] and keep = [value]
```
  
Explanation:  
Drops a partition in the named database and table.  
* [partition name] is optional. If partition name is omitted, the oldest partition of the table is dropped and if the table has only one partition, an error value is returned.    
* [keep] is optional. If a value is provided, the oldest partitions will be dropped to keep the number of partitions as the value provided.  
* If table name is asterisk (*), a partition from every table from the specified database is dropped.  
* If partition name is asterisk (*), all the partitions are dropped.  

Examples:
```anylog
drop partition par_readings_2019_08_02_d07_timestamp where dbms = purpleair and table = readings
drop partition where dbms = purpleair and table = readings
drop partition * where dbms = purpleair and table = readings
drop partition where dbms = aiops and table = factualvalue and keep = 5
```

# Conditional execution

AnyLog supports conditional executions using ***if and else*** statements. 
An ***if and else*** statements are with the following structure:

```anylog
if [condition] then [command A]
else [command B]
```

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

Multiple conditions within parenthesis are allowed with an "_and_" or "_or_" keyword separation.  
The allowed structure is the following:

```anylog
if ([condition a]) and/or ([condition b]) then [command]
else [command]
```

## Using dictionary values in the comparison process

Dictionary values can be mapped to different formats dynamically. Details are available in the 
[Mapping the dictionary values](dictionary.md#mapping-the-dictionary-values) section.

Note:  
* By default, comparison treats all values as strings, if data type is specified, the comparison is treating the compared values by their
data types.  
The supported data types are _str_ (the default), _int_, _bool_ and _float_.
Data types are specified by adding a dot, and a data type to the variable considered. For example: `if !a.float == 1.234`.
  
* The result of an if statement can be assigned to a variable, for example: `a = if not !a`.
  
* Users can test if statements on the AnyLog CLI by executing the if statement, for example: `if not !a`.

* Nested parenthesis are not supported.

Examples:

```anylog 
if not !json_data then process !script_create_table
```
```anylog
if !old_value.int == 128 then print values are equal
```
```anylog
if !number.int < !value then echo true
```
```anylog
if not !old_value then old_value = 5
```
```anylog
if not !a then a = "new value"
else message = "The dictionary value for a is: " + !a
else print !message
```
```anylog
if (!a and !b == 123) or (!c and !d) then print "with value"
else print "no value"
```
```anylog
if !a.int == 5 then print "Comparison as integers succeeded"
```
```anylog
if !a then print with value
else print "without value"
```
```anylog
if not !a then print "without value"
else print "with value"
```
```anylog
a = if not !a
```
```anylog
if !company_name includes "anylog"
```


## Multiple do - then instruction

Conditional execution can make multiple commands dependent on a condition.   
The commands that are executed if the condition returns "_true_" are prefixed by the "_do_" keyword.    
The commands that are executed if the condition returns "_false_" are prefixed by the "_else_" keyword.    
  
Usage:
```anylog
if [condition] then 
do [command A]
do [command B]
do [command C]
else [command d]
else [command f]
else [command f]
```

Example:

```anylog
if (!external_ip and !node_1_port and !ip and !node_1_port) then 
do run tcp server !external_ip !node_1_port !ip !node_1_port
do print "Node connected to the AnyLog Network" 
do get connections
else print "Missing configurations for IP and Port to connect to the AnyLog Network"
else email to my_name@my_company.co where subject = "anylog node" and message = "not connected"
```

# The Wait Command

The **wait** command pauses execution of the thread until a condition is satisfied, or a time limit is reached.  

Usage:
```anylog
 wait [max wait time in seconds] for [condition]
```

A common usage is when a node issues a command to peer nodes, some peers reply and some peers are disconnected.  
The wait command pauses until all peers reply, but no longer than the max wait time.

Example:
```anylog
nodes_reply[] = run client (10.0.0.78:3048, 10.0.0.78:7848) get status
wait 5 for !nodes_reply.diff == 0
```
In the example above, 2 peer nodes are messaged for their status (note: replies are organized in a list).  
The wait command thread pauses for 5 seconds or until the 2 peer nodes replies are received - whichever comes first.  

Note: Associating replies from peer nodes to a key in the dictionary is detailed in the
[Associating peer replies to a key in the dictionary](network%20processing.md#associating-peer-replies-to-a-key-in-the-dictionary) section.