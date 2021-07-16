
# Resource Monitoring

Resources in the network can be monitored in different ways. Resources include nodes that are members of the network as well as devices that generate data and are connected to members of the network.  

Below are examples of deploying monitoring over different resource.  
Additional information is available in the [monitoring nodes section](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#monitoring-nodes).


## Monitoring data ingestion

**Command**: Get streaming status 
<pre>
get streaming
</pre>

**Sample Output**: 
<pre>
Flush Thresholds
Threshold         Value  Streamer
-----------------|------|--------|
Default Time     |    60|Running |
Default Volume   |10,000|        |
Default Immediate|True  |        |
Buffered Rows    |     1|        |
Flushed Rows     |     5|        |

Statistics
DBMS-Table      File Put File Rows Streaming Put Streaming Rows Immediate Last Process
---------------|--------|---------|-------------|--------------|---------|-------------------|
aiops.fic11    |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:06|
aiops.fic12    |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:06|
aiops.fic13    |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.lic1     |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.lic1_sp  |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.ai_mv    |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.valve_pos|       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
aiops.err      |       0|        0|        2,136|         2,136|    2,122|2021-06-24 23:27:07|
</pre>

## Monitoring status using aggregator node

An aggregator node is a node that receives status from member nodes such that a single call to the aggregator can pull updated status from all the participating nodes.  
To provide the functionality, each participating node collects the needed information and periodically pushes the info to the aggregator node.

### Collecting info on a participating node 
Example- pushing the operator status (including disk space and cpu utilization) to an aggregator node:  
In the example below, every 15 seconds the Operator status together with disk space and CPU utilization are collected
    to the variables: operator_stat, disk_space and cpu_percent respectively.  
    Note: disk_space and cpu_percent are reserved names that are added to the JSON structure with the operator info.
    
<pre>
schedule name = disk_space and time = 15 seconds task disk_space = get disk percentage .
schedule name = cpu_percent and time = 15 seconds task cpu_percent = get node info cpu_percent
schedule name = get_operator_stat and time = 15 seconds task operator_stat = get operator stat format = json
</pre>


### Periodically pushing the info to the aggregator node
2.  Using the scheduler, every 15 seconds the info is pushed to the aggregator node.  
On the aggregator node, the pushed info is organized by nodes and topics. The info organized in this example is called ***operators*** 
    and can be queried on the aggregator node using thew following call:
      
<pre>
schedule name = monitor_operator and time = 15 seconds task run client 23.239.12.151:2048 monitor operators where info = !operator_stat
</pre>
  
### retrieving the info from the aggregator node

Using the command ***get monitored operators***, all the info associated with the key ***operators*** (and partitioned by the monitored nodes) is returned to the caller.

### Example - pushing info to the aggregator node using 'get status' command

If a node is operational, the ***get status*** command returns the value "running".  
The ***get status*** command can be extended to return any variable value.  
In the example below, *get status* returns values that are assigned by the device connector API as follows:
Using POST, the variable counter_devices is updated to represent the number of connected devices:
counter_devices is first assigned with the value 0:
<pre>
counter_devices = 0
</pre>
Every new device, increments the value:
<pre>
counter_devices = incr !counter_devices 1
</pre>

Pushing the info to the aggregator node is dome as follows:
* Periodically, on the monitored node, updating the status into variables 
<pre>
schedule name = get_node_stat and time = 15 seconds task node_stat = get status include  counter_devices
</pre>
* Periodically, pushing the info from the monitored node to the aggregator node:
<pre>
schedule name = monitor_status and time = 15 seconds task run client 23.239.12.151:2048 monitor status where info = !node_stat
</pre>

Using the command ***get monitored status*** on the aggregator node, all the info associated with the key ***status*** 
(and partitioned by the monitored nodes) is returned to the caller.
