---
layout: default
title: Training
nav_order: 7
has_children: true
---
# Training
EdgeLake is deployed using Docker as a pre-configured software package.

To address dynamic and ad-hoc needs, each EdgeLake node provides an interactive environment allowing to dynamically 
change configurations and issue commands and queries. 

In addition, the interactive environment is extended to send requests and  inspect responses remotely via REST. Users 
can use tools like [cURL](https://curl.se/), [Postman](..%2Fnorthbound%2Fusing_postman.md), as well AnyLog's 
[Remote-CLI](..%2Fnorthbound%2Fremote_cli.md) to send request against EdgeLake node(s). 

[Remote-CLI](..%2Fnorthbound%2Fremote_cli.md) is a web based application allowing intuitive and simple GUI to interact 
with nodes in the AnyLog Network.

This section, guides EdgeLake users on deployment, management, monitoring and querying nodes in the network.

## Deployment Diagram
In the test network, data will be transferred to the 2 Operator Nodes, and a query that is processed on the _Query Node_ 
will be satisfied as if the entire data set is hosted locally (as if the 2 Operators are a single machine).

<div class="image-frame"><img src="../../../imgs/deployment_diagram.png" /></div>

In this training, some configurations are packaged with the software deployed, and some configurations are done using 
the command-line.

<ol start="1">
    <li>By maintaining configuration commands in a local file that is associated to a node.</li>
    <li>By dynamically creating a configuration file (for the node) during the Docker deployment.</li>
    <li>By maintaining configuration commands in policies stored in the shared metadata and associating a configuration policy to a node.</li>
</ol>

