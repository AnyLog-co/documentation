# Managing SysLog data with AnyLog

## SysLog Formats

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


## Configure the AnyLog SysLog service

Users can configure an AnyLog node to host SysLog messages. The process requires the following:
* Set a rule to accept SysLog messages (see details below).
* Configure the SysLog output protocol to use TCP.
* Direct the output to the Messaging Service of the target AnyLog Node 
  
Notes: 
1) Use the command **get connections** to identify the Messaging IP and Port on the Message Service in the AnyLog Node.
2) Use the command [run message broker](background%20processes.md#message-broker) to configure a message broker service.


## Setting a rule to accept SysLog data

The following rule accepts SysLog data from one or multiple nodes:

```anylog
set msg rule [rule name] if ip = [IP address] and port = [port] and header = [header text] then dbms = [dbms name] and table = [table name] and syslog = [true/false] and format = [data format]
```

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

## Examples:

Example 1 - setting a rule to allow syslog data in BSD format from IP 10.0.0.78 and port 1468.
```anylog
 set msg rule my_rule if ip = 10.0.0.78 and port = 1468 then dbms = test and table = syslog and syslog = true
``` 

Example 2 -

**Part A** below is a script that takes log entries from the systemd journal that are newer than the time specified in the NOW variable, 
formats each entry by prefixing it with a specific string, and then sends these formatted entries to a remote server at 
the specified IP address and port number.   

Linux Example:
```shell
   journalctl --since "${NOW}" | awk '{print "al.sl.header.new_company.syslog", $0}' | nc -w 1 73.202.142.172 7850
```
Mac Example:
```shell
(log show --info --start '2023-11-30 16:50:00' --end '2023-12-01 16:51:00' | awk '{print "al.sl.header.test.syslog", $0}') | nc -w 1 10.0.0.78 7850
```

This script will deliver syslog entries to an Operator Node where every entry is prefixed by the string **al.sl.header.new_company.syslog**.

**Part B** below is a rule on the Operator Node that assigns entries with the prefix **al.sl.header.new_company.syslog**
to table **syslog** in database **test**.  
Users can add additional rules to associate different syslog entries to different tables by the assigned prefix.  
Additional manipulation of the syslog data can be done using policies assigned to a specified topic.

```anylog
 set msg rule my_rule if ip = 139.162.126.241 and header = al.sl.header.new_company.syslog then dbms = test and table = syslog and syslog = true
``` 

## Get the list of rules

The following command retrieves the list of rules:

```anylog
 get msg rules
```

## Remove a rule

The following command removes a rule from the list of rules:

```anylog
 reset  msg rule [rule name]
```

Example:
```anylog
 reset  msg rule my_rule
```