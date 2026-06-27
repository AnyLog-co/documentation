---
layout: default
parent: Southbound
title: FLEDGE
nav_order: 4
---
<link rel="stylesheet" href="just-the-docs.css">

# Using FLEDGE as the data source connector

EdgeLake-fledge-connector is based on fledge-http-north. The connector replaces FLEDGE nodes with EdgeLake nodes and data is streamed using _POST_ or _PUT_. 
* [AnyLog / EdgeLake Northbound connector for FLEDGE](https://github.com/AnyLog-co/fledge-connector)
* [FLEDGE Docker Install](https://hub.docker.com/r/robraesemann/fledge)
* [FLEDGE Documentation](https://fledge-iot.readthedocs.io/en/latest/quick_start/index.html))

## Prerequisites 
<ol> 
<li>EdgeLake REST services enabled. Details are available <a href="https://github.com/EdgeLake/docker-compose" target="_blank">here</a></li> 
<li>FLEDGE & Corresponding plugins
   <ul style="padding-left: 20px;">
   <li>FLEDGE</li>
   <li>FLEDGE-GUI</li>
   <li>FLEDGE Southbound services OpenWeatherMap</li>
</ul></li></ol>

## Stream Data from FLEDGE into EdgeLake
<ol>
<li>Clone EdgeLake's fledge-connector
<pre class="code-frame"><code class="language-shell">cd $HOME
git clone https://github.com/AnyLog-co/fledge-connector</code></pre>
</li>

<li>Copy <code>edgelake_plugin</code> into <i>FLEDGE</i>
<pre class="code-frame"><code class="language-shell">cp -r $HOME/fledge-connector/anylog_rest_conn/ /usr/local/fledge/python/fledge/plugins/north/</code></pre>
</li>

<li>Access Fledge GUI
<div class="image-frame"><img src="../../../imgs/fledge_gui.jpeg" /></div>
</li>

<li>Begin sending data & view <code>readings</code> columns - using the <i>OpenWeatherMap</i> asset as an example
<pre class="code-frame"><code class="language-json"># Sample data being generated
{
 "asset": "OpenWeatherMap",
 "reading": {
   "city": "London",
   "wind_speed": 5.14,
   "clouds": 100,
   "temperature": 289.21,
   "pressure": 1009,
   "humidity": 74,
   "visibility": 10000
 },
 "timestamp": "2022-06-25 19:42:09.916403"
}
</code></pre></li>

<li>Under the <i>North</i> section add <code>anylog_rest_conn</code>
   <ul style="padding-left: 20px">
      <li><b>URL</b> - The IP:Port address to send data to</li>
      <li><b>REST Topic Name</b> - REST topic to send data to</li>
      <li><b>Asset List</b> - Comma separated list of assets to send using this AnyLog connection. If no assets set, then data 
   from all assets will be sent</li>
   <li><b>Database Name</b> - logical database to store data in AnyLog</li>
   </ul>
</li></ol>

<div class="image-frame">
    <img id="enlarge-image" src="../../../imgs/fledge_north_plugin.png" />
    <script src="script.js"></script>
</div>

The process detailed above streams data into EdgeLake via REST. 


## Configuring EdgeLake REST  Client
Notes:
* To stream data using _PUT_, enable the EdgeLake REST service. 
* To stream data via _POST_, enable the message client service on the EdgeLake node. 

**Sample Message Client**:
<pre class="code-frame"><code class="language-anylog">&lt;msg client where broker=rest and user-agent=anylog and log=!mqtt_log and topic=(
    name=fledge-weather and
    dbms=!default_dbms and
    table="bring [asset]" and
    column.timestamp.timestamp="bring [timestamp]" and
    column.city=(type=str and value="bring [readings][city]" and optional=true) and
    column.clouds=(type=float and value="bring [readings][clouds]" and optional=true) and
    column.humidity=(type=float and value="bring [readings][humidity]" and optional=true) and
    column.pressure=(type=float and value="bring [readings][pressure]" and optional=true) and
    column.temperature=(type=float and value="bring [readings][temperature]" and optional=true) and
    column.visibility=(type=float and value="bring [readings][visibility]" and optional=true) and
    column.wind_speed=(type=float and value="bring [readings][wind_speed]" and optional=true)
)&gt;</code></pre>

EdgeLake deployment comes with a sample connection to Fledge that accepts data from both OpenWeather and Random southbound service.        
