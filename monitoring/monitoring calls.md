# Monitoring calls from external applications

## REST server configuration
The command ***get rest server info*** provides the info on how the REST server is configured.

**Usage**: 
```anylog
get rest server info
```

**Explanation output**:

| Attribute Value | Details  |
| ------------- | ------------| 
| buff_size | Internal buffer for nodes communications. | 
| ca_public_key | The Certificate Authority public key. |
| connection | The IP and Port to connect to external applications vis HTTP requests |
| is_ssl | Is connection using SSL|
| lib_open_ssl | Flag indicating if Open SSL libraries are available on the node |
|node_cr | The Certificate Request issued to the node|
|node_private_key| The private key issued to the node | 
|streaming_log | Determine if REST calls are added to the REST Log |
|timeout | Max wait time in seconds for a REST call |
|trace | Flag indicating if REST calls are traced for debug |
|workers_count | The max number of concurrent threads executing REST calls |

## Get REST Calls

The `get rest calls` command returns statistics on the REST calls issued and their execution results.

Usage: 
```anylog
get rest calls
```

###Example reply:
```anylog
Statistics
Caller Call Processed Errors Last Error              First Call          Last Call           Last Caller
------|----|---------|------|-----------------------|-------------------|-------------------|---------------|
anylog|GET |        3|     1|Error Command Structure|2021-11-24 13:29:01|2021-11-24 13:29:19|10.0.0.78:50183|
      |POST|        4|     0|                       |2021-11-24 13:29:08|2021-11-24 13:29:24|10.0.0.78:50185|
```


## Get Streaming
Data provided via REST APIs and message brokers passes to processing through internal buffers.
The buffers are associated with database tables and the ***get streaming*** command provides information on the data 
that passes through these buffers.

The command returns the data in a text format. Adding the key-value pair ***format = json*** returns the info in a JSON structure.

**Usage**: 
```anylog
get streaming
get streaming where format = json
```

The non JSON reply has 2 sections showing configurations and statistics.

**Section A attributes**:
| Attribute name | Details  |
| ------------- | ------------| 
| Default time | The threshold time to flush the buffers (the default value for tables that are not assigned with time) |
| Default volume | The threshold volume to flush the buffers (the default value for tables that are not assigned with volume)|
| Default Immediate | If Immediate write is set as the default value for all tables |
| Buffered Rows | The total number of rows placed in the streaming buffers |
| Flushed Rows | The total number of rows added to databases |

**Section B attributes**:

| Attribute name | Details  |
| ------------- | ------------| 
| DBMS-Table | The Database and table associated with the info |
| Put Files | Counter of the number of calls to add data (in files) using PUT request |
| Put Rows | Counter for the number of rows added using PUT requests |
| Streaming Calls | Counter of calls to add rows to the streaming buffers (using POST or a message broker) |
| Streaming Rows | Counter for rows added to the streaming buffers  (using POST or a message broker) |
| Cached Rows | Counter for rows in the buffers (that needs to be flushed) |
| Immediate | Counter for rows added to the databases without buffer wait (immediate flag is on) |
| Threshold Volume | The buffer volume threshold in KB |
| Buffer Fill | The percentage of the buffer which is with data (that needs to be flushed) |
| Time Threshold | The time threshold in seconds |
| Time Left | The remaining time to flush the cached data |
| Last Process | Last process return value |


# Get MSG Clients

