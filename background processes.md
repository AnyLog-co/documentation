# Background Processes

Background processes are optional processes that if activated, are running using dedicated threads according to the user specifications.

The background threads:

1. A listener for the AnyLog Messaging. Activated by the command: ```run tcp server```
2. A listener for a user REST Request.  Activated by the command: ```run rest server```
3. An automated Operator process. Activated by the command: ```run operator```
4. An automated Publisher process. Activated by the command: ```run publisher```
5. An automated Blockchain Synchronizer. Activated by the command: ```run blockchain sync```
6. A Scheduler process. Activated by the command ```run scheduler```
7. The HA process. Activated by the command ```run ha```

These processes are activated on the AL command line. Command line options are available using ***help***  

## AnyLog Messaging

A listener thread on a declared IP and port.  
The listener is required to receive AnyLog messages from peers in the network. 

## REST requests

A listener thread on a declared IP and port.  
The listener is required to receive REST requests from users of the network.

## Operator Process

A process that identifies JSON files, transforms the files to a structure that can be assigned to a data table and inserts the data to a local database.
Files ingested are recorded such that it is possible to trace the source data and source device of data readings.

#### Overview
Files are placed in a ***Watch Directory***. The Watch Directory is a designated directory such that every file that is copied to the directory is being processed.  
Processing is determined by the type of the file and by ***Instructions*** if the file is associated with Instructions.  
The processing is by mapping each JSON file to SQL Insert Statements such that the JSON data is added to a local database.

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
  

  

 

