# Using Grafana

## Overview

AnyLog includes a Grafana connector such that Grafana can serve as a visualization tier using a build-in/transparent interface that maps Grafana calls to queries over data maintained in the AnyLog Network.  
Using a HTTP and JSON API, Grafana communicates with AnyLog to retrieve data such that the Grafana visualization can be leveraged.  

Using Grafana, users can visualize time series data using using pre-defined queries and add new queries using SQL.

## Prerequisites

* Grafana instance installed.
* An AnyLog Node that provides a REST connection.
To configure an AnyLog Node to satisfy REST calls, issue the following command on the AnyLog command line:  
```run rest server [ip] [port] [max time]```  
[ip] and [port] are the IP and Port that would be available to REST calls.  
[max time] is an optional value that determines the max execution time in seconds for a call before being aborted.  
A 0 value means a call would never be aborted and the default time is 20 seconds.  
 
## Establishing a connection

Open the Grafana ***Data Sources*** configuration page.

* select a JSON data source.
* On the name tab provide a unique name to the connection.
* On the URL Tab add the REST address offered by the AnyLog node (i.e. http://10.0.0.25:2049)
* On the ***Custom HTTP Headers***, name the default database to use as follows:  
```al.dbms.[dbms name]```  For example: al.dbms.lsl_demo  
Declaring the database connects Grafana to the specified database on the http connection and makes the database tables available to query.  
***Note:*** to interact with a different database, create a new JSON data source and declare a different database name in the headers.

Select the ***Save and Test*** option that should return a green banner message: ***Data source is working***.  
Failure to connect may be the result of one of the following:
* AnyLog instance is not running or not configured to support REST calls.
* Wrong IP and Port.
* Firewalls are not properly configured and make the IP and Port not available.
* AnyLog is configured with authentication detection that is not being satisfied.

## Enabling Authentication

Enabling authentication is explained at [Authenticating HTTP requests](https://github.com/AnyLog-co/documentation/blob/master/authentication.md#Authenticating-http-requests).


## Using Grafana to visualize AnyLog data

* On the Grafana menu, use the ***+*** sign to create a new panel.
* Or, open an existing panel in Edit mode.  
* On the left side, under the graph location, select ***Query*** and underneath select the AnyLog data source unique name from the pull down list.
* The Metric window shows the list of tables supported by the database. Select a table from the options provided.

Grafana allows to present data in 2 modes:
* In a ***Time Series*** format and with reference to the time selection (on the upper right side of the panel).  
* In a ***Table*** format where data is presented in rows and columns.  

## Using the Time Series format
The time series format collects and visualize data values as a function of time.  
AnyLog offers 2 predefined queries and users can modify the default queries or specify additional queries using the ***Additional JSON Data*** options on the panel.    

### The predefined queries 
***The increments query*** (The default query)   
A query to retrieve statistics on the time series data in the selected time range.  
Depending on the number of data point requested, the time range is divided to intervals and the min, max and average are collected for each interval and graphically presented.  
In the default behavior, AnyLog makes the best guess to determine the relevant column representing the time and the relevant value column.  
The default behaviour can be modified by updating ***Additional JSON Data*** section (on the lower left side of the panel).  
To execute a period query, include the key: 'type' and the value: 'increments' in the Additional JSON Data section.  

***The period query***  
A query to retrieve data values at the end of the provided time range (or, if not available, before and nearest to the end of the time range).
The derived time is the latest time with values within the time range.         
From the derived time, the query will determine a time interval that ends at the derived time and provides the avg, min and max values.    
To execute a period query, include the key: 'type' and the value: 'period' in the Additional JSON Data section.  

More information on increments and period types of queries are available in [queries and info requests](https://github.com/AnyLog-co/documentation/blob/master/queries%20and%20info%20requests.md).
  
## Using the Table format
The default behaviour shows the data provided to the ***time series format*** with the default query. 
The default behaviour can be modified by updating ***Additional JSON Data*** section (on the lower left side of the panel).

## Modifying the default behaviour

Updating the ***Additional JSON Data*** section provides additional information to the query process.  
The information provided overrides the default behaviour and can pull data from any database managed by AnyLog (as long as the user maintains valid permissions).  
The additional information is provided using a JSON script with the following attribute names:

<pre>
dbms            - The name of the logical database to use. Overrides the dbms name in the configuration page.
table           - The name of the table to use. Overrides the table name in the sql statement.
type            - The type of the query. The default value is 'sq' and other valid types are: 'increments', 'period' and 'info'.         
sql             - A sql statement to use.
details         - An AnyLog command which is not a SQL statement.
where           - A "WHERE" condition added to the SQL statement. Can add filter or other conditions to the executed SQL.
time_column     - The name of the time column in the Time Series format.
value_column    - The name of the value column in the Time Series format.
time_range      - When using a Table view, determines if the query needs to consider the time range. The default value is 'true'.
servers         - Replacing the network determined servers with a list of Operators (data hosting servers) to use.
instructions    - Additional AnyLog query instructions.
</pre>

## Modifying the default behaviour using the Grafana Panel

### Modifying the time range
* A query issued using ***Time Series*** format is always bounded by the time range specified on the panel.
* A query issued using ***Table*** format is bounded by defauly with the time range.  
Users can modify the query to ignore the time selection by updating the Additional JSON Data with the key: 'time_range' and the value: 'false'.
<pre>  
Example:
{
    "sql" : "select * from ping_sensor",
    "time_range" : false
}
</pre>
### Modifying the query data points limit
Both types of queries - ***Time Series*** and ***Table*** are always bounded by ***Max data points*** that determine the number of entries returned.    
This value is configured by modifying the value ***Max data points*** in the Grafana ***Query Options*** on the panel.


## Examples

The examples below query data from logical tables in the AnyLog Network.  
In these examples, the table name is 'ping_senor', the name of the time column is 'timestamp' and the name of the value column is 'value'.  
When interval is considered, the interval is determined by dividing the time range by the number of data points requested. These values can be modified on the Grafana panel or specified in the query.    

### Executing an 'increments' query
A pre-defined qiery - for the time range in the panel, divide the time range to intervals and calculate min, max and average value for each interval in the range.
<pre> 
{
"type" : "increments",
"time_column" : "timestamp",
"value_column" : "value"
}
</pre>

### Executing a 'period' query
A pre-defined qiery that considers the time range in the panel, determines the last time with value and calculate the min max and average values for the data values in the interval.
<pre> 
{
"type" : "period",
"time_column" : "timestamp",
"value_column" : "value"
}
</pre>

### Executing a 'range' query
Depending on the number of data points, divide the time range into intervals and return the difference between the Max value and the Min value in each interval.
In the example below, the intervals are determined by the user to be one day intervals.
<pre>
{
"sql" : "select increments('day', 1, timestamp), max(timestamp), range(value) from ping_sensor",
"time_column" : "timestamp",
"value_column" : "value"
}
</pre>

### Executing multiple queries
The 2 queries below are defined on the same panel and provide visualization of 2 different devices (that are stored at the same table).  
Query 1:
<pre>
{
    "sql": "SELECT increments(), MIN(timestamp), MAX(timestamp), AVG(value) FROM ping_sensor",
    "where": "device_name='SPEED_SENSOR'",
    "time_column" : "timestamp",
    "value_column" : "value"
}
</pre>
Query 2:
<pre>
{
    "sql": "SELECT increments(), MIN(timestamp), MAX(timestamp), AVG(value) FROM ping_sensor",
    "where": "device_name='REMOTE-SENSOR'",
    "time_column" : "timestamp",
    "value_column" : "value"
}
</pre>

## Metadata Queries

The AnyLog Metadata can be queried using Grafana Table Format.
Metadata queries are specified using JSON in the ***Additional JSON Data*** section.  
Using the value ***info*** for the key ***type*** identifies a request which is not SQL.  
The request for Metada is specified using the key ***details***.   
Examples:  
Retrieving the tables in a database called lsl_demo:
<pre>
{
   "type" : "info",
   "details": "blockchain get table where dbms = lsl_demo" 
}
</pre>
Retrieving the list of Operators:
<pre>
{
   "type" : "info",
   "details": "blockchain get operator" 
}
</pre>
Retrieving the list of Publishers:
<pre>
{
   "type" : "info",
   "details": "blockchain get publisher" 
}
</pre>

## Using the Worldmap Panel to plot the AnyLog Network

The Worldmap Panel is a tile map of the world that can be overlaid with circles representing Nodes in the AnyLog Network and their status.

### Prerequisites

* Install the Grafana Worldmap plugin.  
 Instalation details are available on the [Grafana Worldmap Panel Page](https://grafana.com/grafana/plugins/grafana-worldmap-panel/installation).

* AnyLog Nodes registered on the blockchain with the following information:
    
    - Location information in the form of latitude and Longitude.  
    Location should be represented using the key: ***loc*** with the location values as a string with a comma separating between the latitude and Longitude.   
    For example: ```"loc": "33.836082,-81.163727"```      
    The example below demonstrates the AnyLog commands to map IP and Port to latitude Longitude:
    <pre>
    info = rest get where url = https://ipinfo.io/json
    coordinates = from !info bring ['loc']
    latitude = python !coordinates.split(',')[0]
    longitude = python !coordinates.split(',')[1]
    </pre>
    
    Additional optional information that is leveraged by the map:
    - Name
    - IP and Port
    - Hostname
    
### Configuring the Grafana Panel

The grafana Panel includes 2 sections that needs to be updated.

For the Query Info update the following fields:

* Format as: Table
* Matric: Any table
* In the Additional Json Data add the following keys and values:

| key  | value  | Explanation |
| ---- | -------| ------------|
| type | map | Queries the metadata to provide the list of nodes. |
| member | A list one or more members to query | The members listed would be shown on the map. |
| metric  | A list of integer values | Assigns a metric to each listed member. The metric determines the color on the map. |
| attribute | A list with an attribute name of each member / The value assigned to the attribute name in the Policy is shown when the cursor hovers over the circle |

Example:
<pre>
{
    "type" : "map",
    "member" : ["operator","publisher"],
    "metric" : [0,2],
    "attribute" : ["name", "hostname"]
}
</pre>

In the Panel Info under Map Data Options update the following fields:

* Table Query Format: coordinates
* Location Name Field: hostname
* Metric Field: metric
* Latitude Field: latitude
* Longitude Field: longitude

