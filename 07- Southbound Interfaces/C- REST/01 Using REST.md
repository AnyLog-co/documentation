---
title: Using REST
description: Execute AnyLog commands and publish data over HTTP using GET, PUT, and POST.
layout: page
---

<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**                                                                                     | **Version** |
 |------------|----------------|------------------------------------------------------------------------------------------------|----------|
 | 2026-07-20 | Eric Aquaronne | added change log                                                                               | 2.0.2606 |
 | 2026-04-25 |                | hyperlink support                                                                                               |  |
 | 2026-04-25 |                | REST GET via browser support                                                                                               |  |
 | 2026-04-24 |                | there was an issue with the REST POST of commands example                                      |  |
 | 2026-04-23 |                | added POST as GET alternative, AnyLog-Agent header, blockchain insert command, Python examples |  |
 | 2026-04-17 |                | creation                                                                                       |  |
--->

Any AnyLog node with the REST service enabled, can receive commands and data over HTTP. This lets external applications, 
dashboards, and scripts interact with the network without running AnyLog themselves.

---

## HTTP method mapping

| Method | Used for |
|---|---|
| `GET` | Retrieve information — `sql`, `get`, `blockchain get`, `help` |
| `GET` (query string) | Browser-native GET — command and options passed as `?key=value?key=value` parameters |
| `POST` | All commands (alternative to GET) and data publishing via topic mapping |
| `PUT` | Publish time-series data directly to a node |



## Trace REST calls

Users can trace the REST calls using the following command:

```anylog
trace level = 1 run rest server
```


### The AnyLog commands supported by REST

