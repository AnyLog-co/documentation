# Queries 

Queries can be executed against data maintained on the local node and on data maintained by nodes in the network.    
The command ***sql*** directs the node to process a query. The command format is detailed below: 
<pre> 
sql [dbms name] [query options] [select statement]
</pre>  
* ***[dbms name]*** is the logical DBMS containing the data.
* ***[query options]*** include formatting instructions and output directions.
* ***[select statement]*** is a query using a supported format.
* ***run client ()*** ([detailed below](#network-processing)) directs the query to the relevant nodes in the network. If the parenthesis are left empty, all the nodes 
with the tables' data receive and process the query. The parenthesis can detail specific nodes of interest.  

## Query options
The query options are instructions on the format and target location for the result set. The query options are expressed as key = value pairs.
With multiple option, the keyword ***and*** seperates between each key value pair.

| key  | Values Options  | Details     | Default Value |
| ---- | --------------- | ------------| --------------|
| format | json / table | The format of the result set | JSON |
| timezone | utc / local | timezone used for time values in the result set | local |
| include | dbms.table | allows to treat remote tables with a different name as the table being queried | ignored |
| drop | True/False | drop local output table when new query starts | True |
| dest | stdout / rest / dbms / file | destination of result set | stdout |
| file | file name | file name for the output data |  |
| table | table name | table name for the output data | random table names are assigned to each executing query |

### Network processing
Without the ***run client*** directive, the query will be executed on the local node.  
Executing a query against all the nodes in the network with the relevant data is by adding the ***run client ()*** as a command prefix.     
The ***run client*** directive delivers the query to the target nodes specified in the parenthesis. If target nodes are not specified, 
the network protocol will determine the target nodes from the metadata layer and the query will be processed by evaluating the data in 
all the relavant nodes.  
The format for a network query is the following:
<pre> 
run client () sql [dbms name] [query options] [select statement]
</pre> 

Example:
<pre> 
run client () sql litsanleandro format = table "select count(*), min(value), max(value) from ping_sensor"
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

## Time Functions

The WHERE condition can include functions that manipulate time.
The following functions are supported:

<pre>
date
timestamp
</pre>

The following modifiers are supported:

<pre>
start of year
start of month
start of day
</pre>

The keyword ***now*** is converted to the current day-time string.  

The following values and keywords pairs (values including + or - signs) can be used to modify time.  
The plural 's' character at the end of the modifier names is optional. 

<pre>
X seconds
x minutes
x hours
x weeks
x days
x months
x years
</pre>

Time units can be also represented by the first character of the unit name. For example: +3d is equivalent to + 3 days.
Minutes is assigned with the character ***t*** to differentiate from a month.
The following example represents 4 minutes before the current time:  
<pre>
-4t
</pre>
This above example is equivalent to:
<pre>
now() -4t
</pre>

#### Examples

<pre>
run client () sql lsl_demo "select min(value) from ping_sensor where reading_time >= now() -3d and time < now());"
run client (!ip 2048) sql lsl_demo "select * from ping_sensor where reading_time = date(date('now','start of month','+1 month','-1 day', '-2 hours', '+2 minuts'));"    
run client (!ip 2048) sql lsl_demo "select * from ping_sensor where reading_time = timestamp('2020-05-28 18:56:49.890199','+1 month','-1 day', '-2 hours', '+2 minuts');"
</pre>


## Datetime command
Using the commmand ***datetime*** users can translate a date-time function to the date-time string.  
Usage:
<pre>
datetime [utc] [date-time function]
</pre>
***[utc]*** is an optional string to convert the function to UTC time
***[date-time function] is the function used to derive the date-time string.

#### Examples:
<pre>
datetime now() + 3 days
datetime date('now','start of month','+1 month','-1 day', '-2 hours', '+2 minutes')
</pre>

  
## Optimized time series data queries:

The following functions optimize queries over time-series data:

### The Period Function
Usage:
<pre>
period (time-interval, units, date-time, date-column, filter-criteria)
</pre>
The **period** function finds the first occurrence of data before or at a specified date (and if a filter-criteria is 
specified, the occurrence needs to satisfy the filter-criteria) and considers the readings
in a period of time which is measured by the type of the time interval (Minutes, Hours, Days, Weeks, Months or Years)
and the number of units of the time interval (i.e. 3 days - whereas **time-interval** is day and **unit** is 3).

**date-column** is the column name of the column that determines the date and time to consider.
**period** determines the last occurrence which is smaller or equal to the **date-time**.
The **time-interval** and the **units** (of time-interval) determine the time range to consider.
**filter-criteria** is optional. If provided, the data considered needs to satisfy the filter criteria.

### The Increment Function
Usage:
<pre>
increments (time-interval, units, date-column)
</pre>
The **increments** functions considers data in increments of time (i.e. every 5 minutes) within a time range 
(i.e. between October 15 2019 and October 16 2019). 

**date-column** is the column name of the column that determines the date and time to consider.
The **time-interval** and the **units** (of time-interval) determine the time increments to consider (i.e. every 2 days) 
and the time-range is determined in the where clause.

#### Examples:

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

