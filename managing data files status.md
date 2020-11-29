# Managing Data files

Publisher nodes and devices are configured to send data to Operator nodes. Operators receive the data as JSON files or organize the data in JSON files.  
Sending data to nodes in the network is explained at [Adding Data to Nodes in the Network](blob/master/adding%20data.md#adding-data-to-nodes-in-the-network).  
If an Operator is associated with a cluster, it will distribute the JSON files to the cluster members. This process provodes HA and is explained at [Data Distribution and Configuration](blob/master/data%20distribution%20and%20configuration.md#data-distribution-and-configuration).

The JSON files follow a naming convention that include metadata information on the data contained in the file and is explained below.
Each Operator node maintains a set of tables to record information on each JSON file processed. The information in these tables allow to monitor the following:  
* The source of the the data.
* Timestamp associated with the file, the hash value of the file and the number of reading in the file.
* Errors during the load.     

The command ***time file*** allows to modify file names to follow the naming convention and to retrieve information on the files processed on each node. 

  
## The structure of the data files 
The data files contain Time Series Data (TSD) that is organized in JSON format.
Each file name follows a convention. To view the naming comvention use the command:  ```show json file structure```.
More details are provided below.

#### The file naming convention

File name is structured as follows:
<pre>
[dbms name].[table name].[data source].[hash value].[instructions].[TSD member].[TSD ID].[TSD date].[file type]

</pre>
[dbms name] - The name of the database to include the data.
[table name] - The name of the table to include the data.
[data source] - The ID of the data source generating the data.
[hash value] - The hash value of the file.
[instructions] - The ID of the policy that mapps the file data to a table structure (or '0' if no associated policy).
[TSD member] - If the file was send by a cluster member, the member ID sending the data.
[TSD ID] - The ID of the file in the TSD table.
[TSD date] - A 12 bytes key in the format: YYMMDDHHMMSS.
[file type] - json, for a JSON file.

## The info table

Nodes can monitor the state of the data files using a local database.
* The local database name is ```almgm``` (AnyLog Management).
* The local table name is ```tsd_info``` (Time Series Data Info).
* If the data is received from a cluster member, it will be menaged in a table called  ```tsd_id``` whereas id is the member ID in the cluster.

##### The structure of the ```tsd_info``` table:

* Each segment in the file name is a column in the table.
* The table includes 2 status fields which are updated as described below.
* The column ***Hash Value of Data*** is a 16 bytes number and serves as a unique key in the table.


## Identifying duplicate files

When a file is processed on a node, the Hash Value representing the file is calculated.  
If the value exists in the local ```almgm``` database, the file is treated as a duplicate file.

The following command determines the hash value of a file:  
```file hash [file name and path]```

## Creating and Updating the TSD tables
The ***tsd_info*** table organizes the information on the data received from Publishers and devices.  
The ***tsd_id*** are a set of tables whereas ***id*** is the ID of the cluster member that transferred the data.
These tables are created dynamically as data is processed in the cluster and if the ***almgm*** database is connected.
Managing the data data is with the following commands and processes:

* To connect to the ```almgm``` use the ***connect dbms*** command.  
Example: ```'connect dbms psql anylog@127.0.0.1:demo 5432 almgm```

* Creating the ```tsd_info``` table:  
```create table tsd_info where dbms = almgm```  
This call creates the table with the needed columns.

* Dropping the ```tsd_info``` table:  
```drop table tsd_info where dbms = almgm```  
This call creates the table with the needed columns.

## Time File command

The ***time file*** command allows to a) change file names to follow the data files naming convention and b) monitor the data ingested on each Operator node.

### Usage: 
 
#### Set the file name to satisfy the naming convention
<pre>
time file rename [source file path and name] to dbms = [dbms name] and table = [table name] and source = [source ID] and hash = [hash value] and instructions = [instructions id]
</pre>
This command will change the source file name to the convention using the values provided.  
If ***source*** is not provided, the value '0' is used.  
If ***hash*** value is not provided, the hash value of the file will be calculated.  
If ***instructions id*** is not provided, the value '0' is used.    

* Updating a new entry in the ```tsd_mgm``` table:   
```time file new [file name] status```

* Changing the status of a file:  
```time file update [hash value] [status]```

* Retrieving the status of a file:  
```time file get [hash value]```

* Calculating the hash value of a file:  
```file hash [path and file name]```
  
Examples:  

* For a given file, changing the file name to the convention described:  
```given_file = $HOME/AnyLog-Network/data/bkup/dweet_demo.94b54214_d0a9_4e92_8acc_e2b6675da185.2020_03_23_02_24_40_600Z.bldg_pmc.json```  
Changing the file name:  
```new_name = time file rename !given_file dbms = dweet_demo table = bldg_pmc par = 1 device = 265X48X2X34:2787 publisher = 548X23X243X12:2048```  
In this example, the hash value will be calculated and current time would be added to the file such that the new name satisfies the convention.  

* The new file name:  
```dweet_demo.bldg_pmc.1.265X48X2X34:2787.548X23X243X12:2048.2020-04-12T12:57:35Z.78eba9a0938d5f36b0a41135bf55b0e2.json```

* Updating the tsd_mgm table:  
```time file new !new_name delivered```

* Changing the status of a file:  
```time file update 78eba9a0938d5f36b0a41135bf55b0e2 Loaded```

* Retrieving the status of a file:  
```time file get 78eba9a0938d5f36b0a41135bf55b0e2```


---
Usage:

        time file rename [file name] to dbms = [dbms name] and table = [table name] and source = [source name] and instructions = [instructions id]
        time file new [file name] [optional status 1] [optional status 2]
        time file update [hash value] [optional status 1] [optional status 2]
        time file get [retrieve info]
        time file compare [file operator] [file standby] [output file]

Explanation:

        Manage a table with information about files ingested to the database. The table name is tsd_info and the database name is almgm
        To create a local table for a time file use: 'create table tsd_info where dbms = almgm'
        time file rename - Changes a file name to the standard name. If timestamp is not provided, current timestamp is used.
        File name is structured as: [dbms name].[table name].[source].[hash value].[instructions].json
        Values in brackets means a substring taken from the original name whereas the value represent location in the original name
        time file new - update the table tsd_info with new file info. Returns a unique id that represents the file
        time file update - update the time file status
                time file get - retrieve the info on an existing time file entry
                retrieve info can be one of the following:
                range where [conditions] - retrieve the hash values satisfying the condition
                        Output can be redirected to a file to compare values on differet machines
                * - retrieve all data
                Hash Value - retrieve info on a single time file event
                last n events
                count - return the number of events recorded in the tsd_info table
                compare - compare the hash values in 2 sorted files to determine
                        the hash values in the first file which are missing in the second file

Examples:

        time file get range where time >= '2020-01-01' and time < '2021-01-01' into !outfile
        time file rename !json_file to dbms_name = [0] and table_name = [1]
        time file update 6c78d0b005a86933ba44573c09365ad5 "From Publisher 778299-2" "File delivered to backup"
        time file new !json_file
        time file get *
        time file get 6c78d0b005a86933ba44573c09365ad5
        time file get last 20 events
        time file get count
        time file compare !file1 !file2 !outfile

Link: https://github.com/AnyLog-co/documentation/blob/master/managing%20data%20files%20status.md#managing-data-files

