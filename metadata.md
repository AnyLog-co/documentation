# Managing Metadata Changes

The metadata is organized in a local log file in a JSON format on each node that is a member of the network.
* The node operates against the local log file and does not require continues connection to a blockchain.
* The node may maintain a copy of the local JSON log file on a local database.
* The node may update a blockchain with changes to the metadata.
* The node may update a Master Node with changes to the metadata.  

***A Master Node*** is node that maintains a complete copy of the Metadata in a local database.

When a node joins the network, the node can download the existing metadata from a Master Node or from the blockchain.
A node may also store a copy of the metadata on a local database. However, for a node to operate, the node only needs the local log file.
On each node, the metadata represents the information which is relevant to the particular node and therefore the metadata on each node may be different.
When nodes make changes to the metadata, these changes become available to all nodes of the network by the processes explained below.
Each node may be configured such that it will continuously get updates of changes to the metadata. 

Members of the network can syncronize their metadata with other members of the network in 2 ways:

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
Example: ```blockchain_file = $HOME/AnyLog-demo/data/blockchain/blockchain.txt```

* Connect the node to the local database.    
```connect dbms psql anylog@127.0.0.1:demo 5432 blockchain```

* Create the local ***ledger*** table.  
```blockchain create table```


