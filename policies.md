# Policies based Metadata

AnyLog maintains the metadata in a ledger. The metadata is organized as a collection of objects, called policies. A 
policy is a JSON structure with a single key at the root. The root key is called the Policy Type.

Example of policy types: database, table, operator, device. The following Policy describes an Operator (an Operator is a 
node that hosts data):

```json
{"operator": {
    "cluster": "7a00b26006a6ab7b8af4c400a5c47f2a",
    "ip": "24.23.250.144",
    "local_ip": "10.0.0.78",
    "port": 32148,
    "rest_port": 32149,
    "loc": "37.77986, -122.42905",
    "country": "USA",
    "city": "San Francisco",
    "id": "f3a3c56fcfb78aecc110eb911f35851c",
    "date": "2021-12-28T04:10:14.210574Z",
    "member": 91,
    "ledger": "global"
  }
}
```


Policies are written to the ledger and are available to all the members of the network. The ledger can be hosted on a 
blockchain platform (like Ethereum) or contained in a master node. Regardless of where the blockchain is hosted, every 
node maintains a local copy of the ledger such that when the node needs metadata - it can be satisfied from the local 
copy with no dependency on network connectivity or the blockchain latency. The local copy on a node is organized in a 
json file, The path to the file is represented by the `blockchain_file` variable. Use the following command to see the value 
assigned to the variable: `!blockchain_file`. Optionally, the local ledger can be hosted in a local database. If a 
master node is used, the master node is configured such that the ledger is stored on a local database.

When new policies are added to the ledger, they need to update the global metadata layer (the global copy).
As every node continuously synchronizes the local copy with the global copy, evey update will appear on the local copy 
of every member node. Synchronization is enabled with the `run blockchain sync` command. 
Details are available [here](background%20processes.md#blockchain-synchronizer).  

## The Policy ID
When a Policy is added to the metadata, one of the fields describing the object is an ID field.  
The ID value can be provided by the user or generated dynamically when the policy is added to the ledger.  
Users can specify a unique ID to their policies or, if the value is auto-generated, it is based on the MD5 Hash value of the object.


