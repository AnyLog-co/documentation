# Using Grafana

## Overview

Users can use grafana as a visualization tier.  
Using REST, Grafana communicates with AnyLog to retrieve the data such that the Grafana visualization can be leveraged.

## Prerequisites

* Grafana instance installed.
* An AnyLog Node that provides a REST connection.
To configure an AnyLog Node to satisfy REST calls, issue the following command on the AnyLog command line:  
```run rest server [ip] [port] [max time]```  
[ip] and [port] are the IP and Port that would be available to REST calls.  
[max time] is am optional value that determines the max execution time in seconds for a call before being aborted.  
A 0 value means a call would never be aborted and the default time is 20 seconds.  
 
## Establishing connection

Open the Grafana ***Data Sources*** configuration page.

* select a JSON data source.
* On the URL Tab add the REST address (i.e. http://10.0.0.25:2049)
* On the ***Custom HTTP Headers*** name the default database to use as follows:  
```al.dbms.[table name]```  For example: al.dbms.lsl_demo  
Declaring the database connects Grafana to the specified database and makes the database tables available to query.  
***Note:*** to interact with a different database, create a new JSON data source and declare a different database name in the headers.





  





