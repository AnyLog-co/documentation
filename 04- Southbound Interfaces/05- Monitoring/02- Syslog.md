---
title: Syslog Integration
description: Ingest BSD and IETF syslog messages from Linux, Mac, and network devices directly into AnyLog — prerequisites, node configuration, and running/validating the pipeline.
layout: page
source_path: "07- Southbound Interfaces/Syslog Integration.md"
---

<!---
### 📜 Change Log

| **Date** | **Name** | **Change** |
|---|---|---|
| 2026-04-17 | | Creation (original `Syslog integration.md` and `Using Syslog.md`) |
| 2026-04-26 | | Updated to explain how to change syslog configs to get the data |
| 2026-07-14 | | Merged three overlapping syslog docs (`ZZZ syslog.md`, `Using Syslog.md`, `Syslog integration.md`) into a single canonical file |
| 2026-07-17 / 2026-07-20 | Eric Aquaronne | Added change log |
| 2026-07-24 | Ori Shadmon | Consolidated the (still-duplicated, still merge-conflicted) canonical file plus the two original source docs into this
  single final version. Resolved an unresolved git merge conflict marker that had been sitting at the top of the "canonical"
  file. Restructured around three steps — **prerequisites → configure the node → run/validate** — per request, folding the
  syslog-format reference into the configure step (you need to know BSD vs. IETF before you can set `syslog=`/`format=`
  correctly). Standardized all examples on a single running `new_company` / `syslog` dbms+table pair instead of switching
  between `test`, `monitoring`, and `new_company` across examples. Added a callout on the dotenv-based automation path
  (`make setup SERVICE=syslog`) so readers know the manual steps below can be skipped entirely for standard deployments. |
--->

<a href="https://en.wikipedia.org/wiki/Syslog" target="_blank">Syslog</a> is a standardized protocol for sending and
receiving log messages across a network. AnyLog can act as a syslog receiver, accepting messages from any host that
supports TCP syslog output and storing them as queryable time-series data alongside all other data in the network —
letting you monitor and troubleshoot the status of many machines from a single point rather than checking each one
separately.

> **Prefer automation?** Everything below — the rsyslog forwarding rule and the AnyLog-side message rule — can be set
> up automatically via the dotenv-driven `syslog.sh` script, wired into `make setup SERVICE=syslog`. It reads
> `SYSLOG_MONITORING` and `ANYLOG_BROKER_PORT` from your node's `node_configs.env` and is idempotent (safe to re-run,
> and a no-op if `SYSLOG_MONITORING != "true"`). See the <a href="../../13-%20Support%20%26%20Troubleshooting/04-%20Third-Party%20Support/01-%20Docker%20%26%20K8s%20Commands.md#syslog-forwarding" target="_blank">Docker & K8s Commands</a>
> doc for the exact command. The manual walkthrough below is for understanding what that automation is doing, or for
> setting things up by hand.

---

## 1. Prerequisites

### On the physical machine — install and start rsyslog

```shell
sudo apt-get -y update
sudo apt -y install rsyslog
sudo service rsyslog start
```

> The same steps apply to <a href="https://www.syslog-ng.com/" target="_blank">syslog-ng</a> if preferred over rsyslog.

Validate rsyslog is running:

```shell
tail -f /var/log/syslog
```

**Expected output:**
```
Feb 25 02:55:47 localhost systemd[1]: Started User Manager for UID 0.
Feb 25 02:55:47 localhost systemd[1]: Started Session 197 of User root.
Feb 25 02:55:52 localhost systemd-udevd[400]: Network interface NamePolicy= disabled on kernel command line, ignoring.
Feb 25 02:55:53 localhost dbus-daemon[31261]: AppArmor D-Bus mediation is enabled
...
```

---

## 2. Configure the Node

### Understand the syslog formats

Syslog is delivered from each machine in one of two formats — knowing which one you're receiving determines how you'll
set the `syslog` / `format` options on the rule below.

