# Alerts and Monitoring

Nodes in the network can be configured to execute commands and scripts periodically.  
These commands and scripts can monitor the state of the node and the data hosted on the node or the state of peer nodes and their data.  
The output of the calls triggers alerts or aggregated in a database that is queried or monitored as needed.  
Scripts can include any logic expressed using the AnyLog commands.

The mechanism of issuing repeatable commands is based on a Scheduler.  
Nodes can be configured with one or more schedulers. The schedulers are identified with an ID. Scheduler #0 is a system scheduler and 
in most cases schedulers #1 and higher are for users scheduled tasks. 
The Scheduler contains the commands to execute and the time interval to schedule each command.  

The 2 common ways to represent alerts and monitoring are the following:
* Schedule a script. The code in the script is executed periodically to monitor state or data on the local node or on members of the network. The script can update a database that is monitored as needed.
* Schedule a repeatable query. A repeatable query is a query that is executed periodacally and updates a summary (rollup) table that is monitored as needed.

## Invoking a scheduler
The scheduler is initiated using the folowing command:
<pre>
run scheduler [id]
</pre>
***id*** Optional value, representing the scheduler ID. The defailt value is 1, representing a user scheduler.

## View scheduled commands
The ***get scheduler*** command retrieves the scheduled commands for each scheduler as follows:
<pre>
get scheduler [id]
</pre>
***id*** Optional value, representing the scheduler ID. If not specified, the information from all the scheduled commands from all schedulers is returned.




## Repeatable Queries

Repeatable queries are executed periodically and the output is usually directed to a table.  
The query results can either replace the previously queried data or be added to the previously queried data.  
To allow repeatable queries, configure a scheduler process. This process is invoked in time intervals to invoke the queries that need to be issued.


#### Declaring a repeatable query:

<pre>
schedule [options] command [command to execute]
</pre>

***Options:***  
***time*** - repeat command every specified number of seconds (default is 15 seconds)

Example:
<pre>
schedule time 15 command run client () "sql anylog_test text table: my_table drop: false SELECT max(timestamp), avg(value) from ping_sensor where period (  minute, 1, now(), timestamp, and device_name='APC SMART X 3000')"
</pre>

This command will be executed every 15 seconds. The output would be added to a table called 'my_table' on the query node.

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

 