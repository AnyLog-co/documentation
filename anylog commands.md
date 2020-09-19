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



## Set Command

The ***set*** commands allows to set variables and configuration parameters.  

Options:  

| Option        | Explanation  |
| ------------- | ------------| 
| set [variable name] = [value]  | Assigning a value to a variable. Same as: [variable name] = [value] | 
| set query mode  | Setting execution instructions to the issued queries. |
| set query log  | Initiate a log to record the executed queries. |
| set query log profile [n] seconds  | Applying the Query Log to queries with execution time higher than threshold.  |
| set new query timer | Reset the query timer. |
| set debug [on/off]  | Print the executed commands processed in scripts. |
| set debug interactive  | Waits for the user interactive command \'next\' to move to the next command. |
| set threads pool [n]  | Creates a pool of workers threads that distributes query processing to multiple threads. |
| set threads pool [n]  | Creates a pool of workers threads that distributes query processing to multiple threads. |
| set authentication [on/off]  | Enable / Disable user and message authentication. Default value is ON. |


#### Set variable

To see the value assigned to a variable use exclamation point prefixed to the variable name.
<pre>
![variable name]
</pre>

To see all assigned values use the command:
<pre>
show dictionary
</pre>

#### Set query mode

The query mode sets a cap on query exection at the Operator Node by setting a limit on execution time or data volume transferred or both.
  
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

## Show Command

Returns information on variables setup and state of the node.

Options:  

| Option        | Information provided  |
| ------------- | ------------| 
| show event log  | The Last commands processed by the node. | 
| show error log  | The last commands that returned an error. |
| show file log  | The last data files processed by the node. |
| show query log  | The last queries processed by the node. Enable this log using the ***set query log*** command|
| show databases  | The list of databases managed on the local node. |
| show connections | The list of TCP and REST connections supported by the node. |
| show query mode | The query mode variables assigned by the command ***set query mode***. |
| show queries time | Statistics on queries execution time. The statistics is configurable by the command ***set query log profile [n] seconds***  |
| show watch directories | The list of the Watch directories on the node. |
| show dictionary | The list of the variable names and their assigned values. |
| show threads | The list of the threads executing users scripts. |
| show synchronizer | Information on the blockchain synchronize process. |
| show scheduler | Information on the scheduled tasks. |
| show operator | Information on the Operator processes. |
| show publisher | Information on the Publisher processes. |
| show rest | Information on the REST processes. |
| show ha | Information on the High Availability processes. |
| show partitions | Information on how data is partitioned on the local databases. |
| show partitions where dbms = [dbms_name] and table = [table name] | Partition details on a specific table. |
| show partitions dropped | Information on partitions which were dropped.  |
| show workers pool | Details the number of query workers assigned by the command ***set threads pool [n]***. |
| show tcp pool | Details the number TCP workers thread that execute peer command. The number of threads [n] is set by the command ***run tcp server [n]*** |
| show files [directory path] | Details the files in the specified directory |
| show directories [directory path] | Details the sub-directories in the specified directory |
| show version | The code version |
| show json file structure | Details the convention for JSON file name |

#### Show log

In the logs, if info string is specified, only events containing one or more of the keywords in the info string are presented.

Examples:

<pre>
show event log "SQL Error"
</pre>
Will show only log instances containing the keywords "SQL" or "Error".

<pre>
show query log "timestamp"
</pre>
If query log is enabled, only queries with "timestamp" in the SQL text will be returned.

#### show workers pool & show tcp pool
These commands returns the number of threads aligned to satisfy tasks and a flag indicating if each thread is busy executing a task or in a wait state for a new task.  
For example:
<pre>
show workers pool
</pre>
returns:
<pre>
show workers pool
</pre>
returns:
<pre>
Workers Pool with 3 workers: [0, 1, 1]
</pre>
Meaning that the first thread of the 3 is in rest while 2 threads are busy.

## Get Command

The get command provides information on hardware state and status, files, resources and security of the node. 

Options:  

| Option        | Information provided  |
| ------------- | ------------| 
| get status  | Replies with the string 'running' if the node is active. | 
| get hostname | The name assigned to the node. | 
| get disk [usage/total/used/free] [path]  | Disk statistics about the provided path. |
| get memory info | Info on the memory of the current node. |
| get cpu info | Info on the CPU of the current node. |
| get database size [database name] | The size of the named database in bytes. |
| get node id | Returns a unique identifier of the node. |
| get hardware id | Returns a unique identfier of the hardware. |
| get servers for dbms [dbms name] and table [table name] | The list of IPs and Ports of the servers supporting the table. |
| get servers for dbms [dbms name] | The list of IPs and Ports of the servers supporting the dbms. |
| get tables for dbms [dbms name] | The list of tables of the named database. |
| get files in [dir name] where type = [file type] and hash = [hash value] | The list of files in the specified dir that satisfy the optional filter criteria. |

Security related Options:  

| Option        | Information provided  |
| ------------- | ------------| 
| get public key  | The node\'s public key. | 
| get public key using keys_file = [file name] | Retrieves the public key from the specified file. |
| get permissions | Provide the permissions for the current node using the node public key. |
| get permissions for member [member id] | The permissions for the member identified by its public key. |
| get authentication | Returns ON or OFF depending on the current status. |

## Rest Command

<pre>
rest [operation] where url=[url] and [option] = [value] and [option] = [value] ...
</pre>

Explanation:  
The rest command allows to send REST requestd to an AnyLog REST server.  
Using REST to deliver requests between members of the network is used to test and validate the REST functionality of the member that offers REST services.       
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