| AnyLog command | HTTP Method       | Comments | 

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
Details on the **file store** command are available [here](/docs/adding%20data.md#insert-a-file-to-a-local-database)
```anylog
curl -X POST -H "command: file to where dest = !demo_dir/operator_28.al" -F "file=@new_config.al" http://10.0.0.78:7849
curl -X POST -H "command: process !demo_dir\operator_28.al" http://10.0.0.78:7849
```
Details are available at the [file to](/docs/file%20commands.md#copy-a-file-to-a-folder) section.


### Using PUT to add data to nodes in the network.

Details are provided in the section [Data transfer using a REST API](/docs/adding%20data.md#data-transfer-using-a-rest-api).


### Headers setup

The header setup for the PUT command is detailed in the section [Configuring the Sender Node](/docs/adding%20data.md#configuring-the-sender-node-a-client-node-which-is-not-necessarily-a-member-of-the-anylog-network). 
The header setup for GET and POST is the following:

| Key        | Value  | 
| ---------- | -------| 
| command    | The AnyLog command to execute. |
| destination | The list of IPs and Ports which are the destination of the command. |
| User-Agent | AnyLog/1.23 |

* Options for _destination_:

| Option | Comment | 
|---|---| 
| A comma separated IPs and Ports | The command will be delivered on all the specified destinations. | 
| local | The destination is the connected node. | 
| Not specified | Same as local. | 
| network | For SQL queries, if destination is **network**, the network protocol will resolve the destination based on a database name and a table name derived from the command. |

* Options _User-Agent_: 
Needs to specify "AnyLog" as the product followed by the version. 
The value of this header determines the client product and how requests are processed. 
For example, Grafana visualization is using the AnyLog REST API and processing is using this header to determine mapping to Grafana API.


### The message body setup

The message body can include commands that are needed to be executed before the command specified in the header. 
The typical use case are assignments of values to parameters.

Each line in the body segment is assumed to be an independent command.
Commands that broken over multiple lines are enclosed between the signs **<** and **>**.

#### Example

```shell
curl --location --request POST '172.18.12.129:2149' \
--header 'command: blockchain push !operator' \
--header 'destination: !master_node' \
--header 'Content-Type: text/plain' \
--data-raw 'operator_name = anylog_node_323
<operator = {"operator" : {"cluster" : "7a00b26006a6ab7b8af4c400a5c47f2a",
            "name" = !operator_name,
            "ip" : "10.0.0.78",
            "port" : 2048,
            "id" : "1be222b10132005d6d141beecb589ead",
            "date" : "2021-01-30T00:45:35.079162Z",
            "member" : 111669}}>'
```


### Subscribing to REST calls 

Users can associate REST calls with topics and subscribe to the topics such that when data is added, the subscription logic applies to the data.  
This process is done as follows:

1. Define a message client, assign the broker to _REST_ and identify the User-Agent on the rest calls.     
   
   Example: 
  ```anylog
  <run msg client where broker=rest and 
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
  b) Details on the `run msg client` command are available in the [Using MQTT Broker](/docs/message%20broker.md) section.

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


## Specifying commands in the message URL

Users can embed commands and instructions directly in the **message URL** instead of specifying them in HTTP headers.  
This provides a simple way to issue REST requests from environments where setting headers is not convenient (for example, browsers or simple REST clients).

In this method, parameters that normally appear in the headers—such as `User-Agent`, `destination`, and `command`—are included in the URL.

Each `?` in the URL represents a **header directive** and is interpreted by the AnyLog REST server as a header key-value pair.

### Syntax
```AnyLog
http://<node_ip>:<port>/?<header>=<value>?<header>=<value>?<header>=<value>
```

### Example 1 – Retrieve node status:
```AnyLog
http://10.0.0.78:7849/?User-Agent=AnyLog/1.23?command=get status
```

Equivalent request using HTTP headers:

```anylog
curl --request GET '10.0.0.78:7849' \
--header 'User-Agent: AnyLog/1.23' \
--header 'command: get status'
```

### Example 2 – Execute a SQL query across the network

```AnyLog
http://10.0.0.78:7849/?User-Agent=AnyLog/1.23?destination=network?command=sql lsl_demo format=table select * from ping_sensor
```

This request executes a SQL query across the network:

```AnyLog
sql lsl_demo format=table select * from ping_sensor
```

Parameters interpreted from the URL:

| URL Parameter | Equivalent Header | 
|---------------|-----------------------------------------------------|
| User-Agent    | AnyLog/1.23 | 
| destination   | network | 
| command       | sql lsl_demo format=table select * from ping_sensor |


## Specifying commands in the message body

When using the **POST** HTTP method, users can include commands directly in the **message body** instead of using headers or URL parameters.

In this approach, the message body contains a **JSON structure** describing the command to execute.  
The AnyLog REST server parses the JSON payload and executes the corresponding AnyLog command.

### JSON structure

The message body supports the following key–value pairs:

| Key | Description |
|---|---|
| `command` | An AnyLog command to execute. |
| `dbms` | The database name used for executing a SQL statement. |
| `sql` | The SQL statement to execute on the specified database. |

The commands derived from these fields are interpreted and executed by the AnyLog node receiving the request.

---

### Example 1 – Executing an AnyLog command

```anylog
curl --location --request POST 'http://10.0.0.78:7849' \
--header 'Content-Type: application/json' \
--data '{
  "command": "get status"
}'
```

This request executes the following AnyLog command on the node:
```anylog
get status
```

### Example 2 – Executing a SQL query
```anylog
curl --location --request POST 'http://10.0.0.78:7849' \
--header 'Content-Type: application/json' \
--data '{
  "dbms": "lsl_demo",
  "sql": "select * from ping_sensor"
}'
```

This request executes the SQL command:
```anylog
sql lsl_demo select * from ping_sensor
```

Notes:
* The request must use the POST method.
* The body must be formatted as valid JSON.


---

## Headers and the AnyLog-Agent

Every request requires an identity header. AnyLog accepts either `User-Agent` or `AnyLog-Agent`:

| Header | Value | Notes |
|---|---|---|
| `User-Agent: AnyLog/1.23` | Standard HTTP header | Works in server-side scripts (curl, Python `requests`, etc.) |
| `AnyLog-Agent: AnyLog/1.23` | Custom AnyLog header | **Preferred when calling from a browser** — avoids CORS preflight (see below) |

Both are accepted by the node and treated identically. For server-side code either works. For browser-based clients, use `AnyLog-Agent`.

### Why AnyLog-Agent for browser clients

Browsers treat `User-Agent` as a reserved header — `fetch()` cannot set it manually, and its presence in a cross-origin 
request triggers a CORS preflight (`OPTIONS`) that AnyLog nodes are not configured to answer. `AnyLog-Agent` is a 
custom header that both the browser and the node control explicitly, allowing the node to whitelist it:

```
Access-Control-Allow-Headers: AnyLog-Agent, Content-Type
```

See <a href="/docs/network-services/using-rest/#rest-service">Network and Services — REST service</a> 
and the <a href="https://github.com/AnyLog-co/MCP-Examples" target="_blank">MCP-Examples CORS guide</a> for 
proxy-based solutions when direct browser access is not possible.

---

## GET requests

GET passes the command and options as HTTP headers.

### Common GET headers

| Header | Description |
|---|---|
| `command: [anylog command]` | The command to execute |
| `User-Agent: AnyLog/1.23` | Required (or `AnyLog-Agent: AnyLog/1.23`) |
| `destination: network` | Route a query across all relevant nodes |
| `destination: [IP:Port]` | Send to a specific node |

### Check node status
```bash
curl -X GET 'http://10.0.0.78:32349'   -H 'command: get status'   -H 'User-Agent: AnyLog/1.23'
```

### Get running processes
```bash
curl -X GET 'http://10.0.0.78:32349'   -H 'command: get processes'   -H 'User-Agent: AnyLog/1.23'
```

### Query metadata
```bash
curl -X GET 'http://10.0.0.78:32349'   -H 'command: blockchain get operator where company="AnyLog Co."'   -H 'User-Agent: AnyLog/1.23'
```

### SQL query across the network
```bash
curl -X GET 'http://10.0.0.78:32349'   -H 'command: sql mydb format=table "select * from rand_data where timestamp >= now() - 1 minute limit 10"'   -H 'User-Agent: AnyLog/1.23'   -H 'destination: network'   -w "\n"
```

> Always add `-w "\n"` to GET/SQL requests to avoid chunked-encoding display issues.

### Get help
```bash
curl -X GET 'http://10.0.0.78:32349'   -H 'command: help blockchain get'   -H 'User-Agent: AnyLog/1.23'
```

### Browser GET (query string)

When calling from a browser directly — where custom headers cannot be set — pass the command and options as query 
string parameters instead. Each parameter is separated by `?` rather than `&`:

```
http://10.0.0.78:7849/?command=get status?AnyLog-Agent=AnyLog/1.23

http://10.0.0.78:7849/?command=sql anotherpeak select * from battery_pack_logs where period(minute, 5, now(), timestamp) limit 10?AnyLog-Agent=AnyLog/1.23?destination=network
```

| Parameter | Description |
|---|---|
| `command` | The AnyLog command to execute |
| `AnyLog-Agent` | Identity header — use `AnyLog/1.23` |
| `destination` | Optional — `network` to broadcast, or `IP:Port` for a specific node |

> Note the separator between parameters is `?` not `&` — this is specific to AnyLog's query string parsing and differs 
> from standard URL convention.

This is the browser equivalent of the curl GET style. For browser-based applications making programmatic calls, prefer 
[POST with `AnyLog-Agent` in the body](#post-as-an-alternative-to-get) — it gives more control and avoids query string 
length limits.

---

## POST requests

POST serves four distinct purposes in AnyLog:

| Use | Description |
|---|---|
| Publish Data | Ingest time-series data via topic mapping (`run msg client` with `broker=rest`) |
| Publish metadata | Insert policies to the blockchain via `blockchain insert` |
| Execute commands | Send any AnyLog command to the node — same as GET but via JSON body |
| GET via JSON body | Pass GET-style headers as JSON keys — useful where custom HTTP headers are restricted |

---

### Publishing Data via POST

The logic with publishing data via _POST_ allows for a simple logic for getting data into AnyLog with the behavior 
of MQTT's [mapping policies](/docs/Managing-Data-Southbound/mapping-policies) logic.  

As such, POST data publishing requires a `run msg client` with `broker=rest` active on the receiving node. This maps 
incoming JSON fields to a target database and table; thus the actual idea of publishing data (entirely via REST). 

1. **Define Mapping Policy** - The policy describes how incoming JSON fields map to database columns:

```json
{
   "mapping": {
      "id": "my-mappigng1",
      "dbms": "bring [dbms]",
      "table": "bring [table]",
      "readings": "",
      "schema": {
         "timestamp": {
            "default": "now()", 
            "type": "timestamp",
            "bring": "[timestamp]"
         },
         "value": {
            "default": null,
            "type": "float",
            "bring": "[value]"
         }
     }
 }
```

2. **Publish Policy** - Publish mapping policy to the blockchain, this would be used in `run msg client` to understand the data coming in. 

```shell
curl -X POST 'http://10.0.0.69:32149'   -H 'command: blockchain insert where policy=!new_policy and local=true and master_node=!ledger_conn'   -H 'AnyLog-Agent: AnyLog/1.23'   --data-raw '<new_policy={"mapping": {
    "id": "my-mapping1",
    "dbms": "bring [dbms]",
    "table": "bring [table]",
    "readings": "",
    "schema": {
      "timestamp": {
        "default": "now()",
        "type": "timestamp",
        "bring": "[timestamp]"
      },
      "value": {
        "default": null,
        "type": "float",
        "bring": "[value]"
      }
    }
  }}>'
```

3. **Define `msg client`**  - Start message client logic on the operator node 

```shell
curl -X POST 'http://10.0.0.69:32149'    -H "command: run msg client where broker=rest and user-agent=anylog and log=false topic=(name=my-topic and policy=my-mapping1)"    -H "User-Agent: AnyLog/1.23"
```

4. **Publish data** - In the example all the JSON keys would be mapped to the mapping policy. 

```bash
curl -X POST 'http://10.0.0.69:32149'   -H 'command: data'   -H 'topic: my-topic'   -H 'User-Agent: AnyLog/1.23'   -H 'Content-Type: text/plain'   --data-raw '[{
    "dbms": "mydb", "table": "sensor_data", "value": 50, "timestamp": "2019-10-14T17:22:13Z"},
    {"dbms": "mydb", "table": "sensor_data", "value": 55, "timestamp": "2019-10-14T17:22:14Z"}
  ]'
