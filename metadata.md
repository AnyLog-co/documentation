# Managing Metadata Changes

The metadata is organized in a local JSON file on each node that is a member of the network.
When a node joins, the node can download the existing metadata from a different member or from the blockchain.
A node may also store a copy of the metadata on a local database. However, for a node to operate, the node only needs the local JSON file.
On each node, the metadata represents the information which is relevant to the particular node and therefore the metadata on each node may be different.
When nodes make changes to the metadata, these changes become available to all nodes of the network by the processes explained below.
Each node may be configured such that it will continuously get updates of changes to the metadata. 

Members of the network can syncronize their metadata in 2 ways:

* Using a blockchain - By sending updateds to the blockchain and retrieving the metadata from the blockchain.
* Using a Master Node - Nodes can decide on one or more master nodes that receives the metadata updates, maintain a complete copy of the metadata
 and provides members with a copy of the metadata.

### Updating a blockchain
This functionality has not been yet released.

### Updating a master node:

When metadata is created, use the AnyLog command ```blockchain push``` to send the JSON file to the master node

#### To retrieve data from the master node:

* Use the command ```blockchain pull to log``` to pull the log file from the master node. The output file will be paced in the blockchain directory. The file name is prefixed by the name of the log file and the suffix is '.new'.
* Use the command ```blockchain pull to dbms``` to pull the metadata from the master node. The output file is a set of SQL insert statements that will update a local database with the metadata. The file name is prefixed by the name of the log file and the suffix is '.new.sql'.
* To update the local copy of the log file, use the ```file get``` command to copy the new log file to the be the blockchain log file.
* To update the local database with the updates to the metadata, place the insert statement file in the watch directory.
* To copy these files from the master node, use the command ```file get [source location] [destination location]``` whereas:
    * [source location] is the path name and file name on the master node.
    * [destination location] is the path name and file name on the requesting node. 
