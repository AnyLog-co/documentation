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

## Local directory structure
 
This setup is using identical directory structure on all nodes:  

<pre>
Directory Structure   Explabnation
-------------------   -----------------------------------------
--> AnyLog-demo       [AnyLog Root]
    -->data           [Intermediate data processed by this node]
       -->watch       [Data placed on this directory is eithe a JSON file or SQL file and is processed by the node]
       -->in          [Data send from a different node]
       -->out         [Data to be transferred to another node]
       -->test        [Test data]
    -->blockchain     [A JSON file representing the metadata relevant to the node. The file in a Master Node will contains all the metadata]
    -->source         [The source files of the AnyLog instance maintined in a sub-folders]
    -->scripts        [Script files that install and configure the AnyLog instance role]
       -->install     [Installation scripts]
       -->anylog      [AnyLog scripts, configure the AnyLog instance]
</pre>

## Prerequisites

An Ubuntu machine for each instance.  

#### Installing an Ubuntu VM

#### Installing Python

#### Download the code base and scripts from GitHub

#### Configuring the linux machine


## Running an AnyLog Instance

To run the instance on a local machine, from the AnyLog root, issue the command:  
```python3 source/cmd/user_cmd.py```

## Configuring a Publisher Node

## Configuring an Operator Node


 