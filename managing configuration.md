# Managing configurations

Node configuration includes the update of the local dictionary, and the initiation of processes:  
1) Updating the local dictionary - Updating the local dictionary of a node with the values that are needed by the node processes.
2) Initiating processes - Initiating the processes that determine how the node operates.

The AnyLog configuration can be done in different ways:  
a) Dynamically issuing REST calls (with AnyLog commands) from an application.  
b) By a script file that contains AnyLog commands. The advantage in a script file is that it can be organized
as a program with ***if*** conditions and ***goto*** statements.  
c) By a JSON file the contains AnyLog commands.  
d) Using a table in a database that contains the AnyLog command.    


## Dynamically issuing REST calls (with AnyLog commands) from an application

Issuing REST calls to an AnyLog node is explained in the [Using REST](.//using%20rest.md#using-rest) section.

## Using a script file, JSON file, or a table to configure AnyLog command

* The command ***process*** followed by a path and a file name will process all the commands in the specified file.
* The command [process from dbms](#the-process-from-dbms-command) followed by the DBMS and table details will process the commands contained in
  the table.  

## Issuing AnyLog commands as command lime arguments when AnyLog is initiated

Anylog commands can be issued as command line arguments on the OS command line (or on the AnyLog CLI).  
The following command will process the AnyLog commands contained in the script file when AnyLog node is initiated:  
<pre>
AnyLog process !anylog_path/AnyLog-Network/demo/ha_operator1.al
</pre>

Without a script file, with multiple commands, enclose each command with quotation marks and separate each command with the keyword ```and```.  
Example:
<pre>
AnyLog process "run tcp server !external_ip !node_1_port !ip !node_1_port" and "run rest server !ip 7849"
</pre>

## The process from dbms command

The ***process from dbms*** command will retrieve the AnyLog commands contained in the table and process each command:

Usage:
<pre>
process from dbms where name = [dbms name] and table = [table name] and value = [value field name] and command = [command to execute] and condition = [where condition]
</pre>

Command options:

| Key        | Value  | Comments  |
| ---------- | -------| ------- |
| name       | The DBMS name containing the table |  |
| table      | The name of the table containing the AnyLog commands | |
| value      | The field name with the value to associate with the command| |
| command    | The command to execute| |
| condition  | The ***where*** condition to use when the commands are retrieved | optional |