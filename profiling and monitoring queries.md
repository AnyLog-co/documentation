# Profiling and Monitoring Queries

Queries are profiled and monitored by issuing commands on the AnyLog command prompt or from a REST client.
These commands monitor and track the executes queries and allow:
a. information on queries execution time.  
b. identifying slow queries.  
c. identifying the SQL used on each participating node and the execution time on exery participating node.

## Statistical information
In order to get statistical information, use the following command to get a summary of the execution time of queries:  
```anylog
get queries time
```
An example reply is below:
```anylog
Up to  1 sec.: 43
Up to  2 sec.: 12
Up to  3 sec.: 5
Up to  4 sec.: 1
Up to  5 sec.: 0
Up to  6 sec.: 0
Up to  7 sec.: 0
Up to  8 sec.: 0
Up to  9 sec.: 0
Over   9 sec.: 0
Total queries: 4
Time interval: 231 (sec.) : 0:3:51 (H:M:S)
```

Use the following command to reset the statistical information:
```anylog
reset query timer
```

## Identifying slow queries

Slow queries can be redirected to the query log with the following AnyLog command:  
```anylog
set query log profile [n] seconds
```

The  `set query log on` records all queries in the query log whereas adding `profile [n] seconds` places in the query 
log only queries with execution time greater or equal to [n] seconds.

The following example places queries with execution time of 5 seconds or higher in the query log:
```anylog
set query log profile 5 seconds
```

To view the slow query log use the following command on the AnyLog command prompt: 
```anylog
get query log
```

