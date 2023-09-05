# Deploy AnyLog as a background process 

AnyLog can be deployed as a backround process. In this type of deployment, the standard input is disabled and the 
the process includes the following:
* Configure the node from a script file or using a policy on the metadata.
* Enable the rest service and dynamically interact with the node using REST.

Users can interact with a node using the following:
* The remote CLI
* cURL, or any app that issues REST request
* Using the CLI of an AnyLog node which is not running in the background. 

This document explains how to deploy and manage an AnyLog instance as a background process.

## pip Install Package

Instructions are detailed in the [pip Install Document](Pip Install.md)

## Using a config file

The node is configured using a config file that is processed when the node starts.  
Below is an example of a config file:

```anylog 
# Enable the TCP service - allowing the node to be a member of the network (allow the node to receive messages from peer nodes)
run tcp server where internal_ip = !ip and internal_port = 20048 and external_ip = !external_ip and external_port = 20048 and bind = false and threads = 6

# Enable the REST service - allowing to communicate with 3rd parties apps using REST
run rest server where internal_ip = !ip and internal_port = 20049 and external_ip = !external_ip and external_port = 20049 and bind = false

set authentication off      # to dsable security
set echo queue on           # Redirecy messages to a buffer
get connections             # To print the network connections

set cli off                 # Disable the CLI
```   

# Running AnyLog in the background

Use the following command to deploy AnyLog in the background (Linux):
```anylog
 nohup python3 -u anylog.py process start.al &
```
Comments:

* **nohup** - Disassociates the command from the terminal so that it continues to run in the background.  
it redirects standard output (stdout) to a file called **nohup.out** (unless a different output file is specified).
* **-u** - Output to stdout is not buffered.
* **process start.al** The AnyLog command that executes the commands in the config file named **start.al** with the 
contents as in the [above example](#using-a-config-file).

# Disabling the CLI

The node CLI was disabled using the **set cli off** command in the [config script above](#using-a-config-file).

# View the output of the background process

The standard output (stdout) is redirected to a file called **nohup.out** in the folder with the python code (anylog.py).

The config file of the example includes the **get connections** command, showing in **nohup.out** the IP and Port of the TCP and REST services.

## Using the CLI of a peer node to manage the background node. 

The CLI of any node can be assigned to a different node and remotely interact with the node as a local CLI.  
**This process assumes propper permissions.**

The basic process is using the **run client (target)** directive that directs the command to a target node.
For example:
```anylog
 run client 198.74.50.131:32048 get inserts
```  
In the example above, **get inserts** is executed on the target node 198.74.50.131:32048.  

Users can assign a CLI to one or more target nodes as in the examples below:  

### Assigning a CLI to a peer node:
```anylog
 run client 198.74.50.131:32048
```  
The CLI prompt would be extended to show the peer node, and commands are executed on the peer node.  
Below is an example os issuing a command on an assigned peer:
```anylog
AL > 198.74.50.131:32048 >> get connections

[From Node 198.74.50.131:32048]

Type      External Address    Internal Address    Bind Address
---------|-------------------|-------------------|-------------------|
TCP      |198.74.50.131:32048|198.74.50.131:32048|198.74.50.131:32048|
REST     |198.74.50.131:32049|198.74.50.131:32049|0.0.0.0:32049      |
Messaging|Not declared       |Not declared       |Not declared       |
```  

When the CLI is assigned, prefix commands that are executed on the current node with a dot (**.**).  
Example:
```anylog
AL > 198.74.50.131:32048 >> . get connections
```
The command above is executed on the CLI node (and not assigned to the peer).

Note: a command that starts with **run client** is never assigned, it is always executed on the CLI node.

### Assigning a CLI to multiple peer nodes:

Users can assign a CLI to multiple peers. For example, the example below assigns the CLI to all the operator nodes:
 ```anylog
run client (blockchain get operator bring.ip_port)
```
A command issued will be executed on all the target nodes.

### Associating peer replies to a key in the dictionary

A reply from peers can be assigned to a key in the dictionary. 

The examples below assume an assigned CLI:

Example 1:
  ```anylog
current_status = get status
```
The reply from the target node is assigned to the dictionary key **current_status**.

Example 2:
  ```anylog
current_status[] = get status
```
The reply from target nodes is organized as a list and assigned to the key **current_status**.

Example 3:
  ```anylog
current_status[] = get status
```
The reply from target nodes is organized as a dictionary and assigned to the key **current_status**.


 
   

