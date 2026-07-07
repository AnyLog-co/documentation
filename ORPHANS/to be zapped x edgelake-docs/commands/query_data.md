---
layout: default
title: Query Data 
parent: Commands
nav_order: 4
---
# Query Data

EdgeLake provides a unifies view of the distributed data. Using virtualization, users interact with the data as if the data is centralized.      
Using the following commands, users retrieve the list of tables, select a table, retrieve the table's column, and issue a query.  

## Retrieve the list of tables

The following command retrieves the list of tables:
<pre class="code-frame"><code class="language-anylog"> 
get virtual tables [info] where company = [company name] and dbms = [dbms name] and table = [table name]
</code></pre>

Examples:
<pre class="code-frame"><code class="language-anylog"> 
get virtual tables
get virtual tables where table = ping_sensor
</code></pre> 

The following command details the edge nodes that host each table:
<pre class="code-frame"><code class="language-anylog"> 
get data nodes where company = [company name] and dbms = [dbms name] and table = [table name] and sort = (columns IDs)
</code></pre>

Examples:
<pre class="code-frame"><code class="language-anylog"> 
get data nodes
get data nodes where table = ping_sensor
get data nodes where sort = (1,2)
</code></pre> 

## Retrieve the list of columns

The following command lists the columns of a table:
<pre class="code-frame"><code class="language-anylog"> 
get columns where dbms = [dbms name] and table = [table name] and format = [table/json]
</code></pre>

Example:
<pre class="code-frame"><code class="language-anylog"> 
get columns where table = ping_sensor and dbms = dmci

# Example output:

Schema for DBMS: 'my_dbms' and Table: 'printer_status'
Column Name      Column Type
----------------|---------------------------|
row_id          |integer                    |
insert_timestamp|timestamp without time zone|
tsd_name        |char(3)                    |
tsd_id          |int                        |
bed_temp        |decimal                    |
extruder_temp   |decimal                    |
current_file    |char(2)                    |
current_x       |decimal                    |
current_y       |decimal                    |
current_z       |decimal                    |
fan_speed       |float                      |

</code></pre>

Note: the first 4 columns (row_id, insert_timestamp, tsd_name, tsd_id) are added by default when the table is created and are used
for management and traceability of ingested data. Users can ignore these columns in their projection lists.

## SQL supported functionality

In depth details can be found in the [Query Nodes](https://github.com/AnyLog-co/documentation/blob/master/queries.md) section.

**Projection List**: 
* [increments function](#increments-function)
* Column name
* Min
* Max
* Sum
* Count
* Avg
* Count Distinct
* Range
* Time functions over Column values

**Where Conditions**:
* [period function](#period-function)
* Greater than 
* Less than 
* Equal 
* Not Equal 
* Group By 
* Order By 
* Limit

## Query Format 
**Sample Query**: 
<pre class="code-frame"><code class="language-anylog"># Query Format Breakdown 
run client () sql [db_name] format=[output_type] and stats=[true/false] [select statement] 

# Sample Query 
run client () sql litsanleandro format = table "select insert_timestamp, device_name, timestamp, value from ping_sensor limit 100"
</code></pre>

* `run client ()` directs the query to the relevant nodes in the network. When [executing via REST](../../examples/rest_examples), 
the `--headers "destination: network"` replaces the `run client ()` prefix.
* `format` determines the structure of the returned data:
  * `format=json` - The returned results are in JSON.
  * `format=table` - The returned results are in a table format.
  * `format=json:output` - The returned results are organized as rows whereas each row is a JSON structure - this format is identical to the 
data load structure.
  * `format=json;list`- The returned results are organized as a list, every entry in the list represents a row (use this format 
with [PowerBI](../../northbound/PowerBI)).
* The query result sets are extended by statistics that describe how the query was executed. Set `stats=false` to disable the statistics.    
   

## Built-in Query Functions

### Period Function
The `period` function finds the first occurrence of data before or at a specified date; if a filter-criteria is specified, 
the occurrence needs also to satisfy the filter-criteria.  
A period function, considers the readings in a period of time which is measured by the type of the time interval
(_Minutes_, _Hours_, _Days_, _Weeks_, _Months_ or _Years_) and the number of units of the time interval 
(i.e. 3 days - whereas time-interval is day and unit is 3).

**Sample Call**: 
<pre class="code-frame"><code class="language-anylog">run client () sql edgex format=table "select min(timestamp), max(timestamp), count(value) from rand_data WHERE period(day, 1, now(), timestamp);"</code></pre>

### Increments Function
The `increments` functions considers data in increments of time within a time range.   
The function has 3 sections: **time-interval**, **units** and **date-column**.
1. `time-interval` is (_Minutes_, _Hours_, _Days_, _Weeks_, _Months_ or _Years_)
2. `units` associated with the time interval (i.e. 2 weeks). 
3. `date-column` is the name of the column that determines the date and time to consider.

An Increment function returns a single value for time intervals within a time range. For example, rather than returning all column
values within a month, a query returns a smaller data set by returning the average, min and max values for every minute within the month.

**Sample Call**:
<pre class="code-frame"><code class="language-anylog">run client () sql edgex format=table "select increments(day, 1, timestamp), min(timestamp), max(timestamp), count(value) from rand_data  where timestamp >= now() - 1 month"</code></pre>






