
# Blockchain commands

## The metadata
AnyLog maintains the metadata in the blockchain. The metadata is organized as a collection of objects and each object is described by a JSON structure.  
The objects are hierarchical. The top layer represents the type of the object and the lower levels provide a description of the object.  

Example of object types: database, table, operator, device.  
The following example describes an operator (this type of representation is referenced as ***json data***):
```
{"operator" : {	
   "id" : "0xodef4362a4E72E4D2F489773ffaEBF687952FC56441",
   "URL" : "www.sunnyvaledatacenter.com",
   "ip" : “128.132.43.73”,
   "port" : “3028”,
   "SLA" : "5",
   "price per MB" : "0.004",
   "price per row" : "0.00001"
   }
}
```

When a node needs to consider an object, the search is provided with the object type and optionally some attributes and values pairs that describe the object. The search returns all the objects that satisfy the search criteria.  
The following is an example of how a search is described to find all the Operators with SLA equal to 5 and 0.004 as the price for MB of storage (this type of representation is referenced as [json search]).  

```
{"operator" : {   
    "SLA" : "5",    
    "price per MB" : "0.004"
    }
}
```

If a node is interested in some specific attribute values from the derived objects, a second search can be issued against the derived objects to retrieve the values of interest.  
For example, a search may request for all the operators supporting a table and then issue a second search against the retrieved operators for their IP and Port information.  
The second serach is using the command ***from*** and is explained later in this document.

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
```blockchain add [JSON data]``` – add a JSON object to the local JSON file.  
```blockchain get [JSON search]``` – retrieve from the JSON file all objects that satisfy the search criteria.  
```blockchain push [JSON data]``` – add a JSON object to the local database.    
```blockchain pull to sql [optional output file]``` – retrieve the blockchain data from the local database to a SQL file that organizes the metadata as insert statements.    
```blockchain pull to json [optional output file]``` – retrieve the blockchain data from the local database to a JSON file that can be used as the local JSON file.
```blockchain pull to stdout``` – retrieve the blockchain data from the local database to stdout.          
```blockchain update file [path and file name]``` – copy the file to replace the current local blockchain file. Prior to the copy, the current blockchain file is copied to a file with extension ***'.old'***. If file name is not specified, a ***blockchain.new*** is used as the file to copy.    
```blockchain update dbms [path and file name] [ignore message]``` – add the policies in the named file (or in the blockchain file, if a named file is not provided) to the local dbms that maintains the blockchain data. The command outputs a summary on the number of new policies added to the database. To avoid the message printout and messages of duplicate policies to the error log, add ***ignore message*** as a command prefix.  

```blockchain commit [JSON data]``` – add a JSON object to the blockchain  
```blockchain checkout``` – retrieve the blockchain data from the blockchain to a JSON file.  
```blockchain create table``` – creates a local table (called ***ledger***) on the local database that maintains metadata information.  
```blockchain drop table``` – drops the local table (***ledger***) on the local database that maintains metadata information.  
```blockchain drop policy [JSON data]``` – removes the policy specified by the JSON data fom local database that maintains metadata information.    
```blockchain replace policy [policy id] with [new policy]``` - replace an existing policy in the local blockchain database.        
```blockchain delete local file``` - deletes the local JSON file with the blockchain data.  

```blockchain test``` - test the structure of the local JSON file. Returns True if the file structure is valid. Otherwise, returns False. 
```blockchain get id [json data]``` - returns the hash value of the JSON data.  
```blockchain test id``` - returns True if the id exists in the local blockchain file. Otherwise returns False.

```blockchain load metadata [conditions]``` - update the local metadata from policies published on the blockchain.  
```blockchain query metadata [conditions]``` - provides a diagram representation of the local metadata.  
```blockchain test cluster [conditions]``` - provides an analysis of the \'cluster\' policies.  

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

### Interacting with the blockchain data
For a node to be active, it needs to maintain a local copy of the blockchain data in a local JSON file.
The local copy becomes available by assigning the path and file name to the global variable ***blockchain_file***.
A user can validate the availability and the structure of the blockchain using the command: ```blockchain test```.

### Queries over the Metadata
Metadata queries evaluate the data in the local JSON file.  
Queries are done in 2 steps:
* Using the command ```blockchain get``` - retrieving the JSON objects that satisfy the search criteria.
* Using the command ```bring``` - pulling and formatting the values from the retrieved JSON objects.

### Using - Show Commands
The following show commands retrieve data from the blockchain:
* ```show servers for dbms [dbms name]``` - retrieve the IPs and Ports of the database servers hosting tables for the named database.  
* ```show servers for dbms [dbms name] and [table name]``` - retrieve the IPs and Ports of the database servers hosting the named table.
* ```show tables for dbms [dbms name]``` - retrieve the names of the tables that are assigned to the named database.
 
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

