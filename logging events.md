# Logging Events

Each node maintains buffers to record events and errors such that users and applications are able to retrieve the recent events and errors as they accrue.    
The command format: 
<pre>
get [log type] log where format = [format type] and keys = key1 key2 ...
</pre>

***Command options***

* ***log type*** - options are: ***event, error, file, query, msg***   

The ***where*** condition is optional and details the following:
* ***format*** - the format of the output, the valid values are ***table*** or ***json***, ***table*** is the default value.  
* ***key*** - if added, allows to specify one or more keywords to retrieve only logged events containing the keywords.

## The Event Log

The msg log records the events processed on the node. The events include the AnyLog commands being executed and the error messages.  
The following examples retrieve the event log:
1. Return all log instances:
<pre>
get event log
</pre>
2. Return log instances containing the keywords "SQL" or "Error". The reply format is JSON.
<pre>
get event log where format = json and keys = SQL Error
</pre>


## The Error Log

## The MSG Log

## The Query Log


<pre>
get query log where keys = "timestamp"
</pre>
If query log is enabled, only queries with "timestamp" in the SQL text will be returned.
