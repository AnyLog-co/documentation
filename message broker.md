# Using a Message Broker

There are 3 ways to configure a node:
* As a [subscriber to a third party message broker](#subscribing-to-a-third-party-broker)
* As a [message broker](#configuring-an-anylog-node-as-a-message-broker) - receiving published data from a client using standard APIs like MQTT.
* As a [broker receiving REST commands](#anylog-as-a-broker-receiving-rest-commands) and mapping the data to the needed schema based on the provided topic.

In both cases, user are able to do the following:

* Users can subscribe and retrieve data from one or more topics in a  broker.
* Users can publish data to a topic  in a broker.

# Subscribing to a third party broker

This process initiates a client that subscribes to a list of topics registered on a MQTT broker.      
When a new message is added to the broker and associated with the subscribed topic, the broker will push the message to the AnyLog instance.        
On the AnyLog instance, messages are mapped to JSON structures and aggregated to files that are treated according to the configuration of the node. For example, the data can be ingested to a local database or send to a different node.    
The message data on the AnyLog instance is treated as ***streaming data***, this process is explained at [File Mode and Ssreaming Mode](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#file-mode-and-streaming-mode).

## The command structure
<pre>
run mqtt client where [list of options]
</pre>
The list of options are represented by key = value' pairs and separated by an 'and'. 
Providing the ***broker*** value is mandatory. ALl the other fields are optional depending on the broker setting and how the messages need to be processed.       
The details of the topic are enclosed in parentheses and the MQTT client declared on the command line could subscribe to multiple topics.    
The command format with subscriptions to multiple topics is as follows:  
<pre>
run mqtt client where [connection parameters] and [Config parameters] and topic = (topic 1 params) and topic = (topic 2 params) .... 
</pre>

The subscription details of each topic are enclosed in the parenthesis and include 3 types of parameters:    
1. Connection Params - providing the information that allows to connect to the broker.  
2. Config Params - Configuration parameters that apply to all messages regardless of the subscribed topic.  
3. Topic Params - Include the topic name and the rules of how to map the message such that it can be processed by the AnyLog node.  
  

## The connection params  

To connect to a broker, the broker URL is mandatory and the rest depends on the type of broker and the way the broker is configured.  
  
| Option        | Details   |
| ------------- | ------------- | 
| broker  | The url or IP of the broker. |
| port  | The port of the broker. The default value is 1883.|
| user  | The name of the authorized user. |
| password  | The password associated with the user. |
| client_id  | A client ID associated with the account. |
| project_id  | A project ID associated with the broker account. |
| location  | A name identifying the service location. |
| private_key  | A private key to authenticate requests. |

## The Config params

The Config Params provide configuration parameters and can modify the default settings.
  
| Option        | Details   |
| ------------- | ------------- | 
| log  | A true/false value to output the broker log messages. |
| log_error | A true value enables a log file for messages that were not successfully processed. |
| qos  | The Quality of Service. The default value is 0. |
| prep_dir  | The location of a directory to organize the incomming message data. |
| watch_dir  | The location of the watch directory. |
| err_dir  |The location of the error directory. |

## The topic params

The topic params are specified within parenthesis and determine the topic name and how to process the message data.  
The interpretation of the data associated with the topic needs to extract the following:    
The name of the dbms that contains the data, the name of the table that contains the data and the data itself.  
The following params are provided for each topic:  
  
| Option        | Details   |
| ------------- | ------------- | 
| name  | The topic name to which the process subscribes. |
| qos  | The Quality of Service, if omitted, the value provided in the the Config Params is used (or, if not available, the default value). |
| dbms  | The logical DBMS that contains the topic's data or a ***'bring' command*** to extract the dbms name. |
| table  | The name of the table to contain the data or a ***'bring' command*** to extract the table name. |
| column.name.type  | The column name and column type that is associated with the data extracted from the message. The column is associated with the ***'bring' command*** that details the rule to extract the column data. |

## QoS - The Quality of Service:      
0 - No guarantee of delivery. The recipient does not acknowledge receipt of the message. The ) value serves as the default value.
1 - Guarantees that a message is delivered at least one time to the receiver, but the same message may be delivered multiple times.  
2 - The highest level of service. Guarantees that each message is received only once by the client.

## Bring Command
  
The ***bring command*** is an AnyLog command that extracts data from a JSON structure.   
The message data is structured in JSON and the ***bring command*** is applied to the message to retrieve the needed data.  
The ***bring command*** is used in the same way it is being used in the blockchain commands.    
The command usage is explained at: [JSON Data Transformation](https://github.com/AnyLog-co/documentation/blob/master/json%20data%20transformation.md#json-data-transformation).  

***Mapping the message data***  
Values pulled from the message determine the database, table, columns and the columns values to update. 
The parameters provided in the ***run mqtt client*** command, declares, for each subscribed topic, how to retrieve the needed values.    
The chart below summarizes the information extracted from each message:

| Name        | Details   | Command Structure |  Comments |
| ------------- | ------------- | ---- |----|
| dbms  | The dbms to contain the data. | ***dbms = value*** or ***dbms = [bring command]***| Uppercase letters are replaced to lowercase and space is replaced by underscore |
| table  | Determine the table to contain the data. |  ***table = value*** or ***table = [bring command]***| Uppercase letters are replaced to lowercase and space is replaced by underscore |
| column  | Multiple column names are assigned with their value. | ***column.[column name].[data_type] = [bring command]*** | |

***Retrieving column values***  
The columns values pulled from the message are assigned to a new JSON structure which is the structure that creates and updates the database tables.  
The format declaring the columns and their values is the following:
<pre>
column.[column name].[data type] = [bring command]
</pre> 
***column name*** - The name of the column that is used in the database table.    
***data type*** - The data type to use. Supported data types are the following: ***str, int, float, timestamp, bool***.  


***Associating column names with data types and data***  
The ***column.name.type*** groups the following:   
* A column in a table by referencing the column name  
* A data type that is associated with the column  
* A bring command that details how to extract the column data from the source data.  
There are 2 ways to detail the association:  
  1.  identify column name and data type with the bring command and expressed as follows:
    <pre>
    column.[column name].[column type] = [bring command]
    </pre> 
    In the example below, the column **value** is assigned with a float data type and is associated with data retrieved from the source data using the bring command.   
    <pre>
    column.value.float = "bring [readings][][value]"
    </pre> 
  2. identify a column name. The column type and the value are retrieved from the source data using the bring command and expressed as follows:
    <pre>
    column.[column name] = (value = [bring command] and type = [bring command])
    </pre> 
    In the example below, the column **value** is associated with data type and value retrieved from the source data:   
    <pre>
    column.value = (value="bring [readings][][value]" and type="bring [readings][][valueType]")
    </pre> 
    
By default, an error is returns if the bring command does not return a value.  
The keyword ***optional*** assigned to ***true*** designates that if the bring command fails, the process continues without returning an error.  
Example:
    <pre>
    column.info=(type=str and value="bring [info]" and optional=true)
    </pre> 

***Examples - associating published data with the needed schema***

Example 1 - assigning the name ***machines_data*** as the database name:
<pre>
dbms = machines_data
</pre> 
Example 2 - retrieving the machine name and the serial number from the message as the table name:
<pre>
table = "bring [metadata][machine_name] _ [metadata][serial_number]"
</pre> 
Example 3 - retrieving the timestamp and value from the message and mapping the retrieved values to columns in the table.
<pre>
column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]"
</pre> 


A complete example is provided [below](#example).

## Processing messages and terminating a subscription

***Processing Messages***  
* Messages are assumed to be in JSON format and when pushed to an AnyLog node, are transformed to a new JSON structure that can be processed to be included by a target table.  
* Executing ***run mqtt client*** command dedicates a thread (***client*** to the MQTT broker) to process subscribed messages. 
Multiple calls to ***run mqtt client*** dedicates a multiple threads and each thread is processing the topics on the command line.    
* Each of these threads is identified by a unique ID. Use the ***get*** command detailed below to view the ID associated to each client.

***Configuring work directories***    
The MQTT messages are transformed to files which are processed according to the node configuration. These files can update local databases or transferred to peers in the network.    
The processing of the data requires the identification of 3 directories - prep_dir, watch_dir and err_dir.  
Unless modified on the command line, the default locations are used. The command ```get dictionary``` details the path associated to each directory.         

***Setting Buffers Thresholds***  
When a message is processed, it is placed in the AnyLog internal buffers. Multiple messages that update the same table are organized as a JSON file that is placed in the designated directory for processing.    
The amount of data in each file depends on thresholds based on time and file size.  
The time thresholds are enforced by the ***Streaming*** process. To enable the streaming process execute the following command:
<pre>
run streamer 
</pre> 
More information on the Streamer process is available at the [Streamer Process](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#streamer-process) section.  
Setting and viewing the thresholds is explained at [Setting and retrieving thresholds for a Streaming Mode](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#setting-and-retrieving-thresholds-for-a-streaming-mode).      
By default, the node assigns the value 60 seconds to the time threshold and 10,000 bytes to the volume threshold.  

***Terminating Clients***  
* To terminate all the MQTT clients use the command: 
<pre>
exit mqtt
</pre>
* To terminate a particular client use the command (***n*** is the client ID):
<pre>
exit mqtt [n]
</pre>

### View client status
  
* To view status and configuration of all clients use the following command:
<pre>
get msg clients
</pre>    
* To view the status and configuration of a particular client use the command (***n*** is the client ID): 
<pre>
get msg client [n]
</pre>
* To view statistics per topic of all clients use the following command:
<pre>
get msg clients statistics
</pre>    
* To view statistics per each topic of a particular client use the command (***n*** is the client ID): 
<pre>
get msg client statistics [n]
</pre>
* To view the streaming data status, use the following command:
<pre>
get streaming
</pre>    

### View registered brokers
Users can see the list of brokers and the subscribed users and topics in each broker using the command:
<pre>
get msg brokers
</pre>

### View summary of AnyLog processes as a local broker
Users can see the summary of messages processed on ANyLog as a broker using the following command:
<pre>
get broker
</pre>


### Example
The example below connects to a broker to pull data assigned to a topic.
<pre>
run mqtt client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = (name = test and dbms = "bring [metadata][company]" and table = "bring [metadata][machine_name] _ [metadata][serial_number]" and column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]")
</pre>


## Publishing

Users can publish a message to a particular topic in a broker using the following command:  
<pre>
mqtt publish where broker = [url] and port = [port value] and user = [user name]  and password = [password name] and topic = [topic] and qos = [value] and message = [published message]
</pre>

Example:  
Publishing "Hellow World" to a broker:
<pre>
mqtt publish where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = test and message = "hello world"
</pre>

## Debugging

Debug provides the means to track the processing of messages by enabling the following:
* Display of the MQTT processing and calls.
* Display of the messages being processed.
* Flushing source messages.
* Updating a log file with messages that were not successfully processed.
* Subscribing to all topics.

#### Display of the MQTT processing and calls
Users are able to enable the MQTT ***on_log()*** callback and display the MQTT log.  
Enabling the on_log() callback is done on the  ***run mqtt client*** call with the ```log = true``` option.  
Example:
<pre>
run mqtt client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and log = true and topic = (name = test and dbms = "bring [metadata][company]" and table = "bring [metadata][machine_name] _ [metadata][serial_number]" and column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]")
</pre>

#### Display of the messages being processed
Users are able to display the incoming messages using the following command:
<pre>
set mqtt debug [on/off]
</pre>
* on - Sends incoming messages and the processing status to the stdout.
* off - disables the debug functionality.

#### Flushing source messages
Users are able to disable the AnyLog processing and flush incomming messages to files.  
The name of the file is based on the broker ID and the topic associated with the message.    
The following example subscribes to the topic ***anylog*** and writes all the incoming messages to a file in the watch directory.    
<pre>
run mqtt client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = anylog
</pre>

#### Updating a log file with messages that were not successfully processed
By setting the log_error option to true, messages that were not successfully processed will be written to a log file.  
The name of the file starts with "err_" and extended by the broker ID and the topic associated with the message.  
The log file is written to the error directory.  
Example:  
<pre>
run mqtt client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and log_error = true and topic = (name = test and dbms = "bring [metadata][company]" and table = "bring [metadata][machine_name] _ [metadata][serial_number]" and column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]")
</pre>

####  Subscribing to all topics
By setting the topic to the pound sign (#), all published messages are considered such that:    
If the topic is defined - the message is processed according to the subscription definitions.  
If the topic is not defiled, the message is flushed to a log file.  
Example:  
<pre>
run mqtt client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = "#"
</pre>


## Demo - Subscribe and Publish

This demo publishes and subscribes to a topic called ***test*** on a MQTT managed services at [https://www.cloudmqtt.com](https://www.cloudmqtt.com/).  
CloudMQTT are managed Mosquitto servers in the cloud. Mosquitto implements the MQ Telemetry Transport protocol, MQTT, which provides lightweight methods of carrying out messaging using a publish/subscribe message queueing model.  

### Enable the streamer process:
<pre>
run streamer 
</pre> 
Info on the ***run streamer*** command is available in the [Streamer Process](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#streamer-process) in the ***Background Processes" section.

### Subscribing to the topic:

<pre>
run mqtt client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = (name = test and dbms = "bring [metadata][company]" and table = "bring [metadata][machine_name] _ [metadata][serial_number]" and column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]")
</pre>

### Publishing time series data event to a broker:

***Define a message***  
```
<message = {"value":210,
            "ts":1607959427550,
            "protocol":"modbus",
            "measurement":"temp02",
            "metadata":{
                    "company":"Anylog",
                    "machine_name":"cutter 23",
                    "serial_number":"1234567890"}}>
```
***Publish the message***  
<pre>
mqtt publish where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = test and message = !message
</pre>

### View all client status  
<pre>
get msg clients
</pre>    

To view the ***Streaming Data*** buffers state use the following command:
<pre>
get streaming
</pre>   

### View registered brokers
<pre>
get msg brokers
</pre>
 

# Configuring an AnyLog node as a message broker

By enabling the AnyLog [Message Broker](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#message-broker) functionality on a particular node, 
the AnyLog node can serve as an MQTT Broker. A detailed example is available in the [Using Edgex](https://github.com/AnyLog-co/documentation/blob/master/using%20edgex.md#using-edgex) section.

Any AnyLog node can be configured with a [Message Broker](https://en.wikipedia.org/wiki/Message_broker) functionality.  
By configuring a node as message broker, data can be transferred from a client to an AnyLog node without dependency on a third party message broker platform.  

The process of using an AnyLog node as a message broker is similar to the process of using a third party message broker and is as follows:
* Configuring an AnyLog node as a message broker
* Subscribing to the published topics and mapping the data to the needed schema - this process is using the same command options as the [Subscribing to a third party broker](#subscribing0-to-a-third-party-broker) process.
* The [Streamer Process](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#streamer-process) needs to be enabled.

A detailed configuration example is available in the examples section - [Broker Setup](examples/Broker%20Setup.md#setting-anylog-as-a-message-broker).

## The message broker configuration

The AnyLog node serving as the broker is configured as follows:
<pre>
run message broker [ip] [port] [local ip] [Local port] [threads]
</pre>
Details on the the ***run message broker*** command are available at the [Message Broker](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#message-broker)
section in the [Background Processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#background-processes) document.

## Subscription to topics published on the AnyLog node
Subscribe to topics assigned to messages received on the broker and detail the mapping of the messages to the needed structure.  
This process is identical to the  [Subscribing to a third party broker](#subscribing-to-a-third-party-broker) 
  whereas rather than specifying an IP and Port of the 3rd party broker, the broker is identified by the keyword ***local***.  

usage:
<pre>
run mqtt client where broker = local and [Config parameters] and topic = (topic 1 params) and topic = (topic 2 params) .... 
</pre>


## Example:

### Init an AnyLog node as a broker
<pre>
run message broker !external_ip 7850 !ip 7850 6
</pre>

### Subscribe to a topic and provide data mapping instructions
<pre>
run mqtt client where broker = local and user = mqwdtklv and password = uRimssLO4dIo and topic = (name = test and dbms = "bring [metadata][company]" and table = "bring [metadata][machine_name] _ [metadata][serial_number]" and column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]")
</pre>
Note: the key value pair ***broker=local*** replace the assignment of an IP and port (when 3rd parties brokers are used).    

Use the following command to view messages processed on AnyLog as a broker:
<pre>
get broker
</pre>

### Publish a message on the AnyLog node 
***Define a message***  
```
<message = {"value":210,
            "ts":1607959427550,
            "protocol":"modbus",
            "measurement":"temp02",
            "metadata":{
                    "company":"Anylog",
                    "machine_name":"cutter 23",
                    "serial_number":"1234567890"}}>
```
***Publish the message***  
<pre>
mqtt publish where broker = !ip and port = 7850 and user = mqwdtklv and password = uRimssLO4dIo and topic = test and message = !message
</pre>

# AnyLog as a broker receiving REST commands 

This option allows mapping of data streamed to AnyLog using the REST API to the needed schema based on a provided topic.
This option requires 2 special settings:  
1) The subscription identifies the key ***broker*** by the value ***rest***. Data delivered to the REST server using POST command will be mapped as defined in the topic assignment.
2) The target API is identified using the ***user-agent*** keyword, for example: ***user-agent=anylog*** will deliver the call to the AnyLog native process.

## Subscription to topics published on the AnyLog node
Usage:
<pre>
run mqtt client where broker = rest and user-agent = [detination API] and [Config parameters] and topic = (topic 1 params) and topic = (topic 2 params) .... 
</pre>
Note: the key value pair ***broker=rest*** replaces the assignment of an IP and port (when 3rd parties brokers are used).    

## Example

### Subscribe to a topic and provide data mapping instructions
<pre>
run mqtt client where broker = rest and user-agent=anylog and user = mqwdtklv and password = uRimssLO4dIo and topic = (name = test and dbms = "bring [metadata][company]" and table = "bring [metadata][machine_name] _ [metadata][serial_number]" and column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]")
</pre>

### Publish data using REST
curl --location --request POST '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: data' \
--header 'topic: test' \
--header 'Content-Type: text/plain' \
--data-raw '[{"value":210,
            "ts":1607959427550,
            "protocol":"modbus",
            "measurement":"temp02",
            "metadata":{
                    "company":"Anylog",
                    "machine_name":"cutter 23",
                    "serial_number":"1234567890"}},
{"value":210,
            "ts":1607959427550,
            "protocol":"modbus",
            "measurement":"temp02",
            "metadata":{
                    "company":"Anylog",
                    "machine_name":"cutter 23",
                    "serial_number":"1234567890"}}

]'

## Debugging the POST commands
Users can enable trace to debug the POST calls.  
The following command displays (on the AnyLog REST server) the REST command issued by a client.
<pre>
trace level = 1 run rest server 
</pre>

The following command displays (on the AnyLog REST server) the REST command issued by a client including the header and the message body.
<pre>
trace level = 2 run rest server 
</pre>
