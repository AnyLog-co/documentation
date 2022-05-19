# Managing Data files

Publisher nodes and devices are configured to send data to Operator nodes. Operators receive the data as JSON files or organize the data in JSON files.  
Sending data to nodes in the network is explained at [Adding Data to Nodes in the Network](blob/master/adding%20data.md#adding-data-to-nodes-in-the-network).  
If an Operator is associated with a cluster, it will distribute the JSON files to the cluster members. This process provides HA and is explained at [Data Distribution and Configuration](blob/master/data%20distribution%20and%20configuration.md#data-distribution-and-configuration).

The JSON files follow a naming convention that include metadata information on the data contained in the file and is explained below.
Each Operator node maintains a set of tables to record information on each JSON file processed. The information in these tables allow to monitor the following:  
* The source of the the data.
* Timestamp associated with the file, the hash value of the file and the number of reading in the file.
* Errors during the load.     

The command ***time file*** allows to modify file names to follow the naming convention and to retrieve information on the files processed on each node. 

  
## The structure of the data files 
The data files contain Time Series Data (TSD) that is organized in JSON format.
Each file name follows a convention. To view the naming comvention use the command:  ```get json file struct```.
More details are provided below.

#### The file naming convention

File name is structured as follows:
<pre>
[dbms name].[table name].[data source].[hash value].[instructions].[TSD member].[TSD ID].[TSD date].[file type]
</pre>

| Name Section | Functionality  | 
| ---------- | -------| 
| dbms name | The name of the database to include the data. |
| table name | The name of the table to include the data.  | 
| data source | The ID of the data source generating the data. | 
| hash value | The hash value of the file. | 
| instructions | The ID of the policy that mapps the file data to a table structure (or '0' if no associated policy). | 
| TSD member | If the file was send by a cluster member, the member ID sending the data. | 
| TSD ID | The ID of the file in the TSD table. | 
| TSD date | A 12 bytes key in the format: YYMMDDHHMMSS representing the date and time the file was processed. | 
| file type | json, for a JSON file. | 

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

## Time File commands

The ***time file*** commands are a set of commands to monitor and manage data ingested on each Operator node.

### Usage: 
 
#### Set the file name to satisfy the naming convention
The ***time file rename*** command changes the names of files containing data to follow the data files naming convention.  
Usage:  
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
Adding data to a TSD table is by associating to a file that is named using the naming convention.  
The proces retrieves the info from the file name and updates a TSD table. Below is the command format:
<pre>
time file new [file path and name] [optional status 1] [optional status 2] [optional: using the keyword into and: TSD table name and a row id]
</pre>
[file path and name] - a path to a file that is named according to the JSON file naming convention.    
[optional status 1] - a first status field in the table.  
[optional status 2] - a second status field in the table.    

Example:
<pre>
time file new !prep_dir/lsl_demo.ping_sensor.0.c490e6000d9487962d890a7cba2e1e74.0.json 
</pre>

To validate that the file exixts on the local directory use the ketword ***add**. 
<pre>
time file add [file path and name] [optional status 1] [optional status 2] [optional: using the keyword into and: TSD table name and a row id]
</pre>

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
The following command retrieves information from a TSD table. The information includes the details of each file ingested to the local database.
<pre> 
time file get where [options]
</pre>
Options are optional and determine the information of interest, expressed as a where condition with key-value pairs and is summarized below. 
 
| Key        | Value  | Default | 
| ---------- | -------| -------| 
| limit    | Setting a limit on the number of rows retrieved from the table, 0 value sets no limit. | 100 |
| table    | The name of the table to use. | tsd_info |
| hash    | Retrieve a key with the specified hash value. | |
| start_date | Retrieve entries with a date greater or equal to the start_date. | |
| end_date | Retrieve entries with a date earlier than the end_date. | |
| format | Output format - ***table*** or ***json***  | table |
  
Examples:  
<pre> 
time file get
time file get where table = tsd_123 and hash = 6c78d0b005a86933ba44573c09365ad5
time file get where table = tsd_info and hash = a00e6d4636b9fd8e1742d673275a75f7 and format = json
time file get where start_date = -3d and end_date = -2d
</pre>


#### Retrieve summary information from a TSD table
The following command retrieves summary information from a TSD table. 
<pre> 
time file summary where [options]
</pre>
Options are optional and determine the information of interest, expressed as a where condition with key-value pairs and is summarized below. 
 
| Key        | Value  | Default | 
| ---------- | -------| -------| 
| table    | The name of the table to use. | tsd_info |
| start_date | retrieve entries with a date greater or equal to the start_date. | |
| end_date | retrieve entries with a date earlier than the end_date. | |

Note: Setting a star sign (*) for a table name provides information from all the TSD tables hosted on the node.  
Examples:  
<pre> 
time file summary
time file summary where table = *
time file summary where start_date = -3d
</pre>

An example of the output is the following:
<pre>
DBMS          Table       Start Date          From ID End Date            To ID Files Count Source Count Status 1 Status 2 Total Rows
-------------|-----------|-------------------|-------|-------------------|-----|-----------|------------|--------|--------|----------|
litsanleandro|heat_sensor|2021-04-02 02:47:56|      1|2021-04-02 17:50:01|   50|         50|           1|       1|       1|   453,455|
litsanleandro|ping_sensor|2021-04-02 02:47:56|      1|2021-04-02 17:50:01|  378|        378|           1|       1|       1|    77,624|
</pre>
The output provides the summary on each table as follows:
| Column name| explanation | 
| ---------- | -------|
| DBMS | The DBMS containing the ingested data |
| Table | The Table containing the ingested data |
| Start Date | The first date within the requested time range with data ingested |
| From ID | The first Row ID in the TSD table within the requested time range |
| End Date | The last date within the requested time range with data ingested |
| To ID | The last Row ID in the TSD table within the requested time range |
| Files Count | The number of files ingested within the requested time range |
| Source Count | The number of sources (like sensors) providing data during the requested time range |
| Status 1 | The number of unique status-message updates in the "status 1" coulumn. The value 1 indicates all status messages are the same |
| Status 2 | The number of unique status-message updates in the "status 2" coulumn. The value 1 indicates all status messages are the same |
| Total Rows | The number of rows ingested in the requested time range |

#### Retrieve the list of files which were not ingested on the local node
The following command retrieves the list of files that were identified as missing and the source node failed to deliver. 
<pre> 
time file errors where [options]
</pre>
The options are the same as the options in the [time file get](#retrieve-information-from-a-tsd-table) command. 

#### Creating and dropping the TSD tables
The ***tsd_info*** table is created using the following command:
<pre> 
create table tsd_info where dbms = almgm
</pre>
Tables that represent members of the cluster are created dynamically.  

Local TSD tables can be dropped using one of the following commands:
<pre> 
drop table [tsd table name] where dbms = almgm
</pre>
or
<pre> 
time file drop [table name]
</pre>
Dropping all TSD tables is by the following command:
<pre> 
time file drop all
</pre>

Examples:  
<pre> 
drop table tsd_info where dbms = almgm
time file drop tsd_123
time file drop all
</pre>

#### Deleting a single TSD row
Usage
<pre> 
time file delete [row id] from [tsd table name]
</pre>

Examples:  
<pre> 
time file delete 16 from tsd_info
time file delete 126 from tsd_129
</pre>
  
