# Managing Metadata

The metadata is organized on a global metadata platform. The platform can be one of the following:
* A blockchain platform.
* A master node.
***A Master Node*** is node that maintains a complete copy of the Metadata in a local database.
  
Every node in the network is configured to periodically retrieve updates from the global platform and on each node, 
the metadata is organized in a local log file in a JSON format.  
A node operates with the global metadata as follows:  
* The node operates against the local log file and does not require continues connection to a blockchain.
* The node may maintain a copy of the local JSON log file on a local database.
* The node may update a global metadata with changes to the metadata.
* Every node is configured to retrieve all updates from the global platform.  

When a node joins the network, the node can download the existing metadata from a Master Node or from the blockchain.
A node may also store a copy of the metadata on a local database. However, for a node to operate, the node only needs the local log file.
On each node, the metadata represents the information which is relevant to the particular node and therefore the metadata on each node may be different.
When nodes make changes to the metadata, these changes become available to all nodes of the network by the processes explained below.
Each node may be configured such that it will continuously get updates of changes to the metadata. 

Members of the network can synchronize their metadata with other members of the network in 2 ways:

* Using a blockchain - By sending updateds to the blockchain and retrieving the metadata from the blockchain.
* Using a Master Node - By sending updateds to the Master Node and receiving updates from the Master Node/

### Updating a blockchain
This functionality has not been yet released.

### Updating a master node:

When metadata is created, use the AnyLog command ```blockchain push``` to send the JSON file to the master node

#### To retrieve data from the master node:

* Use the command ```blockchain pull to log``` to pull the log file from the master node. The output file will be paced in the blockchain directory. The file name is prefixed by the name of the log file and the suffix is '.new'.
* Use the command ```blockchain pull to dbms``` to pull the metadata from the master node. The output file is a set of SQL insert statements that will update a local database with the metadata. The file name is prefixed by the name of the log file and the suffix is '.new.sql'.
* To update the local copy of the log file, use the ```file get``` command to copy the metadata log file from a Master Node.
* To update the local database with the updates to the metadata, place the insert statement file in the watch directory.
* To copy these files from the master node, use the command ```file get [source location] [destination location]``` whereas:
    * [source location] is the path name and file name on the master node.
    * [destination location] is the path name and file name on the requesting node. 
    
The following script pulls the metadata from a Master Node and copies the log file to the local node to serve as the metadata on the local node.  
```
run client [ip]:[port] "blockchain pull to log"    # create a copy of the log file on the Master Node
run client [ip]:[port] "file get [source path and file name] [destination path and file name] # copy the log file from the Master Node to the Local Node.
```
In the following script:  
``` [ip]:[port] ``` - the ip and port of the Master Node.  
```[source path and file name]``` - the path and file name of the log file on the Master Node.  
```[destination path and file name]``` - the path and file name of the metadata log file on the Local Node.

## Blockchain commands

```blockchain add [JSON data]``` - add the JSON data to the local file that represents the metadata.  
```blockchain get [JSON key attribute pairs]``` - retrieve from the local file the metadata that satisfies the key attribute pairs.  
```blockchain push [JSON data]``` - add a JSON string to the Master Node that hosts the metadata.  
```blockchain pull [to log or dbms]``` - get a copy of the blockchain from the master node.  
```blockchain create table``` - create the ledger table in the database that maintains a copy of the metadata.  

## Using a local database

A node may keep a copy of the blockchain data on a local database. On the local database, the blockchain data is maintain in a table called ***ledger***.   

The following process creates the local blockchain database:

* Define a location for the blockchain log file by declaring ***blockchain_file*** constant 
with the path and file name of the log file.  
Example: ```blockchain_file = $HOME/AnyLog-Network/data/blockchain/blockchain.txt```

* Connect the node to the local database.    
Example using PostgreSQL to manage the blockchain data:  
```connect dbms psql anylog@127.0.0.1:demo 5432 blockchain```  
Example using SQLite to manage the blockchain data:   
```connect dbms sqlite anylog@127.0.0.1:demo 5432 blockchain```

* Create the local ***ledger*** table.  
```blockchain create table```  
The command will create the 'ledger' table in the database assigned to 'blockchain'.

## Creating tables

The structure of each table can be determined by users or generated dynamically, based on the attributes names and the values in the JSON file.  
When a file is ingested, and a schema is not available, and a user provided schema is not available, the  
tables is ctreated dynamically.    
Once a table schema is avaiable, the ingestion process maps the attribute names and values to the table's columns names and values.

### File names

The sensor data (or time series data) is placed in the ***Watch Sirectory***.  
The file name follows a convention that determines how the file is being processed and if needed, allows to locate the file based on the properties of the data being ingested.  
The file type is ***json*** indicating the internal structure.  
The file name structure is composed of 5 substrings seperated by a period. The subsyrings are as follows:
<pre>
DBMS Name - The logical database name
Table Name - The logical table that contains the file data.
Source - (optional) An ID that identifies the source of the data.
Hash - (optional) A hash value that uniquely identifies the file by the contents of the file.
Instructions - (optional) An ID that identifies the set of instructions that map the JSON data to the table structure
</pre>

### File ingestion

When a file is ingested, the local node determines if the table exists in the local database.  
If the table does not exists, the node will determine if the table was declared by a different node and appears on the blockchain.  
If the table is available on the blockchain, the node will create an identical table on the local database.  
If the table is not available on the blockchain, the node will create the table and register the table on the blockchain.  
When the table is located or created, the file is ingested using one of 2 methods:  
1. The default mapping - attribute names are assigned to column names. If a column name is not part of the table's structure, the attribute value is ignored.  
2. If mapping ***Instructions*** appears in the file name, the instructions override, for the relevant columns, the default mapping of step 1.

### Creating a new table

If a table is created in an automated way, based on the first file ingested, the JSON attributes names are mapped to the 
columns names and the attribute values are evaluated to determine the data type.  
A table can be created by a user together with instructions that determines how the JSON data is mapped to the table's schema.  

### Duplicating an existing table to a new node

The copmmand: ```create table [table name] where dbms = [dbms name]``` creates a table assigned to the logical database with a schema identical to the schema published on the blockchain for the named table.

### Validating a schema

As a schema of a table can exist on the local database and on the blockchain, the command ```test table``` compares the table definitions on the local database with the schema definition on the blockchain.  
The structure of the command is as follows:  
```test table [table name] where dbms = [dbms name]```  
Example: ```test table ping_sensor where dbms = lsl_demo```
 
