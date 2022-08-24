# Prerequisites
Our [deployment repository](https://github.com/AnyLog-co/deployments/) provides the scripts and YAML files needed to 
deploy AnyLog (and other related tools - such as _PostgreSQL_ and _Grafana_) as either docker or helm package. In 
addition, the repository contains a shortened version of the shared directions depending on the deployment type.

This section will walk you through preparing to deploy AnyLog using _Docker_ and _docker-compose_. Directions for
deploying via _Helm_ and _Kubernetes_ can be found [here](../Kubernetes)

0. 4 Physical or Virtual machines


1. Clone [AnyLog Deployment Scripts](https://github.com/AnyLog-co/deployments) 
```commandline
git clone https://github.com/AnyLog-co/deployments 
```

2. Install Docker & docker-compose using either the deployment scripts or manually. 
   * Single Command: `bash deployments/docker-compose/docker_install.sh`
   * Full process: 
```commandline
# directions to install docker & docker-compose on Ubuntu 

# update / upgrade env
for CMD in update upgrade update 
do 
    sudo apt-get -y ${CMD} 
done

# install docker & docker-compose 
sudo apt-get -y install docker.io docker-compose 

# Grant user permission to docker 
USER=`whoami` 
sudo groupadd docker 
sudo usermod -aG docker ${USER} 
newgrp docker

# update / upgrade env
for CMD in update upgrade update
do
    sudo apt-get -y ${CMD}
done
```

3. Log into AnyLog docker in order to download the image. If you do not have login credentials for our Docker hub, feel 
free to <a href="mailto:info@anylog.co?subject=Request Docker access">send us a message</a>.    
   * Docker Password: **XXXX-XXXX-XXXX-XXXX**
```commandline
# log into docker for access to AnyLog
docker login -u anyloguser -p ${DOCKER_PASSWORD}
```

If the docker request link doesn't work, please email us at [info@anylog.co](mailto:info@anylog.co).    