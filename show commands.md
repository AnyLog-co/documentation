# The Show commands

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
show queries time           Lists an array of 11 counters representing execution time of queries. 
                            The location in the array represents the time elapsed in seconds.
                            The value is a counter of the number of queries executed with execution time which is less than the represented time.
                            
                            
</pre>
