# Alerts and Monitoring

Nodes in the network can be configured to repeatably execute tasks.   
A task is a single command or multiple commands that are organized in a script file and are executed periodically by the scheduler.    
These tasks monitor the state of nodes and values of data hosted by the nodes of the network. Tasks can process state and data on the local node or on remote nodes.  
The output of the tasks triggers alerts or aggregated in a database that is queried or monitored as needed.  
Tasks can include any logic expressed with the AnyLog commands.

The mechanism of issuing repeatable tasks is based on a Scheduler.  
Nodes can be configured with one or more schedulers. The schedulers are identified by an ID. Scheduler #0 is a system scheduler and 
schedulers #1 and higher are for users scheduled tasks. 
Each Scheduler contains the tasks to execute and the time interval associated with each task.  

## Invoking a scheduler

The scheduler is initiated using the following command:
<pre>
run scheduler [id]
</pre>
***id*** - Optional value, representing the scheduler ID. The defailt value is 1, representing a user scheduler.

## Terminating a scheduler

Users can terminate a specific scheduler or all scheduler using the following commands:
<pre>
exit scheduler [id]
</pre>
***id*** - The ID of the scheduler to terminate. If not specified, all schedulers are terminated.



Additional examples are in the [Appendix](Appendix:-Demo) below.

## Types of alerts and monitoring

Repeatable tasks can consider the status of a node or values of data in a database and trigger the following:

