# Using Grafana

## Overview

AnyLog users can leverage Grafana as a visualization tier using a build-in/transparent interface that maps Grafana calls to queries over data maintained in the AnyLog Network.  
Using a HTTP and JSON API, Grafana communicates with AnyLog to retrieve data such that the Grafana visualization can be leveraged.

## Prerequisites

* Grafana instance installed.
* An AnyLog Node that provides a REST connection.
To configure an AnyLog Node to satisfy REST calls, issue the following command on the AnyLog command line:  
```run rest server [ip] [port] [max time]```  
[ip] and [port] are the IP and Port that would be available to REST calls.  
[max time] is am optional value that determines the max execution time in seconds for a call before being aborted.  
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

## Using Grafana to visualize AnyLog data

* On the Grafana menu, use the ***+*** sign to create a new panel.
* Or, open an existing panel in Edit mode.
* The Metric window shows the list of tables supported by the database. Select a table from the options provided.

Grafana allows to present data in 2 modes:
* In a ***Time Series*** format and with reference to the time selection (on the upper right side of the panel) .
* In a ***Table*** format.

#### Using the Time Series format
The default behaviour - AnyLog issues a query to the selected table for the data in the selected time range.
Depending on the number of data point requested, the query time range is divided to intervals and the min, max and average are collected for each interval and graphically presented.  
In the default behavior, AnyLog makes the best guess to determine the relevant column representing the time and the relevant value column.  
The default behaviour can be modified by updating ***Additional JSON Data*** section (on the lower left side of the panel).
  
 #### Using the Table format
The default behaviour shows the data provided to the ***time series format*** with the default query. 
The default behaviour can be modified by updating ***Additional JSON Data*** section (on the lower left side of the panel).

## Modifying the default behaviour

Updating the ***Additional JSON Data*** section will provide additional information to the query process.  
The information provided overrides the default behaviour and can pull data from any database managed by AnyLog (as long as the user maintains valid permissions).  
The additional information is provided using a JSON script and the user can specify anyone of the following elements:

  







  





