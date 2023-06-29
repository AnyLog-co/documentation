## AnyLog Deployment

This document describes how to deploy and configure an AnyLog Network. The example provides directions to:
* Deploy an  AnyLog Network consisting of  4 nodes (2 operators, 1 query, 1 master) 
* Deploy our Remote CLI - an open source web interface used for querying data 
* Configure EdgeX as a data source  
* Configure Grafana to visualize the data 

We recommend deploying an overlay network, such as [nebula](Networking%20&%20Security/nebula.md), or some other form of 
static IPs when deploying a production network.

## Deployment
**Note Types**:
* Master – A node that manages the shared metadata (if a blockchain platform is used, this node is redundant).
* Operator – A node that hosts the data. For this deployment we will have 2 Operator nodes.
* Query – A node that coordinates the query process. 
* Publisher - A node that supports distribution of data from device(s) to operator nodes. This node is not part of the
deployment diagram. However, is often used in large scale projects. 

**Deployment Diagram**:

![deployment diagram](../imgs/deployment_diagram.png)

## AnyLog Versions
AnyLog has 3 major versions, each version is built on both _Ubuntu:20.04_ with _python:3.9-alpine_. 
* develop - is a stable release that's been used as part of our Test Network for a number of weeks, and gets updated every 4-6 weeks.
* predevelop - is our beta release, which is being used by our Test Network for testing purposes.
* testing - Any time there's a change in the code we deploy a "testing" image to be used for (internal) testing purposes. 
Usually the image will be Ubuntu based, unless stated otherwise.


| Build             | Base Image          | CPU Architecture | Pull Command                                            | Compressed Size | 
|-------------------|---------------------|---|---------------------------------------------------------|-----------------|
| develop           | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop`           | ~320MB                | 
| develop-alpine    | python:3.9-alpine   | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop-alpine`    | ~170MB                |
| develop-rhl       | redhat/ubi8:latest  | amd64,arm64 | `docker pull anylogco/anylog-network:develop-rhl`       |  ~215MB               |
| predevelop        | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop`        | ~320MB          | 
| predevelop-alpine | python:3.9-alpine   | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop-alpine` | ~170MB          |
| predevelop-rhl    | redhat/ubi8:latest   | amd64,arm64 | `docker pull anylogco/anylog-network:predevelop-rhl`    | ~215MB          |
| testing           | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:testing`           |

*Compressed Size - size calculated by summing the image's layers, which are compressed


When an AnyLog node is configured, the configuration determines the services that would be offered by the node.  
The following are the main services which are enabled in most deployments:
* TCP - Allowing the node to join the AnyLog network and communicate with peer nodes.
* REST - Allowing third party applications and data sources to communicate with an AnyLog node.
* BROKER - Allowing third party applications to publish data on an AnyLog node (allowing a data source to treat AnyLog as a message broker).
  
A basic deployment of an AnyLog instance can be executed using the following line:

```shell
docker run --network host -it --detach-keys="ctrl-d" --name anylog-node --rm anylogco/anylog-network:predevelop
```


## Table of Content

### Deploy AnyLog
* [Deploy Database(s)](database_configuration.md)
* [Deploy Node](deploying_node.md)
* [Execute Personalized Scripts](executing_scripts.md)
* [Standalone Network](single_deployment_demo_network.md) - Deploy a full network on a single machine

### Support 
* [Cheat Sheet](Support/cheatsheet.md)
* [Setting Up MongoDB](Support/setting_up_mongodb.md)

### Third-Party Apps 
* [Remote-CLI](Support/Remote-CLI.md)
* [Grafana](Support/Grafana.md)
* [EdgeX](Support/EdgeX.md)
* [Nginx](Networking%20&%20Security/nginx.md)
* [Nebula Overlay](Networking%20&%20Security/nebula.md)

### Other 
* [Docker Volumes](Networking%20&%20Security/docker_volumes.md)
* [Kubernetes Volumes](Networking%20&%20Security/kubernetes_volumes.md)
* [Kubernetes Networking](Networking%20&%20Security/kubernetes_networking.md)

