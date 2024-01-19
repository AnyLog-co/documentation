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
* Direct the output to the Messaging service of the target AnyLog Node 
  
Notes: 
1) Use the command **get connections** to identify the Messaging IP and Port on the AnyLog Node.
2) Use the command [run message broker](background%20processes.md#message-broker) to configure a message broker service.


## Setting a rule to accept SysLog data

The following rule accepts SysLog data from one or multiple nodes:

```anylog
set msg rule [rule name] if ip = [IP address] and port = [Pprt address] and offset = [header offset] and text = [header text] then dbms = [dbms name] and table = [table name] and json = [true/false]
```

Example:

```anylog
 set msg rule my_rule if ip = 10.0.0.78 and port = 1468 then dbms = test and table = syslog and syslog = true
``` 