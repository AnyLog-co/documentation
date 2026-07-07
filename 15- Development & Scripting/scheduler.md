---
title: Scheduler & Scheduled Tasks
description: Run repeatable tasks on a fixed interval to monitor node state, collect metrics, and trigger actions.
layout: page
---
<!--
## Changelog
- 2026-05-29 | Created document
-->

The scheduler executes commands or scripts at a configured interval without manual intervention. Tasks can read local or remote node state, query data across the network, update summary tables, and trigger alerts.

Scheduler `0` is reserved for system use. User schedulers start at `1`.

---

## Quick reference

```anylog
run scheduler [id]                          # start a scheduler (default id = 1)
exit scheduler [id]                         # stop one scheduler, or all if id omitted
schedule time = [interval] and name = [name] task [command]   # add a task
get scheduler                               # list all scheduled tasks
get scheduler 1                             # tasks on scheduler 1
task stop where name = [name]               # pause a task
task resume where name = [name]             # resume a paused task
task remove where name = [name]             # remove a task
task run where name = [name]                # run a task immediately
task init where name = [name] and start = [time]   # reschedule a task's start time
```

---

## Starting and stopping the scheduler

```anylog
run scheduler 1       # start user scheduler
exit scheduler 1      # stop scheduler 1 only
exit scheduler        # stop all schedulers
```

See <a href="{{ '/docs/Network-Services/background-services/#scheduler' | relative_url }}">Background Services — Scheduler</a> for startup configuration.

---

## Adding tasks

```anylog
schedule [options] task [command or script]
```

### Options

| Option | Explanation |
| --- | --- |
| `time` | Interval between executions (e.g. `15 seconds`, `5 minutes`, `1 day`) |
| `start` | When to run the first execution. Defaults to current date and time |
| `name` | Unique name for the task within the scheduler |
| `scheduler` | Scheduler ID to add the task to. Defaults to `1` |

### Examples

```anylog
# Store CPU usage every 15 seconds
schedule time = 15 seconds and name = "Store CPU" task get node info cpu_percent into dbms = monitor and table = cpu_percent

# Check disk space every minute
schedule time = 1 minute and name = "Check disk" task disk_free = get disk free .

# Collect row counts every 5 minutes
schedule time = 5 minutes and name = "Row count" task get rows count where dbms = my_data into dbms = monitor and table = row_counts

# Run a script at the start of each day
schedule time = 1 day and name = "Sync Devices" and start = "start of day" task process !local_scripts/sync_script.al
```

### Setting the start time

The `start` option accepts a date/time string or one of the following keywords:

| Value | Meaning |
| --- | --- |
| `now()` | Immediately |
| `start of year` | First moment of the current year |
| `start of month` | First moment of the current month |
| `start of day` | Midnight of the current day |
| `start of hour` | Top of the current hour |
| `start of minute` | Top of the current minute |

Time-forward values (relative to now) are also accepted:

| Unit | Meaning |
| --- | --- |
| `y` | Year |
| `m` | Month |
| `w` | Week |
| `d` | Day |
| `h` | Hour |
| `t` | Minute |
| `s` | Second |

Example — start two hours from now:
```anylog
task init where name = "Get Disk Space" and start = +2h
```

---

## Viewing scheduled tasks

```anylog
get scheduler       # all schedulers
get scheduler 1     # scheduler 1 only
```

---

## Managing tasks

All `task` commands default to scheduler `1` when no `scheduler` option is given. Tasks can be referenced by name or by their numeric ID shown in `get scheduler`.

### Pause and resume

```anylog
task stop where scheduler = 1 and name = "Monitor CPU"
task resume where scheduler = 1 and name = "Monitor CPU"
```

### Remove

```anylog
task remove where scheduler = 1 and name = "Monitor CPU"
```

### Immediate execution

```anylog
task run where scheduler = 1 and name = "Monitor CPU"
```

### Reschedule start time

Use `task init` to push a task's next execution forward — useful to suppress repeated alerts after one has already fired:

```anylog
# Pause disk-space alerts for 2 hours
task init where scheduler = 1 and name = "Monitor Space" and start = +2h

# Resume at the start of the next day
task init where scheduler = 1 and name = "Monitor Space" and start = +1d
```

---

## Storing metrics in a database

Connect a database and partition the table before scheduling writes:

```anylog
connect dbms monitor where type = sqlite
partition monitor cpu_percent using timestamp by 1 day
```

Then schedule collection and cleanup:

```anylog
# Collect every 15 seconds
schedule time = 15 seconds and name = "Store CPU" task get node info cpu_percent into dbms = monitor and table = cpu_percent

# Drop yesterday's partition daily
schedule time = 1 day and start = +1d and name = "Drop old CPU" task drop partition where dbms = monitor and table = cpu_percent
```

---

## Repeatable queries

A repeatable query runs on a fixed interval and writes results into a summary (rollup) table. `TIME(PREVIOUS)` and `TIME(CURRENT)` are substituted dynamically at each execution.

```anylog
schedule time = 5 minutes and name = "Summary sensor data" task run client () sql my_data table = summary_sensor and drop = false "SELECT max(timestamp), min(value), max(value), avg(value) from cos_data where timestamp >= TIME(PREVIOUS) and timestamp < TIME(CURRENT)"
```

The summary table can be used as a Grafana data source to alert on missing data, late-reporting nodes, or out-of-range values.

---

## Common patterns

### Monitor disk space and alert

```anylog
# Step 1 — collect free space every 5 minutes
schedule time = 5 minutes and name = "Get Disk Space" task disk_free = get disk free d:\

# Step 2 — alert if below threshold, then suspend for 1 day
schedule time = 5 minutes and name = "Alert Disk Space" task if !disk_free < 1000000000 then
do email to admin@company.com where subject = "Disk Space Alert" and message = "Disk drive is under threshold"
do sms to 6505550000 where gateway = tmomail.net and subject = "Disk Space Alert" and message = "Disk drive is under threshold"
do task init where name = "Alert Disk Space" and start = +1d
```

Using `task init` after sending the alert prevents the same message from firing every 5 minutes.

### Distribute row-count checks across the network

```anylog
schedule time = 5 minutes and name = "Network row counts" task run client (blockchain get operator bring.ip_port) get rows count where dbms = my_data
```

See <a href="{{ '/docs/Getting-Started/get-commands/' | relative_url }}">Get Commands</a> for the full list of commands that can be used inside tasks.