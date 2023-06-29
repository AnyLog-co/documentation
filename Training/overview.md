# Training Overview

This document and the set of referenced documents explain the deployment and configuration of an AnyLog test network.

**Note: 
This training is using command-line instructions to configure the nodes in the network.**  
In a customer deployment, these commands are pre-packaged, and associated to a node by one (or more) of these processes:
1) By maintaining the configuration commands in a local file that is associated to a node.
2) By dynamically creating a configuration file (for the node) during the Docker deployment, and associating the file with the node.
3) By maintaining configuration commands in policies stored in the shared metadata and associating a policy to a node.

##The training includes 2 sections:

1) Session I - A presentation that reviews the following:

    A) The nodes types    
        a) Master node (optional)  
        b) Operators node  
        c) Query Node   
    B) The test network to deploy  
    C) The node CLI  
    D) The remote CLI  
    E) Configuration commands  
    F) Status commands  
    G) metadata commands  
    H) Query data  
    
2) Session II - Deployment of the test network
    a) Deploy a Master Node   
    b) Deploy a query node   
    c) Deploy 2 Operator Nodes  
    d) Deploy a data generator  
    e) Issue status commands  
    f) Issue metadata commands  
    g) Query data  
      

  