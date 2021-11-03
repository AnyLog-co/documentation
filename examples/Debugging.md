# Debugging

Debugging details different processes as they accrue and monitor processes that are not executing properly

## Monitor REST calls on the AnyLog CLI

By enabling trace on the command line, it is possible to trace the commands executed and the incoming data.
Command details will be displayed on stdout and depending on the trace level.

<pre>
trace level = N  run rest server
</pre>

N designates the trace level.

Examples:

| Trace Level   | Printout | Example |
| ------------- | ------------- |   ---------- |
|1 | Print message source info |  10.0.0.78 - - [02/Nov/2021 18:40:08] "GET / HTTP/1.1" 200 - |
|2 | Print command execution info |  10.0.0.78 - - [02/Nov/2021 18:40:08] "GET / HTTP/1.1" 200 - |
|  |                              |  10.0.0.78 - - [get status] [Success] |
|3 | Add header and body info     |  Detailed info on the message headers and body |


## The REST Log

A special log contain the rest calls.  
By default, a REST call that failes updates the ***REST log***.  
The following command returns the data at the log:

<pre>
get rest log
</pre>

Users can direct every call to the log (regardless if the call failed) using the following command:
<pre>
set rest log on
</pre>
And reverting to the default behaviour using the following command:
<pre>
set rest log off
</pre>