# Setting AnyLog as a Message Broker

This document demonstrates the following:
1) Configure an AnyLog node as a broker.
2) Associate the published data o a topic.
3) Map the data to a table structure.
4) Ingest the data to a local database.

Additional information:
* Subscribing to a third party message broker and configuring AnyLog as a message broker
  is detailed in the [Using a Message Broker](../message%20broker.md#using-a-message-broker).
* Adding data is detailed in [Adding Data to Nodes in the Network](../adding%20data.md#adding-data-to-nodes-in-the-network).
* Configuring a node as a message broker is detailed in [Message Broker](..//background%20processes.md#message-broker).

Note: Setting AnyLog as a Message Broker is referenced as Option B in [The Southbound Connectors Diagram](../adding%20data.md#the-southbound-connectors-diagram).


## Example - Setting a node as a broker

The following example configures a broker process that listens to incoming messages on designated IPs and Ports.
<pre>
run message broker !external_ip 7850 !ip 7850
</pre>
Note: the first IP and port pair bind to an external network, and the second to a local network (if applicable). 

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
machine including the ID of the process which opened the socket:
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
run mqtt client where broker=local and log=false and topic=(name=mqtt-test and dbms=my_dbms and table=rand_data and column.timestamp.timestamp=now and column.value.float='bring [readings][][value]')
</pre>
In the example below, if the node message broker process is listening on 10.0.0.78:7850, the ***run mqtt client*** command will subscribe
to the data published on the local node and is equivalent to the setup where the broker is set to ***local***.
<pre>
run mqtt client where broker=10.0.0.78 and port=7850 and log=false and topic=(name=mqtt-test and dbms=my_dbms and table=rand_data and column.timestamp.timestamp=now and column.value.float='bring [readings][][value]')
</pre>

The following command details the clients subscribed and information on the messages processed by each client:
<pre>
get msg client
</pre>

## Example - Publishing data

With the configuration detailed above, data can be pushed to the broker, and if assigned to the topic ***mqtt-test*** 
will be processed as detailed in the ***run mqtt client*** command.

Using the following setup and command, data can be published without a third part publisher:
```
<message={"id":"ec798767-617c-467c-984f-ba5fddd474f1",
	"device":"Random-Integer-Generator01",
	"created":1625862443151,
	"origin":1625862443149315045,
	"readings":[{	"id":"4b553911-e41f-4146-a863-a8e5a9ad1cfc",
			"origin":1625862443149271124,
			"device":"Random-Integer-Generator01",
			"name":"RandomValue_Int32",
			"value":"-998060882",
			"valueType":"Int32"}]}>
```
Notes: 
* The assignment of the JSON data to the key ***message*** is contained within angle brackets (***<...>***) 
to allow, on the AnyLog CLI, processing of info provided on multiple lines, as a single line. Therefore, users can 
cut and paste the assignment above to the AnyLog CLI.
* The assignment is ignored with missing brackets.
* The following command validates JSON structure:
  <pre>
  json !message test
  </pre>

The following command publishes data on a broker and assines the published data to a topic:
<pre>
mqtt publish where broker=!ip and port=7850 and topic=mqtt-test and message=!message 
</pre>

Using the ***mqtt publish*** command, the data is received by the node as a broker (on the configured IP and Port in the ***run broker*** commmand).  
The data is processed by the mapping instructions associated with the ***topic*** declared in the ***run msg client*** command.
In the above example, the mapping instructions are:
<pre>
(name=mqtt-test and dbms=my_dbms and table=rand_data and column.timestamp.timestamp=now and column.value.float='bring [readings][][value]')
</pre>

Use the following commands to monitor the data flow from the broker provess to the client mapping process:
<pre>
get msg broker
get msg client
</pre>

## Example - Validating data storage in a local database

The streaming data is pushed to buffers representing the local tables.  
Use the following command to view the status of the buffers:
<pre>
get streaming
</pre>

When the buffers are flushed (depending on configuration options) data is added to the local database and can be queried.  
For example:
<pre>
sql my_dbms format=table and extend=(+ip, +node_name) "select count(*) from rand_data" 
</pre>


