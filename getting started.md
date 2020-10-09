# Getting Started
This document explains how to install and run AnyLog instances.  

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
* The TestNet is using Master Nodes to share metadata information.  
  
## The MetaData
The metadata can be placed on a Master Node that is shared by other members of the network.  
The members that share a Master Node form a group and make their data sharable between the group members.  
For the TestNet members, a Master Node is available at ```IP: 18.217.99.117 and Port: 2049```.  
Members can also use a Master Node which is available to selected members. These members form a private group and only share data among the members of the private group.  
Alternatively, replace the command ```blockchain push``` with the command ```blockchain add``` to manage the metadata locally.
More information on the blockchain commands is available here - [blockchain](https://github.com/AnyLog-co/documentation/blob/master/blockchain%20commands.md)

## Local directory structure
 
This setup is using identical directory structure on all nodes:  

<pre>
Directory Structure   Explabnation
-------------------   -----------------------------------------
--> AnyLog-Network     [AnyLog Root]
    -->data           [Intermediate data processed by this node]
       -->watch       [Data placed on this directory is either a JSON file or SQL file and is processed by the node]
       -->prep        [Data in processing state]
       -->bkup        [Backup of processed data]
       -->error       [Files that triggered failures when processed]
    -->blockchain     [A JSON file representing the metadata relevant to the node. The file in a Master Node will contains all the metadata]
    -->source         [The source files of the AnyLog instance maintained in a sub-folders]
    -->scripts        [Script files that install and configure the AnyLog instance role]
       -->install     [Installation scripts]
       -->anylog      [AnyLog scripts, configure the AnyLog instance]
</pre>

Users can set any other structure by changing the values to the variables that address the different directories or by declaring a home directory to anylog.  
When an AnyLog Node starts, it considers 2 system parameters:  
***anylog_lib*** - to the determine the home directory to the Python Libraries.  
***anylog_home*** - to determine the home directory for the data files.  
The home directory for the data files can be changed dynamically uing the command:
```
set anylog home [absolute path]
```


## Prerequisites

* Access to the [AnyLog codebase](https://github.com/AnyLog-co/AnyLog-Network) on Github
* An Ubuntu machine for each instance.  
* PostgreSQL as a default local database on each node.  
* Installation details are available here - [Install](https://github.com/AnyLog-co/AnyLog-Network/blob/develop/README.md)
* Installation instructions on the packages below are available here - [Wiki](https://github.com/AnyLog-co/AnyLog-Network/wiki) 
     * Install Virtualbox & Ubuntu
     * Install AnyLog Prerequisites
     * Setting a new branch & other Git commands
     * AnyLog Documentation
     * How to do a Pull Request

#### Running an AnyLog Instance

To run the instance on a local machine, from the AnyLog root, issue the command:  
```python3 source/cmd/user_cmd.py```  
Info on starting an AnyLog instance ins available here - [Starting an instance](https://github.com/AnyLog-co/documentation/blob/master/starting%20an%20anylog%20instance.md)

## Running the demo

The Demo directory includes the scripts to configure a node as an Operator and a second node as a Publisher.    
The Publisher node acts as a query node and is offering a REST API such that it can accept queries from a REST client.    
Demo data is available in the ***sample_data*** directory (inside demo directory).  

To build the demo environment, the following needs to be done:
* Install 2 Ubuntu Linux machines.
* Install the AnyLog package on each machine.
* Run the AnyLog instance on each machine.
* On the Operator node, run the script ```operator_init.anylog```.  
This script initiates variables and calls the script ```operator_watch.anylog``` that configures the node to watch data placed in the ***watch*** directory.
* On the Publisher node, run the script ```publisher_init.anylog```.  
This script initiates variables and calls the script ```publisher_watch.anylog``` that configures the node to watch data placed in the ***watch*** directory.  
* Copy one of the data files from the ***sample data*** directory to the watch directory.  
The data will be send to the Operator node and stored on the local database.
* Using a REST client, connect to a Query node (the Publisher node in this demo) and issue a query.  
Details on issuing queries are available here - [Queries](https://github.com/AnyLog-co/documentation/blob/master/queries%20and%20info%20requests.md)
* Details on the AnyLog Demo scripts are available here - [scripts](https://github.com/AnyLog-co/AnyLog-Network/blob/develop/demo/README.md)





 