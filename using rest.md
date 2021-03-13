# Using REST

## Overview

Users can interact with the nodes in the network using REST.  
Using REST, users can execute AnyLog commands over HTTP on any node in the network that is configured to satisfy REST requests.

## Prerequisites

* A rest client software like [Curl](https://man7.org/linux/man-pages/man1/curl.1.html) or [Potman](https://www.postman.com/).
* An AnyLog Node that provides a REST connection.
To configure an AnyLog Node to satisfy REST calls, issue the following command on the AnyLog command line:  
```run rest server [ip] [port] [max time]```  
[ip] and [port] are the IP and Port that would be available to REST calls.  
[max time] is an optional value that determines the max execution time in seconds for a call before being aborted.  
A 0 value means a call would never be aborted and the default time is 20 seconds.    
Additional information on the REST API is available at the section [Rest requests](https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-request).
  
## HTTP methods suported

AnyLog commands are supported using the the HTTP methods GET, PUT and POST.  
***GET*** is used to retrieve information.  
***PUT*** is used to add data to nodes in the network.  
***POST*** is used as a default method to execute all other AnyLog commands.  

### The AnyLog commands supported by GET

| HTTP Method   | AnyLog commands  | Comments | 
| ------------- | -----------------|  ------|
| GET           | sql              | Issue queries to data hosted by nodes of the network network |
|               | get              | Retrieve information from nodes members of the network |
|               | blockchain get   | Query the metadata |
|               | help             | Help on the ANyLog commands |

#### Exampless

<pre>
curl --location --request GET '10.0.0.78:7849' \
--header 'destination: network' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: sql orics "select count(*) from heater_temperature_1"'
</pre>

<pre>
curl --location --request GET '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: blockchain get operator where company = anylog'
</pre>


### Using PUT to add data to nodes in the network.

Details are provided in  the section [Data transfer using a REST API](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#data-transfer-using-a-rest-api).


### Using POST request to execute an AnyLog commands

POST supports all other commands. Some examples are:

| HTTP Method   | AnyLog commands  | Comments | 
| ------------- | -----------------|  ------|
| POST          | set              | Set values or change status |
|               | reset            | Reset values or status |
|               | blockchain       | Manage metadata commands (note the ***blockchain get*** is supported using GET.  |

#### Example
<pre>
curl --location --request POST '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: reset error log'
</pre>

## Headers setup

The header seup for the PUT command is detailed in the section [Configuring the Sender Node](https://github.com/AnyLog-co/documentation/blob/master/adding%20data.md#configuring-the-sender-node-a-client-node-which-is-not-necessarily-a-member-of-the-anylog-network).  
The header setup for GET and POST is the following:

| Key        | Value  |
| ---------- | -------| 
| command    | The AnyLog command to execute. |
| destination | The list of IPs and Ports which are the destination of the command. |
| User-Agent | AnyLog/1.23 |


* Options for ***destination***:

| Option     | Comment  |
| ---------- | -------| 
| A comma separated IPs and Ports | The command will be delivered on all the specified destinations. |
| local |  The destination is the connected node. | 
| Not specified |  Same as local. |
| network | For SQL queries, if destination is ***network***, the network protocol will resolve the destination based on a database name and a table name derived from the command. |

* Options ***User-Agent***:  
Needs to specify "AnyLog" as the product followed by the version. 
  The value of this header determines the client product and how requests are processed. 
  For example, Grafan visualization is using the AnyLog REST API and processing is using this header to determine mapping to Grafana API.

## The message body setup

The message body can include commands that are needed to be executed before the command specified in the header.  
The typical use case are assignments of values to parameters.

Each line in the body segment is assumed to be an independent command.
Commands that broken over multiple lines are enclosed between the signs ***<*** and ***>***.

### Example

<pre>

curl --location --request POST '172.18.12.129:2149' \
--header 'command: blockchain push !operator' \
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
</pre> 

 


