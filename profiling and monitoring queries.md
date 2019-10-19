# Profiling and Monitoring Queries

Queries can be profiled and monitored by issueing commands on the AnyLog command prompt or from a REST client.

Queries are executed in a context of jobs. A job contains a query that was executed by a user or application 
with some additional information that can be presented to users by issueing a monitoring command.

By default, job information in maintained for the last 20 executed queries. 
Each job has a unique ID and the commands can present the status of all jobs,
a particular job (by ID) or the last executed job. 

There are 3 types of information captured on every executed query:
1. Status - details the status of each query
2. Explain - Provides the information on how the queries were executed on the operator nodes and on the node that issued the query.
3. Profile - provides profiling information.

## Command options for profiling and monitoring queries

```job status all``` - provides status information on the last executed jobs<br/>
```job status``` - provides status information on the most recent executed job<br/>
```job status n``` - provides status information on a particular job whereas n is the id of the job<br/>

```job explain all``` - provides the explain plan of the last executed jobs<br/>
```job explain``` - provides the explain plan on the most recent executed job<br/>
```job explain n``` - provides the explain plan on a particular job<br/>

```job profile all``` - provides the profiling information of the last executed jobs<br/>
```job explain``` - provides the profiling information on the most recent executed job<br/>
```job explain n``` - provides the profiling information on a particular job<br/>