
# Streaming Conditions

Streaming conditions are conditions that are applied on streaming data in each node.  
Setting Streaming Conditions triggers alerts and processes based on data values streamed into the nodes.

The streaming Conditions functionality allows to do the following:
* Declare conditions to evaluate data ingested in the node and trigger a process if the conditions are satisfied
* View the declared conditions on each node
* Remove conditions
 
## Condition Declaration

Conditions are associated to data by referencing the database and table name assigned to the data.  
When new data is associated with the table and database - the relevant condition are evaluated against the new data,
and if the condition is satisfied, the command that depends on the condition is processed.  

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

If dbms is not specified, all conditions are returned.  
If table is not specified, all conditions of the specified database are returned.    
ALl example below are valid:
<pre>
get streaming conditions
get streaming conditions where dbms = test
get streaming conditions where dbms = test and table = rand_data
</pre>



