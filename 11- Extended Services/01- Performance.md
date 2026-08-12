---
title: "Performance"
description: "AnyLog insertion performance"
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-08-11 | Ori Shadmon    | define performance document based on https://github.com/AnyLog-co/documentation/blob/2026.08.07-bkup/helpers.md | |
---> 

---
title: "Performance"
description: "AnyLog insertion performance"
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change**         | **Version** |
 |------------|----------------|------------------|----------|
 | 2026-08-11 | Ori Shadmon    | define performance document based on https://github.com/AnyLog-co/documentation/blob/2026.08.07-bkup/helpers.md | |
---> 

# Performance

Data insertion is a critical component of AnyLog as sensors can publish large amounts of data at a very fast rate. 

As such performance is composed of 4 critical things: 

1. [Streaming Buffers](#streaming-buffers)
2. [Parallelization](#parallelization)
3. [PSQL Configs](#psql-configs)
4. [Aggregation](../09-%20Data%20Management/02-2%20Data%20Aggregations.md)

For query performance visit - [Query Profiling](../09-%20Data%20Management/06-%20Query%20Profiling.md)

# Streaming Buffers

Data provided via REST APIs and message brokers passes to processing through internal buffers. The buffers are 
associated with database tables and the get streaming command provides information on the data that passes through 
these buffers.

When configuring a node there are 2 threading processes that increase performance time between data being accepted in 
JSON file format and actually stored in operator. 

As data flows in, it's initially stored in a buffer and only once the buffer is full does this content actually get 
published into the JSON file (under `!watch_dir` directory).

The command, [`set buffer threshold`](../07-%20CLI/02-1%20Nodes.md#data-buffering) configures time and volume thresholds 
for buffered streaming data. The condition can be just a buffer threshold size (in terms of time and/or volume), or 
scoped to a specific database (and table).

```anylog
<set buffer threshold where
    dbms = al_demo and
    table = ping_sensor and
    time = 2 minutes and volume = 1MB>
```

Additionally, when running [`run operator`](../07-%20CLI/02-1%20Nodes.md#run-operator-command), which is the service 
that actually stores JSON (files) into the logical database, the parameter `threads` specifies how many threads are used 
to read content from `!watch_dir/` into logical database storage. 

Finally, the command `get streaming` provides statistics on the streaming processes, while `get streaming config` 
provides information regarding the buffer configurations. 

> Buffer size can be updated while an operator is already running. 

# Parallelization

In general, interaction with the CLI occurs on the main thread, while other active services (`get processes`) run on 
their respective thread(s). In order to increase performance the configurations should enable larger number of 
parallelization for process such as writing to logical database. 

`helpers` are independent processes configured to perform background tasks such as data ingestion, or other 
compute-bound operations in a single node.

These _helpers_ are detached from the main node loop and can operate in parallel, increasing throughput and responsiveness 
for long-running tasks. 

**Usage:**
```anylog
run helpers where type = [helper type] and count = [helpers count]
```

**Parameters:**

| Parameter       | Description                                                                  |
|-----------------|------------------------------------------------------------------------------|
| type            | Helper type (e.g., psql). Defines what kind of task the helper will process. |
| count           | Number of helper processes to launch. Each runs independently in parallel.   |


**Example:**
```anylog
run helpers where type = psql and count = 2
```

### Reset helpers stats

The following command resets the helpers info:
```anylog
reset dynamic stats
```

### Retrieve the list of active helpers

The `get helpers` command provides a list of currently active helper processes running under the current AnyLog node. 
It returns the types of helpers and how many instances of each are active.

**Example:**
```anylog
get helpers
```

### Interacting with a Helper via the Main Process

Once helper processes are launched (using `run helpers`), you can **communicate with them directly** through the main
AnyLog CLI by prefixing any valid AnyLog command with:

```anylog
helper [helper_name] [helper_id] [anylog_command]
```

**Examples:**
```anylog
helper psql 1 get operator
helper psql 1 get error log
helper psql 1 get dynamic stats where name = operator.sql
helper psql 1 get dynamic stats where name = operator.json
```

### Terminating the helper process

The following command terminates the helper process:
```anylog
helper [helper type] [helper ID] exit node
```
The following command terminates all helpers:
```anylog
helper * * exit node
```
**Example:**
```anylog
helper psql 1 exit node
```


## Dynamic monitoring of internal processes

The `get dynamic stats` command retrieves **live execution metadata** about a specific operation running in the main or helper processes
— such as timing, status, or active resource usage — by referencing its associated request or file name.


**Usage:**
```anylog
get dynamic stats where name = [monitored topic]
```

**Monitored Topics:**

| Topic Key     | Helper Type | Description                                           |
|---------------|-------------|--------------------------------------------------------|
| operator.json | psql        | The JSON processing time                              |
| operator.sql  | psql        | The SQL processing time                               |
| operator.jql  | psql        | The SQL processing time directly from JSON conversion |


**Examples:**
```anylog
helper psql 1 get dynamic stats where name = operator.json
helper psql 1 get dynamic stats where name = operator.sql
```

# PSQL Configs

As discussed in the [database section](../09-%20Data%20Management/02-1%20Databases/01-%20SQL%20Storage.md), AnyLog 
supports multiple types of SQL-based physical databases. However, we do not recommend using the SQLite option for 
performance-dependent insertion as it's a single-file store with concurrency limitations. Instead it is recommended to 
use a server-based physical database like Postgres. 


However, even with Postgres, the default configuration can still be improved substantially. On a mid-size machine with configuration: 

| Parameter | Value | 
| :---: | :---: | 
| Operating System |  Ubuntu 22.04 LTS |
| CPU | Intel Broadwell i9 | 
| Physical Cores | 8 |
| Logical Cores |  16 |
| RAM | 64 GB |
| Disk | 150GB  (SSD) | 

```yaml
# Memory Settings
shared_buffers = 16GB        # Set to 25% of system RAM (optimal between 25-40%)
work_mem = 256MB             # Increase for larger operations, especially with many concurrent queries
maintenance_work_mem = 4GB   # Increase for VACUUM, index builds, etc.

# WAL Settings
wal_level = minimal           # Keep at minimal if replication is not required
synchronous_commit = off      # For performance, at the risk of data loss in a crash
wal_buffers = 64MB            # Increase to handle large transactions
commit_delay = 1000           # Delay (microseconds) to batch commits for better performance

# Checkpoint Settings
checkpoint_completion_target = 0.9  # Spread checkpoint load evenly
max_wal_size = 4GB            # Increase WAL size to delay checkpoints
checkpoint_timeout = 15min    # Keep frequent enough to avoid large spikes

# Autovacuum Settings
autovacuum = off              # Disable during bulk inserts; re-enable afterward

# Performance and Data Safety
fsync = off                   # Disable for bulk inserts (use with caution)
full_page_writes = off        # Disable for performance; use with caution

# Parallelism Settings
max_parallel_workers_per_gather = 8  # Increase based on your 16 logical cores
max_worker_processes = 16            # Match to your logical cores
max_parallel_workers = 16            # Match to your logical cores
```

> Disk and Indexing: Remember to drop indexes before bulk inserts and recreate afterward for better performance


## Sample Results 

With the machine above, and the provided Postgres configurations, we configured AnyLog as follows: 

1. Connected to logical database with `UNLOG` set to **True** - changes are applied directly to the table without going 
   into the WAL (equivalent to Postgres `UNLOGGED` tables).
2. Defined `run operator` with `OPERATOR_THREADS` set to 10 
3. Defined `set buffer threshold` with the following params: 
   * `WRITE_IMMEDIATE` set to **False** 
   * `THRESHOLD_TIME` set to **5 seconds** 
   * `THRESHOLD_VOLUME` set to **1KB**

With these params and an insertion of 1 million rows batch size, we saw a performance of nearly 50k rows per second. 

As you increase the machine and thread size, performance should improve.