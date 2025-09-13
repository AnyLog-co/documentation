# Aggregations 

**What is Aggregations**? 

Aggregation functions summarize streaming data over a time interval. 

Users define (per table) the time interval and the number of intervals per each table to allow continuous aggregations. 
The aggregated values can be queried or used to impact the database updates and monitoring. Aggregation functions are 
used to summarize streaming data over a specified time interval. These functions process incoming data continuously, 
computing key statistics such as counts, sums, averages, or max/min values over defined periods. Users define, per 
table, the length of time interval and the number of intervals to maintain.

For a detailed description, please refer to [this document](aggregations.md).

This document provides directions for deploying an aggregation process against a data set; whether it is a publisher 
or an operator node. 

## Requirements for Aggregations 
1. Timestamp column must be with sub-seconds. If the user data does not have timestamp column, then aggregations could 
be done against the `insert_timestamp` column
2. Aggregation is supported with only numeric data types - such as int, float and double. If boolean values are numeric 
(0 and 1) there's no point in setting aggregation as the values will ultimately converges toward 0, 1 or 0.5.  

## Running Aggregations
Aggregations are pretty straightforward to implement, 4 key things: 
* Database / table name 
* Timestamp column 
* Aggregation column (must be of numeric type - int, float, double, etc.)
* Frequency of aggregation. 

Since time-series tables often have multiple columns, or there are multiple tables that require aggregation, we 
developed a python3 script that automates the process. The script also allows you to automatically create a unique 
policy based on dbms.table.column_name (numeric data type). 


### Directions 

In version 1.4.X and later of AnyLog / EdgeLake, the python scripts provided in this document are in docker volume 
`local-scripts` under `sample-scripts/set-aggregations`. The docker container is pre-configured to allow running this 
script from within it. 

The following are steps to run it outside the docker container (and older versions of AnyLog / EdgeLake)

0. Please make sure aggregation related tables exist in the blockchain before hand **or** assert data is flowing in. 

1. Download Script 

```shell
cd $HOME 
wget raw.githubusercontent.com/AnyLog-co/deployment-scripts/refs/heads/os-dev2/sample-scripts/set_aggregations.py
```

2. Run script

```shell
# as is
python3 set_aggregations.py {REST CONN} {LOGICAL DATABASE}  [--create-policies] 

# specify table, comma separate multiple tables  
python3 set_aggregations.py {REST CONN} {LOGICAL DATABASE}  --table [{DB}.{table}]  [--create-policies] 
``` 

The script generates a policy for each of the columns with valid data type. This is so users can easily pull 
aggregation insight for a specific table / column in Grafana and other BI tools. However, that may be too comprehensive 
or simply not needed for different use cases. In such cases please either ignore `--create-polices` or update the script
as you see fit.