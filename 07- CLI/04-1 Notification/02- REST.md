---
title: "REST Notifications"
description: "Send notifications via REST — raw REST/cURL calls (Telegram, Pushover) and webhooks."
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**   | **Version** |
 |------------|-------------|--------------|----------|
 | 2026-07-27 | Ori Shadmon | page created | |
 | 2026-07-27 | Ori Shadmon | Removed stray angle brackets from code blocks; fixed "supported commands" line to include POST; grammar cleanup | |
--->

REST-based notifications are probably the most common form of sending notifications.

* [Raw REST call](#rest-calls) where the notification is sent as a `cURL` request from server to the notification system.
* [Webhook](02-1%20Webhooks.md) is an event-driven communication between applications, and is effectively an extension
of the raw REST call below — see that page for Slack, Discord, Microsoft Teams, and Google Chat specifically.

## REST Calls

AnyLog can send data over REST, in a cURL-like mechanism. The `rest` command allows sending REST requests to a REST
server. The REST server can be an AnyLog node that provides a REST connection, or a non-AnyLog node that satisfies REST
requests.

```anylog
rest [operation] where url=[url] and [option] = [value] and [option] = [value] ...
```

**Explanation**: When an AnyLog node is running, it offers a REST API. The REST API accepts REST calls from users and
applications (like Grafana) to network members. Activating the REST API on a particular node is explained in
[Background Processes](../07-%20CLI/02-%20Background%20Processes.md#network-services). Using the `rest` command, users can issue REST calls between members of the
network and between non-members and members of the network. The rest call provides the target URL (of the REST
server) and additional values. The URL must be provided; the other key/value pairs are optional headers and data
values. Supported operations include `get` (retrieve data and metadata from the AnyLog Network) and `post` (send data
to a target URL, as used throughout the Telegram/Pushover/webhook examples below).

### Telegram & Pushover

**Telegram**:
1. Download & Setup _Telegram_ on your phone / laptop.
2. <a href="https://core.telegram.org/bots/tutorial" target="_blank">Create a bot via @BotFather</a> to obtain an
API_TOKEN. Use your CHAT_ID (or a group chat ID) as the destination for messages.
3. Execute the send command via the `rest` command

```anylog
telegram_body = json {"chat_id": !chat_id, "text": !message}

rest post where
    url = !msg_url and headers = {"Content-Type": "application/json"} and
    body = !telegram_body
```

Without the `json` prefix, `!telegram_body` is stored as a literal string containing the unresolved `!chat_id` /
`!message` tokens rather than their actual values. AnyLog's own error log won't show anything wrong — the request still
goes out — but Telegram will silently reject it since the body isn't valid JSON with real values. Always check the
variable back (e.g. `!telegram_body`, or `json !telegram_body`) before relying on it in a script.


**Pushover**:
1. Download & setup <a href="https://pushover.net/" target="_blank">_Pushover_</a>
2. Obtain an application API_TOKEN and a user or group USER/GROUP_ID.
3. Execute the send command via the `rest` command

```anylog
rest post where
    url = https://api.pushover.net/1/messages.json and
    headers = {"Content-Type":"application/json"} and
    body = {"token":"[API_TOKEN]","user":"[USER/GROUP_ID]","message":"Test 1"}
```



### Automating Notifications with Scripts

The examples above are one-off or manually-triggered `rest post` calls. In practice, notifications are usually driven
by a **scheduled script** that queries data on a Query node (via `system_query`, since it needs to scan across
operator node(s)) and only sends a message when something looks wrong.

As such, while the process could be automated, the configurations need to be manually defined per script /
`process` as status regarding different types of information may need to be sent to different people.

For example, insight regarding the amount of space left on the disk would probably need a notification to the IT
department, while a faucet being turned off would need to notify a water engineer.

* <a href="https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/sample-scripts/notifications/row_count.al" target="_blank">Row Count</a> - Scan all the tables on the blockchain (based on the metadata) and check the row count
* <a href="https://github.com/AnyLog-co/deployment-scripts/blob/os-dev/sample-scripts/notifications/smart_city_sensor_state.al" target="_blank">Check sensor</a> - If a sensor is expected to return a static value, send a notification if said value changes

> **Note:** those two sample scripts are the generic templates. A fully worked, customized example (the water plant
> sensor-state check) also lives in the "Scheduler & Notifications" doc — worth linking directly once that page's
> final path in the tree is settled, to avoid three near-duplicate copies of the same walkthrough.

### The Script

1. Define params — these need to be defined per process

```anylog
:set-params:
# logical database and/or table to check
alert_dbms = ""
alert_table = ""
# value a result is expected to match (or deviate from) to trigger an alert
expected_value = ""

# publish msg configs
# which notification backend to use: "telegram" or "pushover"
msg_type = ""

# REST endpoint for the notification service (Telegram/Pushover API URL)
msg_url = ""
# Telegram chat ID to send the alert message to (telegram only)
chat_id = ""
# Pushover application token (pushover only)
msg_token = ""
# Pushover user key (pushover only)
msg_user = ""
```

2. Get result from query — the query itself is specific to whatever's being checked (a row count, a sensor reading, a
disk-space metric, etc.), but the shape of running it and waiting on it is the same regardless

```anylog
query_result = run client () sql !alert_dbms format=json:list and stat=false "select ... from !alert_table where ..."

# there's a need to wait for a response before continuing with result analysis
wait 30 for !query_result        # Wait up to 30 seconds
```

3. Iterate through the results returned and check the returned versus expected value — note that when multiple
columns are returned we can skip the keys that are less important for data analysis

```anylog
for loop start where list = !query_result
    keys = json !query_result[+] keys
    for loop start where list = !keys
        value = ""
        key = !keys[+]
        if !key != row_id and !key != insert_timestamp and !key != tsd_name and !key != tsd_id and !key != timestamp then
        do value = from !query_result[+] bring [!key]
        if !value != "" and !value != !expected_value then
        do message = "ALERT name=" + !key + " value=" + !value
        do call send-msg
    for loop end
for loop end
```

4. If a value doesn't match, send the message via Pushover or Telegram

```anylog
:send-msg:
if !msg_type == telegram then
do on error goto telegram-err
do telegram_body = json {"chat_id": !chat_id, "text": !message}
do rest post where url = !msg_url and headers = {"Content-Type": "application/json"} and body = !telegram_body

else if !msg_type == pushover then
else do on error goto pushover-err
else do pushover_body = json {"token": !msg_token, "user": !msg_user, "message": !message}
else do rest post where url = !msg_url and headers = {"Content-Type": "application/json"} and body = !pushover_body
```

5. Run it once, or register it as a recurring scheduled task — a query only reflects data as of the moment it runs, so
the check needs to repeat on an interval matched to how quickly the underlying condition (a staleness window, a
sensor flipping state, disk space filling up) could change and go unnoticed between checks

```anylog
# Run once, ad-hoc:
process !local_scripts/smart-city/wp_digital_notification.al

# Or register as a recurring scheduled task:
schedule name = wp-digital-alert and time = 15 minutes and task process !local_scripts/smart-city/wp_digital_notification.al
```

### A note on running multiple copies

Because AnyLog script variables are shared/global on a node, every deployed copy of this script needs its own
variable namespace if more than one copy runs concurrently — for example, one script per table, or the same table
routed to two different destinations. Prefix every variable in a given copy (`alert_dbms`, `alert_table`,
`expected_value`, `msg_type`, `msg_url`, `chat_id`, `msg_token`, `msg_user`, and the working variables `query_result`,
`keys`, `value`, `message`) with something unique to that deployment, e.g. `wp_alert_dbms`, `wwp_alert_dbms`. Rename
consistently across the entire script — `set-params`, the query/analysis loop, and `send-msg` all need to agree — and
avoid reusing another deployed script's prefix, even if it happens to point at the same destination.