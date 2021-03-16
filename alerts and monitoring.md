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

## Types of alerts and monitoring

Repeatable tasks serve as a mechanism to repeatedly monitor the state of nodes or values of data in a database and trigger the following:

* An update of a database table - the table can be a log table, or a summary/rollup table that represents accumulative state of the data.
* A message to a user - messages can be in the form of an emails or SMS messages. The messaging commands are detailed [below](#sending-messages).

A task is expressed in one of 3 ways:
* As a ***scheduled command*** - The task is represented by a command that is continuously executed.
* As a ***scheduled script*** - The task is represented by a script whereas the code in the script monitors state or data on the local node or on members of the network. 
* As a ***scheduled repeatable query*** - A repeatable query is a query that is executed periodically and updates a summary (rollup) table that is monitored as needed.

## Adding tasks to the scheduler

A task is represented by a command or a script with scheduling instructions.  

Usage:
<pre>
schedule [options] task [command/script to execute]
</pre>
The command ***schedule*** declares a scheduled task that is placed in the scheduler.  
If the scheduler is active, the command will be repeatably executed according to the time specified in the options.    

The command options are the following:
  
| Option        | Explanation   |
| ------------- | ------------- | 
| time  | The time intervals for the execution of the task.  |
| start | Scheduled start time for first execution of the task. The default value is the current day and time. | 
| name  | A name that is associated with the task. The name in a scheduler needs to be unique (otherwise an error message is returned). |
| scheduler  | The ID of the scheduler, the default value is 1 (a user scheduler). |

  
### Setting the start time
Start time allows to pause the execution of a tasks. For example, a task that alerts by sending an email or a SMS message may be paused for a few hours to avoid continues messaging.      
When a ***schedule*** command is first initiated, users can express a starting date and time. 

The start date and time can be also initiated with the following strings:

| Option        |
| ------------- | 
| now() |
| start of year | 
| start of month |
| start of day |
| start of hour |
| start of minute |

Example:

<pre>
schedule time = 1 day and name = "Sync Devices" and start = "start of day" task process !local_scripts/sync_spript.al.",
</pre>
Using the above command, sync_script.al is processed at the start of each day.

The start time of a task can be modified using the command [task init](#modifying-the-start-date-and-time-of-a-task).

### Examples

The following tasks are executed every 5 minutes.  
The first command determines the free space of disk drive D and places it in a variable called ***disk_space***.  
The second command sends an email if disk space is under a threshold.

<pre>
schedule time = 5 minutes and name = "Get Disk Space" task disk_d_free = get disk free d:\
schedule time = 5 minutes and name = "Alert Disk Space" task if !disk_d_free < 1000000000 then email to my_name@my_company.com and message = "Disk Drive D is under a threshold"
</pre>

## Repeatable Queries

Repeatable queries are queries that are executed periodically.   
The result set of the query can update a summary table as in the example below:  

Example:
<pre>
schedule time = 5 minutes and name = "Summary cos_data Table" task run client () sql dmci table = my_table and drop = false "SELECT max(timestamp), min(value), max(value), avg(value) from cos_data where timestamp >= TIME(PREVIOUS) and timestamp < TIME(CURRENT)"
</pre>

This command will be executed every 15 seconds. The output would be added to a table called 'my_table' on the query node.

## View scheduled commands
The ***get scheduler*** command retrieves the scheduled commands for each scheduler as follows:
<pre>
get scheduler [id]
</pre>
***id*** - Optional value, representing the scheduler ID. If not specified, the information from all schedulers is returned.

## Managing Tasks

Each task in the scheduler can be called to be executed, paused, removed, or associated with a new start time. 
A task can be called to be immediately executed regardless of the scheduler setting. 
These operations are done using the ***task*** command.  

Note, If the ***task*** command doesn't specify a scheduler ID, scheduler #1 is referenced.

### Pausing and resuming a task
The ***task stop*** pauses a task from being executed. The command remains on the scheduler but will not be executed until ***task resume*** uis called.   
Usage:
<pre>
task stop where scheduler = [scheduler id] and name = [task name]
or
task stop where scheduler = [scheduler id] and id = [task id]
</pre>

The ***task resume*** makes the task active on the scheduler.  
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
task init where scheduler = [scheduler id] and id = [task id] and start = [date and time]
</pre>

The date and time can be a time string or represented as time forward from the current date and time.      
Time Forward Examples:
<pre>
+ 2h - starting two hours from current time.  
+ 1d - starting one day from current day and time.    
</pre>

The following chart includes the time forward options:
    
| Option        | Time Unit   |
| ------------- | ------------- | 
| y  | year  |
| m  | month  |
| w  | week  |
| d  | day  |
| h  | hour  |
| t  | minute  |
| s  | second  |

Example:

<pre>
schedule task init where name = "Get Disk Space" and start = +2h
</pre>
Using the above command, disk space monitoring will be paused for 2 hours.


### Immediate execution of a task

A task can be callued to immediate exection using the following command:
<pre>
task run where scheduler = [scheduler id] and name = [task name]
or
task run where scheduler = [scheduler id] and id = [task id]
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

Multiple message texts on the command line, like the example below, will be represented as multiple lines in the email message:
<pre>
email to my_name@my_company.com  where subject = "anylog alert" and message = "Value of Heater sensor is above threshold" and message = "Reporting node: 24.23.250.144 (Operator SF)"
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
The major USA carriers and their gateways are the following:

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
4) The summary table will be monitored (using Grafana) to alert when nodes are not reporting or a sensor did not deliver data.
5) The summary table will be monitored (using Grafana) to alert when values exceed or below thresholds.

