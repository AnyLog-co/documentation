# Streaming Data into AnyLog 

The following provides insight into sending data into AnyLog via a message broker. 

**Other Documents**
* [Basic Data Generator](Data%20Generator.md) - How to utilize the generic data generator
* [Examples of Streaming Data into AnyLog](../examples/Streaming%20Data%20into%20AnyLog.md) - Examples of sending data into AnyLog 
* [Understanding Message Broker](../background%20processes.md#message-broker)
* [Message Broker](../message%20broker.md)

## Third-Party MQTT Client 
AnyLog can accept data from third-party message brokers - such as CloudMQTT, Eclipse Mosquitto and Kafka. 

In order to process data from message broker, users must specify the mapping between the data coming in, and how it'll 
be stored on Operator node(s). The following example accepts data from an active CloudMQTT broker with data coming in via
an EdgeX process. 

The data coming in will generate 4 tables (lightout1, lightout2, lightout3, lightout4) and will be stored in physical 
database "test".  

* MQTT Call 
```anylog
broker = driver.cloudmqtt.com
port = 18785
user = ibglowct
password = MSY4e009J7ts
mqtt_logs = false 
db_name=test 
<run mqtt client where broker=!broker and port=!port and user=!user and password=!password and log=!mqtt_log  and topic=(
    name=anylogedgex-demo and 
    dbms=!db_name and 
    table="bring [sourceName]" and 
    column.timestamp.timestamp=now and 
    column.value.float="bring [readings][][value]"
)>	
```

* Sample Data coming in 
```json
{
  "apiVersion":"v2",
  "id":"7555df69-2e5d-4777-a438-cb191935eeae",
  "deviceName":"lighting",
  "profileName":"LIGHTING_ANYLOG",
  "sourceName":"LIGHTOUT2",
  "origin":1691017298310934496,
  "readings":[
      {
        "id":"4f68a700-74b3-4b14-90fa-a764d56e5e00",
        "origin":1691017298310934496,
        "deviceName":"lighting",
        "resourceName":"LIGHTOUT2",
        "profileName":"LIGHTING_ANYLOG",
        "valueType":"Int16",
        "value":"1"
      }
  ]
}	
```

## Local MQTT broker 
An AnyLog node can act as its own message broker. In order for that to happen 2 services should be running: 
1. A local running message broker on the AnyLog node 
2. A MQTT client against the local broker for data to be mapped with

### Connecting to a Local Message Broker
**How to Connect to a local Message Broker**: 
```anylog
anylog_broker_port=32150 
broker_bind = false 
broker_threads = 3

<run message broker where
    external_ip=!external_ip and 
    external_port=!anylog_broker_port and
    internal_ip=!ip and 
    internal_port=!anylog_broker_port and
    bind=!broker_bind and 
    threads=!broker_threads>
```

**Validate local Message Broker is running**: 
* Prior to running `run message broker`, notice that only _TCP_ and _REST_ connections are configured 
```anylog
AL anylog-operator_1 > get connections

Type      External Address    Internal Address    Bind Address        
---------|-------------------|-------------------|-------------------|
TCP      |198.74.50.131:32148|198.74.50.131:32148|198.74.50.131:32148|
REST     |198.74.50.131:32149|198.74.50.131:32149|0.0.0.0:32149      |
Messaging|Not declared       |Not declared       |Not declared       |
```
* After running `run message broker`, notice that not only are _TCP_ and _REST_ connections are configured, but also _Messaging_ is configured.  
```anylog
AL anylog-operator_1 > get connections

Type      External Address    Internal Address    Bind Address        
---------|-------------------|-------------------|-------------------|
TCP      |198.74.50.131:32148|198.74.50.131:32148|198.74.50.131:32148|
REST     |198.74.50.131:32149|198.74.50.131:32149|0.0.0.0:32149      |
Messaging|198.74.50.131:32150|198.74.50.131:32150|0.0.0.0:32150      |
```