```

5. **Validate data is being received** - using `get streaming` validate data is being inserted - this is usually done via REST-GET, however, in order to show 
the full scope of how to utilize POST, the example check the streaming status for operator (`10.0.0.69:32149`) through the 
query node `10.0.0.69:32349`. 
 
```shell
curl -X POST 'http://10.0.0.69:32349'   -H "Content-Type: application/json"   -d '{"command": "get streaming", "User-Agent: AnyLog/1.23", "destination": "10.0.0.69:32148"}'
```

> Full working examples can be found in
> <a href="#" onclick="openEnvModal('/assets/examples/sample-post.py'); return false;">sample-post.py</a>

---

### Execute commands via POST

POST can execute any AnyLog command by passing the command as an HTTP header, and can be used to bring services up and 
down as needed without interacting with the actual [CLI](/docs/CLI/AnyLog-CLI). Thus Anylog be configured or altered 
through third-party apps, via our API or simply when [running as a service](/docs/Getting-Started/anylog-as-service)
and the CLI is not enabled.

**Connect to logical database**
```bash
curl -X POST 'http://10.0.0.78:32349'   -H "command: connect dbms mydb where type=sqlite "   -H "AnyLog-Agent: AnyLog/1.23"
```

**Reset the error log**
```bash
curl -X POST 'http://10.0.0.78:32349'   -H "command: reset error log"   -H "AnyLog-Agent: AnyLog/1.23"
```

**Set a variable**
```bash
curl -X POST 'http://10.0.0.78:32349'   -H "command: set company_name = AnyLog"   -H "AnyLog-Agent: AnyLog/1.23"
```

---

### POST as an alternative to GET

[_GET_](#get-requests) is the most common, and probably most natural form, of executing requests against via cURL. 
However, it is far more limited in fetch logic and may not be supported with all tooling example Kubernetes and some
browser-based GUIs; often preferring POST with JSON bodies in order to bypass their security restrictions. For those 
cases, AnyLog accepts GET request as POST, where the GET headers become the serialized JSON body content of the request. 

In addition, `AnyLog-Agent` as opposed to `User-Agent` is often prefer with browser-through requests as browsers 
silently ignore any attempt to set User-Agent manually, and its presence in a cross-origin request triggers a CORS 
preflight that AnyLog nodes are not configured to answer. 

Essentially, `AnyLog-Agent` is a custom header that both sides control, so the node can explicitly whitelist it and 
browsers can set it without restriction.

**GET style**:
* basic `get status`
```bash
curl -X GET 'http://10.0.0.69:32349'   -H 'command: get status'   -H 'AnyLog-Agent: AnyLog/1.23'
```

* Query against the data
```bash
curl -X GET 'http://10.0.0.69:32349'   -H "command: sql mydb format=json:list and stat=false select * from sensor_data where timestamp >= now() - 1 minute limit 10"   -H "AnyLog-Agent: AnyLog/1.23"   -H "destination: network"   -w "\n"
```

**Equivalent POST style**:
* basic `get status`
```bash
curl -X POST 'http://10.0.0.69:32349'   -H 'Content-Type: application/json'   -d '{"command": "get status", "AnyLog-Agent": "AnyLog/1.23"}'
```

* Query against the data
```bash
curl -X POST 'http://10.0.0.69:32349'   -H 'Content-Type: application/json'   -d '{
    "command": "sql mydb format=json:list and stat=false select * from sensor_data where timestamp >= now() - 1 minute limit 10",
    "AnyLog-Agent": "AnyLog/1.23",
    "destination": "network"
  }'   -w "\n"
