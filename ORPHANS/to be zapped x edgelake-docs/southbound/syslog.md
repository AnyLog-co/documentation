---
layout: default
title: Syslog
parent: Southbound
nav_order: 6
---
# Syslog 
Syslog is a standardized protocol used for sending and receiving log messages in a computer network. It facilitates the 
collection and centralization of system logs from various devices and applications for monitoring, analysis, and 
troubleshooting.

Given its importance to manage any system, EdgeLake allows to gather this information (using rsyslog), then querying it 
in the same manner as other time-series data. This allows to better manage the status of machine(s) more easily and from 
a single point; as opposed to manually acess each machine separately.

## Syslog Formats 
SysLog is delivered from each machine in one of 2 formats:
* The traditional BSD (Berkeley Software Distribution) format, specified in RFC 3164.
* The newer IETF (Internet Engineering Task Force) format, specified in RFC 5424.


### BSD format includes the following attributes:
1. **Priority**: Enclosed in angle brackets (< and >). It's a numeric value that combines the facility and severity (e.g., <34>).
2. **Timestamp**: Immediately follows the priority. It's typically in the format MMM dd hh:mm:ss (e.g., Jan 12 23:34:56).
3. **Hostname or IP Address**: Follows the timestamp. It's the name or IP address of the device that sent the message.
4. **Tag**: Often a process name or application identifier, potentially followed by a process ID in square brackets (e.g., sshd[3268]).
5. **Message**: The actual log message text, following the tag.


### IETF Format
1. **Priority**: Similar to the BSD format, enclosed in angle brackets.
2. **Version**: A single digit indicating the syslog protocol version (e.g., 1).
3. **Timestamp**: More precise than BSD format, often in the ISO 8601 format.
4. **Hostname**: As in BSD format.
5. **Application**: The name of the application or process generating the message.
6. **Process ID (PID)**: The PID of the process.
7. **Message ID**: A unique identifier for the type of message.
8. **Structured Data**: Enclosed in square brackets, containing key-value pairs for additional data.
9. **Message**: The actual log message text.

