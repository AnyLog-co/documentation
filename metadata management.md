# Managing Metadata

## Overview

A node in the network interacts with 2 layers of metadata:
* With a local metadata layer. The local metadata layer includes the local databases, tables and views 
  that are used by the node to organize the data locally such that the data is unified with data on peer nodes and is 
  accessible to permitted members of the network.  
* With a global metadata layer shared by all the members of the network.

This document provides an overview on the global metadata layer.  
The document [metadata requests](metadata%20requests.md#metadata-requests) 
provides an overview of the local metadata layer.

## The global metadata

The metadata is organized on a global metadata platform. The platform can be one of the following:
* A blockchain platform
* A master node - A member node in the AnyLog network that maintains a complete copy of the Metadata in a local database.
  
Every node in the network is configured to periodically retrieve updates from the global platform and on each node, 
the metadata is organized in a local log file in a JSON format.

A node operates with the global metadata as follows:  
* The node operates against the local log file and does not require continuous connection to the global metadata platform.
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

```json
{"operator":  {
    "hostname": "orics-test-node",
    "name": "orics-bkup-operator",
    "cluster": "fc86672d4fe687d4f82d0c407063800b",
    "company": "orics",
    "local ip": "45.79.192.111",
    "ip": "45.79.192.111",
    "port":  2048,
    "rest port":  2049,
    "db type": "psql",
    "loc": "33.7490,-84.3880",
    "id": "e87c12fb3c9677be29d5b3c289a0ef5a",
    "date": "2021-02-16T19:56:44.260273Z",
    "member":  86
}}
```

Some types of policies require particular attributes. For example, an Operator Policy requires the declaration of the IP and Port which the Operator uses to receive messages from peers.  
Within a policy, there is no limit on the attributes names and values which are not the root of the policy.    
The attributes _id_ and _date_ are added dynamically when the policy is updating the blockchain or the master node.    
If authentication is enabled, the attributes _public_key_ and _signature_ are added dynamically.

## The blockchain commands

These are sets of command that allow to update and query the metadata layer.   
The blockchain command are issued to a metadata repository which can be on the local node (either as a JSON file or hosted in a database), a master-node or a blockchain platform.  
 
The _blockchain commands_ are detailed in the [blockchain commands section](blockchain%20commands.md).

### Updating a blockchain

The following command updates the blockchain platform with a new policy:

```anylog
blockchain commit to [blockchain name] [policy] 
```

Example:

```anylog
blockchain commit to ethereum !test_policy
```

### Retrieve metadata from a blockchain

The following command retrieves the metadata from the blockchain:

```anylog
blockchain checkout from [blockchain name]
```

Example:

```anylog
blockchain checkout from ethereum
```


### Updating a master node

The following command updates a master node with a new policy:

```anylog
blockchain push [policy] 
```

If the update is done from a node which is not the master node, the update needs to be sent as a message to the master node as in the example below:

```anylog
run client !master_node blockchain push !test_policy
```

### Retrieve metadata from a master node

The following command retrieves the metadata from the blockchain:

```anylog
blockchain pull to [json | sql | stdout] [file name]
```

Examples:  
To retrieve data from the master node:  
* Use the command `blockchain pull` to pull the log file from the master node. The output file will be paced in the blockchain directory with the following options:

| Option        | Explanation  |
| ------------- | ------------| 
| blockchain pull to dbms | The output file is a set of SQL insert statements to create the metadata on a local database |
| blockchain pull to json | The output file are the JSON policies |
| blockchain pull to stdout | The output is policies displayed on the stdout |


* Use the command `file get` to copy the output file (of the pull command) from a node (like the master node) to a destination node.
```anylog
file get [source location] [destination location]
```
[source location] - is the path name and file name on the master node.  
[destination location] - is the path name and file name on the requesting node.

The following script pulls the metadata from a Master Node and copies the log file to the local node to serve as the metadata on the local node.
```anylog
run client [ip]:[port] "blockchain pull to log"    # create a copy of the log file on the Master Node
run client [ip]:[port] "file get [source path and file name] [destination path and file name] # copy the log file from the Master Node to the Local Node.
```
In the above script:
`[ip]:[port]` - the ip and port of the Master Node.
`[source path and file name]` - the path and file name of the log file on the Master Node.
`[destination path and file name]` - the path and file name of the metadata log file on the Local Node.

## Periodically synchronizing the local copy of the metadata with a blockchain or a master node

Details are available at the section [Blockchain Synchronizer](background%20processes.md#blockchain-synchronizer).

## Using a local database

A node may keep a copy of the blockchain data on a local database. On the local database, the blockchain data is maintained in a table called `ledger`.   

The following process creates the local blockchain database:

1. Define a location for the blockchain log file by declaring _blockchain_file_ constant with the path and file name of the log file.  
  Example:
```anylog  
blockchain_file = $HOME/AnyLog-Network/data/blockchain/blockchain.txt
```

2. Connect the node to the local database.    
  * Example using PostgresSQL to manage the blockchain data:
```anylog
connect dbms blockchain where type = psql and user = anylog and ip = 127.0.0.1 and password = demo and port = 5432
```
  * Example using SQLite to manage the blockchain data:   
```anylog
connect dbms blockchain where type = sqlite
```

3. Create the local `ledger` table.
```anylog
create table ledger where dbms=blockchain
```
  The command will create the 'ledger' table in the database assigned to 'blockchain'.

