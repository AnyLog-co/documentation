# Aggregations Examples

This document provides examples of aggregations. The commands details are available in the [Aggregations Section](../aggregations.md).


## Configuring Bounds Aggregations

In **bounds aggregations** all entries in the time interval are replaced with a single entry.

The following commands declare bounds aggregation over the table's data:

* A database name **examples** using SQLite.
* An aggregation table named **intervals**.
* Apply **bounds encoding** on the table's data (modify the source data structure to include Min, Max, Avg and Count for every time interval).
* Inserting data into **intervals**.

### Declare the DBMS

```anylog
connect dbms examples where type = sqlite
```

### Declare an aggregation table

```anylog
set aggregations where dbms = examples and table = intervals and time_column = timestamp and value_column = value
```

### Apply bounds encoding

```anylog
set aggregations encoding where dbms = examples and table = intervals and encoding = bounds
```

### Retrieve the declarations
```anylog
get aggregations config where dbms = examples and table = intervals
```

### Insert Data

Using the data source, add data to the **intervals** table

### View the memory representation of the aggregations

```anylog
get aggregations where dbms = examples and table = intervals
```

### Query the aggregation Data

```anylog
run client () sql examples format = table and timezone = pt "select timestamp, end_interval, min_val, max_val, avg_val, events from bounds_intervals"
```
Note: the table name in the database is prefixed with the keywords **"bounds_"**

### Query the most recent value
The function name is one of the following: **min, max, count, avg**.

```anylog
get aggregations where dbms = examples and table = intervals and function = max
```

## Configuring arle Aggregations

ARLE - Approximated Run-Length Encoding, the entries in the time interval are represented in one or more entries, each entry represents multiple similar values. 

The following commands declare ARLE compression over the table's data:

* A database name **examples** using SQLite.
* An aggregation table named **compression**.
* Apply **arle encoding** on the table's data (modify the source data structure to include a value and counter for the repetitions in every interval)
* Inserting data into **compression**.

### Declare the DBMS

```anylog
connect dbms examples where type = sqlite
```

### Declare an aggregation table

```anylog
set aggregations where dbms = examples and table = compression and time_column = timestamp and value_column = value
```

### Apply arle encoding

```anylog
set aggregations encoding where dbms = examples and table = compression and encoding = arle and tolerance = 10
```
Note: tolerance 10 means that 10% deviation from the initial value is considered unchanged value.

### Retrieve the declarations
```anylog
get aggregations config where dbms = examples and table = compression
```

### Insert Data

Using the data source, add data to the **intervals** table.

### View the memory representation of the aggregations

```anylog
get aggregations where dbms = examples and table = compression
```

### Query the aggregation Data

```anylog
run client () sql examples format = table "select timestamp, end_interval, avg_value, events from arle_compression"
```

### Query the most recent value
The function name is one of the following: **min, max, count, avg**.

```anylog
get aggregations where dbms = examples and table = intervals and function = max
```