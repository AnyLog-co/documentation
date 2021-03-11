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
| swap_memory  | Swap memory statistics. |
| disk_io_counters  | System disk I/O statistics. |
| net_io_counters  | Network I/O statistics. |




