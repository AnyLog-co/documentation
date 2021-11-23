# REST via Python

The following provides python example for communicating with AnyLog via REST

## Blockchain Data
By default AnyLog has a a set of "hard-set" blockchain policies. Howeve  

## Sending Data
AnyLog supports passing data through both REST (_POST_ and _PUT_) as well as through _MQTT_.
* [PUT](data/put_data.py) 
* [POST](data/post_data.py) 
* [MQTT](data/mqtt_data.py)

An AnyLog instance that's receiving data through either _MQTT_ or _POST_ should have a running 
[message client](../../message%20broker.md) process running on it.

In addition, it's important to note that AnyLog can run not just as a message client, but also as a 
[message broker](../../background%20processes.md#message-broker) - allowing content to come in directly via MQTT rather   
than through a third-party application like _Eclipse Mosquito_ and _Cloud MQTT_.



