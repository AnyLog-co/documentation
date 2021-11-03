# Debugging

Debugging details different processes as they accrue and monitor processes that are not executing properly

## Monitor REST calls on the AnyLog CLI

By enabling trace on the command line, it is possible to trace the commands executed and the incoming data.
Command details will be displayed on stdout and depending on the trace level.

<pre>
trace level = N  run rest server
</pre>

N designates the trace level.

Examples:

| Trace Level   | Printout | Example |
| ------------- | ------------- |   ---------- |
|1 | Print message source info |  10.0.0.78 - - [02/Nov/2021 18:40:08] "GET / HTTP/1.1" 200 - |
|2 | Print command execution info |  10.0.0.78 - - [02/Nov/2021 18:40:08] "GET / HTTP/1.1" 200 - |
|  |                              |  10.0.0.78 - - [get status] [Success] |
|3 | Add header and body info     |  Detailed info on the message headers and body |


## The Error Log and the REST Log

Errors always update the error log. The following command returns the errors from the log file.
<pre>
get error log
</pre>

A special log contain the rest calls.  
By default, a REST call that failes updates the ***REST log*** with detailed information from the REST HEADER and BODY.  
The following command returns the data at the log:

<pre>
get rest log
</pre>

Users can direct every call to the log (regardless if the call failed) using the following command:
<pre>
set rest log on
</pre>
And reverting to the default behaviour using the following command:
<pre>
set rest log off
</pre>

## REST calls statistics

Statistics on REST calls is retrieved with the following command:
<pre>
get rest
</pre>

## Monitoring data streams

When data is added using REST, it is first organized by tables (in the streaming buffers) based on the information contained in the REST call 
(details are available in the [adding data](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#adding-data-to-nodes-in-the-network) section.)

Statistics on the mapping of data to the needed schema is available with the following command:
<pre>
get streaming
</pre>

## Monitoring Operator data ingestion processes

Data is ingested to the table with the operator process.

Statistics on the ingestion process is available with the following command:
<pre>
get operator
</pre>

## Monitoring the Message Broker processes
If data is added to an AnyLog Node as a message broker, debugging the broker processes are detailed [here](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#debugging).

## Monitoring and profiling queries

Users can view the queries issued to a node and execution details. In addition users can declare a query log to capture queries which are not efficiently executed.  
Details are available in the [Profiling and Monitoring Queries](https://github.com/AnyLog-co/documentation/blob/master/profiling%20and%20monitoring%20queries.md#profiling-and-monitoring-queries) section.