* An update of a database table - the table can be a log table, or a summary/rollup table that represents accumulative state of the data.
* A message to a user - messages can be in the form of an emails on SMS messages. The messaging commands are detailed [below](#sending-messages).

The way tasks are used to monitor are the following:
* ***Scheduled script*** - The task is represented by a script whereas the code in the script is executed periodically to monitor state or data on the local node or on members of the network. The script can update a database that is monitored as needed.
* ***Scheduled repeatable query*** - A repeatable query is a query that is executed periodacally and updates a summary (rollup) table that is monitored as needed.

## Adding tasks to the scheduler

A task is represented by a command or a script with scheduling instructions.  

Usage:
<pre>
schedule [options] task [command/script to execute]
</pre>
The command ***schedule**** declares a scheduled task that is placed in the scheduler.  
If the scheduler is active, the command will be repeatably executed according to the time specified in the options.    
Options include the following:
  
| Option        | Explanation   |
| ------------- | ------------- | 
| time  | The time intervals for the execution of the task.  |
| start | Scheduled start time for first execution of the task. The default value is the current day and time. | 
| name  | A name that is associated with the task. The name in a scheduler needs to be unique |

Note:
* Multiple tasks with the same name are rejected.
  
### Setting the start time
Start time allows to pause the execution of a tasks. For example, a task that alerts by sending an email or a SMS message may be paused for a few hours to avoid continues messaging.      
When a ***schedule*** command is first initiated, users can express a starting date and time. This value can be modified using the command [task](#Modifying-Tasks).

### Examples

The following commands are executed every 5 minutes. 
The first command determines the free space and places it in a variable called disk_space.  
The second commands sends an email if disk space is under a threshold.

<pre>
schedule time = 5 minutes task disk_d_free = get disk free d:\
schedule time = 5 minutes task if !disk_d_free < 1000000000 then email to my_name@my_company.com and message = "Disk Drive D is under a threshold"
</pre>

## Repeatable Queries

Repeatable queries are queries that are executed periodically.   
The result set of the query can update a summary table as in the example below:  

Example:
<pre>
schedule time = 15 minutes task run client () "sql anylog_test text table: my_table drop: false SELECT max(timestamp), avg(value) from ping_sensor where period (  minute, 1, now(), timestamp, and device_name='APC SMART X 3000')"
</pre>

This command will be executed every 15 seconds. The output would be added to a table called 'my_table' on the query node.

## View scheduled commands
The ***get scheduler*** command retrieves the scheduled commands for each scheduler as follows:
<pre>
get scheduler [id]
</pre>
***id*** - Optional value, representing the scheduler ID. If not specified, the information from all the scheduled commands from all schedulers is returned.

## Managing Tasks

Each task in the scheduler can be called to be executed, paused, removed, or associated with a new start time. 
A task can be called to be immediately executed regardless of the scheduler setting. 
These operations are done using the ***task*** command.  
Note, that the ***task*** command can include the scheduler ID, otherwise scheduler #1 is referenced.

### Pausing and resuming a task
The ***task stop*** pauses a task from being executed. The command remains on the scheduler but will not be executed until ***task resume** uis called.
Usage:
<pre>
task stop where scheduler = [scheduler id] and name = [task name]
or
task stop where scheduler = [scheduler id] and id = [task id]
</pre>

The ***task resume*** makes the task executable. If the ***start*** date and time are validated, the task will be placed to execution by the scheduler.
Usage:
<pre>
task resume where scheduler = [scheduler id] and name = [task name]
or
task resume where scheduler = [scheduler id] and id = [task id]
</pre>

### Removing a task
The ***task remove*** command removes the task from the scheduler.
Usage:
<pre>
task remove where scheduler = [scheduler id] and name = [task name]
or
task remove where scheduler = [scheduler id] and id = [task id]
</pre>

### Modifying the start date and time of a task
The ***task init*** sets a new starting date and time for a task.
Usage:
<pre>
task init where scheduler = [scheduler id] and name = [task name] and start = [date and time]
or
task remove where scheduler = [scheduler id] and id = [task id] and start = [date and time]
</pre>

The date and time can be a time string or represented as time forward from the current date and time.      
Time Forward Examples:
+ 2h - starting two hours from current time.
+ 1d - starting one day from current day and time. 
The following chart includes the time forward options:
    
| Option        | Time Unit   |
| ------------- | ------------- | 
| y  | year  |
| m  | month  |
| w  | week  |
| d  | day  |
| h  | hour  |
| m  | minute  |
| s  | second  |

### Immediate execution of a task

A task can be callued to immediate exection using the following command:
<pre>
task run where scheduler = [scheduler id] and name = [task name]
or
task run where scheduler = [scheduler id] and id = [task id]
</pre>


## Queries using REST client

#### Basic header info:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   sql
dbms                   [the logical database name]
details                [a sql query]
</pre>

#### Servers option:
The ***servers*** option allows to direct a query to a particular server (or servers).
If servers are not specified, the network resolved the destination servers from the metadata information and the participating servers are all the servers that maintain the relevant data.  
If one or more servers are specified, only the specified servers will be included in the query process.

Example:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   sql
dbms                   my_sensors_database
details                select * from g30 limit 10
servers                10.0.0.13:2048, 10.0.0.28:2050     
</pre>

#### Instructions:
***Instructions*** detail execution and output destinations of queries.
Instructions can consider tables that are with different names (but share the same structure) as a single dataset.  
In addition, instructions can redirect the query output to a table on the query node.

##### Include multiple tables of different databases in the same query:
This option allows to treat tables that share the same structure but with different names as a single collection of data.
 
Example:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   sql
dbms                   my_sensors_database
details                SELECT mp_id, timestamp, type, region, substation, bank_customer, aphase, bphase, cphase from readings WHERE type='A' AND mp_id=16976001 OR mp_id=54544001 OR mp_id=37318000 AND timestamp >= '2019-12-01 00:00:00' AND timestamp <= '2019-12-07 00:00:00' 
instructions           include: south_pi.readings, central_pi.readings
</pre>

##### Output the data to a static table on the Query Node:
With this option, the output data is redirected to a table on the Query Node. The database name is ***system_query*** and the table name is specified in the header's value.
When the query is executed the query results overwrite the previous query results unless drop is set to false.

Example:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   sql
dbms                   my_sensors_database
details                SELECT mp_id, timestamp, type, region, substation, bank_customer, aphase, bphase, cphase from readings WHERE type='A' AND mp_id=16976001 OR mp_id=54544001 OR mp_id=37318000 AND timestamp >= '2019-12-01 00:00:00' AND timestamp <= '2019-12-07 00:00:00' 
instructions           include: south_pi.readings, central_pi.readings
instructions           table: static_output drop: false 
</pre>

 ## Sending messages
Users can invoke emails and sms messages when thresholds or alerting conditions are met.  
To facilitate messages, declare the ***SMTP client*** process. Details are available at [run smtp client](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#smtp-client).

### Sending an email
Usage:
<pre>
email to [receiver email] where subject = [message subject] and message = [message text]
</pre>
Command Options: 

| Option        | Explanation  | Default  |
| ------------- | ------------| ---- | 
| receiver email | The destination address | |
| message subject | Any text | AnyLog Alert |
| message text | Any text | AnyLog Network Alert from Node: [node name] |

Example:
<pre>
email to my_name@my_company.com
</pre>

### Sending SMS messages
Usage:
<pre>
sms to [receiver phone] where gateway = [sms gateway] and subject = [message subject] and message = [message text]
</pre>
Command Options: 

| Option        | Explanation  | Default  |
| ------------- | ------------| ---- | 
| receiver phone | The destination phone number | |
| gateway | [The SMS carrier gateway](https://en.wikipedia.org/wiki/SMS_gateway) |  |
| message subject | Any text | AnyLog Alert |
| message text | Any text | AnyLog Network Alert from Node: [node name] |

Example with T-mobile as a carrier:
<pre>
sms to 6508147334 where gateway = tmomail.net
</pre>
The major USA carriers and gateways are the following:

| Carrier        | Gateway  | 
| ------------- | ------------|  
| AT&T | txt.att.netr |
| Sprint |messaging.sprintpcs.com |
| T-Mobile | tmomail.net |
| Verizon | vtext.com |
| Boost Mobile | myboostmobile.com |
| Metro PCS | mymetropcs.com |
| Tracfone | mmst5.tracfone.com |
| U.S. Cellula | email.uscc.net |
| Virgin Mobile | vmobl.com |

A detailed list of mobile carriers and gateways is available [here](https://kb.sandisk.com/app/answers/detail/a_id/17056/~/list-of-mobile-carrier-gateway-addresses).


# Appendix: Demo
# Configuring a cluster of nodes to monitor and alert when nodes status or data values change

This appendix demonstrates a setup of multiple nodes that are configured to monitor and alert when nodes state and data values change above or below configured thresholds.  
Using the setup below, the following processes are enabled:

1) On each monitored machine, if disk space is less than a threshold, an administrator will be notified by an email and a SMS message.
2) On each monitored machine, if CPU utilization is higher than a threshold, an administrator will be notified by an email and a SMS message.
3) A repeatable query on each node that hosts data will update a summary table with aggregated values from the source tables.
4) The shared table will be monitored (using Grafana) to alert when values exceed or below thresholds.
5) The shared table will be monitored (using Grafana) to alert when nodes are not reporting or a sensor did not deliver data.

