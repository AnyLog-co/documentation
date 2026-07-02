---
layout: default
title: Background Services
parent: Commands 
nav_order: 1
---
# Background Services

The background services enable data processing on each participating node.  
Services can be enabled using one of the following methods:
* As command line arguments passed to the EdgeLake process when initiated.
* On the EdgeLake CLI.
* As an EdgeLake configuration file that is processed using the command: *process [path and file name]*
* As a policy in the metadata that is associated to a node using the command: *config from policy where id = [policy id]*

The following command lists the background services and their status:

**Usage**:
<pre class="code-frame"><code class="language-anylog">get processes [where format = json]</code></pre>

**Explanation**: List the background processes and their status.

**Details:** [The "get processes" command](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20nodes.md#the-get-processes-command)

The main services are listed below:
    
- [Connect to the EdgeLake Network](#connect-to-the-edgelake-network)  
- [The local data storage service](#the-local-data-storage-service)  
- [REST Services](#rest-services)  
- [The message broker services](#message-broker-services)  
- [Subscribe to a 3rd party broker](#subscribe-to-a-3rd-party-broker)  
- [Subscribe to Kafka](#subscribe-to-kafka)  
- [gRPC Client Service](#grpc-client-service)  
- [SMTP Client](#enable-smtp-client-service)  
- [The Scheduler Services](#the-scheduler-services)  
- [The Blobs Archiver Services](#blob-archiver-services)  


## Connect to the EdgeLake Network

Connecting to an EdgeLake Network requires 2 services:
1. [Enable the TCP service](#enable-the-tcp-service) - A listener service for incoming messages.
2. [Enable the blockchain synchronization service](#enable-the-blockchain-synchronization-service) - A service that continuously synchronizes the metadata.

Monitoring the services' status:
1. [get connections](#get-the-network-configuration-info) - Return the node's connection information.
2. [get synchronizer](#get-the-metadata-synchronization-info) - Return the metadata synchronization information.


### Enable the TCP service
The TCP service provides the functionality to send and recieve messages from peer nodes using the EdgeLake Network Protocol.  

**Usage**:
<pre class="code-frame"><code class="language-anylog">&lt;run tcp server where 
  external_ip = [ip] and external_port = [port] and 
  internal_ip = [local_ip] and internal_port = [local_port] and 
  bind = [true/false] and threads = [threads count]&gt;
</code></pre>

**Explanation**: Set a TCP server in a listening mode on the specified IP and port.

* The first pair of IP and Port that are used by a listener process to receive messages from members of the network.
* The second pair of IP and Port are optional, to indicate the IP and Port that are accessible from a local network.
* _threads_ - an optional parameter for the number of workers threads that process requests which are sent to the provided IP and Port. The default value is 6.

**Examples**:
<pre class="code-frame"><code class="language-anylog">run tcp server where external_ip = !ip and external_port = !port  and threads = 3

&lt;run tcp server where 
  external_ip = !external_ip and external_port = 7850 and 
  internal_ip = !ip and internal_port = 7850 and 
  bind=false and threads = 6&gt;
</code></pre>

**Details**: [run tcp server](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#the-tcp-server-process)

### Get the network configuration info
**Usage**:
<pre class="code-frame"><code class="language-anylog">get connections</code></pre>

**Explanation:**

Return the node's connection information including the TCP service information.

### Enable the blockchain synchronization service
**Usage**:
<pre class="code-frame"><code class="language-anylog">run blockchain sync [options]</code></pre>
        

**Explanation:**  
Repeatedly update the local copy of the blockchain

**Options:**   
* <code class="language-anylog">source</code> - The source of the metadata (blockchain or a Master Node). 
* <code class="language-anylog">dest</code> - The destination of the blockchain data such as a file (a local file) or a DBMS (a local DBMS).
* <code class="language-anylog">connection</code> - The connection information that is needed to retrieve the data. For a Master, the IP and Port of the master node.
* <code class="language-anylog">time</code> - The frequency of updates.

**Examples:**  
<pre class="code-frame"><code class="language-anylog">run blockchain sync where source = master and time = 3 seconds and dest = file and dest = dbms and connection = !ip_port
run blockchain sync where source = blockchain and time = !sync_time and dest = file and platform = ethereum
</code></pre>


### Get the metadata synchronization info
**Usage**:
<pre class="code-frame"><code class="language-anylog">get synchronizer</code></pre>

**Explanation:**

Return the synchronizer status.

**Details:** [Synchronier Status](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#synchronizer-status).

## The local data storage service

### Configure the Operator service
The Operator service provides the local data storage functionalities.  
The service captures the data streams, identifies or creates schemas and ingest the data into a local database.

**Usage**:
<pre class="code-frame"><code class="language-anylog">run operator where [option] = [value] and [option] = [value] ...</code></pre>

**Explanation:**

Monitors new data added to the watch directory and load the new data to a local database

**Options:**

* <code class="language-anylog">policy</code> - The ID of the operator policy.
* <code class="language-anylog">compress_json</code> - True/False to enable/disable compression of the JSON file.
* <code class="language-anylog">compress_sql</code> - True/False to enable/disable compression of the SQL file.
* <code class="language-anylog">archive_json</code> - True moves the JSON file to the 'archive' dir if processing is successful. The file deleted if archive_sql is false.
* <code class="language-anylog">archive_sql</code> -  True moves the SQL file to the 'archive' dir if processing is successful. The file deleted if archive_sql is false.
* <code class="language-anylog">limit_tables</code> - A list of comma separated names within brackets listing the table names to process.
* <code class="language-anylog">craete_table</code> - A True value creates a table if the table doesn't exist.
* <code class="language-anylog">master_node</code> - The IP and Port of a Master Node (if a master node is used).
* <code class="language-anylog">update_tsd_info</code> - True/False to update a summary table (tsd_info table in almgm dbms) with status of files ingeste

**Examples:**  
<pre class="code-frame"><code class="language-anylog">run operator where create_table = true and update_tsd_info = true and archive_json = true and distributor = true and master_node = !master_node and policy = !operator_policy  and threads = 3
run operator where create_table = true and update_tsd_info = true and archive_json = true and distributor = true and blockchain = ethereum and policy = !operator_policy  and threads = 3
</code></pre>

**Details:** [Operator Process](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#operator-process).


### Get Operator info
The **get operator** command returns info on the configuration and data processed by the Operator service.

**Usage:**
<pre class="code-frame"><code class="language-anylog">get operator [options] [where format = json]</code></pre>

**Explanation:**

Return information on the Operator processes and configuration.

**Examples:**
<pre class="code-frame"><code class="language-anylog">get operator
get operator inserts
get operator summary
get operator config
get operator summary where format = json
</code></pre>

**details:** [get operator](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-operator)

## REST Services
Enable and monitor a service that receives commands and data via REST from 3rd parties applications and data sources.

* Enable the service: [run rest server](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests)
* Monitor the REST service:
    * [get rest server info](#rest-service-info-commands)
    * [get rest calls](#rest-service-info-commands)
    * [get rest pool](#rest-service-info-commands)

###  Enable the REST service
**Usage:**
<pre class="code-frame"><code class="language-anylog">&lt;run rest server where 
  external_ip = [external_ip ip] and external_port = [external port] and 
  internal_ip = [internal ip] and internal_port = [internal port] and 
  timeout = [timeout] and ssl = [true/false] and bind = [true/false]&gt;
</code></pre>

**Explanation:**

Enable a REST server in a listening mode on the specified ip and port.
* The IP and Ports associate the service with external and internal IPs and Ports.
* [timeout] - Max wait time in seconds. A 0 value means no wait limit, and the default value is 20 seconds. A timeout returns an error message to the calling application. 
* If ssl is set to True, connection is using HTTPS.
* If bind is **true**, only the specified IP is allowed (with 2 IPs, the external is ignored).

Examples:
<pre class="code-frame"><code class="language-anylog">&lt;run rest server where 
  internal_ip = !ip and internal_port = 7849 and 
  timeout = 0 and threads = 6 and ssl = true&gt;
</code></pre>


**Details:** [Rest Requests](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests)

### REST service info commands
The following commands return info on the REST service configuration and processes:

Configuration information of the REST service:
<pre class="code-frame"><code class="language-anylog">get rest server info</code></pre>

Statistics on the REST calls:
<pre class="code-frame"><code class="language-anylog">get rest calls</code></pre>

Status of REST threads:
<pre class="code-frame"><code class="language-anylog">get rest pool</code></pre>


## Message broker services
Enable and monitor a service that operates as a message broker, allowing to publish data on the EdgeLake Node.

### Enable the message broker service
**Usage:**
<pre class="code-frame"><code class="language-anylog">&lt;run message broker where 
  external_ip = [ip] and external_port = [port] and 
  internal_ip = [local_ip] and internal_port = [local_port] and 
  bind = [true/false] and threads = [threads count]&gt;
</code></pre>

**Explanation:**  Set a message broker in a listening mode on the specified IP and port. *Threads count* represents the number of threads supporting the service.

**Examples:**
<pre class="code-frame"><code class="language-anylog">run message broker where external_ip = !ip and external_port = !port  and threads = 3
run message broker where external_ip = !external_ip and external_port = 7850 and internal_ip = !ip and internal_port = 7850 and threads = 6
</code></pre>

**Details:** [Message Broker Services](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#message-broker)

### Get info on the Message Broker service
The following command returns statistics on the local broker:

<pre class="code-frame"><code class="language-anylog">get local broker</code></pre>

## Subscribe to a 3rd party broker

Retrieve data from a 3rd party broker and monitor the streaming process.

* [Subscribe to a broker](#subscribe-to-a-3rd-party-broker)
* [Get subscription info](#get-subscription-info)

### Subscribe to a broker
The **run msg client** command subscribes to a 3rd party broker. It includes options to map the source data (the data on the broker) to a destination format.  
The mapping can be done using command variables, or by associating a mapping policy (from the metadata). See details below.

**Usage:**
<pre class="code-frame"><code class="language-anylog">&lt;run msg client where 
  broker = [url] and port = [port] and 
  user = [user] and password = [password] and log=[true/false] 
  topic = (
    name = [topic name] and 
    dbms = [dbms name] and 
    table = [table name] and 
    [participating columns info]
)&gt;</code></pre>

**Explanation:**  Subscribe to a broker according to the URL provided to receive data on the provided topic.

**Examples:**
<pre class="code-frame"><code class="language-anylog">&lt;run msg client where 
  broker = "driver.cloudmqtt.com" and port = 18975 and 
  user = mqwdtklv and password = uRimssLO4dIo and 
  topic = (
    name = test and 
    dbms = "bring [metadata][company]" and 
    table = "bring [metadata][machine_name] _ [metadata][serial_number]" and 
    column.timestamp.timestamp = "bring [ts]" and 
    column.value.int = "bring [value]"
)&gt;
</code></pre>

**Details:** [Message Client](https://github.com/AnyLog-co/documentation/blob/master/message%20broker.md#subscribing-to-a-third-party-broker)

### Get subscription info
Get configuration and statistics information from the subscription process. 

**Usage:**
<pre class="code-frame"><code class="language-anylog">get msg clients where [options]</code></pre>

**Explanation:** Information on messages received by clients subscribed to message brokers.
      
**Examples:**
<pre class="code-frame"><code class="language-anylog">get msg clients
get msg client where id = 3
get msg client where topic = anylogedgex
get msg client where broker = driver.cloudmqtt.com:18785 and topic = anylogedgex
</code></pre>

**Details:** [get msg client](https://github.com/AnyLog-co/documentation/blob/master/monitoring%20calls.md#get-msg-clients)

## Subscribe to Kafka

The command is similar to the [run msg client](#subscribe-to-a-broker) command. Monitoring is with the [get msg client](#get-subscription-info) command.

**Usage:**
<pre class="code-frame"><code class="language-anylog">&lt;run kafka consumer where 
  ip = [ip] and port = [port] and 
  reset = [latest/earliest] and 
  topic = [topic and mapping instructions]&gt;
</code></pre>

**Explanation:** Initialize a Kafka consumer that subscribes to one or more topics of a kafka instance and continuously 
polls data assigned to the subscribed topics using the provided IP and Port. The reset value determines the offset whereas the default is latest.

**Examples:**
<pre class="code-frame"><code class="language-anylog">&lt;run kafka consumer where 
  ip = 198.74.50.131 and port = 9092 and 
  reset = earliest and topic = (
    name = sensor and 
    dbms = lsl_demo and 
    table = ping_sensor and 
    column.timestamp.timestamp = "bring [timestamp]" and 
    column.value.int = "bring [value]"
)&gt;
</code></pre>

**Details:** [Using Kafka](https://github.com/AnyLog-co/documentation/blob/master/using%20kafka.md#using-kafka).

## gRPC Client Service

Subscribe to a gRPC broker and monitor the data flow.
* [run grpc client](#enable-grpc-client-service)
* [get grpc client](#get-grpc-connection-info)

### Enable gRPC client service
**Usage:**
<pre class="code-frame"><code class="language-anylog">run grpc client where name = [unique name] and ip = [IP] and port = [port] and policy = [policy id]</code></pre>

**Explanation:** Subscribe to a gRPC broker on the provided IP and Port and map data using the designated mapping policy.

**Examples:**
<pre class="code-frame"><code class="language-anylog">run grpc client where name = kubearmor and ip = 127.0.0.1 and port = 32767 and policy = deff520f1096bcd054b22b50458a5d1c</code></pre>

**Details:** [Using gRPC](https://github.com/AnyLog-co/documentation/blob/master/using%20grpc.md#using-grpc).

### Get gRPC connection info
List the active gRPC clients and the data exchange info.

**Usage:**
<pre class="code-frame"><code class="language-anylog">get grpc client</code></pre>


##  Enable smtp client service

**Usage:**
<pre class="code-frame"><code class="language-anylog">&lt;run smtp client where 
  host = [host name] and port = [port] and 
  email = [email address] and password = [email password] and 
  ssl = [true/false]&gt;
</code></pre>

**Explanation:** Initiates an SMTP instance encapsulates an SMTP connection to a server.

**Examples:**
<pre class="code-frame"><code class="language-anylog">run smtp client where email = anylog.iot@gmail.com and password = google4anylog</code></pre>

**Details:** [SMTP Client](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#smtp-client).

## The Scheduler Services
Users can enable multiple schedulers. A scheduler contains a group of tasks that are executed periodically.
* [run scheduler](#run-scheduler) - Enable the service.    
* [get scheduler](#get-scheduler) - Get the scheduler service info.

A detailed description is available in the [](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring) section.

### Run Scheduler

**Usage:**
<pre class="code-frame"><code class="language-anylog">run scheduler [id]</code></pre>

<code class="language-anylog">[id]</code> - Optional value, representing the scheduler ID. The default value is 1, representing a user scheduler.

**Explanation:**  Repeatedly execute scheduled jobs.

**Examples:**
<pre class="code-frame"><code class="language-anylog">run scheduler 1</code></pre>

**Details:** [The Scehdualer](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#invoking-a-scheduler).

### Get Scheduler
Monitor the scheduler

**Usage:**
<pre class="code-frame"><code class="language-anylog">get scheduler [n]</code></pre>

**Explanation:** Information on the scheduled tasks. [n] - an optional ID for the scheduler. Scheduler 1 manage user scheduled tasks, 0 is the system scheduler. 

**Examples:**
<pre class="code-frame"><code class="language-anylog">get scheduler
get scheduler 1
</code></pre>

**Details:** [View Scheduled Commands](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#view-scheduled-commands).


## Blob Archiver Services
The Blob Archiver is a service that manage blob data on the node.
* [Enable the blobs archiver service](#enable-the-blobs-archiver-service)
* [Get blobs archiver info](#get-blobs-archiver-info)
 
### Enable the blobs archiver service
  
**Usage:**
<pre class="code-frame"><code class="language-anylog">&lt;run blobs archiver where 
  blobs_dir = [data directory location] and archive_dir = [archive directory location] and 
  dbms = [true/false] and file = [true/false] and compress = [true/false]&gt;</code></pre>

**Explanation:**  Archive large objects.

**Examples:**
<pre class="code-frame"><code class="language-anylog">run blobs archiver where dbms = true and file = true and compress = false</code></pre>

**Details:** [The Blobs Archiver]( https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#the-blobs-archiver).

### Get blobs archiver info
Return information on the Blobs Archiver processes.

**Usage:**
<pre class="code-frame"><code class="language-anylog">get blobs archiver</code></pre>
