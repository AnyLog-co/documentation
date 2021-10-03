# Using a Message Broker

There are 2 ways to configure a node:
* As a [subscriber to a third party message broker](#subscribing-to-a-third-party-broker)
* As a [message broker](#configuring-an-anylog-node-as-a-message-broker)

In both cases, user are are able to do the following:

* Users can subscribe and retrieve data from one or more topics in a  broker.
* Users can publish data to a topic  in a broker.

# Subscribing to a third party broker

This process initiates a client that subscribes to a list of topics registered on a MQTT broker.      
When a new message is added to the broker and associated with the subscribed topic, the broker will push the message to the AnyLog instance.        
On the AnyLog instance, messages are mapped to JSON structures and aggregated to files that are treated according to the configuration of the node. For example, the data can be ingested to a local database or send to a different node.    
The message data on the AnyLog instance is treated as ***streaming data***, this process is explained at [File Mode and Ssreaming Mode](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#file-mode-and-streaming-mode).

***The command structure***
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
  

***The connection params***  

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

***The Config params***

The Config Params provide configuration parameters and can modify the default settings.
  
| Option        | Details   |
| ------------- | ------------- | 
| log  | A true/false value to output the broker log messages. |
| log_error | A true value enables a log file for messages that were not successfully processed. |
| qos  | The Quality of Service. The default value is 0. |
| prep_dir  | The location of a directory to organize the incomming message data. |
| watch_dir  | The location of the watch directory. |
| err_dir  |The location of the error directory. |

***The topic params***  
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

***QoS*** - The Quality of Service:      
0 - No guarantee of delivery. The recipient does not acknowledge receipt of the message. The ) value serves as the default value.
1 - Guarantees that a message is delivered at least one time to the receiver, but the same message may be delivered multiple times.  
2 - The highest level of service. Guarantees that each message is received only once by the client.

***Bring Command***  
The ***bring command*** is an AnyLog command that extracts data from a JSON structure.   
The message data is structured in JSON and the ***bring command*** is applied to the message to retrieve the needed data.  
The ***bring command*** is used in the same way it is being used in the blockchain commands.    
The command usage is explained at: [The 'From JSON Object Bring' command](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#the-from-json-object-bring-command).  

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

### Processing messages and terminating a subscription

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
  
* To view status of all clients use the following command:
<pre>
get mqtt clients
</pre>    
* To view the status of a particular client use the command (***n*** is the client ID): 
<pre>
get mqtt client [n]
</pre>
* To view the streaming data status, use the following command:
<pre>
get streaming
</pre>    

### View registered brokers
Users can see the list of brokers and the subscribed users and topics in each broker using the command:
<pre>
get mqtt brokers
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
get mqtt clients
</pre>    

To view the ***Streaming Data*** buffers state use the following command:
<pre>
get streaming
</pre>   

### View registered brokers
<pre>
get mqtt brokers
</pre>
 

# Configuring an AnyLog node as a message broker

By enabling the AnyLog [Message Broker](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#message-broker) functionality on a particular node, 
the AnyLog node can serve as an MQTT Broker. A detailed example is available in the [Using Edgex](https://github.com/AnyLog-co/documentation/blob/master/using%20edgex.md#using-edgex) section.


Any AnyLog node can be configured with a [Message Broker](https://en.wikipedia.org/wiki/Message_broker) functionality.  
By configuring a node as message broker, data can be delivered from a client directly to AnyLog without the need to of a third party message broker platform.


The AnyLog node receiving the data needs to be configured as follows:

* Enable the ***Message Broker*** functionality:   
Usage:
<pre>
run message broker [ip] [port] [local ip] [Local port] [threads]
</pre>
Details on the the ***run message broker*** command are available at the [Message Broker](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#message-broker)
section in the [Background Processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#background-processes) document.

* Subscribe to topics assigned to messages received on the broker and detail the mapping of the messages to the needed structure.  
This process is identical to the [subscription process to 3rd parties MQTT brokers](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md#subscribing-to-a-broker) 
  whereas rather than specifying an IP and Port of the 3rd party broker, the broker is identified by the keyword ***local***.  

* Add the data and associate the data with a topic assigned to the broker.  


### Example:

#### Init a broker
<pre>
run message broker !external_ip 7850 !ip 7850 6
</pre>

#### Define topic and data mapping instructions
<pre>
run mqtt client where broker = local and user-agent=python and topic=(name="test" and dbms="foglamp" and table=weather and column.timestamp.timestamp="bring [timestamp]" and column.city.str="bring [reading][city]" and column.wind_speed.float="bring [reading][wind_speed]" and column.temperature.float="bring [reading][temperature]" and column.humidity.int="bring [reading][humidity]")
</pre>
Note: the key value pair ***broker=local*** replace the assignment of an IP and port (when 3rd parties brokers are used).    
Details on the ***run mqtt client*** command, and the data mapping instructions are available at the [Subscribing to a Broker](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md#subscribing-to-a-broker) section.  

#### Publish data to the broker
curl --location --request POST '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: data' \
--header 'Content-Type: text/plain' \
--header 'topic: anylog' 
--data-raw ' [{"dbms" : "dmci", "table" : "fic11", "value": 50, "ts": "2019-10-14T17:22:13.051101Z"},
 {"dbms" : "dmci", "table" : "fic16", "value": 501, "ts": "2019-10-14T17:22:13.050101Z"},
 {"dbms" : "dmci", "table" : "ai_mv", "value": 501, "ts": "2019-10-14T17:22:13.050101Z"}]'