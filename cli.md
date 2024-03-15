# The AnyLog CLI

## Overview

Each node offers a Command Line Interface (CLI). The  CLI allows users to interact with the program via the command line or terminal. 
The CLI is a text-based interface where users can enter commands to execute various functions or operations on the AnyLog node or peer nodes.

Notes: 
1. If AnyLog is executed as a background process, the CLI functionality is disabled. See details in 
[Deploy AnyLog as a background process](training/advanced/background%20deployment.md) section.
   
2. Most commans can be executed using the Remote CLI, details are available in the 
   [Remote CLI](northbound%20connectors/remote_cli.md) section.
   

## The command prompt
The node's CLI includes a prompt and by default is as follows:
```anylog 
AL >
```
Users can change the node name using the command **set node name** to associate a node with a unique name.  
The node name extends the CLI prompt. For example the following command changes the prompt:
```anylog 
AL >  set node name Operator_3
AL Operator_3 >
```
Details are available [here](anylog%20commands.md#set-node-name).

A prompt extended by a plus (+) sign indicates a message in the buffer queue.
For example:
```anylog 
AL +>
```
Retrieve the message using the following command:
```anylog 
get echo queue
```

## Executing commands on startup

AnyLog commands can be executed on startup by placing the commands as command line arguments.  
Note: command line arguments are contained in quotations and the keyword **and** separates between multiple commands (see example below). 

Alternatively, commands can be placed in a file and using the command **process**, the commands in the file are executed.  
Details on the **process** command are available [here](node%20configuration.md#the-configuration-process).   
Note: Commands can be organized in policies and stored in the shared metadata. These commands are executed by calling the policies. 
Details are available in the [Configuration Policies](policies.md#configuration-policies) section.

In the following example, a file named *anylog_setup.al* contains the commands that configures the network services for TCP and REST.      
The commands in anylog_setup.al are as follows:
```anylog 
run tcp server where internal_ip = !ip and internal_port = 7848 and external_ip = !external_ip and external_port = 7848 and bind = false and threads = 6
run rest server where internal_ip = !ip and internal_port = 7849 and external_ip = !external_ip and external_port = 7849 and bind = false
```

The following call starts the node, executes the configuration commands contained in the *anylog_setup.al* file (placed in the scripts_dir folder)
and displays the IP and Port for the TCP and REST services. 
```anylog 
python3 anylog.py "process scripts_dir/anylog_setup.al" and "get connections"
```

## Executing commands on the local node and on peer nodes

By default, an AnyLog command is executed on the local node. Adding the keywords **run client** executes the command
on a target node or nodes.  
Note: **run client** means that the command is issued by a node that serves as a client to the network.  
The command output from the target nodes is returned and displayed on the node from which the command was issued.  
Examples:  
A command issued on the local node: 
```anylog 
get processes
```
A command issued on a target node:
```anylog 
run client 10.0.0.78:7848 get processes
```
A command issued on multiple nodes:
```anylog 
run client (10.0.0.78:7848, 10.0.0.25:2548) get processes
```
Additional information is in the following sections:
* [AnyLog Command Line Interface](getting%20started.md#anylog-command-line-interface)
* [Sending messages to peers in the network](getting%20started.md#sending-messages-to-peers-in-the-network)
* [Assigning a CLI to a peer node](training/advanced/background%20deployment.md#using-the-cli-of-a-peer-node-to-manage-the-background-node)


## Script commands

### The "if" command
Scripts can include conditional statements. Details are available in the [Conditional execution](anylog%20commands.md#conditional-execution) section.

### The "end script" command
The **end script** command terminates the execution of the script (see an example below)

### The "goto" command
Script sections can be labeled, and using the command **goto** followed by a label, the execution shifts to a different 
(labeled) part of the code. Labels are required to be at the start of a command line (in the  script) and enclosed by colons.

The following script demonstrates the usage of the **goto** command. In the example below, the **goto** command
transfers the execution to the section that satisfies a value set in an environment variable:
```anylog 
if $setup_type == query then goto query_node
else goto operator_node

:query_node:
connect dbms test where type = sqlite
end_script

:operator_node:
connect dbms sensor_data where type = psql and user = anylog and password = demo and ip = 127.0.0.1 and port = 5432
end_script
```
### The "set debug" command

If a script contains **set debug on**, each command that follows is printed including the execution result.
The command **set debug off** disables the printout.  
For example, if the anylog_setup.al containing the commands **run tcp server** and **run rest server** includes **set debug on**,
the execution output would be as follows:

```anylog 
AL > [] [0002] set debug on --> Success
AL > [] [0003] run tcp server where internal_ip = !ip and internal_port = 7848 and external_ip = !external_ip and external_port = 7848 and bind = false and threads = 6 --> Success
AL > [] [0004] run rest server where internal_ip = !ip and internal_port = 7849 and external_ip = !external_ip and external_port = 7849 and bind = false --> Success
```

## CLI operations

The CLI can operate on values maintained in the local dictionary.     
Details on the dictionary are available at [The "get dictionary" command](monitoring%20nodes.md#the-get-dictionary-command).

### The "incr" command

The **incr** command considers a variable as an integer and return the result of adding a specified value to the variable.    
If value is not specified, it is considered to be 1.  
In the example below, the value set in the variable **b** is 4:
```anylog 
a = 1
b = incr !a 3
```

### Using th "+" sign on the CLI

The plus sign concatenates dictionary strings.  
In the example below, the value set in the variable **c** is 1234:
```anylog 
a = 12
b = 34
c = !a + !b
```

## The "python" command

The **python** commands supports a subset of python operations. If a key from a dictionary is specified, it is replaced with its assigned value.    
Examples:
```anylog 
ip_port = python !ip + ':4028'
python 'D:/Node/AnyLog-Network/data/watch/'.rsplit('/',1)[0] + '.out'
new_dir = python !watch_dir.rsplit('/',1)[0] + '.out'
```
In the examples below, if the following values are set:
```anylog
a = 12
b = 45
```
And the following commands are executed,
```anylog
new_value1 = python !a.str + !b.str
new_value2 = python !a.int + !b.int
new_value3 = python !a.float + !b.float
```
The results are as follows:
```anylog
AL > !new_value1
'1245'
AL > !new_value2
'57'
AL > !new_value3
'57.0
```







