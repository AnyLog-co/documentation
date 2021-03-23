# Using EdgeX

## Overview

EdgeX is an open source product that provides a southbound platform to connect with devices.
Detailed information about Edgex is available with the [EdgeX Foundry](https://www.edgexfoundry.org/ecosystem/members/) project under the LF Edge umbrella.  

EdgeX allows fas integration with devices and supports multiple protocols including Modbus, MQTT, SNMP, Grove, Camera, REST and BACnet.
Additional information on EdgeX supported protocols is available at [Device Services - existing and work underway](https://wiki.edgexfoundry.org/display/FA/Device+Services+-+existing+and+work+underway).  

Integration between Edgex and AnyLog is achieved by configuring EdgeX to send the sensor data to an [MQTT](https://en.wikipedia.org/wiki/MQTT) broker
whereas the broker can be any third party broker or an AnyLog node that is configured to serve as the broker.

### Integration with a third party broker
EdgeX can be configured with a third party MQTT broker. Examples of MQTT brokers are the open source [Eclipse Mosquitto](https://mosquitto.org/) project 
and [CloudMQTT] that provides an MQTT broker (using Mosquitto) as a service.  
Configuring AnyLog to pull data from a third party MQTT broker is explained in the AnyLog [Using MQTT Broker](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md#using-mqtt-broker) section.

### Sending MQTT data to an AnyLog instance

Any AnyLog node can be configured with a [Message Broker](https://en.wikipedia.org/wiki/Message_broker) functionality.  
By configuring a node as message broker, data can be delivered from Edgex directly to AnyLog without the need to deliver the data through a third party platform or through the cloud.

## Direct delivery of data from EdgeX to an AnyLog instance 

As detailed below, Edgex is configured to send the data to a message broker and an AnyLog instance is configured as a Message Broker.  
The AnyLog node receiving the data can be an Operator node that hosts the data or a Publisher node that delivers the data to one or multiple Operator nodes. 

## Prerequisites

