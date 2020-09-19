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
| set debug [on/off]  | Print the executed commands processed in scripts |
| set debug interactive  | Waits for the user interactive command \'next\' to move to the next command. |
| set threads pool [n]  | Creates a pool of workers threads that distributes query processing to multiple threads. |
| set threads pool [n]  | Creates a pool of workers threads that distributes query processing to multiple threads. |
| set authentication [on/off]  | Enable / Disable user and message authentication. Default value is ON. |


#### Set variable

To see the value assigned to a variable use exclamation point prefixed to the variable name.
<pre>
![variable name] = [value]
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
| timeout  | limit execution on each server by the provided time limit | 
| timeout  | limit execution on each server by the provided time limit |


                     '\ttimeout - limit execution on each server by the provided time limit\n'
                     '\tmax_volume - limit data volume returned by each participating operator\n'
                     '\tsend_mode - use \'all\' to return an error if any of the participating servers is not connected\n'
                     '\t\t use \'any\' to send the query only to the connected servers. The default value is \'all\'.\n'
                     '\treply_mode - use \'all\' to return an error if any of the participating servers did not reply after timeout.\n'
                     '\t\t use \'any\' to return the query results using the available data after timeout. The default value is \'all\'.\n'
 






## Get Command


## Show Command

show [info type] [info string]

The show commands provide status information on the node receiving the REST call.
The show commands are supported on the AnyLog command line or by using a REST client with the following key value pairs in the header information:
<pre>
Key      Value
------   -------------
type     info
details  one of the show commands
</pre>

<pre>
Command                             Details
------                              -------------
show [log name] log                 Returns the information maintained in the named log (event, error, file, query) 
show dbms                           Returns the connected databases
show connections                    Returns the type of connections (IPs and ports) supported by the node
show watch directories              Returns the directories being watched for incomming data
show queries time                   Returns execution time of queries
Show servers for dbms [dbms name]   Returns the IP and Port information of the servers supporting the database
Show servers for dbms [dbms name] and table [table name]
</pre>


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

