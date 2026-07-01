---
title: Continuous Monitoring with Automated Alerts 
description: Monitor node health, data volumes, resource usage, and configure automated alerts and scheduled tasks.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
--> 

AnyLog provides multiple layers of monitoring: real-time inspection via `get` commands, continuous polling via the `continuous` command, scheduler-driven metrics collection, streaming conditions for real-time alerting, and aggregator nodes for network-wide visibility.

---

## Quick reference

```anylog
get processes           # service status
get status              # node running status
get connections         # listening IPs and ports
get rows count          # row counts per table
get operator            # operator ingestion status
get streaming           # streaming buffer status
get node info cpu_percent  # CPU usage
get disk free .         # available disk space
```

See <a href="{{ '/docs/Getting-Started/get-commands/' | relative_url }}">Get Commands</a> for the full reference.

---

## Continuous monitoring

`continuous` repeats a set of commands on a fixed interval. Press any key to stop.

```anylog
continuous [seconds] [command1], [command2], ...
```

Examples:
```anylog
continuous cpu, cpu anylog, get operator summary, get streaming

continuous 10 run client () sql my_data select max(timestamp), count(*) from ping_sensor where timestamp >= NOW() - 5 minutes
```

---

## Scheduler-based monitoring

The scheduler runs tasks periodically without manual intervention. See <a href="{{ '/docs/Network-Services/background-services/#scheduler' | relative_url }}">Background Services — Scheduler</a> for how to start it.

### Schedule a monitoring task

```anylog
schedule time = [interval] and name = [task-name] task [command]
```

Examples:
```anylog
schedule time = 15 seconds and name = "Monitor CPU" task cpu_percent = get node info cpu_percent
schedule time = 1 minute and name = "Check disk" task disk_free = get disk free .
schedule time = 5 minutes and name = "Row count" task get rows count where dbms = my_data into dbms = monitor and table = row_counts
```

### Store metrics in a database

First, connect a database and partition the table:
```anylog
connect dbms monitor where type = sqlite
partition monitor cpu_percent using timestamp by 1 day
```

Then schedule collection:
```anylog
schedule time = 15 seconds and name = "Store CPU" task get node info cpu_percent into dbms = monitor and table = cpu_percent
```

Automate cleanup:
```anylog
schedule time = 1 day and start = +1d and name = "Drop old CPU" task drop partition where dbms = monitor and table = cpu_percent
```

### View and manage scheduled tasks

```anylog
get scheduler
get scheduler 1
```

---

## Streaming conditions (real-time alerts)

Streaming conditions evaluate incoming data in real time and trigger actions when conditions are met — without querying the database.

### Set a condition

```anylog
set streaming condition where dbms = [dbms] and table = [table] and limit = [n] if [condition] then [command]
```

- `limit` — optional cap on how many times the action fires (0 = unlimited)
- `condition` — evaluated against each incoming row, e.g. `[value] > 100`
- `command` — any AnyLog command, such as sending an email or SMS

Examples:
```anylog
# Send SMS if temperature exceeds threshold (max 2 times)
set streaming condition where dbms = my_data and table = sensors and limit = 2 if [value] > 85 then sms to 6508147334 where gateway = tmomail.net and subject = "High temp alert" and message = "Value exceeded 85"

# Send email alert
set streaming condition where dbms = my_data and table = sensors if [value] < 0 then email to alerts@company.com where subject = "Below zero" and message = "Sensor reading is negative"

# Log to a table
set streaming condition where dbms = my_data and table = sensors if [status] == "error" then run client () sql my_data "insert into errors values (!timestamp, !device, !value)"
```

### View conditions

```anylog
get streaming conditions
get streaming conditions where dbms = my_data
get streaming conditions where dbms = my_data and table = sensors
```

### Remove conditions

```anylog
reset streaming conditions where dbms = my_data and table = sensors and id = [condition-id]
reset streaming conditions where dbms = my_data
```

---

## Alerts via SMTP

The SMTP client sends emails and SMS messages triggered by streaming conditions or scheduled tasks. Enable it first:

> **Gmail accounts:** The `password` field must be a Google <a href="https://myaccount.google.com/apppasswords" target="_blank">App Password</a>, not your account password. See <a href="{{ '/docs/Network-Services/background-services/#smtp-client' | relative_url }}">Background Services — SMTP</a> for details.

```anylog
run smtp client where email = alerts@company.com and password = mypassword and ssl = true
```

