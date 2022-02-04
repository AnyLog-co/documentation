# Using Kafka

## Overview

Nodes in the AnyLog Network interact with Kafka in 2 ways:
* AnyLog serves as a Data Producer to Kafka - any result set of a query can be directed to a Kafka instance.   
* AnyLog is a Data Consumer - Kafka serves as a [message broker](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#using-a-message-broker) that transfers data to the network nodes.  
  
## Prerequisites

* An AnyLog Network with nodes hosting data.
* A configured Kafka instance.

## AnyLog serves as a Data Producer 

A query issued to the network can direct the result set to a Kafka instance.  
The Kafka instance is identified by an IP and port, and the query result set is associated with a topic.  

The following command, issued on the AnyLog CLI, sends 10 row from a table managed by nodes in the network to a Kafka instance:

<pre>
run client () sql litsanleandro format = json:output and stat  = false and dest = kafka@198.74.50.131:9092 and topic = ping_data "select device_name, timestamp, value, from ping_sensor where timestamp > now() - 1 day limit 10"
</pre>

Note:
* The format directive ***json:output*** organizes each set of timestamp and value (that are returned by the query) in JSON.
* The destination is identified by the key ***kafka*** followed by the Kafka configured IP and Port (dest = kafka@198.74.50.131:9092).
* The Kafka topic that is associated with the data in the example above is ***ping_data***

## AnyLog serves as a Data Consumer

Each node in the AnyLog Network can be configured as a data consumer.  
The flow of data from a Kafka instance to the network is detailed in the [The Southbound Connectors Diagram](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#the-southbound-connectors-diagram).

The command ***run kafka consumer*** initiates a process that serves as a client that subscribes to one or more topics 
and consume published messages by pulling data from the Kafka instance.

Usage:

<pre>
run kafka consumer where ip = [ip] and port = [port] and reset = [latest/earliest] and topic = [topic and mapping instructions]
</pre>

Command options:

| Key        | Value  | Default  |
| ---------- | -------| ------- |
| ip         | The Kafka broker IP. |  |
| Port       | The Kafka broker port. | |
| reset      | Determines the offset policy. Optional values are ***latest*** or ***earliest***.| latest |
| topic      | One or more topics with mapping instructions.| |

Details on the topic declaration and mapping instructions are available [here](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#the-topic-params).  

Example:
<pre>
run kafka consumer where ip = 198.74.50.131 and port = 9092 and offset = latest and topic = (name = ping_data and dbms = lsl_demo and table = ping_sensor and column.timestamp.timestamp = "bring [timestamp]" and column.value.int = "bring [value]")
</pre>


### Related commands

| Command        | Info provided  |
| ---------- | -------|
| [get processes](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#the-get-processes-command)    | Background processes to determine if Kafka is enabled |
| [get msg client](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-msg-clients)   | Subscriptions to brokers to determine related configurations and data consumed from Kafka instances |
| [get streaming](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-streaming)   | Data consumed from brokers associated to dbms tables |
| [get operator](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-operator)   | Statistics on ingestion of data to database tables |
