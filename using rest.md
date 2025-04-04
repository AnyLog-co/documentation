# Using REST

## Overview

Users can interact with the nodes in the network using REST.  
Using REST, users can execute AnyLog commands over _HTTP_ on any node in the network that is configured to satisfy REST requests.

## Prerequisites

* A REST client software like [cURL](https://man7.org/linux/man-pages/man1/curl.1.html) or [Postman](https://www.postman.com/).
* An AnyLog Node that provides a REST connection.
To configure an AnyLog Node to satisfy REST calls, issue the following command on the AnyLog command line:  
```anylog
run rest server [ip] [port] [max time]
```

[ip] and [port] are the IP and Port that would be available to REST calls.  
[max time] is an optional value that determines the max execution time in seconds for a call before being aborted.  
A 0 value means a call would never be aborted and the default time is 20 seconds.    
Additional information on the REST API is available at the section [REST requests](background%20processes.md#rest-requests).
  
## HTTP methods supported

AnyLog commands are supported using the _HTTP_ methods `GET`, `PUT` and `POST`.  
* _GET_ is used to retrieve information.  
* _PUT_ is used to add data to nodes in the network.  
* _POST_ is used as a default method to execute all other AnyLog commands.  

### The AnyLog commands supported by REST

| AnyLog command | HTTP Method       | Comments                                                                       | 
|----------------|-------------------|--------------------------------------------------------------------------------|
| GET            | sql               | Issue queries to data hosted by nodes of the network network                   |
| GET            | help              | Help on the AnyLog commands                                                    |
| GET            | get               | Retrieve information from nodes members of the network                         |
| GET            | blockchain get    | Query the metadata that is considered by the node                              |
| GET            | blockchain read   | Query the disk image of the metadata                                           |
| POST           | blockchain drop   | Drop a policy                                                                  |
| GET            | query status      | Retrieve the status of the currently or previous executed queries              |
| GET            | query explain     | Explain how the currently or previous queries are processed                    |
| GET            | query destination | Detail the participating nodes in each query                                   |
| GET            | job status        | Retrieve status info on jobs assigned to the rule engine                       |
| GET            | job active        | Retrieve status info on the currebly executed jobs assigned to the rule engine |
| POST           | job run           | Execute a specific job assigned to the rule engine                             |
| POST           | job stop          | Stop the execution of a specific job assigned to the rule engine               |
| GET            | file get          | Copy a file from a remote node to the local node                               |
| GET            | file retrieve     | Retrieve a file or files from the designated database                          |
| POST           | file store        | Insert a file into the blobs dbms                                              |
| POST           | file to           | copy a file to a folder                                                        |
| GET            | test              | Issue a test command                                                           |
| POST           | reset             | Issue a reset command                                                          |
| POST           | process           | process an AnyLog script file                                                  |

#### Examples

```anylog
curl --location --request GET '10.0.0.78:7849' \
--header 'destination: network' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: sql orics "select count(*) from heater_temperature_1"'
```

```anylog
curl --location --request GET '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: blockchain get operator where company = anylog'
```

```anylog
curl --location --request POST '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: reset error log'
```

The following example is using HTTP request to copy a configuration file to an AnyLog node and process the file.  
Details on the **file store** command are available [here](image%20mapping.md#insert-a-file-to-a-local-database)
```anylog
curl -X POST -H "command: file to where dest = !demo_dir/operator_28.al" -F "file=@new_config.al" http://10.0.0.78:7849
curl -X POST -H "command: process !demo_dir\operator_28.al" http://10.0.0.78:7849
```
Details are available at the [file to](file%20commands.md#copy-a-file-to-a-folder) section.


### Using PUT to add data to nodes in the network.

Details are provided in  the section [Data transfer using a REST API](adding%20data.md#data-transfer-using-a-rest-api).

## Headers setup

The header setup for the PUT command is detailed in the section [Configuring the Sender Node](adding%20data.md#configuring-the-sender-node--a-client-node-which-is-not-necessarily-a-member-of-the-anylog-network--).  
The header setup for GET and POST is the following:

| Key        | Value  |
| ---------- | -------| 
| command    | The AnyLog command to execute. |
| destination | The list of IPs and Ports which are the destination of the command. |
| User-Agent | AnyLog/1.23 |


* Options for _destination_:

| Option                           | Comment                                                                                                                                                               | 
|----------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
|  A comma separated IPs and Ports | The command will be delivered on all the specified destinations.                                                                                                      |                                                                                                      
| local                            | The destination is the connected node.                                                                                                                                |
| Not specified                    | Same as local.                                                                                                                                                        |
| network                          | For SQL queries, if destination is **network**, the network protocol will resolve the destination based on a database name and a table name derived from the command. |

* Options _User-Agent_:  
Needs to specify "AnyLog" as the product followed by the version. 
  The value of this header determines the client product and how requests are processed. 
  For example, Grafana visualization is using the AnyLog REST API and processing is using this header to determine mapping to Grafana API.

## The message body setup

The message body can include commands that are needed to be executed before the command specified in the header.  
The typical use case are assignments of values to parameters.

Each line in the body segment is assumed to be an independent command.
Commands that broken over multiple lines are enclosed between the signs **<** and **>**.

### Example

```shell
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
``` 

## Subscribing to REST calls 

Users can associate REST calls with topics and subscribe to the topics such that when data is added, the subscription logic applies to the data.  
This process is done as follows:

1. Define a MQTT client, assign the broker to _REST_ and identify the User-Agent on the rest calls.     
   
   Example: 
  ```anylog
  <run mqtt client where broker=rest and 
    user-agent = anylog and 
    topic = (
        name = opcua and 
        dbms = "bring [dbms]" and 
        table = "bring [table]" and 
        column.timestamp.timestamp = "bring [ts]" and 
        column.value.float = "bring [value]"
    )> 
  ```
    
  Notes:  
  a) The User-Agent request header is a characteristic string that lets servers and network peers identify the application, operating system, vendor, and/or version of the requesting user agent.  
  b) Details on the `rum mqtt client` command are available in the [Using MQTT Broker](message%20broker.md) section.

2. Issue REST calls to the AnyLog node.  
   Example:  
```shell
curl --location --request POST '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: data' \
--header 'Content-Type: text/plain' \
--data-raw ' [{"dbms" : "dmci", "table" : "fic11", "value": 50, "ts": "2019-10-14T17:22:13.051101Z"},
 {"dbms" : "dmci", "table" : "fic16", "value": 501, "ts": "2019-10-14T17:22:13.050101Z"},
 {"dbms" : "dmci", "table" : "ai_mv", "value": 501, "ts": "2019-10-14T17:22:13.050101Z"}]'
```