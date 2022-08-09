
# Streaming Conditions

Streaming conditions are conditions that are applied on streaming data in each node.  
Setting Streaming Conditions triggers alerts and processes based on data values streamed into the nodes.

The Streaming Conditions functionality allows to do the following:
* Declare conditions to evaluate data ingested in the node and trigger a process if the conditions are satisfied
* View the declared conditions on each node
* Remove conditions

Note: Alerts and Monitoring assigned to the scheduler are detailed in the [Alerts and Monitoring](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring) section. 
 
## Condition Declaration

Conditions are associated to data by referencing the database and table name assigned to the data.  
When new data is associated with the table and database - the relevant conditions are evaluated against the new data,
and if a condition is satisfied, the command that depends on the condition is processed.  

Usage:
<pre>
set streaming condition where dbms = [dbms name] and table = [table name] if [condition] then [command]
</pre>

Details:
* ***dbms name*** - the logical database name associated with the data
* ***table name*** - the logical table name associated with the data
* ***condition*** - a condition to validate. Details are available in the [conditional execution](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#conditional-execution) section.
* ***command*** - an AnyLog command.

Example:  
<pre>
set streaming condition where dbms = test and table = rand_data  if [value] > 10 then send sms to 6508147334 where gateway = tmomail.net and subject = 'Threshold temperature' and message = 'value in table rand_data is greater than 10' 
</pre>
In the example above, an SMS message is send if the data value is greater than 10.

## View declared conditions

The following command returns the declared conditions:  
Usage:
<pre>
get streaming conditions where dbms = [dbms name] and table = [table name]
</pre>

If a DBMS name is not specified, all conditions are returned.  
If a table name is not specified, all conditions of the specified database are returned.    
All examples below are valid:
<pre>
get streaming conditions
get streaming conditions where dbms = test
get streaming conditions where dbms = test and table = rand_data
</pre>

## Reset Streaming Condition
Reset allows to remove one or more Streaming Conditions.
Usage:
<pre>
reset streaming conditions where dbms = [dbms name] and table = [table name] and id = [condition id]
</pre>
The condition ID is the condition sequence number.
Notes: 
* Use the ***get streaming conditions*** command to view the ID assigned to each condition.
* Multiple IDs are allowed
* If a DBMS name is not specified, all conditions are removed.
* If a table name is not specified, all conditions of the database are removed.

All examples below are valid:
<pre>
reset streaming conditions
reset streaming conditions where dbms = test
reset streaming conditions where dbms = test and table = rand_data
reset streaming conditions where dbms = test and table = rand_data and id = 2 and id = 4
</pre>

