# Using EdgeX

## Overview

EdgeX is an open source product that provides a southbound platform to connect with IoT devices.
Detailed information about Edgex is available with the [EdgeX Foundry](https://www.edgexfoundry.org/ecosystem/members/) project under the LF Edge umbrella.  

EdgeX allows fast integration with devices and supports multiple protocols including Modbus, MQTT, SNMP, Grove, Camera, REST and BACnet.
Additional information on EdgeX supported protocols is available at [Device Services - existing and work underway](https://wiki.edgexfoundry.org/display/FA/Device+Services+-+existing+and+work+underway).  

Integration between Edgex and AnyLog is achieved by configuring EdgeX to send the sensor data to an [MQTT](https://en.wikipedia.org/wiki/MQTT) broker
whereas the broker can be any third party broker or an AnyLog node that is configured to serve as the broker.

### Integration with a third party broker
EdgeX can be configured with a third party MQTT broker. Examples of MQTT brokers are the open source [Eclipse Mosquitto](https://mosquitto.org/) project 
and [CloudMQTT](https://www.cloudmqtt.com/) that provides an MQTT broker (using Mosquitto) as a service.  
Configuring AnyLog to pull data from a third party MQTT broker is explained in the AnyLog [Using MQTT Broker](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md#using-mqtt-broker) section.

### Sending MQTT data to an AnyLog instance

Any AnyLog node can be configured with a [Message Broker](https://en.wikipedia.org/wiki/Message_broker) functionality.  
By configuring a node as message broker, data can be delivered from Edgex directly to AnyLog without the need to deliver the data through a third party platform or through the cloud.

## Direct delivery of data from EdgeX to an AnyLog instance 

As detailed below, Edgex is configured to send the data to a message broker and an AnyLog instance is configured as a Message Broker.  
The AnyLog node receiving the data can be an Operator node that hosts the data or a Publisher node that delivers the data to one or multiple Operator nodes 
(the [getting started](https://github.com/AnyLog-co/documentation/blob/master/getting%20started.md#type-of-instances) document details the types of nodes participating in the AnyLog Network). 

## Prerequisites

* An Anylog node configured as a Message Broker
* An Edgex platform configured to publish the device data on an AnyLog node as the message broker.

## Configuring AnyLog

The AnyLog node receiving the data needs to be configured as follows:

* Enable the ***Message Broker*** functionality:   
Usage
<pre>
run message broker [ip] [port] [local ip] [Local port] [threads]
</pre>
Details on the the ***run message broker*** command are available at the [Message Broker](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#message-broker)
section in the [Background Processes](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#background-processes) document.

* Subscribe to topics assigned to messages received on the broker and detail the mapping of the messages to the needed structure.  
This process is identical to the subscription process to 3rd parties MQTT brokers whereas rather than specifying an IP and Port of the 3rd party broker, the broker is identified by the keyword ***local***.  
  
Example:
<pre>
run mqtt client where broker=local and user=ibglowct and password=MSY4e009J7ts and log=false and topic=(name=anylogedgex and dbms=edgex and table='bring [device]' and column.timestamp.timestamp=now and column.value.int='bring [readings][][value]' and column.name.str='bring [readings][][name]')
</pre>
Note: the key value pair ***broker=local*** replace the assignment of an IP and port (when 3rd parties brokers are used).    
Details on the ***run mqtt client*** command and the data mapping instructions are available at the [Subscribing to a Broker](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md#subscribing-to-a-broker) section.  

## Configuring Edgex

Edgex is configuted to deliver the data to AnyLog as an MQTT broker




