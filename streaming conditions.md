# Streaming Conditions

Streaming conditions are conditions that are applied on streaming data in each node.  
Setting Streaming Conditions triggers alerts and processes based on data values streamed into the nodes.

The Streaming Conditions functionality allows to do the following:
* Declare conditions to evaluate data ingested in the node and trigger a process if the conditions are satisfied
* View the declared conditions on each node
* Remove conditions

Note: Alerts and Monitoring assigned to the scheduler are detailed in the [Alerts and Monitoring](alerts%20and%20monitoring.md#alerts-and-monitoring) section. 
 
## Condition Declaration

Conditions are associated to data by referencing the database and table name assigned to the data.  
When new data is associated with the table and database - the relevant conditions are evaluated against the new data,
and if a condition is satisfied, the command that depends on the condition is processed.  

Usage:
```anylog
set streaming condition where dbms = [dbms name] and table = [table name] and limit = [execution Limit] if [condition] then [command]
```

Details:
* `_dbms name_` - the logical database name associated with the data
* `_table name_` - the logical table name associated with the data
* `_execution limit_` - (optional) if a value greater than 0 is provided, the limit places a cap on the number of times the "then" command is executed. 
* `_condition_` - a condition to validate. Details are available in the [conditional execution](anylog%20commands.md#conditional-execution) section.
* `_command_` - an AnyLog command.

Examples:  
```
set streaming condition where dbms = test and table = rand_data and limit = 2 if [value] > 10 then sms to 6508147334 where gateway = tmomail.net and subject = 'Threshold temperature' and message = 'value in table rand_data is greater than 10' 
```
In the example above, an SMS message is send if the data value is greater than 10. The SMS process is limited to 2 messages.
```
set streaming condition where dbms = test and table = rand_data  if [value] < 3 then return ignore entry  
```
In the example above, the readings are ignored when the value is less than 3  


Note: to send an email, enable the SMTP server as in the example below:
```anylog
run smtp client where email = anylog.iot@gmail.com and password = oeiussclzecgtkxu
```
Details are available at the [SMTP Client](background%20processes.md#smtp-client) section.

## View declared conditions

The following command returns the declared conditions:  
Usage:
```anylog
get streaming conditions where dbms = [dbms name] and table = [table name]
```

If a DBMS name is not specified, all conditions are returned.  
If a table name is not specified, all conditions of the specified database are returned.    
All examples below are valid:
```anylog
get streaming conditions
get streaming conditions where dbms = test
get streaming conditions where dbms = test and table = rand_data
```

## Reset Streaming Condition
Reset allows to remove one or more Streaming Conditions.
Usage:
```anylog
reset streaming conditions where dbms = [dbms name] and table = [table name] and id = [condition id]
```
The condition ID is the condition sequence number.
Notes: 
* Use the `get streaming conditions` command to view the ID assigned to each condition.
* Multiple IDs are allowed
* If a DBMS name is not specified, all conditions are removed.
* If a table name is not specified, all conditions of the database are removed.

All examples below are valid:
```anylog
reset streaming conditions
reset streaming conditions where dbms = test
reset streaming conditions where dbms = test and table = rand_data
reset streaming conditions where dbms = test and table = rand_data and id = 2 and id = 4
```


