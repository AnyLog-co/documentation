# Monitoring nodes

Nodes in the network can collect and monitor information on data and state. The collected information can be retrieved from the 
node, or [collected in a database](#Organizing-node-status-in-a-database-table) or send to an 
[aggregator node](#Organizing-nodes-status-in-an-aggregator-node) where data from multiple nodes is aggregated and available to query.  

Examples of information monitored:
* Data ingested to local databases and data volumes in the tables.
* Disk usage, cpu utilization, memory usage and networking functionality.  

Notes: 
* Some functionalities require psutil installed.
* To support continues monitoring, monitoring tasks are placed on the _scheduler_. The scheduler functionality is explained at [Alerts and Monitoring](alerts%20and%20monitoring.md#alerts-and-monitoring).

## Monitoring data commands

* The command `get rows count` provides the list of tables in databases, and the number of rows in each table.  
Usage:
```anylog
get rows count where dbms = [dbms name] and table = [table name] and format = [json] and group = [partition/table]
```

Notes:
1) If dbms name in not specified, all tables in all databases are considered.  
2) If table name in not specified, all tables in the specified database are considered.
3) The default output format is in a table structure. specifying _format=json_ provides the output in a JSON format.
4) The _group_ variable determines if rows count are presented for each partition (the default) or aggregated and presented for each table (and the table name is prefixed with _per__ string). 

Examples:
```anylog
get rows count
get rows count where dbms = dmci and format = json
get rows count where dbms = aiops and table = lic1_fout
get rows count where dbms = aiops and table = lic1_fout and group = table
```

* The command `get operator` provides details on ingestion of data by an Operator node.  

Usage:
```anylog
get operator
get operator stat format = json
```

* The command `get data nodes` lists the Operator nodes in the network and the tables supported on each node.  

Usage:
```anylog
get data nodes
```

## Monitoring state commands 

* Info on the type and version of the OS, node name and type of processor.
```anylog
get platform info
```

* Info on the memory of the current node. 
```anylog
get memory info	
```

* Info on the CPU of the current node.
```anylog
get cpu info
```

* Info on the CPU temperature.
```anylog
get cpu temperature
```

* Info on the disk usage
```anylog
get disk [options] [path]
```

[options] - Detail the type of information to retrieve. Options are one of the following: usage, free, total or used.
[path] - A valid path to the monitored disk.

* Get the list of IP addresses available on the node.
```anylog
get ip list
```

## The "get os process" command
The `get os process` command retrieves cpu and memory info for each process on the local machine.  
Usage:
```anylog
get os process
get os process anylog
get os process [pid]
get os process all
get os process list
```

* The command `get os process` is identical to `get os process anylog` and provides info on the AnyLog process.
* The command `get os process [pid]` provides info on the process with the provided pid.
* The command `get os process all` provides info on all processes. As CPU measurement is using a second interval,
on the AnyLog CLI, a bar displays the command progress.
* The command `get os process list` lists the processes and their process IDs.


## The "get node info" command

