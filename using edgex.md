# Using EdgeX

## Overview

EdgeX is an open source product that provides a southbound platform to connect with IoT devices.
Detailed information about EdgeX is available with the [EdgeX Foundry](https://www.edgexfoundry.org/ecosystem/members/) project under the LF Edge umbrella.  

EdgeX allows fast integration with devices and supports multiple protocols including Modbus, MQTT, SNMP, Grove, Camera, REST and BACnet.
Additional information on EdgeX supported protocols is available at [Device Services - existing and work underway](https://wiki.edgexfoundry.org/display/FA/Device+Services+-+existing+and+work+underway).  

Integration between EdgeX and AnyLog is achieved by configuring EdgeX to send the sensor data to an [MQTT](https://en.wikipedia.org/wiki/MQTT) broker
whereas the broker can be any third party broker or an AnyLog node that is configured to serve as the broker.

### Integration with a third party broker
EdgeX can be configured with a third party MQTT broker. Examples of MQTT brokers are the open source [Eclipse Mosquitto](https://mosquitto.org/) project 
and [CloudMQTT](https://www.cloudmqtt.com/) that provides an MQTT broker (using Mosquitto) as a service.  
Configuring AnyLog to pull data from a third party MQTT broker is explained in the AnyLog [Using MQTT Broker](message%20broker.md#using-a-message-broker) section.

### Sending MQTT data to an AnyLog instance

Any AnyLog node can be configured with a [Message Broker](https://en.wikipedia.org/wiki/Message_broker) functionality.  
By configuring a node as message broker, data can be delivered from EdgeX directly to AnyLog without the need to deliver the data through a third party platform or through the cloud.

## Direct delivery of data from EdgeX to an AnyLog instance 

As detailed below, EdgeX is configured to send the data to a message broker and an AnyLog instance is configured as a Message Broker.  
The AnyLog node receiving the data can be an Operator node that hosts the data or a Publisher node that delivers the data to one or multiple Operator nodes 
(the [getting started](getting%20started.md#type-of-instances) document details the types of nodes participating in the AnyLog Network). 

## Prerequisites

* An Anylog node configured as a [Message Broker](background%20processes.md#message-broker).
* An EdgeX platform configured to publish the device data on an AnyLog node as the message broker.

## Configuring AnyLog

The AnyLog node receiving the data needs to be configured as follows:

* Enable the _Message Broker_ functionality:   
**Usage**:
```anylog
run message broker [ip] [port] [local ip] [Local port] [threads]
```
Details on the run `message broker` command are available at the [Message Broker](background%20processes.md#message-broker)
section in the [Background Processes](background%20processes.md#background-processes) document.

* Subscribe to topics assigned to messages received on the broker and detail the mapping of the messages to the needed structure.  
This process is identical to the [subscription process to 3rd parties MQTT brokers](message%20broker.md#subscribing-to-a-third-party-broker) 
whereas rather than specifying an IP and Port of the 3rd party broker, the broker is identified by the keyword _local_.  
  
**Example**:
```anylog
run msg client where broker=local and user=ibglowct and password=MSY4e009J7ts and log=false and topic=(name=anylogEdgeX and dbms=EdgeX and table='bring [device]' and column.timestamp.timestamp=now and column.value.int='bring [readings][][value]' and column.name.str='bring [readings][][name]')
```

**Note**: the key value pair `broker=local` replace the assignment of an IP and port (when 3rd parties brokers are used).    
Details on the `run msg client` command and the data mapping instructions are available at the [Subscribing to a Broker](message%20broker.md#subscribing-to-the-topic-) section.  

## Downloading and Configuring EdgeX 
Our [deployments directions](deployments/Support/EdgeX.md) provide details for deploying EdgeX with data being sent into AnyLog via [message broker](https://docs.edgexfoundry.org/1.3/examples/Ch-ExamplesAddingMQTTDevice/); either directly or
through a third-party broker.

1. Clone docker-compose file(s)
```shell
git clone https://github.com/AnyLog-co/lfedge-code
```
2. Deploy EdgeX with [random data generator](https://docs.edgexfoundry.org/1.3/examples/Ch-ExamplesRandomDeviceService/#edgex-apis-related-to-random-integer-device-service) - by default the node is sending data into third-party CloudMQTT broker, using 
`anylogedgex` topic. Please review [deployment directions](deployments/Support/EdgeX.md) to configure MQTT as 
you see fit.  
```shell  
cd lfedge-code/edgex
docker-compose up -d
```
3. Validate EdgeX is running & Data is coming in  
```shell
curl http://127.0.0.1:48080/api/v1/reading | jq
```


## Configuring AnyLog for EdgeX Data 
The following example uses third-party broker to accept random data generator data from EdgeX. 
1. Access AnyLog Node
```shell
docker attach --detach-keys="ctrl-d" anylog-node
```
2. Execute `run msg client`
```anylog
broker=driver.cloudmqtt.com
port=18785
user=ibglowct
password=MSY4e009J7ts
topic_name=anylogEdgeX 
dbms_name=test 
table_name=rand_data 

<run msg client where broker=!broker and port=!port and user=!user and passsword=!password and log=false and topic=(
    name=!topic_name and 
    dbms=!dbms_name and 
    table=!table_name and 
    column.timestamp.timestamp=now and 
    column.value=(type=float and value="bring [readings][][value]") 
)>
```
3. Validate MQTT client is accepting data
```anylog
get msg client
```


