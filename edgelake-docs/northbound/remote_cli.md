---
layout: default
parent: Northbound
title: Remote CLI
nav_order: 1
---
# The Remote CLI

The Remote CLI is a web application that offers a REST based GUI that allows to issue commands to nodes in the network.    
The GUI extends the command-line-interface offered by each node of the network, by delivering the commands using REST.  
This functionality allows to interact, using a web based graphical application, with nodes of the network, from a single point
(with valid certificate).    

A similar functionality is achieved using [cURL](https://curl.se/) as well as with other tools such as [Postman](https://www.postman.com/).  
Note: [Using Postman](using_postman.md) details the usage of Postman with EdgeLake nodes.

The Remote CLI contains the following:
1. A client form to issue commands and queries to nodes in the network.
2. Preconfigured buttons allowing to issue commands by clicking on buttons. Users preconfigure the buttons to their frequently used commands and queries.
3. Forms to display and stream images and video.
4. A form that collects monitored info from monitored nodes.
5. A form that translate commands and queries to a) cURL commands, b) QR Codes and c) HTTP requests.
6. A configuration form.

## The server side

Nodes in the network needs to be configured with their REST service enabled.  
Configuring a node to recieve REST requests is detailed in the [REST Requests](../../commands/backgound_services#rest-services) section.

## Installing the Remote-CLI
The Remote-CLI is an Open-Source django based project that can be [run manually](https://github.com/AnyLog-co/Remote-CLI) or via Docker.   

### Quck install
<pre class="code-frame"><code class="language-shell">docker run -it -d \
  -p 31800:31800 \
  -e CONN_IP=0.0.0.0 \
  -p CONN_PORT=31800 \
  -v remote-cli:/app/Remote-CLI/djangoProject/static/json
--name remote-cli --rm anylogco/remote-cli:lateest
</code></pre>

### Remote-CLI with Query Node
The Remote-CLI makes it simple to view images and videos that are returned from queries. To see these files through 
Remote-CLI, you just need to ensure that the directory (docker volume) where the files are stored is shared with the 
query node that receives them.

To accomplish this, you'll need to update the template docker-compose with the Remote-CLI information (as shown below). 

<pre class="code-frame"><code class="language-config">version: "3"
services:
  remote-cli:
    image: anylogco/remote-cli:latest
    container_name: remote-cli
    restart: always
    stdin_open: true
    tty: true
    ports:
      - 31800:31800
    environment:
      - CONN_IP=0.0.0.0
      - CLI_PORT=31800
    volumes:
      - remote-cli:/app/Remote-CLI/djangoProject/static/json
      - remote-cli-current:/app/Remote-CLI/djangoProject/static/blobs/current/
  anylog-query:
    image: anylogco/edglake:1.3.2404
    restart: always
    env_file:
      - query-configs/base_configs.env
      - query-configs/advance_configs.env
      - .env
    container_name: anylog-query
    stdin_open: true
    tty: true
    network_mode: host
    volumes:
      - edgelake-query-anylog:/app/EdgeLake/anylog
      - edgelake-query-blockchain:/app/EdgeLake/blockchain
      - edgelake-query-data:/app/EdgeLake/data
      - edgelake-query-local-scripts:/app/deployment-scripts
      - remote-cli-current:/app/Remote-CLI/djangoProject/static/blobs/current/
volumes:
  edgelake-query-anylog:
  edgelake-query-blockchain:
  edgelake-query-data:
  edgelake-query-local-scripts:
  remote-cli:
  remote-cli-current:
</code></pre>


# Configuring the Remote CLI
The Remote CLI can be configured to support specific settings, default values and frequently used commands.  
The configurations files are organized in the static/json folder as a set of JSON files.

## The configuration files

When deploying with Docker, the configurations files are located in `remote-cli` volume; while images aand videos coming via 
query are stored in `remote-cli-curennt`. 

#### Accessing Volumes
<ol start="1">
<li>Using <code class="language-shell">docker volume ls</code> locate <code class="language-shell">remote-cli</code> volume.
<pre class="code-frame"><code class="language-shell">root@anylog-co:~# docker volume ls 
DRIVER    VOLUME NAME
local     anylog-gui_anylog-gui
local     docker-makefile_edgelake-master-anylog
local     docker-makefile_edgelake-master-blockchain
local     docker-makefile_edgelake-master-data
local     docker-makefile_edgelake-master-local-scripts
local     docker-makefile_edgelake-operator-anylog
local     docker-makefile_edgelake-operator-blockchain
local     docker-makefile_edgelake-operator-data
local     docker-makefile_edgelake-operator-local-scripts
local     docker-makefile_edgelake-query-anylog
local     docker-makefile_edgelake-query-blockchain
local     docker-makefile_edgelake-query-data
local     docker-makefile_edgelake-query-local-scripts
local     docker-makefile_remote-cli
local     docker-makefile_remote-cli-current
</code></pre></li>

<li>Inspect the volume in order to locate where configuration file(s) reeside.
<pre class="code-frame"><code class="language-shell">root@anylog-co:~# docker volume inspect docker-makefile_remote-cli
[
    {
        "CreatedAt": "2024-05-08T18:33:32Z",
        "Driver": "local",
        "Labels": {
            "com.docker.compose.project": "docker-makefile",
            "com.docker.compose.version": "1.29.2",
            "com.docker.compose.volume": "remote-cli"
        },
        "Mountpoint": "/var/lib/docker/volumes/docker-makefile_remote-cli/_data",
        "Name": "docker-makefile_remote-cli",
        "Options": null,
        "Scope": "local"
    }
]</code></pre></li>

<li>In the directory corresponding to <b>Mountpoint</b> you should be able to locate the configuration file(s)
    <ul style="padding-left: 20px">
        <li><b>settings.json</b> - consists of default configurations for accessing the (query) node(s) in the network</li>
        <li><b>commands.json</b> - queries to be used for viewing / accessing both th data and metadata</li>
    </ul>
<pre class="code-frame"><code class="language-shell">root@anylog-co:~# ls -l /var/lib/docker/volumes/docker-makefile_remote-cli/_data
total 120
-rw-r--r-- 1 root root 31785 Apr  8 03:44 commands.json
-rw-r--r-- 1 root root   591 May  8 18:58 settings.json
</code></pre></li>
</ol>

### The main configuration file

The initial settings for the Remote CLI are determined by the **setting.json** file.

The **setting.json** file includes the following sections:
* **client** - specifies the default values on the client form allowing the following options:
   * connect_info - specifies the default EdgeLake Node to use.
   * buttons - the name of the JSON file that defines the preconfigured buttons options on the client form.
   * help - determines how help is provided when a button is selected and the help option is flagged on the client form:
      - if the value is **open**, the button selection opens the URL that is associated with the button.
      - if the value is **url**, the button selection displays the help URL that is associated with the button.
 
* **certificates** - specifies the certificates to use (if authentication on the EdgeLake node is enabled).

* **Monitor** - specifies the JSON files that configure the monitored pages. Each pair includes a name describing the 
data monitored, and a file name that specifies what is monitored.

Example:
<pre class="code-frame"><code class="language-json">{
  "client" : {
    "connect_info": "23.239.12.151:32349",
    "buttons" : "commands.json",
    "help" : "link"
  },
  "certificates" : {
      "enable"   : false,
      "pem_file" : "ca-anylog-public-key.crt",
      "crt_file" : "server-acme-inc-public-key.crt",
      "key_file" : "server-acme-inc-private-key.key"
  },

  "monitor" : [
    ["Monitor Operators", "monitor_operators.json"],
    ["Monitor Members", "monitor_members.json"]
  ]

}</code></pre>

### The buttons' configuration file

The name of the file is specified in the **setting.json** file under "client/buttons" ("commands.json" in the example above).
The info contained in the file includes the following:
* **button** - The name appearing on the button.
* **command** - The command to issue when the button is selected.
* **type** - The command type (GET or POST).
* **group** - A category name, allowing users to select buttons by categories.
* **help_url** - The URL to use if **help** is selected on the client form.

**Example**:
<pre class="code-frame"><code class="language-json">{
 "commands": [
    {
        "button": "Node Status",
        "command": "get status",
        "type": "GET",
        "group": "Monitor",
        "help_url": "blob/master/monitoring%20nodes.md#the-get-status-command"
    },
    {
        "button": "Get Processes",
        "command": "get processes",
        "type": "GET",
        "group": "Monitor",
        "help_url": "blob/master/monitoring%20nodes.md#the-get-processes-command"
    },
    {
        "button": "Get Dictionary",
        "command": "get dictionary",
        "type": "GET",
        "group": "Monitor",
        "help_url": "blob/master/monitoring%20nodes.md#the-get-dictionary-command"
    },
    {
        "button": "Disk Usage",
        "command": "get disk usage .",
        "type": "GET",
        "group": "Monitor",
        "help_url": "blob/master/monitoring%20nodes.md#monitoring-state-commands"
    },
    {
        "button": "CPU Usage",
        "command": "get cpu usage",
        "type": "GET",
        "group": "Monitor",
        "help_url": "blob/master/monitoring%20nodes.md#monitoring-state-commands"
    },
    {
          "button": "Data Summary per Table",
          "command": "sql new_company format=table and extend=(+node_name as node) \"select min(timestamp), max(timestamp), min(value), avg(value), max(value), count(*) from random_float_device;\"",
          "type": "GET",
          "group": "Data Query"
    },
    {
      "button": "Streaming Video",
      "command": "sql new_company info = (dest_type = rest) and extend=(+country, +city, @ip, @port, @dbms_name, @table_name) and format = json and timezone = utc  select  file, start_ts::ljust(19), end_ts::ljust(19), people_count, confidence::float(3) from people_counter     where start_ts >= NOW() - 1 hour and end_ts <= NOW() order by people_count, confidence --> selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file)",
      "type": "GET",
      "group": "Data Query"
    },
    {
      "button": "Image",
      "command": "sql new_company extend=(+node_name, @ip, @port, @dbms_name, @table_name) and format = json and timezone=Europe/Dublin  select  timestamp, file, class, bbox, score, status  from images where timestamp >= now() - 1 hour and timestamp <= NOW() order by timestamp desc --> selection (columns: ip using ip and port using port and dbms using dbms_name and table using table_name and file using file) -->  description (columns: bbox as shape.rect and score)",
      "type": "GET",
      "group": "Data Query"
    }
 ]
}</code></pre>

### The monitor configuration file

One or more file names are specified in the **setting.json** file under "monitor" ("monitor_operators.json" 
and "monitor_members.json" in the example above).

Each of the file describes the form that is presented to the user including the thresholds that trigger alerts.


## Usage examples

The following demonstrate commands issued via cURL and their web representation using the Remote CLI:

### Return the list of tables supported by the network 

**Using cURL**:
<pre class="code-frame"><code class="language-shell">curl -X GET 23.239.12.151:32349 \
    -H "command: get tables where dbms=*" \
    -H "User-Agent: AnyLog/1.23"</code></pre>

**Using the Remote CLI**:

<div class="image-frame"><img src="../../../imgs/remote_cli_get_databases.png" /></div>

### Return columns in a given table 

Using cURL:

<pre class="code-frame"><code class="language-shell">curl -X GET 23.239.12.151:32349 \
    -H "command: get columns where dbms=litsanleandro and table=ping_sensor" \
    -H "User-Agent: AnyLog/1.23"`</code></pre>

Using the Remote CLI:

<div class="image-frame"><img src="../../../imgs/remote_cli_get_columns.png" /></div>

### Return Operators nodes associated to a company

Using cURL:

<pre class="code-frame"><code class="language-shell">curl -X GET 23.239.12.151:32349 \
    -H 'command:blockchain get operator where company="Lit San Leandro"' \
    -H "User-Agent: AnyLog/1.23"`</code></pre> 

Using the Remote CLI:

<div class="image-frame"><img src="../../../imgs/remote_cli_blockchain_operators.png" /></div>

### Get the list of nodes that host the data (for each table)

Using cURL:

<pre class="code-frame"><code class="language-shell">curl -X GET 23.239.12.151:32349 \
    -H "command:get data nodes" \
    -H "User-Agent: AnyLog/1.23"</code></pre>

Using the Remote CLI:

<div class="image-frame"><img src="../../../imgs/remote_cli_data_nodes.png" /></div>

### Query the last 90 seconds of data

Using cURL:

<pre class="code-frame"><code class="language-shell">curl -X GET /23.239.12.151:32349 \
    -H 'command: sql litsanleandro format=table "select timestamp, value FROM ping_sensor WHERE timestamp >= NOW() -90 seconds"' \
    -H "User-Agent: AnyLog/1.23" \
    -H "destination: network"`</code></pre>

Using the Remote CLI:
<div class="image-frame"><img src="../../../imgs/remote_cli_select_last_90sec.png" /></div>

### Query the last 10 minutes of data including the source node

Using cURL:

<pre class="code-frame"><code class="language-shell">curl -X GET 23.239.12.151:32349 \
    -H 'command: sql test format=table and extend=(+ip, +node_name) "select timestamp, value FROM rand_data WHERE timestamp >= NOW() - 10 minutes ORDER BY value LIMIT 50"' \
    -H "User-Agent: AnyLog/1.23" \
    -H "destination: network"`</code></pre>

Using the Remote CLI:

<div class="image-frame"><img src="../../../imgs/remote_cli_select_last_10min.png" /></div>