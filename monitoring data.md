# Monitoring data

Nodes in the network can collect and monitor data in 2 ways:  
1.  By organizing the data in persistent storage in database tables that are hosted on operator nodes.
This approach allows viewing current and historical data by issuing queries to the database tables. This process of adding data 
    to tables is explained in the section: [Adding Data to Nodes in the Network](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#adding-data-to-nodes-in-the-network).
    
2. By configuring a node to monitor streaming/ingested data and track the recently added data. 
   This process allows evaluating ingested data as it streams into the node and apply monitoring and alerts on the most recent data.
   
## Configuring monitoring on streaming data

Using the command ***data monitor*** users can track data streamed to a node for storage and processing.  
This type of monitoring considers the tables that contain the data, the monitoring aggregates information on the streaming values within predefined time intervals. 
Intervals are time segments for which the following are monitored on a predefined column value:

| Monitored value option | Details  |
| ------------- | ------------| 
| Min  | The lowest value recorded within the time interval. | 
| Max  | The highest value recorded within the time interval. | 
| Avg | The average value within the time interval. |
| Count | The number of events recorded within the time interval. |
| Events/sec | The number of events recorded divided by the number of seconds in the interval. |


Usage: 
<pre>
data monitor where dbms = [dbms name] and table = [table name] intervals = [counter] and time = [interval time] and value_column = [value column name]
</pre>

| Command option | Details  |
| ------------- | ------------| 
| dbms  | The name of the database that hosts the table's data. | 
| table  |The data table name. If table name is not provided, all the tables associated to the database are monitored using the database definitions| 
| intervals | The number of intervals to keep. |
| time | The length of the interval expressed in one of the following: seconds, minutes, hours, days. |

Example: 
<pre>
data monitor where dbms = dmci and intervals = 10 and time = 1 minute and time_column = timestamp and value_column = value
</pre>



