# Network Configuration

The following provides general information regarding how an AnyLog nodes communicates with other members in the network, 
as well as third-party applications.

Information regarding configuring _NGINX_ and/or an overlay network (_nebula_) can be found [here](deployments/Networking & Security) 

## Overview

Nodes in the network are configured to receive messages through _TCP_ (usually used between nodes), _REST_ and [message broker](message%20broker.md). 

* From peer nodes using the native AnyLog API. This functionality is enables by calling the command: 
```anylog
run tcp server
```
* From users and applications using a REST API. This functionality is enabled by calling the command: 
```anylog
run rest server
```  
* From applications such as [_EdgeX_](using%20edgex.md) and [_Kafka_](using%20kafka.md).
This function is enabled by calling the command: 
```anylog
run message broker 
```

## Determining the IP addresses recognized by a node in the network

When a node starts, it determines the local IP addresses available to the node. These addresses initialize 2 dictionary variables:  

| Variable Name | Explanation   | Retrieve value |
| ------------- | ------------- | ------------- |
| ip            | The Public IP or a Local IP if the node is on a local network | !ip |
| external_ip   | The Public IP | !external_ip |


Some systems fail to identify their IP addresses, and the values can be set by the user.  
To view all IPs recognized by the node issue the following command:
```anylog
get ip list
```

## Configuring a REST server process
Any node in the network can be configured to receive requests using the REST API.  
Usage:
```anylog
run rest server [ip] [port] where timeout = [timeout] and threads = [threads count] and ssl = [true/false]
```

More details on the REST API are available at [using rest](using%20rest.md#using-rest).  
More details on setting a node as a REST server is available at [background processes](background%20processes.md#rest-requests).  

## Configuring a TCP server process
This process makes each node a member in the AnyLog Network and allows communication between peers in the network.  

Usage:
```anylog
run tcp server [ip] [port] [threads]
```
   
`[ip] [port]` - The IP and Port of the socket that is in the listening state and accessible by peer nodes in the AnyLog Network.   
`[local ip] [port]` - Optional parameters to indicate an IP and Port that are accessible from a local network.  
`[threads]` - An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 6.
 

### The Source Address
When the command `run tcp server` is initiated, the node dedicates a process to listen to incoming messages on the declared IP and Port.
When the node sends a message to a peer, it requests that the reply is sent to the declared IP and Port.  
Therefore, for an outgoing message, the declared IP and Port serve as a Source Address identifying the node that issued the message and an address for a reply message.   
 
A user can configure a node to use a different reply address in one of the following ways:

a) Request peers to reply using a different address.  
b) Request peers to determine the reply address from the message socket.

### Get the list of NICs

Usage:
```anylog
get nics list
```
Retrieves and displays a list of all network interfaces (NICs) on the system along with their:
* Name – the friendly name of the network interface
* Speed – reported link speed in Mbps (may be 0 or 4294 if unknown)
* Is Up – indicates whether the NIC is active (True) or not (False)

This function helps users identify which interfaces are usable for networking, diagnostics, or configuration tasks.

### Set Internal IP via Network Interface

Usage:
```anylog
set internal ip with [interface_name]
```
**Description:**    
Automatically sets the AnyLog node's internal IP address based on the IP associated with the specified network interface (NIC).

This internal IP is used for all internal communications between nodes (TCP messaging).

If the **set internal ip** call is successful, The value of **ip** in the dictionary is modifoed to the new local IP value.    
Use ```get !ip``` or ```!ip``` to see the updated value. 

**Parameters:**
[interface_name] The name of the network interface (e.g., enp0s3, eth0, wlan0).

**Default:**  
enp0s3 - Ethernet interface on PCI bus 0, slot 3.

**When to Use:**
* When deploying on VMs or hardware where IPs are dynamically assigned.
* To avoid hardcoding IP addresses in configuration files.
* For scripts or automated deployments that target known NICs.

**Example:**  
```anylog
set internal ip with enp0s8
```

**Notes:**
* If the specified interface does not exist or has no IPv4 address, the command will fail silently or fall back to 127.0.0.1.
* Use ```ip addr show``` or ```ifconfig``` to determine available NICs on the host machine.


### Setting a different IP address for replies 
Using the `set reply ip` command, user can direct a node sending a message, to receive the reply on a different IP address.    
Usage:
```anylog
set reply ip = [ip]
```

Examples:
```anylog
set reply ip = !external_ip
set reply ip = 24.23.250.144
```

The value assigned to the `reply ip` can be retrieved using the following command:
```anylog
get reply ip
```

### Using the message socket to determine the reply IP 
This configuration will retrieve the peer IP from the message socket and use the retrieved IP for the reply message.  
Usage:
```anylog
set reply ip = dynamic
```

### Reset the reply IP to the Source IP 
Calling reset will disable the use of reply IP. Replies will use the Source IP.  
Usage:
```anylog
reset reply ip
```


# Testing the network configuration

Different command calls can view and test the network configuration.  

View active connection using the command:
```anylog
get connections
```

Test the node configuration including the status of the REST server and the TCP server using the command:
```anylog
test node
```
 
Test connection between 2 peers in the network:
```anylog
run client (host:port) get status
```

Test the REST server configuration:
```anylog    
rest get url =  http://ip:port type = info details = "get status"
```  
Example:
```anylog
rest get url =  http://10.0.0.159:2049 type = info details = "get status"
```

Display the IP and Port used in a message:
```anylog
trace level = 1 tcp
```

Display the IP and Port used in a REST message by sending a VIEW request to the REST server.    
Example:
```anylog
curl --location --request VIEW 24.23.250.144:2049
```

