---
title: "Conditional Execution & Control Flow"
description: "Scripting constructs for AnyLog scripts: if/else conditions, labeled sections and goto, for loops, end script, and the wait command."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-26 | Ori Shadmon    | New page consolidating control-flow content previously split between "02 CLI.md" and "01 Anylog Commands.md" | |
--->

# Conditional Execution & Control Flow

AnyLog supports conditional executions using ***if and else*** statements. An ***if and else*** statement has the following structure:

```anylog
if [condition] then [command A]
else [command B]
```

* [condition] - an expression that will be evaluated
* [command] - any of the AnyLog commands

The condition is an expression that is validated, a true result triggers the execution of the command following the ***then*** keyword.
A false result triggers the execution of the commands following the ***else*** keyword. Multiple ***else*** statements are allowed.

AnyLog supports the following conditions:

| Sign         | Details                                                                 | Comments                                                                                          |
|--------------|-------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| ==           | Equal                                                                   |                                                                                                   |
| !=           | Not Equal                                                               |                                                                                                   |
| <            | Less than                                                               |                                                                                                   |
| <=           | Less than or equal to                                                   |                                                                                                   |
| >            | Greater than                                                            |                                                                                                   |
| >=           | Greater than or equal to                                                |                                                                                                   |
| is declared  | Tests whether the specified attribute exists in the JSON object         | Returns True if the attribute exists in the JSON object                                           |
| not declared | Tests whether the specified attribute does not exist in the JSON object | Returns True if the attribute does not exist in the JSON object                                   |
|              | Is defined                                                              | No sign - Returns True if the variable is defined in the local dictionary                         |
| not          | Is not defined                                                          | Returns True if the variable is not defined in the local dictionary                               |
| contains     | Includes the provided substring using case insensitive comparison       | if X contains Y - Returns True if X and Y are strings and Y is a substring of X                   |
| startswith   | Starts with the provided substring using case-insensitive comparison    | if X startswith Y - Returns True if X and Y are strings and X starts with Y                       |
| endswith     | Ends with the provided substring using case-insensitive comparison      | if X endswith Y - Returns True if X and Y are strings and X ends with Y                           |
| childfrom    | Determine if a path is an immediate child of a parent path              | Return True if x is an immediate child of Y, else False. The Path separator is the last char of Y |

Multiple conditions within parenthesis are allowed with an "_and_" or "_or_" keyword separation.
The allowed structure is the following:

```anylog
if ([condition a]) and/or ([condition b]) then [command]
else [command]
```

## Using dictionary values in the comparison process

Note:
* By default, comparison treats all values as strings. If a data type is specified, the comparison treats the compared values by their
data types. The supported data types are _str_ (the default), _int_, _bool_ and _float_.
Data types are specified by adding a dot, and a data type to the variable considered. For example: `if !a.float == 1.234`.
* The result of an if statement can be assigned to a variable, for example: `a = if not !a`.
* Users can test if statements on the AnyLog CLI by executing the if statement, for example: `if not !a`.
* Nested parenthesis are not supported.

Examples:

```anylog
if not !json_data then process !script_create_table
```
```anylog
if !old_value.int == 128 then print values are equal
```
```anylog
if !number.int < !value then echo true
```
```anylog
if not !old_value then old_value = 5
```
```anylog
if not !a then a = "new value"
else message = "The dictionary value for a is: " + !a
else print !message
```
```anylog
if (!a and !b == 123) or (!c and !d) then print "with value"
else print "no value"
```
```anylog
if !a.int == 5 then print "Comparison as integers succeeded"
```
```anylog
if !a then print with value
else print "without value"
```
```anylog
if not !a then print "without value"
else print "with value"
```
```anylog
a = if not !a
```
```anylog
if !company_name includes "anylog"
```
```anylog
if !path startswith root/
```
```anylog
if !path childfrom root/
```

## Multiple do - then instruction

Conditional execution can make multiple commands dependent on a condition.
The commands that are executed if the condition returns "_true_" are prefixed by the "_do_" keyword.
The commands that are executed if the condition returns "_false_" are prefixed by the "_else_" keyword.

Usage:
```anylog
if [condition] then
do [command A]
do [command B]
do [command C]
else [command d]
else [command f]
else [command f]
```

Example:

```anylog
if (!external_ip and !node_1_port and !ip and !node_1_port) then
do run tcp server !external_ip !node_1_port !ip !node_1_port
do print "Node connected to the AnyLog Network"
do get connections
else print "Missing configurations for IP and Port to connect to the AnyLog Network"
else email to my_name@my_company.co where subject = "anylog node" and message = "not connected"
```

## The "goto" command

Script sections can be labeled, and using the command **goto** followed by a label, the execution shifts to a different
(labeled) part of the code. Labels are required to be at the start of a command line (in the script) and enclosed by colons.

The following script demonstrates the usage of the **goto** command. In the example below, the **goto** command
transfers the execution to the section that satisfies a value set in an environment variable:
```anylog
if $setup_type == query then goto query_node
else goto operator_node

:query_node:
connect dbms test where type = sqlite
end_script

:operator_node:
connect dbms sensor_data where type = psql and user = anylog and password = demo and ip = 127.0.0.1 and port = 5432
end_script
```

## The "end script" command

The **end script** command terminates the execution of the script (see the example above).

## The "for loop" command

The ```for loop``` command iterates over every element in a list. During each iteration, the current element is made available
through the loop index (+). The loop continues until all list elements have been processed.

Syntax:
```anylog
for loop start where list = <list_variable>
    <commands>
for loop end
```
Inside the loop, use the + index to reference the current element and the value of + is automatically updated on each iteration.

Example:
```anylog
query_result = run client () sql cos format=json:list and stat=false "select * from pp_pm where period(minute, 1, now(), timestamp) limit 3;"

wait 5 for !query_result        # Wait up to 5 seconds

for loop start where list = !query_result
	print !query_result[+]
for loop end
```

Notes
* The loop executes once for every element in the specified list.
* If the list is empty, the commands inside the loop are not executed.

## The Wait Command

The **wait** command pauses execution of the thread until a condition is satisfied, or a time limit is reached.

Usage:
```anylog
 wait [max wait time in seconds] for [condition]
```

**Condition** can be one of the following:
* An if condition, i.e.: if X == Y, whereas a true value terminates the wait.
* Using the keyword **sync** to allow a sync of the metadata before terminating the wait.

A common usage is when a node issues a command to peer nodes, some peers reply and some peers are disconnected.
The wait command pauses until all peers reply, but no longer than the max wait time.

**Example 1** - Wait by a timer:
```anylog
wait 3
```
In the example above, execution will pause for 3 seconds.

**Example 2** - Wait by an if condition:
```anylog
nodes_reply[] = run client (10.0.0.78:3048, 10.0.0.78:7848) get status
wait 5 for !nodes_reply.diff == 0
```
In the example above, 2 peer nodes are messaged for their status (note: replies are organized in a list).
The wait command thread pauses for 5 seconds or until the 2 peer nodes' replies are received - whichever comes first.

**Example 3** - Wait for sync

```anylog
wait 35 for sync
```

In the example above, execution will wait for the shorter of: a) a metadata sync, and b) 35 seconds.

Notes:
1. It is advised to declare a max wait time which is larger than the sync time, allowing the sync to operate, but terminate if the sync is disabled.
2. It is advised to use the command in consecutive blockchain update-with-delete operations to avoid race conditions.
