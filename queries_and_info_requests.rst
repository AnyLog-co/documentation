# Issuing requests and info requests to the AnyLog Network

Queries (and info requests) can be issued from any REST client to the AnyLog Network. Any node member of the network can be configured to serve as a REST server to satisfy client requests. 

## The server side:

Configuring a node is by issuing an AnyLog command: 
```
	run rest server [host] [port] [timeout]
```
Whereas host and port are the connection information and the timeout value represent the max time that a request will wait for a query reply (the default is 20 seconds).

## The client side:

Using a REST client, connect to a network node configured to provide REST services. 
There are 2 types of commands that can be issued: Info commands and SQL commands. 
Info commands provide info on the status and metadata and SQL commands are queries issued to the network.

Requests are done using the GET command with keys and values in the headers as detailed below.

#### Status Requests:
To retrieve the status of the node:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   info
details                get status
</pre>

To retrieve the last executed query:
<pre>
Header Key             Header Value            
--------------         ------------------
type                   info
details                job status
</pre>

To retrieve the last executed queries:
<pre>
Header Key             Header Value            
--------------         ------------------
type                   info
details                job status all
</pre>

#### Metadata Requests:
To retrieve the list of tables in a database:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   info
dbms                   [the logical database name]
details                info dbms [the logical database name] tables
</pre>

To retrieve columns info of a particular table:
<pre>
Header Key             Header Value            
--------------         ------------------
type                   info
dbms                   [the logical database name]
details                info table [the logical database name] [the logical table name] columns
</pre>

#### SQL Queries:
To issue a SQL query:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   sql
dbms                   [the logical database name]
details                [a sql query]
</pre>

## SQL supported:

##### On the projection list:
* Column name
* Min
* Max
* Sum
* Count
* Avg
* Count Distinct
* Range
* Time functions over Column values

#### On the where clause
* Greater than
* Less than
* Equal
* Not Equal
* Group By
* Order By
* Limit

## Optimized time series data queries:

The following proprietry functions can be used:
```
period (time-interval, units, date-time, date-column, filter-criteria)
```
The **period** function finds the first occurrence of data before or at a specified date (and if a filter-criteria is 
specified, the occurrence needs to satisfy the filter-criteria) and considers the readings
in a period of time which is measured by the type of the time interval (Minutes, Hours, Days, Weeks, Months or Years)
and the number of units of the time interval (i.e. 3 days - whereas **time-interval** is day and **unit** is 3).

**date-column** is the column name of the column that determines the date and time to consider.
**period** determines the last occurrence which is smaller or equal to the **date-time**.
The **time-interval** and the **units** (of time-interval) determine the time range to consider.
**filter-criteria** is optional. If provided, the data considered needs to satisfy the filter criteria.


```
increments (time-interval, units, date-column)
```
The **increments** functions considers data in increments of time (i.e. every 5 minutes) within a time range 
(i.e. between October 15 2019 and October 16 2019). 

**date-column** is the column name of the column that determines the date and time to consider.
The **time-interval** and the **units** (of time-interval) determine the time increments to consider (i.e. every 2 days) 
and the time-range is determined in the where clause.

Examples:

1) Consider the last minute of reading from ping_sensor  
```
select  max(timestamp), avg(value) from ping_sensor where period ( minute, 1, now(), timestamp) 
```
This query provides the max and avg values of the last minute of the last reading.

2) Consider the last minute of reading prior to the specified date and time  
```
select  max(timestamp), avg(value) from ping_sensor where period ( minute, 1, '2019-09-29 19:34:09', timestamp)
```
This query provides the max and avg values of the last minute of the last reading prior to 2019-09-29 19:34:09'.

3) Consider the last day of readings prior to the specified date of ping_sensor with filter criteria  
```
select  max(timestamp), avg(value) from ping_sensor where period ( minute, 1, '2019-09-29 19:34:09', timestamp, and device_name = 'APC SMART X 3000')
```
This query will find the last reading prior to the specified date and where the device name is  'APC SMART X 3000'

4) Consider time range and provide the trend in time increments 
```
SELECT increments(minute, 5,timestamp), max(timestamp), avg(value) from ping_sensor where timestamp >= '2019-06-01 19:34:09' and timestamp < '2019-09-29 19:34:09';```
```
This query will provide the max and avg values every 5 minutes between the specified dates and times.
