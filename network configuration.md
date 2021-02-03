# Network Configuration

## overview

Nodes in the network are configured to receive messages from 2 sources:  

a. From users and applications using a REST API.  
This functionality is enabled by calling the command: ***run rest server***  

b. From peer nodes using the native AnyLog API.  
This functionality is enables by calling the command: ***run tcp server***  

## Determining the IP addresses recognized by the current node

When a node starts, it determines the local IP addresses available to the node. These addresses initialize 2 dictionary variables:  

| Variable Name | Explanation   | Retrieve value |
| ------------- | ------------- | ------------- |
| ip            | IPv4 Address | !ip |
| external_ip   | The Public IP | !external_ip |

Some systems fail to identify their IP addresses and the values can be set by the user.  
To view all networks recognized by the node issue the following command:
<pre>
get ip list
</pre> 

## Configuring a REST server process
Any node in the network can be configured to receive requests using the REST API.
Usage:
<pre>
run rest server [ip] [port] where timeout = [timeout] and ssl = [true/false]
</pre>
More details on the REST API are available at (using rest)[https://github.com/AnyLog-co/documentation/blob/master/using%20rest.md#using-rest].  
More details on setting a node as a REST server is available at (background processes)[https://github.com/AnyLog-co/documentation/blob/master/background%20processes.md#rest-requests].  

## Configuring a TCP server process
This process is used for communication between peers in the network and makes the node a member in the AnyLog Network.  

Usage:
<pre>
run tcp server [ip] [port] [threads]
</pre>
Explanation:  
[ip] [port] - The process listens for incoming messages on the assigned IP and and Port.
[Threads] - An optional parameter for the number of workers threads that process requests which are send to the provided IP and Port. The default value is 1

Additional information is available at (network configuration)[https://github.com/AnyLog-co/documentation/blob/master/network%20configuration.md]. 

When the command ***run tcp server*** is initiated, the node dedicates a process to listen for incoming messages on the IP and Port.
The IP and Port specified on the command line are considered as the Source IP and Port.  
When a message is send to a peer, the node requests the peer to reply to the Source IP and Port.

In some use cases, the Source IP represent an internal network which is not accessible by the peer nodes. 
To address the internal netwoks, a user can configure the node as follows:

a) Request peers to reply using a different IP address.  
b) Request peers to determine the IP address from the message socket.

### Setting a different IP address for replies 
Using the ***set reply ip*** command, user can direct a server to use a different IP address for replies.
Usage:
<pre>
set reply ip = [ip]
</pre>

Examples:
<pre>
set reply ip = !external_ip
set reply ip = 24.23.250.144
</pre>

### Using the message socket to determine the reply IP 
This configuration will retrieve the peer IP from the message socket and use the retrieved IP for the reply
Usage:
<pre>
set reply ip = none
</pre>

# Testing the network configuration

Different command line calls can view and test the network configuration.  

View active connection using the command:
<pre>
get connections
</pre>

Test the node configuration including the status of the REST server and the TCP server using the command:
<pre>
test node
</pre>
 
Test connection between 2 peers in the network:
<pre>
run client (host:port) get status
</pre>

Test the REST server configuration:
<pre>    
rest get url =  http://ip:port type = info details = "get status"
</pre>  
Example:
<pre>
rest get url =  http://10.0.0.159:2049 type = info details = "get status"
</pre>

DIsplay the IP and Port used in a message:
<pre>
trace level = 1 tcp
</pre>

DIsplay the IP and Port used in a REST message:  
Send a view message to the REST IP and Port.  
Example:
<pre>
curl --location --request VIEW 24.23.250.144:2049
</pre>
