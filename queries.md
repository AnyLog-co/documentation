# Query nodes in the network

The `run client ()` ([detailed below](#network-processing)) directs the query to the relevant nodes in the network. 
If the parenthesis are left empty, all the nodes with the tables' data receive and process the query. Users can detail 
specific nodes of interest by providing their IP and Ports.  
The format of SQL commands is detailed in the [Issuing a SQL command](sql%20setup.md#issuing-a-sql-command-to-a-node-in-the-network) section.  
Query examples are available in the [Query Data](examples/Querying%20Data.md) page.
  
## Query options
The query options are instructions on the format and target location for the result set. The query options are expressed 
as key = value pairs. With multiple option, the keyword _and_ separates between each key value pair.

| key       | Values Options              | Details                                                                                                                                               | Default Value                                           |
|-----------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| format    | json / table                | The format of the result set                                                                                                                          | JSON                                                    |
| timezone  | utc / local                 | Timezone used for time values in the result set                                                                                                       | local                                                   |
| include   | dbms.table                  | Allows to treat remote tables with a different name as the table being queried. The value is specified as `dbms.table`                                | ignored                                                 |
| drop      | True/False                  | Drops the local output table with the issued query.                                                                                                   | True                                                    |
| dest      | stdout / rest / dbms / file | Destination of the query result set (i.e. stdout, rest, file)                                                                                         | Set dynamically depending on the interface used         |
| file      | file name                   | File name for the output data                                                                                                                         |                                                         |
| table     | table name                  | A table name for the output data.                                                                                                                     | random table names are assigned to each executing query |
| stat      | True/False                  | Adds processing statistics to the query output                                                                                                        | True                                                    |
| test      | True/False                  | The output is organized as a test output                                                                                                              | False                                                   |
| source    | file name                   | A file name that is used in a test process to determine the processing result                                                                         |                                                         |
| title     | a query title               | Added to the test information in the test header                                                                                                      |                                                         |
| max_time  | Number of seconds           | Cap the query execution time.                                                                                                                         |                                                         | 
| extend    | True/False                  | Include node variables (which are not in the table data) in the query result set. Example: extend = (@ip, @port.str, @DBMS, @table, !disk_space.int). |                                                         |
| topic     | A topic string              | Topic that will be associated with the data, if the query result-set destination is a broker.                                                         |                                                         |
| info      | additional info             | Additional info to the query process. See details [below](#info).                                                                                     |                                                         |
| nodes     | main / all                  | With HA enabled - main: executes the query against the operators designated as **main**, all: operattors are selected using round robin               | main                                                   |
| committed | True/False                  | With HA enabled - only returns data that is synchronized on cluster nodes.                                                                            | False                                                   |


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
If the query is provided by a REST call, the node that executes the query is the node receiving the REST call (and the 
local timezone is determined by this node).  
Users can determine the local timezone on a node using the command:
```anylog 
get timezone info
``` 
Users can validate a timezone using the command [get datetime](#get-datetime-command).

### Output format
The key _format_ determines the output format.
The following chart summarizes the optional values:

| value  | Explanation |
| ---- | ------------------------------------------------------------------------ |
| json | The default value - a json structure whereas the output data is assigned to the key "Query" and if statistics is enabled, it is assigned to the key "Statistics".  |
| json:output | The output is organized in rows whereas each row is a JSON structure - this format is identical to the data load structure. |
| json:list | The output is organized in a list, every entry in the list represents a row (use this format with PowerBI).  |
| table | The output is organized as a table.  |

### Info
Additional info that is delivered to the participating node.       
**Adding info to facilitate sreaming:**  
Streaming mp4 files to an application (like the remote CLI), requires to notify the node which is the target for the streaming,
which is the IP and Port (on each operator node) that would satisfy the streaming request.  
To provide the info, the query provides the following info:
```anylog 
info = (dest_ip =[IP of the streaming target], dest_type = [rest/tcp])
``` 
**dest_ip** - the IP of the process requesting the streaming.   
**dest_type** - the type of connection for the streaming process.    
Example:
```anylog 
info = (dest_ip =67.180.101.158, dest_type = rest)
``` 
Example query:
```anylog 
sql edgex info = (dest_ip =67.180.101.158, dest_type = rest) and extend=(+country, +city, @ip, @port, @dbms_name, @table_name) and format = json and timezone = utc  select  file, start_ts::ljust(19), end_ts::ljust(19), num_cars, speed from video order by speed --> selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file)
``` 

### Network processing
Without the `run client` directive, the query will be executed on the local node.  
Executing a query against all the nodes in the network with the relevant data is by adding the `run client ()` as a command prefix.     
The `run client` directive delivers the query to the target nodes specified in the parenthesis. If target nodes are not specified, 
the network protocol will determine the target nodes from the metadata layer and the query will be processed by evaluating the data in 
all the relevant nodes.  
The format for a network query is the following:
```anylog 
run client () sql [dbms name] [query options] [select statement]
``` 

WIth the first example below, the query process considers all the nodes with relevant data. With the second example, only the specified nodes are participating n the query process:
```anylog 
run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor limit 100"
run client (24.23.250.144:7848, 16.87.143.85:7848) sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor limit 100"
``` 


## SQL supported:

**On the projection list**:
* Column name
* Min
* Max
* Sum
* Count
* Avg
* Count Distinct
* Range
* Time functions over Column values

**On the where clause**:
* Greater than
* Less than
* Equal
* Not Equal
* Group By
* Order By
* Limit

## Time Functions

The WHERE condition can include functions that manipulate time. The following functions are supported:
* `date`
* `timestamp`

The following modifiers are supported:
* start of year
* start of month
* start of day 

**Examples**:
```anylog
timestamp('now','start of month','+1 month','-1 day', '-2 hours', '+2 minutes')
date('now','start of month','-2 month','+ 3 days', '-5 hours', '+1 minute')
```

The function `NOW()` is converted to the current day-time string.   
The function `date()` is converted to the current date string.  

The following values and keywords pairs (prefixed by _+_ or _-_ signs) can be used to modify a date-time function or string.  
The plural 's' character at the end of the modifier names is optional.
* seconds
* minutes
* hours
* weeks
* days
* months
* years


Time units can be also represented by the first character of the unit name. For example: `+3d` is equivalent to `+ 3 days`. 
Minutes is assigned with the character `t` to differentiate from a month. The following examples are equivalent and represents 
4 minutes before the current time:
* `-4t`
* `now() -4t`
* `now() -4 minutes`

**Examples**:
```anylog
run client () sql lsl_demo "select min(value) from ping_sensor where reading_time >= now() -3d and time < now());"
run client (!ip 2048) sql lsl_demo "select * from ping_sensor where reading_time = date('now','start of month','+1 month','-1 day', '-2 hours', '+2 minuts');"    
run client (!ip 2048) sql lsl_demo "select * from ping_sensor where reading_time = timestamp('2020-05-28 18:56:49.890199','+1 month','-1 day', '-2 hours', '+2 minuts');"
```

## Cast Data
Cast allows to map the projected data to a different format. Casting is applied by adjacent double semicolons (::) to the 
projected column name. For example, the SQL statement below projects the value in the column _speed_ as a float rounded 
to 2 digits after the decimal point:

```anylog
run client () sql lsl_demo "select reading_time, speed::float(2) from performance where reading_time >= now() -3d;"
```

The casting options are detailed in the table below:

| Cast                    | details                                                                                                                                                                        |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| float(x)                | Cast to a _float_ value. x represents rounding to x digits after the decimal point. Adding the percent sigh (**%**) before the digits adds comma separation and padding zeros. |
| int                     | Cast to an _int_.                                                                                                                                                              |
| str                     | Cast to a _string_.                                                                                                                                                            |
| ljust(x)                | Cast to a _left-justified string_ with a given X-bytes width.                                                                                                                  |
| rjust(x)                | Cast to a _right-justified_ string with a given X-bytes width.                                                                                                                 |
| format(formatting type) | Apply formatting instructions on the column value.                                                                                                                             |
| datetime(format code)   | Apply formatting instructions on a date-time value. The process parse the datetime string and extract using the format code.                                                   |
| function(expression)    | Execute a function and replace the column value with the result returned by the function. See examples 5 and 6 below.                                                          |
| lstrip                  | Remove leading spaces.                                                                                                                                                         |
| rstrip                  | Remove trailing spaces.                                                                                                                                                        |
| timediff                | Return time difference between date and time returned from the databse and a date and time string (or now()). The returned format is HH:MM:SS.f                                |


**Note**: multiple casting is allowed.  

### Formatting options
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


## **Examples**:

### Example 1 - Number Format
```anylog
run client () sql lsl_demo "select reading_time, speed::int::format(":,") from performance where reading_time >= now() -3d;"
```
The example above represents the speed as an int and formats the speed value with commas.

### Example 2 - Float Format
```anylog
run client () sql lsl_demo "select reading_time, speed::float(%3) from performance where reading_time >= now() -3d;"
```
The example above represents the speed as a float, rounded to 3 digits with commas as a thousand separators and padded with zeros.
This has the same result as formatting with the formatting string: ***:,.03f***.

### Example 3 - Fill Formating

The following queries provides fill formatting examples:
```anylog
AL anylog-node > run client () sql lsl_demo format = table "select count(*)::str::format(0:*>8s)  from ping_sensor"

count(*)
--------
******21
```

```anylog
AL anylog-node > run client () sql lsl_demo format = table "select count(*)::format(0:#<8d)  from ping_sensor"

count(*)
--------
21######
```

```anylog
AL anylog-node > run client () sql lsl_demo format = table "select count(*)::str::format(0:*^8s) from ping_sensor"

count(*)
--------
***21***
```
### Example 4 - Date Formating

The example below extracts only the month and year from a datetime string: 
```anylog
AL anylog-node > run client () sql smart_city "SELECT increments(hour, 1, timestamp), max(timestamp)::datetime(%m-%Y) as timestamp , min(a_n_voltage), max(a_n_voltage), avg(a_n_voltage) from bf where timestamp >= now() - 1 day and timestamp <= now()";
```

### Example 5 - Function

The following example replaces, for each returned row, the min_val with the result returned from the following function:   
([min_val] + [max_val]) / 2)    
**Note**: keys contained in square parenthesis are replaced with the columns values of the row processed. 
```anylog
run client () sql power_plant timezone = local SELECT increments(timestamp), max(timestamp) as timestamp , min(a_current)::function(([min_val] + [max_val]) / 2) as min_val , avg(a_current) as avg_val , max(a_current) as max_val from bf where timestamp >= '2024-07-19T18:57:46.909Z' and timestamp <= '2024-07-20T00:57:46.909Z' and (id=1 ) limit 861;
```
The following example concatenates columns:
```anylog
run client () sql lsl_demo format = table "select min(insert_timestamp)::function(' - ' + '[min]' + ' - ') as min, max(insert_timestamp) as max from ping_sensor"
```
    

### Example 6 - Function with if statement

In the example below, **min_val** is replaced with the string **On** if **min_val** is greater than 10, else, the value returned is the string **Off**. 
```anylog
run client () sql power_plant timezone = local SELECT increments(timestamp), max(timestamp) as timestamp , min(a_current)::function('On' if [min_val] > 10 else 'Off') as min_val , avg(a_current) as avg_val , max(a_current) as max_val from bf where timestamp >= '2024-07-19T18:57:46.909Z' and timestamp <= '2024-07-20T00:57:46.909Z' and (id=1 ) limit 861;
```

### Example 7 - return the time difference
The examples belows return time difference:
```anylog
run client () sql orics stat = false "select max(insert_timestamp)::timediff(now()) as time_diff FROM r_50"
{"Query": [{"time_diff": "00:02:33.50343"}]}

run client () sql orics stat = false "select max(insert_timestamp)::timediff('2024-08-29T01:47:32.554411Z') as time_diff FROM r_50"
{"Query": [{"time_diff": "04:04:33.44671"}]}

run client () sql lsl_demo "select max(insert_timestamp), min(insert_timestamp)::timediff(max(insert_timestamp)) as diff from ping_sensor"

run client () sql lsl_demo "select max(insert_timestamp) as max, min(insert_timestamp)::timediff(max) as diff from ping_sensor"

```


## Get datetime command
Using the command `get datetime` users can translate a date-time function to the date-time string.    
**Usage**:
```anylog
get datetime timezone [date-time function]
```

[date-time function] is the function used to derive the date-time string.

**Examples**:
```anylog
get datetime et now()
get datetime Europe/London now()
get datetime local now() + 3 days
get datetime utc date() + 2 days
get datetime local timestamp('now','start of month','+1 month','-1 day', '-2 hours', '+2 minutes')
get datetime Asia/Shanghai timestamp('now','start of month','+1 month','-1 day', '-2 hours', '+2 minutes')
```

  
## Optimized time series data queries:

The following functions optimize queries over time-series data:

### The Period Function

The `period` function finds the first occurrence of data before or at a specified date (and if a filter-criteria is 
specified, the occurrence needs to satisfy the filter-criteria) and considers the readings in a period of time which is 
measured by the type of the time interval (Minutes, Hours, Days, Weeks, Months or Years) and the number of units of the 
time interval (i.e. 3 days - whereas **time-interval** is day and **unit** is 3).

* `date-column` is the column name of the column that determines the date and time to consider.
* `period` determines the last occurrence which is smaller or equal to the **date-time**. 
* The `time-interval` and the **units** (of time-interval) determine the time range to consider.
* `filter-criteria` is optional. If provided, the data considered needs to satisfy the filter criteria.

**Usage**:
```anylog
period(time-interval, units, date-time, date-column, filter-criteria)
```

**Example**; 
````anylog
sql edgex format=table "select min(timestamp), max(timestamp), count(value) from rand_data WHERE period(day, 1, now(), timestamp);" 
````

### The Increment Function
The `increments` function is used to segment time-series data into fixed, contiguous time intervals (e.g., every 5 minutes, every hour, every day).    
It enables time-based analysis and aggregation by generating a synthetic column representing the start of each time bucket.

**Usage**:
```anylog
increments (units, time-interval, date-column)
```
**Increments Parameters Explained**:  
The increments function helps divide time-series data into uniform time buckets. It takes three key parameters:
1. unit:
   * Type: String
   * Description: Specifies the unit of time to use for the interval.
   * Valid options:
     * second
     * minute
     * hours
     * days
     * weeks
     * month
     * year
   * Examples:
     * minute → minute buckets
     * day → daily buckets
2. time-interval:
    * Type: Integer
    * Description: Defines the size of each time bucket.
    * Examples:
      * 5 — creates buckets every 5 units (e.g., 5 minutes if units is 'minute')
      * 1 — creates buckets of 1 unit length (e.g., 1 hour if units is 'hour')
3. date-column
    * Type: String (column name)
    * Description: The name of the column in the table that contains date or timestamp values. This column determines how each row is assigned to a time bucket.
    * Requirements: Must contain a valid datetime column name - typically used in the WHERE clause to define a time-range.

Increment Example:
```sql
increments(event_time, 10, minute)
```
Assigns each row to a 10-minute bucket based on its event_time.

**Example**: 
```anylog
sql edgex format=table "select increments(day, 1, timestamp), min(timestamp), max(timestamp), count(value) from rand_data where timestamp >= '2025-04-08 17:30:19.390017' and timestamp <= '2025-04-08 19:12:01.229118'" 
```

### Increments Optimized Version
The optimized increments function simplifies time-based bucketing by automatically determining the appropriate time interval   
and unit needed to return an approximate number of evenly spaced data points over a given time range.

Usage:
```sql
increments(number_of_points, date_column)
```
**Parameters:**
* number_of_points (integer): The approximate number of data points (or time buckets) the user wants in the result set. The system will divide the overall time span into this number of equally sized intervals.
* date_column (string): The name of the column containing timestamp or datetime values. This column is used to calculate the time span and assign each row to the appropriate time bucket.

**Note:** The optimized version requires to specify the WHERE clause filtering the date_column.

How it works:
1. The total time span is determined based on the WHERE clause filtering the date_column.
2. An estimated row count within that time range is used to compute the appropriate time interval and unit.
3. The goal is to select a time granularity that yields approximately number_of_points time buckets.
4. The result is a synthetic column that represents the start time of each computed bucket.

**Example query with optimized increments:** 
```sql
select increments(timestamp, 1000), min(timestamp), max(timestamp), count(value) from t13 where timestamp >= '2025-04-08' and timestamp < '2025-04-09'
```
Explanation: Automatically computes the best time interval and unit (e.g., 1 hour, 2 days) to return ~1000 data points between April 8 and April 9.

### The get increments params command

The **get increments params** command calculates the optimal parameters for the increments function based on a specified column, time range, and desired number of data points.
It is used to dynamically determine the most appropriate time_interval and time_unit to apply when aggregating time-series data.

This is especially useful for visualization systems that need to control the number of rows returned in time-based queries.

Usage:
```
get increments params where dbms = [dbms name] 
                        and table = [table name] 
                        and column = [column name] 
                        and where = [where condition] 
                        and data_points = [int] 
                        and format = [table/json]
```
**Parameters:**
* dbms (string): The name of the DBMS (data source) where the target table resides.
* table (string): The name of the table containing the time-series data.
* column (string): The name of the timestamp or datetime column used for time-based bucketing.
* where (string): A condition specifying the time range and any other filters to apply to the data. This helps define the time span for which increment parameters are calculated.
* data_points (integer): The desired number of time buckets (data points) to be returned when using increments.
* format (string): The output format: either "table" for a tabular result or "json" for machine-readable output.

**Example**: 
```anylog
get increments params where dbms = my_dbms and table = t13 and column = timestamp and where = "timestamp >= '2025-04-08 17:30:19.390017' and timestamp <= '2025-04-08 19:12:01.229118'"
```

## Query Examples:

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

