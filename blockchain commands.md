
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
```blockchain push [JSON data]``` – add a JSON object to the local database  
```blockchain pull to sql``` – retrieve the blockchain data from the local database to a SQL file that organizes the metadata as insert statements.  
```blockchain pull to JSON``` – retrieve the blockchain data from the local database to a JSON file that can be used as the local JSON file.  


```blockchain commit [JSON data]``` – add a JSON object to the blockchain  
```blockchain checkout``` – retrieve the blockchain data from the blockchain to a JSON file.  
```blockchain create table``` – creates a local table (called ***ledger***) on the local database that maintains metadata information.  
```blockchain drop table``` – drops the local table (***ledger***) on the local database that maintains metadata information.  
```blockchain drop policy [JSON data]``` – removes the policy specified by the JSON data fom local database that maintains metadata information.  
```blockchain delete local file``` - deletes the local JSON file with the blockchain data. 


```blockchain test``` - test the structure of the local JSON file. Returns True if the file structure is valid. Otherwise, returns False. 
```blockchain get id [json data]``` - returns the hash value of the JSON data.  
```blockchain test id``` - returns True if the id exists in the local blockchain file. Otherwise returns False.

### Updating a Master Node
Updating the Master Node is Done by a blockchain push request that is send to the Master Node (using ***run client*** command).  

### Retrieving the Metadata from a Master Node
Retrieving the metadata from a Master Node is done by a blockchain pull request that is send to the Master Node (using “run client” command) and copying the data to the desired location on the client node (using ***file get*** command).  

### Interacting with the blockchain data
For a node to be active, it needs to maintain a local copy of the blockchain data in a local JSON file.
The local copy becomes available by assigning the path and file name to the global variable ***blockchain_file***.
A user can validate the availability and the structure of the blockchain using the command: ```blockchain test```.

### Queries over the Metadata
Metadata queries evaluate the data in the local JSON file.  
Queries are done in 2 steps:
* Using the command ```blockchain get``` - retrieving the JSON objects that satisfy the search criteria.
* Using the command ```bring``` - pulling and formatting the values from the retrieved JSON objects.

#### bring options
The keyword bring can be suffixed with ***.unique*** or ***.recent***.     
* ```bring.unique``` returns unique values.  
* ```bring.recent``` - considering and returning the recent event satisfying the ***get*** criteria. The most recent event is determined by the following:  
        - If the JSON file includes a "date" attribite, comparing the dates.  
        - Without the "date" attribute, the last object satisfying the ***get*** criteria in the JSON file is considered the ***recent*** object.

The following examples retrieves all the operators with SLA at level 5 that are located in California:  

a) Using an assignment of the JSON objects to ***selected_operators*** and pulling the IP and Port from each JSON object:
 
<pre>
selected_operators = blockchain get "operator" {"SLA" : "5", “location”:”CA”} # get operators with SLA == 5 and location is CA
ip_port = from !selected_operators bring ['operator']['ip'] ":" ['operator']['port'] seperator = " " # get the IPs and ports of these operators
</pre>

b) Using a single call:
 
<pre>
blockchain get operator {"SLA" : "5", “location”:”CA”} bring ['operator']['ip'] ":" ['operator']['port'] seperator = " " 
</pre>

c) Using a ***where*** condition replacing the JSON structure in the search of the JSON objects:
 
<pre>
blockchain get operator where SLA = 5 and location = CA bring ['operator']['ip'] ":" ['operator']['port'] seperator = " " 
</pre>

The following examples retrieves all the databases which are in the JSON objects describing the tables:  

<pre>
blockchain get table bring ['table']['dbms'] seperator = " " 
</pre>

The following examples retrieves unique databases which are in the JSON objects describing the tables:  

<pre>
blockchain get table bring.unique ['table']['dbms'] seperator = " " 
</pre>

The following examples retrieves the most recent declaration of an operator supporting a database called lsl_demo:  

<pre>
blockchain get operator where dbms = lsl_demo bring.recent 
</pre>


### Using - Show Commands
The following show commands retrieve data from the blockchain:
* ```show servers for dbms [dbms name]``` - retrieve the IPs and Ports of the database servers hosting tables for the named database.  
* ```show servers for dbms [dbms name] and [table name]``` - retrieve the IPs and Ports of the database servers hosting the named table.
* ```show tables for dbms [dbms name]``` - retrieve the names of the tables that are assigned to the named database.
 
### Retrieve blockchain data from the local database

Retrieve blockchain data from the local database on the AnyLog command line can be done using SQL.  
Example: ```sql blockchain text "select * from ledger"```
