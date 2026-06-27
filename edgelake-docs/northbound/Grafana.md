---
layout: default
parent: Northbound
title: Using Grafana
nav_order: 2
---
# Using Grafana

## Overview

Grafana is an open-source BI tool managed by [Grafana Labs](https://grafana.com/). We utilize Grafana as our default 
demo BI tool. However, directions for other BI tools, such as [Microsoft's PowerBI](PowerBI.md), can be found in our 
[North Bound services](../) section.   

* Using Grafana, users can visualize time series data using pre-defined dashboards.
* Details on how to use Grafana to visualize data in the network are available in the 
[Using Grafana](https://github.com/AnyLog-co/documentation/blob/master/northbound%20connectors/using%20grafana.md#using-grafana) document. 
* Example configurations and dashboards can be found at [import grafana dashboard document](https://github.com/AnyLog-co/documentation/blob/master/northbound%20connectors/import_grafana_dashboard.md).

## Prerequisites & Links

* [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
* [Grafana Install](https://grafana.com/docs/grafana/latest/setup-grafana/installation/) - We support _Grafana_ 9.5.16 or higher.
* The REST service enabled on the EdgeLake node (the Query Node) that services the Grafana Request.
* Use the following command on the EdgeLake CLI to enable the REST service:
<pre class="code-frame"><code class="language-anylog">&lt;run rest server where
    external_ip=!external_ip and external_port=!anylog_rest_port and
    internal_ip=!ip and internal_port=!anylog_rest_port and
    bind=!rest_bind and threads=!rest_threads and timeout=!rest_timeout
&gt;</code></pre>
Note:  
  * `[ip]` and `[port]` are the IP and Port that would be available to REST calls.
  * `[max time]` is an optional value that determines the max execution time in seconds for a call before being aborted.
  * A 0 value means a call would never be aborted and the default time is 20 seconds.

## Setting Up Grafana 
<ol start="1">
<li><a href="https://grafana.com/docs/grafana/latest/getting-started/getting-started/" target="_blank">Login to Grafana</a> - 
The default <i>HTTP</i> port that Grafana listens to is 3000 - On a local machine go to <code>http://localhost:3000</code>.
<br>
<div class="image-frame">
    <img src="../../../imgs/grafana_login.png" alt="Grafana page" />
</div>
</li>
<li>In <i>Data Sources</i> section, create a new JSON data source
    <ul style="padding-left: 20px">
        <li>Select a JSON data source</li>
        <li>On the name tab provide a unique name to the connection.</li>
        <li>On the URL Tab add the REST address offered by the EdgeLake node (i.e. http://10.0.0.25:32149)</li>
        <li>On the <b>Custom HTTP Headers</b>, name the default database. If no header is set, then all accessible databases to 
   the node will be available to query</li>
    </ul>

<table>
  <tr>
    <td align="center"><img src="../../../imgs/grafana_datasource_connector.png" alt="Data Source Option" /></td>
    <td align="center"><img src="../../../imgs/grafana_data_source.png" alt="Data Source Config" /></td>
  </tr>
</table>

</li>
<br/>
<li>Select the <b>Save and Test</b> option that should return a green banner message: ***Data source is working***.
    <div class="image-frame">
        <img src="../../../imgs/grafana_confirmation.png" alt="Confirmation Message" />
    </div>
</li>
</ol>

## Enabling Authentication

Enabling authentication is explained at [Authenticating HTTP requests](../authentication.md#Authenticating-http-requests).

* For Basic Authentications, the Grafana configuration should have _basic auth_ enabled.
* Basic Authentications validates _username_ and _password_, details are at [basic authentication](../authentication.md#enabling-basic-authentication-in-a-node-in-the-network). 
<div class="image-frame">
    <img src="../../../imgs/grafana_basic_auth.png" alt="basic authentication"  >
</div>

* Using certificates is detailed in [SSL Certificates](../authentication.md#using-ssl-certificates).
* On Grafana, set _TLS Client Auth_ and _Skip TLS Verify_ enabled. 

<div class="image-frame">
    <img src="../../../imgs/grafana_auth_image.png" alt="SSL Authentication" />
</div>

**Notes**: Failure to connect may be the result of one of the following
* EdgeLake instance is not running or not configured to support REST calls.
* Wrong IP and Port.
* Firewalls are not properly configured and the needed IP and Port not available.
* EdgeLake is configured with authentication detection that is not being satisfied.
* If Grafana is properly connected, the database and tables of the EdgeLake network can be selected on the Grafana GUI.
  If Gragfana fails to connect, the dashboard (Edit Panel/Metric Selection) presents "Error: No table connected" in the pull-down menu.

## Using Grafana to visualize EdgeLake data

Grafana allows to present data in 2 modes _Time Series_ collects and visualize data values as a function of time, and 
_Table_ format where data is presented in rows and columns.

EdgeLake queries are represented in the Grafana JSON API, and details of the configuration are available 
[here](https://github.com/AnyLog-co/documentation/blob/master/northbound%20connectors/using%20grafana.md#using-the-time-series-data-visualization).
Queries are represented in the JSON API using one of the following methids:
1. As a SQL query.
2. As a push-down Increment function.
3. As a push-down period function.

The push-down functions are very efficient as processing are fone on the edge and only summaries are returned on the network.

The query information is represented using JSON in the Payload section. The Grafana info including the Payload is 
transferred to the EdgeLake query node, where it is transforms to a query that is executed on the nodes in the network.

To represent a query, follow the following steps for each Panel:
1. Select the JSON data Source.
2. Select the logical database and table from the pull down menu in the Metric section.
3. Represent the EdgeLake query in the Payload section.

The chart below summarized the attribute names for the JSON payload:  


<table>
  <tbody>
    <tr>
      <td>dbms</td>
      <td>The name of the logical database to use. Overrides the dbms name in the configuration page.</td>
    </tr>
    <tr>
      <td>table</td>
      <td>The name of the table to use. Overrides the table name in the sql statement.</td>
    </tr>
    <tr>
      <td>type</td>
      <td>The type of the query. The default value is 'sql' and other valid types are: 'increments', 'period' and 'info'.</td>
    </tr>
    <tr>
      <td>sql</td>
      <td>A sql statement to use.</td>
    </tr>
    <tr>
      <td>details</td>
      <td>An EdgeLake native command which is not a SQL statement.</td>
    </tr>
    <tr>
      <td>where</td>
      <td>A "WHERE" condition added to the SQL statement. Can add filter or other conditions to the executed SQL.</td>
    </tr>
    <tr>
      <td>functions</td>
      <td>A list of SQL functions to use which override the default functions.</td>
    </tr>
    <tr>
      <td>time_column</td>
      <td>The name of the time column in the Time Series table.</td>
    </tr>
    <tr>
      <td>value_column</td>
      <td>The name of the value column in the Time Series table.</td>
    </tr>
    <tr>
      <td>time_range</td>
      <td>When using a Table view, determines if the query needs to consider the time range. The default value is 'true'.</td>
    </tr>
    <tr>
      <td>servers</td>
      <td>Replacing the network determined Operators (nodes hosting data) with a list of user determined Operators to use.</td>
    </tr>
    <tr>
      <td>instructions</td>
      <td>Additional EdgeLake query instructions.</td>
    </tr>
    <tr>
      <td>trace_level</td>
      <td>By setting debug level to 1, the executed query and the number of rows returned are printed on the Query Node CLI.</td>
    </tr>
    <tr>
      <td>timezone</td>
      <td>Overwrite the default timezone. Note that the same timezone needs to be set on the Grafana dashboard. See details in the **Timezone considerations** section below.</td>
    </tr>
    <tr>
      <td>interval</td>
      <td>Overwrite the intervals calculated by the query process. See details in the <b>increment</b> function detailed below.</td>
    </tr>
    <tr>
      <td>grafana:format_as</td>
      <td>Determines the format of the returned values.</td>
    </tr>
    <tr>
      <td>grafana:data_points</td>
      <td>The value <b>fixed</b> presents the returned values using the Grafana Intervals (as detailed in the <b>Query options</b> section. See details in the section **Fixed data points** below.</td>
    </tr>
  </tbody>
</table>

<div class="image-frame">
    <img src="../../../imgs/grafana_dashboard_layout.png" alt="Grafana Page Layout" />
</div> 

## Timezone considerations
When a query is issued from the Grafana Dashboard, the timezone is selected by the user (in the dropdown timerange menu).
The grafana timezone options might not be consistent with the timezones options supported by EdgeLake and if needed, users 
can specify the timezone in the JSON Payload section.    
For example, Grafana can issue the value "browser" as a timezone (to indicate that the timezone of the browser is selected).
However, the query node can be deployed in a different timezone which may lead to inconsistencies.  
By adding a timezone attribute and a value in the JSON payload, users can associate between the Grafana timezone abbreviation and EdgeLake timezone abbreviation.
Note that EdgeLake returns the values in the target timezone, and the Grafana timezone needs to represent the same timezone as EdgeLake.    
The list of timezone abbreviations used by EdgeLake is available [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).  
The following are additional abbreviation for EdgeLake:
* **utc** - utc timezone
* **pt**  - America/Los_Angeles
* **mt**  - America/Denver
* **ct**  - America/Chicago
* **et**  - America/New_York


## Metadata based Visualization - A Network Map

1. In the _Visualizations_ section, select _Geomap_

2. In the _Metric_  section, select a table name to "query" against

3. Update _Payload_ with the following information
<pre class="code-frame"><code class="language-json">{
    "type" : "map",
    "member" : ["master", "query", "operator", "publisher"],
    "metric" : [0,0,0],
    "attribute" : ["name", "name", "name", "name"]
}
</code></pre>

<div class="image-frame">
    <img src="../../../imgs/grafana_geomap.png" alt="Network Map" />
</div> 

## Metadata based Visualization - Visualizing Blockchain Data (Metadata)
1. In the _Visualizations_ section, select _Table_

2. In the _Metric_  section, select a random table - the JSON instruction will override the selction.

3. Update _Payload_ with the following information

<pre class="code-frame"><code class="language-json">{
    "type": "info", 
    "details": "blockchain get operator bring.json [*][cluster] [*][name] [*][company] [*][ip] [*][country] [*][state] [*][city]"
}
</code></pre>

<div class="image-frame">
    <img src="../../../imgs/grafana_blockchain_table.png" alt="Network Map" />
</div>

## SQL Query

The following SQL query returns the last values ingested by the database.
Note that without the limit, the entire table's data is returned, and even if a time range is added, it may include a huge
number of rows.

The **increment** and **period** pushdown functions detailed below consider all relevant data while also allowing control over the volume of data returned.

Example SQL query:
<pre><code class="language-sql">SELECT 
  timestamp, a_current, b_current, c_current 
FROM 
  bf 
WHERE 
  id = 1 
ORDER BY 
  timestamp DESC
LIMIT 1</code></pre>

Example JSON Payload:
<pre><code class="language-json">{
  "sql": "select timestamp, a_current, b_current, c_current from bf where id = 1 order by timestamp desc limit 1;"
}</code></pre>

Example Gauge with latest values:
<img src="../../../imgs/grafanaa_sql_widget.png" alt="SQL generated table" />

## The Increment Query

**Increments query** (The default query) is used to retrieve statistics on the time series data in the selected time 
range. Depending on the number of data point requested, the time range is divided to intervals and the min, max and 
average are collected for each interval and graphically presented.  

<ol start="1">
  <li>In the <i>Visualizations</i> section, select Time series</li>
  <li>In the <i>Metric</i> section, select a table name to “query” against</li>
  <li>Update Payload with the following information
  <pre class="code-frame"><code class="language-json"># Input in Grafana 
{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "grafana": {
    "format_as": "timeseries"
  }
}</code></pre></li>
  <li>Under Query Options, update <i>Max data points</i> (limit value), and see comment below (Considering the Grafana limit).
  <br/>
  <br/>
  <div class="image-frame">
    <img src="../../../imgs/grafana_increments_graph.png" alt="Increments Graph"   />
  </div>
  </li>
</ol>

When the query type is set to _increments_, the query being executed on the EdgeLake side is as follows:
<pre class="code-frame"><code class="language-sql">SELECT 
  increments(second, 1, timestamp), max(timestamp) as timestamp, avg(value) as avg_val, min(valu e) as min_val, 
  max(value) as max_val 
FROM 
  percentagecpu_sensor 
WHERE 
  timestamp >= '2024-02-19T19:42: 02.133Z' and timestamp <= '2024-02-19T19:57:02.133Z' 
LIMIT 2128;
</code></pre>

### Understanding and Tuning Increments queries  

The increment function allows to push processing to the edge nodes and return summaries. This is a very powerful way to 
query data for the following reasons:
1. Rows are processed concurrently by multiple edge nodes.
2. Only summaries are transferred over the network as well as keeping the Grafana memory usage contained.


An increment query is executed on each participating node as follows:  
1. A time range is divided to intervals.
2. All the rows in the time range are visited and evaluated.
3. For each interval, the selected query functions are calculated (min, max, average, count, sum).
4. A single entry is returned for each time interval.
5. The query node unifies the replies from all the participating nodes to a unified result.

### The number of time points returned

The number of points returned to an increment function determines on the time intervals that are considered.  
With Grafana, 3 options are available:
1. Not specifying the time intervals - in this case, EdgeLake will determine an optimized time interval.
2. Specifying a time interval (in the JSON Payload using the attribute key **interval** with the interval value,
   for example: "interval" : "3 minutes", or in the query statement, for example: **increments(minute,1,timestamp)**).
3. Using the time intervals provided by Grafana (specify the value: **dashboard** for the key **interval**).  

To see the optimized value, add ```"trace_level" : 1``` to the JSON Payload. The Query node displays the increment details.  
Here is an output example where a point is returned for every 1 hour interval:

<pre class="code-frame"><code class="language-sql">DEBUG 
Process: [0:Success] Rows: [248] Details: [increments(hour, 1, insert_timestamp)]
Stmt: [run client () sql cos timezone = local SELECT increments(insert_timestamp), max(insert_timestamp) as timestamp , avg(chemicalscale4ai_pv) as avg_val from cos_wp_analog where insert_timestamp >= '2024-07-26T20:08:44.761Z' and insert_timestamp <= '2024-07-27T02:08:44.761Z' limit 1260;]
</code></pre>

To query with a different time interval, specify the interval in the JSON Payload.  
The following example overwrites the optimized setting with a user defined interval.  
In the example below, each data point represents 10 minutes interval and provides to Grafana the average min and max values for each 10 minutes (note also that the Payload includes the trace option enabled):

<pre class="code-frame"><code class="language-sql">JSON  
{
  "type": "increments",
  "time_column": "insert_timestamp",
  "value_column": "chemicalscale4ai_pv",
  "functions": ["avg", "min", "max"],
  "grafana": {
    "format_as": "timeseries"
  },
  "interval" : "10 minutes",
  "trace_level" : 1

}
</code></pre>

### Fixed data points
The fixed data points option considers the number of data points specified in the **Grafana Query options**.  
With this option, the returned data (by an increment function) aligns with the Grafana derived interval (see the **Time Range/max data points** value in the **Query options** of the Grafana dashboard).  
For every interval, a data point is returned, and if no data point exists in the interval, a null value is returned.    

In the example below, **data_points** are set to **fixed** to indicate a returned value (or null) for each time interval
and the **interval** attribute maintains the value **dashboard** to indicate that the intervals are to leverage the values from the Grafana dashboard.
<pre class="code-frame"><code class="language-json">{
  "type": "increments",
  "time_column": "insert_timestamp",
  "value_column": "hw_influent",
  "functions": ["avg"],
  "grafana": {
    "format_as": "timeseries",
    "data_points" : "fixed"
  },
  "1timezone": "pt",
  "interval" : "dashboard",
  "trace_level" : 1
}</code></pre>

### Considering the Grafana limit  
When Grafana issues a query it will include a limit. Users need to make sure that the limit is not lower than the number of points returned.    
Note that the trace option provides the info on the number of points returned to Grafana.
Using the defaults (and not specifying intervals that overwrite the defaults) with a limit to set to 1000 or higher, will always return all the needed values.


## The Period Query
**Period query** is a query to retrieve data values at the end of the provided time range (or, if not available, before 
and nearest to the end of the time range).    
The derived time is the latest time with values within the time range. From the derived time, the query will determine 
a time interval that ends at the derived time and provides the avg, min and max values.         
To execute a period query, include the key: 'type' and the value: 'period' in the Additional JSON Data section.  

<ol start="1">
  <li>In the <i>Visualizations</i> section, select <i>Gauge</i></li>
  <li>In the <i>Metric</i> section, select a table name to “query” against</li>
  <li>Update Payload with the following information
<pre class="code-frame"><code class="language-json"># Input in Grafana
{
  "type": "period", 
  "time_column": "timestamp",
  "value_column": "value",
  "grafana" : {
    "format_as" : "timeseries"
  }
}</code></pre>
  </li>
  <li>Under <i>Query Options</i>, update <i>Max data points</i> (ie limit) otherwise the outcome would look like a single line as opposed to clearly showing <i>min / max / avg</i> value(s).
  <div class="image-frame">
    <img src="../../../imgs/grafana_period_gauge.png" alt="Increments Graph"   />
  </div></li>
</ol>

When the query type is set to _period_, the query being executed on the EdgeLake side is as follows:
<pre class="code-frame"><code class="language-sql">SELECT 
    max(timestamp) as timestamp, avg(value) as avg_val, min(value) as min_val, max(value) as max_val 
FROM 
    ping_sensor 
</code></pre>

More information on increments and period types of queries are available in [queries and info requests](https://github.com/AnyLog-co/documentation/blob/master/queries.md#optimized-time-series-data-queries).

## Other Grafana Examples

* Extending query to use where conditions
<pre class="code-frame"><code class="language-json">{
  "type": "increments",
  "time_column": "timestamp",
  "value_column": "value",
  "where": "device_name='ADVA FSP3000R7'",
  "grafana" : {
    "format_as" : "timeseries"
  }
}</code></pre>

* Example without where conditions
<pre class="code-frame"><code class="language-json">{
  "type": "period", 
  "time_column": "timestamp",
  "value_column": "value",
  "time_range": false,
  "functions": ["min", "max", "avg", "count"],
  "grafana" : {
    "format_as" : "timeseries"
  }
}</code></pre>

## Monitoring and Trace Options

### Tracing Grafana Queries

Users can trace queries that are generated from the Grafana panels as follows:    
* By setting debug level to 1, the executed query and the number of rows returned are printed on the CLI of the node that services Grafana.   
This setting enables trace on the specific queries where **trace_level** is set.  
Example:
<pre class="code-frame"><code class="language-json">{
  "sql": "SELECT insert_timestamp, servicepump1running_di FROM cos_wp ORDER BY insert_timestamp DESC limit 1",
  "time_range": false,
  "timezone": "local",
  "trace_level" : 1
}</code></pre>

* Trace of all the queries from the Grafana instance can be enabled using the **trace level** command on the CLI of the Query Node:
<pre class="code-frame"><code class="language-json">trace level = 1 grafana</code></pre>

Setting trace level to 0 disables the trace.

### Queries time statistics

Users can view statistics on the queries execution time using the following command:
<pre class="code-frame"><code class="language-anylog"> 
  get queries time
</code></pre>

Users can reset the statistics using the following command:
<pre class="code-frame"><code class="language-anylog"> 
  reset query timer
</code></pre>

### Identifying slow queries

Slow queries can be redirected to the query log with the following command:
<pre class="code-frame"><code class="language-anylog"> 
  set query log profile [n] seconds
</code></pre>

Whereas **[n]** is a threshold in seconds. Queries with execution time higher than the threshold will be logged to the query log.  

Use the following command to log all queries to the query log:
<pre class="code-frame"><code class="language-anylog"> 
  set query log
</code></pre>

Use the following command to retrieve the query log:
<pre class="code-frame"><code class="language-anylog"> 
  get query log
</code></pre>

Use the following command to reset the query log:
<pre class="code-frame"><code class="language-anylog"> 
  reset query log
</code></pre>

### Info on a query execution

Users can drill to specific queries to find how the query was executed using the following command:
<pre class="code-frame"><code class="language-anylog"> 
  query status
</code></pre>

Additional information is available int the 
[Profiling and Monitoring Queries](https://github.com/AnyLog-co/documentation/blob/master/profiling%20and%20monitoring%20queries.md) section.