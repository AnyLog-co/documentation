## AnyLog Deployment

This document describes how to deploy and configure an AnyLog Network. The example provides directions to:
* Deploy an  AnyLog Network consisting of  4 nodes (2 operators, 1 query, 1 master) 
* Deploy our Remote CLI - an open source web interface used for querying data 
* Configure EdgeX as a data source  
* Configure Grafana to visualize the data 

## Deployment
**Note Types**:
* Master – A node that manages the shared metadata (if a blockchain platform is used, this node is redundant).
* Operator – A node that hosts the data. For this deployment we will have 2 Operator nodes.
* Query – A node that coordinates the query process. 

**Deployment Diagram**: 

![deployment diagram](../imgs/deployment_diagram.png)


## Table of Contents
**[Docker](Docker)**
* [Preparing Machine(s) for Deployment](Docker/Prerequisites.md)
* (Optional) [Install PostgreSQL](Docker/Postgres.md)
* [Install Master Node]()
* [Install Operator Node I]()
* [Install Operator Node II]()
* [Install Query Node]()
* [Install Grafana]()
* [Install Remote CLI]()
* [Setting Up EdgeX]()

**[Kubernetes](Kubernetes)**
* [Preparing Machine(s) for Deployment]()
* [Understanding Kubernetes Networking for AnyLog]()
* (Optional) [Install PostgreSQL]()
* [Install Master Node]()
* [Install Operator Node I]()
* [Install Operator Node II]()
* [Install Query Node]()

