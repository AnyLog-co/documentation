# Adding Data

The following provides examples of adding via: 
* [PUT](put_data.py)
* [POST](post_data.py) 
* [MQTT](mqtt_data.py)

For MQTT & POST commands user should have a running `mqtt client` on the correlated node. 

AnyLog has an option to run a built-in [MQTT](../../message%20broker.md) broker/client combo, to configure: 

```
run message broker !external_ip !anylog_borker_port !ip !anylog_broker_port

run mqtt client where broker=local and port=!anylog_broker_port and log=false and topic=(...)
```