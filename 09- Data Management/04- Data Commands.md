---
title: "Data Commands"
description: "CLI commands for querying, backing up, and partitioning data: SQL, backup, partition, and drop partition."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-07-26 | Ori Shadmon    | New page — Backup/Partition/Drop Partition split out of "01 Anylog Commands.md"; SQL Command section pending | |
--->

# Data Commands

## SQL Command

> **Pending** — this section will document the `sql` command (querying data hosted by members of the network,
> `run client () sql ...`, query options, and predefined time-series SQL functions). To be filled in once the
> source content for this section is available.

## Backup Command

The ***backup*** command transfers data from a local database to a file for archival.
If the table's data is not partitioned, the backup includes the entire table's data set.
If the table data is partitioned, the backup operates at a partition level and can include one partition or all the partitions of the table.

Usage:
```anylog
backup table where dbms = [dbms name] and table = [table name] and partition = [partition name] and dest = [output directory]
```

Explanation:

Backup the data of a particular partition or all the partitions of a table.
Partition name is optional — if omitted, all the partitions of the table participate in the backup process.
If the table is not partitioned, the entire table participates in the backup process.
The data of each partition is written into a file at the location specified with the keyword `dest`.
The file data is organized in a JSON format which can be processed and ingested by a node in the network.

Examples:
```anylog
backup table where dbms = purpleair and table = readings and dest = !bkup_dir
backup partition where dbms = purpleair and table = readings and partition = par_readings_2018_08_00_d07_timestamp and dest = !bkup_dir
```

## Partition Command

Users' data is maintained on local databases organized in tables. As the data is ***time series data***, it is possible to organize the data in partitions based on time.
If the data of a table is partitioned, the partitioning is hidden from users and applications. Users interact with the data using the table name and the distribution of the processing to the different partitions is transparent.
Any date-time column can be leveraged as the partition column.

Usage:
```anylog
partition [dbms name] [table name] using [column name] by [time interval]
```

Time interval options are:
* year
* month
* week
* day

The time interval can be assigned with a counter (and can be expressed as singular or plural) — for example, ***3 months*** sets 4-month partitions.

Examples:
```anylog
partition lsl_demo ping_sensor using timestamp by 2 days
partition lsl_demo ping_sensor using timestamp by month
partition lsl_demo * using timestamp by month
```

### Partitions status and configurations

The following command lists the partitions configurations:
```anylog
get partitions
```

The ***info table*** command provides information on the partitions existing on the node:

Usage:
```anylog
 info table [db name] [table name] [info type]
```
- [dbms name] — the name of the logical database containing the table and its partitions
- [table name] — the name of the table
- [info type] — the type of the requested info

The type of information provided on each table is determined by the ***info type*** as follows:

| Info Type | Details |
|---|---|
| exists | Returns 'true' or 'false' indicating if the table exists |
| columns | The table's/partition's columns names and data types |
| partitions | The list of partitions of the specified table |
| partitions last | The name of the last partition (by the partition date/time interval) |
| partitions first | The name of the first partition (by the partition date/time interval) |
| partitions count | The number of partitions |
| partitions dates | The date/time interval assigned to each partition |

Examples:
```anylog
info table sensors readings columns
info table sensors readings exists
info table sensors readings partitions
info table sensors readings partitions last
info table sensors readings partitions first
info table sensors readings partitions count
```

## Drop Partition Command

When data needs to be removed from a node, users can process the removal by dropping partitions. As the data is partitioned by time, it is possible to drop the oldest partition while the system continues to process data with the remaining partitions.
Users can leverage the [Backup command](#backup-command) prior to dropping a partition.

Usage:
```anylog
drop partition [partition name] where dbms = [dbms name] and table = [table name] and keep = [value]
```

Explanation:

Drops a partition in the named database and table.
* [partition name] is optional. If omitted, the oldest partition of the table is dropped; if the table has only one partition, an error value is returned.
* [keep] is optional. If a value is provided, the oldest partitions will be dropped to keep the number of partitions at the value provided.
* If table name is asterisk (`*`), a partition from every table in the specified database is dropped.
* If partition name is asterisk (`*`), all partitions are dropped.

Examples:
```anylog
drop partition par_readings_2019_08_02_d07_timestamp where dbms = purpleair and table = readings
drop partition where dbms = purpleair and table = readings
drop partition * where dbms = purpleair and table = readings
drop partition where dbms = aiops and table = factualvalue and keep = 5
```
