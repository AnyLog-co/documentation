---
title: Syslog
description: Ingest BSD and IETF syslog messages from Linux, Mac, and network devices directly into AnyLog.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-04-26 | updated to explain how to change syslog configs to get the data   
-->

| Date of change | Relevant AnyLog version | Author | Description |
|---|---|---|---|
| - | - | - | Documentation Copyright AnyLog.co 2026 |
| 2026-04-17 | All | - | Created document |

<a href="https://en.wikipedia.org/wiki/Syslog" target="_blank">Syslog</a> is a standardized protocol for sending and 
receiving log messages across a network. AnyLog can act as a syslog receiver, accepting messages from any host that 
supports TCP syslog output, storing them as queryable time-series data alongside all other data in the network.

---

## Syslog formats

| Format | Standard | Timestamp | Key fields |
|---|---|---|---|
| BSD | RFC 3164 | `MMM dd hh:mm:ss` | Priority, Timestamp, Hostname, Tag (process + PID), Message |
| IETF | RFC 5424 | ISO 8601 | Priority, Version, Timestamp, Hostname, Application, PID, Message ID, Structured Data, Message |

---

## Prerequisites

1. Physical machine — install and start rsyslog

```shell
sudo apt-get -y update
sudo apt -y install rsyslog
sudo service rsyslog start
```

2. Validate rsyslog is running:

```shell
tail -f /var/log/syslog
```

**Expected output**:
```
Feb 25 02:55:47 localhost systemd[1]: Started User Manager for UID 0.
Feb 25 02:55:47 localhost systemd[1]: Started Session 197 of User root.
Feb 25 02:55:52 localhost systemd-udevd[400]: Network interface NamePolicy= disabled on kernel command line, ignoring.
Feb 25 02:55:53 localhost dbus-daemon[31261]: AppArmor D-Bus mediation is enabled
...
```

> The same steps apply to <a href="https://www.syslog-ng.com/" target="_blank">syslog-ng</a> if preferred over rsyslog.

2. AnyLog node — start the message broker

The message broker is the TCP listener that receives syslog traffic. AnyLog's TCP service is dedicated to
communication between AnyLog nodes and cannot be used for external data ingestion — the 
[message broker](/docs/Network-Services/messaging-services/) is the correct service for receiving data from outside the 
network. Start it on the operator or publisher node:


```anylog
<run message broker where
    external_ip = !external_ip and external_port = !anylog_broker_port and
    internal_ip = !ip and internal_port = !anylog_broker_port and
    bind = !broker_bind and threads = !broker_threads>
```

Check which port to direct syslog output to:

```anylog
get connections
```

3. AnyLog node — configure partitioning (recommended)

Due to the volume of syslog data, partition the table and schedule automatic cleanup:

```anylog
connect dbms monitoring where type=sqlite
partition monitoring syslog using insert_timestamp by 12 hours
schedule time = 12 hours and name = "Drop Partition Sync - Syslog" task drop partition where dbms = !default_dbms and table = syslog and keep = 3
```

---

## Connect rsyslog to AnyLog

Add the following lines to the bottom of `/etc/rsyslog.conf`, replacing `DESTINATION_IP` and `DESTINATION_PORT`
with the AnyLog operator or publisher IP and message broker port:

```
$template remote-incoming-logs, "/var/log/remote/%HOSTNAME%.log"
*.* ?remote-incoming-logs
*.* action(type="omfwd" target="{DESTINATION_IP:-127.0.0.1}" port="{DESTINATION_PORT:-32150}" protocol="tcp")
```

Restart rsyslog to apply:

```shell
sudo service rsyslog restart
```

---

## Set a syslog rule

Rules tell AnyLog how to route and parse incoming syslog messages:

```anylog
set msg rule [rule name] if ip = [source IP] and port = [port] and header = [header text] then dbms = [dbms] and table = [table] and syslog = [true/false] and extend = ip and format = [format] and topic = [topic]
```

