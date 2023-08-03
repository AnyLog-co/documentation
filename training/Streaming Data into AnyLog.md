# Streaming Data into AnyLog 

This document provides examples of configurations to data sources. 

**Other Related Documents**
* [Examples of Streaming Data into AnyLog](../examples/Streaming%20Data%20into%20AnyLog.md) 
* [Configuring the Message Broker service](../background%20processes.md#message-broker)
* [Message Broker](../message%20broker.md)
* [Using REST](../using%20rest.md)
* [Using Kafka](../using%20kafka.md)
* [Using Edgex](../using%20edgex.md)
* [The Data Generator](Data%20Generator.md)

## Third-Party MQTT Client 
AnyLog can accept data from third-party message brokers such as CloudMQTT, Eclipse Mosquitto and Kafka. 

In order to process data from a message broker, users specify the mapping between the source data and the table's 
schema. The following example demonstrates subscription to a third-party broker (_CloudMQTT_). 
 
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
Note: In the training, the data coming in will generate 4 tables (lightout1, lightout2, lightout3, lightout4) and will be stored in dbms "test".  

Sample Source Data: 
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
An AnyLog node can be configured with a local message broker service.
   
The needed configuration:  
1. Configure a message broker service on the AnyLog node 
2. Configure an MQTT client process against the local broker with the proper data mapping of the source data.

### Enable the Message Broker Service
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

After enabling the message broker service, the connection information is validated as follows:  
```anylog
AL anylog-operator_1 > get connections

Type      External Address    Internal Address    Bind Address        
---------|-------------------|-------------------|-------------------|
TCP      |198.74.50.131:32148|198.74.50.131:32148|198.74.50.131:32148|
REST     |198.74.50.131:32149|198.74.50.131:32149|0.0.0.0:32149      |
Messaging|198.74.50.131:32150|198.74.50.131:32150|0.0.0.0:32150      |
```

### Publishing to Message Broker 
Like with a third-party broker, subscribe to the local broker using the `run message client` command.
 
The example below uses the same data as the [data generator](Data%20Generator.md), but with a the message client subscribed to
a local message broker. 
 
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

**Sending Data** (using the data simulator) - make sure to update **CONN** to your MQTT IP + Port 
 
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

To publish data via REST _POST_ (using the simulator), make the following changes: 
1. In the `run message client`, change _broker_ from **local** to _rest_ and _port_ from **anylog_broker_port** to **anylog_rest_port**
2. In the sending data, change _DATA_TYPE_ from **mqtt** to **post** and update the _CONN_ info, to the REST connection information

## Support Functionality  
* `get streaming` - Monitor the number of rows added via REST or MQTT per table
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

* `get msg client` – Monitor the number of rows added by topic 
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

* `get local broker` - Monitor the calls to the local broker
```anylog
AL anylog-operator_1 +> get local broker

Message Broker Stat
Protocol IP              Event   Success Last message time   Error Last error time Error Code Details 
--------|---------------|-------|-------|-------------------|-----|---------------|----------|-------|
MQTT    |172.104.180.110|CONNECT|  1,463|2023-08-02 23:21:41|    0|               |          |       |
MQTT    |172.104.180.110|PUBLISH| 43,887|2023-08-02 23:22:07|    0|               |          |       |
```