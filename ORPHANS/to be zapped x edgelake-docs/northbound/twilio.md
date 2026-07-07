---
layout: default
parent: Northbound
title: Twilo (Email & SMS) 
nav_order: 5
---
# Twilio  - Email and SMS Notifications
EdgeLake includes a rule engine that can be configured to execute periodic tasks and monitor and alert using services 
like REST, SMS and STMP (eMail). For example, users can be alerted on CPU, Network, RAM, Disk utilization and data 
ingestion.

Twilio is  cloud communications platform that enables developers to integrate various communication channels such as voice, 
messaging, and video into their applications using APIs. EdgeLake is able to send data into Twilio using either _eMail_,
_SMS_ or _Webhooks_.

**Support URLs**
* <a href="https://github.com/AnyLog-co/documentation/blob/master/alerts%20and%20monitoring.md#alerts-and-monitoring" target="_blank">Alerts & Monitoring</a>
* <a href="https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#smtp-client" target="_blank">SMTP background process</a>
* [Webhook Support](notifciation.md)

**Twilio Support**
* <a href="https://www.twilio.com/docs/proxy/api/webhooks#example-webhook-payloads" target="_blank">Webhooks</a>
* <a href="https://www.twilio.com/docs/flex/admin-guide/setup/email/address-creation" target="_blank">Email</a>
* <a href="https://www.twilio.com/docs/phone-numbers" target="_blank">Twilio Phone Number</a>

## Email & SMS Notifications
The _SMTP_ client process facilitates sending eMail and SMS messages from EdgeLake to users.  

### Email Configurations
<ol start="1">
    <li>Disable less <a href="https://support.google.com/accounts/answer/6010255?hl=en&visit_id=638521804216877928-230827673&p=less-secure-apps&rd=1" target="_blank">secure apps</a></li>
    <li>Enable <i>SMTP service</i>
        <table style="border: none;">
    <tr>
        <td align="center"><h3>Configurations</h3></td>
        <td align="center"><h3>Command</h3></td>
    </tr>
    <tr>
        <td>
            <table border="1">
                <tr>
                    <td align="center"><b>Parameter</b></td>
                    <td align="center"><b>Details</b></td>
                    <td align="center"><b>Default</b></td>
                </tr>
                <tr>
                    <td>host name</td>
                    <td>The connection URL to the email server</td>
                    <td>smtp.gmail.com</td>
                </tr>
                <tr>
                    <td>port</td>
                    <td>The email server port to use</td>
                    <td></td>
                </tr>
                <tr>
                    <td>email</td>
                    <td>The sender email address</td>
                    <td></td>
                </tr>
                <tr>
                    <td>password</td>
                    <td>The sender email password</td>
                    <td></td>
                </tr>
                <tr>
                    <td>SSL</td>
                    <td>Using SMTP with secure connection</td>
                    <td><i>false</i></td>
                </tr>
            </table>
        </td>
        <td>
            <pre class="code-frame"><code class="language-anylog">&lt;run smtp client where 
    host = [optional host name] and 
    port = [opttional port] and 
    email = [email address] and 
    password = [email password] and 
    ssl = [true/false]&gt;</code></pre>
        </td>
    </tr>
</table>
    </li>
    <li>Sending message via Email
        <table style="border: none;">
    <tr>
        <td align="center"><h3>Configurations</h3></td>
        <td align="center"><h3>Command</h3></td>
    </tr>
    <tr>
        <td>
            <table border="1">
                <tr>
                    <td align="center"><b>Option</b></td>
                    <td align="center"><b>Explanation</b></td>
                    <td align="center"><b>Default</b></td>
                </tr>
                <tr>
                    <td>receiver email</td>
                    <td>The destination address</td>
                    <td></td>
                </tr>
                <tr>
                    <td>message subject</td>
                    <td>Any text</td>
                    <td>AnyLog Alert</td>
                </tr>
                <tr>
                    <td>message text</td>
                    <td>Any text</td>
                    <td>AnyLog Network Alert from Node: [node name]</td>
                </tr>
            </table>
        </td>
        <td>
            <pre class="code-frame"><code class="language-anylog">&lt;email to [receiver email] where 
    subject = [message subject] and
    message = [message text]&gt;</code></pre>
        </td>
    </tr>
