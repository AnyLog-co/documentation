# Aggregation Functions

Aggregation functions summarize streaming data over a time interval. Users can define the time interval and the number of intervals
per each table to allow continues aggregations. The aggregated values can be queried or used to impact the database updates and monitoring. 
   
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
set aggregations where dbms = dmci and intervals = 10 and time = 1 minute and time_column = timestamp and value_column = value
```

## Retrieve aggregations

The command `get aggregations` retrieves the monitored data.   
**Example**:  
```anylog
get aggregations
get aggregations where dbms = dmci and table = sensor_reading
```
