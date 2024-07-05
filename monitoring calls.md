# Monitoring calls from external applications

## REST server configuration
The command `get rest server info` provides the info on how the REST server is configured.

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
The buffers are associated with database tables and the `get streaming` command provides information on the data 
that passes through these buffers.

The command returns the data in a text format. Adding the key-value pair _format=json_ returns the info in a JSON structure.

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
The mapping is done using the command `run mqtt client`, details are available at the [AnyLog as a broker receiving REST commands](message%20broker.md#anylog-as-a-broker-receiving-rest-commands) section.

Usage: 
```anylog
get msg clients where [options]
```
Options are represented as key value pairs and are one of the following:

| Option name   | Details                                             | Default            |
| ------------- |-----------------------------------------------------| -----------------  |
| id            | The subscription ID (assigned for each `run mqtt client` call.) | All subscriptions  |
| broker        | The broker connection information (ip and port)     |                    |
| topic         | The topic name                                      |                    |
| detailed      | 'true' provides the list of directories used in the process  |  False    |

Examples:
```anylog
get msg clients 
get msg client where id = 2
get msg client where broker = driver.cloudmqtt.com:18785
get msg client where broker = driver.cloudmqtt.com:18785 and topic = anylogedgex
get msg client where id = 2 and detailed = true
```
The reply has 4 sections showing configurations and statistics.  

**Section A attributes**:

| Attribute name | Details                                                                                                                           |
| ------------- |-----------------------------------------------------------------------------------------------------------------------------------| 
| Subscription | The subscription ID                                                                                                               |
| User | The ID of the user connecting to the broker (if the data is published on a broker), or _unused_ if data is published via REST |
| Broker | The URL of the broker, or _REST_ if data is published via REST                                                                      |
| Connection | The type of connection                                                                                                            |

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
This section is provided by assigning the keyword ***detailed*** to the value ***true***:

**Example reply**:
```anylog
AL anylog-node > get msg clients where detailed = true

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

# Get Operator

The Operator service transforms data from native JSON format to a SQL format and adds the data to a local database.      
The **get operator** command provides information on the transformation and storage process.

Usage: 
```anylog
get operator [topic] [where format = json]
```

* **topic** is optional and is one of the following keywords: **config, summary, json, sql, error**.
* **where format = json** specify the returned info in JSON format.

The table below summarizes the command options:

| Command               | Info returned  |
| --------------------- | ------------| 
| get operator          | Returning the info associated with the keywords: **json**, **sql**, **inserts** and **error** - see details below |
| get operator config   | The relevant configuration parameters |
| get operator summary  | A summary of the ingestion process |
| get operator json     | Ingestion info of the source JSON per each table that is serviced by the operator |
| get operator sql      | Ingestion info per each partition that is serviced by the operator |
| get operator inserts  | Inserted rows count by tables serviced by the operator |
| get operator error    | A summary of operations failed |


**Get Operator Config**

| Attribute name | Details  |
| ------------- | ------------| 
| Status | Indicates if the operator service is enabled |
| Time | The timestamp when the service is enabled and the opOperator activity time |
| Policy | The ID of the operator poicy |
| Cluster | The cluster ID assigned to the operator |
| Member | A unique member ID assigned to the operator as member of the cluster |

**Get Operator Summary**:

| Attribute name | Details  |
| ------------- | ------------| 
| Node name | The name of the node processing the data |
| Status | The operator service status |
| Operational time | The time in which the service is enabled  |
| Processing time | The time measured between the first processed row and the last processed row  |
| Elapsed Time | The elapsed time since the previous call to **get operator summary** command  |
| New rows | Number of rows added since previous call to **get operator summary** |
| Total rows | Number of rows added since the service was enabled |
| New errors | Number of errors since previous call to **get operator summary** |
| Total errors | Number of errors since the service was enabled |
| Avg. rows/sec | The **Total rows** divided by the **Processing time**  |

**Note:** reset the Summary statistics using the **reset stats** command:

```anylog
reset stats where service = operator and topic = summary
```

**Get Operator JSON**:

| Attribute name | Details  |
| ------------- | ------------| 
| DBMS | The name of the dbms associated with data |
| Table | The name of the table associated with data |
| Files | The number of JSON files processed |
| Immediate | The number of files processed with immediate flag |
| Elapsed time | The time since the last file processed |


**Get Operator SQL**:

| Attribute name | Details  |
| ------------- | ------------| 
| DBMS | The name of the dbms associated with data |
| Table | The name of the table (or partition if used) associated with data |
| Files | The number of SQL files processed |
| Immediate | The number of files processed with immediate flag |
| Elapsed_time | The time of the last file processed |

**Get Operator Inserts**:

| Attribute name | Details  |
| ------------- | ------------| 
| DBMS | The name of the dbms associated with data |
| Table | The name of the table associated with data |
| First Timestamp | The timestamp of the first insert to the table |
| Last Timestamp | The timestamp of the last insert to the table |
| First Insert | The elapsed time from the first insert |
| Last Insert | The elapsed time from the last insert |
| Batch Inserts | The number of rows inserted in a buffered mode |
| Immediate Inserts | The number of rows inserted in an immediate mode |

**Get Operator Error**:

| Attribute name | Details  |
| ------------- | ------------| 
| Type | processing mode: JSON or SQL  |
| Counter | The number of errors |
| Timestamp | The timestamp of the last error |
| DBMS Name | The DBMS name associated with the last error |
| Table Name | The table name associated with the last error |
| Last Error | The ID of the last error |
| Last Error Text | The error text message |

## Continuous monitoring of the Operator service

Details are available in the
[continuous command section](monitoring%20nodes.md#monitoring-nodes-operations)


