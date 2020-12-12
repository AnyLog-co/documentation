# Commands and Scheduled Tasks

AnyLog commands are issued against data and metadata on the local node and can be send to peers in the network.

Command can be send to peers in 2 ways:  
a) By specifying the IP and Ports of the peers.  
b) By issuing a SQL command and the network protocol determines the peers that maintain the data.  

Examples:  
The SQL command below will be transferred to all the nodes that maintain data of the ping_sensor table.
<pre>
run client () sql lsl_demo format = table "SELECT count(*), min(value), max(value) from ping_sensor"
</pre>
The SQL command below will be transferred to a specific node.
<pre>
run client 192.173.200,312:2048 sql lsl_demo format = table "SELECT count(*), min(value), max(value) from ping_sensor"
</pre>
The SQL command below will be executed on the current node.
<pre>
sql lsl_demo format = table "SELECT count(*), min(value), max(value) from ping_sensor"
</pre>
The command below will be send to 2 designated nodes.
<pre>
run client (192.173.200,312:2048,192.185.10,32:2048) "get status"
</pre>

## Job status

When a SQL command is issued, a special structure (called job) monitors the state of the execution.   
The command ```job status``` provides information on state of the last command executed.  
The command  ```job status all``` provides information on state of the last 100 commands executed.  
The command ```job status all``` provides information on state of the last 100 commands executed.  
The command ```job status [ID]``` provides information on state of a particular command executed, whereas ID is the sequence number associated with the command.  

More information is available at [Profiling and Monitoring Queries](https://github.com/AnyLog-co/documentation/blob/master/profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries)


## Scheduled tasks

The Scheduler enables to control when computing tasks take place in the network environment without manual intervention.  
Using the scheduler, users can schedule commands and processes such that they will be executed within specified time intervals.      
Each scheduler object is an AnyLog command or an AnyLog script that contains a process that is executed periodically.  
Initiating the scheduler is explained at [Scheduler Process](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#scheduler-process).  

To review the list of scheduled tasks, issue the command:
<pre>
show scheduler
</pre>

When a task is placed in the scheduler, it is set as an Active task that is executed. 
Users can switch the status of a task to be non-active, change a non-active status to active and remove a task from the scheduler using the following commands:
<pre>
task [id] stop
task [id] run
task [id] remove
</pre>

