# Adding Data to Nodes in the Network
 
AnyLog hosts the data on nodes in the network that are configured as Operators (Operators nodes are sometimes called Contractors).
Any connected node can host data. 
 
There are 2 methods to deliver data to Operators in the network:
1) Using a WATCH directory - Adding data is by placing the data in the WATCH directory.  
2) Using a REST API - the REST client is not necessarily a member of the network, data is delivered using the PUT command.
   
Files received by nodes are processed depending on the configuration of the node.
If a node is configured as a Publisher, it will send each file received to one of the Operators that manage the table containing the data.
If a node is configured as an Operator, it will add each file received to a local table that contains that type of data.

## Placing data in the WATCH directory

This option allows to add data by placing new data in a Watch Directory.  
A Watch Directory is a disk directory designated to new data. Operators monitor data placed in a watch directory such that when new data is identified, the data processing functionality is triggered.   
Operator nodes are configured such that any file (of the type JSON or SQL) that is placed on a WATCH directory is being processed.  
The default processing is as follows:  
1. The file is read by the operator.
2. From the file name, the processing variables and logic are determined. These include the logical database, table name and the method to determine the mapping of the data.
3. If a logical table does not exists, a table is created.
4. The file data is added to the table.

## JSON File naming

The file name includes the information needed to determine how the file's data is processed.  
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
data source     - A unique ID to identify the data source (i.e. an ID of the sensor).
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
Depending on the configuration, the receiving node can operate as an Operator and host the data, or it can be configured to operate as a Publisher and transfers the data to one or more Operator nodes that will host the data.  

In both cases, the receiving node serves as a REST server waiting for incoming messages with new data.

### Configuring the Receiving Node (an AnyLog node): 
Configure the node to operate as a REST server using the following command on the AnyLog command prompt:
 
<pre>
run rest server [ip] [port] [timeout]
</pre>

***[ip]*** - The IP supporting the REST connection  
***[port]*** - The REST port  
***[timeout]*** - Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns ***timeout error***.  
The default value is 20 seconds.  
    
### Configuring the Sender Node (a client node which is not necessarily a member of the AnyLog Network):
 
Use a REST client software (such as Curl or Postman) and issue a ***PUT*** command to send the data with the following keys and values in the header:
  
<pre>
Key             Value
------          -------------
type            The type of data transferred. The default value is ***json***.
dbms            The logical database to contain the data.
table           The logical table to contain the data.
source          A unique ID to identify the data source (i.e. an ID of a sensor).
instructions    An ID of a policy that determines the mapping of the file data to the table's structure.
</pre>

The JSON data is transferred using the data-raw part of the REST call and can include any number of readings.

##### Example using Curl:

<pre>
curl --location --request PUT '10.0.0.78:2049' \
--header 'type: json' \
--header 'dbms: lsl_demo' \
--header 'table: ping_sensor' \
--header 'Content-Type: text/plain' \
--data-raw '{"parentelement": "62e71893-92e0-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "ADVA FSP3000R7", "value": 0, "timestamp": "2019-10-11T17:05:08.0400085Z"}
{"parentelement": "68ae8bef-92e1-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "Catalyst 3500XL", "value": 50, "timestamp": "2019-10-14T17:22:13.0510101Z"}
{"parentelement": "68ae8bef-92e1-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "Catalyst 3500XL", "value": 50, "timestamp": "2019-10-14T17:22:18.0360107Z"}
</pre>
