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
  Usage:
  <pre>
  process [path and file name]
  </pre>
  Example:
  <pre>
  process !anylog_path/AnyLog-Network/demo/ha_operator1.al
  </pre>
* The command [process from dbms](#configuration-from-a-database-table) followed by the DBMS and table details will process the commands contained in
  the table.  

## Issuing AnyLog commands as command lime arguments when AnyLog is initiated

Anylog commands can be issued as command line arguments on the OS command line (or on the AnyLog CLI).  
The following command will process the AnyLog commands contained in the script file when AnyLog node is initiated:  
<pre>
anyLog process !anylog_path/AnyLog-Network/demo/ha_operator1.al
</pre>

Without a script file, with multiple commands, enclose each command with quotation marks and separate each command with the keyword ```and```.  
Example:
<pre>
AnyLog process "run tcp server !external_ip !node_1_port !ip !node_1_port" and "run rest server !ip 7849"
</pre>

## Configuration from a database table

The ***process from dbms*** command will retrieve the AnyLog commands contained in the table and process each command:

Usage:
<pre>
process from table where name = [table name] and dbms = [dbms name] and value = [value field name] and command = [command to execute] and condition = [where condition]
</pre>

Command options:

| Key        | Value  | Comments  |
| ---------- | -------| ------- |
| name      | The name of the table containing the AnyLog commands | |
| dbms       | The DBMS name containing the table |  |
| value      | The field name with the value to associate with the command (the designated value)|  |
| command    | The command to execute| If the command string contains the ***%s*** sign, it will be assigned with the row's designated value |
| condition  | The ***where*** condition to use when the commands are retrieved | optional |

Example:

A table in a database needs to be available with the configuration commands. The update of the table can be done by any application.  

In the example below we create the table and update the configuration from the AnyLog CLI:

<pre>
connect dbms psql anylog@127.0.0.1:demo 5432 config_dbms   # Create/connect to the database containing the config info
# Create the table struct
sql config_dbms "create table my_config (command_id serial primary key not null, al_value varchar, al_command varchar not null)"
# Insert value that will generate the AnyLog config commands
sql config_dbms "insert into my_config (al_command, al_value) values ('anylog_server_port=<>', '2148')"
sql config_dbms "insert into my_config (al_command, al_value) values ('sync_time=<>', '30 seconds')"
</pre>

The following command issued as a command argument issued on the OS command line when AnyLog is initiated or on the AnyLog CLI 
will process the commands in the table.

<pre>
process from table where name = my_config and dbms = config_dbms and value = al_value and command = al_command and condition = "order by command_id"
</pre>

