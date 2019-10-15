# Issuing requests and info requests to the AnyLog Network

Queries (and info requests) can be issued from any REST client to the AnyLog Network. Any node member of the network can be configured to serve as a REST server to satisfy client requests. 

## The server side:

Configuring a node is by issuing an AnyLog command: 
```
	run rest server [host] [port] [timeout]
```
Whereas host and port are the connection information and the timeout value represent the max time that a request will wait for a query reply (the default is 20 seconds).

## The client side:

Using a REST client, connect to a network node configured to provide REST services. 
There are 2 types of commands that can be issued: Info commands and SQL commands. Info commands provide info on the metadata and the SQL commands are queries issued to the network.

Requests are done using the GET command with keys and values in the headers as detailed below.

#### Status Requests:
To retrieve the status of the node:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   info
details                get status
</pre>

To retrieve the last executed query:
<pre>
Header Key             Header Value            
--------------         ------------------
type                   info
details                job status
</pre>

To retrieve the last executed queries:
<pre>
Header Key             Header Value            
--------------         ------------------
type                   info
details                job status all
</pre>

#### Metadata Requests:
To retrieve the list of tables in a database:
<pre>
Header Key             Header Value          
--------------         ------------------
type                   info
dbms                   [the logical database name]
details                info dbms [the logical database name] tables
</pre>

To retrieve columns info of a particular table:
<pre>
Header Key             Header Value            
--------------         ------------------
type                   info
dbms                   [the logical database name]
details                info table [the logical database name] [the logical table name] columns
</pre>
