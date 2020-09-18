# Background Processes

Background processes are optional processes that if activated, are running using dedicated threads according to the user specifications.

The background threads:

1. A listener for the AnyLog Peer-to-Peer Messaging. Activated by the command: ```run tcp server```
2. A listener for a user REST Request.  Activated by the command: ```run rest server```
3. An automated Operator process. Activated by the command: ```run operator```
4. An automated Publisher process. Activated by the command: ```run publisher```
5. An automated Blockchain Synchronizer. Activated by the command: ```run blockchain sync```
6. A Scheduler process. Activated by the command ```run scheduler```
7. The HA process. Activated by the command ```run ha```

These processes are activated on the AL command line. Command line options are available using ***help***  

## AnyLog Messaging

A process that receives messages from member nodes in the network. This process makes the node a member in the AnyLog Network.  

Usage:
<pre>
run tcp server [ip] [port] [threads]
</pre>
Explanation:  
[ip] [port] - The process listens for incomming messages on the assigned IP and and Port.
[Threads] - An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 1

 
## REST requests

A process that receives REST messages from users and applications which are not members of the network.  
This process receives requests to query data and metada, process the request and replies with the requested information.

Usage:
<pre>
run rest server [ip] [port] [timeout]
</pre>
Explanation:  
[ip] [port] - The process listens for incomming messages on the assigned IP and and Port.  
[timeout] - An optional parameter that determines wait a timeout period in seconds.    
When a REST request is issued, if a respond is not provided within the specified wait time, the request process terminates.  A 0 value means no wait limit and the default value is 20 seconds.

## Operator Process

A process that places users data in a local database. The Operator identifies JSON files, transforms the files to a structure that can be assigned to a data table and inserts the data to a local database.  
Files ingested are recorded such that it is possible to trace the source data and source device of data readings.

#### Overview
Files with new data are placed in a ***Watch Directory***. The Watch Directory is a designated directory such that every file that is copied to the directory is being processed.  
Processing is determined by the type of the file and by ***Instructions*** if the file is associated with policies that modify the default processing.    
The processing is by mapping the data in each JSON file to SQL Insert Statements that update a local database.

#### The mapping process
The JSON file name follows a convention that uniquely identifies the file and determines the processes that assign the JSON data to a table.  
The file naming convention id detailed at the [metadata section.](https://github.com/AnyLog-co/documentation/blob/master/metadata.md#file-names)
From the file name, the logical database and table names are determined. In addition, the file name optionaly includes the ID of the Mapping Instructions.  
Mapping instructions are detailed in the [mapping data to tables section.](https://github.com/AnyLog-co/documentation/blob/master/mapping%20data%20to%20tables.md)  

#### Recording file ingested
This is an optional process to recod the details of the ingested files.
When JSON files are processed, a local table named **tsd_info** assigned to a database named **almgm** is updated to reflect the list of files processed.  
Interaction with the data maintained by **tsd_info** is by the command ```time file```.  The command provides the functionality to create the table and retrieve the data maintained in the table.  
The information maintained by **tsd_info** is leveraged to trace source data, source devices, and to support the High Availability (HA) processes.

Usage:
<pre>
run operator where [option] = [value] and [option] = [value] ...
</pre>
        
Explanation:  
Monitors new data added to the watch directory and load the new data to a local database.
Options:  

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| watch_dir  | The location of the watch directory.  | !watch_dir  |
| bkup_dir   | The directory location to store JSON and SQL files that were processed successfully.  | !bkup_dir. |
| error_dir   | The directory location to store files containing data that failed processing.  | !error_dir. |
| delete_json   | True/False for deletion of the JSON file if processing is successful.  | false |
| delete_sql   | True/False for deletion of the SQL file if processing is successful.  | false |
| compress_json   | True/False to enable/disable compression of the JSON file if processing is successful.  | false |
| compress_sql   | True/False to enable/disable compression of the SQL file if processing is successful.  | false |
| move_json   | True moves the JSON file to the 'bkup' dir if processing is successful.  | false |
| move_sql   | True moves the SQL file to the 'bkup' dir if processing is successful.  | false |
| dbms_name   | The segment in the file name from which the database name is taken.  | 0 |
| table_name   | The segment in the file name from which the table name is taken.  | 1 |
| limit_tables   | a list of comma separated names within brackets listing the table names to process.  |  |
| craete_table   |  A True value creates a table if the table doesn\'t exists.  | true |
| master_node   |  The IP and Port of a Master node (if a master node is used).  |  |
| update_tsd_info   | True/False to update a summary table (tsd_info table in almgm dbms) with status of files ingested.  |  |

Examples:  
Usage:
<pre>
run operator where create_table = true and dbms_name = file_name[0] and table_name = file_name[1] and source = file_name[2] and compress_sql = true and compress_json = true and update_tsd_info = true
</pre>

## Publisher Process

A process that identifies JSON files and distributes the files to Operators that are hosting the data.

#### Overview
Files are placed in a ***Watch Directory***. The Watch Directory is a designated directory such that every file that is copied to the directory is being processed.  
The process locates from the blockchain the Operators that are hosting the table's data, designates an Operator to the file and transfers the file to the designated Operator.  
  

## Blockchain Synchronizer

A process that maintains an updated version of the blockchain data.
With a master node, the process sends a message to the master node to receive updates of the metadata.

## Scheduler Process
 
A process that triggers the scheduled tasks.
 
## HA Process
 
Delivers data files processed by the local node to a standby node or nodes.  
When an operator ingests data, the process records the hash values of the files ingested.
    
If HA is activated, every file processed is transferred to the standby nodes. 
Users can enable a synchronization process to validate that all the data on a particular node is available on the standby nodes and if differences are found, the process will transfer the needed data to make the nodes identical.  
  

  

 

