# Profiling and Monitoring Queries

Queries are profiled and monitored by issuing commands on the AnyLog command prompt or from a REST client.

Profiling is supported by several processes:  
a. a process providing statistical information on queries execution time.  
b. a process identifying slow queries.  
c. a process to identify the SQL used on each participating node.  

## Statistical information
In order to get statistical information, use the following command to get a summary of the execution time of queries:  
```anylog
get queries time
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


The  `set query log` on records all queries in the query log whereas adding `profile [n] seconds` places in the query 
log only queries with execution time greater or equal to [n] seconds.

To view the slow query log use the following command on the AnyLog command prompt: 
```anylog
get query log
```

more details are available at [The Query Log](../monitoring/logging%20events.md#the-query-log) section.

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
 
Operation is one of the following:
* status - the query status
* explain - the generated queries that are processed on each participating node.
* destination - the list of nodes participating in the query (and associated to the data tables that are queried).
* id / all - these are optional parameters:
    - If not provided - the information on the last executed query is returned. 
    - If ID is provided - the information associated with the job ID is returned.
    - ALL - The information in the currently executed and recently executed queries are returned.
  
Note: The query status information is maintained in a stack, old information is removed.

Examples:  
The info below is returned when a `query status` command is issued.  
It provides the ID of the query, the destination (Operators) nodes and the process status with each Operator node.  
It details the execution time, and a breakdown to the processing time of each operator. 
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

## Retrieving the status of queries being processed on an Operator node

Each operator can process many concurrent queries.  
The command `get operator execution` provides the info on the currently processed queries.  
Usage:
```anylog
get operator execution where node = [node id] and job = [job id]
```

[node id] is the IP of the Query Node (the node that issued the query).  
[job id] is the id of the job assigned by the Query Node (the command `query status` on the query node provides the job id).

If `node id` and `job id` are not provided, all recently executed queries information is provided.  
If only _node id_ is provided, the query information of the specified node is provided.  

**Examples**:
```anylog
 get operator execution where node = 10.0.0.78 and job = 12
 get operator execution where node = 10.0.0.78
 get operator execution
``` 

**Notes**:
1) The call provides the Operator side information complimentary to the [query status](#command-options-for-monitoring-queries) call that is executed on the Query Node. 
2) The information is maintained in a stack, old information is removed.