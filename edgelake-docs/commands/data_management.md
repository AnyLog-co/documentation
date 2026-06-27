---
layout: default
parent: Commands
title: Data Management
nav_order: 2
---
# Data Management Commands

The data management commands organize the node's local databases and provide the functionalities to monitor the state of the
data during ingestion, storage and query.

**Note**:
* Logical databases are declared by users.
* Users associate logical databases to physical databases (like SQLite or PostgreSQL).
* Tables are declared dynamically and transparently based on the data ingestion.
* When a table is created, it would be assigned to a default logical database. Or users can configure data streams to logical databases.

## Associate a physical database to a logical database
The <code class="language-anylog">connect dbms</code> command associates a physical database to a logical database. This 
process is per node, to determine, when a data table is created, the physical database to host the table's data.  
Note: The same logical database (and the database tables), can be hosted on different nodes by a different physical database.

### Connect DBMS
**Usage**:
<pre class="code-frame"><code class="language-anylog">&lt;connect dbms [db name] where 
  type = [db type] and 
  user = [db user] and 
  password = [db passwd] and 
  ip = [db ip] and 
  port = [db port] and 
  memory = [true/false]&gt;
</code></pre>

**Explanation**: Associate a physical database to a logical database.

**Examples**:
<pre class="code-frame"><code class="language-anylog">connect dbms test where type = sqlite
connect dbms sensor_data where type = psql and user = anylog and password = demo and ip = 127.0.0.1 and port = 5432
</code></pre>

**Details**: [Connect to a local DBMS](https://github.com/AnyLog-co/documentation/blob/master/sql%20setup.md#connecting-to-a-local-database).

### Get associations between logical and physical databases

**Usage**:
<pre class="code-frame"><code class="language-anylog">get databases</code></pre>

**Explanation**: Get the list of connected databases on this node.

**Examples**:
<pre class="code-frame"><code class="language-anylog">get databases</code></pre>

### Get the list of tables on the node
**Usage**:
<pre class="code-frame"><code class="language-anylog">get tables where dbms = [dbms name] and format = [format type]</code></pre>

**Explanation**:
* Get the list of tables for the named dbms or all databases (if named dbms is asterisk). Each table is flagged if declared on the shared metadata (blockchain or master) 
  and if declared locally (on the local physical database).  
* <code class="language-anylog">[format type]</code> is optional to determine the output format (*table* or *json* and *table* being the default).

**Examples**:
<pre class="code-frame"><code class="language-anylog">get tables where dbms = dmci
get tables where dbms = *
get tables where dbms = aiops and format = json
</code></pre>

**Details**: [Get Tables Command](https://github.com/AnyLog-co/documentation/blob/master/sql%20setup.md#the-get-tables-command).

### Drop a table on the local node

**Usage**:
<pre class="code-frame"><code class="language-anylog">drop table [table name] where dbms = [dbms name]</code></pre>

**Explanation**: Drop a table in the named database. If the table is partitioned, all partitions are dropped.

**Examples**:
<pre class="code-frame"><code class="language-anylog">drop table my_table where dbms = my_dbms</code></pre>


## Partition Data

### Partition table's data by time
**Usage**:
<pre class="code-frame"><code class="language-anylog">partition [dbms name] [table name] using [column name] by [time interval]</code></pre>

**Explanation**: 
* Partition a table or a group of tables by time interval
* Time intervals options are: year, month, week, days in a month

**Examples**:
<pre class="code-frame"><code class="language-anylog">partition lsl_demo ping_sensor using timestamp by 2 days
partition lsl_demo ping_sensor using timestamp by month
partition lsl_demo * using timestamp by month</code></pre>

**Details**: [Data Partitioning](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#partition-command).

### Get partition information
**Usage**:
<pre class="code-frame"><code class="language-anylog">get partitions [info string]</code></pre>

**Explanation**: Get partitions declarations for all tables or a designated table or the recently dropped partitions.

**Examples**:
<pre class="code-frame"><code class="language-anylog">get partitions
get partitioned dropped
get partitions where dbms = lsl_demo and table = ping_sensor
</code></pre>

**Details**: [Partition Status](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#partitions-status-and-configurations).

### Drop Partition

<pre class="code-frame"><code class="language-anylog">drop partition [partition name] where dbms = [dbms name] and table = [table name] and keep = [value]</code></pre>

**Explanation**: Drops a partition in the named database and table.
* <code class="language-anylog">[partition name]</code> is optional. If partition name is omitted, the oldest partition of the table is dropped.
* <code class="language-anylog">keep = [value]</code> is optional. If a value is provided, the oldest partitions will be dropped to keep the number of partitions 
  as the value provided.If the table has only one partition, an error value is returned.
* If table name is asterisk (*), a partition from every table from the specified database is dropped.
* If partition name is asterisk (*), all the partitions are dropped.

**Examples**:
<pre class="code-frame"><code class="language-anylog">drop partition par_readings_2019_08_02_d07_timestamp where dbms = purpleair and table = readings
drop partition where dbms = purpleair and table = readings
drop partition where dbms = aiops and table = cx_482f2efic11_fb_factualvalue and keep = 5
drop partition where dbms = aiops and table = * and keep = 30
</code></pre>

**Details**: [Drop Partition](https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#drop-partition-command)
