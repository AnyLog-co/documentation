# Networking 

Since AnyLog is on a distributed network (ie. AnyLog nodes can exist on different subnetworks) there may be other 
requirements to overcome barriers in order to have them communicate. This section covers resolving the issue using an  
overlay network and (NGINX) proxy IP support. 

## Process 
1. Install an overlay network, we do not recommend having the administrative instance seat on the same machine as AnyLog
_master_ node. - [Nebula Install](nebula.md)


2. Install & configure a proxy IP address - we utilize [NGINX](nginx.md)


3. Update the _`PROXY_IP`_ address in the anylog configuration file. The reason for the proxy IP address, specifically 
when deploying Kubernetes, is to have consistent IP addresses in the AnyLog ledger. Otherwise, a new blockchain policy
will be created each time the node initiates.  

   
4. Deploy AnyLog 

For Kubernetes - the proxy IP could be the overlay IP address (if set) or the local IP address of the machine

