# Adding Data to Nodes in the Network
 
AnyLog hosts the data on nodes in the network that are configured as Operators (Operators nodes are sometimes called Contractors).
Any connected node can host data. 
 
There are multiple ways to add data to Operators in the network:
* [Using a WATCH directory](#placing-data-in-the-watch-directory) - Adding data is by placing files containing JSON data in the WATCH directory. An example is available [here](https://github.com/AnyLog-co/documentation/blob/master/examples/network%20setup.md#push-data-to-the-network).
* [Using a REST API](#data-transfer-using-a-rest-api) - the REST client is not necessarily a member of the network, data is delivered using the PUT or POST commands.
* [Subscribing to a third party message broker](#subscribing-to-a-third-party-message-broker) and receiving the published data from the third party broker. 
* [Configuring the AnyLog node as a message broker](#configuring-the-anylog-node-as-a-message-broker) and receiving published data from clients.   
    If an AnyLog node is configured as a message broker, clients are able to publish data on the AnyLog node and map the published data to an existing schema. 

Note: Below is [The Southbound Connectors Diagram](#the-southbound-connectors-diagram).

## The node type
An AnyLog node can be configured in many ways. A node that receives streams data from devices can be configured as a Publisher node or an Operator Node.
Files received by nodes are processed depending on the configuration of the node.
If a node is configured as a Publisher, it will send each file received to one of the Operators that manage the table containing the data.
If a node is configured as an Operator, it will add each file received to a local table that contains that type of data.

## Placing data in the WATCH directory

This option allows adding data by placing new data in a Watch Directory.  
A Watch Directory is a disk directory designated to new data. Operator nodes monitor data placed in a watch directory such that when new data is identified, the data processing functionality is triggered.   
Operator nodes are configured such that any file (of the type JSON or SQL) that is placed on a WATCH directory is being processed.  
The default processing is as follows:  
1. The file is read by the operator.
2. From the file name, the processing variables and logic are determined. These include the logical database, table name, and the method to determine the mapping of the data.
3. If a logical table does not exist, a table is created.
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

Using HTTP methods, data is transferred to a particular node in the network.
There are 2 methods that support the transfer of data:
* PUT - data is provided in JSON format and mapped to a table structure whereas attribute names are dynamically mapped to column names and attribute values are mapped to column values.
* POST - data is provided in JSON format, the data includes a topic that determines the mapping to the table structure.
  Details are available in the section [AnyLog as a broker receiving REST commands](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#anylog-as-a-broker-receiving-rest-commands).
  

Depending on the configuration, the receiving node can operate as an Operator and host the data, or it can be configured to operate as a Publisher and transfers the data to one or more Operator nodes that will host the data.  
In both cases, the receiving node serves as a REST server waiting for incoming messages with new data.
Configuring a node as a ***rest server*** is detailed at [REST requests](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests).  

The transferred data is processed in one of two modes:
* In a file mode - The transferred data is a file, the file is written to the Prep Directory and then moved to the Watch Directory.
* In a streaming mode - Data is accumulated in an internal buffer and being processed when a time threshold, or a volume threshold are triggered. 
File Mode and Streaming Mode are detailed [below](#file-mode-and-streaming-mode).


### Configuring the Receiving Node (an AnyLog node): 

The node processing the REST request needs to be configured as follows:

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

### Using a PUT command
 
Use a REST client software (such as Curl or Postman) and issue a ***PUT*** command to send the data with the following keys and values in the header:
  
<pre>
Key             Value
------          -------------
User-Agent      AnyLog/1.23
type            The type of data transferred. The default value is ***json***.
dbms            The logical database to contain the data.
table           The logical table to contain the data.
source          A unique ID to identify the data source (i.e. an ID of a sensor).
mode            File or Streaming (see details below). The default value is 'file'.
instructions    An ID of a policy that determines the mapping of the file data to the table's structure.
</pre>

The JSON data is transferred using the data-raw part of the REST call and can include any number of readings.

##### Example using Curl:

```shell
curl --location --request PUT '10.0.0.226:32149' \
--header 'type: json' \
--header 'dbms: test' \
--header 'table: table1' \
--header 'Content-Type: text/plain' \
--header 'User-Agent: AnyLog/1.23' \
-w "\n" \ 
--data-raw '[{"parentelement": "62e71893-92e0-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "ADVA FSP3000R7", "value": 0, "timestamp": "2019-10-11T17:05:08.0400085Z"}, 
             {"parentelement": "68ae8bef-92e1-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "Catalyst 3500XL", "value": 50, "timestamp": "2019-10-14T17:22:13.0510101Z"}, 
             {"parentelement": "68ae8bef-92e1-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "Catalyst 3500XL", "value": 50, "timestamp": "2019-10-14T17:22:18.0360107Z"}]' 

# Expected output: {"AnyLog.status":"Success", "AnyLog.hash": "0dd6b959e48c64818bf4748e4ae0c8cb" }   
```


### The Data Format

To process a PUT or POST requests with new data, the data is organized in the message body as strings with the new line character separating between the JSON instances.
Extra New-Line (LF), Tab and Carriage Return characters (CR) are replaced with space. 


## File Mode and Streaming Mode

Data ingested to a local database is organized in files. Each file contains one or more sensor readings (or other type of time series data) organized in a JSON format.
Users adding data with the REST API determines the mode in which data is processed:

* Using a ***File Mode*** (the default mode) - a single data file is transferred using the PUT request, the file is registered (in the tsd_info table) and processed independently of other PUT requests.  
A File Mode is usually used when the PUT request contains a large amount of data or when the data is not frequenty created.  
    
* Using a ***Streaming Mode*** - The AnyLog instance receiving the data serves as a buffer that accumulates the data from multiple PUT requests. Upon a threshold, the accumulated data is organized as a file that is processed as a single unit.
A Streaming Mode is usually used when the frequency of data creation is high and the amount of data transferred in each PUT request is low.

File mode is the default mode. Changing the mode to streaming is by updating the header with the key ***mode*** and the value ***streaming***.  

***Header options for loading data:***

| key  | value  | Explanation |
| ---- | -------| ------------|
| mode | file | The body of the message is JSON data. Database load (on an Operator Node) and data send (on a Publisher Node) are with no wait. File mode is the default behaviour. |
| mode | streaming | The body of the message is JSON data that is buffered in the node. Database load (on an Operator Node) and data send (on a Publisher Node) are based on time and volume thresholds. |


## Setting and retrieving thresholds for a Streaming Mode

Thresholds determine when buffered data is processed and are based on a time threshold and a data volume threshold.
As multiple thresholds ate set, the earlier of the two triggers the processing of the data.  

Usage:
<pre> 
set buffer threshold where dbms_name = [dbms name] and table_name = [table name] and time = [time] and volume = [data volume] and write_immediate = [true/false]
</pre>  

Options:

| Option        | Explanation   | Default Value |
| ------------- | ------------- | ------------- |
| dbms_name  | The name of the database associated with the data  | All databases  |
| table_name  | The name of the table associated with the data  | All tables of the specified database  |
| time  | The time threshold to flush the streaming data  | 60 seconds  |
| volume  | The accumulated data volume that calls the data flush process  | 10KB  |
| write_immediate  | Local database is immediate (independent of the calls to flush)  | false  |

Note:
* Time threshold can be specified in seconds, minutes, hours or days.  
* Volume threshold can be specified byes, KB, MB or GB.
* Volume thresholds are enforced by the processes that add the data to the buffers (i.e. REST processes and MQTT processes).  
* The time thresholds are enforced by the ***Streaming*** process. To enable the streaming process execute the following command:
    <pre>
    run streamer 
    </pre>
    More information on the streamer process is available at the [Streamer Process](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#streamer-process) section.
* If the table name is not provided, the thresholds are assigned to all the tables in the database which are not assigned with values.
* If the time is set to 0 seconds and the volume is set to 0 bytes - the thresholds are reverted to the default values.    

Example:  
<pre>
set buffer threshold where time = 1 hour and volume = 2KB
</pre>

### Retrieving the thresholds values is with the following command:  
The command provides information on the REST API usage and status including the buffer thresholds.
<pre>
get streaming
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-streaming).


### Using a POST command

With the POST command, the data is mapped to a destination format. The mapping is determined by the topic which is provided 
in the headers as the value for the key ***topic***. If a topic value is not provided, the default topic is used.  
The default topic is the first topic described in the command ```run mqtt client ... ```. Command Details are available 
in the [Subscribing to REST calls](./using%20rest.md#subscribing-to-rest-calls) section.

**MQTT Call**
For the following sample _POST_ the `run mqtt client` is as follows: 
```
<run mqtt client where broker=rest and port=!anylog_rest_port and user-agent=anylog and log=false and topic=(
  name=new_data and 
  dbms=bring [dbms] and 
  table=bring [table] and 
  column.timestam.timestamp=bring [timestamp] and 
  column.value=(type=int and value=bring[value])
 )>  
```
**cURL Example**: 
```
curl --location --request POST '10.0.0.226:32149' \
--header 'command: data' \
--header 'topic: new_data' \
--header 'User-Agent: AnyLog/1.23' \
--header 'Content-Type: text/plain' \
--data-raw ' [{"dbms" : "aiops", "table" : "fic11", "value": 50, "timestamp": "2019-10-14T17:22:13.051101Z"},
 {"dbms" : "aiops", "table" : "fic16", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"},
 {"dbms" : "aiops", "table" : "ai_mv", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"}]'
```

**Python Example**: 
```python
import json 
import requests

# REST connection information (IP + Port) 
conn = '192.168.50.159:2051' 

# Header for POST data 
headers = {
    'command': 'data',
    'topic': 'new_data',
    'User-Agent': 'AnyLog/1.23',
    'Content-Type': 'text/plain'
}

# data to POST 
data = [
    {"dbms" : "aiops", "table" : "fic11", "value": 50, "timestamp": "2019-10-14T17:22:13.051101Z"},
    {"dbms" : "aiops", "table" : "fic16", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"},
    {"dbms" : "aiops", "table" : "ai_mv", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"}
]

# Convert to JSON 
jdata = json.dumps(data) 

# POST proces 
try:
    r = requests.post('http://%s' % conn, headers=headers, data=jdata)
except Exception as e: 
    print('Failed to POST data to %s (Error: %s)' % (conn, e))
else: 
    if r.status_code != 200: 
        print('Failed to POST data to %s due to network error: %s' % (conn, r.status_code))
    else:
        print('Success') 
```


## Subscribing to a third party message broker

Details are available at the [message broker section - Subscribing to a third party broker](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#subscribing-to-a-third-party-broker).

## Configuring the AnyLog node as a message broker

Details are available at the [message broker section - Configuring an AnyLog node as a message broker](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#configuring-an-anylog-node-as-a-message-broker).


## The Southbound Connectors Diagram

<pre>
                                                       --------------------------       --------------------------
  Option A:                                            |                        |       |                        |   
  Data published to external Broker                    |       MQTT Broker      |       |          Kafka         |   
  ------------------------------------------------>    |                        |       |                        |   
                                                       --------------------------       --------------------------
                                                                           |                   |
 ================================================================================================================
  AnyLog                                                                   |                   |
                                                                           V                   V
                                         -------------------            --------------------------
  Option B:                              |                 |            |                        |
  Data published to AnyLog Broker        |  AnyLog Broker  |  ------>   |      Broker Client     |
  ---------------------------------->    |                 |            |                        |
                                         -------------------            --------------------------
                                                                           |
                                                                           |
                                                                           V
                                                               -----------------
  Option C:                                                    |  Client Data  |
  Data transferred using POST                                  |  Mapper       |
  -------------------------------------------------------->    |  f(Topic)     |
                                                               -----------------
                                                                       |
                                                                       |
                                                                       V
                                                               -----------------        -----------------
  Option D:                                                    |               |        |  (Optional)   |
  Data transferred using PUT (without mapping)                 |  Data Buffers |   -->  |  Immediate    |
  -------------------------------------------------------->    |               |        |  DBMS update  |
                                                               -----------------        -----------------
                                                                       |
                                                                       |
                                                                       V
                                                               -----------------        -----------------
  Option E:                                                    |               |        |  (Optional)   |
  Adding JSON files to the watch directory                     |  JSON Files   |   -->  |  Archive      |
  -------------------------------------------------------->    |               |        |  JSON files   |
                                                               -----------------        -----------------
                                                                       |
                                                                       |
                                                                       V
                                                               -----------------        -----------------
  Option F:                                                    |               |        |  (Optional)   |
  Adding SQL files to the watch directory                      |  SQL Files    |   -->  |  Archive      |
  -------------------------------------------------------->    |               |        |  SQL files    |
                                                               -----------------        -----------------
                                                                       |
                                                                       |
                                                                       V
                                                               ----------------- 
                                                               |               |
                                                               |  DBMS Update  |
                                                               |               |
                                                               -----------------
                                                                       |
                                                                       |
                                                                       V
                                                               ----------------- 
                                                               |  (Optional)   |
                                                               |  TSD Update   |
                                                               |               |
                                                               -----------------
 
</pre>

The diagram describes the different southbound connectors options and the data flow.

***Option A: Data published to an external Broker***  

Data is published to an external broker. 
Example of brokers are: MQTT broker and Kafka.  
AnyLog client is registered to the broker and does the following:  
a) pulls the data from the broker and b) transfers the data to the mapper.  
Details are available at the [message broker section - Subscribing to a third party broker](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#subscribing-to-a-third-party-broker).

The following command provides status and statistics on the mapping of published messages on the external broker to the table's schema:
<pre>
get msg client
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-msg-clients).

***Option B: Data published to AnyLog as a Broker***  

An AnyLog node is configured as a local message broker and data is published to the AnyLog Node.  
AnyLog client is registered to the broker, and similarly to an external broker, pulls the data from the broker and
pushes to the mapper.  
Details are available at: [Configuring the AnyLog node as a message broker](#configuring-the-anylog-node-as-a-message-broker).

The following command provides status and statistics on data published on the AnyLog message broker process:
<pre>
get broker
</pre>

The following command provides status and statistics on the mapping (of published data on the local broker) to the table's schema:
<pre>
get msg client
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-msg-clients).

***Option C: Data transferred using POST***    

The data is transferred using REST POST messages. The headers include a topic (or if not provided, the default topic is used) 
and the AnyLog mapper transforms the received data to the destination format.  
Details are available at the section [Using a POST command](#using-a-post-command).

The following command provides status and statistics on HTTP POST messages:
<pre>
get rest calls
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-rest-calls).

The following command provides status and statistics on the mapping (of POST calls) to the table's schema:
<pre>
get msg client
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-msg-clients).

***Option D: Data transferred using PUT***    

The data is transferred using REST PUT messages. The data is provided in a format representative of the table's schema.  
Details are available at the section [Using a PUT command](#using-a-put-command).

The following command provides status and statistics on HTTP PUT messages:
<pre>
get rest calls
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-rest-calls). 

***Monitoring the data passing through the internal buffers***

The following command provides status and statistics on the internal buffers:
<pre>
get streaming
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-streaming).


***Option E: Adding JSON files to the watch directory***   

The JSON files are in a format representative of the table's schema and the file names follow the naming convention.  
Details are available at the section [Placing data in the WATCH directory](#placing-data-in-the-watch-directory).  
File naming convention is detailed at [Managing Data files](https://github.com/AnyLog-co/documentation/blob/master/managing%20data%20files%20status.md).

The following command provides status and statistics on the processing of the JSON files:
<pre>
get operator
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-operator).

***Option F: Adding SQL files to the watch directory***   

The SQL files are in a format representative of the table's schema and the file names follow the naming convention.  
Details are available at the section [Placing data in the WATCH directory](#placing-data-in-the-watch-directory).

The following command provides status and statistics on the processing of the SQL files:
<pre>
get operator
</pre>
Command details are available [here](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-operator).
