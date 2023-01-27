# AnyLog Requirements 

An AnyLog node can be run as either a Docker image with Docker or Kubernetes, or it can run as a standalone product. 

## AnyLog Requirements
AnyLog is a Python-based software, which means that as long as Python3.5 or higher and 
[package requirements](deployments/requirements.txt) are installed AnyLog should be able to run.

Please [contact us](mailto:info@anylog.co) if you'd like to deploy AnyLog without a container. 

### Container Based Deployment 
AnyLog has 3 major versions -  
* develop - is a stable release that's been used as part of our Test Network for a number of weeks, and gets updated every 4-6 weeks.
* predevelop - is our beta release, which is being used by our Test Network for testing purposes.
* testing - Any time there's a change in the code we deploy a "testing" image to be used for (internal) testing purposes. 
Usually the image will be Ubuntu based for an amd64 unless stated otherwise.

For _develop_ and _predevelop_ users can deploy with  base operating system of _Ubuntu:20.04_, _python:3.9-alpine_ and 
_redhat/ubi8:latest_ on CPU architecture types amd64 (ex. PCs and servers), arm/v7 (ex. RaspberryPi4), arm64 (ex. NVIDIA 
InfiniBand Switches)


| Build             | Base Image          | CPU Architecture | Pull Command                                            | Compressed Size | 
|-------------------|---------------------|---|---------------------------------------------------------|-----------------|
| develop           | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop`           | ~320MB                | 
| develop-alpine    | python:3.9-alpine   | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:develop-alpine`    | ~170MB                |
| develop-rhl       | redhat/ubi8:latest  | amd64,arm64 | `docker pull anylogco/anylog-network:develop-rhl`       |  ~215MB               |
| predevelop        | Ubuntu:20.04        | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop`        | ~320MB          | 
| predevelop-alpine | python:3.9-alpine   | amd64,arm/v7,arm64 | `docker pull anylogco/anylog-network:predevelop-alpine` | ~170MB          |
| predevelop-rhl    | redhat/ubi8:latest   | amd64,arm64 | `docker pull anylogco/anylog-network:predevelop-rhl`    | ~215MB          |
| testing           | Ubuntu:20.04        | amd64 | `docker pull anylogco/anylog-network:testing`           |


## Requirements for Container-based Deployment
### Docker 
* 64-bit processor with Second Level Address Translation (SLAT)
* 4GB system RAM
* For [Windows](https://docs.docker.com/desktop/install/windows-install/) BIOS-level hardware virtualization support must 
be enabled in the BIOS settings
* For [Linux](https://docs.docker.com/desktop/install/linux-install/#:~:text=To%20install%20Docker%20Desktop%20successfully%2C%20your%20Linux%20host,ID%20mapping%20in%20user%20namespaces%2C%20see%20File%20sharing) 
KVM virtualization support and Enable configuring ID mapping in user namespaces

### Kubernetes 
* \>= 2GB of RAM
* \>= 2 CPUs or more
* \>= 20GB of free disk space
* network connectivity between all machines in the cluster
* Unique hostname, MAC address, and product_uuid for every node
* Swap memory disabled

For testing purposes we use [minikube](https://minikube.sigs.k8s.io/docs/start/) and [helm](https://helm.sh/docs/) via 
Docker; but can also be used with [other deployment tools](https://kubernetes.io/docs/tasks/tools/).





