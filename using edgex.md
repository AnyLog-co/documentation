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

* An Anylog node configured as a [Message Broker](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#message-broker).
* An Edgex platform configured to publish the device data on an AnyLog node as the message broker.

## Configuring AnyLog

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
  
Example:
<pre>
run mqtt client where broker=local and user=ibglowct and password=MSY4e009J7ts and log=false and topic=(name=anylogedgex and dbms=edgex and table='bring [device]' and column.timestamp.timestamp=now and column.value.int='bring [readings][][value]' and column.name.str='bring [readings][][name]')
</pre>
Note: the key value pair ***broker=local*** replace the assignment of an IP and port (when 3rd parties brokers are used).    
Details on the ***run mqtt client*** command and the data mapping instructions are available at the [Subscribing to a Broker](https://github.com/AnyLog-co/documentation/blob/master/mqtt.md#subscribing-to-a-broker) section.  

## Downloading and Configuring Edgex
An overview on how Edgex publishes data on a message broker is available [here](https://docs.edgexfoundry.org/1.3/examples/Ch-ExamplesAddingMQTTDevice/). 

The following instruction specify how to download Edgex, start and stop an Edgex instance:

1) Create a working directory for Edgex install (in the example below called edgex).
<pre>
mkdir edgex 
cd edgex 
</pre>

2) Download EdgeX
<pre>
wget https://raw.githubusercontent.com/jonas-werner/EdgeX_Tutorial/master/docker-compose_files/docker-compose_step1.yml
</pre>

3) Create the yml file to use
<pre>
cp docker-compose_step1.yml docker-compose.yml 
</pre>
Change the file configuration as [detailed below](#configure-the-edgex-docker-composeyml-file).

4) Download Docker-Compose
<pre>
docker-compose pull 
</pre>

5) Start Edgex
<pre>
docker-compose up -d 
</pre>

6) Validate Edgex is running

* Validate services through browser - ```http://127.0.0.1:8500/ui/dc1/services```
* Validate services through docker
    * check docker images
    <pre>
    docker image ls
    </pre>
    * check docker containers 
    <pre>
    docker ps -a
    </pre>
* valide services using cURL by listing connected devices(s) - curl http://localhost:48082/api/v1/device

7) Stop EdgeX
*  Stop & remove docker containers
<pre>
docker-compose down
</pre>
*  Stop & remove docker containers and volumes
<pre>
docker-compose down -v
</pre>


### Configure the Edgex docker-compose.yml file

In a docker-compose.yml file, services represent the containers that will be created. 
To configure EdgeX to publish data on AnyLog as an MQTT message broker, configure the file as follows:

* uncomment the app-service-mqtt
* Replace "YOUR-UNIQUE-BROKER-URL" and "YOUR-UNIQUE-BROKER-PORT" with the AnyLog URL and Port declared on the AnyLog ***run message broker*** command.
* Replace "YOUR-UNIQUE-TOPIC" with the topic name to use.

<pre>
app-service-mqtt:
      image: edgexfoundry/docker-app-service-configurable:1.1.0
      ports:
        - "0.0.0.0:48101:48101"
      container_name: edgex-app-service-configurable-mqtt
      hostname: edgex-app-service-configurable-mqtt
      networks:
        edgex-network:
          aliases:
            - edgex-app-service-configurable-mqtt
      environment:
        <<: *common-variables
        edgex_profile: mqtt-export
        Service_Host: edgex-app-service-configurable-mqtt
        Service_Port: 48101
        MessageBus_SubscribeHost_Host: edgex-core-data
        Binding_PublishTopic: events
        # Added for MQTT export using app service
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_ADDRESS: "YOUR-UNIQUE-BROKER-URL" 
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_PORT: "YOUR-UNIQUE-BROKER-PORT" 
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_PROTOCOL: tcp
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_TOPIC: "YOUR-UNIQUE-TOPIC"
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_AUTORECONNECT: "true"
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_RETAIN: "true"
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_PERSISTONERROR: "false"
        # WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_PUBLISHER: 
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_USER: "YOUR-UNIQUE-USER"
        WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_ADDRESSABLE_PASSWORD: "YOUR-UNIQUE-PASSWORD"
        # WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_QOS: ["your quality or service"]
        # WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_KEY: [your Key]  
        # WRITABLE_PIPELINE_FUNCTIONS_MQTTSEND_PARAMETERS_CERT: [your Certificate]

      depends_on:
        - consul
  #     - logging  # uncomment if re-enabled remote logging
        - data
</pre>

### VIew statistics relating data processed on the AnyLog Broker

The ***get broker*** command provides statistics on the data processed using the broker service on the AnyLog node.  
Usage:  
<pre>
get broker
</pre>




