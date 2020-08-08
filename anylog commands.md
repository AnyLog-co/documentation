# AnyLog Commands

Commands can be issued in 2 ways:  
a) Using the AnyLog command line - AnyLog instances provide a command line interface. Users can issue commands using the command line interface.  
All the available commands are supported by the command line interface.  
b) Using a REST API - A subset of the commands are supported using a REST API.
The REST API is the main method to issue queries that evaluate data maintained by members of the network. 


## The help command

The command: ```help``` lists all the coommand options.
The command ```help``` followed by a specific command, provides information and examples on the specific command.  
Example: ```help blockchain```  provides information and command options to the command ```blockchain```.

## Scripts, Threads and Policies

These are different methods to execute commands on the command line.

### script
The command ```script``` folowed by a path and file name will execute all the script commands.

### thread
The command ```thread``` folowed by a path and file name will execute all the commands that are specified in the script file.  
The command ```thread``` allocates a dedecated thread to execute the commands. This option is used to support commands that are continually executing.  
An example would be a script that waits for files to be generated and process the files when identified.
    
### policy
A set of commands that are placed on the blockchhain.
When the policy is called, the commands asociated with the policy are executed.

## Show Commands

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

### REST status commands
The following commands are issued using the REST API to provide REST API status.  

<pre>
Command                     Details
------                      -------------
show peer                   Provides the host and port of the peer issueing the REST call. The values are returned   
                            to the caller and send to the AnyLog stdout.
show peer command on        Enable monitoring of peer commands. When REST calls are issued, the IP and Port of the caller and the command are send 
                            to the AnyLog stdout.
show peer command off       Disable monitoring of peer commands.     
</pre>


## Set Commands

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
                                    Interactive mode pauses the execution after a command is being execute.  
                                    The user is required to input 'next' to proceed to the next command.
set threads pool [n]                create a pool of workers thread that distributes query processing. n represents the number of threads.
</pre>

