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
1) The value for the key ***cluster*** is the Cluster ID that identifies the cluster policy.
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
The configuration example enable the HA processes.  
The policy ID associate the operator with the cluster. If multiple operators support the same cluster 
(their operator policy reference the same cluster ID), they will share the same data.   

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

The following command provides the list of tables supported by the Operator and the list of peer Operators that support the cluster:
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
Note: When an Operator policy is added, the policy is updated with a member ID. The member ID is unique among the cluster members.
  
The following ***time file*** commands allow to query the TSD tables:

* Use the ***time file summary*** command to find the total rows ingested within a time interval.
```anylog
time file summary where table = * and start_date = -10d
```

* Use the errors command to list the files that were not ingested within a time interval.
```anylog
time file errors where table = tsd_159 and start_date = -10d
```

Additional information on the time file commands is available at the [Time File Commands](managing%20data%20files%20status.md#time-file-commands) section.  

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


