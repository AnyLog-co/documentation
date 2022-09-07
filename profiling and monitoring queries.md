# Profiling and Monitoring Queries

Queries are profiled and monitored by issuing commands on the AnyLog command prompt or from a REST client.

Profiling is supported by several processes:  
a. a process providing statistical information on queries execution time.  
b. a process identifying slow queries.  
c. a process to identify the SQL used on each participating node.  

## Statistical information
In order to get statistical information, use the following command to get a summary of the execution time of queries:  
<pre>
get queries time
</pre>

## Identifying slow queries

Slow queries can be redirected to the query log with the following AnyLog command:  
<pre>
set query log profile [n] seconds
</pre>


The  ***set query log on*** records all queries in the query log whereas adding ***profile [n] seconds***
places in the query log only queries with execution time greater or equal to [n] seconds.

To view the slow query log use the following command on the AnyLog command prompt: 
<pre>
get query log
</pre>

more details are available at [The Query Log](https://github.com/AnyLog-co/documentation/blob/master/logging%20events.md#the-query-log) section.

## Command options for monitoring queries

Queries are executed in a context of jobs. A job is a process that communicates with a peer or peers in the network.  
When a job is executed, it triggers a process that maintains information on the status of the message and the execution status.

The command ***query*** considers the queries that are sent to peers in the network. 
As multiple jobs are processed on each node concurrently, each job (including a query) is assigned with an ID which identifies the job.

The command ***query*** provides information on the last executed queries.

Usage:
<pre>
query [operation] [id/all] 
</pre>
 
Operation is one of the following:
* status - the query status
* explain - the generated queries that are processed on each participating node.
* destination - the list of nodes participating in each table
* id / all - these are optional parameters:
    - If not provided - the information on the last executed query is returned. 
    - If ID is provided - the information associated with the job ID is returned.
    - ALL - The information in the currently executed and recently executed queries are returned.
    
Examples:  
The info below is returned when a ***query status*** command is issued.  
It provides the ID of the query, the destination (Operators) nodes and the process status with each Operator node.  
It details the execution time, and a breakdown to the processing time of each operator. 
<pre>
AL > query status

Job  ID Output   Run Time Operator              Par Status    Blocks Rows Command
----|--|--------|--------|---------------------|---|---------|------|----|----------------------------------------------------------------------------------------------------|
0009|10|['rest']|00:00:01|All                  |---|Completed|     2|   0|select  increments(minute, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as m|
    |  |        |        |                     |   |         |      |    |ax_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value from ping_sensor wh|
    |  |        |        |                     |   |         |      |    |ere timestamp >= NOW() - 1hour GROUP BY device_name ORDER BY min_ts DESC                            |
    |  |        |00:00:00|172.105.112.207:32148|  0|Completed|     1|   0|                                                                                                    |
    |  |        |00:00:00|                     |  1|Completed|     1|   0|                                                                                                    |
    |  |        |00:00:00|172.105.13.202:32148 |  0|Completed|     1|   0|                                                                                                    |
    |  |        |00:00:00|                     |  1|Completed|     1|   0|                                                                                                    | |
</pre>

The example below details the destination nodes of the query.
<pre>
AL +> query destination

Job Destination           DBMS          Table                Command
---|---------------------|-------------|--------------------|----------------------------------------------------------------------------------------------------|
  9|172.105.112.207:32148|litsanleandro|ping_sensor         |select  increments(minute, 1, timestamp), device_name, min(timestamp) as min_ts, max(timestamp) as m|
   |                     |             |                    |ax_ts, min(value) as min_value, avg(value) as avg_value, max(value) as max_value from ping_sensor wh|
   |                     |             |                    |ere timestamp >= NOW() - 1hour GROUP BY device_name ORDER BY min_ts DESC                            |
   |172.105.13.202:32148 |litsanleandro|ping_sensor         |                                                                                                    |
</pre>

## Retrieving the status of queries being processed on an Operator node

Each operator can process many concurrent queries.  
The command ***get operator execution*** provides the info on the currently processed queries.  
Usage:
<pre>
get operator execution where node = [node id] and job = [job id]
</pre>

[node id] is the IP of the Operator Node.  
[job id] is the id of the query assigned by the Query Node (the command ***query status*** on the query node provides the job id).

If ***node id*** and ***job id*** are not provided, all recently executed queries information is provided.  
If only ***node id*** is provided, the query information of the specified node is provided.  

Examples:
<pre>
 get operator execution where node = 10.0.0.78 and job = 12
 get operator execution where node = 10.0.0.78
 get operator execution
</pre> 

Notes:
1) The call can be compared with the ***query status*** cam executed on the Query Node. 
2) The information is maintained in a stack, old information is removed.