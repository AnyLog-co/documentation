# Aggregation Functions

Aggregation functions summarize streaming data over a time interval. Users define (per table) the time interval and the number of intervals
per each table to allow continues aggregations. The aggregated values can be queried or used to impact the database updates and monitoring.

Aggregation functions are used to summarize streaming data over a specified time interval. These functions process incoming 
data continuously, computing key statistics such as counts, sums, averages, or max/min values over defined periods.    
Users define, per table, the length of time interval and the number of intervals to maintain.    

## How They Work:
* Users define a time interval (e.g., 1 minute, 5 minutes, or hourly).
* Users define the number of intervals to maintain.
* The system continuously aggregates incoming data within each interval.
* Aggregated results are stored in tables, where each table can have multiple intervals.
* Aggregated values can be used in real-time for:
  * Querying the current trends
  * Triggering alerts or monitoring changes
  * dImpacting database updates (e.g., adjusting thresholds dynamically)

## Declaring Aggregations

Using the command `set aggregation` users can track data streamed to a node for storage and processing. This type of 
monitoring considers the tables that contain the data and the monitoring aggregates information on the streaming values 
within predefined time intervals. Intervals are time segments for which the following are monitored on a predefined column 
value:

| Monitored value option | Details  |
| ------------- | ------------| 
| Min  | The lowest value recorded within the time interval. | 
| Max  | The highest value recorded within the time interval. | 
| Avg | The average value within the time interval. |
| Count | The number of events recorded within the time interval. |
| Events/sec | The number of events recorded divided by the number of seconds in the interval. |


Usage: 
```anylog
set aggregation where dbms = [dbms name] and table = [table name] intervals = [counter] and time = [interval time] and value_column = [value column name]
```

| Command option | Default  | Details  |
| ------------- | ------------| ------------| 
| dbms  |  |  The name of the database that hosts the table's data. | 
| table  |  |The data table name. If table name is not provided, all the tables associated to the database are monitored using the database definitions.| 
| intervals | 10 | The number of intervals to keep. |
| time | 1 minute | The length of the interval expressed in one of the following: seconds, minutes, hours, days. |
| value_column | value | The name of the column being monitored (the column name in the tablr that hosts the data). |

Example: 
```anylog
set aggregations where dbms = dmci and intervals = 10 and time = 1 minute and time_column = timestamp and value_column = value and format = [table/json]
```
## Declaring Thresholds

Users can declare thresholds on each stream. These thresholds can be referenced by the rule engine to impact the processing 
of the stream and trigger operations that consider the thresholds.

Usage:
```anylog
set aggregations thresholds where dbms = [dbms name] and table = [table name] and and min = [min value] and max = [max value] and avg = [average value] and count = [events count] 
 ```

## Reset aggregations

The command `reset aggregations` removed the aggregation declarations.      
Usage:
```anylog
reset aggregations where dbms = [dbms name] and table = [table name]
```
If table name is not provided, aggregations associated with all the tables assigned to the database are removed.

## Aggregation encoding

The command `set aggregations encoding` applies encoding on the values in the time interval.  
The encoding is represented by a new data set associated to a new schema (described below, for each type of encoding).  
The table name with the encoding format is using the original table name, prefixed by the encoding type.  
For example, if the source data is assigned to a table named **my_table** and the encoding type is arle, 
the table with the encoded data is called **alre_my_table**.

Usage:
```anylog
set aggregations encodeing where dbms = lsl_demo and table = ping_sensor and encoding = [encoding type] and tolerance = [value]
```

**Encoding types:**

* None - No encoding (default).
* bounds - all entries in the time interval are replaced with a single entry representing: 
  * **timestamp** - The earliest date and time of the entries represented in the interval.
  * **end_interval** - The latest date and time of the entries represented in the interval.
  * **min_val** - The lowest value recorded within the time interval.
  * **max_val** - The highest value recorded within the time interval.
  * **avg_val** - The average of the values recorded within the time interval.
  * **events** - The number of events recorded within the time interval.


* arle - Approximated Run-Length Encoding, the entries in the time interval are represented in a sequence of entries. Each entry includes:
  * **timestamp** - The earliest date and time of the entries represented in the interval.
  * **end_interval** - The latest date and time of the entries represented in the interval.
  * **avg_val** - average of grouped values.
  * **events** - The number of events recorded within the time interval.
      
 **tolerance**  
Allowable difference between consecutive values while treating them as part of the same group or segment.    
Tolerance is represented as percentage difference. 

Example:
```anylog
set aggregations encoding where dbms = lsl_demo_ok and table = rand_table and encoding = arle and tolerance = 5
```

## Retrieve aggregations

The command `get aggregations` retrieves the monitored data.   
**Example**:  
```anylog
get aggregations
get aggregations where dbms = lsl_demo and table = ping_sensor
```

The following example shows the retuned info to a **get aggregation** command:
```anylog
DBMS     Table       interval H:M:S Events/sec Count Min Max   Avg
--------|-----------|--------|-----|----------|-----|---|-----|------|
lsl_demo|ping_sensor|       0|0:3:0|      0.35|   21|  2|2,221|413.38|
lsl_demo|ping_sensor|       1|0:2:0|      0.35|   21| 21|3,221|256.24|
```

| Column Returned | Details                                                                                                                                        |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------| 
| DBMS            | The database name.                                                                                                                             | 
| Table           | The table name.                                                                                                                                | 
| Interval        | The sequential ID of the interval, if time in **set aggregation** command is set to 1 minute, the data added from second 20 to 29 is Inteval 2 |
| H:M:S           | The time elapsed since the interval data was processed (to the current interval)                                                               |
| Count           | The number of rows (readings) processed in the interval.                                                                                       |
| Min             | The Min value processed in the interval.                                                                                                       |
| Max             | The Max value processed in the interval.                                                                                                       |
| Avg             | The Average value processed in the interval.                                                                                                   |

## Retrieve aggregations declarations

The following command retrieves the aggregation declarations:
```anylog
get aggregations config
get aggregations config where dbms = lsl_demo and table = ping_sensor
```

## Retrieve the most recent value

The following command retrieves the most recent value:
```anylog
get aggregations where dbms = [dbms name] and table = [table name] and function = [function name]
```
The function name is one of the following: **min, max, count, avg**

Example:
```anylog
get aggregations where dbms = lsl_demo and table = ping_sensor and function = max
```
