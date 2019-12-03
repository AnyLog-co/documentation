# Starting an AnyLog Instance

An AnyLog instance is initiated by calling AnyLog on the OS command line.  
Once an AnyLog instance is called, it presents the AnyLog command prompt. The command prompt allows to issue AnyLog commands.    
These commands configure the AnyLog instance to operate in one or more of the roles: as a Publisher of data, as an Operator managing data or as a Query node that issues queries against the data in the network.    
Commands can be arranged in a text file, the command ***script*** followed by the location and name of the file will trigger an execution of all the commands in the script.  

There are 3 ways to issue AnyLog commands:    

1)	On the OS command line, by initiating an AnyLog instance followed by one or more commands to execute.  
If multiple commands are issued on the OS command line, the commands needs to be separated by the keyword ***and***.  
Example: the command ```anylog run tcp server 192.168.234.6:2046 and run rest server 192.168.234.6:2047```   
will initiate an AnyLog instance and configure the node to listen to TCP messages and REST messages on the detailed IPs and Ports.     
2)	On the AnyLog command line by issuing the command on the AnyLog command line prompt.  
3)	By configuring a node as a REST server and issuing command to the configured REST IP and Port. The REST API only support a subset of the commands.

## Assigning values to variables
Values are assigned by using the equal sign.  
my_location =  $HOME/AnyLog-demo/tests/scripts/script_test_blockchain.anylog assignes the detailed path to the variable my_location.  
Referencing the assigned value is by an exclamation point followed by the variable name.  
```!my_location``` provides the assigned path and file name.  

## Execution flow commands
Managing commands in scripts allows to control the execution path by issuing ```if then``` commands and redirecting the execution using a ```goto``` statement to a named location in the script.
Naming a location in a script  is by adding a colon sign as a prefix and suffix to the named location.  
```:process_start:``` is an example of a named location that can be referenced by a ```goto``` command.
  
## The help command
Using the command ***help*** on the AnyLog command line lists all the commands and how they are called.  
Using the command ***help*** followed by a ***command name*** details how the command is called.  
Using the command ***help*** followed by the keyword ***example*** and a command name provides an example of how the command is called.  
Using the command ***help*** followed by the keyword ***text*** and a command name provides an explanation on the command.  

## Using a local database
An Anylog node can use a local database. The local database is leveraged to support several functionalities:  
On a Publisher Node – the local database is optional. If available, it maintains a copy of the metadata information.  
On an Operator Node – it maintains the data hosted by the node and optionally copy of the metadata.  
On a Query Node – it maintains intermediate query results and optionally copy of the metadata.  

### Connecting to a local database
Connecting to a local database is done on the AnyLog command prompt. It connects a logical database to a physical database and is done as follows:

```connect dbms [dbms_type] [db_user@db_ip:db_passwd] [db_port] [db_name]```  
***[dbms_type]*** is the type of database.  
***[db_user@db_ip:db_passwd]*** is the connection info: username, database connection IP, password.  
***[db_port]*** is the database connection port.  
***[db_name]*** is the logical database name.  

The following example connects a logical database, named my_iot_dbms to a PostgreSQL database:
```connect dbms psql anylog@127.0.0.1:demo 5432 my_iot_dbms```

### Disconnecting from a local database
Disconnect is done by calling the disconnect command as follows:  
```disconnect dbms [dbms_name]```  
***[dbms_name]*** is the logical database name.

### Management commands
```show event log``` - shows the last events processed on the node.  
```show error log``` - shows the last errors identified on the node.   
```show file log``` - on an operator node, shows the last data files processed on the node.  
If keywords are added to the ***show*** commands, than the output considers only log entries containing the keywords.  
For example: ```show event log SQL``` will only show log entries containing the keyword ***sql***  

```dictionary show``` - shows definitions maintained in the dictionary.  
```directory show``` - show the active watch directories.  

## Configuration checklist

This section details a configuration checklist for each type of node in the cluster.
  
#### All Nodes

* Correct IP and ports defined. Use ```!ip``` to see the default IP used on each machine.
* Dictionary definitions that map to the directory structure used. Use ```dictionary show``` to see all the dictionary definitions.
* Listener for TCP incoming messages. Use ```show connections``` to see open connections. Use ```run tcp server [ip] [port]``` to declare a TCP connection.


If a local database is used to manage the metadata:
* Connect to the ***blockchain database***.
* If the ***ledger table*** was not created on the blockchain database, use ```blockchain create table``` to create the table.  

***Note:***  
Use ```show dbms``` to see the databases connected on each node.  
Use ```connect dbms psql [dbms user] [dbms port] [dbms name]``` to connect to a specif database.

#### Operator Node

* Test that the supported databases are connected. These needs to include the databases that support the user's data.
* Test that the ***watch directory*** is being used. Use ```directory show``` to see the watched directories. 

#### Publisher Node

* Test that the ***watch directory*** is being used. Use ```directory show``` to see the watched directories. 

#### Query Node

* Test that the ```system_query``` database is connected.
* Listener for REST incoming messages. Use ```show connections``` to see open connections. Use ```run rest server [ip] [port] [timeout]``` to declare a REST connection.

#### Master Node (if available)

* Test that the ```blockchain``` database is connected.

