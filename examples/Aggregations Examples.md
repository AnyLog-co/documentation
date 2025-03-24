# Aggregations Examples

This document provides examples of aggregations. The commands details are available in the [Aggregations Sections](../aggregations.md)

Prerequisite: 
* AnyLog node deployed
* The tables **intervals** and **compression** are not declared (as the table structure is defined by the aggregation declaration and not by the source data).
* Data Generator deployed

## Configuring Bounds Aggregations

In **bounds aggregations** all entries in the time interval are replaced with a single entry.

The following commands declare the following:

* A database name **examples** using SQLite.
* An aggregation table named **intervals**.
* Apply **bounds encoding** on the table's data (modify the source data structure to include Min, Max, Avg and Count for every time interval)
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
set aggregations encoding where dbms = examples and table = intervals and encoding = bounds and tolerance = 10
```

### Insert Data

Using the AnyLog data generator, issue the following command:

```anylog

```

### View the memory representation of the aggregations

```anylog
get aggregations where dbms = examples and table = intervals
```

### Query the aggregation Data

```anylog
run client () sql examples format = table select ... 
```


## Configuring arle Aggregations

arle - Approximated Run-Length Encoding, the entries in the time interval are represented in one or more entries, each entry represents multiple similar values. 

The following commands declare the following:

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
set aggregations encoding where dbms = examples and table = compression and encoding = bounds and tolerance = 10
```


### Insert Data

Using the AnyLog data generator, issue the following command:

```anylog

```

### View the memory representation of the aggregations

```anylog
get aggregations where dbms = examples and table = compression
```

### Query the aggregation Data

```anylog
run client () sql examples format = table select ... 
```