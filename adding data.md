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

### JSON File naming

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

### The Data Format

To process a file containing JSON instances, the JSON instances need to be organized as strings with the new line character (LF) separating between the instances.  
Example:  
<pre>
{"parentelement": "62e71893-92e0-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "ADVA FSP3000R7", "value": 0, "timestamp": "2019-10-11T17:05:08.0400085Z"}  
{"parentelement": "68ae8bef-92e1-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "Catalyst 3500XL", "value": 50, "timestamp": "2019-10-14T17:22:13.0510101Z"}  
{"parentelement": "68ae8bef-92e1-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "Catalyst 3500XL", "value": 50, "timestamp": "2019-10-14T17:22:18.0360107Z"}  
</pre>

## Data transfer using a REST API

In this method, data is being transferred to a particular node in the network using a REST API.
Depending on the configuration, the receiving node can operate as an Operator and host the data, or it can be configured to operate as a Publisher and transfers the data to one or more Operator nodes that will host the data.  

In both cases, the receiving node serves as a REST server waiting for incoming messages with new data.  

The transferred data is processed in one of two modes:
* In a file mode - The transferred data is a file, the file is written to the Prep dirctory and then moved to the Watch directory.
* In a streaming mode - Data is accumulated in an internal buffer and being processed when a time threshold or a volume threshold are triggered. 
File Mode and Streaming Mode are detailed [below](#file-mode-and-streaming-mode).


### Configuring the Receiving Node (an AnyLog node): 

The node processing the PUT request needs to be configured as follows:

* As a REST server to receive the REST requests from the client.
using the following command on the AnyLog command prompt:
<pre>
run rest server [ip] [port] [timeout]
</pre>
***[ip]*** - The IP supporting the REST connection  
***[port]*** - The REST port  
***[timeout]*** - Timeout in seconds to determine a time interval such that if no response is being returned during the time interval, the system returns ***timeout error***.  
The default value is 20 seconds.  
* As an Operator (to host the new data) or as a Publisher (to transfer the new data to open or more Operators).  
Details on how an operator is configured are available [here](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#publisher-process).
    
### Configuring the Sender Node (a client node which is not necessarily a member of the AnyLog Network):
 
Use a REST client software (such as Curl or Postman) and issue a ***PUT*** command to send the data with the following keys and values in the header:
  
<pre>
Key             Value
------          -------------
type            The type of data transferred. The default value is ***json***.
dbms            The logical database to contain the data.
table           The logical table to contain the data.
source          A unique ID to identify the data source (i.e. an ID of a sensor).
mode            File or Streaming (see details below). The default value is 'file'.
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

### The Data Format

To process a PUT request with new data, the data is organized in the message body as strings with the new line character separating between the JSON instances.
Extra New-Line (LF), Tab and Carriage Return characters (CR) are replaced with space. 


## File Mode and Streaming Mode

Data ingested to a local database is organized in files. Each file contains one or more sensor readings (or other type of time series data) organized in a JSON format.
Users adding data with the REST API determine the mode in which data is processed:

* Using a ***File Mode*** (the default mode) - a single data file is transferred using the PUT request, the file is registered (in the tsd_info table) and processed independently of other PUT requests.  
A File Mode is usually used when the PUT request contains a large amount of data or when the data is not frequenty created.  
    
* Using a ***Streaming Mode*** - The AnyLog instance receiving the data serves as a buffer that accumulates the data from multiple PUT requests. Upon a threshold, the accumulated data is organized as a file that is processed as a single unit.
A Streaming Mode is usually used when the frequency of data creation is high and the amount of data transferred in each PUT request is low.

#### Setting and retrieving thresholds for a Streaming Mode

Thresholds determine when buffered data is processed and are based on a time threshold and a data volume threshold.
If both are set, the earlier of the two triggers the processing of the data.

Time threshold can be specified in seconds, minutes, hours or days.  
Volume threshold can be specified byes, KB, MB or GB.

 
Users can configure a default value as well as thresholds for each each type of data by assigning a threshold to the table associated with the data.  

Setting the default values is with the following command:  
```set buffer threshold where time = [time] and volume = [data volume]```  
Example:  
```set buffer threshold where time = 1 hour and volume = 2KB```  

If the default values are not set, the node assigned the value 60 seconds to the time threshold and 10,000 bytes to the volume threshold.

Setting the threshold for a particular table is with the following command:  
<pre> 
set buffer threshold where dbms_name = [dbms name] and table_name = [table name] and time = [time] and volume = [data volume]
</pre>  
Notes:    
* If the table name is not provided, the thresholds are assigned to all the tables in the database which are not assigned with values.
* If the time is set to 0 seconds and the volume is set to 0 bytes - the threshold for the table's buffer is removed and the data associated with the table is assigned with the threshold default values.    

Retrieving the thresholds values is with the following command:  
```show rest``` 

The command provides information on the REST API usage and status including the buffer thresholds.





 
  

 
   


