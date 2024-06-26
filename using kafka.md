# Using Kafka

## Overview

Nodes in the AnyLog Network interact with Kafka in 2 ways:
* AnyLog serves as a Data Producer to Kafka - any result set of a query can be directed to a Kafka instance.   
* AnyLog is a Data Consumer - Kafka serves as a [message broker](message%20broker.md#using-a-message-broker) that transfers data to the network nodes.  
  
## Prerequisites

* An AnyLog Network with nodes hosting data.
* A configured Kafka instance.

## AnyLog serves as a Data Producer 

A query issued to the network can direct the result set to a Kafka instance.  
The Kafka instance is identified by an IP and port, and the query result set is associated with a topic.  

The following command, issued on the AnyLog CLI, sends 10 row from a table managed by nodes in the network to a Kafka instance:

```anylog
run client () sql litsanleandro format = json:output and stat  = false and dest = kafka@198.74.50.131:9092 and topic = ping_data "select device_name, timestamp, value, from ping_sensor where timestamp > now() - 1 day limit 10"
```

Note:
* The format directive _json:output_ organizes each set of timestamp and value (that are returned by the query) in JSON.
* The destination is identified by the key _Kafka_ followed by the Kafka configured IP and Port (dest = kafka@198.74.50.131:9092).
* The Kafka topic that is associated with the data in the example above is `ping_data`

## AnyLog serves as a Data Consumer

Each node in the AnyLog Network can be configured as a data consumer.  
The flow of data from a Kafka instance to the network is detailed in [The Southbound Connectors Diagram](adding%20data.md#the-southbound-connectors-diagram).

The command `run kafka consumer` initiates a process that serves as a client that subscribes to one or more topics 
and consume published messages by pulling data from the Kafka instance.

**Usage**:

```anylog
run kafka consumer where ip = [ip] and port = [port] and reset = [latest/earliest] and topic = [topic and mapping instructions]
```

**Command options**:

| Key        | Value  | Default  |
| ---------- | -------| ------- |
| ip         | The Kafka broker IP. |  |
| Port       | The Kafka broker port. | |
| reset      | Determines the offset policy. Optional values are _latest_ or _earliest_| _latest_ |
| topic      | One or more topics with mapping instructions.| |

Details on the topic declaration and mapping instructions are available [here](message%20broker.md#the-topic-params).  

**Example**:
```anylog
run kafka consumer where ip = 198.74.50.131 and port = 9092 and reset = latest and topic = (name = ping_data and dbms = lsl_demo and table = ping_sensor and column.timestamp.timestamp = "bring [timestamp]" and column.value.int = "bring [value]")
```


### Related commands

| Command                                                          | Info provided  |
|------------------------------------------------------------------| -------|
| [get processes](monitoring%20nodes.md#the-get-processes-command) | Background processes to determine if Kafka is enabled |
| [get msg client](monitoring%20calls.md#get-msg-clients)          | Subscriptions to brokers to determine related configurations and data consumed from Kafka instances |
| [get streaming](monitoring%20calls.md#get-streaming)             | Data consumed from brokers associated to dbms tables |
| [get operator](monitoring%20calls.md#get-operator)               | Statistics on ingestion of data to database tables |
