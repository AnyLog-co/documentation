---
title: Qlik 
description: Demonstration on how to connect between AnyLog and Qlik BI REST service
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

Qlik is a data integration, analytics, and artificial intelligence platform. Using their <a href="https://help.qlik.com/en-US/connectors/Subsystems/REST_connector_help/Content/Connectors_REST/REST-connector.htm" target="_blank">REST connector plugin</a>, 
users are able to pull data from AnyLog/EdgeLake and use it to generate insight on their data. 

## Requirements 
1. An active AnyLog network 
2. A subscription with Qlik 

## Preparing the Environment   
1. From _Home_ go to _Create_
2. In _Create_ select _Analytics App_
3. Data is coming from _Files & Other Data Sources_

!<a href="{{ '/docs/assets/img/qlik1.png/' | relative_url }}">Qlik source options</a>

4. Select _REST_ as the data source type

!<a href="{{ '/docs/assets/img/qlik2.png/' | relative_url }}">Qlik REST connector</a>

For this demo we'll be creating REST connections for the _increments_ and _period_ functions respectively.
The main components of the REST interface are the URL bar and cURL request headers.

| Qlik REST URL config | Qlik REST header config |
|---------------------|------------------------|
| !<a href="{{ '/docs/assets/img/qlik3.png/' | relative_url }}">Qlik REST URL config</a> | !<a href="{{ '/docs/assets/img/qlik4.png/' | relative_url }}">Qlik REST header config</a> |


## Increments Data 
The <a href="{{ '/docs/Querying-Data-Northbound/queries/#the-increment-function' | relative_url }}">increments function</a> segments time-series data into fixed, contiguous 
time intervals (e.g., every 5 minutes, every hour, every day).

1. Set the URL to the REST IP and port of the AnyLog node to query

!<a href="{{ '/docs/assets/img/qlik5.png/' | relative_url }}">Qlik URL field</a>
 
2. In the headers section add the following parameters: 
    * **command**: `sql nov format=json and stat=false and include=(t2) and extend=(@table_name) "select increments(second, 1, timestamp), min(timestamp) as timestamp, min(value) as min_val, avg(value) as avg_val, max(value) as max_val from t1 WHERE timestamp >= NOW() - 15 minutes ORDER BY timestamp"`
    * **User-Agent**: `AnyLog/1.23`
    * **destination**: `network`

!<a href="{{ '/docs/assets/img/qlik6.png/' | relative_url }}">Qlik headers</a>

3. Validate the data and continue

!<a href="{{ '/docs/assets/img/qlik7_increments.png/' | relative_url }}">Qlik increments data preview</a>

4. Create a new Analytics app

!<a href="{{ '/docs/assets/img/qlik8.png/' | relative_url }}">Qlik new analytics</a>

5. Create a graph using the available dimensions

!<a href="{{ '/docs/assets/img/qlik9_increments.png/' | relative_url }}">Qlik increments graph</a>

## Period Data 
The <a href="{{ '/docs/Querying-Data-Northbound/queries/#the-period-function' | relative_url }}">period function</a> finds the first occurrence of data before or at a specified 
date and considers readings within a time period defined by a type (minutes, hours, days, weeks, months, or years) 
and a unit count (e.g. 3 days).

1. Set the URL to the REST IP and port of the AnyLog node to query

!<a href="{{ '/docs/assets/img/qlik5.png/' | relative_url }}">Qlik URL field</a>
 
2. In the headers section add the following parameters: 
    * **command**: `sql nov format=json and stat=false and include=(t2) and extend=(@table_name) "select timestamp, value from t1 where period(minute, 1, now(), timestamp) order by timestamp"`
    * **User-Agent**: `AnyLog/1.23`
    * **destination**: `network`

!<a href="{{ '/docs/assets/img/qlik6.png/' | relative_url }}">Qlik headers</a>

3. Validate the data and continue

!<a href="{{ '/docs/assets/img/qlik7_period.png/' | relative_url }}">Qlik period data preview</a>

4. Create a new Analytics app

!<a href="{{ '/docs/assets/img/qlik8.png/' | relative_url }}">Qlik new analytics</a>

5. Create a graph using the available dimensions

!<a href="{{ '/docs/assets/img/qlik9_period.png/' | relative_url }}">Qlik period graph</a>