---
title:  Publishing data via REST
description: How to insert data into AnyLog via REST — PUT vs. POST, mapping policies, and support commands.
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**            | **Version** |
|------------|----------------|-----------------------|----------|
| 2026-04-17 |                | creation              |          |
| 2026-04-25 |                | hyperlinks            |          |
| 2026-07-20 | Eric Aquaronne | added change log      | 2.0.2606 |
| 2026-07-24 | Ori Shadmon    | rewrite               |          |
--->

The following document provides directions on how to insert data via REST.

## Setting Up the Node

The `run rest` connection should be enabled by default as part of the configuration policy.

A more detailed explanation of this command can be found in the <a href="../../06-%20Networking%20&%20Security/02-%20Network%20Processing.md" target="_blank">network configuration section</a>.

```anylog
<run rest server where 
    external_ip = [external_ip ip] and external_port = [external port] and 
    internal_ip = [internal ip] and internal_port = [internal port] and 
    timeout = [timeout] and ssl = [true/false] and bind = [true/false]>
```

## Publishing Data via PUT

When publishing data into AnyLog via PUT, AnyLog takes the data as-is and stores it into the given database & table
based on the information in the headers.

**Sample Command**:

```shell
curl -X PUT http://[Operator IP]:[Operator Port] \
  -H "type: json" \
  -H "dbms: my_db" \
  -H "table: table3" \
  -H "mode: streaming" \
  -H "Content-Type: application/json" \
  -d '[
    {"timestamp": "2026-01-03 10:52:32", "sensor": "temp", "value": 80},
    {"timestamp": "2026-01-03 10:52:32", "sensor": "humidity", "value": 1.2},
    {"timestamp": "2026-01-03 10:52:32", "sensor": "maf", "value": 0.0}
  ]'
```

The data in this example would be stored under the `my_db` logical database, table `table3`.

### Header: Mode - streaming vs file

Data ingested to a local database is organized in files. Each file contains one or more sensor readings (or other type of time series data) organized in a JSON format.
Users adding data with the REST API determines the mode in which data is processed:

* Using a **File Mode** (the default mode) - a single data file is transferred using the PUT request, the file is registered (in the tsd_info table) and processed independently of other _PUT_ requests.  
A File Mode is usually used when the PUT request contains a large amount of data or when the data is not frequently created.  
    
* Using a **Streaming Mode** - The AnyLog instance receiving the data serves as a buffer that accumulates the data from multiple PUT requests. Upon a threshold, the accumulated data is organized as a file that is processed as a single unit.
A Streaming Mode is usually used when the frequency of data creation is high and the amount of data transferred in each PUT request is low.

File mode is the default mode. Changing the mode to streaming is by updating the header with the key _mode_ and the value _streaming_.  

**Header options for loading data**:

| key  | value  | Explanation |
| ---- | -------| ------------|
| mode | file | The body of the message is JSON data. Database load (on an Operator Node) and data send (on a Publisher Node) are with no wait. File mode is the default behaviour. |
| mode | streaming | The body of the message is JSON data that is buffered in the node. Database load (on an Operator Node) and data send (on a Publisher Node) are based on time and volume thresholds. |

## Publishing Data via POST

When publishing data via POST, we can manipulate the data more, since the user is defining the mapping logic for the
table, as opposed to letting AnyLog define it for them.

**Process**:
1. Define a mapping policy

> Sample `run msg client` command:
> ```anylog
> <run msg client where 
>  broker=rest and user-agent=anylog and 
>  log=false and topic=(
>   name=my-data and
>   dbms="bring [dbms]" and
>   table="bring [sensor]" and
>   column.timestamp.timestamp="bring [timestamp]" and
>   column.value.float="bring [value]"
> )>
> ```

```shell
curl -X POST http://[Operator IP]:[Operator Port] \
  -H "command: run msg client where broker=rest and user-agent=anylog and log=false and topic=(...)" \
  -H "AnyLog-Agent: AnyLog/1.23"
```

2. Publish data

```shell
curl -X POST http://[Operator IP]:[Operator Port] \
  -H "command: data" \
  -H "topic: my-data" \
  -H "AnyLog-Agent: AnyLog/1.23" \
  -H "Content-Type: application/json" \
  -d '[
    {"dbms": "my_db", "timestamp": "2026-01-03 10:52:32", "sensor": "temp", "value": 80},
    {"dbms": "my_db", "timestamp": "2026-01-03 10:52:32", "sensor": "humidity", "value": 1.2},
    {"dbms": "my_db", "timestamp": "2026-01-03 10:52:32", "sensor": "maf", "value": 0.0}
  ]'
```

Unlike with <a href="#publishing-data-via-put" target="_blank">REST-PUT</a>, each timestamp/value pair would be stored in its own table,
based on _sensor_, in the `my_db` logical database.

## Support Commands

* `get streaming` - statistics on the data flowing

```anylog 
Statistics
                          Put    Put     Streaming Streaming Cached Counter    Threshold   Buffer   Threshold  Time Left Last Process 
DBMS-Table                files  Rows    Calls     Rows      Rows   Immediate  Volume(KB)  Fill(%)  Time(sec)  (Sec)     HH:MM:SS     
-------------------------|------|-----|-|---------|---------|------|----------|-----------|--------|----------|---------|------------|
monitoring.docker_insight|     0|    0| |   49,842|   49,842|     5|         0|         10|   27.43|        60|       57|00:00:03    |
```

* `get msg client` - Information on messages received by clients subscribed to message brokers.

* `get operator` & `get publisher` - view the amount of data already processed through the operator or publisher node.