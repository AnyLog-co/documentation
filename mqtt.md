# Using MQTT Broker

Users can subscribe and retrieve data from one or more topics in a MQTT broker.
Users can publish data to a topic  in a broker.

## Subscribing to a broker

This process initiates a client that subscribes to a list of topics registered on a MQTT broker.

<pre>
run mqtt client where [list of options]
</pre>
The list of options are represented by 'key' = value' and separated by 'and'. 
Providing the ***broker*** value is mandatory. ALl the other fields are optional depending on the broker setting.   
The details of the topic are enclosed in brackets and the command could subscribe to multiple topics.  
Options:  
| Option        | Explanation   |
| ------------- | ------------- | 
| broker  | The url or IP of the broker. |
| port  | The port of the broker. The default value is 1883.|
| topic  | The topic name, the AnyLog dbms and table to use for each topic's data and the Quality of Service requested. |
| user  | The name of the authorized user. |
| password  | The password associated with the user. |
| log  | A true/false value to output the broker log messages. |
| project_id  | A project ID associated with the broker account. |
| client_id  | A client ID associated with the account. |
| location  | A name identifying the service location. |
| private_key  | A private key to authenticate requests. |


The MQTT command can include multiple topics whereas each topic and the database and table assigned to host the data, and the QoS are described using the following format:    
 (name = [topic name] and dbms = [dbms name] and table = [table name] and qos = [value]).

***name*** - The topic name to which the process subscribes.  
***dbms*** - The logical DBMS that contains the topic's data.  
***table*** - The name of the table to contain the data.  
***QoC*** - The Quality of Service:    
0 - No guarantee of delivery. The recipient does not acknowledge receipt of the message.  
1 - Guarantees that a message is delivered at least one time to the receiver, but the same message may be delivered multiple times.  
2 - The highest level of service. Guarantees that each message is received only once by the client.  

 
Example:  
The example below connects to a broker to pull data assigned to a topic ***ping*** and associate the data to the DBMS ***lsl_demo*** and the ***ping_sensor*** table.
<pre>
run mqtt client where broker = "mqtt.eclipseprojects.io" and topic = (name = $SYS/# and dbms = lsl_demo and table =ping_sensot and qos = 2)
run mqtt client where broker = "mqtt.googleapis.com" and client_id = "114497471765763749456" and project_id = "sound-micron-297304" and topic = (name = $SYS/# and dbms = lsl_demo and table =ping_sensor and qos = 1)
</pre>

Executing ***run mqtt client*** dedicates a thread to process subscribed messages. To terminate the thread process use the command:
<pre>
exit mqtt
</pre>

To determine the state of the processing use the command:
<pre>
show mqtt client
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

