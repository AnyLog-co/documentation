# Prerequisites
Our [deployment repository](https://github.com/AnyLog-co/deployments/) provides the scripts and YAML files needed to 
deploy AnyLog (and other related tools - such as _PostgreSQL_ and _Grafana_) as either docker or helm package. In 
addition, the repository contains a shortened version of the shared directions depending on the deployment type.

## Setup
Our demo network requires 4 machines - either physical or virtual that will act as: Master, Query and (2) Operator 
nodes. The following steps should be done on each of them.

1. Clone [AnyLog Deployment Scripts](https://github.com/AnyLog-co/deployments) 
```shell
git clone https://github.com/AnyLog-co/deployments 
```

2. For Kubernetes deployments, we recommend having a proxy IP address (we use [NGINX](Networking/nginx.md)) in order to 
have consistent IP address(es) for a given node. 


3. Since AnyLog is a distributed network, we recommend setting up an overlay network for those super secure 
systems. For our testing purposes, we had used [nebula](Networking/nebula.md) - an overlay network created by _Slack_ 
which was easy to deploy and utilize. 


### Docker 
1. Install Docker & docker-compose
```shell
bash $HOME/deployments/installations/docker_install.sh
```

2. Validate Docker & docker-composer are installed
```shell
docker --version
docker-compose --version 
```

3. Log into AnyLog docker in order to download the image. If you do not have login credentials for our Docker hub, feel 
free to <a href="mailto:info@anylog.co?subject=Request Docker access">send us a message</a>.
```shell
bash $HOME/deployments/installations/docker_credentials.sh ${DOCKER_PASSWORD}
```
If the docker request link doesn't work, please email us at [info@anylog.co](mailto:info@anylog.co).    

### Kubernetes with Helm
Our Kubernetes installation script conssits of [helm](https://helm.sh/) and minikube; however, it has also been tested with [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) and other flavors of kubernetes installations. Unlike Docker, Kubernetes has the following [machine requirements](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#:~:text=Before%20you%20begin%201%20A%20compatible%20Linux%20host.,on%20your%20machines.%20...%207%20Swap%20disabled.%20): 
   * \>= 2GB of RAM per machine
   * \>=2 CPUs 
   * network connectivity between all machines in the cluster (public or private)
   * Unique hostname, MAC address, and product_uuid for every node
   * Swap memory disabled

1. Install Kubernetes & Helm - our deployment script uses _minikube_. Directions for other can be found on the [official website](https://kubernetes.io/docs/setup/production-environment/tools/)
```shell
bash $HOME/deployments/installations/kube_install.sh
```

2. Validate Kubernetes & Helm are installed 
```shell
helm version 
kubectl version
```

3. Log into AnyLog docker in order to download the image. This will create a [secret object](https://kubernetes.io/docs/concepts/configuration/secret/)
called `imagepullsecret`. If you do not have login credentials for our Docker hub, feel free to <a href="mailto:info@anylog.co?subject=Request Docker access">send us a message</a>. 
```shell
bash $HOME/deployments/installations/kube_credentials.sh ${DOCKER_PASSWORD}
```
If the docker request link doesn't work, please email us at [info@anylog.co](mailto:info@anylog.co).