The `get node info` command retrieves additional info and statistics on the current operation of the node.  
The command maps to a psutil call as detailed below.
Values can be returned to the user or to an [aggregator node](#organizing-nodes-status-in-an-aggregator-node) 
or [sored on a local database](#organizing-node-status-in-a-database-table).  
The psutil functions are detailed [here](https://psutil.readthedocs.io/en/latest/).
 
Usage:
```anylog
get node info [options] [attribute name]
```

**Options** are one of the following keys:

| Key        | Details  |
| ------------- | ------------| 
| cpu_percent  | A number representing the current system-wide CPU utilization as a percentage. | 
| cpu_times  | System CPU times, every attribute represents the seconds the CPU has spent in the given mode. |
| cpu_times_percent  | Utilization percentages for each CPU. |
| getloadavg  | Return the average system load over the last 1, 5 and 15 minutes. |
| swap_memory  | Swap memory statistics. |
| disk_io_counters  | System disk I/O statistics. |
| net_io_counters  | Network I/O statistics. |

**Attribute name** is optional, if provided, the named attribute is returned. 

Examples:
```anylog
get node info disk_io_counters
get node info disk_io_counters read_count
get node info net_io_counters
get node info net_io_counters bytes_recv
get node info swap_memory free
```


## The "get status" command

A node can issue a `get status` command to any peer in the network. Below is an example of the command and the returned reply:
  
```anylog
run client (10.0.0.78:7848) get status
[From Node 10.0.0.78:7848]  'AnyLog@24.23.250.144:7848 running'
```

Usage:
```anylog
get status where format = [reply format] include [list of dictionary names]
```
Details:  
**format** - an optional parameter to define the reply format. specifying **format=json** returns the reply in JSON.   
**include** - extends the returned info with additional information.  
For example, the scheduler can be configured to monitor the CPU utilization, 
CPU temperature and disk free space and usage. The `get status` command can request to include their values.  

**Example**:  
* Setup on the monitored node:
```anylog
cpu_percent = get node info cpu_percent
cpu_temperature = get cpu temperature
disk_free = get disk free d:\
disk_percentage = get disk percentage d:\
```
* Getting the status information:
```anylog
AL anylog-node > run client (10.0.0.78:7848) get status include !cpu_percent !cpu_temperature !disk_free !disk_percentage
[From Node 10.0.0.78:7848]
{'status' : 'AnyLog@24.23.250.144:7848 running',
 'cpu_percent' : '6.7',
 'disk_free' : '990713614336',
 'disk_percentage' : '99.05'}
```

* The keyword **statistics** in the include list adds default statistics to the status info.  
Example:  
```anylog
get status include statistics
```

## The "get processes" command

The `get processes command` lists state and configuration choices using a single call:     
a) The list of background processes and their current status.  
b) The main configuration choices selected for the node.  
**Example**:
```anylog
AL anylog-node > get processes
    Process         Status       Details
    ---------------|------------|---------------------------------------------------------------------|
    TCP            |Running     |Listening on: 24.23.250.144:7848 and 10.0.0.78:7848, Threads Pool: 6 |
    REST           |Running     |Listening on: 10.0.0.78:7849, Threads Pool: 5, Timeout: 20, SSL: None|
    Operator       |Running     |Cluster Member: True, Using Master: 10.0.0.25:2548                   |
    Publisher      |Not declared|                                                                     |
    Blockchain Sync|Running     |Failed to connect to master using: 10.0.0.25:2548                    |
    Scheduler      |Running     |Schedulers IDs in use: [0 (system)]                                  |
    Distributor    |Running     |                                                                     |
    Consumer       |Running     |No peer Operators supporting the cluster                             |
    MQTT           |Running     |                                                                     |
    Message Broker |Running     |Listening on: 24.23.250.144:7850 and 10.0.0.78:7850, Threads Pool: 6 |
    SMTP           |Not declared|                                                                     |
    Streamer       |Running     |Default streaming thresholds are 60 seconds and 10,000 bytes         |
    Query Pool     |Running     |Threads Pool: 3   
```


## The "get dictionary" command

Each node is using a dictionary to map keys to values.  
Some mappings represent default assignments, and some mappings are declared using scripts or on the CLI.  
The `get dictionary` command lists the key values pairs.  
Usage:
```anylog
get dictionary
```
Use the following command to retrieve the keys and values in JSON format:
```anylog
get dictionary where format = json
```

The following command retrieves a single value:
```anylog
!key
```


## The "get env var" command

The `get env var` command lists the environment variables key values pairs.  
**Usage**:
```anylog
get env var
```
Use the following command to retrieve the keys and values in JSON format:
```anylog
get env var where format = json
```

The following command retrieves a single value:
```anylog
$key
```


## Organizing node status in a database table

Users can use the scheduler to continuously call for statistics and organize the statistics in a database table.  
The format to place statistics in a table is the following:

```anylog
get node info [options] into dbms = [dbms name] and table = [table name]
```

### Example

The following example organizes the CPU utilization in a database table.   
The tables' data is partitioned by date such that data of the previous day is removed.

1) Background processes to enable:

* [Streamer](background%20processes.md#streamer-process) such that the data is flushed to disk.
* [Operator](background%20processes.md#operator-process) for the flushed data to be ingested to the table.
* [Scheduler](alerts%20and%20monitoring.md#invoking-a-scheduler) to process scheduled tasks.


1) Connect to a SQLite database. The logical database name is `monitor`.
```anylog
connect dbms monitor where type=sqlite 
```

2) Partition the data collected by day
```anylog
partition dmci ping_sensor using timestamp by 1 day
```

Note: Partition command is detailed [here](anylog%20commands.md#partition-command).

3) Using the scheduler, collect _CPU utilization_ every 15 seconds
```anylog
schedule time = 15 seconds and name = "Monitor CPU" task get node info cpu_percent into dbms = monitor and table = cpu_percent
```

4) Removing older than 1 day data (by placing the `drop partition` command in the scheduler)

```anylog
schedule time = 1 day and start = +1d and name = "Drop 1 day CPU data" task drop partition where dbms = monitor and table = cpu_percent
```