| Option | Required | Description |
|---|---|---|
| `rule name` | ✅ | Unique name for this rule |
| `ip` | — | Source IP to match — omit to match all IPs |
| `port` | — | Source port to match — omit to match all ports |
| `header` | — | Match messages with a specific prefix string |
| `dbms` | ✅ | Target logical database |
| `table` | ✅ | Target table |
| `syslog` | — | `true` — parse as BSD syslog. Set `format = IETF` for RFC 5424 |
| `extend` | — | Add extra fields — `extend = ip` adds the source IP |
| `format` | — | Override default format: `IETF` for RFC 5424 |
| `topic` | — | Route through the msg client mapping layer (like MQTT) |
| `structure` | — | `included` — first message event defines the column schema |

> When `syslog = true`, column names are pre-determined by the format (BSD by default).
> When `syslog` is not set, use `structure = included` so the first event defines the schema.

---

## Examples

### Example 1 — rsyslog from a specific host

Basic rule accepting BSD syslog from a specific host:

```anylog
set msg rule syslog_rule if ip = !ip then dbms = !default_dbms and table = syslog and syslog = true
```

### Example 2 — Linux journalctl via netcat with a header prefix

Pipe `journalctl` output to AnyLog, prefixing each line with a custom header:

```bash
journalctl --since "${NOW}" | awk '{print "al.sl.header.new_company.syslog", $0}' | nc -w 1 10.0.0.78 7850
```

Rule on the operator matching the prefix:

```anylog
set msg rule my_rule if ip = 10.0.0.50 and header = al.sl.header.new_company.syslog then dbms = test and table = syslog and syslog = true
```

### Example 3 — Mac syslog with dynamic structure from first event

```bash
(log show --info --start '2024-01-01 16:50:00' --end '2024-12-01 16:51:00' | awk '{print "al.sl", $0}') | nc -w 1 10.0.0.78 7850
```

The first event contains the column headers:
```
al.sl Timestamp                       Thread     Type        Activity             PID    TTL
al.sl 2024-01-01 17:51:35.253053-0800 0x4d0c71   Default     0x39223d             482    3   ...
```

Rule using `structure = included`:

```anylog
set msg rule my_rule if ip = 10.0.0.251 and header = al.sl then dbms = test and table = syslog_mac and structure = included
```

---

## Validate

### Check the rule is active and receiving data

```anylog
get msg rules
```

Expected output:

```
Name        IF            IF    IF      THEN        THEN   THEN    THEN   THEN       Batches Events Errors Error Msg
            Source IP     Port  Header  DBMS        Table  SysLog  Topic  Structure
-----------|-------------|-----|-------|-----------|------|-------|------|----------|-------|------|------|---------|
syslog_rule|10.0.0.78    |*    |       |new_company|syslog|True   |      |          |     18|    32|     0|         |
```

### Trigger test data

Run an update/upgrade on the monitored machine to generate syslog activity:

```shell
sudo apt-get -y update
sudo apt-get -y upgrade
```

### Query the data

From a query node:

```anylog
-- row count
run client () sql new_company format=table "select count(*) from syslog"

-- sample rows
run client () sql new_company "select * from syslog limit 10"
```

Sample output:

```json
{"Query":[
  {"row_id":1,
   "insert_timestamp":"2024-02-25 03:18:35.023262",
   "priority":38,
   "timestamp":"2024-02-25 03:17:27.000000",
   "hostname":"localhost",
   "tag":"sshd[32839]:",
   "message":"Invalid user lighthouse from 10.0.0.100 port 45126"},
  {"row_id":2,
   "insert_timestamp":"2024-02-25 03:18:35.023262",
   "priority":85,
   "timestamp":"2024-02-25 03:17:27.000000",
   "hostname":"localhost",
   "tag":"sshd[32839]:",
   "message":"pam_unix(sshd:auth): check pass; user unknown"}
]}
```

---

## Manage and debug

```anylog
get msg rules                  -- list all active rules and event counts
reset msg rule [rule name]     -- remove a rule
```

Enable trace to see the source IP, port, and first 100 bytes of each incoming message:

```anylog
trace level = 2 run message broker
```

Example trace output:

```
[Message Broker Received 1650 Bytes] [Source: 10.0.0.78:1468] [Data: <134>Jan 26 17:30:10 DESKTOP sshd[3268] User login...]
```