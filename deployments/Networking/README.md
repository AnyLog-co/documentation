# Networking 

## Overview

AnyLog nodes uses the following IP addresses:
* External IP -  the public IP address by which AnyLog nodess are reachable. It is generally the IP address assigned to one of the interfaces on the machine (physical or virtual) on which the AnyLog node is deployed. Users should provide the this IP address during the node deployment.
* Internal IP  - the IP address by which AnyLog nodes are reachable within a subnet. If nodes are not on the same subnet the External IP should also be used as the Internal IP. Users should provide this address during the node deployment process.
* Overlay IP - An AnyLog overlay network may be deployed on AnyLog nodes to provide secure communication between nodes and assist in reaching nodes behind firewalls. The Overlay IP is used as the Internal IP of the nodes when overlay network is deployed. Overlay IPs are part of the same subnet. Users should choose a subnet and provide Overlay IP addresses from this subnet for each node during the node deployment. See [Nebula Install](nebula.md) for further detail.

to during better reachability further in An overlay network the overlay network 
External and Intthe overlay network ernal IP addresses are set during deployment either via the config files or by the values provided when using the AnyLog questionnaire based deployment.
An overlay network may be deployed to provide secure communications between AnyLog nodes and firewall bypass capability.


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

