# Monitoring nodes

Nodes in the network can be monitored to determine disk usage, cpu usage, memory usage and networking functionality.  
Monitoring can be done by retrieving utilization values or by continuously updating database tables with the monitoring data.  

The commands below detail the monitoring functionality:
Note: Some functionalities require psutil installed.

## Monitoring commands

* Info on the type and version of the OS, node name and type of processor.
<pre>
get platform info
</pre>

* Info on the memory of the current node. 
<pre>
get memory info	
</pre>

* Info on the CPU of the current node.
<pre>
get cpu info
</pre>

* Info on the CPU temperature.
<pre>
get cpu temperature
</pre>

* Info on the disk usage
<pre>
get disk [options] [path]
</pre>

[options] - Detail the type of information to retrieve. Options are one of the following: usage, free, total or used.
[path] - A valid path to the monitored disk.

* Get the list of IP addresses available on the node.
<pre>
get ip list
</pre>

## Statistics commands

The ***get node info*** command retrieves additional info and statistics on the current operation of the node.  
Usage:
<pre>
get node info [options]
</pre>

Options are one of the following keys:

| Key        | Details  |
| ------------- | ------------| 
| cpu_percent  | A number representing the current system-wide CPU utilization as a percentage. | 
| cpu_times  | System CPU times, every attribute represents the seconds the CPU has spent in the given mode. |
| cpu_times_percent  | utilization percentages for each specific CPU. |
| getloadavg  | the average system load over the last 1, 5 and 15 minutes. |
| swap_memory  | Swap memory statistics. |
| disk_io_counters  | System disk I/O statistics. |
| net_io_counters  | Network I/O statistics. |

Example:
<pre>
get node info disk_io_counters
</pre>


## Organizing statistics in a database table

Users can use the scheduler to continuously call for statistics and organize the statistics in a database table.  
The format to place statistics in a table is the following:

<pre>
get node info [options] into dbms = [dbms name] and table = [table name]
</pre>

### Example

The following example organizes the CPU utilization in a database table.   
The tables' data is partitioned by date such that data of the previous day is removed.

1) Bacground processes to enable:

* [Streamer](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#streamer-process) such that the data is flushed to disk.
* [Operator](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#operator-process) for the flushed data to be ingested to the table.
* [Scheduler](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#invoking-a-scheduler) to process scheduled tasks.


1) Connect to a SQLite database. The logical database name is ***monitor***.
<pre>
connect dbms sqlite !db_user !db_port monitor
</pre>

2) Partition the data collected by day
<pre>
partition dmci ping_sensor using timestamp by 1 day
</pre>

Note: Partition command is detailed [here](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#partition-command).

3) Using the scheduler, collect CPU utilization every 15 seconds
<pre>
schedule time = 15 seconds and name = "Monitor CPU" task get node info cpu_percent into dbms = monitor and table = cpu_percent
</pre>

4) Removing older than 1 day data (by placing the ***drop partition*** command in the scheduler)

<pre>
schedule time = 1 day and start = +1d and name = "Drop 1 day CPU data" task drop partition where dbms = monitor and table = cpu_percent
</pre>

Note:
* Drop partition command is detailed [here](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#drop-partition-command).
* As partition name is not specified, only the oldest partition is dropped and the active partition is never dropped.

 

