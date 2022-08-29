# Query nodes in the network
The ***run client ()*** ([detailed below](#network-processing)) directs the query to the relevant nodes in the network. If the parenthesis are left empty, all the nodes 
with the tables' data receive and process the query. Users can detail specific nodes of interest in providing their IP and Ports.  
  
## Query options
The query options are instructions on the format and target location for the result set. The query options are expressed as key = value pairs.
With multiple option, the keyword ***and*** separates between each key value pair.

| key  | Values Options  | Details     | Default Value |
| ---- | --------------- | ------------| --------------|
| format | json / table | The format of the result set | JSON |
| timezone | utc / local | Timezone used for time values in the result set | local |
| include | dbms.table | Allows to treat remote tables with a different name as the table being queried. The value is specified as ***dbms.table***. | ignored |
| drop | True/False | Drops the local output table with the issued query. | True |
| dest | stdout / rest / dbms / file | Destination of the query result set (i.e. stdout, rest, file) | Set dynamically depending on the interface used |
| file | file name | File name for the output data |  |
| table | table name | A table name for the output data. | random table names are assigned to each executing query |
| stat | True/False | Adds processing statistics to the query output | True |
| test | True/False | The output is organized as a test output | False |
| source | file name | A file name that is used in a test process to determine the processing result |  |
| title | a query title | Added to the test information in the test header |  |
| max_time   | Cap the query execution time.  | |
| extend     | Include node variables (which are not in the table data) in the query result set. Example: extend = (@ip, @port.str, @DBMS, @table, !disk_space.int).  | |


### Timezones
Timezones can be a timezone from the [list of tz database timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).   
in addition, timezone can be expressed using the following keys:  
* utc - UTC timezone
* local - The local timezone on the AnyLog node that is processing the query
* pt - Pacific Time (same as "America/Los_Angeles")
* mt - Mountain Time (same as "America/Denver")
* ct - Central Time (same as America/Chicago")
* et - Eastern Time (same as "America/New_York")

The default timezone is local. Therefore, when queries are executed and timezone is not specified, results are returned using the timezone 
of the AnyLog node executing the query.   
If the query is provided by a REST call, the node that executes the query is the node receiving the REST call (and the local timezone is determined by this node).  
Users can determine the local timezone on a node using the command:
<pre> 
get timezone info
</pre> 
Users can validate a timezone using the command [get datetime](#get-datetime-command).

### Output format
The key ***format*** determines the output format.
The following chart summarizes the optional values:

| value  | Explanation |
| ---- | ------------------------------------------------------------------------ |
| json | The default value - a json structure whereas the output data is assigned to the key "Query" and if statistics is enabled, it is assigned to the key "Statistics".  |
| json:output | The output is organized in rows whereas each row is a JSON structure - this format is identical to the data load structure. |
| json:list | The output is organized in a list, every entry in the list represents a row (use this format with PowerBI).  |
| table | The output is organized as a table.  |

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

WIth the first example below, the query process considers all the nodes with relevant data. With the second example, only the specified nodes are participating n the query process:
<pre> 
run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor limit 100"
run client (24.23.250.144:7848, 16.87.143.85:7848) sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor limit 100"
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

Examples:
<pre>
timestamp('now','start of month','+1 month','-1 day', '-2 hours', '+2 minutes')
date('now','start of month','-2 month','+ 3 days', '-5 hours', '+1 minute')
</pre>

The function ***now()*** is converted to the current day-time string.   
The function ***date()*** is converted to the current date string.  

The following values and keywords pairs (prefixed by + or - signs) can be used to modify a date-time function or string.  
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

Time units can be also represented by the first character of the unit name. For example: ***+3d*** is equivalent to ***+ 3 days***.
Minutes is assigned with the character ***t*** to differentiate from a month.
The following examples are equivalent and represents 4 minutes before the current time:  
<pre>
-4t
now() -4t
now() -4 minutes
</pre>

#### Examples

<pre>
run client () sql lsl_demo "select min(value) from ping_sensor where reading_time >= now() -3d and time < now());"
run client (!ip 2048) sql lsl_demo "select * from ping_sensor where reading_time = date('now','start of month','+1 month','-1 day', '-2 hours', '+2 minuts');"    
run client (!ip 2048) sql lsl_demo "select * from ping_sensor where reading_time = timestamp('2020-05-28 18:56:49.890199','+1 month','-1 day', '-2 hours', '+2 minuts');"
</pre>

## Cast Data
Cast allows to map the projected data to a different format.  
Casting is applied by adjacent double semicolons (::) to the projected column name.  
For example, the SQL statement below projects the value in the column ***speed*** as a float rounded to 2 digits after the decimal point:
<pre>
run client () sql lsl_demo "select reading_time, speed::float(2) from performance where reading_time >= now() -3d;"
</pre>

The casting options are detailed in the table below:

| Cast  | details |
| ---- | -----------------|
| float(x) | Cast to a ***float*** value. X represents rounding to x digits after the decimal point. Adding the percent sigh ***%*** before the digits adds comma separation and padding zeros|
| int | Cast to an ***int***. |
| str | Cast to a ***string***. |
| ljust(x) | Cast to a ***left-justified string*** with a given x bytes width.  |
| rjust(x) | Cast to a ***right-justified*** string with a given x bytes width.  |
| format(formatting type) | Apply formating instructions on the column value.  |

Note: multiple casting is allowed.  
Examples:
<pre>
run client () sql lsl_demo "select reading_time, speed::int::format(":,") from performance where reading_time >= now() -3d;"
</pre>
The example above represents the speed as an int and formats the speed value with commas. 
<pre>
run client () sql lsl_demo "select reading_time, speed::float("%3") from performance where reading_time >= now() -3d;"
</pre>
The example above represents the speed as a float, rounded to 3 digits with commas as a thousand separators and padded with zeros.
This has the same result as formatting with the formatting string: ***:,.03f***.


The following chart provides formatting types options:

| Type  | details |
| ---- | -----------------|
| :, | Use a comma as a thousand separator |
| :b | Binary format |
| :x | Hex format |
| :o | Octal format |
| :e | Scientific format |
| :+ | Places the plus sign to the left most position |

The following examples provide number formatting with padding for int and float:
| Example  | details |
| ---- | -----------------|
| :.3f | float with digits length  |
| :08.3f | float with padding zeros  |
| :8d | int with padding zeros  |

The following queries provides fill formatting examples:
<pre>
run client () sql lsl_demo format = table "select count(*)::str::format(0:*>8s)  from ping_sensor"

count(*)
--------
******21
</pre>

<pre>
run client () sql lsl_demo format = table "select count(*)::format(0:#<8d)  from ping_sensor"

count(*)
--------
21######
</pre>

<pre>
run client () sql lsl_demo format = table "select count(*)::str::format(0:*^8s) from ping_sensor"

count(*)
--------
***21***
</pre>



## Get datetime command
Using the command ***get datetime*** users can translate a date-time function to the date-time string.  
Usage:
<pre>
get datetime timezone [date-time function]
</pre>

***[date-time function]*** is the function used to derive the date-time string.

#### Examples:
<pre>
get datetime et now()
get datetime Europe/London now()
get datetime local now() + 3 days
get datetime utc date() + 2 days
get datetime local timestamp('now','start of month','+1 month','-1 day', '-2 hours', '+2 minutes')
get datetime Asia/Shanghai timestamp('now','start of month','+1 month','-1 day', '-2 hours', '+2 minutes')
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

