---
title: "SMTP"
description: "Send notifications via SMTP (email and SMS)"
layout: page
---
<!---
### 📜 Change Log
 **Date**   | **Name**    | **Change**   | **Version** |
 |------------|-------------|--------------|----------|
 | 2026-07-27 | Ori Shadmon | page created | |
 | 2026-07-27 | Ori Shadmon | Fixed broken/stale links, removed stray angle brackets, redacted example password/phone number, added current (2026) status of carrier email-to-SMS gateways — most major US carriers have shut theirs down | |
--->

Simple Mail Transfer Protocol (SMTP) is a protocol to send and relay emails. In addition it can be used as a tool to
send SMS messages via email (i.e. email -> phone) as well — though see the important caveat under
[Sending SMS messages](#sending-sms-messages) before relying on that path.

This document describes how to initiate the SMTP service on AnyLog and how to use it.

## Setting up SMTP

Enables email and SMS notifications triggered by the scheduler or rule engine.
See <a href="{{ '/docs/Monitoring/alerts-and-monitoring/' | relative_url }}">Alerts and Monitoring</a> for how to
configure notification rules.

```anylog
run smtp client where
  host = [host] and port = [port] and
  email = [address] and password = [password] and
  ssl = [true/false]
```

| Option | Description | Default |
|---|---|---|
| `host` | SMTP server URL | `smtp.gmail.com` |
| `port` | SMTP server port | |
| `email` | Sender email address | |
| `password` | Sender email password | |
| `ssl` | Use secure SMTP connection | `false` |

Example:
```anylog
run smtp client where email = anylog.iot@gmail.com and password = [password]
```


## Sending a message

To facilitate messages, declare the _SMTP_ client process. Details are available at
[Background Processes](../07-%20CLI/02-%20Background%20Processes.md) (see the Services overview table — `run smtp client`).

### Sending an email
**Usage**:
```anylog
email to [receiver email] where subject = [message subject] and message = [message text]
```
Command Options:

| Option        | Explanation  | Default  |
| ------------- | ------------| ---- |
| receiver email | The destination address | |
| message subject | Any text | AnyLog Alert |
| message text | Any text | AnyLog Network Alert from Node: [node name] |

Example:
```anylog
email to my_name@my_company.com
```

Multiple message texts on the command line, like the example below, will be represented as multiple lines in the email message:
```anylog
email to my_name@my_company.com  where subject = "anylog alert" and message = "Value of Heater sensor is above threshold" and message = "Reporting node: 24.23.250.144 (Operator SF)"
```


### Sending SMS messages

> **Important — carrier gateways are largely deprecated as of 2026.** The `sms to` command below works by emailing a
> carrier's free "email-to-SMS" gateway address (e.g. `[number]@txt.att.net`), a mechanism most major US carriers have
> now shut down or are actively winding down due to spam abuse. Before depending on this for anything operationally
> important (alerting, monitoring, incident response), see the status table below and consider using the `rest post`
> based notification pattern documented in [Notification Services](../07-%20CLI/08-%20Notifications.md) instead
> (Telegram, Pushover, Slack, or a dedicated SMS API such as Twilio) — those go through a real, maintained API rather
> than a side-channel carriers are actively closing.

Usage:
```anylog
sms to [receiver phone] where gateway = [sms gateway] and subject = [message subject] and message = [message text]
```
**Command Options**:

| Option        | Explanation  | Default  |
| ------------- | ------------| ---- |
| receiver phone | The destination phone number | |
| gateway | [The SMS carrier gateway](https://en.wikipedia.org/wiki/SMS_gateway) |  |
| message subject | Any text | AnyLog Alert |
| message text | Any text | AnyLog Network Alert from Node: [node name] |

Example with T-Mobile as a carrier (see status note below — **this gateway no longer works**):
```anylog
sms to 4155550123 where gateway = tmomail.net
```

#### Carrier gateway status (as of 2026)

Gateway addresses for the major USA carriers, along with their current known status. Verify independently before
depending on any of these — this space has been changing quickly and carriers have shut gateways down with no notice.

| Carrier        | Gateway  | Status (2026) |
| ------------- | ------------| --- |
| AT&T | txt.att.net | **Dead** — shut down June 17, 2025 |
| Sprint | messaging.sprintpcs.com | **Dead** — shut down 2022; carrier absorbed into T-Mobile |
| T-Mobile | tmomail.net | **Dead** — stopped working by December 2024 |
| Verizon | vtext.com | **Degrading** — increasingly unreliable, full shutdown announced for March 2027 |
| Boost Mobile | myboostmobile.com | **Dead** — no longer delivering |
| Metro PCS | mymetropcs.com | **Likely dead** — Metro PCS has been a T-Mobile-owned brand since 2013 |
| Tracfone | mmst5.tracfone.com | **Unreliable** — rides on whichever underlying network (AT&T/T-Mobile/Verizon) the plan uses |
| U.S. Cellular | email.uscc.net | **Reportedly still working**, but U.S. Cellular's wireless business was acquired by T-Mobile in August 2025 — treat as at-risk |
| Virgin Mobile | vmobl.com | **Dead** — Virgin Mobile USA is defunct; folded into Boost, whose new owner (Dish) shut the gateway down |

For a currently-maintained list and more background on why these are disappearing, see
[this 2026 overview of email-to-SMS gateways](https://20somethingfinance.com/how-to-send-text-messages-sms-via-email-for-free/).