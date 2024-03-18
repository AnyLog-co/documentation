# System Notification 

AnyLog provides services like _REST_, _SMS_ and _STMP_ (eMail) in order allow your network to send notifications regarding 
the system; this can be things like CPU utilization, data not coming in or simply when ever a partition is being dropped / created.


## Setting up Webhooks

_Webhooks_ are user-defined _HTTP_ callbacks that enable real-time communication between web applications; they are the
simplest and fastest way to send messages into third-party applications as it simply uses a _REST_ (post) request as 
opposed to needing to develop a full application for messaging. 

This example creates a _Webhoook_ for _Slack_ messaging platform, but the same logic can be done for other messaging boards.

* [Slack](https://api.slack.com/messaging/webhooks)
* [Discord](https://docs.gitlab.com/ee/user/project/integrations/discord_notifications.html#create-webhook)
* [Microsoft Teams](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet)
* [Google Hangouts](https://developers.google.com/workspace/chat/quickstart/webhooks)


### Steps
1. Go https://api.slack.com/apps/ 
2. Under _Create_, Create an app from manifest 

| <img src="../imgs/notification_slack_your_app.png" height="75%" width="75%" /> | <img src="../imgs/notification_slack_manifest.png" height="75%" width="75%" /> | 
|:------------------------------------------------------------------------------:|:------------------------------------------------------------------------------:|

3. Select the preferred channel 

<img src="../imgs/notification_slack_workspace.png" height="50%" width="50%" />


4. Press continue / next till the end 

5. Select _Incoming Webhooks_

<img src="../imgs/notification_slack_webhook.png" height="50%" width="50%" />

6. Enable Webhooks

<img src="../imgs/notification_slack_enable_webhooks.png" height="50%" width="50%" />

7. At the bottom, add _Webbook_ to workspace

<img src="../imgs/notification_slack_create_webhook.png" height="50%" width="50%" />


8. Select which channel in Slack to send messages to 


<img src="../imgs/notification_slack_select_channel.png" height="50%" width="50%" />

9. When done you should see a _webhook_ (URL) - this will be used as part of your REST request in AnyLog

<img src="../imgs/notification_slack_webhook_generated.png" height="50%" width="50%" />


```URL
https://hooks.slack.com/services/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
```

