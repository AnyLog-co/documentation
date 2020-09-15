# Adding Data to Nodes in the Network
 
AnyLog hosts the data on nodes in the network that are configured as Operators (Operators nodes are sometimes called Contractors).
Any connected node can host data. 
 
There are 2 methods to deliver data to Operators in the network:
1) Using a WATCH directory - Adding data is by placing the data in the WATCH directory.  
2) Using a REST API - the REST client is not necessarily a member of the network, data is delivered using the PUT command.
   
Files received by nodes are processes depending on the configuration of the node.
If a node is configured as a Publisher, it will send each file received to one of the Operators that manage the table containing the data.
If a node is configured as an Operator, it will add each file received to a local table that contains that type of data.

## Placing data in the WATCH directory

This option allows to add data by placing the data on the watch directory.  
Operator nodes are configured such that any file (of the type JSON or SQL) that is placed on a WATCH directory is being processed.  
The default processing is as follows:  
1. The file is read by the operator.
2. From the file name, the processing variables are determined. These include the logical database, table name and the method to determine the mapping of the data.
3. If a logical table does not exists, a table is created.
4. The file data is added to the table.

## JSON File naming
test
The file name is used to identify the file and determine how the file is processed.  
The file name is partitioned to segments separated by a dot as follows: 

<pre>
[dbms name].[table name].[data source].[hash value].[instructions].json
</pre>

Users can display the segments dynamically by issuing the following command:
<pre>
show json file structure
</pre>
The name segments are treated as follows:
 
<pre>
dbms name       - The logical database to contain the file data.
table name      - The logical table to contain the file data.
data source     - A unique ID to identify the data source (i.e. and ID of the sensor).
hash value      - A hash value that identifies the file. 
instructions    - An ID of a policy that determines the mapping of the file data to the table's structure.
json            - The content of data inside the file is of JSON data.
</pre>

Users can determine the hash value of a file by issuing the command:
<pre>
file hash [file name and path]
</pre>


## Data transfer using a REST API

In this method, data is being transferred to a particular node in the network using a REST API.
Depending on the configuration, the receiving node can operate as an Operator and host the data,  
or it can be configured to operate as a Publisher and transfers the data to one or more Operator nodes that will host the data.

In both cases, the receiving node serves as a REST server waiting for incoming messages with data.

#### On the Receiving Node (an AnyLog node): 
Configure the node to operate as a REST server using the following command on the AnyLog command prompt:
 
<pre>
run rest server [ip] [port] [timeout]
</pre>

***[ip]*** - The IP supporting the REST connection  
***[port]*** - The REST port  
***[timeout]*** - Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns ***timeout error***.  
The default value is 20 seconds.
    
#### On the sender node (a client node which is not necessarily a member of the AnyLog Network):
 
Use a REST client software (such as curl pr postman) and issue a ***PUT*** command to send the data with the following keys and values in the header:  
<pre>
Key     Value
------  -------------
type    [type of data transferred]
dbms    [database name]
table   [table name]
details [data to add]
</pre>

***[type of data transferred]*** - for JSON data use ***json file ***, for SQL data use ***sql file***     
***[database name]*** - the logical name of the database to use  
***[table name]*** - the table to use  
***[data to add]*** - the data to add  

##### Example:

<pre>
curl    --header "type":"json file"  
        --header "dbms":"anylog_test" 
        --header "table":"my_table"
        --header "details":"{"parentelement": "11e78320-93b1-11e9-b465-d4856454f4ba", "webid": "F1AbEfLbwwL8F6EiShvDV-QH70AIIPnEbGT6RG0ZdSFZFT0ugL19tYGrwdFojNpadLPwI4gWE9NUEFTUy1MSVRTTFxMSVRTQU5MRUFORFJPXFNBTiBTRUJBU1RJQU4gMjg4MVxSRU1PVEUtU0VSVkVSLUFORFJFU3xQSU5H", "device_name": "REMOTE-SERVER-ANDRES", "value": 168, "timestamp": "2019-10-11T17:13:39.0430145Z"}"
        --request PUT host:port
</pre>


## Configuring a Publisher Node to receive data
 
 1) Configure an AnyLog Node as a Publisher Node.
 2) Configure the node as a REST server.
 3) Create the directory structure that hosts local data.
 4) Configure the node to include the policies to determine the Operators that would service the data.
 5) Configure a ***watch directory*** to a parameter called ***watch_dir***.
 6) Configure a ***rest directory*** to a parameter called ***rest_dir***.
 7) Configure an ***error directory*** to a parameter called ***err_dir***.
 
 ## The process
 * The rest client sends the data to the AnyLog Node.
 * The data is placed on the ***rest directory***.
 * The data is moved to the ***watch directory***.
 * If the process fails, the data is moved to the ***error directory***.
 * The AnyLog Node applies the ***watch process*** on the data.
