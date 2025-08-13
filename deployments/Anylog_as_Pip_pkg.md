# AnyLog as a _pip_ Package 

In scenarios where lightweight deployment, tight integration with Python-based applications, or limited system resources 
are primary concerns, utilizing AnyLog via its pip package offers a flexible and efficient alternative to containerized 
or service-based setups. This approach is particularly valuable for developers building edge applications, prototyping 
data pipelines, or embedding data management directly within Python scripts. By installing AnyLog as a pip package, 
users can seamlessly run a local node, interact with data using familiar Python tools, and avoid the overhead and 
complexity of Docker orchestration—making it ideal for development environments, automation scripts, and constrained IoT 
devices.

* [Requirements](#requirements)
* [Deploying AnyLog](#deploying-anylog-as-a-service)

--- 

## Requirements

* Request a trial license via <a href="https://anylog.network/download" target="_blank">Download Page</a>
* Software Requirements 
    * Relational database - either _SQLite_ (built-in) or _PostgresSQL_
    * BLobs database (if images / data files) - either File-store (built-in) or MongoDB
    * Python3.9 or higher
      * Python pip packages can be found in [Quick Start](../quick_start.md#requirements)
* Hardware Requirements 

|                                               |                                                  Requirements                                                   | 
|:---------------------------------------------:|:---------------------------------------------------------------------------------------------------------------:| 
| Operating System |                            Ideally Linux-based, but also support Mac OSX and Windows                            |
|                      RAM                      |                                                  2 GB or more                                                   | 
|                      CPU                      |                                    2 or more - both arm64 and am64 supported                                    |
| Image Size |              AnyLog / EdgeLake is less than 150MB - everything else is either pip package or data               | 
|                  Networking                   | Network connectivity between machines in cluster<br/><br/>Unique hostname / MAC address for every physical node | 


--- 

## Deploying AnyLog as a Service

1.  Install AnyLog as a `pip` package

```shell
# Ubuntu
python3 -m pip install --upgrade http://45.33.11.32/ubuntu/anylog_network-0.0.7-cp310-cp310-linux_x86_64.whl 

# Alpine
python3 -m pip install --upgrade http://45.33.11.32/alpine/anylog_network-0.0.7-cp311-cp311-linux_x86_64.whl 

# Mac OSX  
python3 -m pip install --upgrade http://45.33.11.32/macosx/anylog_network-0.0.7-cp310-cp310-macosx_12_0_x86_64.whl
```

2. Sample Python3 Script to deploy AnyLog
```python
import sys
import anylog_node.cmd.user_cmd as user_cmd  # import AnyLog Node 

argv = sys.argv
argc = len(argv)

user_input = user_cmd.UserInput()
user_input.process_input(arguments=argc, arguments_list=argv) # Start AnyLog with CLI
```

3. Enable AnyLog  
```anylog
set license where activation_key=XXX
```
