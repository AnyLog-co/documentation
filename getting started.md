# Getting Started
This document explains how to install and run anylog instances.  

## Type of instances
***Publishers*** - nodes that receive data from a data source (i.e. devices) and distribute the data to Operators.  
***Operators*** - nodes that host the data and satisfy queries.  
***Query Nodes*** - nodes that receive the queries and manage the query processes.
***Master Nodes*** - optional nodes, nodes that maintain a complete copy of the metadata. Any node can be declared as a Master node.   
A node can have one or more roles.

## The AnyLog TestNet
* Nodes participating with this setup are members of the AnyLog TestNet.
* This setup assumes permitted network without security restrictions (unless metadata is kept private, see details below).
* If metadata is shared, data placed on the network is available to all participating members.
* The TestNet is using Master Nodes to share metadata information. A later version would enable the blockchain.
  
## The MetaData
The metadata can be placed on a Master Node that is shared by other members of the network.  
The members that share a Master Node for a group and make their data sharable between the group members.  
For the TestNet members, a Master Node is available at IP: 18.217.99.117 and Port: 2049



 