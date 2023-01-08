# High Availability (HA)

AnyLog can be configured such that data is highly available. The HA process is such that multiple Operators maintain the 
same data such that if an Operator fails, the data is available on a surviving Operator and queries are directed to the 
surviving node. This document explains how to configure AnyLog to provide High Availability, and details the commands that 
monitor and report on the HA state.

This document extends the explanations in [Data Distribution and Configuration](data%20distribution%20and%20configuration.md#data-distribution-and-configuration).

## Overview

High Availability (HA) is enabled by configuring the network nodes to maintain multiple copies of the data.  
In HA setup, multiple nodes are grouped together and assigned to maintain copies of the data such that if a node fails, 
the data is available from a surviving peer node.    
To be in a state where multiple nodes have identical set of data, each participating Operator node is configured with 
push and pull processes, that operate on the data, such that, when data is added to one of the nodes, it will be replicated the  
assigned peer nodes.
This setup requires the following:
1) Associating multiple Operator nodes to the same cluster such that these nodes have identical copies of the data.  
2) Enabling the following background processes on each node:
   1) The Operator Background Process to ingest data to the local databases.
   2) The Distributor Background Process to push new data to the peer nodes that host a copy of the data.
   3) The  Consumer Background Process to pull data which is missing on the current node.
3) Enabling the TSD tables operations.

## Testing the node configuration for HA
The **test ha setup** command details if the node is properly configured to support HA.  
Usage:
<pre> 
test ha setup
</pre>
The command returns the HA configuration and relevant status. The info includes the following:

| Functionality | Expected Status                    | Details       |
| --------------| ---------------------------------- | --------------- | 
| Operator      | Running: distributor flag enabled  | Configure Operator in the **run operator** command with command option **distributor = true**.  |
| Distributor   | Running                            |                |
| Consumer      | Running                            |                |
| Operator Name | Valid name                         | The Operator name from the Operator policy.     |
| Member ID     | Valid ID                           | The member ID from the Operator policy.     |
| Cluster ID    | Valid Cluster ID                   | The cluster ID assigned by the Operator in the **run operator** command.     |
| almgm.tsd_info | Defined                           | A tsd_info table defined. If missing, it needs to be created (using **create table** command).                |


## HA related commands
The following list summarizes the commands supporting the HA processes:
 
| command           | Details | 
| ----------------- | ----------------| 
| get data nodes    | The list of user tables and the physical nodes that manage each table |
| blockchain query metadata   | Similar to the "get data nodes" command, with a different output format |
| get tsd list   | The list of tsd tables on the current node |
| get tsd details  | Query one or more TSD tables  |
| get tsd summary  | Summary info of TSD tables  |
| get tsd error  | Query TSD tables for entries indicating errors in the database update process  |
| get tsd sync status  | The sync status on the current node  |
| test ha setup  | The configuration of the node to support HA  |
| test ha cluster  | Compare the data status on all the nodes that support the same cluster  |


## The Cluster Policy

HA is based on distributing the data to clusters. A cluster is a logical collection of data and each cluster is supported by
one or more operators. Operators are assigned to clusters (each operator can be assigned to only one cluster), and the number of
operators assigned to each cluster determine the number of copies of the data hosted by the cluster (all the operators assigned to a cluster maintain the same data).  

Below is an example of a policy declaring a cluster:

```json
{"cluster": {
  "company": "Lit San Leandro",
  "name": "lsl-cluster2",
  "status": "active"
}}
```
WHen the cluster policy is added to the metadata, it will be added with additional attributes as follows:
```json
{"cluster" : {
   "company": "Lit San Leandro",
   "name": "lsl-cluster2",
   "status": "active",
   "id" : "7a00b26006a6ab7b8af4c400a5c47f2a",
   "date" : "2022-12-23T01:48:33.794562Z",
   "ledger" : "global"}}
```


Notes: 
1) A cluster is a logical definition, the actual storage is on the operator nodes that are associated with the cluster (and all the operators assigned to a cluster maintain the same data).
2) A policy ID and Date attributes of the policy are added by the network protocol.
3) The policy ID uniquely identifies the cluster.

## The Operator Policy

