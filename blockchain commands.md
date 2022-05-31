
# Blockchain commands

## The metadata
AnyLog maintains the metadata in a ledger. The metadata is organized as a collection of objects, called policies.
A policy is a JSON structure with a single key at the root. The root key is called the Policy Type.

Example of policy types: database, table, operator, device.  
The following Policy describes an Operator (an Operator is a node that hosts data):
```
 {'operator' : {'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2a',
                'country' : 'USA',
                'city' : 'San Francisco',
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

## The Policy ID
When a Policy is added to the metadata, one of the fields describing the object is an ID field.  
The ID value can be provided by the user or generated dynamically when the policy is added to the ledger.  
If the value is auto-generated, it is based on the MD5 Hash value of the object. 

### Interacting with the blockchain data
For a node to be active, it needs to maintain a local copy of the ledger in a local JSON file.
The local copy becomes available by assigning the path and file name to the global variable ***blockchain_file***.
A user can validate the availability and the structure of the blockchain using the command: ```blockchain test```.

## A Master Node
A master node is a node that maintains a complete copy of the metadata in a local database.  
Maintaining a master node in the network is optional.

## The Storage of the Metadata
The metadata is stored ias follows:  
a.	In a JSON file on each node – the JSON file on each node needs to maintain only the metadata that is needed for the operation of the node.
b.	In a local database in the node – the local database only needs to maintain the metadata that is needed for the operation of the node. 
The existence of the local database is optional.  
c.	In a ledger of blockchain platform – the ledger maintains the complete set of metadata information.  

If the network is configured with a master node, the master node maintains the complete set of metadata information in a local database.

Note: a node operates in the same manner regardless if the global ledger is maintained in a blockchain platform or a master node.  
The difference is only in the configuration that determine the location of the the global ledger.

## Maintaining the global copy on a blockchain platform

Using a blockchain platform requires the following :
1. Connecting to the blockchain platform. 
   The following command connects to the blockchain platform:
   <pre>
   blockchain connect to [platform name] where [connection parameters]
   </pre>
   Details are available [here](https://github.com/AnyLog-co/documentation/blob/master/using%20ethereum.md#connecting-to-ethereum).  
2. Updating the blockchain platform with new policies using the commands [blockchain insert](#the-blockchain-insert-command) or ***blockchain push***.    
3. [Configuring synchronization](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20configuration.md) against the blockchain platform.  

## Adding policies

AnyLog offers a set of commands to add new policies to the ledger.
The generic command is ***blockchain insert***. This command is used to update both - the global copy and the local copy.  
If only the global copy is updated, it may take a few seconds for the update to be reflected on the local copy. The 
***blockchain insert*** command makes the new policy immediately available on the node that triggered the update.  
Policies that are added using the ***blockchain insert*** command will also persist locally (if the command directs to update the local copy), such that if during the time of 
the update, the global ledger is not accessible, when the network reconnects, the new policies will be delivered to the global ledger.

Below are the list of commands to add new policies to the ledger:

| Command                              | Platform Updated | Details |
| ------------------------------------ | ------------ | ------------ | 
| [blockchain insert](#the-blockchain-insert-command) [policy and ledger platforms information] | All that are specified | Add a new policy to the ledger in one or more blockchain platform. |
| blockchain add [policy]           | Local Copy |Add a Policy to the local ledger file. |
| blockchain push [policy]          | DBMS |Add a Policy to the local database. |
| blockchain commit [policy]       | Blockchain Platform (i.e. Ethereum) |  – Add a Policy to a blockchain platform. |  

When policies are added, nodes validate the structure of the policies and their content. In addition, when policies are added, the policies are
updated with a date and time of the update and a [unique ID](#the-policy-id).

## Query policies

AnyLog offers commands to query policies.  
Queries are processed on the local copy of the ledger and are not dependent on the availability or latency of the global ledger.  
Queries detail filter criteria to return the needed policies in JSON format and can be augmented by formatting instructions.   
Alternatively, the process can be split to a process that retrieves the needed policies and use a second command to apply the formatting instructions on the derived policies.  
For example, a search may request for all the operators supporting a table and then issue a second search against the retrieved operators for their IP and Port information.  
The second search is using the command ***from*** and is explained at the
section called: [The 'From JSON Object Bring' command](json%20data%20transformation.md#the-from-json-object-bring-command).

Queries are done in 2 steps:
* Using the command ```blockchain get``` - retrieving the JSON objects that satisfy the search criteria.
* Using the command ```bring``` - pulling and formatting the values from the retrieved JSON objects.
 
Usage:
<pre>
blockchain get [policy type] [where] [where conditions] [bring] [bring command instructions]
</pre>

Explanation:
The ***blockchain get*** command retrieves one the policies that satisfy the search criteria from the local copy of the ledger.  
* ***policy type*** - the key at the root of the JSON representing the policy.
* ***where conditions*** - reference the policy values that are evaluated to determine if the policy is selected.
* ***bring command*** - determined the retrieved data and formatting options.  

### Selecting the policy type

AnyLog policies have a single attribute at the root of the policy. The root attribute name is the policy type.  
For example, in the [Metadata Section](#the-metadata), the policy type is ***operator***.  
The following command selects all policies of a particular type:
<pre>
blockchain get [policy type]
</pre>
The following example selects all policies of a type ***operator***:
<pre>
blockchain get operator
</pre>

Selecting multiple types is allowed by separating policies using a comma and placing the policies types in parentheses.    
The following example selects all policies of a type ***operator*** and type ***publisher***:
<pre>
blockchain get (operator, publisher)
</pre>
Selecting all policies is allowed as in the following example:
<pre>
blockchain get *
</pre>

### The where condition

The where condition is provided in one of 2 ways:  
* As a list of attribute name value pairs, expressed as ***name = value*** (or ***name with value*** to validate a value in a list) separated by the ***and*** keyword.   
The list of attribute name (key) value pairs in the where conditions is provided as follows:
    <pre>
    key1 = value1 and key2 = value2 and key3 = value3 and ... keyN = valueN
    </pre>
    A key represents the path in the policy to the tested value, for example ***[operator][name]*** is the path to the name value in the operator policy.  
    Note that the root name in the path does not have to be enclosed with square brackets: ***[operator][name]*** is equivalent to ***operator[name]***.

* As a ***conditional execution*** whereas policy values are evaluated to determine if these values satisfy the search criteria.  
 Attribute name value pairs are referenced using squere brackets, for example ***[operator][name]*** will pull the name from the Operator policy.  
 The following example evaluates attribute values of the policy example in the [Metadata Section](#the-metadata):
     <pre>
    [operator][country] == USA and ([operator][country] == "San Francisco" or [operator][country] == "San Jose")
    </pre>
 Conditional execution is detailed [here](anylog%20commands.md#conditional-execution). 

Examples:
<pre>
blockchain get operator where dbms = lsl_demo
blockchain get operator where dbms = lsl_demo and ip = 24.23.250.144
blockchain get cluster where table[dbms] = purpleair and table[name] = cos_data bring [cluster][id] separator = ,
blockchain get operator where [name] == operator11 or [name] ==  operator1 bring [*][name]
</pre>

### Formatting retrieved data 

The ***bring*** command can be added to a blockchain ***get*** command such that ***get*** retrieves metadata in a JSON format and the keyword ***bring*** operates on the retrieved JSON data.  
See details and examples in the [JSON data transformation](https://github.com/AnyLog-co/documentation/blob/master/json%20data%20transformation.md#json-data-transformation) section.

### Setting command destination from policies

A common usage of policies is to determine the destination of a command or a query (in case of a query, to overwrite the network protocol's destination).    
The process evaluates policies by some criteria and sets a command destination to the IPs and ports detailed in the policies that satisfies the criteria.   
The structure of the command is as follows:
<pre>
run client (blockchain get ...) anylog command
</pre>
The ***blockchain get*** includes a ***bring*** directive to construct the command destination as a list of comma separated IPs and Ports.
 
The following example sends a network status command to all Operator and Query nodes in San Francisco or San Jose. 
Note that in the example below, rather than placing the ***blockchain get*** command in the destination parenthesis of the ***run client ()*** command,
it is places in a dictionary variable which is referenced in the parenthesis to determine the destination. However, both methods are supported.
<pre>
destinations = blockchain get (operator, query) where [operator][country] == USA and ([operator][country] == "San Francisco" or [operator][country] == "San Jose") bring [*][ip] : [*][port] separator = ,
run client (!destinations) get node info net_io_counters 
</pre>

    
## The blockchain insert command
The ***blockchain insert*** command adds a policy to the blockchain ledger. 
This command can update both - the local copy and the global copy of the ledger. In addition, it facilitates a process that validates that all the updates
are represented on the global copy (as during the issue of the insert command, the global copy may not be accessible).  

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

When the policy is updated on the local ledger, the policy is updated with the key: "ledger" and a value "local" to indicate that 
the policy is not yet confirmed on the global ledger (the blockchain platform or a master node).   
When the local ledger is synchronized with the global ledger, the status of the key "ledger" is changed from "local" to "global".

Examples:
<pre>
blockchain insert where policy = !policy and local = true and master = !master_node
blockchain insert where policy = !policy and local = true and blockchain = ethereum
</pre>


## Copying policies representing the metadata to the local ledger
The local representation of the blockchain file is updated continuously if the [blockchain synchronization](./background%20processes.md#blockchain-synchronizer) 
process is enabled.  
If the blockchain sync process is disabled, and the local blockchain file is updated or copied from a different node, the command ***blockchain load metadata*** 
will force the node to use the updated local file.  
For example, ***blockchain sync*** is not enabled, and a local file is copied from a member node as follows:
<pre>
run client 10.0.0.25:2548 file get !!blockchain_file !blockchain_file
</pre>
The following command will force the node to replace the metadata representation with the local file:
<pre>
blockchain load metadata
</pre>


## Using a local database to host the ledger

A Master Node maintains the ledger in a local database. In addition, any node can keep the local copy of the ledger in a local database.
The following are commands that interact with a database that hosts the ledger:

 ===========Command============ | ===============Details=============== |
| ------------------------------------ | ------------| 
| blockchain pull to sql [optional output file]  | Retrieve the blockchain data from the local database to a SQL file that organizes the metadata as insert statements. |
| blockchain pull to json [optional output file]| Retrieve the blockchain data from the local database to a JSON file that can be used as the local JSON file. |
| blockchain pull to stdout| Retrieve the blockchain data from the local database to stdout. |
| blockchain update dbms [path and file name] [ignore message]| Add the policies in the named file (or in the blockchain file, if a named file is not provided) to the local dbms that maintains the blockchain data. The command outputs a summary on the number of new policies added to the database. To avoid the message printout and messages of duplicate policies to the error log, add ***ignore message*** as a command prefix. |  
| blockchain create table| Create a local table (called ***ledger***) on the local database that maintains metadata information. |  
| blockchain drop table|  Drop the local table (***ledger***) on the local database that maintains metadata information. |  
| blockchain drop policy [JSON data]| Remove the policy specified by the JSON data from the local database that maintains metadata information. |
| blockchain drop by host [ip]| Remove all policies that were added from the provided IP. |        
| blockchain replace policy [policy id] with [new policy]| Replace an existing policy in the local blockchain database. |     

### Retrieve blockchain data from the local database

Retrieve blockchain data from the local database on the AnyLog command line can be done using SQL.  
Example: ```sql blockchain text "select * from ledger"```

### Retrieving the Metadata from a Master Node
Retrieving the metadata from a Master Node is done by a blockchain pull request that is send to the Master Node (using “run client” command) 
and copying the data to the desired location on the client node (using ***file get*** command).  
Example:
<pre>
mater_node = 127.45.35.12:2048
run client (!master_node) blockchain pull to json
run client (!master_node) file get !!blockchain_file !blockchain_file
</pre>
Notes:
* ```blockchain_file``` is configured to the path and file name of the ledger.
* The double exclamation points (!!) determine to derive the value of the key ```blockchain_file``` on the target node (127.45.35.12).
* Details on the ***file get*** command are available [here](https://github.com/AnyLog-co/documentation/blob/master/file%20commands.md#file-copy-from-a-remote-node-to-a-local-node).
* With synchronization enabled, this process is done continuously as configured and is not required to be triggered by the user. 

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

### Reflecting blockchain updates on the local copy of the metadata

When a process on a node updates a policy on a remote blockchain platform (or on a master node), the process can wait for 
the update to be reflected on the local copy using the ***blockchain wait for ...*** command:
<pre>
blockchain prepare policy !policy     # Add an ID and a date to the policy being updated
run client (!master_node) blockchain push !policy   # Make the update
is_updated = blockchain wait for !policy  # Force sync and validate that the update is available
</pre>
The wait command forces synchronization with the blockchain platform and validates that the update is reflected on the local file.

Note: This process is redundant if the update of the new policies was done using the [blockchain insert](#the-blockchain-insert-command) command.

## Other blockchain commands:

| ===========Command============ | ===============Details=============== |
| ------------------------------------ | ------------| 
| blockchain update file [path and file name]| Copy the file to replace the current local blockchain file. Prior to the copy, the current blockchain file is copied to a file with extension ***'.old'***. If file name is not specified, a ***blockchain.new*** is used as the file to copy. |    
| blockchain checkout| Retrieve the blockchain data from the blockchain platform to a JSON file. |  
| blockchain delete local file| Delete the local JSON file with the blockchain data. |  
| blockchain test| Test the structure of the local JSON file. Returns True if the file structure is valid. Otherwise, returns False. | 
| blockchain get id [json data]| Return the hash value of the JSON data. |  
| blockchain test id| Return True if the id exists in the local blockchain file. Otherwise returns False. |
| blockchain query metadata [conditions]| Provide a diagram representation of the local metadata. | 
| blockchain test cluster [conditions] | Provid an analysis of the \'cluster\' policies. |  
| blockchain prepare policy [JSON data] | Adds an ID and a date attributes to an existing policy. |  
| blockchain wait where [condition] | Pause current process until the local copy of the blockchain is updated with the policy (with a time threshold limit which is based on the sync time of the synchronizer). |