Then use in a condition or scheduled task:
```anylog
email to recipient@company.com where subject = "Alert" and message = "Node disk usage exceeded 90%"
sms to 6508147334 where gateway = tmomail.net and subject = "Alert" and message = "Threshold exceeded"
```

See <a href="{{ '/docs/Network-Services/background-services/#smtp-client' | relative_url }}">Background Services — SMTP</a>.

---

## Alerts via REST POST

AnyLog can send alerts to third-party services by issuing outbound `rest post` requests from streaming conditions, scheduled tasks, or the CLI. This works with any service that accepts an HTTP POST with a JSON body — including <a href="https://core.telegram.org/bots/api" target="_blank">Telegram</a>, <a href="https://pushover.net/api" target="_blank">Pushover</a>, Slack webhooks, and custom endpoints.

See <a href="{{ '/docs/Querying-Data-Northbound/notification/' | relative_url }}">Notification Services</a> for Slack setup and additional examples.

### Telegram

Create a bot via <a href="https://t.me/BotFather" target="_blank">@BotFather</a> to obtain an `API_TOKEN`, and get your `CHAT_ID` from the bot or chat you want to notify.

```anylog
rest post where url = https://api.telegram.org/bot[API_TOKEN]/sendMessage and headers = {"Content-Type": "application/json"} and body = {"chat_id":"[CHAT_ID]","text":"Door ALARM"}
```

In a streaming condition:
```anylog
set streaming condition where dbms = my_data and table = sensors if [status] == "alarm" then rest post where url = https://api.telegram.org/bot[API_TOKEN]/sendMessage and headers = {"Content-Type": "application/json"} and body = {"chat_id":"[CHAT_ID]","text":"Door ALARM"}
```

### Pushover

Register at <a href="https://pushover.net/" target="_blank">pushover.net</a> to obtain an application `API_TOKEN` and a user or group `USER/GROUP_ID`.

```anylog
rest post where url = https://api.pushover.net/1/messages.json and headers = {"Content-Type":"application/json"} and body = {"token":"[API_TOKEN]","user":"[USER/GROUP_ID]","message":"Test 1"}
```

In a streaming condition:
```anylog
set streaming condition where dbms = my_data and table = sensors if [value] > 85 then rest post where url = https://api.pushover.net/1/messages.json and headers = {"Content-Type":"application/json"} and body = {"token":"[API_TOKEN]","user":"[USER/GROUP_ID]","message":"High temp alert: value exceeded 85"}
```

---

## Aggregator node

An aggregator node collects status pushed from multiple nodes, providing a network-wide view without requiring a database. It stores only the **current** status, not historical data.

### On each monitored node

Schedule the push:
```anylog
aggregator = 10.0.0.78:32048

schedule name = get_cpu and time = 15 seconds task node_info[CPU] = get node info cpu_percent
schedule name = get_disk and time = 15 seconds task node_info[Disk Free] = get disk free .
schedule name = get_op and time = 15 seconds task node_info[Operator] = get operator stat format = json
schedule name = get_status and time = 15 seconds task node_info[Status] = get status where format = json
schedule name = push_status and time = 15 seconds task run client (!aggregator) monitor operators where info = !node_info
```

### On the aggregator node

```anylog
get monitored                  # list all topics being monitored
get monitored operators        # current status from all participating nodes
reset monitored operators      # clear the node list for a topic
```

### monitor command

```anylog
monitor [topic] where ip = [node-ip] and name = [node-name] and info = [json-struct]
```

---

## Logging

AnyLog maintains several logs that can be queried on the CLI:

```anylog
get error log               # system errors
get event log               # node events (start, stop, connections)
get query log               # executed SQL queries (must be enabled)
get rest log                # REST requests received
```

Enable the query log:
```anylog
set query log on
set query log profile 10 seconds    # log queries taking longer than 10s
```

Clear a log:
```anylog
reset error log
reset event log
```

---

## Data node visibility

```anylog
get data nodes              # all Operator nodes and the tables they host
get rows count              # row counts across all local tables
get operator                # local operator ingestion stats
get operator inserts        # insert counts per table
get operator summary        # summary of operator activity
```

Query row counts across the network:
```anylog
run client (blockchain get operator bring.ip_port) get rows count where dbms = my_data
```

---

## Resource monitoring

```anylog
get memory info
get cpu info
get cpu temperature
get disk usage .
get disk free .
get disk percentage .
get node info cpu_percent
get node info net_io_counters bytes_recv
get os process anylog
```

See <a href="{{ '/docs/Getting-Started/get-commands/#resource-monitoring' | relative_url }}">Get Commands — Resource monitoring</a> for the full list.