An Operator is assigned to a cluster in the following manner:

```anylog
{'operator' : {'cluster' : '7a00b26006a6ab7b8af4c400a5c47f2a',
                'ip' : '24.23.250.144',
                'local_ip' : '10.0.0.78',
                'port' : 7848,
                'id' : '52612f21b18cf29f7d2e511e3ca56ca6',
                'date' : '2021-04-02T21:43:20.129597Z',
                'member' : 145}}]
```

Note: 
1) The value for the key ***cluster*** is the Cluster ID that identifies the cluster policy (the ID of the cluster policy).
2) All the data provided to the cluster will be hosted by the operator (as well as by all other operators that are associated with the cluster).

## Configuring an Operator Node

The example below enables 3 processes on an Operator node. By enabling these processes on all Operators, the data  
will be synchronized among the Operators such that the local databases on each Operator maintain a complete data set 
and all the Operators supporting the cluster maintain identical data.

| Command        | Functionality  | 
| ---------- | -------| 
| [run operator](background%20processes.md#operator-process) | Enables the process that ingests data to the local databases. |
| [run data distributor](background%20processes.md#invoking-the-data-distributor-process) | Distributes data received from external sources, like sensors, to the operators that support the cluster. |
| [run data consumer](background%20processes.md#invoking-the-data-consumer-process) | Enables the process that retrieves data which is missing on the Operator Node from the peer operators that support the cluster. |

Example:

```anylog
run operator where policy = 52612f21b18cf29f7d2e511e3ca56ca6 and create_table = true and update_tsd_info = true and archive = true and distributor = true and master_node = !master_node
run data distributor
run data consumer where start_date = -30d 
```
Note:  
With the configuration above, each operator that receives data will share the data with all peer operators and each operator will constantly and continuously
synchronize its locally hosted data with the peer operators that support the cluster.

## View the distribution of data to clusters

The command ***get data nodes*** details the Operators that host each table's data.  
Usage:
```anylog
get data nodes where company = [company name] and dbms = [dbms name] and table = [table name]  
```

The where condition is optional. If company name or database name or table name are not provided, the process assumes a 
request for all values.

The following example lists the operators that host the data of each supported table:
```anylog
get data nodes
```
Note: More details are available [here](data%20distribution%20and%20configuration.md#view-data-distribution-policies).

## View the distribution of data to an operator

The following command provides 2 lists:
1) The list of peer Operators that support the cluster.
1) The list of tables supported by the Operator.
```anylog
get cluster info
```

## The Time Series Data (TSD) Management Tables

As multiple Operators support each cluster and as each operator can receive data from different sources, the operators sync the data they receive
such that all operators supporting the same cluster host identical set of data.  
The synchronization is supported by push and pull processes:  
The push is done when an Operator receives data from a data source, the data is pushed by the Operator to the peer members of the cluster.
The pull is done by each member when the member determines that data available on peer nodes is missing.  
The state of the data on each node is recorded on a set of tables called TSD tables in the following manner:  
* Data received from a data source is registered in a table called TSD_INFO.
* Data received from a different member of the cluster is registered in a table called TSD_ID whereas ID is the Member ID.
Note: When an Operator policy is added, the policy is updated with an attribute called member and a value representing an ID. The member ID is unique among the cluster members.
  
The TSD tables can be queried (as detailed below) to control and monitor the data state on each participating node.

### The TSD tables on each node

Nodes synchronize their data using a set of tables called TSD tables. The current node is represented by tsd_info and
peers that support the same cluster are represented by a tsd suffixed with their member ID.
The following command returns the list of TSD tables on this node:  

```anylog
get tsd list
```

## Retrieve information from TSD tables
The following command retrieves information from a TSD table. The information includes the details of each file ingested to the local database.
```anylog 
get tsd [info type] [options]
```
* **Info type** is one of the following keywords:
   * details - the last entries in the requested TSD tables (note: by default, the list has a limit of the last 1-- entries of each table).
   * summary - a summary view of the info in the requested TSD tables.
   * errors - entries in TSD tables that represent sync processes that failed.

* Options determine the information of interest, expressed as a where condition with key-value pairs and is summarized below. 
 
| Key        | Value  | Default | 
| ---------- | -------| -------| 
| limit    | Setting a limit on the number of rows retrieved from the table, 0 value sets no limit. | 100 |
| table    | The name of the table to use. If **table=*** is specified, all the TSD tables are considered. Otherwise only **tsd_info** is considered. | tsd_info |
| hash    | Retrieve a key with the specified hash value. | |
| start_date | Retrieve entries with a date greater or equal to the start_date. | |
| end_date | Retrieve entries with a date earlier than the end_date. | |
| format | Output format - **table** or **json**  | table |


### Retrieve details from TSD tables
Each ingested log file is represented as an entry in one TSD table.    
Log files with data from devices are represented in tsd_info and files with log files from peers are represented in tsd_id whereas ID is the peer member ID.       
  
**Examples**:  
```anylog 
get tsd details
get tsd details where table = *
get tsd details where table = tsd_123 and hash = 6c78d0b005a86933ba44573c09365ad5
get tsd details where table = tsd_info and hash = a00e6d4636b9fd8e1742d673275a75f7 and format = json
get tsd details where start_date = -3d and end_date = -2d
```

### Retrieve summary information from a TSD table
The following command retrieves summary information from a TSD table.  
The summary information allows to validate that the different nodes supporting the same cluster maintain the same data.

```anylog 
get tsd summary where [options]
```
Options are optional and determine the information of interest, expressed as a where condition with key-value pairs and is summarized below. 
 
| Key        | Value  | Default | 
| ---------- | -------| -------| 
| table    | The name of the table to use (or asterisk (*) for all tables). | tsd_info |
| start_date | retrieve entries with a date greater or equal to the start_date. | |
| end_date | retrieve entries with a date earlier than the end_date. | |

**Note**: Setting a star sign (*) for a table name provides information from all the TSD tables hosted on the node.  
**Examples**:  
```anylog 
get tsd summary
get tsd summary where table = *
get tsd summary where start_date = -3d
```

An example of the output is the following:
```anylog
DBMS          Table       Start Date          From ID End Date            To ID Files Count Source Count Status 1 Status 2 Total Rows
-------------|-----------|-------------------|-------|-------------------|-----|-----------|------------|--------|--------|----------|
litsanleandro|heat_sensor|2021-04-02 02:47:56|      1|2021-04-02 17:50:01|   50|         50|           1|       1|       1|   453,455|
litsanleandro|ping_sensor|2021-04-02 02:47:56|      1|2021-04-02 17:50:01|  378|        378|           1|       1|       1|    77,624|
```
The output provides the summary on each table as follows:
| Column name| explanation | 
| ---------- | -------|
| DBMS | The DBMS containing the ingested data |
| Table | The Table containing the ingested data |
| Start Date | The first date within the requested time range with data ingested |
| From ID | The first Row ID in the TSD table within the requested time range |
| End Date | The last date within the requested time range with data ingested |
| To ID | The last Row ID in the TSD table within the requested time range |
| Files Count | The number of files ingested within the requested time range |
| Source Count | The number of sources (like sensors) providing data during the requested time range |
| Status 1 | The number of unique status-message updates in the "status 1" column. The value 1 indicates all status messages are the same |
| Status 2 | The number of unique status-message updates in the "status 2" column. The value 1 indicates all status messages are the same |
| Total Rows | The number of rows ingested in the requested time range |

### Retrieve the list of files which were not ingested on the local node
The following command retrieves the list of files that were identified as missing and the source node failed to deliver. 
```anylog 
get tsd errors where [options]
```
The options are the same as the options detailed [above](#retrieve-information-from-TSD-tables) command. 

## Creating and dropping the TSD tables
The _tsd_info_ table is created using the following command:
```anylog 
create table tsd_info where dbms = almgm
```
Tables that represent members of the cluster are created dynamically.  

Local TSD tables can be dropped using one of the following commands:
```anylog 
drop table [tsd table name] where dbms = almgm
```
or
```anylog 
time file drop [table name]
```
Dropping all TSD tables is by the following command:
```anylog 
time file drop all
```

**Examples**:  
```anylog 
drop table tsd_info where dbms = almgm
time file drop tsd_123
time file drop all
```

#### Deleting a single TSD row
Usage
```anylog 
time file delete [row id] from [tsd table name]
```

Examples:  
```anylog 
time file delete 16 from tsd_info
time file delete 126 from tsd_129
```

## Node synchronization status 
When multiple nodes support the same cluster, they sync their TSD info.  
The **get tsd sync status** provides the synchronization status. If a table is not specified, all tsd tables ate considered.  
Usage:
```anylog
get tsd sync status where table = [tsd table name]
```
Examples:
```anylog
get tsd sync statu
get tsd sync status where table = tsd_128
```

Additional information on the time file commands is available at the [Time File Commands](managing%20data%20files%20status.md#time-file-commands) section.

## Cluster synchronization status

The **test ha cluster** command provides the synchronization status for each user table.  
The info returned presents, for each user table, the number of rows and the number of files processed on each node that supports the cluster.  
Usage:
```anylog
test ha cluster [options]
```

Options determine the information of interest, expressed as a where condition with key-value pairs and is summarized below. 
 
| Key        | Value  | 
| ---------- | -------| 
| start_date | Retrieve entries with a date greater or equal to the start_date. |
| end_date | Retrieve entries with a date earlier than the end_date. |

Examples:
```anylog
test ha cluster
test ha cluster where start_date = -7d
```

Example output:
```anylog
Table                Node_128        Node_222
                     10.0.0.78:7848  10.0.0.78:3048
--------------------|---------------|---------------|
lsl_demo.ping_sensor|1034/21778        |1034/21     |

```
In the example above, 2 operators supporting the cluster. The cluster table ping_sensor (in DBMS) lsl_demo was update by
1034 files and a total of 21778 rows.

## The Archive of source data

When a data file is provided to an Operator, the file is ingested into the local database. The source file is compressed and 
archived in an archive directory such that, if needed, the source file can be used to complete a data set on an Operator node that 
requests the data.  
The location of the archive is configurable, and the root of the archive is addressed by ```archive_dir``` parameter.  
The following command displays the location:
```anylog
!archive_dir
```
The subdirectories of the archive partition the files by days using the following hierarchy: Year --> Month --> Day.  
Users can navigate in the hiereachy using the ***get directories*** and ***get files*** commands.  
The example below retrieves the list of files ingested on April 4th, 2021:
```anylog
get files !archive_dir/21/04/04
```
The [time file errors](#the-time-series-data--tsd--management-tables) command list the files which were not properly ingested 
and each listed file name includes the directory name where the file is archived as in the example below:  
A listed file name:
```anylog
/app/AnyLog-Network/data/archive/21/04/04/litsanleandro.ping_sensor.0.bd617b6ddb873750d9db561814297f23.0.120.119.210404201021.json
```
The archive directory is determined by the first 6 digits of the last field in the file name (the name segment before the file type 
representing the file ingestion date and time - 210404201021 in the example below).  
Details on file naming are available at the [file naming convention](managing%20data%20files%20status.md#the-file-naming-convention) section.

## Query execution

Queries are executed by dynamically and transparently identifying the clusters that host the relevant data, identifying an active Operator for each cluster 
and shipping the query to the identified Operators for execution. The query process assembles a unified and complete reply from
the participating data regardless of the Operator that participated in the query process. If an Operator fails to respond, the Operator is flagged as non-active and 
queries will not be shipped to the non-active Operator.

The following command provides information on the queries being executed, their status and the Operators that participate in the query process:
```anylog
query status
```
Additional information is available in [Command options for profiling and monitoring queries](profiling%20and%20monitoring%20queries.md#command-options-for-monitoring-queries).

## Adding Operator Nodes to a Cluster

Users can add to a cluster as many Operator Nodes as needed. This process can be done when an Operator node fails or
if it is needed to increase the number of copies of the data.  
Adding a node is by [configuring an AnyLog Instance](#configuring-an-operator-node) to be an Operator and adding
a [policy](#the-operator-policy) that associates the Operator to the cluster.       
The added Operator will automatically synchronize with the cluster peers to create on the newly added node a complete set of the cluster's data.


