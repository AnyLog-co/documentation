# Scheduled Pull

## Overview

The **scheduled pull** command in AnyLog is used to periodically retrieve data from an external source — such as logs, 
metrics, or device readings — and insert it into a local database table or distribute it to other AnyLog nodes.

This mechanism is particularly useful for environments like **Windows**, where data cannot be pushed natively via syslog. 
In such cases, AnyLog uses a **scheduled pull** to fetch data directly (e.g., from the Windows Event Log).

## Command: `run scheduled pull`

This command pulls data from a specified source node on a scheduled basis.

### 📌 Usage:
```anylog
run scheduled pull where type = [data_type] and source = [IP or hostname] and frequency = [seconds] and continuous = [true/false] and dbms = [dbms name] and table = [table name] and stdout = [true/false]
```

Parameters

| Parameter | Default | Description                                                                                                    |
|-----------|---------|----------------------------------------------------------------------------------------------------------------|
| type      |         | The type of data to pull (e.g., `syslog`, `eventlog`, `modbus`)                                                |
| source    |         | The network identifier of the data source (`localhost` or a remote IP)                                         |
| frequency |         | Interval in seconds between pulls (e.g., `5`)                                                                  |
| continuous | False   | If `true`, pulls continuously as long as data is available, ignoring frequency                                 |
| dbms      |         | The name of the target DBMS instance where the data will be inserted                                           |
| table     |         | The name of the target table within the DBMS                                                                   |
| stdout   | False   | If `true`, a single read result will be printed to the console (stdout) instead of being inserted into a table |

Notes:  
* Use `stdout = true` when you want to test the pull behavior or inspect the output without writing to a database.
* When `stdout = true`, only **one** data read is performed and the result is printed to the terminal or log. The pull does **not continue** even if `continuous = true`.

## Associating the pulled data with a topic

In the context of a scheduled pull, the topic = (...) clause maps the data retrieved by the pull process 
into a topic that is associated with mapping instructions.

Example:

```anylog
<run scheduled pull where 
  type = eventlog 
  and source = localhost 
  and frequency = 1 
  and topic = (
    name = eventlog 
    and dbms = my_dbms 
    and table = my_table  
    and column.timestamp.timestamp = "bring [timestamp]" 
    and column.value.int = "bring [message]"
  )>
```

Using a **topic** is optional. Details of the **topic** params are available [here](message%20broker.md#the-topic-params).

## Scheduled pull of Windows Event Log

Unlike Linux or Unix-based systems, Windows does not use the syslog protocol to manage logs.    
Instead, it uses a proprietary system called the Windows Event Log, which stores structured event records internally 
and does not natively support sending logs over the network in real-time.

Details on servicing Syslog data to AnyLog in a Unix system is available at [Using Syslog](using%20syslog.md) document.  

As a result, log data on Windows must be accessed via APIs, such as the Windows Event Log API, rather than being 
pushed out like syslog messages.

Using the **run scheduled pull** command, users can pull the Windows event log from local or remote Windows machine.

Usage:
```anylog
run scheduled pull where type = eventlog and source = localhost and frequency = 1 and dbms = sensor_data and table = event_log
```

### Filtering by Event Type

For Windows even log, users can optionally filter events by their **type** using the `event_type` parameter.

### Supported Values for `event_type`

You may specify one or more of the following event types using lowercase and underscores instead of spaces:

| Value             | Description                          |
|------------------|--------------------------------------|
| `error`           | Logs that indicate significant problems or failures |
| `warning`         | Logs that indicate potential issues or conditions to watch |
| `information`     | Logs that record normal operations and successful activity |
| `audit_success`   | Security-related logs for successful operations (e.g., login success) |
| `audit_failure`   | Security-related logs for failed operations (e.g., login failure) |
| `all`             | No filtering; pulls all available event types |

### 🔧 Usage Examples

#### Pull only error logs:

```anylog
<run scheduled pull 
where type = eventlog 
  and source = localhost 
  and frequency = 5
  and continuous = false 
  and event_type = error
  dbms = sensor_data
  and table = event_log>
```