## Setting up Syslog & EdgeLake
### On the Machine Side
The following provides directions for using [rsyslog](https://www.rsyslog.com/). The same directions can be applied to 
[syslg-ng](https://www.syslog-ng.com/) if preferred.

<ol start="1">
<li>Install rsyslog
<pre class="code-frame"><code class="language-shell">sudo apt-get -y update
sudo apt -y install rsyslog
sudo service rsyslog start
</code></pre></li>
<li>Validate rsyslog is running
<pre class="code-frame"><code class="language-shell">root@localhost:~# tail -f /var/log/syslog
Feb 25 02:55:47 localhost systemd[31139]: Reached target Basic System.
Feb 25 02:55:47 localhost systemd[1]: Started User Manager for UID 0.
Feb 25 02:55:47 localhost systemd[1]: Started Session 197 of User root.
Feb 25 02:55:47 localhost systemd[31139]: Reached target Main User Target.
Feb 25 02:55:47 localhost systemd[31139]: Startup finished in 160ms.
Feb 25 02:55:52 localhost systemd-udevd[400]: Network interface NamePolicy= disabled on kernel command line, ignoring.
Feb 25 02:55:53 localhost systemd[31139]: Started D-Bus User Message Bus.
Feb 25 02:55:53 localhost dbus-daemon[31261]: [session uid=0 pid=31261] AppArmor D-Bus mediation is enabled
Feb 25 02:55:53 localhost systemd[31139]: Started snap.docker.docker-6d2688ea-6061-49f4-bb62-b2bbe1e1d054.scope.
Feb 25 02:55:54 localhost systemd[31139]: Started snap.docker.docker-0c97bdf4-f93e-440f-9034-4a41e5ff56d0.scope.
...
</code></pre></li></ol>

### On EdgeLake Side
<ol start="3">
<li>Make sure the message broker is running either via configurations / policy or manually (as shown)
<pre class="code-frame"><code class="language-anylog">&lt;run message broker where
    external_ip=!external_ip and external_port=!anylog_broker_port and
    internal_ip=!ip and internal_port=!anylog_broker_port and
    bind=!broker_bind and threads=!broker_threads&gt;
</code></pre></li>
<li>Due to the quantity of data coming in via syslog, we recommend partitioning and cleaning it automatically. 
(This step should be done on operator node)
<pre class="code-frame"><code class="language-anylog">partition !default_dbms syslog using !partition_column by !partition_interval
schedule time=12 hours and name="Drop Partition Sync - Syslog" task drop partition where dbms=!default_dbms and table=syslog and keep=3
</code></pre></li>
</ol>

## Connect between Syslog & EdgeLake
### Syslog rule engine on EdgeLake
The following rule accepts Syslog data from one or multiple nodes:
<pre class="code-frame"><code class="language-anylog">&lt;set msg rule [rule name] if 
    ip = [IP address] and port = [port] and 
    header = [header text] then dbms = [dbms name] and table = [table name] and 
    syslog = [true/false] and format = [data format] and topic = [topic name]&gt; 
</code></pre>

The following chart summarizes the command options:

| Option           | Mandatory |  Details |
| ---------------- | ---------  | -------------------------- | 
| Rule Name        | Y          | A unique name that identifies the rule. |
| IP               | N          | A source IP that is assigned to the rule. If IP is not provided, the rule will apply to messages from every source IP. |
| Port             | N          | A source port that is assigned to the rule. If port is not provided, the rule will apply to all ports of from source IPs. |
| Header           | N          | Assign the rules to messages with a specified header. Note: headers can be added using one of the syslog redirecting tools (see example below). |
| DBMS             | Y          | A database name that will host the syslog data. Use the command ```get databases``` to see that the database is enabled on the operator node. |
| Table            | Y          | A table name to host the syslog data on the node. |
| syslog           | N          | A True/False value to indicate syslog data. Unless format is specified, the destination structure represents the BSD format of syslog.  |
| format           | N          | A different format than BSD.  |
| topic            | N          | A topic to assign to the syslog data. Data that is assigned to a topic is treated like MQTT data and can be manipulated using a policy. |
| structure        | N          | If the value is assigned is **included**, the structure of the data is provided by the first event. See example 3 below.  |


**Note**: 
1. If syslog option is enabled, column names are pre-determined (by default as BSD or with format = IETF). If syslog 
option is not enabled, structure needs to detail the structure of the source data.
2. For SysLog data stream, enable CR and LF to end of message.
3. <code class="language-anylog">structure = included</code> designates that the first event describes the structure.
Examples:

### Deployment Steps
<ol start="1"> 
<li>On EdgeLake side - Set configurations message rule to accept syslog data
<pre class="code-frame"><code class="language-anylog">set msg rule syslog_rule if ip = !ip then dbms = !default_dbms and table = syslog and syslog = true</code></pre></li>
<li>At the bottom of <code class="language-shell">/etc/rsyslog.conf</code> add the following lines
    <ul style="padding-left: 20px;">
        <li><code class="language-config">DESTINATION_IP</code> - EdgeLake Operator or Publisher IP address associated with the Message Broker</li>
        <li><code class="language-shell">DESTINATION_PORT</code> - EdgeLake Operator or Publisher port address associated with the Message Broker</li>
    </ul>
    <pre class="code-frame"><code class="language-config">...
$template remote-incoming-logs, "/var/log/remote/%HOSTNAME%.log"
*.* ?remote-incoming-logs
*.* action(type="omfwd" target="{DESTINATION_IP}" port="{DESTINATION_PORT}" protocol="tcp")
</code></pre></li>
<li>Restart rsyslog
    <pre class="code-frame"><code class="language-shell">sudo service rsyslog restart</code></pre></li>
</ol> 

## Test & Querying syslog 
<ol start="1">
<li>Execute update / upgrade against the node
<pre class="code-frame"><code class="language-shell">sudo apt-get -y update
sudo apt-get -y upgrade</code></pre></li>
<li>On the EdgeLake instance that's accepting syslog, users should see data coming in
<pre class="code-frame"><code class="language-anylog">AL anylog-operator +&gt; get msg rules

Name        IF            IF    IF      THEN        THEN   THEN    THEN   THEN       Batches Events Errors Error Msg 
            Source IP     Port  Header  DBMS        Table  SysLog  Topic  Structure                                  
-----------|-------------|-----|-------|-----------|------|-------|------|----------|-------|------|------|---------|
syslog_rule|172.105.4.104|*    |       |new_company|syslog|True   |      |          |     18|    32|     0|         |
</code></pre></li>
<li>Through the query node, users can query the data
<pre class="code-frame"><code class="language-anylog"># row count 
AL anylog-query +> run client () sql new_company format=table "select count(*) from syslog" 
[8]
AL anylog-query +> 
count(*)
-------- 
      75 

{"Statistics":[{"Count": 1,
                "Time":"00:00:00",
                "Nodes": 1}]}
                

# sample data
AL anylog-query +> run client () sql new_company "select * from syslog limit 10"             
[10]
AL anylog-query +> 
{"Query":[{"row_id":1,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":38,
          "timestamp":"2024-02-25 03:17:27.000000",
          "hostname":"localhost",
          "tag":"sshd[32839]:",
          "message":"Invalid user lighthouse from 78.47.129.226 port 45126"},
          {"row_id":2,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":85,
          "timestamp":"2024-02-25 03:17:27.000000",
          "hostname":"localhost",
          "tag":"sshd[32839]:",
          "message":"pam_unix(sshd:auth): check pass; user unknown"},
          {"row_id":3,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":85,
          "timestamp":"2024-02-25 03:17:27.000000",
          "hostname":"localhost",
          "tag":"sshd[32839]:",
          "message":"pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tt
                    y=ssh ruser= rhost=78.47.129.226 "},
          {"row_id":4,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":38,
          "timestamp":"2024-02-25 03:17:29.000000",
          "hostname":"localhost",
          "tag":"sshd[32839]:",
          "message":"Failed password for invalid user lighthouse from 78.47.129.226 port 4
                    5126 ssh2"},
          {"row_id":5,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":38,
          "timestamp":"2024-02-25 03:17:29.000000",
          "hostname":"localhost",
          "tag":"sshd[32839]:",
          "message":"Received disconnect from 78.47.129.226 port 45126:11: Bye Bye [preaut
                    h]"},
          {"row_id":6,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":38,
          "timestamp":"2024-02-25 03:17:29.000000",
          "hostname":"localhost",
          "tag":"sshd[32839]:",
          "message":"Disconnected from invalid user lighthouse 78.47.129.226 port 45126 [p
                    reauth]"},
          {"row_id":7,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":85,
          "timestamp":"2024-02-25 03:17:31.000000",
          "hostname":"localhost",
          "tag":"sshd[32841]:",
          "message":"pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tt
                    y=ssh ruser= rhost=218.92.0.112  user=root"},
          {"row_id":8,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":85,
          "timestamp":"2024-02-25 03:17:32.000000",
          "hostname":"localhost",
          "tag":"sshd[32843]:",
          "message":"pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tt
                    y=ssh ruser= rhost=5.42.80.189  user=root"},
          {"row_id":9,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":38,
          "timestamp":"2024-02-25 03:17:33.000000",
          "hostname":"localhost",
          "tag":"sshd[32841]:",
          "message":"Failed password for root from 218.92.0.112 port 52045 ssh2"},
          {"row_id":10,
          "insert_timestamp":"2024-02-25 03:18:35.023262",
          "tsd_name":"131",
          "tsd_id":4610,
          "priority":38,
          "timestamp":"2024-02-25 03:17:34.000000",
          "hostname":"localhost",
          "tag":"sshd[32843]:",
          "message":"Failed password for root from 5.42.80.189 port 59486 ssh2"}],
"Statistics":[{"Count": 10,
                "Time":"00:00:00",
                "Nodes": 1}]}
</code></pre></li>
</ol>








