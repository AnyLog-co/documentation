# Adding Data to Nodes in the Network
 
 AnyLog hosts the data on nodes in the network that are configured as Operators (Operators nodes are sometimes called Contractors).
 Any connected node can host data.  
 The methods to deliver data to Operator nodes in the network is described in the this document.
 
 ## Data transfer to Operator with REST API
 
 In this method, data is being transferred to a particular node in the network using a REST API.
 Depending on the configuration, the receiving node can operate as an Operator and host the data,  
 or operate as a Publisher and transfers the data to Operator nodes that will host the data.
  
 In both cases, the receiving node serves as a REST server waiting for incoming messages with data.
 
 #### On the Receiving Node (an AnyLog node): 
 Configure the node to operate as a REST server using the following command on the AnyLog command prompt:
 
<pre>
run rest server [ip] [port] [timeout]
</pre>
***[ip]*** - The ip supporting the REST connection  
***[port]*** - The REST port  
***[timeout]*** - Timeout in seconds to determine a time interval such that if no response is being returned in the time interval, the system returns ***timeout error***.  
The default value is 20 seconds.
    
 #### On the sender node (a client node which is not necessarily a member of the AnyLog Network):
 
Using a REST client, use the ***PUT*** command and send the data with the following keys and values in the header:  
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
 
 Install the AnyLog software on the node that receives the data.
 Configure the AnyLog agent as a Publisher Node.
 Configure the node to include the policies to determine the Operators that would service the data.
 Configure a ***watcg directory***.
 
 Place the data at the ***watcg directory***.
 
 The Publisher node connects with the Operators that will host the data and delivers the new data to the Operators.
  
 
 
