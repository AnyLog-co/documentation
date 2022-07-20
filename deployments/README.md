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
AnyLog has 3 major versions, each version is built on both _Ubuntu:20.04_ with _python:3.9-alpine_. 
* develop - is a stable release that's been used as part of our Test Network for a number of weeks, and gets updated every 4-6 weeks.
* predevelop - is our beta release, which is being used by our Test Network for testing purposes.
* testing - Any time there's a change in the code we deploy a "testing" image to be used for (internal) testing purposes. Usually the image will be Ubuntu based, unless stated otherwise.


| Build | Base Image | CPU Architecture | Pull Command | Size | 
|---|---|---|---|---|
| develop | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop` | 664MB | 
| develop-alpine | python:3.9-alpine | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop-alpine` | 460MB| 
| predevelop | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop` | ~245MB | 
| predevelop-alpine | python:3.9-alpine | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop-alpine` | ~178MB | 
| testing | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:testing` |


**[Docker](Docker)**
* [Preparing Machine(s) for Deployment](Docker/Prerequisites.md)
* [Install PostgreSQL](Docker/Postgres.md)
* [Install Master Node]()
* [Install Operator Node I]()
* [Install Operator Node II]()
* [Install Query Node]()
* [Install Grafana]()
* [Install Remote CLI]()
* [Setting Up EdgeX](Docker/EdgeX.md)

**[Kubernetes](Kubernetes)**
* [Preparing Machine(s) for Deployment]()
* [Understanding Kubernetes Networking for AnyLog]()
* [Install PostgreSQL]()
* [Install Master Node]()
* [Install Operator Node I]()
* [Install Operator Node II]()
* [Install Query Node]()

