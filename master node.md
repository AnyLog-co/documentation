# Using a Master Node

## Overview

A Master Node captures the metadata information in a local database and serves as a replacement to a blockchain.    
Any member node can serve as a master - a Master Node is a node that is considered by members of the network as a node that maintains an updated copy of the metadata.      
That means that member nodes are in agreement to reflect updates of the metadata with the Master Node and nodes will update their local copy of the metadata from the metadata maintained by the Master Node.

## Configuring a Master Node

The Master Node maintains the metadata using a local database - the metadata information is stored in a database called ***blockchain*** and a table called ***ledger***.

To create the database using SQLite use the following command:

<pre>
connect dbms sqlite !db_user !db_port blockchain 
</pre>

To create the ledger table use the following command:

<pre>
create table ledger where dbms = blockchain
</pre>

## Updating the metadata on a Master Node

Nodes in the network need to update the Master Node with changes to the blockchain.  
Updating the Master Node with changes to the metadata is by issuing the following command:
<pre>
run client (destination) blockchain push [JSON data]
</pre>
***destination*** - the IP and Port of the master node.
***JSON data*** - the policy to update.

Additional information on the blockchain commands is available at [blockchain commands](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md).

## Synchronizing a local copy of the blockchain

Nodes maintain a local copy of the blockchain in a text file. The file name and location is declared in the local dictionary using ***!blockchain_file***.    
A node can enable a synchronization process. This process periodically pulls the blockchain data from the local database of the Master Node to the local blockchain file on the target node (the node that is executing the sync process).    
The synchronization process is detailed at [blockchain synchronizer](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#blockchain-synchronizer).  


