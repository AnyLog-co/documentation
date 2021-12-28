
# Blockchain commands

## The metadata
AnyLog maintains the metadata in a ledger. The metadata is organized as a collection of objects, called policies.
A policy is a JSON structure with a single key at the root. The root key is called the Policy Type.

Example of policy types: database, table, operator, device.  
The following Policy describes an Operator (an Operator is a node that hosts data):
```
 {'operator' : {'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2a',
                'ip' : '24.23.250.144',
                'port' : 7848,
                'id' : 'f3a3c56fcfb78aecc110eb911f35851c',
                'date' : '2021-12-28T04:10:14.210574Z',
                'member' : 91,
                'ledger' : 'global'}}
```
Policies are written to the ledger and are available to all the members of the network.  
The ledger can be hosted on a blockchain platform (like Ethereum) or contained in a master node. 
Regardless of where the blockchain is hosted, every node maintains a local copy of the ledger such that when the node needs
metadata - it can be satisfied from the local copy with no dependency on network connectivity or the blockchain latency.
The local copy on a node is organized in a json file, The path to the file is stored by the ```blockchain_file``` variable.
Use the following command to see the value assigned to the variable: ```!blockchain_file```.
Optionaly, the local ledger can be hosted in a local database. If a master node is used, the master node is configured such 
that the ledger is stored on a local database.

