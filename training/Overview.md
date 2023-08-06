# Training Overview

This document and the referenced documents explain the deployment and configuration of an AnyLog test network.

AnyLog is deployed using Docker or Kubernetes as a pre-configured software package.  
To address dynamic and ad-hoc needs, each AnyLog node provides an interactive environment allowing to dynamically change configurations 
and issue commands and queries. In addition, the interactive environment is extended to send requests and
 inspect responses remotely via REST. Users can use tools like [cURL](https://curl.se/) or [Postman](../northbound%20connectors/using%20postman.md) 
 as well as a [remote CLI](../northbound%20connectors/remote_cli.md) which is an AnyLog web based application allowing 
 intuitive and simple GUI to interact with nodes in the AnyLog Network.  
 
 
The training reviews the basic operations with AnyLog nodes and guides users to manage, monitor and query nodes, metadata and data.
This training demonstrates how to make changes to the default configurations to satisfy proprietary processes, data connectors, 
and specific/domain requirements .

In this training, **Session I** reviews basic operations and **Session II** provides the guidance to deploy a network that manages
data and satisfies queries.  

The test network deployed is shown in the following diagram:

![deployment diagram](../imgs/deployment_diagram.png)


In the test network, data will be transferred to the 2 Operator Nodes, and a query that is processed on the Query Node will be satisfied
as if the entire data set is hosted locally (as if the 2 Operators are a single machine).

**Note 1:** The table of content to the AnyLog documentation is available in the [README Section](../README.md)

**Note 2:** In this training, some configurations are packaged with the software deployed, and some configurations are done
using the AnyLog command-line.    
In a customer deployment, all configurations are pre-packaged, and associated to a node by one (or more) of these processes:
1) By maintaining configuration commands in a local file that is associated to a node.
2) By dynamically creating a configuration file (for the node) during the Docker deployment.
3) By maintaining configuration commands in policies stored in the shared metadata and associating a configuration policy to a node.
 
**Note 3:** Advanced users can review the [Network Setup Document](../examples/Network%20setup.md) to deploy a test
network using the AnyLog CLI without pre-packaged configuration. 

### Session I - The Basic Guided Tour
 This guided tour introduces you to the basics of AnyLog and its main feature.  
 This tour uses a single pre-installed node (not configured), that demonstrates the basic operations.
 
 Prior to the guided tour, it is recommended to review the following documents:
 * [Getting Started](../getting%20started.md) - An overview of the network, nodes types, deployment, metadata and commands.
 * [Session I](Session%20I%20(Demo).md) - This document lists the basic commands that are demonstrated in this training session.
 * [Connecting Nodes](../examples/Connected%20Nodes.md) - Configuring nodes to participate in the network and communicate with 3rd parties apps.
 
The presentation in this session reviews the following:

    1. The nodes types
        - Master node (optional)
        - Operators node
        - Query Node   
    2. The test network to deploy
    4. The local dictionary
    5. The node CLI
    6. The remote CLI
    7. Configuration commands
    8. Status commands
    9. Metadata commands
    10. Monitoring commands
    11. Query data  
    
### Session II - Deployment of the test network
   This session guides users to deploy and configure a test network on their machines.  
   
   Prior to the guided tour, it is recommended to review the the [Session II (Deployment) document](Session%20II%20(Deployment).md).  
        
   This session will allow users to do the following on their machines:
   
     1. Download, install and configure AnyLog on each node:
        - Deploy a Master Node
        - Deploy a query node
        - Deploy 2 Operator Nodes
     2. Deploy and configure a data generator
     3. Deploy and configure the Remote CLI
     4. Issue status commands
     5. Issue metadata commands
     6. Query data  
      

  