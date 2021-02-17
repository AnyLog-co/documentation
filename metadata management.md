# Managing Metadata

The metadata is organized on a global metadata platform. The platform can be one of the following:
* A blockchain platform
* A master node - A member node in the AnyLog network that maintains a complete copy of the Metadata in a local database.
  
Every node in the network is configured to periodically retrieve updates from the global platform and on each node, 
the metadata is organized in a local log file in a JSON format.

A node operates with the global metadata as follows:  
* The node operates against the local log file and does not require continues connection to the global metadata platform.
* The node may maintain a copy of the local JSON log file in a local database.
* The node is configured to periodically retrieve all updates from the global platform.  

When a node joins the network, the node downloads the existing metadata from a Master Node or from the blockchain.  
A node may also store a copy of the metadata on a local database. However, for a node to operate, the node only needs the local log file.
On each node, the metadata represents the information which is relevant to the particular node and therefore the metadata on each node may be different.
When nodes make changes to the metadata, these changes become available to all nodes of the network as each node synchronizes the local metadata with the global platform.

Members of the network synchronize their metadata with other members of the network in the following manner:

* Using a blockchain - By sending updates to the blockchain and retrieving the metadata from the blockchain.
* Using a Master Node - By sending updates to the Master Node and receiving updates from the Master Node.

## Policies

Policies are rules and logic that determine how nodes in the network operate. 
The policies are placed on the global metadata layer and become available to the nodes of the network with the blockchain/master-node synchronization process.  
Each node determines the policies to consider and these policies configure the mechanisms that manage the processes on the node.  
Using policies nodes declare their availability on the network, the list of tables supported, how data is being distributed, mapping roles, security policies and more.  
Policies are organized as JSON objects with a single root attribute name. The root attribute name is called the policy type.  
Below is an example of a policy declaring an Operator node:

<pre>
 {'operator' : {'hostname' : 'orics-test-node',
                'name' : 'orics-bkup-operator',
                'cluster' : 'fc86672d4fe687d4f82d0c407063800b',
                'company' : 'orics',
                'local ip' : '45.79.192.111',
                'ip' : '45.79.192.111',
                'port' : 2048,
                'rest port' : 2049,
                'db type' : 'psql',
                'loc' : '33.7490,-84.3880',
                'id' : 'e87c12fb3c9677be29d5b3c289a0ef5a',
                'date' : '2021-02-16T19:56:44.260273Z',
                'member' : 86}}]
</pre>

Some types of policies require particular attributes. For example, an Operator Policy requires the declaration of the IP and Port which the Operator uses to receive messages from peers.  
Within a policy, there is no limit on the attributes names and values which are not the root of the policy.    
The attributes ***id*** and ***date*** are added dynamically when the policy is updating the blockchain or the master node.    
If authentication is enabled, the attributes ***public_key*** and ***signatire*** are added dynamically.

## The blockchain commands

These are sets of command that allow to update and query the global metadata layer.   
The blockchain command are issued to a metadata repository which can be on the local node (either as a JSON file or hosted in a database), a master-node or a blockchain platform.  
 
The ***blockchain commands*** are detailed in the [blockchain commands section](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md).

### Updating a blockchain

The following command updates the blockchain platform with a new policy:

<pre>
blockchain commit to [blockchain name] [policy] 
</pre>

Example:

<pre>
blockchain commit to ethereum !test_policy
</pre>

### Retrieve metadata from a blockchain

The following command retrieves the metadata from the blockchain:

<pre>
blockchain checkout from [blockchain name]
</pre>

Example:

<pre>
blockchain checkout from ethereum
</pre>


### Updating a master node

The following command updates a master node with a new policy:

<pre>
blockchain push [policy] 
</pre>

If the update is done from a node which is not the master node, the update needs to be send as a message to the master node as in the example below:

<pre>
run client !master_node blockchain push !test_policy
</pre>

### Retrieve metadata from a master node

The following command retrieves the metadata from the blockchain:

<pre>
blockchain pull to [json | sql | stdout] [file name]
</pre>

Examples:  
To retrieve data from the master node:  
* Use the command ***blockchain pull*** to log to pull the log file from the master node. The output file will be paced in the blockchain directory with the following options:

| Option        | Explanation  |
| ------------- | ------------| 
| blockchain pull to dbms | The output file is a set of SQL insert statements to create the metadata on a local database |
| blockchain pull to json | The output file are the JSON policies |

* Use the command ***file get*** to copy a file from a node (like the master node) to a destination node.
<pre>
file get [source location] [destination location]
</pre>
[source location] is the path name and file name on the master node.
[destination location] is the path name and file name on the requesting node.

The following script pulls the metadata from a Master Node and copies the log file to the local node to serve as the metadata on the local node.
<pre>
run client [ip]:[port] "blockchain pull to log"    # create a copy of the log file on the Master Node
run client [ip]:[port] "file get [source path and file name] [destination path and file name] # copy the log file from the Master Node to the Local Node.
</pre>
In the above script:
[ip]:[port] - the ip and port of the Master Node.
[source path and file name] - the path and file name of the log file on the Master Node.
[destination path and file name] - the path and file name of the metadata log file on the Local Node.

## Using a local database

A node may keep a copy of the blockchain data on a local database. On the local database, the blockchain data is maintained in a table called ***ledger***.   

The following process creates the local blockchain database:

* Define a location for the blockchain log file by declaring ***blockchain_file*** constant 
with the path and file name of the log file.  
Example:
<pre>  
blockchain_file = $HOME/AnyLog-Network/data/blockchain/blockchain.txt```
</pre>

### Connect the node to the local database.    
Example using PostgreSQL to manage the blockchain data:
<pre>
connect dbms psql anylog@127.0.0.1:demo 5432 blockchain
</pre>

Example using SQLite to manage the blockchain data:   
<pre>
connect dbms sqlite anylog@127.0.0.1:demo 5432 blockchain
</pre>

### Create the local ***ledger*** table.
<pre>
blockchain create table
</pre>
The command will create the 'ledger' table in the database assigned to 'blockchain'.

## Creating tables

The structure of each table can be determined by users or generated dynamically, based on the attributes names and the values in the JSON file.  
When a file is ingested, and a schema is not available, and a user provided schema is not available, the  
tables is ctreated dynamically.    
Once a table schema is avaiable, the ingestion process maps the attribute names and values to the table's columns names and values.

### File names

The sensor data (or time series data) is placed in the ***watch directory***.  
Note: ***watch directories*** are explained at [Adding Data to Nodes in the Network](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#adding-data-to-nodes-in-the-network).
The file name follows a convention that determines how the file is being processed and if needed, allows to locate the file based on the properties of the data being ingested.  
The command ***get json file struct*** details the file structure convention and has the following output:  
<pre>
[dbms name].[table name].[data source].[hash value].[instructions].[TSD member ID].[TSD row ID].[TSD date].json
</pre>

The file type is ***json*** indicating the internal structure.  
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
| TSD date | The time and date when the file was injested to the local database. | No |

Note: Details on the TSD tables is available at [Managing Data files](https://github.com/AnyLog-co/documentation/blob/master/managing%20data%20files%20status.md#managing-data-files).

### File ingestion

When a file is ingested, the local node determines if the table exists in the local database.  
If the table does not exist, the node will determine if the table was declared by a different node and appears on the blockchain.  
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