Note:
* Drop partition command is detailed [here](anylog%20commands.md#drop-partition-command).
* As partition name is not specified, only the oldest partition is dropped and the active partition is never dropped.

 
## Organizing nodes status in an aggregator node

An aggregator node is a node that maintains info from multiple nodes, organizes the info by topics and provide a view on 
the status (associated with each topic) of the different nodes in a single query. Setting a node as an aggregator is simple 
and does not require a database. It provides near real-time view of the monitored nodes' status. However, not as with a database, 
it only provides the current status and not the historical status information. The monitoring process is based on a push 
process, each participating node pushes a state to the aggregator node periodically. The push process is triggered by the 
scheduler on each participating node.  

The configuration of a setup with an aggregator node is as follows:
* On the scheduler of each participating node, trigger the command that retrieves the monitored info, and assigns the retrieved status info (in JSON format) to a variable.
* On the scheduler of each participating node, trigger a message to the aggregator (using the command: `monitor`) that details a topic name with the status info (by naming the assigned variable).
* The command `get monitored` on the aggregator retrieves the list of monitored topics.
* The command `get monitored [topic]` on the aggregator retrieves the info associated with the specific topic for each participating node.

### The monitor command

The `monitor` command organizes data by topics such that when a topic is queried, the status associated with the topic, 
from each participating node is available.   

Command details:
```anylog
monitor [topic] where ip = [node-ip] and name = [node-name] and info = [json-struct]
```

| Command option | Details  |
| ------------- | ------------| 
| topic  | A string representing a topic. | 
| ip  |the IP of the node associated with the info. If IP is not provided, the IP of the node sending the monitored info is used. | 
| name | Optional string identifying a name for the node. |
| info | A json structure containing the monitored info. |

Example:

```anylog
monitor operator where ip = 127.0.0.1 and name = 'dmc-usa' and info = { "total events" : 1000, "events per second" : 10" }
```

### Retrieving the list of monitored topics

```anylog
get monitored
```

### Retrieving monitored info

The following command retrieves monitored info, for each participating node, on each monitored topic:

```anylog
get monitored [topic]
```


### Example, configuring a participating node

The following example configures monitoring of 2 topics:
1. Nodes status (topic name: nodes)
2. Monitor operators status  (topic name: operators)  

In the examples below, the monitoring commands are assigned to the scheduler for continues monitoring (on each participating/monitored node).

Monitored topic: **nodes**
```anylog
schedule name = node_status and time = 15 seconds task node_status = get status where format = json
schedule name = monitor_node and time = 15 seconds task run client 23.239.12.151:2048 monitor Nodes where info = !node_status"
```

Monitored topic **Operators**  

```anylog
schedule_time = "15 seconds"
aggregator = 10.0.0.78:7848
schedule name = get_operator_stat and time = !schedule_time task node_insight = get operator stat format = json
schedule name = node_status and time = !schedule_time task node_insight[Node Status] = get status where format = json
schedule name = disk_space and time = !schedule_time task node_insight[Free space %] = get disk percentage .
schedule name = cpu_percent and time = !schedule_time task node_insight[CPU %] = get node info cpu_percent
schedule name = network_info and time = !schedule_time task node_insight[Network] = get node info net_io_counters
schedule name = monitor_operator and time = 15 seconds task run client (!aggregator) monitor operators where info = !node_insight
```


## Monitoring Nodes Operations

Users can monitor node status throughout execution periods using the command: _continuous_. The command continuously 
monitors status and provides status results to the stdout. 

**Usage**:
```anylog
continuous [list of commands]
```

The allowed commands are detailed below. If the command is longer than a single word, it needs to be enclosed in quotations.


| Command option | Details  |
| ------------- | ------------| 
| cpu  | CPU usage | 
| cpu anylog  | CPU usage of AnyLog. | 
| cpu [process name]  | CPU usage of the named process. | 
| get cpu usage  | Usage per each CPU. |
| get operator | The operator status. |
| get operator summary| Summary of the operator status. |
| get streaming | The streaming buffers status. |
| get query pool | The query threads status. |
| get operator pool | The operator threads status. |
| get rest pool | The REST threads status. |
| get tcp pool | The TCP threads status. |
| get msg pool | The message broker threads status. |

**Example**:

```anylog
continuous cpu "cpu anylog" "cpu postgres" “get operator summary” "get cpu usage"
```

Continuous repeats the monitoring every 5 seconds. If a key on the keyboard is hit, continuous terminates.