</table>
    </li>
</ol>

<h3>Most Common <i>SMTP</i> addresses</h3>
<table>
    <thead>
        <tr>
            <td align="center"><b>SMTP Provider</b></td>
            <td align="center"><b>URL</b></td>
            <td align="center"><b>SMTP Settings</b></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>AOL</td>
            <td>aol.com</td>
            <td>smtp.aol.com</td>
        </tr>
        <tr>
            <td>AT&T</td>
            <td>att.net</td>
            <td>smtp.mail.att.net</td>
        </tr>
        <tr>
            <td>Comcast</td>
            <td>comcast.net</td>
            <td>smtp.comcast.net</td>
        </tr>
        <tr>
            <td>iCloud</td>
            <td>icloud.com/mail</td>
            <td>smtp.mail.me.com</td>
        </tr>
        <tr>
            <td>Gmail</td>
            <td>gmail.com</td>
            <td>smtp.gmail.com</td>
        </tr>
        <tr>
            <td>Outlook</td>
            <td>outlook.com</td>
            <td>smtp-mail.outlook.com</td>
        </tr>
        <tr>
            <td>Yahoo!</td>
            <td>mail.yahoo.com</td>
            <td>smtp.mail.yahoo.com</td>
        </tr>
    </tbody>
</table>

### SMS Notifications

1. Start <i><a href="#email-configurations">SMTP service</a></i>
<br/>
2. Sending SMS message
<table style="border: none;">
    <tr>
        <td align="center"><h3>Configurations</h3></td>
        <td align="center"><h3>Command</h3></td>
    </tr>
    <tr>
        <td>
            <table border="1">
                <tr>
                    <td align="center"><b>Option</b></td>
                    <td align="center"><b>Explanation</b></td>
                    <td align="center"><b>Default</b></td>
                </tr>
                <tr>
                    <td>receiver phone</td>
                    <td>The destination phone number</td>
                    <td></td>
                </tr>
                <tr>
                    <td>gateway</td>
                    <td><a href="#major-us-carriers">SMS carrier gateway</a></td>
                    <td></td>
                </tr>
                <tr>
                    <td>subject</td>
                    <td>message subject</td>
                    <td>AnyLog Alert</td>
                </tr>
                <tr>
                    <td>message</td>
                    <td>sms text content</td>
                    <td>AnyLog Network Alert from Node: [node name]</td>
                </tr>
            </table>
        </td>
        <td>
            <pre class="code-frame"><code class="language-anylog">&lt;sms to [receiver phone] where 
gateway = [sms gateway] and 
subject = [message subject] and 
message = [message text]&gt;</code></pre>
        </td>
        <td>
        </td>
    </tr>
</table>

<h3>Major US Carriers</h3> 

The major USA carriers and their <a href="https://en.wikipedia.org/wiki/SMS_gateway" target="_blank">gateways</a> are the following:

<table>
    <tr>
        <td align="center"><b>Carrier</b></td>
        <td align="center"><b>Gateway</b></td>
    </tr>
    <tr>
        <td>AT&T</td>
        <td>txt.att.net</td>
    </tr>
    <tr>
        <td>Sprint</td>
        <td>messaging.sprintpcs.com</td>
    </tr>
    <tr>
        <td>T-Mobile</td>
        <td>tmomail.net</td>
    </tr>
    <tr>
        <td>Verizon</td>
        <td>vtext.com</td>
    </tr>
    <tr>
        <td>Boost Mobile</td>
        <td>myboostmobile.com</td>
    </tr>
    <tr>
        <td>Metro PCS</td>
        <td>mymetropcs.com</td>
    </tr>
    <tr>
        <td>Tracfone</td>
        <td>mmst5.tracfone.com</td>
    </tr> 
</table>
