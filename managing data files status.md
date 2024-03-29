# Managing Data files

Publisher nodes and devices are configured to send data to Operator nodes. Operators receive the data as JSON files or organize the data in JSON files.  
Sending data to nodes in the network is explained at [Adding Data to Nodes in the Network](adding%20data.md#adding-data-to-nodes-in-the-network).  
If an Operator is associated with a cluster, it will distribute the JSON files to the cluster members. This process provides HA and is explained at [Data Distribution and Configuration](data%20distribution%20and%20configuration.md#data-distribution-and-configuration).

The JSON files follow a naming convention that include metadata information on the data contained in the file and is explained below.
Each Operator node maintains a set of tables to record information on each JSON file processed. The information in these tables allow to monitor the following:  
* The source of the data.
* Timestamp associated with the file, the hash value of the file and the number of reading in the file.
* Errors during the load.     

The command `time file` allows to modify file names to follow the naming convention and to retrieve information on the files processed on each node. 

  
## The structure of the data files 
The data files contain Time Series Data (TSD) that is organized in JSON format.
Each file name follows a convention. To view the naming convention use the command: 
```anylog
AL anylog-node > get json file struct
[dbms name].[table name].[data source].[hash value].[mapping policy].[TSD member ID].[TSD row ID].[TSD date].json
```
More details are provided below.

#### The file naming convention

File name is structured as follows:
```anylog
[dbms name].[table name].[data source].[hash value].[instructions].[TSD member].[TSD ID].[TSD date].[file type]
```

| Name Section | Functionality  | 
| ---------- | -------| 
| dbms name | The name of the database to include the data. |
| table name | The name of the table to include the data.  | 
| data source | The ID of the data source generating the data. | 
| hash value | The hash value of the file. | 
| instructions | The ID of the policy that maps the file data to a table structure (or '0' if no associated policy). | 
| TSD member | If the file was send by a cluster member, the member ID sending the data. | 
| TSD ID | The ID of the file in the TSD table. | 
| TSD date | A 12 bytes key in the format: YYMMDDHHMMSS representing the date and time the file was processed. | 
| file type | json, for a JSON file. | 

## The info table

Nodes can monitor the state of the data files using a local database.
* The local database name is `almgm` (AnyLog Management).
* The local table name is `tsd_info` (Time Series Data Info).
* If the data is received from a cluster member, it will be managed in a table called  `tsd_id` whereas id is the member ID in the cluster.

##### The structure of the `tsd_info` table:

* Each segment in the file name is a column in the table.
* The table includes 2 status fields which are updated as described below.
* The column ***Hash Value of Data*** is a 16-bytes number and serves as a unique key in the table.


## Identifying duplicate files

When a file is processed on a node, the Hash Value representing the file is calculated.  
If the value exists in the local `almgm` database, the file is treated as a duplicate file.

The following command determines the hash value of a file:  
```anylog 
file hash [file name and path]
```

## Creating and Updating the TSD tables
The `tsd_info` table organizes the information on the data received from Publishers and devices.  
The `tsd_id` are a set of tables whereas _id_ is the ID of the cluster member that transferred the data.
These tables are created dynamically as data is processed in the cluster and if the `almgm` database is connected.
Managing the data is with the following commands and processes:

* To connect to the `almgm` use the `connect dbms` command.   

```anylog
AL anylog-node > connect dbms almgm where type=psql and ip=127.0,0.1 and port=5432 and user=admin and password=passwd
```

* Creating the `tsd_info` table:  
```anylog
AL anylog-node > create table tsd_info where dbms = almgm
```  
This call creates the table with the needed columns.

* Dropping the `tsd_info` table:  
```anylog
drop table tsd_info where dbms = almgm
```

This call creates the table with the needed columns.

## Time File commands

The `time file` commands are a set of commands to monitor and manage data ingested on each Operator node.

### Usage: 
 
**Set the file name to satisfy the naming convention**
The `time file rename` command changes the names of files containing data to follow the data files naming convention.  
  
```anylog
time file rename [source file path and name] to dbms = [dbms name] and table = [table name] and source = [source ID] and hash = [hash value] and instructions = [instructions id]
```
This command will change the source file name to the convention using the values provided.
If _dbms_ or _table_ are not provided, they are unchanged.  
If _source_ is not provided, the value '0' is used.  
If _hash_ value is not provided, the hash value of the file will be calculated.  
If _instructions id_ is not provided, the value '0' is used.   

Examples:
1) The example below adds the hash value to the file name.
```anylog
time file rename !prep_dir/lsl_demo.ping_sensor.json
```

2) The example below modifies the file name to include a different table name and the hash value.
```anylog
time file rename !prep_dir/lsl_demo.ping_sensor.json to table = heat_sensor 
```

#### Show the list of TSD tables on this node
```anylog
time file tables
```

#### Add a new entry to the TSD table
Adding data to a TSD table is by associating to a file that is named using the naming convention.  
The proces retrieves the info from the file name and updates a TSD table. Below is the command format:
```anylog
time file new [file path and name] [optional status 1] [optional status 2] [optional: using the keyword into and: TSD table name and a row id]
```
[file path and name] - a path to a file that is named according to the JSON file naming convention.    
[optional status 1] - a first status field in the table.  
[optional status 2] - a second status field in the table.    

Example:
```anylog
time file new !prep_dir/lsl_demo.ping_sensor.0.c490e6000d9487962d890a7cba2e1e74.0.json 
```

To validate that the file exists on the local directory use the keyword `add`. 
```anylog
time file add [file path and name] [optional status 1] [optional status 2] [optional: using the keyword into and: TSD table name and a row id]
```

#### Update the status fields in an TSD entry
```anylog 
time file update [hash value] [optional status 1] [optional status 2]
```
This command will update the status fields in a _tsd_info_ entry with the specified hash value.    
**Example**:
```anylog 
time file update 6c78d0b005a86933ba44573c09365ad5 "From Publisher 778299-2" "File delivered to backup"
```

