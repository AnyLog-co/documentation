# AnyLog Commands


## Show Commands

The show commands provide status information on the node receiving the REST call.
These commands are supported on the AnyLog command line or by using a REST client with the following key value pairs in the header information:
<pre>
Key      Value
------   -------------
type     info
details  one of the show commands
</pre>

<pre>
Command                     Details
------                      -------------
show [log name] log         Provides the information maintained in the named log (event, error, file, query) 
show dbms                   Lists the connected databases
show connections            Lists the type of connections (IPs and ports) supported by the node
show watch directories      List the directories being watched for incomming data
show queries time           Lists execution time of queries      
</pre>

### Set Commands

The set commands modify state and setting information

<pre>
Command                             Details
------                              -------------
set [name] = [value]                Assigns a value to a given name 
set query log                       Activates a log recording queries being processed
set query log profile [n] seconds   Records in the query log only queries with execution time greater or equal to [n] seconds
set new query timer                 Resets the list and timers that monitor query execution time     
</pre>