# Using a Master Node

## Overview

A Master Node stores the metadata information in a local database and serves as a replacement to a blockchain.    
Any member node can serve as a master - a Master Node is a node that is considered by members of the network as a node that maintains an updated copy of the metadata.      
That means that member nodes are in agreement to reflect updates of the metadata with the Master Node and nodes will update their local copy of the metadata from the metadata maintained by the Master Node.

## Configuring a Master Node

The Master Node maintains the metadata using a local database - the metadata information is stored in a database called `_blockchain_` and a table called `_ledger_`.

To create the database using SQLite use the following command

```anylog
connect dbms sqlite !db_user !db_port blockchain 
```

To create the ledger table use the following command:

```anylog
create table ledger where dbms = blockchain
```

## Updating the metadata on a Master Node

Nodes in the network need to update the Master Node with changes to the blockchain.  
Updating the Master Node with changes to the metadata is by issuing the following command:
```anylog
run client (destination) blockchain push [JSON data]
```
`_destination_` - the IP and Port of the master node.
_JSON data_ - the policy to update.

Additional information on the blockchain commands is available at [blockchain commands](blockchain%20commands.md).

## Synchronizing a local copy of the blockchain

Nodes maintain a local copy of the blockchain in a JSON file. The file name and location is declared in the local dictionary using `_!blockchain_file_`.    
A node can enable a synchronization process. This process periodically pulls the blockchain data from the local database of the Master Node to the local blockchain file on the target node (the node that is executing the sync process).    
The synchronization process is detailed at [blockchain synchronizer](background%20processes.md#blockchain-synchronizer).  


