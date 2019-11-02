# Profiling and Monitoring Queries

Queries are profiled and monitored by issuing commands on the AnyLog command prompt or from a REST client.

Profiling is supported by several processes:  
a. a process providing statistical information on queries execution time.  
b. a process identifying slow queries.  
c. a process to identify the SQL used on each participating node.  

## Statistical information
In order to get statistical information, use the following command:  
On the AnyLog command prompt:  
```show queries time```  
From a REST client send a REST message and place in the headers the following keys and values:  
```type : info```  
```details : show queries time```

## Identifying slow queries

Slow queries can be redirected to the query log with the following AnyLog command:  

```set query log profile [n] seconds```   

The  ***set query log*** records all queries in the query log whereas adding ***profile [n] seconds***
places in the query log only queries with execution time greater or equal to [n] seconds.

To view the slow query log use the following command on the AnyLog command prompt:  
```show query log```  
From a REST client send a REST message and place in the headers the following keys and values:  
```type : info```  
```details : show query log```

## Identify the SQL used on each participating node

Queries are executed in a context of jobs. A job contains a query that was executed by a user or application 
with some additional information that can be presented to users by issueing a monitoring command.

By default, job information in maintained for the last 20 executed queries. 
Each job has a unique ID and the commands can present the status of all jobs,
a particular job (by ID) or the last executed job. 

There are 3 types of information captured on every executed query:
1. Status - details the status of each query
2. Explain - Provides the information on how the queries were executed on the operator nodes and on the node that issued the query.
3. Profile - provides profiling information.

### Command options for profiling and monitoring queries

```job status all``` - provides status information on the last executed jobs<br/>
```job status``` - provides status information on the most recent executed job<br/>
```job status n``` - provides status information on a particular job whereas n is the id of the job<br/>

```job explain all``` - provides the explain plan of the last executed jobs<br/>
```job explain``` - provides the explain plan on the most recent executed job<br/>
```job explain n``` - provides the explain plan on a particular job<br/>

```job profile all``` - provides the profiling information of the last executed jobs<br/>
```job explain``` - provides the profiling information on the most recent executed job<br/>
```job explain n``` - provides the profiling information on a particular job<br/>