Additional details are available in the [Query Log](../monitoring/logging%20events.md#the-query-log) section.

## Command options for monitoring queries

When a query is executed, it triggers a process that maintains information on the status of the query.  
The information details, for each executed query, the nodes (Operators) that participate in the query, the amount
of data transferred and execution time.

The command that starts with the key _query_, returns the query execution information.  
As multiple queries are processed on each node concurrently, each query is assigned with an ID that identifies the query.

The command _query_ provides information on the last executed queries and is issued on the Query Node.  
Use the command [get operator execution](#retrieving-the-status-of-queries-being-processed-on-an-operator-node) to monitor the 
execution of the query on the Operator side. 

Usage:
```anylog
query [operation] [id/all] 
```
 
Operations are detailed below:

| Operation   | Command           | Details                                 |
|-------------|-------------------|-----------------------------------------| 
| status      | query status      | The status of each executed query       |
| destination | query destination | The participating Operator Nodes        |
| explain     | query explain     | The SQL executed on the local databases |

id / all - are optional parameters:
* If not provided - the information on the last executed query is returned. 
* If ID is provided - the information associated with the job ID is returned.
* ALL - The information in the currently executed and recently executed queries are returned.
  
Note: The query status information is maintained in a stack, old information is removed.

### Example : query status  
The info below is returned when a `query status` command is issued.   
It details how the query was executed on each participating node: 
```anylog
AL > query status

Job  ID Output   Run Time Operator              Par Status    Blocks Rows Command
----|--|--------|--------|---------------------|---|---------|------|----|----------------------------------------------------------------------------------------------------|
0009|10|['rest']|00:00:01|All                  |---|Completed|     2|   0|select  increments(minute, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as m|
    |  |        |        |                     |   |         |      |    |ax_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value from ping_sensor wh|
    |  |        |        |                     |   |         |      |    |ere timestamp >= NOW() - 1hour GROUP BY device_name ORDER BY min_ts DESC                            |
    |  |        |00:00:00|172.105.112.207:32148|  0|Completed|     1|   0|                                                                                                    |
    |  |        |00:00:00|                     |  1|Completed|     1|   0|                                                                                                    |
    |  |        |00:00:00|172.105.13.202:32148 |  0|Completed|     1|   0|                                                                                                    |
    |  |        |00:00:00|                     |  1|Completed|     1|   0|                                                                                                    |
```

Attributes returned:

| Attribute  | Details                                                                     |
|------------|-----------------------------------------------------------------------------| 
| Job        | A slot number to contain the query info (500 by default).                   | 
| ID         | A Unique ID of the query.                                                   |
| Output     | Where the query output is directed: stdout, rest, DBMS table, file, kafka   |
| Run Time   | Total time and reply time of each Operator Node by partition.               |
| Operator   | The IP and Port of each participating Operator.                             |
| Par        | The Partition ID on each Operator.                                          |
| Status     | The status of each participating Operator and Partition (see details below) |
| Blocks     | The nuber of blocks returned.                                               |
| Rows       | The number of rows returned.                                                |
| Command    | The Query or Pushdown Function executed.                                    |

Status options:
* **Completed** - Reply is completed
* **Sending** - Message being sent
* **Delivered** - Message send without an Operator reply
* **Processing** - Operator is in the process of returning data
* **Empty Set** - No data satisfies the query
* **Error** - Operator returned an error

### Example : query destination
The example below details the destination nodes of the query.
```anylog
AL +> query destination

Job Destination           DBMS          Table                Command
---|---------------------|-------------|--------------------|----------------------------------------------------------------------------------------------------|
  9|172.105.112.207:32148|litsanleandro|ping_sensor         |select  increments(minute, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as m|
   |                     |             |                    |ax_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value from ping_sensor wh|
   |                     |             |                    |ere timestamp >= NOW() - 1hour GROUP BY device_name ORDER BY min_ts DESC                            |
   |172.105.13.202:32148 |litsanleandro|ping_sensor         |                                                                                                    |
```

### Example : query explain
The example below details the SQL processed on each participating database:


```anylog
AL +> query explain

Job ID        |                                         0|
Remote DBMS   |lsl_demo                                  |
Remote Table  |ping_sensor                               |
Source Command|select count(*) from ping_sensor          |
Remote Query  |select count(*) from ping_sensor          |
Local Create  |create table query_0 (count_all integer );|
Local Query   |select sum(count_all) from query_0        |
```

Attributes returned:

| Attribute      | Details                                                                                       |
|----------------|-----------------------------------------------------------------------------------------------| 
| Remote DBMS    | The logical database name  on the Operator Nodes                                              | 
| Remote Table   | The logical table name  on the Operator Nodes                                                 |
| Source Command | The use SQL or pushdown function                                                              |
| Remote Query   | The SQL executed on the database node                                                         |
| Local Create   | The create statement on the Query Node to create a table to host intermediary result sets     |
| Local Query    | The SQL statement executed on the Query node which represents the result returned to the user |


## Retrieving the status of queries being processed on an Operator node

Each operator can process many concurrent queries.  
Queries statistics are returned in the same way they are returned on the Query Node.  
Use the following command to retrieve the statistics or log queries in the **query log**:
```anylog
get queries time
```
See details in the [get queries time](#statistical-information) section.

### Details on the execution of a query in the operator node 

The command `get operator execution` provides the info on the processed queries.  
Usage:
```anylog
get operator execution where node = [node id] and job = [job id]
```

[node id] is the IP of the Query Node (the node that issued the query).  
[job id] is the id of the job assigned by the Query Node (the command `query status` on the query node provides the job id).

If **node id** and **job id** are not provided, all recently executed queries information is provided.  
If only **node id** is provided, the query information of the specified node is provided.  

**Examples usage**:
```anylog
 get operator execution where node = 10.0.0.78 and job = 12
 get operator execution where node = 10.0.0.78
 get operator execution
``` 

**Notes**:
1) The **get operator execution** command provides the Operator side information and is associated with the [query status](#command-options-for-monitoring-queries) call that is executed on the Query Node. 
2) The information is maintained in a stack, old information is removed.

Example:

The following query is executed on the query node:
```anylog
run client () sql lsl_demo format = table "select count(*) from ping_sensor"
```

The CLI returns **[2]** followed by the query result.  
The number 2 in brackets represents the Job ID, which can show how the query was executed:
```anylog
query status 2
```
Users can issue **query status** without the Job ID to see the info on the last query executed. Below is an example:

````anglog
AL +> query status

Job  ID Output     Run Time Operator       Par Status    Blocks Rows Command
----|--|----------|--------|--------------|---|---------|------|----|--------------------------------|
0001| 2|['stdout']|00:00:00|All           |---|Completed|     3|   3|select count(*) from ping_sensor|
    |  |          |00:00:00|10.0.0.78:7848|  0|Completed|     1|   1|                                |
    |  |          |00:00:00|              |  1|Completed|     1|   1|                                |
    |  |          |00:00:00|              |  2|Completed|     1|   1|                                |

````
With this info, users can retrieve details on the execution of the query from the participating Operator Nodes:

````anglog
AL +> run client 10.0.0.78:7848 get operator execution where node = 10.0.0.85 and job = 1

[From Node 10.0.0.78:7885]


Node      Job ID Rows limit threads Completed DBMS     Table       Par ID Par Name                                 Error blocks Rows SQL Time Fetch Time Network Time
---------|---|--|----|-----|-------|---------|--------|-----------|------|----------------------------------------|-----|------|----|--------|----------|------------|
10.0.0.78|  1| 2|   3|    0|      3|        3|lsl_demo|ping_sensor|     1|par_ping_sensor_2019_11_01_d07_timestamp|    0|     1|   1|00:00:00|00:00:00  |00:00:00    |
         |   |  |    |     |       |         |lsl_demo|ping_sensor|     2|par_ping_sensor_2020_10_01_d07_timestamp|    0|     1|   1|00:00:00|00:00:00  |00:00:00    |
         |   |  |    |     |       |         |lsl_demo|ping_sensor|     0|par_ping_sensor_2019_10_01_d07_timestamp|    0|     1|   1|00:00:00|00:00:00  |00:00:00    |

````

Attributes returned:

| Attribute    | Details                                                                            |
|--------------|------------------------------------------------------------------------------------| 
| Node         | The IP of the node that issued the query                                           | 
| Job          | The job ID                                                                         |
| ID           | A unique Query ID (on the query node)                                              |
| Rows         | The total number of rows returned                                                  |
| Limit        | A limit value incuded in the query                                                 |
| Threads      | Number of query threads participated in the query                                  |
| DBMS         | The logical dbms name                                                              |
| table        | The logical table name                                                             |
| Par ID       | The partition ID participating in the query                                        |
| Par Name     | The name of the partition                                                          |
| Error        | 0 represents no error and a value is the error number returned from each partition |
| Blocks       | The number of data blocks delivered to the app by each partition                   |
| Rows         | The number of data rows retrieved from the database by each partition              |
| SQL Time     | The physical database execution time                                               |
| Fetch Time   | The processing time (including the database time) in the operator node             |
| Network Time | The operator time to send the data blocks (high value indicates a busy Query Node) |


## Profiling

Profiling requires to start the AnyLog instances with a system variable **PROFILER** set to **TRUE**.
The system variable will trigger the load of the profiling libraries.

The profiler is assigned to the needed processes using the following command:

```anglog
set profiler [on/off] where target = [process name]
```
The profiler output is retrieved using the following command:
```anglog
get profiler output where target = [process name]
```
Processes that are profiled are detailed in the chart below:

| Process Name | Details                                   |
|--------------|-------------------------------------------| 
| operator     | Profile data inserts in the Operator node | 
| get          | Profile REST GET                          |
| put          | Profile REST PUT                          |
| post         | Profile REST POST                         |


### Example:
Set environment Variable: ```PROFILER=true```

```anglog
set profiler on where target = operator         # Start operator profiling
set profiler off where target = operator        # Stop profiling
get profiler output where target = operator     # Get profiling output
```
