# Setting AnyLog as a Message Broker

This document demonstrates the following:
1) Configure an AnyLog node as a broker.
2) Associate the published data o a topic.
3) Map the data to a table structure.
4) Ingest the data to a local database.

Additional information:
* Subscribing to a third party message broker and configuring AnyLog as a message broker
  is detailed at the [Using a Message Broker](../message%20broker.md#using-a-message-broker).
* Adding data is detailed at [Adding Data to Nodes in the Network](../adding%20data.md#adding-data-to-nodes-in-the-network).
* Configuring a node as a message broker is detailed at the [Message Broker](..//background%20processes.md#message-broker) 
  section.

Note: Setting AnyLog as a Message Broker is referenced as Option B in [The Southbound Connectors Diagram](../adding%20data.md#the-southbound-connectors-diagram).


## Example - Setting a node as a broker

The following example configures a broker process that listens to incoming messages on designated IPs and Ports.
<pre>
run message broker !external_ip 7850 !ip 7850
</pre>

Use the following command to validate that the process is properly configured and bound:
<pre>
get connections
</pre>

Use the following command to see messages received by the broker:
<pre>
get broker
</pre>

### Helper commands would be:

Get the list of available IPs on the node:
<pre>
get ip list
</pre>

If the broker process fails to bind, the following command returns the list of active connections on the 
machine including the PID of the process which opened the socket:
<pre>
get machine connections
</pre>

The following command details the process using port 7850:
<pre>
get machine connections where port = 7850
</pre>

## Example - Subscribing to messages

When data is published on a broker, it is assigned to a topic.  
An AnyLog node can subscribe to messages published on a third party broker or, if the same node is configured as a broker,
to messages published on the AnyLog node.  
Subscription is with the command ```run mqtt client``` and such that:  
* If the node is subscribing to a third part broker, the IP and Port of the third party broker are provided.
* If the same node acts as a broker, the broker IP is declared as ***local***, and the process determines that the data is published on the local node.

The following command subscribes to local messages:
<pre>
run mqtt client where broker=local and log=false and topic=(name=mqtt-test and dbms=edgex and table=rand_data and column.timestamp.timestamp=now and column.value.float='bring [reading][][value]')
</pre>
In the example below, if the node message broker process is listening on 10.0.0.78:7850, the ***run mqtt client*** command will subscribe
to the data published on the local node and is equivalent to the setup where broker is set to ***locaal***.
<pre>
run mqtt client where broker=10.0.0.78 and port=7850 and log=false and topic=(name=mqtt-test and dbms=edgex and table=rand_data and column.timestamp.timestamp=now and column.value.float='bring [reading][][value]')
</pre>

## Example - Publishing data