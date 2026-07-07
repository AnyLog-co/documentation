---
layout: default
title: Using REST
nav_order: 6
---
 
# Using REST

Users can interact with the nodes in the network using REST.

Using REST, users can execute EdgeLake commands over HTTP on any node in the network that is configured to satisfy REST 
requests.

## Prerequisites
* A REST client software like [cUrL](https://man7.org/linux/man-pages/man1/curl.1.html) or [Postman](https://www.postman.com/)
* An EdgeLake Node that provides a REST connection. To configure an EdgeLake Node to satisfy REST calls, issue the 
following command on the EdgeLake command line:
<pre class="code-frame"><code class="language-anylog">&lt;run rest server where 
   external_ip = [external_ip ip] and 
   external_port = [external port] and 
   internal_ip = [internal ip] and 
   internal_port = [internal port] and 
   timeout = [timeout] and 
   ssl = [true/false] and 
   bind = [true/false] 
&gt;
</code></pre>

## HTTP methods supported
EdgeLake commands are supported using the HTTP methods `GET`, `PUT` and `POST`.

* `GET` is used to retrieve information.  
* `PUT` is used to add data to nodes in the network.  
* `POST` is used as a default method to execute all other EdgeLake commands.  

<table>
  <thead>
    <tr>
      <th>HTTP Method</th>
      <th>EdgeLake commands</th>
      <th>Comments</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>GET</td>
      <td>sql</td>
      <td>Issue queries to data hosted by nodes of the network</td>
    </tr>
    <tr>
      <td></td>
      <td>get</td>
      <td>Retrieve information from nodes members of the network</td>
    </tr>
    <tr>
      <td></td>
      <td>blockchain get</td>
      <td>Query the metadata</td>
    </tr>
    <tr>
      <td></td>
      <td>help</td>
      <td>Help on the ANyLog commands</td>
    </tr>
    <tr>
      <td>POST</td>
      <td>set</td>
      <td>Set values or change status</td>
    </tr>
    <tr>
      <td></td>
      <td>reset</td>
      <td>Reset values or status</td>
    </tr>
    <tr>
      <td></td>
      <td>blockchain</td>
      <td>Manage metadata commands (note the `blockchain get` is supported using GET)</td>
    </tr>
    <tr>
      <td>PUT</td>
      <td>command</td>
      <td>publish time-series data to node</td>
    </tr>
  </tbody>
</table>

## Sample cURL Requests

### `GET` requests 

* `get status` - check whether a node is active or not
<pre class="code-frame"><code class="language-shell">curl --location --request GET '10.0.0.78:7849' \
    --header 'command: get status' \
    --header 'User-Agent: AnyLog/1.23'
</code></pre>
* `blockchain get operator where company='New Company'` - get list of all operators owned by _New Company_
<pre class="code-frame"><code class="language-shell">curl --location --request GET '10.0.0.78:7849' \
    --header 'command: blockchain get operator where company="New Company" \
    --header 'User-Agent: AnyLog/1.23'
</code></pre> 
* `sql new_company format=table "select * from rand_data where timestamp >= NOW() - 1 minute limit 5;"` -
Sample `SELECT` request
<pre class="code-frame"><code class="language-shell">curl --location --request GET '10.0.0.78:7849' \
    --header 'command:sql new_company format=table "select * from rand_data where timestamp >= NOW() - 1 minute limit 5;"' \
    --header 'User-Agent: AnyLog/1.23' \
    --header 'destination: network'
</code></pre> 

### `POST` request

The `POST` command provides support for both publishing data and all other, non-`GET` commands. 

When sending data via `POST`, there's a need for mapping between the data comming and organazing it; similar to _MQTT_. 
Farther details regardin `run msg client` can be found in [subscribing to rest calls](https://github.com/AnyLog-co/documentation/blob/master/using%20rest.md#subscribing-to-rest-calls)
in AnyLog documentation. 

<pre class="code-frame"><code class="language-anylog">&lt;run msg client where broker=rest and port=!anylo_rest_port and user-agennt=anylog/1.23 and log=false and topic=(
  name=new_data and 
  dbms=bring [dbms] and 
  table=bring [table] and 
  column.timestam.timestamp=bring [timestamp] and 
  column.value=(type=int and value=bring [value]) 
)&gt;
    </code>
</pre>

**Sample Calls**:
* Adding Data
<pre class="code-frame"><code class="language-shell">curl --location --request POST '10.0.0.226:32149' \
  --header 'command: data' \
  --header 'topic: new_data' \
  --header 'User-Agent: AnyLog/1.23' \
  --header 'Content-Type: text/plain' \
  --data-raw ' [{"dbms" : "aiops", "table" : "fic11", "value": 50, "timestamp": "2019-10-14T17:22:13.051101Z"},
    {"dbms" : "aiops", "table" : "fic16", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"},
    {"dbms" : "aiops", "table" : "ai_mv", "value": 501, "timestamp": "2019-10-14T17:22:13.050101Z"}]'
</code></pre>

* Reset (error) log
<pre class="code-frame"><code class="language-shell">curl --location --request POST '10.0.0.78:7849' \
  --header 'User-Agent: AnyLog/1.23' \
  --header 'command: reset error log'
</code></pre>

* Set value 
<pre class="code-frame"><code class="language-shell">curl --location --request POST '10.0.0.78:7849' \
  --header 'User-Agent: AnyLog/1.23' \
  --header 'command: set company_name=AnyLog'
</code></pre>

* Publish Blockchain Policy 
<pre class="code-frame"><code class="language-shell">curl -X POST \
  http://172.18.12.129:2149 \
  -H 'command: blockchain push !new_policy' \
  -H 'User-Agent: AnyLog/1.23' \
  -H 'Content-Type: application/json' \
  -d '&lt;new_policy={"panel": {"name": "panel 1", "city": "Los Angeles, CA", "loc": "33.8121, -117.91899", "owner": "AFG"}}&gt;'
</code></pre>


### `PUT` request

Use a REST client software (such as _cURL_ or _Postman_) and issue a `PUT` command to send the data with the following 
keys and values in the header

<table>
  <tr>
    <th>Key</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>User-Agent</td>
    <td>AnyLog/1.23</td>
  </tr>
  <tr>
    <td>type</td>
    <td>The type of data transferred. The default value is JSON.</td>
  </tr>
  <tr>
    <td>dbms</td>
    <td>The logical database to contain the data.</td>
  </tr>
  <tr>
    <td>table</td>
    <td>The logical table to contain the data.</td>
  </tr>
  <tr>
    <td>source</td>
    <td>A unique ID to identify the data source (i.e. an ID of a sensor).</td>
  </tr>
  <tr>
    <td>mode</td>
    <td>File or Streaming (see details below). The default value is 'file'.</td>
  </tr>
  <tr>
    <td>instructions</td>
    <td>An ID of a policy that determines the mapping of the file data to the table's structure.</td>
  </tr>
</table>

<pre class="code-frame"><code class="language-shell">curl --location --request PUT '10.0.0.226:32149' \
    --header 'type: json' \
    --header 'dbms: test' \
    --header 'table: table1' \
    --header 'Content-Type: text/plain' \
    --header 'User-Agent: AnyLog/1.23' \
    -w "\n" \ 
    --data-raw '[{"parentelement": "62e71893-92e0-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "ADVA FSP3000R7", "value": 0, "timestamp": "2019-10-11T17:05:08.0400085Z"}, 
                 {"parentelement": "68ae8bef-92e1-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "Catalyst 3500XL", "value": 50, "timestamp": "2019-10-14T17:22:13.0510101Z"}, 
                 {"parentelement": "68ae8bef-92e1-11e9-b465", "webid": "F1AbEfLbwwL8F6EiS", "device_name": "Catalyst 3500XL", "value": 50, "timestamp": "2019-10-14T17:22:18.0360107Z"}]'
</code></pre>
**Expected Output**: <code class="language-shell">{"AnyLog.status":"Success", "AnyLog.hash": "0dd6b959e48c64818bf4748e4ae0c8cb" }</code>








 
 
