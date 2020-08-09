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
When the policy is called, the commands asociated with the policy are executed.



## The commands

blockchain [add] [json data]
blockchain [get] [key][atribute name value pairs]
blockchain [push] [json data]
blockchain [pull] to [json | sql | stdout]
blockchain create table
blockchain drop table
blockchain delete local file
blockchain get id [json]
blockchain test
call [name]
connect dbms [db_type] [db_user@db_ip:db_passwd][db_port][db_name] ["memory"]
create table [table name] where dbms = [dbms_name]
create view [dbms name].[table name] (comma seperated column names, values and mapping information)
debug [on/off] [list of process names]
dictionary set [key] = [value] or [key] = [value]
dictionary get [key] or [!key]
dictionary show
directory [path] get [file|dir] [repeat = n]
directory show
disconnect dbms [dbms name]
do [command]
drop table [table name] where dbms = [dbms name]
echo [text]
else [command]
email where from = [sender email] and password = [sender password] and to = [receiver email] and message = [message text]
end script
event [event_name] [info]
exit [process type|reset]
file  [option] [file name] [second file] [ignore error]
from [json string] bring [attribute names or strings] seperatotr = [value]
generate insert from json where dbms_name = [dbms_name] and table_name = [table_name] and json_file = [json_file] and sql_dir = [sql_directory] and instructions = [instructions_id]
get [info type] [info string]
goto [name]
help [command]
if [int/str] [condition] then [command]
include policy [where conditions to identify the policy]
incr [variable] [value]
info dbms [table name] [info type]
info table [db name] [table name] [info type]
info view [db name] [table name] [info type]
job [operation] [job id|'all']
log [type of log] [function] [info string]
next
on error goto [name]
on error call [name]
on error end script
on error ignore
partition [dbms name] [table name] using [column name] by [time interval]
pi sql text [sql stmt]
pi debug [on/off]
print [text to print]
process [path and file name]
python [python string]
random substr [seperator] [string]
rest get where url=[url] and [list list of 'key' = 'value' pairs]
return
run blockchain sync [options]
run client (IPs and Ports) [AnyLog command]
run ha [options]
run operator [options]
run publisher [options]
run rest server [ip] [port] [timeout]
run scheduler [time]
run tcp server [ip] [port]
run udp server [ip] [port]
schedule [options] command [command to execute]


## Set Command

set [variable name] = [value]
set query mode using [params]
set query log
set query log profile [n] seconds
set new query timer
set function key f[value] [string]
set debug [on/off/interactive]
set thread pool [n]


The set commands modify state and setting information

<pre>
show peer
</pre>


<pre>
Command                             Details
------                              -------------
set [name] = [value]                Assigns a value to a given name. 
set query log                       Activates a log recording queries being processed.
set query log profile [n] seconds   Records in the query log only queries with execution time greater or equal to [n] seconds.
set new query timer                 Resets the list and timers that monitor query execution time.
set debug [on/off]                  Print the executed commands processed in scripts.  
set debug interactive               Interactive mode is only available with threads.  
                                    Interactive mode pauses the execution after a command is being executed.  
                                    The user is required to input 'next' to proceed to the next command.
set threads pool [n]                create a pool of workers thread that distributes query processing. n represents the number of threads.
</pre>



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



sleep [sleep time in seconds]
sql [db_name][source] [sql stmt]
stop [all/thread id]
suggest create [input JSON file]
system [OS command]
test node
test connect ip:port
test table [table name] where dbms = [dbms name]
thread [path and file name]
time file rename [file name] to dbms = [dbms name] and table = [table name] and source = [source name] and instructions = [instructions id]
time file new [file name] [optional status 1] [optional status 2]
time file update [hash value] [optional status 1] [optional status 2]
time file get [retrieve info]
trace level = [value] [command]

