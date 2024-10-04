# Node configuration

Node configuration includes the update of the local dictionary, and the initiation of processes:  
1) Updating the local dictionary - Updating the local dictionary of a node with the values that are needed by the node processes.
2) Initiating processes - Initiating the processes that determine how the node operates (detailed explanations of the 
   processes are available in the [Background Processes](background%20processes.md#background-processes) section).

The AnyLog configuration can be done in different ways:  
* Dynamically issuing REST calls (with AnyLog commands) from an application (issuing REST calls to an AnyLog node is explained in the [Using REST](using%20rest.md#using-rest) section).  
* By a script file that contains AnyLog commands. The advantage in a script file is that it can be organized
as a program with _if_ conditions and _goto_ statements (details are available in the [Configuration Examples](examples/Configuration.md#configuration-examples) section).
* By a JSON file the contains AnyLog commands (using a JSON file to configure a node is demonstrated in the [Configuring a node with a JSON file](examples/Configuration.md#configuring-a-node-with-a-json-file) section).
* Using a table in a database that contains the AnyLog command as detailed below.    

## The configuration process 
Configuration is by calling multiple AnyLog commands.
AnyLog commands can be provided on the CLI or organized in a script file, a JSON file, or a table in a database.    
A node is configured by calling a group of commands that determine how a node operates.

* The command _process_ followed by a path and a file name will process all the commands in the specified file.  
  Usage:
```anylog
process [path and file name]
```
  Example:
```anylog
process !anylog_path/AnyLog-Network/demo/ha_operator1.al
```
* The command [process from dbms](#configuration-from-a-database-table) followed by the DBMS and table details will process the commands contained in
  the table.  

## Issuing AnyLog commands as command lime arguments when AnyLog is initiated

Anylog commands can be issued as command line arguments on the OS command line (or on the AnyLog CLI).  
The following command will process the AnyLog commands contained in the script file when AnyLog node is initiated:  
```anylog
anyLog process !anylog_path/AnyLog-Network/demo/ha_operator1.al
```

Without a script file, with multiple commands, enclose each command with quotation marks and separate each command with the keyword `and`.  
Example:
```anylog
anyLog process "run tcp server !external_ip !node_1_port !ip !node_1_port" and "run rest server !ip 7849"
```

## Configuration from a database table

The `process from dbms` command will retrieve the AnyLog commands contained in the table and process each command:

Usage:
```anylog
process from table where name = [table name] and dbms = [dbms name] and value = [value field name] and command = [command to execute] and condition = [where condition]
```

Command options:

| Key        | Value  | Comments                                                                                                                                             |
| ---------- | -------|------------------------------------------------------------------------------------------------------------------------------------------------------|
| name      | The name of the table containing the AnyLog commands |                                                                                                                                                      |
| dbms       | The DBMS name containing the table |                                                                                                                                                      |
| value      | The field name with the value to associate with the command (the designated value)| Optional key-value                                                                                                                                   |
| command    | The command to execute| If the command string contains the _<>_ sign, it will be assigned with the row's designated value (the _<>_ sign is similar to `%s` in `C/Python`) |
| condition  | The _where_ condition to use when the commands are retrieved | Optional key-value                                                                                                                                   |

Example:

A table in a database needs to be available with the configuration commands. The update of the table can be done by any application.  

In the example below we create the table and update the configuration from the AnyLog CLI:  

**Step A**: Connect to the database containing the config table:
```anylog
connect dbms config_dbms where type = psql and user = anylog and ip = 127.0.0.1 and password = demo and port = 5432
```

**Step B**: Create the config table and update the AnyLog configuration commands.  
Note: this step can be done once (or whenever configurations are updated) and can be done from an application.
```anylog
# Create the table struct
sql config_dbms "create table my_config (command_id serial primary key not null, al_value varchar, al_command varchar not null)"

# Insert value that will generate the AnyLog config commands
sql config_dbms "insert into my_config (al_command, al_value) values ('anylog_server_port=<>', '2148')"
sql config_dbms "insert into my_config (al_command, al_value) values ('sync_time=<>', '30 seconds')"
```

Use the following command to view the config data:

```anylog
sql config_dbms format = table "select * from my_config"
```

**Step C**: The following command will process the commands in the table. Trigger the command whenever AnyLog is initiated.
The command can be issued as a command argument on the OS command line when AnyLog is initiated or on the AnyLog CLI or using REST. 

```anylog
process from table where name = my_config and dbms = config_dbms and value = al_value and command = al_command and condition = "order by command_id"
```

### The setup with database configuration
* Using the AnyLog commands, an AnyLog node is configured.   
* An application updates multiple database tables with AnyLog commands.    
* On startup, the AnyLog instance connects to the database and executes the commands in the tables.  

The AnyLog instance is initiated with command line arguments as follows:
```anylog
process !anylog_path/AnyLog-Network/demo/dbms_config.al
```

`dbms_config` is a script file inside the folder `!anylog_path/AnyLog-Network/demo`.

The Config file includes the following commands:
```anylog
connect dbms config_dbms where type = psql and user = anylog and ip = 127.0.0.1 and password = demo and port = 5432
process from table where name = my_config_1 and dbms = config_dbms and value = al_value and command = al_command and condition = "order by command_id"
process from table where name = my_config_2 and dbms = config_dbms and value = al_value and command = al_command and condition = "order by command_id"
```

Using this setup, an application can manage the AnyLog config script by updating and adding rows in the configuration tables.

## Threads Configuration and Monitoring

Each node is leveraging multiple pools of threads that are associated with different functionalities.  
The command **get system threads** outputs the groups, and information on each group:

Usage:
```anylog
get system threads where pool = [pool type] and with_details = [true/false] and reset = [true/false]
```
Options:
* pool - The pool name and is one of the following:
  * TCP - The threads that listen to messages from peer nodes and execute the message requests.
  * REST - The threads that listen to REST requests from 3rd party applications and execute the REST requests.
  * Message - The threads that listen to requests from data sources (like MQTT Publish) and execute the requests.
  * query - A group of threads that process queries on the operator node.
* with_details - A True value provides statistics on each thread in the pool
* reset - A True value resets statistics

Example:
```anylog
AL > get system threads

Query Pool with 3 threads:                                  [0, 0, 0]
Message Pool with 6 threads:                                [0, 0, 0, 0, 0, 0]
TCP Pool with 6 threads:                                    [0, 0, 0, 0, 0, 0]
REST Pool with 5 threads:                                   [0, 0, 0, 0, 0]
```

In the example above, the reply shows the number of threads in each group and a flag (on/off) per each thread 
indicating if the thread is in rest (0 value) or active (1 value).

### Configuring the size of the pools

The following chart details where the number of threads is configured for each pool:

| Pool Name | Configuration                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------|
| TCP       | In the TCP service command [run tcp server](background%20processes.md#the-tcp-server-process) |
| REST      | In the REST service command [run rest server](background%20processes.md#rest-requests)        |
| Message   | In the Message service command [run message broker](background%20processes.md#message-broker) |
| Query     | In the **set query pool** command (see below)                                                 |
| Operator  | In the Operator service command [run operator](background%20processes.md#operator-process).   |

Note: If an Operator is configured with 1 thread, it will not be included in the **get system threads** command output.

### Configuring the size of the Query Pool
The following command sets the number of threads supporting the queries on each Operator Node:
```anylog
set query pool [n]
```
[n] is the number of threads (the default value is 3).

### Configuring the number of threads supporting "message send" to peer nodes
Users can modify the number of threads that deliver messages from a node to peers. This group of threads allows to send a single message to many nodes concurrently:
```anylog
set send pool [n]
```
[n] is the number of threads (the default value is 10).
 
The following command returns the number of **send threads** configured:
```anylog
get send pool [n]
```
