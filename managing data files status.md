# Managing Data files

A Publisher Node sends data to one or multiple servers. A server may be down and the data may not be transferred to the server. In addition, when the data is processed by the Operator, the data load may fail.  
The status of each data file is registered on the Publisher Node and the Operator Node. Each node updates the status and satisfies queries on the status of each file.

The processes described below are optional and activation requires the relevant scripts.
  
## The structure of the data files 
The data files contain Time Series Data (TSD) that is organized in JSON format.
Each file name follows a convention that is described below:

#### The file naming convention

File name is structured as follows:
<pre>
[DBMS name].[Table Name].[ID device].[ID Operator].[Timestamp].[Hash Value of Data].[File Type]
</pre>
[Local File ID] - Sequential File ID
[DBMS name] - The logical database name      
[Table Name] - The data table name    
[ID device] - Unique ID of the data source (i.e. the device generated the data)    
[ID Publisher] - Unique ID of the publisher  
[Time] - Time assigned to the file    
[Hash Value of Data] - Unique ID of the data file  
[File Type] - Describing how data is organized (JSON/SQL).  

#### The info table

Nodes can monitor the state of the data files using a local database.
* The local database name is ```almgm``` (AnyLog Management).
* The local table name is ```tsd_info``` (Time Series Data Info).

##### The structure of the ```tsd_info``` table:

* Each segment in the file name is a column in the table.
* The table includes a status field which is updated as described below.
* The column ***Hash Value of Data*** is a 16 bytes number and serves as a unique key.
* Each row in the table is extended with a 2 status fields. The status fields are described below.

##### The values on the status fields:

***On the Operator Node:***  
Status Field 1 is not in use.  
Status Field 2 is updated with the value 1 when the data file is loaded.

***On the Publisher Node:***  
Status Field 1 lists the Hosts and Ports to the destination servers where the data file was send.  
Status Field 2 is maintains the status for each destination server as follows:
Status 0 means the data was send  
Status 1 means the destination server processed the data. Status 1 is updated when a destination server reports on sucessful processing.

## Identifying duplicate files

When a Publisher or an Operator process a file, the Hash Value representing the file is calculated.  
If the value exists in the local database, the file is treated as a duplicate file.

The following command determines the hash value of a file:  
```file hash [file name and path]```

## Creating and Updating the ```tsd_info``` table