| Format | Standard | Timestamp | Key fields |
|---|---|---|---|
| BSD | RFC 3164 | `MMM dd hh:mm:ss` | Priority, Timestamp, Hostname, Tag (process + PID), Message |
| IETF | RFC 5424 | ISO 8601 | Priority, Version, Timestamp, Hostname, Application, PID, Message ID, Structured Data, Message |

<details>
<summary>Field-by-field breakdown</summary>

**BSD format fields**
1. **Priority** — enclosed in angle brackets (`<` and `>`); a numeric value combining facility and severity (e.g. `<34>`).
2. **Timestamp** — immediately follows the priority, typically `MMM dd hh:mm:ss` (e.g. `Jan 12 23:34:56`).
3. **Hostname or IP address** — the name or IP of the device that sent the message.
4. **Tag** — often a process name or application identifier, potentially followed by a process ID in square brackets (e.g. `sshd[3268]`).
5. **Message** — the actual log message text, following the tag.

**IETF format fields**
1. **Priority** — same as BSD, enclosed in angle brackets.
2. **Version** — a single digit indicating the syslog protocol version (e.g. `1`).
3. **Timestamp** — more precise than BSD, typically ISO 8601.
4. **Hostname** — as in BSD format.
5. **Application** — the name of the application or process generating the message.
6. **Process ID (PID)** — the PID of the process.
7. **Message ID** — a unique identifier for the type of message.
8. **Structured data** — enclosed in square brackets, key-value pairs for additional data.
9. **Message** — the actual log message text.

</details>

### Start the message broker

The message broker is the TCP listener that receives syslog traffic. AnyLog's regular TCP service is dedicated to
communication *between* AnyLog nodes and cannot be used for external data ingestion — the message broker is the
correct service for receiving data from outside the network. Start it on the operator or publisher node:

```anylog
<run message broker where
    external_ip = !external_ip and external_port = !anylog_broker_port and
    internal_ip = !ip and internal_port = !anylog_broker_port and
    bind = !broker_bind and threads = !broker_threads>
```

Check which IP/port to direct syslog output to:

```anylog
get connections
```

### Point rsyslog at AnyLog

Add the following to the bottom of `/etc/rsyslog.conf`, replacing `DESTINATION_IP` and `DESTINATION_PORT` with the
AnyLog operator/publisher IP and message broker port found above:

```
$template remote-incoming-logs, "/var/log/remote/%HOSTNAME%.log"
*.* ?remote-incoming-logs
*.* action(type="omfwd" target="{DESTINATION_IP}" port="{DESTINATION_PORT}" protocol="tcp")
```

Restart rsyslog to apply:

```shell
sudo service rsyslog restart
```

> This is exactly the step `syslog.sh setup` automates on Linux (via an rsyslog drop-in) and on macOS (via
> `/etc/syslog.conf`) — see the automation callout above.

### Set a syslog rule

Rules tell AnyLog how to route and parse incoming syslog messages:

```anylog
set msg rule [rule name] if ip = [source IP] and port = [port] and header = [header text] then dbms = [dbms] and table = [table] and syslog = [true/false] and extend = ip and format = [format] and topic = [topic]
```

| Option | Required | Description |
|---|---|---|
| `rule name` | ✅ | Unique name for this rule |
| `ip` | — | Source IP to match — omit to match all IPs |
| `port` | — | Source port to match — omit to match all ports |
| `header` | — | Match messages with a specific prefix string (see Example 2 below) |
| `dbms` | ✅ | Target logical database |
| `table` | ✅ | Target table |
| `syslog` | — | `true` — parse as BSD syslog. Set `format = IETF` for RFC 5424 |
| `extend` | — | Add extra fields — `extend = ip` adds the source IP |
| `format` | — | Override the default format: `IETF` for RFC 5424 |
| `topic` | — | Route through the msg-client mapping layer (like MQTT) |
| `structure` | — | `included` — first message event defines the column schema (see Example 3 below) |

> When `syslog = true`, column names are pre-determined by the format (BSD by default, or `format = IETF`).
> When `syslog` is not set, use `structure = included` so the first event defines the schema instead.

**Basic example** — accept BSD syslog from this node's own default database/table:

```anylog
set msg rule syslog_rule if ip = !ip then dbms = new_company and table = syslog and syslog = true
```