```

Both return the same response. Use `AnyLog-Agent` in the body when calling from a browser.

---

## PUT requests — publish data directly

PUT bypasses topic mapping entirely. The target database and table are specified directly in the request headers, and 
data is written to the node immediately (or buffered in streaming mode).

### Required headers

| Header | Description |
|---|---|
| `type: json` | Data format (default) |
| `dbms: [name]` | Target logical database |
| `table: [name]` | Target logical table |
| `mode: streaming` | Optional — buffer data instead of writing immediately |
| `User-Agent: AnyLog/1.23` | Required (or `AnyLog-Agent: AnyLog/1.23`) |
| `Content-Type: text/plain` | Required |

### curl example

```bash
curl -X PUT 'http://10.0.0.78:32149'   -H 'type: json'   -H 'dbms: mydb'   -H 'table: sensor_data'   -H 'mode: streaming'   -H 'Content-Type: text/plain'   -H 'User-Agent: AnyLog/1.23'   -w "\n"   --data-raw '[{
    "device_name": "sensor-01", "value": 42.5, "timestamp": "2024-01-01T10:00:00Z"},
    {"device_name": "sensor-01", "value": 43.1, "timestamp": "2024-01-01T10:00:01Z"}
  ]'
```

Expected response: `{"AnyLog.status":"Success", "AnyLog.hash": "0dd6b959..."}`

> Full working examples can be found in
> <a href="#" onclick="openEnvModal('/assets/examples/sample-put.py'); return false;">sample-put.py</a>
