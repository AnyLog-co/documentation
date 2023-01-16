# Installing AnyLog using Docker

You can deploy AnyLog via _helm_ by using either our deployment script or manually. 

For login credentials contact us at: [info@anylog.co](mailto:info@anylog.co)

**Support Links**
* Deploy [Remote-CLI](../Support/Remote-CLI)
* Deploy [EdgeX](../Support/EdgeX.md)
* Deploy [Grafana](../Support/Grafana.md)
* [Trouble Shooting]()
* [Sample Queries]()



### Requirements
Unlike _Docker_, Kubernetes has [machine requirements](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin) 
in order to run. 
* 2GB or more of RAM
* 2 CPUs or more
* 20GB of free disk space
* network connectivity between all machines in the cluster

For testing purposes we use [minikube](https://minikube.sigs.k8s.io/docs/start/) and [helm](https://helm.sh/docs/) via 
Docker; but can also be used with [other deployment tools](https://kubernetes.io/docs/tasks/tools/). 


## Deployment 
### Scripted Process
0. Clone [deployments](https://github.com/AnyLog-co/deployments/) directory  & login into our Docker hub.  
```shell
cd $HOME ; git clone https://github.com/AnyLog-co/deployments
bash $HOME/deployments/installations/docker_credentials.sh ${USER_PASSWORD}
```

### Manual Process  
0. Clone [deployments](https://github.com/AnyLog-co/deployments/) directory & login into our Docker hub.
```shell
cd $HOME ; git clone https://github.com/AnyLog-co/deployments
bash $HOME/deployments/installations/docker_credentials.sh ${USER_PASSWORD}
```