### Partition & clean up (recommended)

Syslog volume adds up quickly — partition the table and schedule automatic cleanup so it doesn't grow unbounded:

```anylog
connect dbms new_company where type=sqlite
partition new_company syslog using insert_timestamp by 12 hours
schedule time = 12 hours and name = "Drop Partition Sync - Syslog" task drop partition where dbms = new_company and table = syslog and keep = 3
```

### More configuration examples

**Example — Linux `journalctl` via netcat, with a header prefix**

Pipe `journalctl` output to AnyLog, prefixing each line with a custom header so the rule below can match on it:

```bash
journalctl --since "${NOW}" | awk '{print "al.sl.header.new_company.syslog", $0}' | nc -w 1 10.0.0.78 7850
```

```anylog
set msg rule my_rule if ip = 10.0.0.50 and header = al.sl.header.new_company.syslog then dbms = new_company and table = syslog and syslog = true
```

**Example — Mac syslog with dynamic structure from the first event**

```bash
(log show --info --start '2024-01-01 16:50:00' --end '2024-12-01 16:51:00' | awk '{print "al.sl", $0}') | nc -w 1 10.0.0.78 7850
```

The first event contains the column headers, which `structure = included` uses to define the schema:

```
al.sl Timestamp                       Thread     Type        Activity             PID    TTL
al.sl 2024-01-01 17:51:35.253053-0800 0x4d0c71   Default     0x39223d             482    3   ...
```

```anylog
set msg rule my_rule if ip = 10.0.0.251 and header = al.sl then dbms = new_company and table = syslog_mac and structure = included
```

---

## 3. Run & Validate

### Trigger test data

On the monitored machine, run an update/upgrade (or anything else that generates log activity):

```shell
sudo apt-get -y update
sudo apt-get -y upgrade
```

### Confirm the rule is active and receiving data

```anylog
get msg rules
```

**Expected output:**
```
Name        IF            IF    IF      THEN        THEN   THEN    THEN   THEN       Batches Events Errors Error Msg
            Source IP     Port  Header  DBMS        Table  SysLog  Topic  Structure
-----------|-------------|-----|-------|-----------|------|-------|------|----------|-------|------|------|---------|
syslog_rule|10.0.0.78    |*    |       |new_company|syslog|True   |      |          |     18|    32|     0|         |
```

### Query the data

From a query node:

```anylog
-- row count
run client () sql new_company format=table "select count(*) from syslog"

-- sample rows
run client () sql new_company "select * from syslog limit 10"
```

**Sample output** (note the `tsd_name` / `tsd_id` partition-metadata columns AnyLog adds automatically):

```json
{"Query":[
  {"row_id":1,
   "insert_timestamp":"2024-02-25 03:18:35.023262",
   "tsd_name":"131",
   "tsd_id":4610,
   "priority":38,
   "timestamp":"2024-02-25 03:17:27.000000",
   "hostname":"localhost",
   "tag":"sshd[32839]:",
   "message":"Invalid user lighthouse from 10.0.0.100 port 45126"},
  {"row_id":2,
   "insert_timestamp":"2024-02-25 03:18:35.023262",
   "tsd_name":"131",
   "tsd_id":4610,
   "priority":85,
   "timestamp":"2024-02-25 03:17:27.000000",
   "hostname":"localhost",
   "tag":"sshd[32839]:",
   "message":"pam_unix(sshd:auth): check pass; user unknown"}
],
"Statistics":[{"Count": 10, "Time":"00:00:00", "Nodes": 1}]}
```

### Manage & debug

```anylog
get msg rules                  -- list all active rules and their event counts
reset msg rule [rule name]     -- remove a rule
```

Enable trace to see the source IP, port, and first 100 bytes of each incoming message:

```anylog
trace level = 2 run message broker
```

**Example trace output:**
```
[Message Broker Received 1650 Bytes] [Source: 10.0.0.78:1468] [Data: <134>Jan 26 17:30:10 DESKTOP sshd[3268] User login...]
```

A single message may contain multiple events — trace only shows the first 100 bytes of each. Use `get msg rules` to
see the actual number of events processed.