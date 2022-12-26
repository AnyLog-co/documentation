# Logging Events

Each node maintains buffers to record events and errors such that users and applications are able to retrieve the recent 
events and errors as they accrue. The command format: 
```anylog
get [log type] log where format = [format type] and keys = key1 key2 ...
```

**Command options**
* `log type` - options are: _event_, _error_, _file_, _query_, _msg_

The `where` condition is optional and details the following:
* `format` - the format of the output, the valid values are _table_ or _JSON_. The default value is _table_.
* `key` - if added, allows to specify one or more keywords to retrieve only logged events containing the keywords.  

### Reset the log data
All the logged data can be reset using the following command:

```anylog
reset [log type] log
```

**Examples**:
```anylog
reset event log
reset error log
reset streaming log
reset query log
```


## The Event Log

The event log records the events processed on the node. The events include the AnyLog commands being executed and the error 
messages. The following examples retrieve the event log:
1. Return all log instances:
```anylog
get event log
```
2. Return log instances containing the keywords "SQL" or "Error". The reply format is JSON.
```anylog
get event log where format = json and keys = SQL Error
```

## The Error Log

The error log contains all error messages.  
The following examples retrieve the error log instances:  
1. Return all error instances:
```anylog
get error log
```
2. Return error instances containing the keywords "rest". The reply format is JSON.
```anylog
get error log where format = json and keys = rest
```

## The Streaming Log

The streaming log collects the HTTP calls from external applications that interact with the node. These calls include the 
REST calls issued to the node. This log is optional and needs to be activated in order to collect the query information.
The following command activates the log:
```anylog
set streaming log on
```

The following command disables the log:
```anylog
set streaming log off
```

The following examples retrieve the streaming log instances:  
1. Return all streaming instances:
```anylog
get error log
```
2. Return streaming instances containing the keywords "put". The reply format is JSON.
```anylog
get error log where format = json and keys = put
```

## The Query Log

The query log collects the queries processed allowing to view and monitor the queries. This log is optional and needs to 
be activated in order to collect the query information.  

### Activating the Query Log
The query log can be activated in 2 modes:

| Mode |   Details    |  Command  |
| ------------------------------------ | ------------| ----|
| All queries Included | Every executed query on the node will be included in the log | `set query log on` |
| Only slow queries included | Only queries that exceed a threshold time execution are included  | `set query log profile [n] seconds` |

The following command disables the query log:
```anylog
set query log off
```

**Examples**:
1. Collecting all queries executed on the node in the log:
```anylog
set query log on
```
2. Collecting all queries executed on the node with execution time equal or greater than 6 seconds:
```anylog
set query log profile 6 seconds
```

3. Disable the query log
```anylog
set query log off
```