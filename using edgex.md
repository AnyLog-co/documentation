# Using EdgeX

## Overview

EdgeX provides a southbound platform to connect with devices.
Detailed information on Edgex is available with the [EdgeX Foundry](https://www.edgexfoundry.org/ecosystem/members/) project under he LF Edge umbrella.  

EdgeX allows fas integration with devices and suports multiple protocols including Modbus, MQTT, SNMP, Grove, Camera, REST and BACnet.
Additional information on EdgeX supported protocols is available at [Device Services - existing and work underway](https://wiki.edgexfoundry.org/display/FA/Device+Services+-+existing+and+work+underway).  

Integration between Edgex and AnyLog is achieved by configuring EdgeX to send the sensor data to an [MQTT](https://en.wikipedia.org/wiki/MQTT) 
whereas the broker can be any third party broker or an AnyLog node that is configured to serve as the broker.


* 
AnyLog connects to Edgex in one of as a [Message Broker](https://en.wikipedia.org/wiki/Message_broker) where EdgeX is configured to send the sensor data to an MQTT broker and  



## Prerequisites

