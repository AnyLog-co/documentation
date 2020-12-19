# Using MQTT Broker

Users can subscribe and retrieve data from one or more topics in a MQTT broker.
Users can publish data to a topic  in a broker.

## Subscribing to a broker

This process initiates a client that subscribes to a list of topics registered on a MQTT broker.      
When a new message is added to the broker and associated with the subscribed topic, the broker will push the message to the AnyLog instance.        
On the AnyLog instance, messages are mapped to JSON structures and aggregated to files that are treated according to the configuration of the node.      
For example, the data can be ingested to a local database or send to a different node.    
The message data on the nNyLog instance is treated as ***streaming data***, this process is explained at [File Mode and STreaming Mode](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#file-mode-and-streaming-mode).

***The command structure***
<pre>
run mqtt client where [list of options]
</pre>
The list of options are represented by 'key' = value' and separated by 'and'. 
Providing the ***broker*** value is mandatory. ALl the other fields are optional depending on the broker setting.     
The details of the topic are enclosed in brackets and the MQTT client process could subscribe to multiple topics.  
The command format with subscriptions to multiple topics is as follows:  
<pre>
run mqtt client where [connection parameters] and [generic parameters] and topic = [topic 1 params] and topic = [topic 2 params] .... 
</pre>

To subscribe to one or more topics, 3 types of parameters needs to be provided:  
1. Connection Params - providing the information that allows to connect to the broker.  
2. Generic Params - Configuration parameters that apply to messages regardless of the subscribed topic.  
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

***The generic params***

The generic params provide configuration parameters and can modify the default settings.
  
| Option        | Details   |
| ------------- | ------------- | 
| log  | A true/false value to output the broker log messages. |
| qos  | The quality of service. THe default value is 0. |
| prep_dir  | The location of a directory to organize the incomming message data. |
| watch_dir  | The location of the watch directory. |
| err_dir  |The location of the error directory. |

***The topic params***
The topic params are specified within brackets and determine the topic name and how to process the message data.  
The interpretation of the data associated with the topic needs to extract the following:    
The name of the dbms that contains the data, the name of the table that contains the data and the data itself.  
The following params can be detailed for each topic:  
  
| Option        | Details   |
| ------------- | ------------- | 
| name  | The topic name to which the process subscribes. |
| qos  | The Quality of Service, if omitted, the value provided in the the generic params is used (or, if not available, the default value). |
| dbms  | The logical DBMS that contains the topic's data or a 'bring' command to extract the dbms name. |
| table  | The name of the table to contain the data or a 'bring' command to extract the table name. |
| column.name.type  | The column name of the data to extract from the message, the data type and the 'bring' command' to extract the column data. |

***QoC*** - The Quality of Service:      
0 - No guarantee of delivery. The recipient does not acknowledge receipt of the message.  
1 - Guarantees that a message is delivered at least one time to the receiver, but the same message may be delivered multiple times.  
2 - The highest level of service. Guarantees that each message is received only once by the client.  

***Bring Command***  
An AnyLog command that extracts data from a JSON structure. 
The message data is structured in JSON and the ***bring command*** is applied to the message to retrieve the needed data.  
The ***bring command*** is expressed and processed in the same way it is being expressed and used in the blockchain commands.  
The command usage is explained at: [The 'From JSON Object Bring' command](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md#the-from-json-object-bring-command).

### Processing messages and terminating a subscription
* Messages are assumed to be in JSON format and when pushed to an AnyLog node, are transformed to a new JSON structure that can be processed to be included by a target table.
* Executing ***run mqtt client*** dedicates a thread (client) to process subscribed messages. Every call to ***run mqtt client*** dedicates a new thread to process the detailed topics. Each thread is identified by a unique id.  
* To view status of each processing thread information use the ```show mqtt clients``` command.   
* To view the status of a particular client use the command: ``show mqtt client [n]``` whereas ***n*** is the client id.
* To terminate all the MQTT clients use the command: 
<pre>
exit mqtt
</pre>
* To terminate a particular client use the command:
<pre>
exit mqtt [n]
</pre>
***n*** is the client id.
 
### Example:  
The example below connects to a broker to pull data assigned to a topic.
<pre>
run mqtt client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = (name = test and dbms = "bring [metadata][company]" and table = "bring [metadata][machine_name] _ [metadata][serial_number]" and column.timestamp.timestamp = "bring [ts]" and column.value.int = "bring [value]")
</pre>

## Publishing

Users can publish a message to a particular topic in a broker using the following command:  
<pre>
mqtt publish where broker = [url] and topic = [topic]
</pre>

Example:  
Publishing "Hellow World" to a broker:
<pre>
mqtt publish where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = test and message = "hello world"
</pre>

## Demo - Subscribe and Publish

This demo publishes and subscribes to a topic called ***anylog*** on a MQTT managed services at [https://www.cloudmqtt.com](https://www.cloudmqtt.com/).  
CloudMQTT are managed Mosquitto servers in the cloud. Mosquitto implements the MQ Telemetry Transport protocol, MQTT, which provides lightweight methods of carrying out messaging using a publish/subscribe message queueing model.  

### Subscribing to the topic is using the following command:

<pre>
run mqtt client where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = (name = test and dbms = lsl_demo and table =ping_sensor and qos = 1)
</pre>

### Publishing time series data event to a broker:
```


<message = {"value":210,
            "ts":1607959427550,
            "protocol":"modbus",
            "measurement":"temp02",
            "metadata":{
                    "company":"Anylog",
                    "machine_name":"cutter 23",
                    "serial_number":"1234567890"}}>


mqtt publish where broker = "driver.cloudmqtt.com" and port = 18975 and user = mqwdtklv and password = uRimssLO4dIo and topic = test and message = !message

```

