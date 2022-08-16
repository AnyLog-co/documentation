# Deployment of Docker Compose & Kubernetes

AnyLog can be deployed using either _Docker_ or _Kubernetes_. Our [deploymeents](deployments) directory provided detailed 
directions in terms of deployment of each type; including troubleshooting, networking support, and persistent data 
maintenance.

In general, we recommend users begin with a single physical machine consisting of _Master_ node, 2 _Operator_ nodes and 
a _Query_ node, as shown in the image below, using the [Demo Deployment Network](deployments/Docker/single_deployment_demo.md) 
setup. 

![deployment diagram](imgs/deployment_diagram.png)


## Node Types 
In addition to the sample deployment, mentioned above, users can configure and deploy different types of AnyLog node(s) 
independently. 
* Master – A node that manages the shared metadata (if a blockchain platform is used, this node is redundant).
* Operator – A node that hosts the data. For this deployment we will have 2 Operator nodes.
* Query – A node that coordinates the query process. 
* Publisher - A node that supports distribution of data from device(s) to operator nodes. This node is not part of the
deployment diagram. However, is often used in large scale projects. 
* (default) REST - A node consisting **only** _TCP_ and _REST_, to act as a testbed / sandbox for playing with AnyLog 
without external / internal processed running in the background.

## Versions 
AnyLog has 3 major versions, each version is built on both _Ubuntu:20.04_ with _python:3.9-alpine_. 
* develop - is a stable release that's been used as part of our Test Network for a number of weeks, and gets updated every 4-6 weeks.
* predevelop - is our beta release, which is being used by our Test Network for testing purposes.
* testing - Any time there's a change in the code we deploy a "testing" image to be used for (internal) testing purposes. 
Usually, the image will be Ubuntu based, unless stated otherwise.


| Build | Base Image | CPU Architecture | Pull Command | Size | 
|---|---|---|---|---|
| develop | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop` | 664MB | 
| develop-alpine | python:3.9-alpine | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop-alpine` | 460MB| 
| predevelop | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop` | ~245MB | 
| predevelop-alpine | python:3.9-alpine | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop-alpine` | ~178MB | 
| testing | Ubuntu:20.04 | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:testing` |

By default, the AnyLog image is configured to run as a _REST_ node, which means that the TCP (port `2148`) and REST 
(port `2149`) options are running, but no other process is enabled. This allows for users to play with the system with 
no other services running in the background, but already having the default network configurations. The deployment command 
is: 

```
docker run --network host -it --detach-keys="ctrl-d" --name anylog-node --rm anylogco/anylog-network:develop
```
