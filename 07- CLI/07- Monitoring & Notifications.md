---
title: "Scheduler & Notifications"
description: "Node monitoring commands, the scheduler for time-based and situational tasks, and sending notifications via REST/webhooks."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**   | **Version** |
 |------------|-------------|--------------|----------|
 | 2026-07-26 | Ori Shadmon | initial file |          |
--->

# Scheduler & Notifications

One of the features AnyLog provides is node monitoring through a schedule or rules engine logic.

* [Node Monitoring](#node-monitoring)
* [Scheduler](#scheduler)
* [Notification](#notification)

## Node Monitoring

The following provides commands for getting insight about the node. Please review [Southbound Monitoring](../04-%20Southbound%20Interfaces/05-%20Monitoring)
for further details on node, docker and syslog monitoring.

* `get stats where service = [type] and topic = [type]` - provide statistics on a service enabled on the node (e.g. `operator`, `publisher`).

```anylog
get stats where service = operator and topic = inserts
get stats where service = publisher and topic = files
get stats where service = operator and topic = summary and format = json
get stats where service = publisher and topic = summary and format = json
```

**Example output**:
```
AL > get stats where service = operator

Stats: OPERATOR SUMMARY
Node name                                Status Operational time Processing time Elapsed time New rows Total rows New errors Total errors Avg. rows/sec
----------------------------------------|------|----------------|---------------|------------|--------|----------|----------|------------|-------------|
power-plant-operator1@172.105.6.90:32148|Active|176:56:09       |176:56:09      |00:00:28    |      62|   473,798|         0|           1|         0.74|
```

`get disk [usage/free/total/used/percentage] [path]` - get information on the status of the disk addressed by the path. A path is required; omitting it returns an error.

```anylog
AL > get disk percentage .
14.93
```

* `get node info [function monitored] [attribute name]` - get monitored information on the current node (`cpu_percent`, `cpu_times`, `cpu_times_percent`, `getloadavg`, `swap_memory`, `disk_io_counters`, `net_io_counters`).

```anylog
AL > get node info cpu_percent
8.6

AL > get node info net_io_counters bytes_recv
33476307972
```

## Scheduler

The `schedule` or _rules engine_ logic acts as a scheduling tool to execute a process based on a time interval and/or when a certain
situation occurs.

**Example**
* **Time-based**: clean partitions older than 35 days every 30 days.
* **Situational**: Send a notification to IT / admin when free disk space drops below 20%.

A situational scheduled process is based on a time-based scheduled process, where a primary script runs every X amount
of time, and if the situation (e.g. free disk space below 20%) occurs, then send a notification.

### Example: node health monitoring schedule

The following set of scheduled tasks polls CPU, network packet counts, and network errors every 30 seconds, and pushes
the results into a shared `node_insight` dictionary object that gets sent to an aggregator node via `monitor operators`
(see [Aggregator node](./03-%20Get%20&%20Set.md#aggregator-node)):

```anylog
schedule name = get_cpu_percent and time = 30 seconds task cpu_percent = get node info cpu_percent
schedule name = get_packets_recv and time = 30 seconds task packets_recv = get node info net_io_counters packets_recv
schedule name = get_packets_sent and time = 30 seconds task packets_sent = get node info net_io_counters packets_sent
schedule name = disk_space   and time = 30 seconds task if !disk_space   then node_insight[Free Space Percent] = !disk_space.float
schedule name = cpu_percent  and time = 30 seconds task if !cpu_percent  then node_insight[CPU Percent] = !cpu_percent.float
schedule name = packets_recv and time = 30 seconds task if !packets_recv then node_insight[Packets Recv] = !packets_recv.int
schedule name = packets_sent and time = 30 seconds task if !packets_sent then node_insight[Packets Sent] = !packets_sent.int
schedule name = errin and time = 30 seconds task errin = get node info net_io_counters errin
schedule name = errout and time = 30 seconds task errout = get node info net_io_counters errout
schedule name = get_error_count and time = 30 seconds task if !errin and !errout then error_count = python int(!errin) + int(!errout)
schedule name = error_count and time = 30 seconds task if !error_count then node_insight[Network Error] = !error_count.int
schedule name = local_monitor_node and time = 30 seconds task monitor operators where info = !node_insight
```

### Schedule commands

* `run scheduler` - initiate a scheduler group (default is 0, and 1 is automatically initiated with default start up)

```anylog
AL > run scheduler
```

* `get scheduler [n]` - information on the scheduled tasks. `[n]` is an optional ID for the scheduler; scheduler 1 manages user-scheduled tasks, 0 is the system scheduler.

```anylog
AL > get scheduler

Scheduler ID:     0
Scheduler Status: Running
Scheduled Tasks
ID Mode   Name          Counter Run Status Start-Time                 Repeat-Time Task
--|------|-------------|-------|----------|--------------------------|-----------|----------------|
 1|Active|Metadata Ping|  10637|Success   |2026-07-19 19:34:26.436329|0:1:0      |set servers ping|

Scheduler ID:     1
Scheduler Status: Running
Scheduled Tasks
ID Mode   Name                         Counter Run Status                                                   Start-Time                 Repeat-Time Task
--|------|----------------------------|-------|------------------------------------------------------------|--------------------------|-----------|----------------------------------------------------------------------------------------------------|
 1|Active|Drop Partitions             |      8|Success                                                     |2026-07-19 19:34:31.714551|24:0:0     |drop partition where dbms = !default_dbms and table = !table_name and keep = !partition_keep        |
 2|Active|remove_archive              |      8|Success                                                     |2026-07-19 19:34:31.714915|24:0:0     |delete archive where days = !archive_delete                                                         |
 3|Active|Monitoring - Drop Partitions|     15|Success                                                     |2026-07-19 19:35:08.390648|12:0:0     |drop partition where dbms = monitoring and table = * and keep = 3                                   |
```

## Notification

AnyLog is able to send notifications via both REST and webhooks, meaning we can send to an array of services:
* [Telegram / Pushover](04-1%20Notification/02-%20REST.md#telegram--pushover)
* [Slack](04-1%20Notification/02-1%20Webhooks.md#slack-webhooks)
* [SMTP](04-1%20Notification/01-%20SMTP.md)
* [others](04-1%20Notification)
