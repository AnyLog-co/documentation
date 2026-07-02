---
title: Alerts & Messaging
description: Send email, SMS, and webhook notifications from scheduled tasks or streaming conditions.
layout: page
---
<!--
## Changelog
- 2026-04-17 | Created document
- 2026-05-29 | Rewrote document to better different notification / scheduler options
-->

AnyLog can send email, SMS, and webhook notifications when thresholds are crossed or conditions are met. Messages are 
triggered from <a href="{{ '/docs/Monitoring/scheduler/' | relative_url }}">scheduled tasks</a> or 
<a href="{{ '/docs/Monitoring/node-monitoring/#streaming-conditions-real-time-alerts' | relative_url }}">streaming conditions</a>.

---

## Quick reference

```anylog
run smtp client where email = [address] and password = [pwd] and ssl = true   # enable SMTP

email to [address] where subject = [text] and message = [text]                # send email
sms to [phone] where gateway = [gateway] and subject = [text] and message = [text]  # send SMS

rest post where url = [webhook-url] and body = [json-payload] and headers = "{'Content-Type': 'application/json'}"  # webhook
```

---

## Enabling the SMTP client

Start the SMTP client before issuing any `email` or `sms` commands:

```anylog
run smtp client where email = alerts@company.com and password = mypassword and ssl = true
```

See <a href="{{ '/docs/Network-Services/background-services/#smtp-client' | relative_url }}">Background Services — SMTP</a> for full configuration options.

---

## Sending email

```anylog
email to [receiver email] where subject = [subject] and message = [message text]
```

| Option | Explanation | Default |
| --- | --- | --- |
| `receiver email` | Destination address | — |
| `subject` | Subject line text | `AnyLog Alert` |
| `message` | Body text | `AnyLog Network Alert from Node: [node name]` |

Multiple `message` options appear as separate lines in the email body:

```anylog
email to admin@company.com where subject = "High CPU Alert" and message = "CPU utilization exceeded threshold" and message = "Reporting node: 10.0.0.5 (Operator-West)"
```

---

## Sending SMS

```anylog
sms to [phone number] where gateway = [sms gateway] and subject = [subject] and message = [message text]
```

| Option | Explanation | Default |
| --- | --- | --- |
| `phone number` | Destination phone number | — |
| `gateway` | SMS carrier email gateway | — |
| `subject` | Subject line text | `AnyLog Alert` |
| `message` | Message text | `AnyLog Network Alert from Node: [node name]` |

Example with T-Mobile:
```anylog
sms to 6508147334 where gateway = tmomail.net and subject = "Threshold exceeded" and message = "Sensor value above limit"
```

### US carrier gateways

| Carrier | Gateway |
| --- | --- |
| AT&T | `txt.att.net` |
| Sprint | `messaging.sprintpcs.com` |
| T-Mobile | `tmomail.net` |
| Verizon | `vtext.com` |
| Boost Mobile | `myboostmobile.com` |
| Metro PCS | `mymetropcs.com` |
| Tracfone | `mmst5.tracfone.com` |
| U.S. Cellular | `email.uscc.net` |
| Virgin Mobile | `vmobl.com` |

A full carrier list is available at the [SMS gateway reference](https://kb.sandisk.com/app/answers/detail/a_id/17056/).

---

## Triggering alerts from scheduled tasks

Combine a condition check with messaging inside a scheduled task:

```anylog
# Alert if disk space drops below 1 GB, then suppress for 1 day
schedule time = 5 minutes and name = "Monitor Space" task process !scripts_dir/monitor_space.al
```

Where `monitor_space.al` contains:

```anylog
disk_free = get disk free !monitored_drive
if !disk_free < 1000000000 then
do email to admin@company.com where subject = "Disk Space Alert" and message = "Disk drive is under threshold"
do sms to 6505550000 where gateway = tmomail.net and subject = "Disk Space Alert" and message = "Disk drive is under threshold"
do task init where name = "Monitor Space" and start = +1d
```

The `task init` call at the end pushes the task's next start time forward by one day, preventing the alert from re-firing every 5 minutes. See <a href="{{ '/docs/Monitoring/scheduler/' | relative_url }}">Scheduler & Scheduled Tasks</a> for details on `task init`.

---

## Webhooks

Webhooks are HTTP callbacks that deliver messages into third-party applications using a single REST POST — no custom integration required. AnyLog sends webhook notifications using the `rest` command.

Supported platforms and their setup guides:

- [Slack](https://api.slack.com/messaging/webhooks)
- [Discord](https://docs.gitlab.com/ee/user/project/integrations/discord_notifications.html#create-webhook)
- [Microsoft Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
- [Google Chat](https://developers.google.com/workspace/chat/quickstart/webhooks)

### Send a webhook notification

Once you have a webhook URL from your platform, use the `rest` command to POST a message:

```anylog
# Store the webhook URL
webhook_url = "https://hooks.slack.com/services/T9EB83JTF/B06Q4F5R0QK/..."

# Build the payload (Slack uses "text"; Discord, Teams, and Google Chat use "content")
cpu_percent = get node info cpu_percent
date_time = python "datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')"
text_msg = !date_time + "  CPU usage: " + !cpu_percent
payload = json {"text": !text_msg}

# POST to Slack
rest post where url = !webhook_url and body = !payload and headers = "{'Content-Type': 'application/json'}"
```

> **Note:** Discord, Microsoft Teams, and Google Chat use `content` as the payload key instead of `text`.

### Use in a scheduled task

```anylog
schedule time = 15 seconds and name = "CPU webhook" task
do cpu_percent = get node info cpu_percent
do date_time = python "datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')"
do text_msg = !date_time + "  CPU usage: " + !cpu_percent
do payload = json {"text": !text_msg}
do rest post where url = !webhook_url and body = !payload and headers = "{'Content-Type': 'application/json'}"
```

See <a href="{{ '/docs/anylog-commands/#rest-command' | relative_url }}">AnyLog Commands — REST</a> for full `rest` command syntax.

---

## Triggering alerts from streaming conditions

Streaming conditions evaluate incoming data rows in real time, before they are written to the database. Use them for low-latency alerting without polling.

### Set a condition

```anylog
set streaming condition where dbms = [dbms] and table = [table] and limit = [n] if [condition] then [command]
```

| Option | Explanation |
| --- | --- |
| `limit` | Maximum number of times the action fires. `0` = unlimited |
| `condition` | Expression evaluated against each incoming row, e.g. `[value] > 100` |
| `command` | Any AnyLog command — email, SMS, SQL insert, etc. |

Examples:

```anylog
# SMS alert, fires at most 2 times
set streaming condition where dbms = my_data and table = sensors and limit = 2 if [value] > 85 then sms to 6508147334 where gateway = tmomail.net and subject = "High temp alert" and message = "Value exceeded 85"

# Email alert for negative readings
set streaming condition where dbms = my_data and table = sensors if [value] < 0 then email to alerts@company.com where subject = "Below zero" and message = "Sensor reading is negative"

# Write error rows to a separate table
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
# Remove a specific condition by ID
reset streaming conditions where dbms = my_data and table = sensors and id = [condition-id]

# Remove all conditions on a database
reset streaming conditions where dbms = my_data
```