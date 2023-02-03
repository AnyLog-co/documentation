# Installing AnyLog using Docker

You can deploy AnyLog via _helm_ by using either our deployment script or manually. 

For login credentials contact us at: [info@anylog.co](mailto:info@anylog.co)

**Support Links**
* [Remote-CLI](../Support/Remote-CLI)
* [EdgeX](../Support/EdgeX.md)
* [Grafana](../Support/Grafana.md)
* [Trouble Shooting](../Support/cheatsheet.md)


**Requirements**
Unlike _Docker_, Kubernetes has [machine requirements](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin) 
in order to run. 
* \>= 2GB of RAM
* \>= 2 CPUs or more
* \>= 20GB of free disk space
* network connectivity between all machines in the cluster
* Unique hostname, MAC address, and product_uuid for every node
* Swap memory disabled

For testing purposes we use [minikube](https://minikube.sigs.k8s.io/docs/start/) and [helm](https://helm.sh/docs/) via 
Docker; but can also be used with [other deployment tools](https://kubernetes.io/docs/tasks/tools/). 

## Deployment Process 
1. Download [deployments](https://github.com/AnyLog-co/deployments) & log into AnyLog Docker Hub
```shell
cd $HOME

git clone https://github.com/AnyLog-co/deployments

cd $HOME/deployments/

bash $HOME/deployments/installations/kube_credentials.sh ${YOUR_ANYLOG_DOCKER_CREDENTIALS}
```

2. Deploy relevant database, this can be done as docker image(s) or as services on your machine. Directions can be found 
[here](database_configuration.md)


3. [Deploy AnyLog](deploying_node.md)


4. Deploy other services like [Remote-CLI](../Support/Remote-CLI.md) and [Grafana](../Support/Grafana.md)

