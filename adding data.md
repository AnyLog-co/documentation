# Adding Data to Nodes in the Network
 
AnyLog hosts the data on nodes in the network that are configured as Operators (Operators nodes are sometimes called Contractors).
Any connected node can host data. 
 
There are 2 methods to deliver data to Operators in the network:  
1) Using a REST API - the client is not necessarily a member of the network, data is delivered using the PUT command.
2) Using a WATCH directory -  The client is a a member of the network (the AnyLog software is installed ion the client). Adding data is by placing the data in the WATCH directory.   


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


## Data transfer using a Publisher Nodes
 
 1) Install the AnyLog software on the node that receives the data.
 2) Configure the AnyLog agent as a Publisher Node.
 3) Configure the node to include the policies to determine the Operators that would service the data.
 4) Configure a ***watch directory***.
 
 The configured AnyLog node processes data placed on the watch directory whenever new data is added to the directory.
 Therefore, when data is added to the watch directory, the Publisher node connects with the Operators that will host the data and delivers the new data to the Operators.
 