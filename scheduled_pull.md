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
run scheduled pull 
where type = [data_type] 
  and source = [IP or hostname] 
  and frequency = [seconds] 
  and continuous = [true/false]
```

Parameters

| Parameter | Default | Description                                                          |
|-----------|---------|----------------------------------------------------------------------| 
| type      |         | The type of data to pull (e.g., syslog)                              |
| source    |         | The network identifier of the data source (localhost or a remote IP) |
| frequency |         | Interval in seconds between pulls (e.g., 5)                          |
| continuous | False  | If true, pulls continuously as long as data is available, ignoring frequency  |

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
run scheduled pull where type = eventlog and source = localhost and frequency = 1
```


