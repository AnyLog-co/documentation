# Metadata Requests

Nodes in the network interact with a global metadata layer that manages and synchronizes the data views and processes among 
the member nodes and with a local setup and configurations that determine how data is managed locally on the node.  

An overview on the global metadata layer is provided in [Managing Metadata](metadata%20management.md#managing-metadata).  
This document explains the layout and organization of the data on the nodes and how the node processes interact with the global and local metadata.  
 
Note: The processes of a node in the network are agnostic to where the global metadata is hosted (a blockchain or a master node). 
References to the blockchain should be interpreted as references to the metadata that can be hosted using a blockchain as well as a master node.

## Creating data tables

The structure of each table can be determined by users or generated dynamically, based on the attributes names and the values in the JSON files.  
When a file is ingested, and a schema is not available, the table schema is created dynamically.    
When a schema is first created (by a user or by a node in the network), it is added as a policy to the blockchain such that the table's schema is available to all 
the nodes in the network. If a table is available as a policy on the blockchain, a node that needs to manage data associated with the table retrieves the policy and 
transforms the policy to a table that is maintained by a local database.  
A node can determine to partition the data by time. This process is done by declaring the table and the time interval for partitioning. The partitioning 
is transparent to the query processes in the network.  
The partitioning command is as follows:
```anylog
partition [dbms name] [table name] using [column name] by [time interval]
```
An example of time partitioning is the following configuration command:  
```anylog
partition dmci ping_sensor using timestamp by 1 month
```
Once a table schema is available, the ingestion process maps the data in the JSON files to the table's schema.


### Adding data

A node that hosts the data is responsible to satisfy queries over the data. The way the data is managed on each node can vary as long
as the query protocol and interfaces are satisfied.
Data can be received as files in JSON format or can be collected by the node and transformed to files in JSON format.  
The JSON files are placed in a _watch_ directory and ingested to the local database.
The _watch_ directory is determined by the configuration and when a file is placed in the directory, it is read and ingested by the local databases.  
A description of the directory structure of a node is available at the section [Local Directory Structure](getting%20started.md#local-directory-structure).  
The section [Adding Data](adding%20data.md#adding-data-to-nodes-in-the-network) 
details how watch-directories are used and how data is added to nodes in the network using REST.       
The section [Using MQTT Broker](message%20broker.md#using-a-message-broker) details how data is added using a broker.  

### File names

The sensor data (or time series data) is placed in the `watch` directory.
The file name follows a convention that determines how the file is being processed.    
The command `get json file struct` details the file structure convention and has the following output:  
```anylog
[dbms name].[table name].[data source].[hash value].[instructions].[TSD member ID].[TSD row ID].[TSD date].json
```

The file type is _JSON_ indicating the internal structure.  
The file name structure is composed of 8 substrings separated by a period. The substrings are as follows:

| Section       | Explanation  | Mandatory  |
| ------------- | ----------- | --------  |
| DBMS Name | The logical database name | Yes |
| Table Name | The logical table that contains the file data. | Yes |
| Source | An ID that identifies the source of the data. | No |
| Hash | A hash value that uniquely identifies the file by the contents of the file. | No |
| Instructions | An ID that identifies the set of instructions that map the JSON data to the table structure. | No |
| TSD member ID | An ID of the TSD table containing information on the JSON file. | No |
| TSD row ID | The ID of the row in  the TSD table that contains information about the file. | No |
| TSD date | The time and date when the file was ingested to the local database. | No |

Note: Details on the TSD tables is available at [Managing Data files](managing%20data%20files%20status.md#managing-data-files).

### File ingestion

When a file is ingested, the local node determines if the table exists in the local database.  
If the table does not exist, the node will determine if the table was declared by a different node and appears on the blockchain.  
If the table is available on the blockchain, the node will create an identical table on the local database.  
If the table is not available on the blockchain, the node will create the table and register the table on the blockchain.  
When the table is located or created, the file is ingested using one of 2 methods:  
1. The default mapping - attribute names are assigned to column names. If a column name is not part of the table's structure, the attribute value is ignored.  
2. If mapping _instructions_ appears in the file name, the instructions override, for the relevant columns, the default mapping of step 1.


### Creating a local dbms table published as a policy on the blockchain

The command: `create table [table name] where dbms = [dbms name]` creates a table assigned to the logical database with a schema identical to the schema published on the blockchain for the named table.


## Retrieving the list of databases

### The local databases

A node may manage data locally. The command `get databases` lists the databases that are serving data on the local node.  
The listed databases are available to host data and query data and were assigned using the command `connect dbms`.  

**Example**:
```anylog
AL anylog-network > get databases
List of DBMS connections
Logical DBMS         Database Type IP:Port                        Storage
-------------------- ------------- ------------------------------ -------------------------
almgm                psql          127.0.0.1:5432                 Persistent
dmci                 psql          127.0.0.1:5432                 Persistent
system_query         sqlite        Local                          Memory
```

### The network databases

The following command retrieves the list of databases on the network.
```anylog
get network databases
```
Or if company name is included in the JSON policies:
```anylog
get network databases where company = my_company
```

### The network tables
The following command retrieves the list of tables declared the network and determines which table is hosted on the current node.
```anylog
get tables where dbms = [dbms name]
```

The following example retrieves all tables:
```anylog
get tables where dbms = *
```

And an example output is the following:
```anylog
Database      Table name   Local DBMS  Blockchain
-------------|------------|----------------------|
litsanleandro|ping_sensor |           |     V    |
dmci         |cos_data    |     V     |     V    |
             |sin_data    |     V     |     V    |
             |machine_data|     V     |     V    |
orics        |sensor_1    |           |     V    |
             |sensor_2    |           |     V    |
             |sensor_3    |           |     V    |
             |sensor_4    |           |     V    |
             |sensor_5    |           |     V    |
```

###  Retrieving the columns list for a Tables

The following command retrieves the list of columns and the data types for a particular table:
```anylog
get columns where dbms = [dbms name] and table = [table name]
```

The list represents the columns declared on the global metadata layer.

Example:
```anylog
get columns where dbms = dmci and table = machine_data
```

To retrieve how the table is declared on  the local database on this node use the following command:

```anylog
info table [dbms name] [table name] columns
```

Example:
```anylog
info table dmci machine_data columns
```

### Validating a schema

As a schema of a table can exist on the local database and on the blockchain, the command `test table` compares the table definitions on the local database with the schema definition on the blockchain.  
The structure of the command is as follows:  
```anylog
test table [table name] where dbms = [dbms name]
```

Example: 
```anylog
test table ping_sensor where dbms = lsl_demo
``` 



