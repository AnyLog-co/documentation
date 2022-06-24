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

Helper commands would be:

Get the list of available IPs on the node:
<pre>
get ip list
</pre>

If the broker process fails to bind, the following command returns the list of active connections on the 
machine including the PID of the process which opened the socket:
<pre>
get machine connections
</pre>


