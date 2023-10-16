# Blockchain commands

## The metadata
AnyLog maintains the metadata in a ledger. The metadata is organized as a collection of objects, called policies. A 
policy is a JSON structure with a single key at the root. The root key is called the Policy Type.

An overview of the structure of the policies is available in the [Policies based Metadata](policies.md#policies-based-metadata) section.

### Interacting with the blockchain data
For a node to be active, it needs to maintain a local copy of the ledger in a local JSON file.
The local copy becomes available by assigning the path and file name to the global variable _blockchain_file_.
A user can validate the availability and the structure of the blockchain using the command: ```blockchain test```.

## A Master Node
A master node is a node that maintains a complete copy of the metadata in a local database.  
Maintaining a master node in the network is needed only if a blockchain platform is not used.

## The Storage of the Metadata
The metadata is stored ias follows:

a. In a JSON file on each node – the JSON file on each node needs to maintain only the metadata that is needed for  the 
operation of the node.

b. In a local database in the node – the local database only needs to maintain the metadata that is needed for the 
operation of the node. The existence of the local database is optional.

c. In a ledger of blockchain platform – the ledger maintains the complete set of metadata information.  

If the network is configured with a master node, the master node maintains the complete set of metadata information in a local database.

Note: a node operates in the same manner regardless if the global ledger is maintained in a blockchain platform or a master node.  
The difference is only in the configuration that determine the location of the global ledger.

## Maintaining the global copy on a blockchain platform

Using a blockchain platform requires the following :
1. Connecting to the blockchain platform. The following command connects to the blockchain platform, Details are available [here](using%20ethereum.md#connecting-to-ethereum). 
```anylog
blockchain connect to [platform name] where [connection parameters]
```
     
2. Updating the blockchain platform with new policies using the commands [blockchain insert](#the-blockchain-insert-command) or `blockchain push`.

3. [Configuring synchronization](blockchain%20configuration.md) against the blockchain platform.  

## Executing the blockchain commands
The blockchain commands can be executed on each node of the cluster and operate on the blockchain platform or the master node 
that is used by the network. The commonly used commands are the following:
* ```blockchain insert``` - add a policy to the ledger.
*```blockchain delete policy``` - delete a policy from the ledger.
* ```blockchain get``` - query a policy or policies from the ledger.
  
Other commands may be specific to a blockchain platform or a master node and are used to debug and monitor a particular 
setup of a particular environment.
These blockchain commands are detailed below.

## Adding policies

AnyLog offers a set of commands to add new policies to the ledger.
The generic command is `blockchain insert`. This command is used to update both - the global copy and the local copy.  
If only the global copy is updated, it may take a few seconds for the update to be reflected on the local copy. The 
`blockchain insert` command makes the new policy immediately available on the node that triggered the update.  
Policies that are added using the `blockchain insert` command will also persist locally (if the command directs to update the local copy), such that if during the time of 
the update, the global ledger is not accessible, when the network reconnects, the new policies will be delivered to the global ledger.

Below are the list of commands to add new policies to the ledger:

| **Command** | **Platform Updated** |  **Details** |
| ------------ | ------------------------------------ | --- | 
| [blockchain insert](#the-blockchain-insert-command) [policy and ledger platforms information] | All that are specified | Add a new policy to the ledger in one or more blockchain platform. |
| `blockchain add [policy]`           | Local Copy |Add a Policy to the local ledger file. |
| `blockchain push [policy]`          | DBMS |Add a Policy to the local database. |
| `blockchain commit [policy]`       | Blockchain Platform (i.e. Ethereum) | Add a Policy to a blockchain platform. |  

When policies are added, nodes validate the structure of the policies and their content. In addition, when policies are added, the policies are
updated with a date and time of the update and a [unique ID](#the-policy-id).

## Delete policies

AnyLog offers a set of commands to delete policies from the ledger.
The generic command is `blockchain delete policy`. This command is used to update both - the global copy and the local copy.  

Policies that are deleted using the `blockchain delete` command will also deleted from the local copy of the ledger 
(if the command directs to update the local copy), such that if during the time of the update, the global ledger is 
not accessible, when the network reconnects, the new policies will be delivered to the global ledger.

Below are the list of commands to add new policies to the ledger:

| **Command** | **Platform Updated** |  **Details** |
| ------------ | ------------------------------------ | --- | 
| [blockchain delete policy](#the-blockchain-delete-policy-command) [policy and ledger platforms information] | All that are specified | Delete an existing policy from the ledger. |
| `blockchain drop policy`           | Local DBMS | Remove a policy from the local database. |
| `blockchain drop by host`          | local DBMS | Remove all policies updated by a particular host. |

When policies are added, nodes validate the structure of the policies and their content. In addition, when policies are added, the policies are
updated with a date and time of the update and a [unique ID](#the-policy-id).

## Retrieving the metadata from a source node
The following command retrieves the metadata from a source node:
```anylog
blockchain seed from [ip:port]
```
The command is used when a new node starts in an existing network, it allows the new node to sync with an exiting metadata.

## Query policies

AnyLog offers commands to query policies.  
Queries are processed on the local copy of the ledger and are not dependent on the availability or latency of the global ledger.  
Queries detail filter criteria to return the needed policies in JSON format and can be augmented by formatting instructions.   
Alternatively, the process can be split to a process that retrieves the needed policies and use a second command to apply the formatting instructions on the derived policies.  
For example, a search may request for all the operators supporting a table and then issue a second search against the retrieved operators for their IP and Port information.  
The second search is using the command _from_ and is explained at the
section called: [The 'From JSON Object Bring' command](json%20data%20transformation.md#the--from-json-object-bring-command).

Queries are done in 2 steps:
* Using the command ```blockchain get``` - retrieving the JSON objects that satisfy the search criteria.
* Using the command ```bring``` - pulling and formatting the values from the retrieved JSON objects.
 
Usage:
```anylog
blockchain get [policy type] [where] [where conditions] [bring] [bring command instructions]
```


Explanation:
The `blockchain get` command retrieves one the policies that satisfy the search criteria from the local copy of the ledger.  
* _policy_ type - the key at the root of the JSON representing the policy.
* _where_ conditions - reference the policy values that are evaluated to determine if the policy is selected.
* _bring_ command - determined the retrieved data and formatting options.  

### Selecting the policy type

AnyLog policies have a single attribute at the root of the policy. The root attribute name is the policy type.  
For example, in the [Metadata Section](#the-metadata), the policy type is _operator_.  
The following command selects all policies of a particular type:
```anylog
blockchain get [policy type]
```
The following example selects all policies of a type operator_:
```anylog
blockchain get operator
```

Selecting multiple types is allowed by separating policies using a comma and placing the policies types in parentheses.    
The following example selects all policies of a type ***operator*** and type ***publisher***:
```anylog
blockchain get (operator, publisher)
```
Selecting all policies is allowed as in the following example:
```anylog
blockchain get *
```

### The where condition

The where condition is provided in one of 2 ways:  
* As a list of attribute name value pairs, expressed as ***name = value*** (or ***name with value*** to validate a value in a list) separated by the ***and*** keyword.   
The list of attribute name (key) value pairs in the where conditions is provided as follows:
    ```anylog
    key1 = value1 and key2 = value2 and key3 = value3 and ... keyN = valueN
    ```
    A key represents the path in the policy to the tested value, for example ***[operator][name]*** is the path to the name value in the operator policy.  
    Note that the root name in the path does not have to be enclosed with square brackets: ***[operator][name]*** is equivalent to ***operator[name]***.

* As a ***conditional execution*** whereas policy values are evaluated to determine if these values satisfy the search 
criteria. Attribute name value pairs are referenced using square brackets, for example ***[operator][name]*** will pull 
the name from the Operator policy. The following example evaluates attribute values of the policy example in the 
[Metadata Section](#the-metadata):

     ```anylog
    [operator][country] == USA and ([operator][country] == "San Francisco" or [operator][country] == "San Jose")
    ```
 Conditional execution is detailed [here](anylog%20commands.md#conditional-execution). 

Examples:
```anylog
blockchain get operator where dbms = lsl_demo
blockchain get operator where dbms = lsl_demo and ip = 24.23.250.144
blockchain get cluster where table[dbms] = purpleair and table[name] = cos_data bring [cluster][id] separator = ,
blockchain get operator where [name] == operator11 or [name] ==  operator1 bring [*][name]
```

### Formatting retrieved data 

The ***bring*** command can be added to a blockchain ***get*** command such that ***get*** retrieves metadata in a JSON format and the keyword ***bring*** operates on the retrieved JSON data.  
See details and examples in the [JSON data transformation](json%20data%20transformation.md#json-data-transformation) section.

### Setting command destination from policies

A common usage of policies is to determine the destination of a command or a query (in case of a query, to overwrite the network protocol's destination).    
The process evaluates policies by some criteria and sets a command destination to the IPs and ports detailed in the policies that satisfies the criteria.   
The structure of the command is as follows:
```anylog 
run client (blockchain get ...) anylog command
```

The ***blockchain get*** includes ***bring*** directive to construct the command destination as a list of comma separated IPs and Ports.
 
The following 2 examples sends a network status command to all Operator and Query nodes in specific countries. 
Note that the 2 examples below return equivalent result -  
In the first example, the first command queries the metadata to retrieve the destination nodes and places the destination 
in a dictionary variable.  
The second command sends a request to get the network status from the destination nodes assigned to the variable.  
The second example details the destination using the ***blockchain get*** command in the destination parenthesis of the ***run client ()*** command.

```anylog
# Using an AnyLog variable get network information regarding nodes in the US and Israel
destinations = blockchain get (operator, query) where [country] == US or [country] == IL  bring [*][ip] : [*][port] separator = ,

run client (!destinations) get node info net_io_counters 

# Without first declaring a variable (destination) get network information regarding nodes in the US and Israel 
run client (blockchain get (operator, query) where [country] == US or [country] == IL  bring [*][ip] : [*][port] separator = ,) get node info net_io_counters
```
## The blockchain read command
The ```blockchain read``` command in interpreted as the ```blockchain get``` command with the following difference:
* blockchain get - retrieves the policies after the analysis done by the node. Some policies are updated dynamically during normal operations.  
* blockchain read - retrieves the policies from the copy provided by the blockchain platform or master node. This version of the policies does not include dynamic updates.
Usually, users query the metadata using ***blockchain get***.  
The ***blockchain read*** option is only used to determine the source format of the policies at their time of arrival. 

## The blockchain insert command
The ***blockchain insert*** command adds a policy to the blockchain ledger. 
This command can update both - the local copy and the global copy of the ledger. In addition, it facilitates a process that validates that all the updates
are represented on the global copy (as during the issue of the insert command, the global copy may not be accessible).  

Usage:
```anylog
blockchain insert where policy = [policy] and blockchain = [platform] and local = [true/false] and master = [IP:Port]
```

Command details:

| Key | Value | 
| ------------ | ------------------------------------ |
| policy          | A json policy that is added to the ledger                                                                                                                                                  |
| blockchain      | A connected blockchain platform (i.e. Ethereum, and see Ethereum connection info in [this doc](using%20ethereum.md#using-ethereum-as-a-global-metadata-platform)).                                                                         |
| local           | A true/false value to determine an update to the local copy of the ledger. The default value is True                               |
| master          | The IP and Port value of a master node (configuring a master node is detailed in [this doc](master%20node.md#using-a-master-node).) |

Using the ***blockchain insert*** command, all the specified ledgers are updated. The common configuration would include the local ledger and 
either a blockchain platform (like Ethereum) or a master node.  

When the policy is updated on the local ledger, the policy is updated with the key: "ledger" and a value "local" to indicate that 
the policy is not yet confirmed on the global ledger (the blockchain platform or a master node).   
When the local ledger is synchronized with the global ledger, the status of the key "ledger" is changed from "local" to "global".

Examples:
```anylog
blockchain insert where policy = !policy and local = true and master = !master_node
blockchain insert where policy = !policy and local = true and blockchain = ethereum
```

## The blockchain delete policy command

The ***blockchain delete policy*** command removes a policy from the ledger.   
The command updates the local copy and the global copy of the ledger. 

Usage:
```anylog
blockchain delete policy where id = [policy id] and blockchain = [platform] and master = [IP:Port] and local = [true/false]
```

Command details:

| Key | Value | 
| ------------ | ------------------------------------ |
| id  | The Policy ID|
| blockchain      | A connected blockchain platform (i.e. Ethereum, and see Ethereum connection info in [this doc](using%20ethereum.md#using-ethereum-as-a-global-metadata-platform)).                                                                         |
| master          | The IP and Port of a master node (configuring a master node is detailed in [this doc](master%20node.md#using-a-master-node).) |
| local           | A true/false value to determine an update to the local copy of the ledger. The default value is True    |

Examples:
```anylog
blockchain delete policy where id = !policy_id and master = !master_node
blockchain delete policy where policy_id = !policy_id and local = true and blockchain = ethereum
```

## Copying policies representing the metadata to the local ledger
The local representation of the blockchain file is updated continuously if the [blockchain synchronization](background%20processes.md#blockchain-synchronizer) 
process is enabled.  
If the blockchain sync process is disabled, and the local blockchain file is updated or copied from a different node, the command ***blockchain load metadata*** 
will force the node to use the updated local file.  
For example, ***blockchain sync*** is not enabled, and a local file is copied from a member node as follows:
```anylog
run client 10.0.0.25:2548 file get !!blockchain_file !blockchain_file
```
The following command will force the node to replace the metadata representation with the local file:
```anylog
blockchain load metadata
```

## Using a local database to host the ledger

A Master Node maintains the ledger in a local database. In addition, any node can keep the local copy of the ledger in a local database.
The following are commands that interact with a database that hosts the ledger:

| **Commands** | **Details** |
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
Example: `sql blockchain "select * from ledger"`

### Retrieving the Metadata from a Master Node
Retrieving the metadata from a Master Node is done by a blockchain pull request that is sent to the Master Node (using 
“run client” command) and copying the data to the desired location on the client node (using ***file get*** command).  
Example:
```anylog
mater_node = 127.45.35.12:32048
run client (!master_node) blockchain pull to json
run client (!master_node) file get !!blockchain_file !blockchain_file
```
Notes:
* `blockchain_file` is configured to the path and file name of the ledger.
* The double exclamation points (!!) determine to derive the value of the key `blockchain_file` on the target node (127.45.35.12).
* Details on the ***file get*** command are available [here](file%20commands.md#file-copy-from-a-remote-node-to-a-local-node).
* With synchronization enabled, this process is done continuously as configured and is not required to be triggered by the user. 

### Removing policies from a master node
Policies are deleted using the ***blockchain drop policy*** command.   
Policies are dropped on the master node and if issued on a member node, the command is transferred to the master node using 
`run client !master_node` directive.  
The `blockchain drop policy` command can be issued in one of the following forms:  
 * Specifying the policy ID
    ```anylog 
    blockchain drop policy where id = [one or more policy ids]
    ```
   For examples:
    ```anylog
    blockchain drop policy where id = b90b40ff46ea7244a49357a46901e114
    blockchain drop policy where id = b90b40ff46ea7244a49357a46901e114, 4a0c16ff565c6dfc05eb5a1aca4bf825 
    blockchain drop policy where id = !id_string  # id_string is a comma separated IDs
   ```
* specifying the IP-Port list as a `blockchain get` command: 
    ```anylog
    blockchain drop policy where id = blockchain get (cluster, operator) where [company] contains ibm bring [*][id] separator = ,
    ```
* specifying the policy data 
    ```anylog
    blockchain drop policy [JSON data]
    ```
  JSON data is the policy to drop and can be expressed as a variable.  
  For example:
    ```anylog
    blockchain drop policy !operator
    ```
  If the variable is a list to multiple policies, a where condition is required, for example:
    ```anylog
    blockchain drop policy !operator where ip = 10.0.0.25
    ```


### Reflecting blockchain updates on the local copy of the metadata

When a process on a node updates a policy on a remote blockchain platform (or on a master node), the process can wait for 
the update to be reflected on the local copy using the ***blockchain wait for ...*** command:
```anylog
# Add an ID and a date to the policy being updated
AL anylog-node > blockchain prepare policy !policy     

# Make the update
AL anylog-node > run client (!master_node) blockchain push !policy

# Force sync and validate that the update is available   
AL anylog-node > is_updated = blockchain wait for !policy  
```
The wait command forces synchronization with the blockchain platform and validates that the update is reflected on the local file.

Note: This process is redundant if the update of the new policies was done using the [blockchain insert](#the-blockchain-insert-command) command.

## Other blockchain commands:

| **Command** | **Details** |
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


