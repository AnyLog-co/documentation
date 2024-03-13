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
Note: Commands can be placed and executed using policies hosted in the shared metadata. Details are available in the 
[Configuration Policies](policies.md#configuration-policies) section.

In the following example, a file named anylog_setup.al contains the commands that configures the network services for TCP and REST.    
anylog_setup.al is as follows:
```anylog 
run tcp server where internal_ip = !ip and internal_port = 7848 and external_ip = !external_ip and external_port = 7848 and bind = false and threads = 6
run rest server where internal_ip = !ip and internal_port = 7849 and external_ip = !external_ip and external_port = 7849 and bind = false
```

The following call starts the node, executes the configuration commands in the anylog_setup.al file (placed in the scripts_dir folder)
and displays the IP and Port for the TCP and REST services. 
```anylog 
python3 anylog.py "process scripts_dir/anylog_setup.al" and "get connections"
```

# Executing commands on the local node and on peer nodes

By default, an AnyLog command is executed on the local node. Adding the keywords **run client** executes the command
on a target node or nodes. 
Note: **run client** means that the command is issued by a node that serves as a client to the network.  
The command output from the target nodes is returned and displayed on the node from which the command was issued.  
Examples:  
A command issued on the current node: 
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
[AnyLog Command Line Interface](getting%20started.md#anylog-command-line-interface) and
[Sending messages to peers in the network](getting%20started.md#sending-messages-to-peers-in-the-network) and
[Assigning a CLI to a peer node](training/advanced/background%20deployment.md#using-the-cli-of-a-peer-node-to-manage-the-background-node).




