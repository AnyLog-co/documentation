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

### Publishing to Message Broker 
Like with a third-party broker, the AnyLog node needs a `mqtt client` associated with the local message broker. The example 
below uses the same data as our [data generator](Data%20Generator.md), but uses a local MQTT client to send data into the 
AnyLog node, rather than REST _PUT_. 

**Set Message Client**
```anylog
broker = local
anylog_broker_port = 32150 
mqtt_logs = false 
topic_name = ping-percentage
<run mqtt client where broker=!broker and port=!anylog_broker_port and user-agent=anylog and log=!mqtt_log and topic=(
    name=!topic_name and
    dbms="bring [dbms]" and
    table="bring [table]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.device_name.str="bring [device_name]" and
    column.parentelement.str="bring [parentelement]" and
    column.webid.str="bring [webid]" and
    column.value.float="bring [value]"
)> 
```

**Sending Data** - make sure to update **CONN** to your MQTT IP + Port 
* -d – detach mode
* --name – docker running container name 
* --network (host) – connect container to the internet 
* --rm – remove container when finished 
 
```shell
docker run -d --name data-generator --network host \
   -e DATA_TYPE=ping,percentagecpu \
   -e INSERT_PROCESS=mqtt \
   -e DB_NAME=test \
   -e TOTAL_ROWS=100 \
   -e BATCH_SIZE=10 \
   -e SLEEP=1 \
   -e CONN=127.0.0.1:32150 \
   -e TOPIC=ping-percentage \
   -e TIMEZONE=utc \
--rm anylogco/sample-data-generator:latest &
```

If you'd like to publish data via REST _PUSH_ instead of local message broker, please make the following changes: 
1. In the `run message client`, change _broker_ from **local** to _rest_ and _port_ from **anylog_broker_port** to **anylog_rest_port**
2. In the sending data, change _DATA_TYPE_ from **mqtt** to **post** and update the _CONN_ info, to the REST connection information

## Support Functionality  
* `get streaming` - shows the number of rows that came into the node (through REST or MQTT)  per table 
```anylog
AL anylog-operator_1 > get streaming 

Flush Thresholds
Threshold         Value  Streamer 
-----------------|------|--------|
Default Time     |    60|Running |
Default Volume   |10,240|        |
Default Immediate|True  |        |
Buffered Rows    |    27|        |
Flushed Rows     |    10|        |


Statistics
                          Put    Put     Streaming Streaming Cached Counter    Threshold   Buffer   Threshold  Time Left Last Process 
DBMS-Table                files  Rows    Calls     Rows      Rows   Immediate  Volume(KB)  Fill(%)  Time(sec)  (Sec)     HH:MM:SS     
-------------------------|------|-----|-|---------|---------|------|----------|-----------|--------|----------|---------|------------|
test.ping_sensor         |     0|    0| |       48|       93|    14|        63|         10|   43.15|        60|        4|00:00:07    |
test.lightout4           |     0|    0| |       30|       30|     2|        27|         10|    1.04|        60|       10|00:00:20    |
test.lightout2           |     0|    0| |       29|       29|     2|        26|         10|    1.04|        60|        8|00:00:22    |
test.lightout3           |     0|    0| |       29|       29|     2|        26|         10|    1.04|        60|        8|00:00:22    |
test.lightout1           |     0|    0| |       29|       29|     1|        25|         10|    0.52|        60|       39|00:00:21    |
test.percentagecpu_sensor|     0|    0| |       47|       47|    15|        15|         10|   46.29|        60|        3|00:00:09    |
```

* `get msg client` – shows the number of rows that come into the node through a specific topic, either via MQTT or REST POST. 
```anylog
AL anylog-operator_1 > get msg client 

Subscription ID: 0001
User:         ibglowct
Broker:       driver.cloudmqtt.com:18785
Connection:   Connected

     Messages    Success     Errors      Last message time    Last error time      Last Error
     ----------  ----------  ----------  -------------------  -------------------  ----------------------------------
            113         113           0  2023-08-02 22:38:40
     
     Subscribed Topics:
     Topic            QOS DBMS Table            Column name Column Type Mapping Function        Optional Policies 
     ----------------|---|----|----------------|-----------|-----------|-----------------------|--------|--------|
     anylogedgex-demo|  0|test|['[sourceName]']|timestamp  |timestamp  |now()                  |False   |        |
                     |   |    |                |value      |int        |['[readings][][value]']|False   |        |
```

* `get local broker` - Statistics on the local broker (if the data is published to the IP and Port of the node's message broker server).
```anylog
AL anylog-operator_1 +> get local broker

Message Broker Stat
Protocol IP              Event   Success Last message time   Error Last error time Error Code Details 
--------|---------------|-------|-------|-------------------|-----|---------------|----------|-------|
MQTT    |172.104.180.110|CONNECT|  1,463|2023-08-02 23:21:41|    0|               |          |       |
MQTT    |172.104.180.110|PUBLISH| 43,887|2023-08-02 23:22:07|    0|               |          |       |
```