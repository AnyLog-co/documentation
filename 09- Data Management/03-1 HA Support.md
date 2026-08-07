---
title: "HA Support"
description: "The database and storage backends AnyLog can connect to — SQL, NoSQL, blob/object storage, and vector search."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**       | **Version** |
 |------------|-------------|------------------|----------|
 | 2026-07-28 | Ori Shadmon | Split "NoSQL / Blob storage" into two separate categories (NoSQL document DB vs. object/blob storage — different technology categories); restructured the S3-compatible bullets so AWS S3/MinIO/Akave are siblings rather than MinIO/Akave nested under AWS S3; fixed "PostgresSQL" → "PostgreSQL"; added a brief note on what Akave actually is; added frontmatter/H1 (missing entirely); typo/grammar fixes | |
--->

## Overview

High availability in AnyLog rests on three things working together: every ingested file is **archived** so it can be 
replayed if a node needs to catch up, the network exposes commands to **test and locate** where each table's data 
actually lives across a cluster, and each file's ingestion is tracked in a **TSD (Time Series Data)** table so gaps, 
errors, and sync status can be audited. The sections below walk through each piece — archiving, cluster/data-location 
testing, and TSD/file commands — as parts of that same HA story.

## Archive Recording

### The Archive of Source Data

When a data file is provided to an Operator, the file is ingested into the local database. The source file is then 
compressed and archived so it can later be used to complete a data set on another Operator node if requested.

The location of the archive is configurable, and the root of the archive is addressed by the `archive_dir` parameter. 
The following command displays the location:
```anylog
!archive_dir
```

The subdirectories of the archive partition the files by days using the following hierarchy: Year → Month → Day. 
Users can navigate in the hierarchy using the `get directories` and `get files` commands.

The example below retrieves the list of files ingested on April 4th, 2021:
```anylog
get files !archive_dir/21/04/04
```

The `get tsd errors` command lists the files which were not properly ingested, and each listed file name includes the 
directory name where the file is archived, as in the example below.

A listed file name:
```anylog
/app/AnyLog-Network/data/archive/21/04/04/litsanleandro.ping_sensor.0.bd617b6ddb873750d9db561814297f23.0.120.119.210404201021.json
```

The archive directory is determined by the first 6 digits of the last field in the file name — the name segment before 
the file type, representing the file ingestion date and time (`210404201021` in the example above). Details on file 
naming are available in the file naming convention section.

### Blobs Archiver

Manages storage of large binary objects (images, video, audio) by routing them to a dedicated blobs database, a folder, 
or both.

```anylog
<run blobs archiver where
  blobs_dir = [data dir] and archive_dir = [archive dir] and
  dbms = [true/false] and file = [true/false] and compress = [true/false]>
```

| Option | Description | Default |
|---|---|---|
| `blobs_dir` | Directory where blobs are staged before archival | `!blobs_dir` |
| `archive_dir` | Root directory for archived blobs | `!archive_dir` |
| `dbms` | Store blobs in a dedicated database | `true` |
| `file` | Save blobs to a folder organised by date | `false` |
| `compress` | Apply compression | `false` |

Example:
```anylog
run blobs archiver where dbms = true and file = true and compress = false
```

Monitor:
```anylog
get blobs archiver
```

### Archive and Cleanup

The Operator service can be configured to archive processed JSON and SQL files (see the `archive_json` and `archive_sql` 
options under Background Services — Operator).

Delete archived files older than N days:
```anylog
delete archive where days = 60
```

### Backup a Partition to a File

```anylog
backup table where dbms = my_data and table = ping_sensor and partition = [partition-name] and dest = [path]
```

## Testing the Cluster & Locating Data

A special group of commands allows you to monitor the configuration of the nodes supporting each cluster and the 
cluster state.

### Testing the Node Configuration for HA

The `test cluster setup` command details if the node is properly configured to support HA.

Usage:
```anylog
test cluster setup
```

The command returns the HA configuration and relevant status. The info includes the following:

| Functionality | Expected Status | Details |
|---|---|---|
| Operator | Running: distributor flag enabled | Configure Operator in the `run operator` command with option `distributor = true`. |
| Distributor | Running | |
| Consumer | Running | |
| Operator Name | Valid name | The Operator name from the Operator policy. |
| Member ID | Valid ID | The member ID from the Operator policy. |
| Cluster ID | Valid Cluster ID | The cluster ID assigned by the Operator in the `run operator` command. |
| almgm.tsd_info | Defined | A tsd_info table defined. If missing, it needs to be created (using the `create table` command). |

### View Data Distribution Policies

There are 2 commands that provide visualization of how data is distributed (from logical tables) to physical nodes in 
the network:
```anylog
blockchain query metadata

get data nodes
```

The `blockchain query metadata` command shows, for each logical table, the list of clusters and the physical nodes 
assigned to each cluster. The `get data nodes` command provides the same info, but in a table format.

### Test Cluster Policies

The command below tests the validity of the cluster policies:
```anylog
blockchain test cluster
```

### View the Distribution of Data to Clusters

The command `get data nodes` details the Operators that host each table's data.

**Usage**:
```anylog
get data nodes where company = [company name] and dbms = [dbms name] and table = [table name] and sort = (Columns IDs)
```

The where condition is optional. If company name, database name, or table name are not provided, the process assumes a 
request for all values.

Examples:
```anylog
get data nodes                          # operators hosting each supported table
get data nodes where table = ping_sensor  # operators hosting a particular table
get data nodes where sort = (1,2)         # ordered by DBMS (col 1), then Table (col 2)
```

