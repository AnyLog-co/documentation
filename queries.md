**Issuing queries to the AnyLog Network**

Using a REST client, connect to a node in the AnyLog network.
Any node in the network can serve as a REST server and accept requests from clients, however, the node needs to be configured to provide the REST service.
Configuring a node is by issuing the command: 
	run rest server [host] [port] [timeout]
Whereas host and port are the connection information and the timeout value represent the max time that a request will wait for a query reply (the default is 20 seconds).
 There are 2 types of commands that can be issued: Info commands and SQL commands. 
Commands are send using GET and the headers are set with keys and values to detail the command.

Key       Value    Comments
-----      -------    -----------------------
type   info        status or metadata information
type   sql          SQL query
dbms                dbms name (for SQL queries)
detail  info or query string

