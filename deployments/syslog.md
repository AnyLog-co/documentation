# Syslog with AnyLog 

Syslog is a standardized protocol used for sending and receiving log messages in a computer network. It facilitates the 
collection and centralization of system logs from various devices and applications for monitoring, analysis, and 
troubleshooting.

Given its importance to manage your system, AnyLog allows to gather this information (using rsyslog), then querying it in 
the same manner as other time-series data. This allows to better manage the status of machine(s) more easily and from a 
single point; as opposed to manually acess each machine separately.

## Prepare Physical Machine
The following provides directions for using [_rsyslog_](https://www.rsyslog.com/). The same directions can be applied to
[syslg-ng](https://www.syslog-ng.com/) if prefered. 

1. Install rsyslog
```shell
sudo apt-get -y update
sudo apt -y install rsyslog
sudo service rsyslog start
```

2. validate _rsyslog_ is running
```shell
root@localhost:~# tail -f /var/log/syslog
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
``` 

## Prepare AnyLog 
1. Make sure the message broker is running either via configurations / policy or manually (as shown)
```anylog
<run message broker where
    external_ip=!external_ip and external_port=!anylog_broker_port and
    internal_ip=!ip and internal_port=!anylog_broker_port and
    bind=!broker_bind and threads=!broker_threads>
```

2. Due to the quantity of data coming in via syslog, we recommend partitioning and cleaning it automatically.
(This step should be done on operator node)
```anylog 
partition !default_dbms syslog using !partition_column by !partition_interval
schedule time=12 hours and name="Drop Partition Sync - Syslog" task drop partition where dbms=!default_dbms and table=syslog and keep=3
```

## Connect between syslog & AnyLog 
1. At the bottom of `/etc/rsyslog.conf` add the following lines
   * DESTINATION_IP - AnyLog _Operator_ or _Publisher_ IP address associated with the Message Broker
   * DESTINATION_PORT - AnyLog _Operator_ or _Publisher_ port address associated with the Message Broker
```editorconfig
$template remote-incoming-logs, "/var/log/remote/%HOSTNAME%.log"
*.* ?remote-incoming-logs
*.* action(type="omfwd" target="{DESTINATION_IP}" port="{DESTINATION_PORT}" protocol="tcp")
```

2. Restart _rsyslog_
```shell
sudo service rsyslog restart
```

3. Set configurations message rule to accept syslog data
```anylog
set msg rule syslog_rule if ip = !ip then dbms = !default_dbms and table = syslog and syslog = true
```

## Test rsyslog
1. Execute update / upgrade against the node 
```shell 
sudo apt-get -y update
sudo apt-get -y upgrade 
```

2. On the AnyLog instance that's accepting syslog, users should see data coming in   
```anylog
AL anylog-operator +> get msg rules 

Name        IF            IF    IF      THEN        THEN   THEN    THEN   THEN       Batches Events Errors Error Msg 
            Source IP     Port  Header  DBMS        Table  SysLog  Topic  Structure                                  
-----------|-------------|-----|-------|-----------|------|-------|------|----------|-------|------|------|---------|
syslog_rule|172.105.4.104|*    |       |new_company|syslog|True   |      |          |     18|    32|     0|         |
```

3. Through the query node, users can query the data 
```anylog 
# row count 
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
```

  