# Monitoring nodes

Nodes in the network can collect and monitor information on data and state. The collected information can be retrieved from the 
node, or [collected in a database](#Organizing-node-status-in-a-database-table) or send to an 
[aggregator node](#Organizing-node-status-in-an-aggregator-node) where data from multiple nodes is aggregated and available to query.  

Examples of information monitored:
* Data ingested to local databases and data volumes in the tables.
* Disk usage, cpu utilization, memory usage and networking functionality.  

Notes: 
* Some functionalities require psutil installed.
* To support continues monitoring, monitoring tasks are placed on the ***scheduler***. The scheduler functionality is explained at [Alerts and Monitoring](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring).

## Monitoring data commands

* The command ***get rows count*** provides the list of tables in databases and the number of rows in each table.
<pre>
get rows count where dbms = [dbms name] and table = [table name] and format = [json]
</pre>

Notes:
1) If dbms name in not specified, all tables in all databases are considered.  
2) If table name in not specified, all tables in the specified database are considered.
3) The default output format is in a table structure. specifying ***format = json*** provides the output in a JSON format.

Examples:
<pre>
get rows coun
get rows count where dbms = dmci and format = json
get rows count where dbms = aiops and table = lic1_fout
</pre>

* The command ***get operator*** provides details on ingestion of data by an Operator node.

<pre>
get operator
get operator stat format = json
</pre>

* The command ***get data nodes*** lists the Operator nodes in the network and the tables supported on each node.
<pre>
get data nodes
</pre>

## Monitoring state commands 

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

## The "get node info" command

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


## Organizing node status in a database table

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

 
## Organizing nodes status in an aggregator node

An aggregator node is a node that maintains info from multiple nodes, organizes the info by topics and provide a view on 
the status (associated with each topic) of the different nodes in a single query. Setting a node as an aggregator is simple and does not require a database.
It provides near real-time view of the monitored nodes' status. However, not as with a database, it only provides the current status 
and not the historical status information.
The monitoring process is based on a push process, each participating node pushes a state to the aggregator node periodically.
The push process is triggered by the scheduler on each participating node.  

The configuration of a setup with an aggregator node is as follows:
* On the scheduler of each participating node, trigger the command that retrieved the monitored info, and save the retrieved info in JSON format7 in a variable.
* On the scheduler of each participating node, trigger a message to the aggregator with the command: ***monitor*** that details a topic name with the retrieved info.
* The command ***get monitored*** on the aggregator retrieves the list of monitored topics.
* The command ***get monitored [topic]*** on the aggregator retrieves the info associated with the specific topic for each participating node.

### The monitor command

The ***monitor*** command organizes data by topics such that when a topic is queried, the status associated with the topic, 
from each participating node is available.   

Command details:
<pre>
monitor [topic] where ip = [node-ip] and name = [node-name] and info = [json-struct]
</pre>

| Command option | Details  |
| ------------- | ------------| 
| topic  | A string representing a topic. | 
| ip  |the IP of the node associated with the info. If IP is not provided, the IP of the node sending the monitored info is used. | 
| name | Optional string identifying a name for the node. |
| info | A json structure containing the monitored info. |

Example:

<pre>
monitor operator where ip = 127.0.0.1 and name = 'dmc-usa' and info = { "total events" : 1000, "events per second" : 10" }
</pre>

### Retrieving the list of monitored topics

<pre>
get monitored
</pre>

### Retrieving monitored info

The following command retrieves monitored info, for each participating node, on each monitored topic:

<pre>
get monitored [topic]
</pre>


### Example configuring a participating node

The following example configures monitoring of 2 topics:
1. Nodes status (topic name: nodes)
2. Monitor operators status  (topic name: operators)  

In the examples below, the monitoring commands are assigned to the scheduler for continues monitoring.

Configuring topic ***nodes***
<pre>
schedule name = node_status and time = 15 seconds task node_status = get status format = json
schedule name = monitor_node and time = 15 seconds task run client 23.239.12.151:2048 monitor Nodes where info = !node_status"
</pre>

Configuring topic ***Operators***
Note: the command ***get operator stat*** will be using the variables ***disk_space*** and ***cpu_percent*** is assigned with values.
<pre>
schedule name = disk_space and time = 15 seconds task disk_space = get disk percentage .
schedule name = cpu_percent and time = 15 seconds task cpu_percent = get node info cpu_percent
schedule name = get_operator_stat and time = 15 seconds task operator_stat = get operator stat format = json
schedule name = monitor_operator and time = 15 seconds task run client 23.239.12.151:2048 monitor operators where info = !operator_stat
</pre>
