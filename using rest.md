# Using Grafana

## Overview

Users can interact with the nodes in the network using REST.  
Using REST, users can execute AnyLog commands over HTTP on any network member that is configured to satisfy REST requests.

## Prerequisites

* A rest client software like [Curl](https://man7.org/linux/man-pages/man1/curl.1.html) or [Potman](https://www.postman.com/).
* An AnyLog Node that provides a REST connection.
To configure an AnyLog Node to satisfy REST calls, issue the following command on the AnyLog command line:  
```run rest server [ip] [port] [max time]```  
[ip] and [port] are the IP and Port that would be available to REST calls.  
[max time] is an optional value that determines the max execution time in seconds for a call before being aborted.  
A 0 value means a call would never be aborted and the default time is 20 seconds.  

## Using POST request to execute an AnyLog command

### Headers setup

| Key        | Value  |
| ---------- | -------| 
| command    | The AnyLog command to execute. |
| destination | The list of IPs and Ports which are the destination of the command. |


Options for destination:

| Option     | Comment  |
| ---------- | -------| 
| A comma separated IPs and Ports | The command will be delivered on all the specified destinations. |
| local |  The destinaruion is the connected node. | 
| Not specified |  Same as local. |
| network | For SQL queries, if destination is ***network***, the network protocol will resolve the destination based on a database name and a table name derived from the command. |

### The message body setup

The message body can include commands that are needed to be executed before the command specified in the header.  
The typical use case are assignments of values to parameters.

Each line in the body segment is assumed to be an independent command.
Commands that broken over multiple lines are enclosed between the signs ***<*** and ***>***.

### Example

curl --location --request POST '172.18.12.129:2149' \
--header 'command: blockchain add !operator' \
--header 'destination: !master_node' \
--header 'Content-Type: text/plain' \
--data-raw 'operator_name = anylog_node_323
<operator = {“operator” : {“cluster” : “7a00b26006a6ab7b8af4c400a5c47f2a”,
                “name” = !operator_name,
                “ip” : “10.0.0.78”,
                “port” : 2048,
                “id” : “1be222b10132005d6d141beecb589ead”,
                “date” : “2021-01-30T00:45:35.079162Z”,
                “member” : 111669}}>'
 

 


