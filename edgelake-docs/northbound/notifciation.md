---
layout: default
parent: Northbound
title: System Notification (Webhooks)
nav_order: 4
---
# System Notification 

EdgeLake includes a rule engine that can be configured to execute periodic tasks and monitor and alert
using services like _REST_, _SMS_ and _STMP_ (eMail).
For example, users can be alerted on CPU, Network, RAM, Disk utilization and data ingestion.  
Details on the Rule Engine is available in the section
[Alerts and Monitoring](https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring).

## Setting up Webhooks

_Webhooks_ are user-defined _HTTP_ callbacks that enable real-time communication between web applications; they are the
simplest and fastest way to send messages into third-party applications as these callbacks use _REST_ (POST) requests for messaging.

* [Slack](https://api.slack.com/messaging/webhooks)
* [Discord](https://docs.gitlab.com/ee/user/project/integrations/discord_notifications.html#create-webhook)
* [Microsoft Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet)
* [Google Hangouts](https://developers.google.com/workspace/chat/quickstart/webhooks)


### Steps
For demonstration purposes, this document uses _Slack_, however, the same logic can be applied with other webhooks.   

<ol start="1">
    <li>Go to <a href="https://api.slack.com/apps/" target="_blank">Slack Applications Sections</a> -- may require to login 
        / admin permissions
    </li>
    <br/>
    <li>Under _Create_, Create an app from manifest
        <table>
            <tr>
                <td align="center"><img src="../../../imgs/notification_slack_your_app.png" height="75%" width="75%" /></td>
                <td align="center"><img src="../../../imgs/notification_slack_manifest.png" height="75%" width="75%" /></td>
            </tr>
        </table>
    </li>
    <br/>
    <li>Select the preferred channel
        <div class="image-frame"><img src="../../../imgs/notification_slack_workspace.png" /></div>
    </li>
    <br/>
    <li>Press continue / next till the end</li>
    <li>Select <i>Incoming Webhooks</i>
        <div class="image-frame"><img src="../../../imgs/notification_slack_webhook.png" /></div>
    </li>
    <br/>
    <li>Enable Webhooks
        <div class="image-frame"><img src="../../../imgs/notification_slack_enable_webhooks.png" /></div>
    </li>
    <br/>
    <li>At the bottom, add <i>Webbooks</i> to workspace
        <div class="image-frame"><img src="../../../imgs/notification_slack_create_webhook.png" /></div>
    </li>
    <br/>
    <li>Select which channel in Slack to send messages to
        <div class="image-frame"><img src="../../../imgs/notification_slack_select_channel.png" /></div>
    </li>
    <br/>
    <li>When done you should see a <i>Webhook</i> (URL) - this will be used as part of your REST request in EdgeLake
        <div class="image-frame"><img src="../../../imgs/notification_slack_webhook_generated.png" /></div>
    </li>
</ol>

**Generated URL**: 
<pre class="code-frame"><code class="language-shell">https://hooks.slack.com/services/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</code></pre>


## Send Notifications via EdgeLake

EdgeLake allows to send cURL requests the 
<a href="https://github.com/AnyLog-co/documentation/blob/master/anylog%20commands.md#rest-command" target="_blank"><i>rest</i> command</a>. 
Since _Webhooks_ are essentially URLs embedded with messages, below is a _rest_ command that sends notifications from EdgeLake into Slack.

<ol start="1">
    <li>Create webhook URL as a variables
        <pre class="code-frame"><code class="language-anylog">webhook_url = "https://hooks.slack.com/services/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"</code></pre>
    </li>
    <br/>
    <li>get percentage of CPU used and current timestamp
        <pre class="code-frame"><code class="language-anylog">cpu_percent = get node info cpu_percent
date_time = python "datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')"</code></pre>
    </li>
    <br/>
    <li>Create payload
        <pre class="code-frame"><code class="language-anylog">text_msg = !date_time + "  CPU usage: " + !cpu_percent 
payload = json {"text": !text_msg}</code></pre>
    </li>
    <br/>
    <li>Publish information to Slack via _REST_
        <pre class="code-frame"><code class="language-anylog">&lt;rest post where 
    url = !webhook_url and 
    body = !payload and 
    headers = "{'Content-Type': 'application/json'}"&gt;</code></pre>
    <br/>
    <b>Note</b>: <i>Google Hangouts</i>, <i>Discord</i> and <i>Microsoft Teams</i> use <code>content</code> for the <i>payload</i> key as opposed to <code>text</code>.
    </li>
</ol>


Once sent, an output would appear in the proper Slack channel
<div class="image-frame"><img src="../../../imgs/notification_slack_messsage.png"  height="50%" width="50%" /></div>


