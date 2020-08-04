# Background Processes

Background processes are optional processes that if activated, are running using dedicated threads according to the user specifications.

The background threads:

1. A listener for the AnyLog Messaging. Activated by the command: ```run tcp server```
2. A listener for a user REST Request.  Activated by the command: ```run rest server```
3. An automated Operator process. Activated by the command: ```run operator```
4. An automated Publisher process. Activated by the command: ```run publisher```
5. An automated Blockchain Synchronizer. Activated by the command: ```run blockchain sync```
6. A Scheduler process. Activated by the command ```run scheduler```

These processes are activated on the AL command line. Command line options are available using ***help***  

## AnyLog Messaging

A listener thread on a declared IP and port.  
The listener is required to receive AnyLog messages from peers in the network. 

## REST requests

A listener thread on a declared IP and port.  
The listener is required to receive REST requests from users of the network.

## Operator Process

A process that identifies JSON files, transforms the files to a structure that can be assigned to a data table and inserts the data to a local database.
Files injested are recorded such that it is possible to trace the source data and source device of data readings.

## Publisher Process

A process that identifies JSON files and distributes the files to Operators that are hosting the data.

## Blockchain Synchronizer

A process that maintains an updated version of the blockchain data.
With a master node, the process sends a message to the master node to receive updates of the metadata.

 ## Scheduler Process
 
 A process that triggers the scheduled tasks.
 


