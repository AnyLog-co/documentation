# Monitoring calls from external applications

## REST server configuration
The command ***get rest server info*** provides the info on how the REST server is configured.

Usage: 
<pre>
get rest server info
</pre>

Explanation output:

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

The ***get rest calls*** command returns statistics on the REST calls issued and their execution results.

Usage: 
<pre>
get rest calls
</pre>

Example reply:
<pre>
Statistics
Caller Call Processed Errors Last Error              First Call          Last Call           Last Caller
------|----|---------|------|-----------------------|-------------------|-------------------|---------------|
anylog|GET |        3|     1|Error Command Structure|2021-11-24 13:29:01|2021-11-24 13:29:19|10.0.0.78:50183|
      |POST|        4|     0|                       |2021-11-24 13:29:08|2021-11-24 13:29:24|10.0.0.78:50185|
</pre>


## Get Streaming

Information on data provided via REST APIs and message brokers is distributed to the different tables that are hosted by the node.

Usage: 
<pre>
get streaming
get streaming format = json
</pre>

The reply has 2 parts showing configurations and statistics.

***Part A attributes:***
| Attribute name | Details  |
| ------------- | ------------| 
| Default time | The threshold time to flush the buffers (the default value for tables that are not assigned with time) |
| Default volume | The threshold volume to flush the buffers (the default value for tables that are not assigned with volume)|
| Default Immediate | If Immediate write is set as the default value for all tables |
| Buffered Rows | The total number of rows placed in the streaming buffers |
| Flushed Rows | The total number of rows added to databases |

***Part B attributes:***

| Attribute name | Details  |
| ------------- | ------------| 
| DBMS-Table | The Database and table associated with the data |
| File Put | Counter for PUT calls to add file data |
| File Rows | Counter for rows within the files added |
| Streaming Put | Counter of PUT calls to add rows to the streaming buffers |
| Streaming Rows | Counter for rows added to the streaming buffers |
| Immediate | Counter for rows added to the databases without buffer wait |
| Last Process | Last process return value |


