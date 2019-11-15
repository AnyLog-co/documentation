# Running an AnyLog instance and AnyLog commands

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

### Disconnecting from a logical database
Disconnect is done by calling the disconnect command as follows:  
```disconnect dbms [dbms_name]```  
***[dbms_name]*** is the logical database name.