## Nodes setup
* The monitoring and alerts instructions are placed in scripts that are organized in a designated directory.
* The path to the scripts directory is assigned with the key ***scripts_dir***. The example below associates a physical location to the scripts' directory.
<pre>
scripts_dir = D:\Node\AnyLog-Network\scripts
</pre>
The physical location may be different for every node, depending on the node hardware and the OS used.
* nodes will assign the key ***monitored_drive*** to the hard drive containing the sensor data. The example below declares the monitored drive.
monitored_drive = D:\

## Example 1 - monitoring disk space

The following is the script to monitor the disk space:

<pre>
disk_free = get disk free !monitored_drive
if !disk_free < 1000000000 
then email to my_name@my_company.com where subject = "AnyLog Disk Space Alert" and message = "Disk Drive is under a threshold"
then sms to 6503466174  where gateway = tmomail.net and subject = "AnyLog Disk Space Alert" and message = "Disk Drive is under a threshold"
then stop alert for one day
</pre>

Note, once a message is sent, the repeatable script is suspended for one day such that the Email box and the messaging will not be exhausted with the same message every 5 minutes.

The script is placed in a file called ***monitor_space*** and is added to the scheduler using the ***schedule*** command:

<pre>
schedule new time = 5 minutes and name = "monitor_space" task process !scripts_dir/monitor_space
</pre>

