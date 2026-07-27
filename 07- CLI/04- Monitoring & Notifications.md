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

The following provides commands for getting insight about the node. Please review [Southbound Monitoring](../04-%20Southbound%20Interfaces/04-%20Monitoring)
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

The `schedule` logic acts as a scheduling tool to execute a process based on a time interval and/or when a certain
situation occurs.

**Example**
* **Time-based**: clean partitions older than 35 days every 30 days.
* **Situational**: Send a notification to IT / admin when free disk space drops below 20%.

A situational scheduled process is based on a time-based scheduled process, where a primary script runs every X amount
of time, and if the situation (e.g. free disk space below 20%) occurs, then send a notification.

### Example: node health monitoring schedule

The following set of scheduled tasks polls CPU, network packet counts, and network errors every 30 seconds, and pushes
the results into a shared `node_insight` dictionary object that gets sent to an aggregator node via `monitor operators`
(see [Aggregator node](03-%20Get%20and%20Set%20Reference.md#aggregator-node)):

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
* Telegram / Pushover - shown in the example below
* Slack
* SMTP
* others

See [Notification Services]() for the general setup steps (webhooks, per-service URL
formats) referenced by the script below.

```anylog
#----------------------------------------------------------------------------------------------------------------------#
# Notifications regarding insight from the actual data tend to run via the Query node as it requires `system_query`
# request, scanning all relevant operator node(s).
#
# As such, it is recommended that the user **manually** defines configurations per table / notification system.
# the following example is "specifically" for smart city water (wp_digital) and waste water (wwp_digital) to check if
# the value changed from False -> True.
#
# Query configs and message configs are both defined per-script rather than in a shared/central config. This is because
# scripts run per-table (and thus potentially per database) via the Query node, and different (database and) tables may
# need to notify different destinations (e.g. a different chat_id, msg_url, or msg_type). Keeping both sets of params
# together in one script  per table keeps the query-to-notification mapping explicit and avoids needing conditional
# routing logic in a shared config.
#
#:steps:
#   1. copy existing script per table
#   2. update params
#   3. run as a scheduled process
#----------------------------------------------------------------------------------------------------------------------#
# process !local_scripts/smart-city/wp_digital_notification.al
# schedule name = [service name] and time = 15 minutes and task process !local_scripts/smart-city/wp_digital_notification.al

set debug on

on error ignore

:set-params:
# query configs
# target database (dbms) name to query, e.g. wp_digital or wwp_digital
alert_dbms = cos
# target table name within alert_dbms to check for sensor state
alert_table = wwp_digital
# value that triggers an alert when a column's value matches this (e.g. "true")
expected_value = false
# specify a column you want to use query
query_column = ""

# publish msg configs
# which notification backend to use: "telegram" or "pushover"
msg_type = telegram

# REST endpoint for the notification service (Telegram/Pushover API URL) -
# must match the endpoint for the selected msg_type above
msg_url = https://api.telegram.org/bot[API_TOKEN]/sendMessage
# Telegram chat ID to send the alert message to (telegram only)
chat_id = [CHAT_ID]
# Pushover application token (pushover only)
msg_token = ""
# Pushover user key (pushover only)
msg_user = ""


:query-data:
on error goto query-err
set query_result = ""

if !query_column then query_result = run client () sql !alert_dbms format=json:list and stat=false "select !query_column from !alert_table where period(hour, 1, now(), timestamp) order by timestamp desc limit 1"
else query_result = run client () sql !alert_dbms format=json:list and stat=false "select * from !alert_table where period(hour, 1, now(), timestamp) order by timestamp desc limit 1"

wait 30 for !query_result        # Wait up to 30 seconds

:analyze-data:

if not !query_result then print "results not found"
on error goto analyze-err

for loop start where list = !query_result
    keys = json !query_result[+] keys
    for loop start where list = !keys
        act_value = ""
        key = !keys[+]
        if !key != row_id and !key != insert_timestamp and !key != tsd_name and !key != tsd_id and !key != timestamp then
        do act_value = from !query_result[+] bring [!key]
        if !act_value != "" and !act_value != !expected_value then
        do message = "Water Plant ALERT name=" + !key + " value=" + !act_value
        do call send-msg
    for loop end
for loop end

goto end-script

:send-msg:
if !msg_type == telegram then
do on error goto telegram-err
do telegram_body = json {"chat_id": !chat_id, "text": !message}
do rest post where url = !msg_url and headers = {"Content-Type": "application/json"} and body = !telegram_body

else if !msg_type == pushover then
else do on error goto pushover-err
else do pushover_body = json {"token": !msg_token, "user": !msg_user, "message": !message}
else do rest post where url = !msg_url and headers = {"Content-Type": "application/json"} and body = !pushover_body

else goto missing-type

return

:end-script:
end script

:terminate-scripts:
exit scripts

:query-err:
echo "Failed to get results for query"
goto terminate-scripts

:analyze-err:
echo "Failed to extract results from query"
goto terminate-scripts

:telegram-err:
echo "Error: Failed to send Telegram alert: !message"
goto terminate-scripts

:pushover-err:
echo "Error: Failed to send Pushover alert: !message"
goto terminate-scripts

:missing-type:
echo "Error: Invalid message type: " !msg_type
goto terminate-scripts
```