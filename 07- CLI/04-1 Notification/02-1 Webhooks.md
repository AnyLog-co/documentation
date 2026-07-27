---
title: Webhooks
description: "Setting up and sending notifications via webhooks (Slack, Discord, Microsoft Teams, Google Chat) — an extension of the raw REST call pattern."
layout: page
visibility: public
version: open source
tags:
    - notification
    - northbound
    - rest
---
<!---
### 📜 Change Log
 **Date**   | **Name**       | **Change** | **Version** |
 |------------|----------------|------------|----------|
 | 2026-07-27 | Ori Shadmon    | Fixed broken rest-command link (stray `>` + stale path), genericized reused Slack workspace/webhook IDs, renamed "Google Hangouts" to "Google Chat" (Hangouts shut down in 2022), fixed typo, aligned headers quoting style | |
 | 2026-07-20 | Eric Aquaronne | added change log | 2.0.2606 |
 | 2026-07-07 |  | Merged with legacy Notifications.md; added Automating Notifications with Scripts section |  |
 | 2026-04-17 |  | created document |  |
--->

# Webhooks

Webhooks are an extension of the [raw REST call](02-%20REST.md#rest-calls) pattern — instead of you constructing the
target URL/body yourself for a general REST/Telegram/Pushover endpoint, the destination service (Slack, Discord,
Microsoft Teams, Google Chat) hands you a pre-built URL that you `rest post` to directly.

## Setting up Webhooks

_Webhooks_ are user-defined _HTTP_ callbacks that enable real-time communication between web applications; they are the
simplest and fastest way to send messages into third-party applications as it simply uses a _REST_ (post) request as
opposed to needing to develop a full application for messaging.

* <a href="https://api.slack.com/messaging/webhooks" target="_blank">Slack</a>
* <a href="https://core.telegram.org/bots/api" target="_blank">Telegram</a>
* <a href="https://pushover.net/api" target="_blank">Pushover</a>
* <a href="https://docs.gitlab.com/ee/user/project/integrations/discord_notifications.html#create-webhook" target="_blank">Discord</a>
* <a href="https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet" target="_blank">Microsoft Teams</a>
* <a href="https://developers.google.com/workspace/chat/quickstart/webhooks" target="_blank">Google Chat</a>


### Steps
<ol>
  <li>
    Go to <a href="https://api.slack.com/apps/" target="_blank">https://api.slack.com/apps/</a>.
  </li>
  <li>
    Under <i>Create</i>, create an app from manifest.
    <table>
      <tr>
        <td align="center"><img src="../../imgs/notification_slack_your_app.png" height="75%" width="75%" /></td>
        <td align="center"><img src="../../imgs/notification_slack_manifest.png" height="75%" width="75%" /></td>
      </tr>
    </table>
  </li>
  <li>
    Select the preferred channel.
    <br />
    <img src="../../imgs/notification_slack_workspace.png" height="50%" width="50%" />
  </li>
  <li>Press continue / next till the end.</li>
  <li>
    Select <i>Incoming Webhooks</i>.
    <br />
    <img src="../../imgs/notification_slack_webhook.png" height="50%" width="50%" />
  </li>
  <li>
    Enable Webhooks.
    <br />
    <img src="../../imgs/notification_slack_enable_webhooks.png" height="50%" width="50%" />
  </li>
  <li>
    At the bottom, add <i>Webhook</i> to the workspace.
    <br />
    <img src="../../imgs/notification_slack_create_webhook.png" height="50%" width="50%" />
  </li>
  <li>
    Select which channel in Slack to send messages to.
    <br />
    <img src="../../imgs/notification_slack_select_channel.png" height="50%" width="50%" />
  </li>
  <li>
    When done, you should see a <i>webhook</i> URL. This will be used as part of your REST request in AnyLog.
    <br />
    <img src="../../imgs/notification_slack_webhook_generated.png" height="50%" width="50%" />
  </li>
</ol>


**Generated URL** (example format — yours will have your own workspace and webhook IDs):
```URL
https://hooks.slack.com/services/[team_id]/[webhook_id]/[token]
```

## Send Notifications via AnyLog

### Slack Webhooks
AnyLog allows sending cURL requests via the [_rest_ command](02-%20REST.md#rest-calls). Since _Webhooks_ are
essentially URLs to send messages into a system, we'll be using the _rest_ command to send notifications from AnyLog into
Slack.

1. Create webhook URL as a variable
```anylog
webhook_url = "https://hooks.slack.com/services/[team_id]/[webhook_id]/[token]"
```

2. get percentage of CPU used and current timestamp
```anylog
cpu_percent = get node info cpu_percent
date_time = python "datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')"
```

3. Create payload
```anylog
text_msg = !date_time + "  CPU usage: " + !cpu_percent
payload = json {"text": !text_msg}
```

4. Publish information to Slack via _REST_
```anylog
rest post where url = !webhook_url and body = !payload and headers = {"Content-Type": "application/json"}
```

Once sent, an output would appear in the proper Slack channel

<img src="../../imgs/notification_slack_messsage.png"  height="50%" width="50%" />

**Note**: _Google Chat_, _Discord_ and _Microsoft Teams_ use `content` for the _payload_ key as opposed to `text`.