### View the Distribution of Data to an Operator

Executing the command `get cluster info` on an Operator node presents the cluster supported by the operator, the member 
Operators that are supporting the cluster, and the tables associated with the cluster.

```anylog
AL anylog-node > get cluster info
Cluster ID : 2436e8aeeee5f0b0d9a55aa8de396cc2
Member ID  : 206
Participating Operators:
      IP          
    Port Member Status 
      ---------------|----|------|------|
      139.162.126.241|2048|   206|active|
      139.12.224.186 |2048|   008|active|
Tables Supported:
      Company       DBMS          Table                
      -------------|-------------|--------------------|
      litsanleandro|litsanleandro|ping_sensor        |
      litsanleandro|litsanleandro|percentagecpu_sensor|
```

### Cluster Databases

Nodes assigned to the same cluster need to be in sync on the logical databases that store the data tables (note that 
the physical databases on each node can be different). The `test cluster databases` command provides a comparison list 
of all the databases defined on each node in the cluster.

Usage:
```anylog
test cluster databases
```

### Cluster Synchronization Status

The `test cluster data` command provides the synchronization status for each user table. The info returned presents, for 
each user table, the number of rows and the number of files processed on each node that supports the cluster.

Usage:
```anylog
test cluster data [options]
```

Options determine the information of interest, expressed as a where condition with key-value pairs:

| Key | Value |
|---|---|
| `start_date` | Retrieve entries with a date greater or equal to the start_date. |
| `end_date` | Retrieve entries with a date earlier than the end_date. |

Examples:
```anylog
test cluster data
test cluster data where start_date = -7d
```

Example output:
```anylog
Table                Node_128        Node_222
                     10.0.0.78:7848  10.0.0.78:3048
--------------------|---------------|---------------|
lsl_demo.ping_sensor|1034/21778        |1034/21     |
```
In the example above, 2 operators are supporting the cluster. The cluster table `ping_sensor` (in DBMS `lsl_demo`) was 
updated by 1034 files and a total of 21778 rows.

### HA Related Commands

The following list summarizes the commands supporting the HA processes:

| Command | Details |
|---|---|
| `get data nodes` | The list of user tables and the physical nodes that manage each table |
| `get metadata version` | The ID representing the metadata version used on the node |
| `blockchain query metadata` | Similar to `get data nodes`, with a different output format |
| `blockchain test cluster` | Validates that the structure of the cluster policies is correct |
| `get tsd list` | The list of tsd tables on the current node |
| `get tsd details` | Query one or more TSD tables |
| `get tsd summary` | Summary info of TSD tables |
| `get tsd error` | Query TSD tables for entries indicating errors in the database update process |
| `get tsd sync status` | The sync status on the current node |
| `test cluster setup` | The configuration of the node to support HA |
| `test cluster data` | Compare the data status on all the nodes that support the same cluster |
| `test network metadata` | Returns metadata version on each participating node |


## TSD Tables & File Commands

A detailed document on TSD table logic can be found in the [previous section](03-%20High%20Availability.md#tsd--almgm-logical-database).

### TSD (Time Series Data) File Management Tables

Each ingested log file is represented as an entry in one TSD table. Log files with data from devices are represented in 
`tsd_info`, and files with log files from peers are represented in `tsd_id` (where ID is the peer member ID).

### Retrieve Details from TSD Tables

```anylog
get tsd details
get tsd details where table = *
get tsd details where table = tsd_123 and hash = 6c78d0b005a86933ba44573c09365ad5
get tsd details where table = tsd_info and hash = a00e6d4636b9fd8e1742d673275a75f7 and format = json
get tsd details where start_date = -3d and end_date = -2d
```

### Retrieve Summary Information from a TSD Table

```anylog
get tsd summary where [options]
```

| Key | Value | Default |
|---|---|---|
| `table` | The name of the table to use (or `*` for all tables) | `tsd_info` |
| `start_date` | Retrieve entries with a date greater or equal to the start_date | |
| `end_date` | Retrieve entries with a date earlier than the end_date | |

Examples:
```anylog
get tsd summary
get tsd summary where table = *
get tsd summary where start_date = -3d
```

### Retrieve the List of Files Not Ingested on the Local Node

```anylog
get tsd errors where [options]
```
Options are the same as `get tsd details` / `get tsd summary` above.

### Creating and Dropping TSD Tables

The `tsd_info` table is created using:
```anylog
create table tsd_info where dbms = almgm
```

Tables that represent members of the cluster are created dynamically.

Local TSD tables can be dropped using either:
```anylog
drop table [tsd table name] where dbms = almgm
```
or
```anylog
time file drop [table name]
```

Dropping all TSD tables:
```anylog
time file drop all
```

Examples:
```anylog
drop table tsd_info where dbms = almgm
time file drop tsd_123
time file drop all
```

### Deleting a Single TSD Row

Usage:
```anylog
time file delete [row id] from [tsd table name]
```

Examples:
```anylog
time file delete 16 from tsd_info
time file delete 126 from tsd_129
```

### Node Synchronization Status (TSD)

When multiple nodes support the same cluster, they sync their TSD info. The `get tsd sync status` command provides the 
synchronization status. If a table is not specified, all TSD tables are considered.

Usage:
```anylog
get tsd sync status where table = [tsd table name]
```

Examples:
```anylog
get tsd sync status
get tsd sync status where table = tsd_128
```