# REST via Python

The following provides python example for communicating with AnyLog via REST

## Sending Data
Data can be added to nodes in the network in many ways. Detailes are available in the [adding data](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#adding-data-to-nodes-in-the-network) sectiion.    
Python examples are available with the following links:
* [PUT](data/put_data.py) 
* [POST](data/post_data.py) 
* [MQTT](data/mqtt_data.py)

An AnyLog instance that's receiving data through either _MQTT_ or _POST_ should have a running 
[message client](../../message%20broker.md) process running on it.

Note that AnyLog can run not just as a client subscribed to a broker (and a topic), but also as a 
[message broker](../../background%20processes.md#message-broker) - allowing external applications to treat AnyLog as an MQTT broker.   