The `get msg clients` command provides statistics and details on the mapping of data to the tables structures.  
The mapping is done using the command ***run mqtt client***, details are available at the [AnyLog as a broker receiving REST commands](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#anylog-as-a-broker-receiving-rest-commands) section.

Usage: 
```anylog
get msg clients 
get msg client N
```
N represents the subscription ID which is assigned for each ***run mqtt client*** call.
if N is specified, only the specified subscription info is returned, otherwise all subscription declarations are returned.

The reply has 4 sections showing configurations and statistics.  

**Section A attributes**:

| Attribute name | Details  |
| ------------- | ------------| 
| Subscription | The subscription ID |
| User | The ID of the user connecting to the broker (if the data is published on a broker), or ***unused*** if data is published via REST |
| Broker | The URL of the broker, or ***rest*** if data is published via REST  |
| Connection | The type of connection  |

**Section B attributes**:

Statistics on the mapping of data using the subscription.

| Attribute name | Details  |
| ------------- | ------------| 
| Messages | The number of messages received |
| Success | The number of successful mapping |
| Errors | The number of failed mapping | 
| Last message time | The data and time of the last message received | 
| Last error time | The data and time of the last mapping error identified | 
| Last error | The details of the last error recorded | 

**Section C attributes**:

Details of the topic and mapping instructions between the source data and the table structure.

**Section D attributes**:

The locations of the local directories that are used to organize the data for the database ingestion.   
This section is provided by adding the keyword detailed to the command:
```anylog
get msg clients detailed 
get msg client N detailed
```


**Example reply**:
```anylog
AL anylog-node > get msg clients detailed

Subscription: 0001
User:         unused
Broker:       rest
Connection:   Connected to local Message Server

     Messages    Success     Errors      Last message time    Last error time      Last Error
     ----------  ----------  ----------  -------------------  -------------------  ----------------------------------
            194         194           0  2021-11-24 13:29:08
     
     Subscribed Topics:
     Topic QOS DBMS       Table       Column name, type, bring function           
     -----|---|----------|-----------|-------------------------------------------|
     aiops|  0|['[dbms]']|['[table]']|('timestamp', 'timestamp', ['[timestamp]'])|
          |   |          |           |('value', 'float', ['[value]'])            |

     
     Directories Used:
     Directory Name Location                          
     --------------|---------------------------------|
     Prep Dir      |D:\Node\AnyLog-Network\data\prep |
     Watch Dir     |D:\Node\AnyLog-Network\data\watch|
     Error Dir     |D:\Node\AnyLog-Network\data\error|
```

## Get Operator

The `get operator` command provides information on data ingested to the local databases. Data is mapped from a JSON format 
to a SQL format and added to the local database, the command provides information on the process of transforming the JSON 
to SQL and the ingestion process.

The command returns the data in a text format. Adding the key-value pair `format = json` returns the info in a JSON structure.

Usage: 
```anylog
get operator
get operator format = json
```

The non-JSON reply has 4 sections showing configurations and statistics.

### Section A attributes

**Operator Information**:

| Attribute name | Details  |
| ------------- | ------------| 
| Status | Indicate if operator processes are enabled |
| Time | The Operator activity time |
| Cluster | The cluster ID assigned to the operator |
| Member | A unique member ID assigned to the operator as member of the cluster |

### Section B attributes

**JSON Data information**:

| Attribute name | Details  |
| ------------- | ------------| 
| DBMS | The name of the dbms associated with data |
| Table | The name of the table associated with data |
| Files | The number of JSON files processed |
| Immediate | The number of files processed with immediate flag |
| Last Process | The time of the last file processed |


### Section C attributes:

**SQL Data information**:

| Attribute name | Details  |
| ------------- | ------------| 
| DBMS | The name of the dbms associated with data |
| Table | The name of the table associated with data |
| Files | The number of SQL files processed |
| Immediate | The number of files processed with immediate flag |
| Last Process | The time of the last file processed |

### Section D attributes:

Files with failed processes identifying the table and the error.

**Example reply**:
```anylog
AL anylog-node > get operator
Status:     Active
Time:       0:8:50 (H:M:S)
Cluster:    7a00b26006a6ab7b8af4c400a5c47f2a
Member:     61
Statistics JSON files:
DBMS                   TABLE                  FILES      IMMEDIATE  LAST PROCESS
---------------------- ---------------------- ---------- ---------- --------------------
aiops                  ai_mv_2                         1          0 2021-11-24 16:41:49

Statistics SQL files:
DBMS                   TABLE                  FILES      IMMEDIATE  LAST PROCESS
---------------------- ---------------------- ---------- ---------- --------------------
aiops                  ai_mv_2                         1          0 2021-11-24 16:41:49

Errors summary
Error Type           Counter DBMS Name Table Name Last Error Last Error Text
--------------------|-------|---------|----------|----------|---------------|
Duplicate JSON Files|      0|         |          |         0|               |
JSON Files Errors   |      0|         |          |         0|               |
SQL Files Errors    |      0|         |          |         0|               |
```

## Get Operator Summary

The ***get operator summary*** command provides summary information on the operator processes.  
Usage
```anylog
get operator summary
get operator summary format = json
```

The summary call returns info in a table format or in a JSON format.  
The returned info is the following:

| Attribute name | Details  |
| ------------- | ------------| 
| Status | The Operator status - Active or Not Active |
| Operational | HH:MM:SS indicating how long the operator is operational |
| Total Rows | The number of rows processed by the Operator (in all logical tables) |
| Delta Rows | The number of rows processed by the Operator (in all logical tables) since the previous summary call |
| Errors | The total number of errors (in all logical tables) |

The ***get operator summary*** command can be placed on continuous display as follows: 
```anylog
continuous "get operator summary"
```

Details are available in the
[continuous command section](monitoring%20nodes.md#monitoring-nodes-operations)


