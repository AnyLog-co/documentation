---
title: "Qlik"
description: Demonstration on how to connect between AnyLog and Qlik BI REST service
layout: page
source_path: "northbound connectors/02 Qlik How to.md"
---
<!--
### 📜 Change Log

| **Date** | **Name** | **Change** | **Version** |
|---|---|---|---|
| 2026-04-17 | | Created document | |
| 2026-07-14 | | Merged the two overlapping Qlik docs (`Qlik.md` and `Qlik Connector.md`) into this single file.
  Base is `Qlik Connector.md` — its images use working `<img>` tags, where `Qlik.md`'s use a broken Jekyll-era
  `!<a href="{{ relative_url }}">` construct that doesn't render as an image. Fixed one typo carried in
  `Qlik Connector.md` ("QLik" → "Qlik"). Kept `Qlik.md`'s fuller Period function explanation (the filter-criteria
  caveat and the worked "3 days" example), which `Qlik Connector.md` was missing. | |
| 2026-07-20 | Eric Aquaronne | Added change log | 2.0.2606 |
| 2026-07-25 | Ori Shadmon | Resolved a doubly-nested, unresolved git merge conflict sitting in this file's changelog
  header (present in two separate re-uploads of this same already-merged file — just the header was still
  conflicted, not the body). Also confirmed "02 Qlik How to.md," uploaded alongside, is the stale pre-merge
  `Qlik.md` source already described above — excluded, nothing new in it. **Flagging separately:** one of the
  conflict markers referenced a folder path containing a stray backtick (`...data source\`/`) — this is the
  *second* time this exact broken path has turned up (the first was in the Grafana doc's PowerBI cross-link),
  which suggests an actual typo'd folder name somewhere in the repo rather than two unrelated one-off link typos.
  Worth fixing the folder name itself rather than patching around it in each link that points to it. | |
-->

# Qlik

Qlik is a data integration, analytics, and artificial intelligence platform. Using their <a href="https://help.qlik.com/en-US/connectors/Subsystems/REST_connector_help/Content/Connectors_REST/REST-connector.htm" target="_blank">REST connector plugin</a>, 
users are able to pull data from AnyLog/EdgeLake and use it to generate insight on their data. 

## Requirements 
1. An active AnyLog network 
2. A subscription with Qlik 

## Preparing the Environment   
1. From _Home_ goto _Create_
2. In _Create_ we want to use the _Analytics App_
3. Data is coming from _Files & Other Data  Sources_

<img src="../imgs/qlik1.png" height=50% width=50% alt="source options" />

4. We use a standard _REST_

<img src="../imgs/qlik2.png" height=50% width=50% alt="source options" />

For this demo we'll be creating REST connections for _increments_ and _period_ function respectively.
The main components of the REST interface delt with are the URL bar and cURL request headers. 

| <img src="../imgs/qlik3.png" height=50% width=50% /> | <img src="../imgs/qlik4.png" height=50% width=50% /> |
| :----: | :----: |

## Increments Data 
The [increments function](../07-%20CLI/04-%20SQL.md#the-increment-function) is used to segment time-series data into fixed, contiguous 
time intervals (e.g., every 5 minutes, every hour, every day).

1. For the URL specify the REST IP and port of the node to send the request against

<img src="../imgs/qlik5.png" height=50% width=50% />
 
2. In the headers section add the following params: 
    * **command**: `sql nov format=json and stat=false and include=(t2) and extend=(@table_name) "select increments(second, 1, timestamp), min(timestamp) as timestamp, min(value) as min_val, avg(value) as avg_val, max(value) as max_val from t1 WHERE timestamp >= NOW() - 15 minutes ORDER BY timestamp"`
    * **User-Agent**: `AnyLog/1.23`
    * **destination**: `network`

 <img src="../imgs/qlik6.png" height=50% width=50% />

3. Validate the data and continue 

<img src="../imgs/qlik7_increments.png" height=50% width=50% />

4. Create a new Analytics

<img src="../imgs/qlik8.png" height=50% width=50% />

5. Create a graph based on the given Dimensions 

<img src="../imgs/qlik9_increments.png" height=50% width=50% />

## Period Data 
The [period function](../07-%20CLI/04-%20SQL.md#the-period-function) finds the first occurrence of data before or at a specified 
date (and if a filter-criteria is specified, the occurrence needs to satisfy the filter-criteria) and considers the 
readings in a period of time which is measured by the type of the time interval (Minutes, Hours, Days, Weeks, Months 
or Years) and the number of units of the time interval (i.e. 3 days - whereas time-interval is day and unit is 3).

1. For the URL specify the REST IP and port of the node to send the request against

<img src="../imgs/qlik5.png" height=50% width=50% />
 
2. In the headers section add the following params: 
    * **command**: `sql nov format=json and stat=false and include=(t2) and extend=(@table_name) "select timestamp, value from t1 where period(minute, 1, now(), timestamp) order by timestamp"`
    * **User-Agent**: `AnyLog/1.23`
    * **destination**: `network`

<img src="../imgs/qlik6.png" height=50% width=50% />

3. Validate the data and continue 

<img src="../imgs/qlik7_period.png" height=50% width=50% />

4. Create a new Analytics

<img src="../imgs/qlik8.png" height=50% width=50% />

5. Create a graph based on the given Dimensions

<img src="../imgs/qlik9_period.png" height=50% width=50% />