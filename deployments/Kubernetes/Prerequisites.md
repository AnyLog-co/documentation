# Prerequisites
Our [deployment repository](https://github.com/AnyLog-co/deployments/) provides the scripts and YAML files needed to 
deploy AnyLog (and other related tools - such as _PostgreSQL_ and _Grafana_) as either docker or helm package. In 
addition, the repository contains a shortened version of the shared directions depending on the deployment type.

This section will walk you through preparing to deploy AnyLog using _Helm_ and _Kubernetes_ tools. Directions for
deploying via _Docker_ can be found [here](../Docker) 

0. 4 Physical or Virtual machines -- unlike Docker, Kubernetes has the following [machine requirements](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#:~:text=Before%20you%20begin%201%20A%20compatible%20Linux%20host.,on%20your%20machines.%20...%207%20Swap%20disabled.%20): 
   * \>= 2GB of RAM per machine
   * \>=2 CPUs 
   * network connectivity between all machines in the cluster (public or private)
   * Unique hostname, MAC address, and product_uuid for every node
   * Swap memory disabled


1. Clone [AnyLog Deployment Scripts](https://github.com/AnyLog-co/deployments) 
```commandline
git clone https://github.com/AnyLog-co/deployments 
```

2. Each machine with docker, [Helm](https://helm.sh/docs/intro/install/) and [Kubernetes deployment tool](https://kubernetes.io/docs/tasks/tools/). 
For simplicity, the example uses [Minikube](https://minikube.sigs.k8s.io/docs/start/) via docker, but other Kubernetes 
deployment  tools will work as well.  
   * Single Command: `bash deployments/configurations/scripts/docker_install.sh`
   * Script: 
```shell

# update / upgrade env
for CMD in update upgrade update 
do 
    sudo apt-get -y ${CMD} 
done
# install docker 
sudo apt-get -y install docker.io docker-compose

# Grant user permission to docker 
USER=`whoami` 
sudo groupadd docker 
sudo usermod -aG docker ${USER} 
newgrp docker

# requirements for kubectl 
sudo apt-get install -y apt-transport-https ca-certificates curl
# Download the Google Cloud public signing key
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg

# Add the Kubernetes apt repository
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Update apt package index with the new repository and install kubectl
sudo apt-get update
sudo apt-get install -y kubectl

# download minikube - replace amd64 with arm64 for RPI4
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Install minikube
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# install helm 
sudo snap instal helm --clasic 

# update / upgrade env
for CMD in update upgrade update 
do 
    sudo apt-get -y ${CMD} 
done

# start minikube
minikube start 
```

3. Log into AnyLog docker in order to download the image. If you do not have login credentials for our Docker hub, feel 
free to <a href="mailto:info@anylog.co?subject=Request Docker access">send us a message</a>.    
   * Docker Password: **XXXX-XXXX-XXXX-XXXX**
   * Single Command: `bash deployments/helm/credentials.sh ${DOCKER_PASSWORD}`
   * Script:
```shell
# Set docker credentials for Kubernetes & Helm
kubectl create secret docker-registry imagepullsecret \
  --docker-server=docker.io \
  --docker-username=anyloguser \
  --docker-password=${DOCKER_PASSWORD} \
  --docker-email=anyloguser@anylog.co
```

If the docker request link doesn't work, please email us at [info@anylog.co](mailto:info@anylog.co). 