## Nodes setup
* The monitoring and alerts instructions are placed in scripts that are organized in a designated directory.
* The path to the scripts directory is assigned with the key ***scripts_dir***. The example below associates a physical location to the scripts' directory.
<pre>
scripts_dir = D:\Node\AnyLog-Network\scripts
</pre>
The physical location may be different for every node, depending on the node hardware and the OS used.
* nodes will assign the key ***monitored_drive*** to the hard drive containing the sensor data. The example below declares the monitored drive.
<pre>
monitored_drive = D:\
</pre>

## Example - Monitoring disk space

The following is the script to monitor the disk space:

<pre>
disk_free = get disk free !monitored_drive
if !disk_free < 1000000000 then
do email to my_name@my_company.com where subject = "AnyLog Disk Space Alert" and message = "Disk Drive is under a threshold"
do sms to 650555555  where gateway = tmomail.net and subject = "AnyLog Disk Space Alert" and message = "Disk Drive is under a threshold"
do task init where name = "Monitor Space" and start +1d
</pre>

Note, in the example above, using the command [task init](#modifying-the-start-date-and-time-of-a-task), when the message is sent, the repeatable script is suspended for one day such that the Email box and the messaging will not be exhausted with the same message every 5 minutes.

The script is placed in a file called ***monitor_space*** and is added to the scheduler using the [schedule](#Adding-tasks-to-the-scheduler) command:

<pre>
schedule time = 5 minutes and name = "Monitor Space" task process !scripts_dir/monitor_space.al
</pre>

## Example - Repeatable query

The following is a repeatable query, configured on a query node and monitoring a demo table (called cos_data) that is distributed over multiple Operators.  
The repeatable query is issued every 5 minutes to query all the nodes that host data assigned to the demo table.    
The repeatable query does not specify time ranges, these are set dynamically, as needed, replacing the query key strings - ***TIME(PREVIOUS)*** and ***TIME(CURRENT)*** of the SQL command.

<pre>
schedule time = 5 minutes and name = "Summary cos_data Table" task run client () sql dmci table = summary_sensor and drop = false "SELECT max(timestamp), min(value), max(value), avg(value) from cos_data where timestamp >= TIME(PREVIOUS) and timestamp < TIME(CURRENT)"
</pre>

The summary table is configured as a data source to Grafana to monitor and alert as follows:
1) If operator nodes are not reporting within the last 10 minutes, an alert is sent to the system administrator.
2) If sensors did not generate data within the last 30 minutes, the system administrator is notified.
3) If data values are above or below thresholds, the system administrator is notified.

## Example - Monitoring CPU usage

The section [Organizing statistics in a database table](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#organizing-statistics-in-a-database-table)
details how to organize operational statistics (like CPU utilization) in a table.

