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
If ***dbms*** or ***table*** are not provided, they are unchanged.  
If ***source*** is not provided, the value '0' is used.  
If ***hash*** value is not provided, the hash value of the file will be calculated.  
If ***instructions id*** is not provided, the value '0' is used.   

Examples:
1) The example below adds the hash value to the file name.
<pre>
 time file rename !prep_dir/lsl_demo.ping_sensor.json
</pre>
2) The example below modifies the file name to include a different table name and the hash value.
<pre>
 time file rename !prep_dir/lsl_demo.ping_sensor.json to table = heat_sensor 
</pre>

#### Show the list of TSD tables on this node
<pre>
time file tables
</pre>

#### Add a new entry to the TSD table
<pre>
time file new [file name] [optional status 1] [optional status 2]
</pre>
This command will add the information in the file name as a new entry to the ***tsd_info*** table.

#### Update the status fields in an TSD entry
<pre> 
time file update [hash value] [optional status 1] [optional status 2]
</pre>
This command will update the status fields in a ***tsd_info*** entry with the specified hash value.    
Example:
<pre> 
time file update 6c78d0b005a86933ba44573c09365ad5 "From Publisher 778299-2" "File delivered to backup"
</pre>

#### Retrieve information from a TSD table
The following call allows to retrieve information from a TSD table:
<pre> 
time file get [options]
</pre>
Options determine the information of interest, expressed as a where condition with key-value pairs and is summarized below. 
 
| Key        | Value  | Default | 
| ---------- | -------| -------| 
| limit    | Setting a limit on the number of rows retrieved from the table, 0 value sets no limit. | 100 |
| table    | The name of the table to use. | tsd_info |
| hash    | retrieve a key with the specified hash value. | |
| start_date | retrieve entries with a date greater or equal to the start_date. | |
| end_date | retrieve entries with a date earlier than the end_date. | |
  
Examples:  
<pre> 
time file get
time file get where table = tsd_123 and hash = 6c78d0b005a86933ba44573c09365ad5
time file get where start_date = -3d and end_date = -2d
</pre>

