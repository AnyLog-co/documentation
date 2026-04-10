# Using Helpers

Helpers are independent processes configured to perform background tasks such as data ingestion, or other compute-bound 
operations in a single node.

These helpers are detached from the main node loop and can operate in parallel, increasing throughput and responsiveness for long-running tasks.

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

## Reset helpers stats:

The following command resets the helpers info:
```anylog
reset dynamic stats
```

## 🧭 Retrieve the list of active helpers

The `get helpers` command provides a list of currently active helper processes running under the current AnyLog node. 
It returns the types of helpers and how many instances of each are active.

**Example:**
```anylog
get helpers
```

## 🤝 Interacting with a Helper via the Main Process

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

## Terminating the helper process
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


# 📊 Dynamic monitoring of internal processes

The `get dynamic stats` command retrieves **live execution metadata** about a specific operation running in the main or helper processes
— such as timing, status, or active resource usage — by referencing its associated request or file name.


**Usage:**
```anylog
get dynamic stats where name = [monitored topic]
```

**Monitored Topics:**

| Topic Key     | Helper Type | Description                                           |
|---------------|-------------|-------------------------------------------------------|
| operator.json | psql        | The JSON processing time                              |
| operator.sql  | psql        | The SQL processing time                               |
| operator.jql  | psql        | The SQL processing time directly from JSON conversion |


**Examples:**
```anylog
helper psql 1 get dynamic stats where name = operator.json
helper psql 1 get dynamic stats where name = operator.sql
```

The following example queries the time difference between first and last row:
```anglog
run client () sql lsl_demo format = table "select max(insert_timestamp) as max, min(insert_timestamp)::timediff(max) as diff from ping_sensor"
```



