# Training Overview

This document and the set of referenced documents explain the deployment and configuration of an AnyLog test network.

**Note 1:** Detailed explanations are available in the AnyLog Documentation. the table of content is available in the 
[READ ME File](../README.md)

**Note 2:** This training is using command-line instructions to configure the nodes in the network.
In a customer deployment, these commands are pre-packaged, and associated to a node by one (or more) of these processes:
1) By maintaining the configuration commands in a local file that is associated to a node.
2) By dynamically creating a configuration file (for the node) during the Docker deployment.
3) By maintaining configuration commands in policies stored in the shared metadata and associating a policy to a node.
 
### Session I - The Basic Guided Tour
 This guided tour introduces you to the basics of AnyLog and its main feature.  
 This tour uses a single pre-installed node (however, not configured), that demonstrates the basic operations.
 
 Prior to the guided tour, it is recommended to review the following documents:
 * [Getting Started](../getting%20started.md) - An overview of the network, nodes types, deployment, metadata and commands.
 * [Session I](onboarding.md) - The basic commands that are demonstrated in this training session. 
 
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
   This guided session will support users to deploy and configure a test network on their machines.  
   Prior to this session, users are required to prepare 5 machines (physical or virtual) as follows:
   * A minimum of 256MB of RAM.
   * A minimum of 10GB of disk space.
   * Each node accessible by IP and Port (remove firewalls limitations).
   * [Docker](https://docs.docker.com/) installed (navigate to [Get Docker](https://docs.docker.com/get-docker/) site to access
   the Docker download that’s suitable for your platform).

   Note: The prerequisites for a customer deployment are available [here](..//deployments/Prerequisite.md).
   
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
      

  