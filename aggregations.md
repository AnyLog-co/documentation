# Aggregation Functions

Aggregation functions summarize streaming data over a time interval. Users define (per table) the time interval and the number of intervals
per each table to allow continues aggregations. The aggregated values can be queried or used to impact the database updates and monitoring.

Aggregation functions are used to summarize streaming data over a specified time interval. These functions process incoming 
data continuously, computing key statistics such as counts, sums, averages, or max/min values over defined periods.    
Users define, per table, the length of time interval and the number of intervals to maintain.   

Notes: 
1. Deployment examples are in the [Aggregations Examples](examples/Aggregations%20Examples.md) section.
2. Example of aggregations applied on data retrieved by the AnyLog OPC UA service is available in the [Declaring OPC UA with Aggregations](opcua.md#example---declaring-opc-ua-with-aggregations) section.

## How They Work:
* Users define a time interval (e.g., 1 minute, 5 minutes, or hourly).
* Users define the number of intervals to maintain.
* The system continuously aggregates incoming data within each interval.
* Aggregated values can be used in real-time for:
  * Querying the current trends
  * Triggering alerts or monitoring changes
  * dImpacting database updates (e.g., adjusting thresholds dynamically)

Users can replace the source data with encoding. With high volumes of data streams, encoding reduces the volumes of data processed. 

## Declaring Aggregations

Using the command `set aggregation` users can track data streamed to a node for storage and processing. This type of 
monitoring considers the tables that contain the data and the monitoring aggregates information on the streaming values 
within predefined time intervals. Intervals are time segments for which the following are monitored on a predefined column 
value:

| Monitored value option | Details  |
| ------------- | ------------| 
| Min  | The lowest value recorded within the time interval. | 
| Max  | The highest value recorded within the time interval. | 
| Avg | The average value within the time interval. |
| Count | The number of events recorded within the time interval. |
| Events/sec | The number of events recorded divided by the number of seconds in the interval. |


Usage: 
```anylog
set aggregation where dbms = [dbms name] and table = [table name] intervals = [counter] and time = [interval time] 
      and time_column = [time column name] and value_column = [value column name]
      and target_dbms = [target dbms name] and target_table = [target table name]
```

| Command option | Default     | Details                                                                                                                                     |
|----------------|-------------|---------------------------------------------------------------------------------------------------------------------------------------------| 
| dbms           |             | The name of the database that hosts the table's data.                                                                                       | 
| table          |             | The data table name. If table name is not provided, all the tables associated to the database are monitored using the database definitions. | 
| intervals      | 10          | The number of intervals to keep.                                                                                                            |
| time           | 1 minute    | The length of the interval expressed in one of the following: seconds, minutes, hours, days.                                                |
| time_column    | "timestamp" | The name of the time column.                                                                                                                |
| value_column   | "value"     | The name of the column being monitored.                                                                                                     |
| target_dbms    | [dbms]      | The name of the dbms to host the aggregation data. Defaults to the same as the source dbms if not provided.                                 |
| target_table   | [table]     | The name of the table to host the aggregation data. Defaults to the same as the source table.                                                                                        |

Example: 
```anylog
set aggregations where dbms = dmci and table = sensor_table and intervals = 10 and time = 1 minute and time_column = timestamp and value_column = value
```
**Note:**
The **set aggregations** command enables aggregation on a stream of data identifies by the DBMS and Table assigned to the stream.
  It can be followed by a one or more commands that determine additional functionalities such as:
   * [Declaring Thresholds](#declaring-thresholds) that can be referenced in the rule engine.
   * [Aggregation Encoding](#aggregation-encoding) that provide compression to the data stream.

## Declaring Thresholds

Users can declare thresholds on each stream. These thresholds can be referenced by the rule engine to impact the processing 
of the stream and trigger operations that consider the thresholds.

Usage:
```anylog
set aggregations thresholds where dbms = [dbms name] and table = [table name] and and min = [min value] and max = [max value] and avg = [average value] and count = [events count] 
 ```

## Reset aggregations

The command `reset aggregations` deletes the aggregation declarations.      
Usage:
```anylog
reset aggregations where dbms = [dbms name] and table = [table name] and value_column = [column name]
```
* If table name is not provided, aggregations associated with all the tables assigned to the database are removed.
* If column name is not provided, aggregations associated with all the columns assigned to the table are removed.

## Aggregation encoding

The command `set aggregations encoding` applies encoding on the values assigned to each time interval.  
The encoding is represented by a new data set associated to a new schema (described below, for each type of encoding).  
The table name with the encoding format is using the original table name, prefixed by the encoding type.  
For example, if the source data is assigned to a table named **my_table** and the encoding type is **arle**, 
the table with the encoded data is called **arle_my_table**.

Usage:
```anylog
set aggregations encodeing where dbms = lsl_demo and table = ping_sensor and encoding = [encoding type] and tolerance = [value]
```

**Encoding types:**

* None - No encoding (default).


* bounds - all entries in the time interval are replaced with a single entry representing: 
  * **timestamp** - The earliest date and time of the entries represented in the interval.
  * **end_interval** - The latest date and time of the entries represented in the interval.
  * **min_val** - The lowest value recorded within the time interval.
  * **max_val** - The highest value recorded within the time interval.
  * **avg_val** - The average of the values recorded within the time interval.
  * **events** - The number of events recorded within the time interval.


* arle - Approximated Run-Length Encoding, the entries in the time interval are represented in a sequence of entries. Each entry includes:
  * **timestamp** - The earliest date and time of the entries represented in the interval.
  * **end_interval** - The latest date and time of the entries represented in the interval.
  * **avg_val** - average of grouped values.
  * **events** - The number of events recorded within the time interval.
      
 **tolerance**  
With Approximated Run-Length Encoding, allowable difference between consecutive values while treating them as part of the same group or segment.    
Tolerance is represented as percentage difference. 

Example:
```anylog
set aggregations encoding where dbms = lsl_demo_ok and table = rand_table and encoding = arle and tolerance = 5
```

## 📥 Retrieve Aggregations

The command `get aggregations` retrieves the monitored data configured via the `set aggregation` command.

### 🔧 Usage Examples

```anylog
get aggregations 
get aggregations where dbms = orics
get aggregations where dbms = orics and table = r_50
get aggregations where dbms = orics and table = r_50 and value_column = seal_storage
```
Each command filters the aggregation definitions based on the provided criteria (dbms, table, and value_column).

### Sample output
```anylog

DBMS  Target DBMS Table Target Table          Vlue Column      interval H:M:S       Events/sec Count Min     Max     Avg
-----|-----------|-----|---------------------|----------------|--------|-----------|----------|-----|-------|-------|-------|
orics|orics_agg  |r_50 |r_50_seal_storage    |seal_storage    |       0|0:3:0      |      0.17|   10| 11.020| 93.030| 39.064|
orics|orics_agg  |r_50 |r_50_heater1_temp    |heater1_temp    |       0|0:0:0      |      0.17|   10|103.010|299.290|202.909|
orics|orics_agg  |r_50 |r_50_heater1_setpoint|heater1_setpoint|---     |Not Started|---       |    0|---    |---    |---    |
orics|orics      |r_50 |r_50                 |value           |---     |Not Started|---       |    0|---    |---    |---    |
```
| Column Returned | Details                                                                                                                                           |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------| 
| DBMS            | The name of the source database.                                                                                                                  |
| Target DBMS	    | The database where the aggregated data is stored.                                                                                                | 
| Table           | The name of the source table being monitored.                                                                                                     |
| Target Table    | The name of the table that stores the aggregated results.                                                                                         |
| Value Column    | TThe column being aggregated (e.g., temperature, pressure, etc.).                                                                                    | 
| Interval        | The sequential ID of the interval, if time in **set aggregation** command is set to 1 minute, the data added from second 180 to 240 is Interval 2 |
| H:M:S           | The time elapsed since the interval data was processed (to the current interval)                                                                  |
| Count           | The number of rows (readings) processed in the interval.                                                                                          |
| Min             | The Min value processed in the interval.                                                                                                          |
| Max             | The Max value processed in the interval.                                                                                                          |
| Avg             | The Average value processed in the interval.                                                                                                      |

## Retrieve aggregations by time

The command `get aggregations by time` retrieves the interval summaries **by date and time**.

```anylog
get aggregations by time where dbms = [dbms name] and table = [table name] and value_column = [column name] and function = [function name] and limit = [limit] and format = [table/json]  
```
Command options:

| Option       | Default                  | Details                                                                                               |
|--------------|--------------------------|-------------------------------------------------------------------------------------------------------|
| dbms         |                          | Database name                                                                                         |
| table        |                          | Table name                                                                                            |
| value_column |                          | One or more column names. The asterisks (*) retrieves all table columns                               |
| function     | count, avg, min, max     | One or more of the aggregation function. Each function can be extended by casting (see details below) |
| timezone     | local (of the edge node) | The timezone for the timestamp value.                                                                 |
| format       | table                    | The returned format - table or JSON                                                                  |

**Examples:**
```anylog
get aggregations by time where dbms = nov and table = table_3 and value_column = seal_storage
get aggregations by time where dbms = nov and table = table_3 and value_column = seal_storage and format = json and function = min and function = max
get aggregations by time where dbms = orics and table = r_50 and value_column = cy_min and value_column = outfeed_conv_i and function = min and function = max and function = avg and function = count and format = json
get aggregations by time where dbms = orics and table = r_50 and value_column = *  
```

**Casting:**

Functions can be extended using casting (like columns and functions in a query). See details in the [Cast Data](https://github.com/AnyLog-co/documentation/blob/master/queries.md#cast-data) section.

**Example:**
```anylog
get aggregations by time where dbms = orics and table = r_50 and value_column = cy_min and function = min::int and function = max and function = avg::float(3) and function = count and format = json
```




### Aggregations can be called fom the Grafana Dashboard by specifying the following in the Payload section:

* **type** - "aggregations"
* **servers** - the target server IP and Port. Only a single server is allowed per each Payload.
* **functions** - the list of aggregation function to call (optional)

Example Payload: 
```anylog
{
  "servers": [
    "10.0.0.78:7848"
  ],
  "type": "aggregations",
  "functions" : ["min", "max"]
}
```

Note: Grafana configuration is detailed in the [Using Grafana](northbound%20connectors/using%20grafana.md) section.

## Retrieve aggregation configurations

The following command retrieves the aggregation declarations:
```anylog
get aggregation configs
get aggregation configs where dbms = lsl_demo and table = ping_sensor
```

## Retrieve the most recent value

The following command retrieves the most recent value:
```anylog
get aggregations where dbms = [dbms name] and table = [table name] and function = [function name]
```
The function name is one of the following: **min, max, count, avg**

Example:
```anylog
get aggregations where dbms = lsl_demo and table = ping_sensor and function = max
```

## Retrieve aggregation tables

The `get aggregation tables` command provides information about the ingestion of aggregation tables into the local database.

### Description
This command retrieves metadata and ingestion status for tables used in aggregations. 
It monitors the ingestion process of aggregated data from streaming sources into the local database.


### Usage
```anylog
get aggregation tables where dbms = [dbms name] and table = [table name]
```
### Example
```anylog
get aggregation tables where dbms = orics and table = r_50
```

## Set Ingestion Frequency for Aggregation Tables

The `set ingestion in aggregations` command allows you to modify or stop the ingestion frequency of aggregation tables in the local database.


### Usage
```anylog
set ingestion in aggregations where dbms = [dbms name] and table = [table name] and frequency = [frequency] and interval = [interval]
```

### Description
This command controls how frequently the system ingests data from aggregation tables. It can:
* Enable continuous real-time ingestion
* Configure time-based ingestion
* Stop ingestion for specific tables

If dbms and table are omitted, the command applies globally to all aggregation tables.

### Parameters

| Name       | Required | Type        | Description                                                                 |
|------------|----------|-------------|-----------------------------------------------------------------------------|
| `dbms`     | No       | `string`    | Name of the DBMS. If omitted, applies to all DBMSs.                        |
| `table`    | No       | `string`    | Name of the table. If omitted, applies to all tables in the specified DBMS.|
| `frequency`| Yes      | `string`    | Ingestion mode. Options: `continuous`, `time`, or `none`.                  |
| `interval` | Conditionally (if `frequency = time`) | `int` (with time unit) | Time interval for ingestion (e.g., seconds, minutes). Ignored for other modes. |

### Examples
```anylog
set ingestion in aggregations where dbms = orics and table = r_50 and frequency = continuous
set ingestion in aggregations where dbms = orics and frequency = time and interval = 1 minute
set ingestion in aggregations where dbms = orics and table = r_50 and frequency = none   # Stop Ingestion
```