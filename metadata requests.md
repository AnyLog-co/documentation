# Metadata Requests

Metadata is maintained on a global platform (such as a blockchain or a master node) and locally on each node.  
This document details how to extract the global metadata and the local metadata on a particular node.  

## Retrieving the list of databases

### The local databases

A node may manage data locally. The command ***get databases*** lists the databases that are serving data on the local node.  
The listed databases are available to host data and query data and were assigned using the command ***connect dbms***.  

Example:

<pre>
List of DBMS connections
Logical DBMS         Database Type IP:Port                        Storage
-------------------- ------------- ------------------------------ -------------------------
almgm                psql          127.0.0.1:5432                 Persistent
blockchain           psql          127.0.0.1:5432                 Persistent
dmci                 sqlite        Local                          D:\Node\AnyLog-Network\data\dbms\dmci.dbms
lsl_demo             psql          127.0.0.1:5432                 Persistent
system_query         psql          127.0.0.1:5432                 Persistent
</pre>

### The network databases

The following command retrieves the list of databases on the network.
<pre>
get network databases
</pre>
Or if company name is included in the JSON policies:
<pre>
get network databases where company = my_company
</pre>

### The network tables
The following command retrieves the list of tables declared the network and determines which table is hosted on the current node.
<pre>
get tables where dbms = [dbms name]
</pre>

The following example retrieves all tables:
<pre>
get tables where dbms = *
</pre>

And an example output is the following:
<pre>
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
</pre>

###  Retrieving the columns list for a Tables

The following command retrieves the list of columns and the data types for a particular table:
<pre>
get columns where dbms = [dbms name] and table = [table name]
</pre>

The list represents the columns declared on the global metadata layer.

Example:
<pre>
get columns where dbms = dmci and table = machine_data
</pre>

To retrieve how the table is declared on  the local database on this node use the following command:

<pre>
info table [dbms name] [table name] columns
</pre>

Example:
<pre>
info table dmci machine_data columns
</pre>

### Validating a schema

As a schema of a table can exist on the local database and on the blockchain, the command ***test table*** compares the table definitions on the local database with the schema definition on the blockchain.  
The structure of the command is as follows:  
<pre>
test table [table name] where dbms = [dbms name]
</pre>

Example: 
<pre>
test table ping_sensor where dbms = lsl_demo
</pre> 