When new policies are added to the ledger, they need to update the global metadata layer (the global copy). As every node continuously synchronizes 
the local copy with the global copy, evey update will appear on the local copy of every member node.  
Synchronization is enabled with the ***run blockchain sync*** command. Details are available [here](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#blockchain-synchronizer).  

## Adding policies

AnyLog offers a set of commands to add new policies to the ledger.
The generic command is ***blockchain insert***. This command is used to update both - the global copy and the local copy.  
If only the global copy is updated, it may take a few seconds for the update to be reflected on the local copy. The 
***blockchain insert*** command makes the new policy immediately available on the nodes that triggers the update.
Policies that are added using the ***blockchain insert*** command will also persist locally, such that if during the time of 
the update, the global ledger is not accessible, when the network reconnects, the new policies will be delivered to the global ledger.

Below are the list of commands to add new policies to the ledger:


| Command                              | Platform Updated | Details |
| ------------------------------------ | ------------ | ------------ | 
| [blockchain insert](#the-blockchain-insert-command) [policy and ledger platforms information] | all that are specified | Add a new policy to the ledger in one or more blockchain platform. |
| blockchain add [JSON data]           | Local Copy |Add a JSON object to the local JSON file. |
| blockchain push [JSON data]          | DBMS |Add a JSON object to the local database. |
| blockchain commit [JSON data]       | Blockchain Platform (i.e. Ethereum) |  – Add a JSON object to a blockchain platform. |  

## Query policies

AnyLog offers commands to query policies.  
Queries are processed on the local copy of the ledger and are not dependent on the availability or latency of the global ledger.  
Queries detail filter criteria to return the needed policies in JSON format and can be augmented by formatting instructions.   
ALternatively, the process can be split to a process that retrieves the needed policies and use a second command to apply the formatting instructions on the derived policies.  
For example, a search may request for all the operators supporting a table and then issue a second search against the retrieved operators for their IP and Port information.  
The second search is using the command ***from*** and is explained [below](#the-from-json-object-bring-command).

Usage:
<pre>
blockchain get [policy type] [where] [attribute name value pairs] [bring] [bring command variables]
</pre>

Explanation:
The ***blockchain get*** command retrieves one the policies that satisfy the search criteria from the local copy of the ledger.  
* policy type - the key at the root of the JSON representing the policy.
* attribute name value pairs - a list that describes key and value pairs that filter the search.
* bring command variables = determined the formatting of the retrieved data.  

Details: 
<pre>
blockchain get [policy type] - Retrieve a list of all the requested policies of the specified type.
blockchain get [object] where [key] = [value] - Retrieve a list of all the requested objects that contain the specidied value.
blockchain get [object] where [key] with [value] - Retrieve a list of all the requested objects that contain a list of values including the specidied value.
</pre>

Examples:
<pre>
blockchain get *
blockchain get operator where dbms = lsl_demo
blockchain get cluster where table[dbms] = purpleair and table[name] = cos_data bring [cluster][id] separator = ,
</pre>


## The Objects IDs

When a JSON object is added to the metadata, one of the fields describing the object is an ID field.  
The ID value can be provided by the user or generated dynamically when the object is added to the blockchain data.  
If the value is auto-generated, it is based on the MD5 Hash value of the object. 

## The Storage of the Metadata
The metadata is stored in 3 places:  
a.	In a JSON file on each node – the JSON file on each node needs to maintain only the metadata that is needed for the operation of the node.   
b.	In a local database in the node – the local database only needs to maintain the metadata that is needed for the operation of the node. The existence of the local database is optional.  
c.	In a blockchain – the blockchain maintains the complete set of metadata information.  

### A Master Node
A master node is a node that maintains a complete copy of the metadata in a local database.  
Maintaining a master node in the network is optional.

## The blockchain commands:

| ===========Command============ | ===============Details=============== |
| ------------------------------------ | ------------| 
| blockchain connect to [platform name] where [connection parameters] | Connect to a blockchain platform. | 
| blockchain get [JSON search]         | Retrieve from the JSON file all objects that satisfy the search criteria.   |
| blockchain pull to sql [optional output file]  | Retrieve the blockchain data from the local database to a SQL file that organizes the metadata as insert statements. |
| blockchain pull to json [optional output file]| Retrieve the blockchain data from the local database to a JSON file that can be used as the local JSON file. |
| blockchain pull to stdout| Retrieve the blockchain data from the local database to stdout. |
| blockchain update file [path and file name]| Copy the file to replace the current local blockchain file. Prior to the copy, the current blockchain file is copied to a file with extension ***'.old'***. If file name is not specified, a ***blockchain.new*** is used as the file to copy. |    
| blockchain update dbms [path and file name] [ignore message]| Add the policies in the named file (or in the blockchain file, if a named file is not provided) to the local dbms that maintains the blockchain data. The command outputs a summary on the number of new policies added to the database. To avoid the message printout and messages of duplicate policies to the error log, add ***ignore message*** as a command prefix. |  
| blockchain checkout| Retrieve the blockchain data from the blockchain platform to a JSON file. |  
| blockchain create table| Create a local table (called ***ledger***) on the local database that maintains metadata information. |  
| blockchain drop table|  Drop the local table (***ledger***) on the local database that maintains metadata information. |  
| blockchain drop policy [JSON data]| Remove the policy specified by the JSON data from the local database that maintains metadata information. |
| blockchain drop by host [ip]| Remove all policies that were added from the provided IP. |        
| blockchain replace policy [policy id] with [new policy]| Replace an existing policy in the local blockchain database. |        
| blockchain delete local file| Delete the local JSON file with the blockchain data. |  
| blockchain test| Test the structure of the local JSON file. Returns True if the file structure is valid. Otherwise, returns False. | 
| blockchain get id [json data]| Return the hash value of the JSON data. |  
| blockchain test id| Return True if the id exists in the local blockchain file. Otherwise returns False. |
| blockchain load metadata [conditions]| Update the local metadata from policies published on the blockchain. |  
| blockchain query metadata [conditions]| Provide a diagram representation of the local metadata. | 
| blockchain test cluster [conditions] | Provid an analysis of the \'cluster\' policies. |  
| blockchain prepare policy [JSON data] | Adds an ID and a date attributes to an existing policy. |  
| blockchain wait where [condition] | Pause current process until the local copy of the blockchain is updated with the policy (with a time threshold limit which is based on the sync time of the synchronizer). |

### The blockchain insert command
The ***blockchain insert*** command adds a policy to the blockchain ledger.  

Usage:
<pre>
blockchain insert where policy = [policy] and blockchain = [platform] and local = [true/false] and master = [IP:Port]
</pre>

Command details:

| Key             | Value |
| --------------- | ------------| 
| policy          | A json policy that is added to the ledger  |
| platform        | A connected blockchain platform (i.e. Ethereum, and see Ethereum connection info in [this doc](https://github.com/AnyLog-co/documentation/blob/master/using%20ethereum.md#using-ethereum-as-a-global-metadata-platform)). |
| local           | A true/false value to determine an update to the local copy of the ledger  |
| master          | The IP and Port value of a master node (configuring a master node is detailed in [this doc](https://github.com/AnyLog-co/documentation/blob/master/master%20node.md#using-a-master-node).) |

Using the ***blockchain insert*** command, all the specified ledgers are updated. The common configuration would include the local ledger and 
either a blockchain platform (like Ethereum) or a master node.  

The ***blockchain insert*** command requires a ***policy*** information and one or more ledgers to update. In most cases, the insert would
include the local update and either a platform (like Ethereum) or a master.

When the policy is updated on the local ledger, the policy is updated with the key: "ledger" and a value "local" to indicate that 
the policy is not yet confirmed on the global ledger (the blockchain platform or a master node).   
When the local ledger is synchronized with the global ledger, the status of the key "ledger" is changed from "local" to "global".

Examples:
<pre>
blockchain insert where policy = !policy and local = true and master = !master_node
blockchain insert where policy = !policy and local = true and blockchain = ethereum
</pre>


### Updating a Master Node
Updating the Master Node is Done by a blockchain push request that is send to the Master Node (using ***run client*** command).  

### Retrieving the Metadata from a Master Node
Retrieving the metadata from a Master Node is done by a blockchain pull request that is send to the Master Node (using “run client” command) and copying the data to the desired location on the client node (using ***file get*** command).  

### Removing policies from a master node
Deleting a policy from a master node is with the command:
<pre>
blockchain drop policy [JSON data]
</pre>
JSON data is the policy to drop.
If JSON data is a list of multiple policies, a where condition is required. For example:  
<pre>
blockchain drop policy !operator where ip = 10.0.0.25
</pre>

### Reflecting blockchain updates on a the local copy of the metadata
When a process on a node updates a policy on a remote blockchain platform (or on a master node), the process can wait for 
the update to be reflected on the local copy using the ***blockchain wait for ...*** command:
<pre>
blockchain prepare policy !policy     # Add an ID and a date to the policy being updated
run client (!master_node) blockchain push !policy   # Make the update
is_updated = blockchain wait for !policy  # Force sync and validate that the update is available
</pre>
The wait command forces synchronization with the blockchain platform and validates that the update is reflected on the local file.

### Interacting with the blockchain data
For a node to be active, it needs to maintain a local copy of the blockchain data in a local JSON file.
The local copy becomes available by assigning the path and file name to the global variable ***blockchain_file***.
A user can validate the availability and the structure of the blockchain using the command: ```blockchain test```.

### Queries over the Metadata
Metadata queries evaluate the data in the local JSON file.  
Queries are done in 2 steps:
* Using the command ```blockchain get``` - retrieving the JSON objects that satisfy the search criteria.
* Using the command ```bring``` - pulling and formatting the values from the retrieved JSON objects.
 
### Retrieve blockchain data from the local database

Retrieve blockchain data from the local database on the AnyLog command line can be done using SQL.  
Example: ```sql blockchain text "select * from ledger"```

#### bring options
The blockchain ***get*** command can be extended to retrieve predefined sections from the metadata. This option is detailed below.

## The 'From JSON Object Bring' command

The Bring command retrieves and formats data from a JSON object as follows:
<pre>
from [JSON object] bring [list of keys and formatting instructions]
</pre>

The bring is followed by a list of keys that are applied on the JSON object. 
The keys are structured such that a Python call with each key on the JSON data returns a value, which if available, is returned to the caller.    
Each key can be prefixed or suffixed with strings that are added to the returned values. 
   
* The formatting instruction may use the keyword ***separator*** to provide a suffix to the output string returned from each object.  
Special separators:

| separators  | Explanation |
| ---- | ------------|
| separator = \n | A new line character is added at the end of the data returned from each JSON object  |
| separator = \t | A tab is added at the end of the data returned from each JSON object  |
  

* The ***bring*** command can be added to a blockchain ***get*** command such that ***get*** retrieves metadata in a JSON format and the keyword ***bring*** operates on the retrieved JSON data.  

* The keyword bring can be suffixed with the following keywords:     
    * ```bring.unique``` - returns unique values.  
    * ```bring.first``` - returns the value from the JSON object with the earliest date. If a date is missing from the objects, the first object in the ledger file is returned.
    * ```bring.recent``` - returns the value from the JSON object with the latest date. If a date is missing from the objects, the last object in the ledger file is returned.  
    * ```bring.json``` - returns the requested keys and values in a JSON format. Additional formatting instructions are ignored.
    
## Data Distribution Policies
The policies that determine how data is distributed among nodes of the network are managed by a set of commands that are detailed below.  
```blockchain load metadata [conditions]``` - when the blockchain is updated, ***load*** forces an update of the metadata tier by evaluating the relevant policies published on the blockchain.  
```blockchain query metadata [conditions]``` - provides a visual diagram representation of data is distributed to the nodes in the network.  
```blockchain test cluster [conditions]``` - provides analysis of the \'cluster\' policies. These are the policies that determine how data is distributed.  
****conditions*** - a set of conditions that limit the number of policies participate in the process.  
For example, a node can specify the company nad or database and or table of interest.  
More information is available at [Data Distribution and Configuration](https://github.com/AnyLog-co/documentation/blob/master/data%20distribution%20and%20configuration.md#data-distribution-and-configuration).  

### Examples

The following examples retrieve all the operators with SLA at level 5 that are located in California:  

a) Using an assignment of the JSON objects to ***selected_operators*** and pulling the IP and Port from each JSON object:
 
<pre>
selected_operators = blockchain get "operator" {"SLA" : "5", “location”:”CA”} # get operators with SLA == 5 and location is CA
ip_port = from !selected_operators bring ['operator']['ip'] ":" ['operator']['port'] separator = " " # get the IPs and ports of these operators
</pre>

b) Using a single call:
 
<pre>
blockchain get operator {"SLA" : "5", “location”:”CA”} bring ['operator']['ip'] ":" ['operator']['port'] separator = " " 
</pre>

c) Using a ***where*** condition replacing the JSON structure in the search of the JSON objects:
 
<pre>
blockchain get operator where SLA = 5 and location = CA bring ['operator']['ip'] ":" ['operator']['port'] separator = " " 
</pre>

The following example retrieves all the databases which are in the JSON objects describing the tables:  

<pre>
blockchain get table bring ['table']['dbms'] separator = " " 
</pre>

The following example retrieves unique databases which are in the JSON objects describing the tables:  

<pre>
blockchain get table bring.unique ['table']['dbms'] separator = " " 
</pre>

The following example retrieves the most recent declaration of an operator supporting a database called lsl_demo:  

<pre>
blockchain get operator where dbms = lsl_demo bring.recent 
</pre>

The following example returns the list of IPs and Ports of the Operators as a list of JSON objects.

<pre>
blockchain get operator bring.json ['operator']['ip'] [operator']['port']
</pre>

