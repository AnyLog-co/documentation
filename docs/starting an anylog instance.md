# Starting an AnyLog Instance

An AnyLog instance is initiated by calling AnyLog on the OS command line.  
Once an AnyLog instance is called, it presents the AnyLog command prompt. The command prompt allows to issue AnyLog commands.    
These commands configure the AnyLog instance to operate in one or more of the roles: as a Publisher of data, as an Operator managing data or as a Query node that issues queries against the data in the network.    
Commands can be arranged in a text file, the command `script` followed by the location and name of the file will trigger an execution of all the commands in the script.  

There are 3 ways to issue AnyLog commands:    

1)	On the OS command line, by initiating an AnyLog instance followed by one or more commands to execute.  
If multiple commands are issued on the OS command line, the commands needs to be separated by the keyword _and_.  
Example: the command `run tcp server 192.168.234.6:2046 and run rest server 192.168.234.6:2047`   
will initiate an AnyLog instance and configure the node to listen to TCP messages and REST messages on the detailed IPs and Ports.     
2)	On the AnyLog command line by issuing the command on the AnyLog command line prompt.  
3)	By configuring a node as a REST server and issuing command to the configured REST IP and Port. The REST API only support a subset of the commands.

## Assigning values to variables
Values are assigned by using the equal sign. `my_script = !anylog_path/AnyLog-Network/scripts/deployment_scripts/local_script.al` 
assigns the detailed path to the variable my_location. Referencing the assigned value is by an exclamation point followed 
by the variable name. `!my_script` provides the assigned path and file name.  

**Example**: 
```anylog
AL anylog-node > my_script = !anylog_path/AnyLog-Network/scripts/deployment_scripts/local_script.al 
AL anylog-node > !my_script 
'/app/AnyLog-Network/scripts/deployment_scripts/local_script.al' 
```

## Execution flow commands
Managing commands in scripts allows to control the execution path by issuing `if then` commands and redirecting the execution using a `goto` statement to a named location in the script.
Naming a location in a script  is by adding a colon sign as a prefix and suffix to the named location.  
```:process_start:` is an example of a named location that can be referenced by a `goto` command.
  
## The help command
Using the command `help` on the AnyLog command line lists all the commands and how they are called.  
Using the command `help` followed by a `command name` details how the command is called.  
Using the command `help` followed by the keyword `example` and a command name provides an example of how the command is called.  
Using the command `help` followed by the keyword `text` and a command name provides an explanation on the command.  

## Using a local database
An Anylog node can use a local database. The local database is leveraged to support several functionalities:  
On a Publisher Node – the local database is optional. If available, it maintains a copy of the metadata information.  
On an Operator Node – it maintains the data hosted by the node and optionally copy of the metadata.  
On a Query Node – it maintains intermediate query results and optionally copy of the metadata.  

### Connecting to a local database
Connecting to a local database is done on the AnyLog command prompt. It connects a logical database to a physical database and is done as follows:
  * `[db_name]` is the logical database name to connect to 
  * `[dbms_type]` is the type of database.  
  * `[db_ip]` is the IP address associated to connect to the database
  * `[db_port]` is the port value associated to connect to the database
  * `[db_user]` is the username used to connect to the database 
  * `[db_password]` is the database password associated with the database user
  * `[db_memory_option]` is a True/False value - whether to deploy database in-memory (used in SQLite)
  
```anylog 
connect dbms [db_name] where type=[dbms_type] and ip=[db_ip] and port=[db_port] and user=[db_user] and password=[db_password] and memory=[db_memory_option]
```

The following example connects a logical database, named my_iot_dbms to a PostgresSQL database:
```anylog
# connect to PostgresSQL database 
AL anylog-node> connect dbms my_iot_dbms where type=psql and ip=127.0.0.1 and port=5432 and user=anylog and passowrd=passwd

# connect to SQLite Database 
AL anylog-node> connect dbms system_query where type=sqlite and memory=true 
```

### Disconnecting from a local database
Disconnect is done by calling the disconnect command as follows:
 * `[dbms_name]` is the logical database name.
```anylog 
disconnect dbms [dbms_name]
``` 

### Management commands
```anylog
# shows the last events processed on the node.
AL anylog-node > get event log 

# shows the last errors identified on the node.
AL anylog-node > get error log

# on an operator node, shows the last data files processed on the node.
AL anylog-node > get file log  

# shows definitions maintained in the dictionary.
AL anylog-node > get dictionary

# shows the active watch directories.
AL anylog-node > get watch directories
```

## Configuration checklist

This section details a configuration checklist for each type of node in the cluster.
  
#### All Nodes

* Directory structure to maintain local copy of the blockchain and local data was created.
 Dictionary definitions that map to the directory structure used. Use `get dictionary` to see all the dictionary definitions.
* Correct IP and ports defined. Use `!ip` to see the default IP used on each machine.
* Listener for TCP incoming messages. Use `get connections` to see open connections. Use `run tcp server [ip] [port]` to declare a TCP connection.


If a local database is used to manage the metadata:
* Connect to the _blockchain_ database.
* If the _ledger_ table was not created on the blockchain database, use `blockchain create table` to create the table.  

**Note**:
Use `get databases` to see the databases connected on each node.  
Use `connect dbms psql [dbms user] [dbms port] [dbms name]` to connect to a specif database.

#### Operator Node

* Test that the supported databases are connected. These needs to include the databases that support the user's data.
* Test that the _watch directory_ is being used. Use `get watch directories` to visualize the watched directories. 

#### Publisher Node

* Test that the _watch directory_ is being used. Use `get watch directories` to see the watched directories. 

#### Query Node

* Test that the `system_query` database is connected -- `get database`
* Listener for REST incoming messages. Use `show connections` to see open connections. Use `run rest server [ip] [port] [timeout]` to declare a REST connection.

#### Master Node (if available)

* Test that the _blockchain_ database is connected and the ledger table is created declared.  

#### Example calls
* To view connections use `get conections` 
* To view the location of the watch directories use: `get watch directories`
* Example connecting to the blockchain database: `connect dbms psql !db_user !db_port blockchain`
* To view database connected use: `get databases`
* Creating the _ledger_ table is by calling `blockchain create table`

